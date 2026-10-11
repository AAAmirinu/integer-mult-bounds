from pathlib import Path
import argparse
parser=argparse.ArgumentParser();parser.add_argument('base',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args();BASE=args.base
"""Screen donor entrance at rank-one E with forced exact monotone label closure.
No candidate or scalar correctness claim; locality counts are full-path nominator.
"""
import sys,json,math,time
from collections import defaultdict,Counter
import common as C
c=json.loads(BASE.read_text());P=set(dict(c['ext']));pool=[r for r in range(240,1021) if r not in P];first=C.first_frames(c);dim=[len(b) for b in c['frames']];gates=[(g[1],C.gate_roles(g)) for ph in ['A','B'] for g in c[ph]];n=1021
es=sorted({c['frames'][first[r]][0] for r in pool if dim[first[r]]==1});alpha=.00101756;chi=lambda r:r*((73/r)**alpha-1) if r else 0
# Cache exact baseline rank and each role's previous frame for all chronological visits.
visits=[];cur=c['start'][:]
for f,rs in gates:
 visits.append((f,[(r,cur[r]) for r in rs]))
 for r in rs:cur[r]=f
finalold=cur[:]
def close(E,seeds):
 contains=[C.inside([E],bs) for bs in c['frames']];added=[False]*n;addedmass=[0]*n;delta=Counter({1:len(seeds)})
 # Initially forcing a rank1 donor touch changes each oldstart0 toE.
 for r in seeds:assert c['start'][r]==0;added[r]=True;addedmass[r]=1
 for f,rs in visits:
  need=not contains[f] and any(added[r] for r,o in rs)
  newdim=dim[f]+need
  for r,old in rs:
   olddim=dim[old]+addedmass[r]
   base=dim[f]-dim[old];actual=newdim-olddim
   assert actual>=0,(E,r,old,f,need,addedmass[r])
   if base:delta[base]-=1
   if actual:delta[actual]+=1
   added[r]=need;addedmass[r]=int(need)
 for r,f in enumerate(c['final']):
  if added[r] and not contains[f]:return None
  base=dim[f]-dim[finalold[r]];actual=base-addedmass[r]
  assert actual>=0
  if base:delta[base]-=1
  if actual:delta[actual]+=1
 return {r:k for r,k in delta.items() if k}
results={};t0=time.time()
for E in es:
 good=[]
 for r in pool:
  if C.inside([E],c['frames'][first[r]]):continue
  d=close(E,[r])
  if d is not None:good.append(dict(donor=r,delta=d,chi=sum(chi(k)*v for k,v in d.items())))
 results[E]=sorted(good,key=lambda z:z['chi']);print('VECTOR',E,'newlegal',len(good),'best',results[E][:3],flush=True)
 json.dump(results,open(args.output,'w'),indent=2)
print('seconds',time.time()-t0,flush=True)
