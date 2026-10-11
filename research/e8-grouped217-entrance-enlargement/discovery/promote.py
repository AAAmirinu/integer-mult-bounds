"""Exact acyclic donor-as-pivot nomination by PREPENDING a shear word.
Usage: python promote.py candidate781.json enlarged-selection.json output.json --pivot760
Full search omits --pivot; random basis ordering only nominates exact relations.
Later construction must verify actual chronological raw map and all local/outer obligations.
"""
import argparse,json,random
from pathlib import Path
from collections import defaultdict
from fractions import Fraction as Q
from types import SimpleNamespace
import common
parser=argparse.ArgumentParser();parser.add_argument('base',type=Path);parser.add_argument('selection',type=Path);parser.add_argument('output',type=Path);parser.add_argument('--pivot',type=int);parser.add_argument('--trials',type=int,default=300);args=parser.parse_args()
word=json.loads(args.base.read_text());plans=json.loads(args.selection.read_text())['plans'];Re=SimpleNamespace(inside=common.inside);first=common.first_frames(word);firstdim={r:len(word['frames'][f]) for r,f in first.items()}
rows=common.replay(word);K={p:{t:rows[t][p] for t in range(word['v'],2*word['v']) if p in rows[t]} for p in range(2*word['v'],2*word['v']+word['R'])}
P={z['pivot'] for p in plans for z in p['pivots']};D={d for p in plans for d in p['donors']};chains=defaultdict(list)
for p in plans:
 for d in p['donors']:
  if not any(Re.inside(p['basis'],e) and Re.inside(e,p['basis']) for e in chains[d]):chains[d].append(p['basis'])
pool=[r for r in K if r not in P];rng=random.Random(401399);alpha=.00101434
chi=lambda r:(r*(73/r)**alpha-r) if r else 0

def donorcost(r,bs):
 old=sorted({len(x) for x in chains[r]})+[firstdim[r]]
 new=sorted(set(old[:-1]+[len(bs)]))+[firstdim[r]]
 cost=lambda x:sum(chi(b-a) for a,b in zip([0]+x,x))
 return cost(new)-cost(old)
def solveone(target,ds):
 piv={}
 for r in ds:
  row=K[r].copy();co={r:Q(1)}
  while row:
   k=min(row);a=row[k]
   if k not in piv:piv[k]=({j:x/a for j,x in row.items()},{j:x/a for j,x in co.items()});break
   vv,cc=piv[k]
   for j,x in vv.items():
    z=row.get(j,0)-a*x
    if z:row[j]=z
    else:row.pop(j,None)
   for j,x in cc.items():
    z=co.get(j,0)-a*x
    if z:co[j]=z
    else:co.pop(j,None)
 want=K[target].copy();co={}
 while want:
  k=min(want);a=want[k]
  if k not in piv:return None
  vv,cc=piv[k]
  for j,x in vv.items():
   z=want.get(j,0)-a*x
   if z:want[j]=z
   else:want.pop(j,None)
  for j,x in cc.items():co[j]=co.get(j,0)-a*x
 return {j:q for j,q in co.items() if q}
results=[]
for p in sorted(D if args.pivot is None else D&{args.pivot}):
 es=sorted(chains[p],key=len);entry=es[0];kill=entry;ed=len(entry)
 allowed=[r for r in pool if r!=p and Re.inside(kill,word['frames'][first[r]]) and (r not in D or Re.inside(kill,min(chains[r],key=len)))]
 existing=[r for r in allowed if r in D];fresh=[r for r in allowed if r not in D]
 best=None
 for trial in range(args.trials):
  rng.shuffle(existing);rng.shuffle(fresh);cm=solveone(p,existing+fresh)
  if not cm or any(q.denominator not in (1,2) or abs(q.numerator)>4 for q in cm.values()):continue
  score=-chi(ed)+sum(donorcost(r,kill) for r in cm)
  if best is None or score<best['score']:best=dict(pivot=p,entry=entry,kill=kill,coefficients={r:str(q) for r,q in cm.items()},score=score)
 if best:
  results.append(best)
  if best['score']<0:print('GAIN',best,flush=True)
print('tested',len(D if args.pivot is None else D&{args.pivot}),'solutions',len(results),'positive',sum(x['score']<0 for x in results),flush=True)
json.dump(sorted(results,key=lambda x:x['score']),open(args.output,'w'),indent=2)
