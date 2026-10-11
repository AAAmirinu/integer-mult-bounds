"""Rank-one grouped entrances with free pivot and donor frame closure.
OpenAI Codex,2026-10-11. Raw relation and local profile discovery only.
Backward capacities include fixed retained snapshot labels and final endpoints.
"""
import sys,json,time,random,math,argparse
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parent))
import common as C
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('output',type=Path);ap.add_argument('--trials',type=int,default=100);args=ap.parse_args()
c=json.loads(args.base.read_text());n=2*c['v']+c['R'];P=set(dict(c['ext']));pool=[r for r in range(240,n) if r not in P]
dim=[len(f) for f in c['frames']];first=C.first_frames(c);alpha=.00101875;chi=lambda r:r*((73/r)**alpha-1) if r else 0;bank=.000615953010
rng=random.Random(215672);t0=time.time()
def span(bs):
 s={0}
 for x in bs:s|={y^x for y in s}
 return frozenset(s)
spans=[span(f) for f in c['frames']];cap=[spans[f] for f in c['final']]
for part in ['B','A']:
 if part=='A':
  for _,r,f in c['ret']:cap[r]=cap[r]&spans[f]
 for g in reversed(c[part]):
  roles=C.gate_roles(g);common=frozenset.intersection(*(cap[r] for r in roles))
  assert spans[g[1]]<=common
  for r in roles:cap[r]=common
assert all(spans[c['start'][r]]<=cap[r] for r in range(n))
json.dump({r:sorted(cap[r]) for r in pool},open(args.output.parent/'CAPACITIES.json','w'))
raw=C.replay(c);K={r:{t:raw[t][r] for t in range(120,240) if r in raw[t]} for r in pool};print('READY',time.time()-t0,flush=True)
def basis_dep(roles):
 piv={};deps=[];basis=[]
 for p in roles:
  row=K[p].copy();co={p:Q(1)}
  while row:
   k=min(row);a=row[k]
   if k not in piv:piv[k]=({j:x/a for j,x in row.items()},{j:x/a for j,x in co.items()});basis.append(p);break
   vv,cc=piv[k]
   for j,x in vv.items():
    z=row.get(j,0)-a*x
    if z:row[j]=z
    else:row.pop(j,None)
   for j,x in cc.items():
    z=co.get(j,0)-a*x
    if z:co[j]=z
    else:co.pop(j,None)
  if not row:
   cm={r:q for r,q in co.items() if r!=p};assert all(r in basis for r in cm)
   if cm and all(q.denominator in (1,2) and abs(q.numerator)<=4 for q in cm.values()):deps.append((p,cm))
 return deps

def closure_model(E,allowed):
 ids={r:1<<i for i,r in enumerate(allowed)};state=[ids.get(r,0) for r in range(n)];cur=c['start'][:];events=Counter()
 for part in ['A','B']:
  if part=='B':
   for _,r,f in c['ret']:assert state[r]==0 or E in spans[f]
  for g in c[part]:
   f=g[1];roles=C.gate_roles(g);new=0
   if E not in spans[f]:
    for r in roles:new|=state[r]
   for r in roles:
    if state[r] or new:events[dim[f]-dim[cur[r]],new,state[r]]+=1
    state[r]=new;cur[r]=f
 for r,f in enumerate(c['final']):
  assert state[r]==0 or E in spans[f]
  if state[r]:events[dim[f]-dim[cur[r]],0,state[r]]+=1
 events=list(events.items());cache={}
 def delta(seeds):
  mask=0
  for r in seeds:mask|=ids[r]
  if mask not in cache:
   hist=Counter({1:len(seeds)})
   for (rank,nxt,prev),cnt in events:
    newrank=rank+bool(mask&nxt)-bool(mask&prev)
    if rank!=newrank:
     if rank:hist[rank]-=cnt
     if newrank:hist[newrank]+=cnt
   cache[mask]={r:v for r,v in hist.items() if v}
  return cache[mask]
 return delta

results=[];tested=0
for E in range(1,512):
 allowed=[r for r in pool if E in cap[r]]
 if len(allowed)<2:continue
 close=closure_model(E,allowed);dc={r:sum(chi(k)*v for k,v in close([r]).items()) for r in allowed}
 def scored(deps):
  seeds={r for p,cm in deps for r in cm}|{p for p,cm in deps};h=close(seeds)
  return sum(chi(k)*v for k,v in h.items())-(chi(1)+bank)*len(deps)
 def fastscore(deps):
  seeds={r for p,cm in deps for r in cm}|{p for p,cm in deps}
  return sum(dc[r] for r in seeds)-(chi(1)+bank)*len(deps)
 local=None;seen=set()
 for tr in range(args.trials):
  rr=allowed[:];rng.shuffle(rr)
  if tr%4==1:rr.sort(key=lambda r:dc[r]+.003*rng.random())
  if tr%4==2:rr.sort(key=lambda r:dc[r]+.0003*rng.random())
  if tr%4==3:rr.sort(key=lambda r:dc[r]+.00003*rng.random())
  deps=basis_dep(rr);tested+=1
  if not deps:continue
  key=tuple(sorted((p,tuple(sorted(cm.items()))) for p,cm in deps))
  if key in seen:continue
  seen.add(key)
  # Exact greedy removal keeps shared-frame closure interactions in objective.
  best=scored(deps)
  while len(deps)>1:
   win=None
   for i in range(len(deps)):
    ss=scored(deps[:i]+deps[i+1:])
    if ss<best-1e-12:win=i;best=ss
   if win is None:break
   deps=deps[:win]+deps[win+1:]
  if local is None or best<local['score']:
   donors=sorted({r for p,cm in deps for r in cm});pivots={p for p,cm in deps};seeds=set(donors)|pivots;hist=Counter(close(seeds));hist[1]-=len(pivots)
   local=dict(basis=[E],score=best,local_delta={r:v for r,v in hist.items() if v},donors=donors,pivots=[dict(pivot=p,coefficients={r:str(q) for r,q in cm.items()}) for p,cm in deps],changed_pivot_firsts=sorted(p for p in pivots if E not in spans[first[p]]))
 if local:
  results.append(local)
  print('VECTOR',E,'score',local['score'],'gauges',len(local['pivots']),'newpivotframes',local['changed_pivot_firsts'],flush=True)
 json.dump(dict(results=sorted(results,key=lambda z:z['score']),tested=tested,seconds=time.time()-t0),open(args.output,'w'),indent=2)
print('DONE',tested,time.time()-t0,flush=True)
