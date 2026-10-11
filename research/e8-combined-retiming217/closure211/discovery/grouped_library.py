"""Grouped prepend search inspired by PR409 ordered batch promotion.
Uses frozen enlarged206 raw entrance word. No publication claim.
"""
import sys,json,random,time,copy
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
import common as C
c=json.loads(BASE.read_text());P=set(dict(c['ext']));pool=[r for r in range(240,1021) if r not in P];first=C.first_frames(c);dim={r:len(c['frames'][first[r]]) for r in pool};raw=C.replay(c);K={r:{t:raw[t][r] for t in range(120,240) if r in raw[t]} for r in pool};alpha=.001018666082678438
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

