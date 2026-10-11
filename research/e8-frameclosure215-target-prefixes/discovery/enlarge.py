"""Enumerate admissible strict entrance enlargements with frozen rational dependencies.
Usage: python enlarge.py candidate781.json selection205.json output.json
Candidate is only nominated by chi; reconstruct.py and full local/outer replay certify.
"""
import argparse,json,copy
from pathlib import Path
from collections import defaultdict
from types import SimpleNamespace
import common
parser=argparse.ArgumentParser();parser.add_argument('base',type=Path);parser.add_argument('selection',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args()
word=json.loads(args.base.read_text());plans=json.loads(args.selection.read_text())['plans'];Re=SimpleNamespace(inside=common.inside)
first=common.first_frames(word);firstdim={r:len(word['frames'][f]) for r,f in first.items()};alpha=.00101434
chi=lambda r:(r*(73/r)**alpha-r) if r else 0
from functools import lru_cache
@lru_cache(None)
def span(bs):
 z={0}
 for b in bs:z|={v^b for v in list(z)}
 return frozenset(z)
def canonical(vs):
 piv={}
 for x in sorted(vs,reverse=True):
  for k,y in sorted(piv.items(),reverse=True):
   if x>>k&1:x^=y
  if x:
   k=x.bit_length()-1
   for j,y in list(piv.items()):
    if y>>k&1:piv[j]^=x
   piv[k]=x
 return tuple(y for k,y in sorted(piv.items(),reverse=True))
def fullcost(plans):
 chains=defaultdict(list);v=0
 for pl in plans:
  d=len(pl['basis'])
  for p in pl['pivots']:v+=chi(firstdim[p['pivot']]-d)-chi(firstdim[p['pivot']])
  for r in pl['donors']:chains[r].append(pl['basis'])
 for r,es in chains.items():
  for a in es:
   for b in es:
    if not (Re.inside(a,b) or Re.inside(b,a)):return None
  ranks=sorted({len(e) for e in es})+[firstdim[r]]
  v+=sum(chi(b-a) for a,b in zip([0]+ranks,ranks))-chi(firstdim[r])
 return v
origcost=fullcost(plans);allwins=[]
for iteration in range(10):
 winner=None;cost=fullcost(plans)
 for i,pl in enumerate(plans):
  E=span(tuple(pl['basis']))
  for j,pp in enumerate(pl['pivots']):
   roles=[pp['pivot']]+[int(r) for r in pp['coefficients']]
   V=set.intersection(*(set(span(tuple(word['frames'][first[r]]))) for r in roles))
   if len(V)==len(E):continue
   levels={canonical(E)};front=list(levels)
   while front:
    a=front.pop()
    for v in V-set(span(a)):
     b=canonical(set(span(a))|{v})
     if b not in levels:levels.add(b);front.append(b)
   for bs in levels:
    if len(bs)<=len(pl['basis']):continue
    cand=copy.deepcopy(plans);pivot=cand[i]['pivots'].pop(j)
    if cand[i]['pivots']:cand[i]['donors']=sorted({int(r) for p in cand[i]['pivots'] for r in p['coefficients']})
    else:cand.pop(i)
    cand.append(dict(basis=list(bs),ed=len(bs),donors=sorted(int(r) for r in pivot['coefficients']),pivots=[pivot]))
    cst=fullcost(cand)
    if cst is not None and cst<cost-1e-12 and (winner is None or cst<winner[0]):winner=(cst,cand,i,j,pl['basis'],list(bs),pp['pivot'])
 if winner is None:print('NO FURTHER',iteration,'score',cost,'initial',origcost,flush=True);break
 cost,plans,i,j,a,b,p=winner
 print('ENLARGE',iteration,'pivot',p,'old',a,'new',b,'cost',cost,'gain',origcost-cost,flush=True)
 allwins.append(dict(pivot=p,old=a,new=b,cost=cost))
 json.dump(dict(plans=plans,changes=allwins),open(args.output,'w'),indent=2)
