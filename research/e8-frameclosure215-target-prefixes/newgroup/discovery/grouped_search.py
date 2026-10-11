"""Grouped prepend search inspired by PR409 ordered batch promotion.
Uses supplied enlarged206 raw entrance word. Adds explicit normalization LP marginal to local paid moment; no publication claim.
"""
import sys,json,random,time,copy
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
import argparse,common as C
parser=argparse.ArgumentParser();parser.add_argument('base',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
c=json.loads(args.base.read_text());P=set(dict(c['ext']));pool=[r for r in range(240,1021) if r not in P];first=C.first_frames(c);dim={r:len(c['frames'][first[r]]) for r in pool};raw=C.replay(c);K={r:{t:raw[t][r] for t in range(120,240) if r in raw[t]} for r in pool};alpha=.001018666082678438
chi=lambda r:r*((73/r)**alpha-1) if r else 0
rng=random.Random(409206)
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

def score(deps,d):
 D={r for p,cm in deps for r in cm}
 return sum(chi(dim[p]-d)-chi(dim[p]) for p,cm in deps)+sum(chi(d)+chi(dim[r]-d)-chi(dim[r]) for r in D)-.000615953010*d*len(deps)
def prune(deps,d):
 best=score(deps,d)
 while len(deps)>1:
  winner=None
  for i in range(len(deps)):
   trial=deps[:i]+deps[i+1:];s=score(trial,d)
   if s<best-1e-12:best=s;winner=i
  if winner is None:break
  deps=deps[:winner]+deps[winner+1:]
 return deps

results=[];best=None;tested=0;t0=time.time()
for e in range(1,512):
 allowed=[r for r in pool if C.inside([e],c['frames'][first[r]])]
 if len(allowed)<2:continue
 localbest=None
 for tr in range(200):
  rr=allowed[:];rng.shuffle(rr)
  if tr%2:rr.sort(key=lambda r:dim[r],reverse=True)
  deps=prune(basis_dep(rr),1);tested+=1
  if not deps:continue
  s=score(deps,1)
  if localbest is None or s<localbest['score']:
   localbest=dict(basis=[e],score=s,donors=sorted({r for p,cm in deps for r in cm}),pivots=[dict(pivot=p,coefficients={r:str(q) for r,q in cm.items()}) for p,cm in deps])
 if localbest:
  results.append(localbest)
  if localbest['score']<0:print('PROFIT',e,len(localbest['pivots']),len(localbest['donors']),localbest['score'],flush=True)
  if best is None or localbest['score']<best['score']:
   best=localbest;print('BEST',e,len(best['pivots']),len(best['donors']),best['score'],flush=True)
 json.dump(dict(results=sorted(results,key=lambda z:z['score']),best=best,tested=tested),open(args.output,'w'),indent=2)
print('FINISHED',tested,'seconds',time.time()-t0,flush=True)
