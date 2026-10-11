"""Optional deterministic shared-donor selection search, Python stdlib only.
OpenAI Codex adaptation of the recorded 205-pivot search; PR401/404 exact
response constructor and notices remain in force. Discovery score is heuristic;
verify.py and the frozen selection supply the correctness certificate.
Run: python -B research-notes/discover205.py /absolute/new-selection.json
"""
import sys
sys.dont_write_bytecode=True
import argparse,importlib.util,json,random,math
from pathlib import Path
from fractions import Fraction as Q
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('output',type=Path);ap.add_argument('--rounds',type=int,default=10);args=ap.parse_args();assert not args.output.exists()
s=importlib.util.spec_from_file_location('Re',ROOT/'frames/reconstruct.py');Re=importlib.util.module_from_spec(s);s.loader.exec_module(Re)
word=json.loads((ROOT/'inputs/candidate781.json').read_text());rows=Re.replay(word)
K={p:{t:rows[t][p] for t in range(120,240) if p in rows[t]} for p in range(240,1021)}
first=Re.first_frames(word);firstdim={r:len(word['frames'][first[r]]) for r in range(240,1021)}
plans=json.loads((ROOT/'shared/selection194.json').read_text())['plans']
alpha=.00101434;chi=lambda r:(r*(73/r)**alpha-r) if r else 0
rng=random.Random(401399);forbidden=set()

def basis_dep(roles):
 piv={};deps=[];basis=[]
 for p in roles:
  row=K[p].copy();co={p:Q(1)}
  while row:
   k=min(row);a=row[k]
   if k not in piv:
    row={j:x/a for j,x in row.items()};co={j:x/a for j,x in co.items()};piv[k]=(row,co);basis.append(p);break
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
   if p not in forbidden and cm and all(q.denominator in (1,2) for q in cm.values()) and max(abs(q.numerator) for q in cm.values())<=4:deps.append((p,cm))
 return deps

def fromdeps(pl,deps):
 return dict(basis=pl['basis'],ed=pl['ed'],donors=sorted({r for p,cm in deps for r in cm}),pivots=[dict(pivot=p,coefficients={str(r):str(q) for r,q in cm.items()}) for p,cm in deps])

def donorcost(r,bs):
 old=sorted({len(x) for x in chains[r]})+[firstdim[r]]
 new=sorted(set(old[:-1]+[len(bs)]))+[firstdim[r]]
 cost=lambda x:sum(chi(b-a) for a,b in zip([0]+x,x))
 return cost(new)-cost(old)
def score2(pl):
 d=len(pl['basis']);return sum(chi(firstdim[p['pivot']]-d)-chi(firstdim[p['pivot']]) for p in pl['pivots'])+sum(donorcost(r,pl['basis']) for r in pl['donors'])
def prune2(pl,deps):
 best=fromdeps(pl,deps);bs=score2(best)
 while len(deps)>1:
  winner=None
  for i in range(len(deps)):
   dd=deps[:i]+deps[i+1:];ss=score2(fromdeps(pl,dd))
   if ss<bs-1e-12:winner=i;bs=ss
  if winner is None:break
  deps=deps[:winner]+deps[winner+1:]
 return fromdeps(pl,deps)

def attempt(bs,trials):
 allowed=[r for r in pool if Re.inside(bs,word['frames'][first[r]]) and all(Re.inside(e,bs) or Re.inside(bs,e) for e in chains[r])]
 if not any(r not in D for r in allowed):return None
 donor=[r for r in allowed if r in D];free=[r for r in allowed if r not in D];best=None
 for trial in range(trials):
  rng.shuffle(donor);rng.shuffle(free)
  if trial%2:free.sort(key=lambda r:firstdim[r],reverse=True)
  deps=basis_dep(donor+free)
  if not deps:continue
  pl=prune2(dict(basis=bs,ed=len(bs)),deps)
  if best is None or score2(pl)<score2(best):best=pl
 return best

def setup(current):
 global P,D,chains,forbidden,pool,available,contain
 P={z['pivot'] for p in current for z in p['pivots']};D={d for p in current for d in p['donors']};chains=defaultdict(list)
 for p in current:
  for d in p['donors']:
   if not any(Re.inside(p['basis'],e) and Re.inside(e,p['basis']) for e in chains[d]):chains[d].append(p['basis'])
 forbidden=P|D
 pool=[r for r in range(240,1021) if r not in P];available=[r for r in pool if r not in D];contain={r:{0} for r in pool}
 for r in pool:
  for b in word['frames'][first[r]]:contain[r]|={x^b for x in list(contain[r])}


for iteration in range(args.rounds):
 order=list(range(len(plans)));rng.shuffle(order);changes=0
 for i in order:
  current=plans[:i]+plans[i+1:];setup(current);pl=plans[i];base_score=score2(pl);z=attempt(pl['basis'],200)
  if z and score2(z)<base_score-1e-12:
   print('IMPROVE',iteration,i,pl['basis'],'oldpiv',len(pl['pivots']),'newpiv',len(z['pivots']),'oldscore',base_score,'newscore',score2(z),flush=True);plans[i]=z;changes+=1
 print('ROUND',iteration,'changes',changes,'pivots',sum(len(p['pivots']) for p in plans),flush=True)
 json.dump(dict(plans=plans),args.output.open('w'),indent=2)
 if not changes and iteration>2:break
