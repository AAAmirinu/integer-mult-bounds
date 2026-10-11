"""Nominate and realize whole-owner patterns for an explicit atomic call order.

The MILP uses floating objectives only for discovery. Every selected integer
constraint is checked exactly, then a literal role map is edge-colored and
independently admitted elsewhere. No solver optimality claim is made.
"""
from pathlib import Path
from collections import Counter,defaultdict
import gzip,json,itertools,math,sys,time,importlib.util
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix,csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching

base,planfile,out=map(Path,sys.argv[1:4]);assert not out.exists();out.mkdir()
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
plan=read(planfile);canon=read(base/'split-centres/CANONICAL-WORD.json.gz');checks=read(base/'split-centres/LOCAL-CHECKS.json')
ws=(5,7,8,9);helpers=defaultdict(list)
for h in range(560):helpers[9-len(canon['frames'][canon['start'][240+h]])].append(h)
quota={w:len(helpers[w])for w in ws}
groups={tuple(map(int,k.split(','))):(int(v[0]),tuple(v[1]))for k,v in plan['windows'].items()}

def patterns(rank,n):
 return [v for v in itertools.product(*(range(rank//w+1)for w in ws))if sum(v)<=n and sum(a*w for a,w in zip(v,ws))<=rank]

class Model:
 def __init__(self):self.names=[];self.cost=[];self.bounds=[];self.entries=[];self.lows=[];self.highs=[]
 def var(self,name,cost=0,bound=120):
  i=len(self.names);self.names.append(name);self.cost.append(cost);self.bounds.append(bound);return i
 def row(self,terms,lo,hi=None):
  i=len(self.lows);self.lows.append(lo);self.highs.append(lo if hi is None else hi)
  self.entries.extend((i,j,v)for j,v in terms.items()if v)
 def solve(self,label):
  rr,cc,vv=zip(*self.entries);A=coo_matrix((vv,(rr,cc)),shape=(len(self.lows),len(self.names))).tocsc()
  print('SOLVE',label,A.shape,A.nnz,flush=True);start=time.monotonic()
  r=milp(np.array(self.cost),integrality=np.ones(len(self.names)),bounds=Bounds(np.zeros(len(self.names)),np.array(self.bounds)),constraints=LinearConstraint(A,np.array(self.lows),np.array(self.highs)),options={'time_limit':180,'mip_rel_gap':0.0000001})
  report=dict(status=int(r.status),message=r.message,seconds=time.monotonic()-start,objective=None if r.fun is None else float(r.fun),variables=len(self.names),constraints=len(self.lows))
  (out/(label+'-SOLVER.json')).write_text(json.dumps(report,indent=2)+'\n')
  assert r.x is not None,report
  x=np.rint(r.x).astype(np.int64);assert np.max(np.abs(r.x-x))<1e-5
  assert all(0<=int(v)<=b for v,b in zip(x,self.bounds))
  sums=[0]*len(self.lows)
  for row,col,v in self.entries:sums[row]+=int(v)*int(x[col])
  assert all(lo<=s<=hi for s,lo,hi in zip(sums,self.lows,self.highs))
  print('EXACT_INTEGER_FEASIBLE',label,report,flush=True)
  return x

def objective(r):return r*math.log(73/r)if r else 0

# Aggregate patterns and call/width flows. This first nomination may require
# repair because each individual pattern copy may serve a call only once.
m=Model();xp={};yg={};supply=defaultdict(dict);demand=defaultdict(dict)
for g,(rank,times)in groups.items():
 for p in patterns(rank,len(times)):
  xp[g,p]=m.var(('x',g,p),objective(rank-sum(a*w for a,w in zip(p,ws))))
 m.row({v:1 for (gg,p),v in xp.items()if gg==g},120)
 for t in times:
  row={}
  for w in ws:
   if w>rank:continue
   j=m.var(('y',g,t,w));yg[g,t,w]=j;row[j]=1;supply[g,w][j]=1;demand[t,w][j]=1
  m.row(row,0,120)
 for wi,w in enumerate(ws):
  row=dict(supply[g,w]);row.update({j:-p[wi]for (gg,p),j in xp.items()if gg==g and p[wi]})
  m.row(row,0)
for t in range(72):
 for w in ws:m.row(demand[t,w],quota[w])
x=m.solve('aggregate')
selected={g:[p for (gg,p),j in xp.items()if gg==g and x[j]]for g in groups}
(out/'AGGREGATE.json').write_text(json.dumps([dict(group=g,pattern=p,count=int(x[j]))for(g,p),j in xp.items()if x[j]],indent=2)+'\n')

# Repair with explicit per-pattern/call capacities. Counts may change among
# nominated patterns; all actual pattern copies must now have a realizable
# coloring. This is sufficient for the independent whole-family construction.
m=Model();xp={};yp={};demand=defaultdict(dict)
for g,(rank,times)in groups.items():
 for p in selected[g]:
  j=m.var(('x',g,p),objective(rank-sum(a*w for a,w in zip(p,ws))));xp[g,p]=j
  supply=defaultdict(dict)
  for t in times:
   cap={j:-1}
   for wi,w in enumerate(ws):
    if not p[wi]:continue
    y=m.var(('y',g,p,t,w));yp[g,p,t,w]=y;supply[w][y]=1;demand[t,w][y]=1;cap[y]=1
   m.row(cap,-120,0)
  for wi,w in enumerate(ws):
   if p[wi]:m.row(dict(supply[w])|{j:-p[wi]},0)
 m.row({j:1 for(gg,p),j in xp.items()if gg==g},120)
for t in range(72):
 for w in ws:m.row(demand[t,w],quota[w])
x=m.solve('pattern-capacities')
(out/'PATTERN-FLOW.json').write_text(json.dumps([dict(group=g,pattern=p,count=int(x[j]),flow=[[t,w,int(x[y])]for(gg,pp,t,w),y in yp.items()if gg==g and pp==p and x[y]])for(g,p),j in xp.items()if x[j]],indent=2)+'\n')

roles=[];ports=Counter();paid=Counter();nexthelper={(t,w):iter(helpers[w])for t in range(72)for w in ws}
for (g,p),j in xp.items():
 count=int(x[j])
 if not count:continue
 rank,times=groups[g];owrep,child=g;slots=[w for w,n in zip(ws,p)for _ in range(n)]
 # Regular bipartite multigraph: left = width slots, right = eligible calls.
 # Every real left vertex has degree count. Fill only dummy rows to regularize;
 # count perfect matchings then give count actual physical-port assignments.
 n=max(len(slots),len(times));a=np.zeros((n,n),dtype=np.int64)
 for w in ws:
  rows=[i for i,v in enumerate(slots)if v==w];ri=0
  for ti,t in enumerate(times):
   left=int(x[yp[g,p,t,w]])if(g,p,t,w)in yp else 0
   while left:
    r=rows[ri];take=min(left,count-int(a[r].sum()));a[r,ti]+=take;left-=take
    if int(a[r].sum())==count:ri+=1
  assert ri==len(rows)
 assert all(int(a[i].sum())==count for i in range(len(slots)))
 assert max(a.sum(axis=0),default=0)<=count
 for i in range(len(slots),n):
  need=count
  for ti in range(n):
   take=min(need,count-int(a[:,ti].sum()));a[i,ti]+=take;need-=take
   if not need:break
  assert not need
 assert np.all(a.sum(axis=0)==count)and np.all(a.sum(axis=1)==count)
 for color in range(count):
  assignment=maximum_bipartite_matching(csr_matrix(a>0),perm_type='column');assert np.all(assignment>=0)
  port=ports[g];ports[g]+=1;off=0
  for ri,ti in enumerate(assignment):
   assert a[ri,ti]>0;a[ri,ti]-=1
   if ri>=len(slots):continue
   t=times[ti];w=slots[ri];stage,rep=plan['order'][t];h=next(nexthelper[t,w])
   family=owrep*960+(2*plan['pairs'][str(child)]+plan['sides'][str(child)])*120+port
   roles.append(dict(child=child,copy=owrep*120+port,family=family,helper=h,offset=off,owner_replica=owrep,port=port,replica=rep,stage=stage,time=t,width=w));off+=w
  left=rank-off
  if left:paid[left]+=1
 assert not a.any()
assert all(n==120 for n in ports.values())and len(roles)==40320
for t in range(72):
 call=[z for z in roles if z['time']==t];assert len(call)==560 and len({z['helper']for z in call})==560 and len({z['family']for z in call})==560
for stage,rep in plan['order']:
 # Orientation counts are balanced in the pinned nine-stage template.
 parent=read(base/'split-centres/GLOBAL-TEMPLATE.json.gz')
 call=next(c for c in parent['calls']if(c['stage'],c['replica'])==(stage,rep))
 paid.update({int(k):v for k,v in checks[call['orientation']]['paid_profile'].items()})
assert 73*7680-sum(r*n for r,n in paid.items())==2496 and max(paid)<=48
roles.sort(key=lambda z:(z['time'],z['helper']));plan['profile']=dict(sorted(paid.items()));plan['baseline_widths']=[9-len(canon['frames'][canon['start'][240+h]])for h in range(560)]
(out/'OWNERS.json.gz').write_bytes(gzip.compress(json.dumps(roles,separators=(',',':')).encode(),mtime=0))
(out/'PLAN.json').write_text(json.dumps(plan,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('moment',base/'work/pr361/code/engines/moment.py');engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
price=engine.certify(dict(paid),73,7680,True)
(out/'NOMINATION.json').write_text(json.dumps(dict(status='NOMINATION_EXACT_INTEGER_PATTERN_FLOW_AND_LITERAL_OWNERS',profile=dict(sorted(paid.items())),price=price,scope='New literal matching and exact price; physical/controller/invoice admission is separate.'),indent=2)+'\n');print('NOMINATION',price['lower'],flush=True)
