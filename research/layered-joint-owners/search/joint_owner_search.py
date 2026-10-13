"""Bounded two-call owner nomination, with full integer footprint checks.
The optimizer is discovery only. A nomination needs fresh global admission.
"""
from pathlib import Path
from collections import Counter, defaultdict, deque
import argparse, gzip, hashlib, itertools, json, math, os, time
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_matrix

# Optional discovery only. Verification never imports NumPy, SciPy, or this file.
PKG=Path(os.environ['GAUGE44_PARENT']).resolve()
read=lambda p:json.loads(gzip.decompress(p.read_bytes()) if p.suffix=='.gz' else p.read_bytes())
packed=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def rate(profile):
 lo,hi=0.,.02
 for _ in range(60):
  b=(lo+hi)/2
  if sum(n*r*math.expm1(b*math.log(73/r)) for r,n in profile.items())<2560:lo=b
  else:hi=b
 return lo

class Instance:
 def __init__(self, owners=None):
  self.plan=read(PKG/'data/PLAN.json');self.roles=read(owners or PKG/'data/OWNERS.json.gz')
  self.sig=self.plan['provider_registry']['gauge44'];self.widths=self.sig['widths'];assert Counter(self.widths)=={4:52,5:48,7:42,8:116,9:234}
  self.caps={};self.eligible=defaultdict(set);self.families={}
  for key,(cap,times) in self.plan['windows'].items():
   rep,ch=map(int,key.split(','))
   for port in range(112):
    g=rep,ch,port;self.caps[g]=cap
    self.families[g]=rep*896+(2*self.plan['pairs'][str(ch)]+self.plan['sides'][str(ch)])*112+port
    for t in times:self.eligible[t].add(g)
  self.used=Counter();self.bycall=defaultdict(dict)
  for z in self.roles:
   g=z['owner_replica'],z['child'],z['port'];self.used[g]+=z['width'];self.bycall[z['time']][z['helper']]=(g,z['width'])
  self.baseline=self.check(self.roles)
 def check(self,roles):
  used=defaultdict(set);seen=defaultdict(set);fams=defaultdict(set)
  for z in roles:
   t,h=z['time'],z['helper'];s,rep=self.plan['order'][t];g=z['owner_replica'],z['child'],z['port'];w=self.widths[h]
   assert (z['stage'],z['replica'])==(s,rep) and z['width']==w and h not in seen[t];seen[t].add(h)
   assert g in self.eligible[t] and z['family']==self.families[g] and z['copy']==g[0]*112+g[2]
   assert z['family'] not in fams[t];fams[t].add(z['family'])
   assert not(g[0]==rep and self.plan['pairs'][str(g[1])]==max(0,(s-1)//2))
   cells=set(range(z['offset'],z['offset']+w));assert z['offset']>=0 and z['offset']+w<=self.caps[g] and not cells&used[g];used[g]|=cells
  assert len(roles)==72*492 and all(seen[t]==set(range(492)) for t in range(72))
  assert all(v==set(range(len(v))) for v in used.values())
  idle=Counter(self.caps[g]-len(used[g]) for g in self.caps if self.caps[g]>len(used[g]))
  profile=Counter({int(r):72*n for r,n in self.sig['actual_paid_profile'].items()});profile.update(idle)
  assert sum(r*n for r,n in profile.items())==520704 and 73*7168-520704==2560
  return {'idle':dict(sorted(idle.items())),'profile':dict(sorted(profile.items())),'b':rate(profile)}
 def model(self,a,b):
  gs=self.eligible[a]|self.eligible[b];buckets=defaultdict(list)
  olda={g:w for g,w in self.bycall[a].values()};oldb={g:w for g,w in self.bycall[b].values()}
  for g in sorted(gs):
   c=self.caps[g]-self.used[g]+olda.get(g,0)+oldb.get(g,0)
   typ=int(g in self.eligible[a])+2*int(g in self.eligible[b]);buckets[c,typ].append(g)
  cats=sorted(buckets);widths=sorted(set(self.widths));columns=[];row=[];col=[];val=[];obj=[];ub=[]
  constraints=[len(buckets[x]) for x in cats]+[Counter(self.widths)[w] for _ in range(2) for w in widths]
  equalrows=len(constraints)
  oldres=[self.caps[g]-self.used[g] for g in gs]
  constraints.extend(sum(max(r-k,0) for r in oldres) for k in range(1,48))
  for ci,(c,typ) in enumerate(cats):
   for wa in ([0]+widths if typ&1 else [0]):
    for wb in ([0]+widths if typ&2 else [0]):
     if wa+wb>c:continue
     j=len(columns);columns.append((ci,wa,wb));row.append(ci);col.append(j);val.append(1)
     for side,w in enumerate((wa,wb)):
      if w:row.append(len(cats)+side*len(widths)+widths.index(w));col.append(j);val.append(1)
     r=c-wa-wb
     for k in range(1,48):
      if r>k:row.append(equalrows+k-1);col.append(j);val.append(r-k)
     # Minimize exact same scalar pressure, scaled for solver conditioning.
     obj.append((r*math.expm1(.0016522089943684118*math.log(73/r)) if r else 0)*1e6);ub.append(len(buckets[c,typ]))
  A=coo_matrix((val,(row,col)),shape=(len(constraints),len(columns))).tocsc()
  return cats,buckets,columns,np.asarray(obj),np.asarray(ub),A,np.asarray(constraints),equalrows
 def solve(self,a,b,seconds):
  cats,buckets,columns,obj,ub,A,rhs,equalrows=self.model(a,b);start=time.monotonic()
  upper=np.concatenate((rhs[:equalrows],np.full(len(rhs)-equalrows,np.inf)))
  res=milp(obj,integrality=np.ones(len(obj)),bounds=Bounds(np.zeros(len(obj)),ub),constraints=LinearConstraint(A,rhs,upper),options={'time_limit':seconds,'mip_rel_gap':0.0,'threads':1})
  report={'pair':[a,b],'calls':[self.plan['order'][a],self.plan['order'][b]],'status':int(res.status),'message':str(res.message),'seconds':time.monotonic()-start,'variables':len(obj),'buckets':len(cats)}
  if res.x is None:return report,None
  x=np.rint(res.x).astype(np.int64);assert np.max(np.abs(res.x-x))<1e-5 and np.all((A@x)[:equalrows]==rhs[:equalrows]) and np.all((A@x)[equalrows:]>=rhs[equalrows:]) and np.all(x>=0) and np.all(x<=ub)
  report.update({'integer_equations_checked':True,'mip_gap':float(res.mip_gap),'mip_nodes':int(res.mip_node_count)})
  assigned={a:defaultdict(list),b:defaultdict(list)}
  choices=defaultdict(Counter)
  for count,(ci,wa,wb) in zip(x,columns):choices[ci][wa,wb]+=int(count)
  oldmaps={t:{g:(h,w) for h,(g,w) in self.bycall[t].items()} for t in (a,b)}
  for ci,key in enumerate(cats):
   pending=[]
   for g in buckets[key]:
    pair=tuple(oldmaps[t].get(g,(None,0))[1] for t in (a,b))
    if choices[ci][pair]:choices[ci][pair]-=1
    else:pending.append(g);continue
    for t,w in zip((a,b),pair):
     if w:assigned[t][w].append(g)
   left=deque(pair for pair,n in sorted(choices[ci].items()) for _ in range(n))
   assert len(left)==len(pending)
   for g in pending:
    pair=left.popleft()
    for t,w in zip((a,b),pair):
     if w:assigned[t][w].append(g)
  assert all(sum(len(v) for v in assigned[t].values())==492 for t in (a,b))
  roles=[dict(z) for z in self.roles if z['time'] not in (a,b)]
  for t in (a,b):
   s,rep=self.plan['order'][t]
   nominated={};available={w:set(gs) for w,gs in assigned[t].items()}
   for h,(g,w) in sorted(self.bycall[t].items()):
    if g in available[w]:available[w].remove(g);nominated[h]=g
   for h,w in enumerate(self.widths):
    if h not in nominated:g=min(available[w]);available[w].remove(g);nominated[h]=g
    g=nominated[h];orp,ch,port=g
    roles.append(dict(child=ch,copy=orp*112+port,family=self.families[g],helper=h,offset=0,owner_replica=orp,port=port,replica=rep,stage=s,time=t,width=w))
   assert not any(available.values())
  groups=defaultdict(list)
  for z in roles:groups[z['owner_replica'],z['child'],z['port']].append(z)
  for g,zs in groups.items():
   off=0
   for z in sorted(zs,key=lambda z:(z['time'],z['helper'])):z['offset']=off;off+=z['width']
  roles.sort(key=lambda z:(z['time'],z['helper']))
  checked=self.check(roles);report['candidate']=checked;report['gain_b']=checked['b']-self.baseline['b']
  old=Counter(self.baseline['idle']);new=Counter(checked['idle']);ks=list(range(49))
  margins=[sum(n*max(r-k,0) for r,n in new.items())-sum(n*max(r-k,0) for r,n in old.items()) for k in ks]
  assert margins[0]==margins[-1]==0
  report['integer_stoploss_margins']=margins;report['strict_majorization']=min(margins)>=0 and max(margins)>0
  return report,roles

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--owners',type=Path);ap.add_argument('--pairs',type=int,default=50);ap.add_argument('--seconds',type=float,default=5);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 inst=Instance(a.owners);scores=[]
 for x,y in itertools.combinations(range(72),2):
  common=inst.eligible[x]&inst.eligible[y]
  score=sum(1 for g in common if 0<inst.caps[g]-inst.used[g]<inst.caps[g])
  scores.append((score,x,y))
 reports=[];best=inst.baseline['b'];beg=time.monotonic()
 for _,x,y in sorted(scores,reverse=True)[:a.pairs]:
  report,roles=inst.solve(x,y,a.seconds);reports.append(report)
  print(json.dumps({k:report[k] for k in ('pair','status','seconds','gain_b','strict_majorization') if k in report}),flush=True)
  if roles is not None and report['candidate']['b']>best+1e-16:
   best=report['candidate']['b'];raw=packed(roles);(a.out/'BEST-OWNERS.json.gz').write_bytes(gzip.compress(raw,mtime=0));(a.out/'BEST-RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
  result={'status':'BOUNDED_TWO_CALL_NOMINATION_SEARCH','source_head':'3e669dc7987cb2295a71664b77e110c0cd979a87','source_plan_sha256':sha(PKG/'data/PLAN.json'),'source_owners_sha256':sha(PKG/'data/OWNERS.json.gz'),'baseline':inst.baseline,'pairs_requested':a.pairs,'pairs_checked':len(reports),'per_pair_time_limit':a.seconds,'reports':reports,'best_b':best,'seconds':time.monotonic()-beg,'scope':'Discovery only. Every returned integer owner nomination passes capacity/window/active-family/unique-helper/compacted-footprint checks. Requires fresh provider/global phase/finite invoice/moment/outer admission.'}
  (a.out/'SEARCH.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
