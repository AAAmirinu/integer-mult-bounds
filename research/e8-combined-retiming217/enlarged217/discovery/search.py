"""Exact local profile search for existing-gauge capacity enlargements."""
from pathlib import Path
import sys,json,math,copy
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parent))
import common as C
import argparse
ap=argparse.ArgumentParser();ap.add_argument('base',type=Path);ap.add_argument('capacities',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args()
c=json.loads(args.base.read_text())
caps={int(r):frozenset(s) for r,s in json.loads(args.capacities.read_text()).items()}
alpha=.00101875;chi=lambda r:r*((73/r)**alpha-1) if r else 0;bank=.000615953010
def span(bs):
 s={0}
 for x in bs:s|={y^x for y in s}
 return frozenset(s)
def basis(ss):
 piv={}
 for x in sorted(ss,reverse=True):
  for k,y in sorted(piv.items(),reverse=True):
   if x>>k&1:x^=y
  if x:
   k=x.bit_length()-1
   for j,y in list(piv.items()):
    if y>>k&1:piv[j]^=x
   piv[k]=x
 return [y for k,y in sorted(piv.items(),reverse=True)]
spans=[span(f) for f in c['frames']]
def closure(p,F):
 flags=[False]*len(c['start']);flags[p]=True;cur=c['start'][:];dim=list(map(len,c['frames']));miss=[len(basis(F|S))-dim[i] for i,S in enumerate(spans)];h=Counter();changes=[]
 for part in ['A','B']:
  if part=='B':
   for _,r,f in c['ret']:assert not flags[r] or not miss[f]
  for i,g in enumerate(c[part]):
   f=g[1];rs=C.gate_roles(g);new=bool(miss[f] and any(flags[r] for r in rs))
   if new:changes.append((part,i,f,basis(F|spans[f])))
   for r in rs:
    old=cur[r];base=dim[f]-dim[old];rank=base+new*miss[f]-flags[r]*miss[old]
    assert rank>=0
    if base:h[base]-=1
    if rank:h[rank]+=1
    flags[r]=new;cur[r]=f
 for r,f in enumerate(c['final']):
  assert not flags[r] or not miss[f]
  base=dim[f]-dim[cur[r]];rank=base-flags[r]*miss[cur[r]]
  assert rank>=0
  if base:h[base]-=1
  if rank:h[rank]+=1
 return {r:n for r,n in h.items() if n},changes
results=[]
for p,f in c['ext']:
 S=spans[f];seen=set()
 for E in sorted(caps[p]-S):
  F=S|frozenset(E^x for x in S)
  if F in seen:continue
  seen.add(F);hist,changes=closure(p,F);score=sum(chi(k)*v for k,v in hist.items())-bank
  results.append(dict(pivot=p,old=c['frames'][f],basis=basis(F),local_delta=hist,changes=changes,score=score))
results.sort(key=lambda x:x['score']);json.dump(results,open(args.output,'w'),indent=2)
for x in results[:15]:print(x,flush=True)
