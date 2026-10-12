"""Float objectives and modular elimination nominate; exact G.build admits structure.
Scores the actual local frame increments plus an optimistic whole-helper packing
LP. No floating objective or modular relation is a certificate.
"""
from pathlib import Path
from collections import Counter
import copy,gzip,json,random,sys,time,math,itertools
import numpy as np
from scipy.optimize import linprog
root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent/'refine518';here.mkdir(exist_ok=True)
sys.path.insert(0,str(root/'e8-partial-collapse-release/research/partial-own-coordinated-asynchronous/vendor/pr507/vendor/complex/e8-complex-gauge-kernel/code'));import gk_word as G
base=json.load(gzip.open(Path('/private/tmp/pr518-macos-fresh/base/split-centres/RETIMED-BASE.json.gz')));reference=json.loads((root/'resume-20261011/pr518/research/nodal-pair-async/inputs/PAIR-SELECTION.json').read_text());cols=G.responses(base);first=G.first_frames(base);prime=1000003;mod=[{t:int(x.numerator)*pow(int(x.denominator),-1,prime)%prime for t,x in c.items()}for c in cols]
initial=set(range(560))-set(map(int,reference['gauge']));groups={e:{h for h in initial if e in G.span(first[h])}for e in range(1,512)};groups={e:hs for e,hs in groups.items()if len(hs)>1}
stock={8:5760,16:3840,32:3840,48:3840};ws=[7,8,9];patterns=[]
for r in stock:
 for p in itertools.product(*(range(r//w+1)for w in ws)):
  left=r-sum(w*n for w,n in zip(ws,p))
  if left>=0:patterns.append((r,p,left))
f=lambda r:r*math.log(73/r)if r else 0
A=np.array([[int(rr==r)for r,p,left in patterns]for rr in stock]+[[p[i]for r,p,left in patterns]for i in range(3)],float);cost=np.array([f(left)for r,p,left in patterns]);phi={}
for n in range(161):
 rhs=np.array([stock[r]for r in stock]+[18*72,(62+n)*72,(480-n)*72],float);r=linprog(cost,A_eq=A,b_eq=rhs,bounds=(0,None),method='highs');assert r.success;phi[n]=r.fun
no_kernel=G.build(base,dict(gauge=reference['gauge']));baseP=G.profile(no_kernel)
def score(P,n):return 72*sum(f(int(r))*x for r,x in P.items())+phi[n]
refscore=score(G.profile(G.build(base,reference)),99);best=refscore;cache={}
def split(hs):
 basis={};ds=[];ps=[];used=set()
 for h in hs:
  v=dict(mod[h]);combo={}
  while v:
   t=min(v)
   if t not in basis:
    q=pow(v[t],-1,prime);rep={j:-c*q%prime for j,c in combo.items()};rep[h]=q;basis[t]=({k:x*q%prime for k,x in v.items()},rep);ds.append(h);break
   q=v[t];row,rep=basis[t]
   for k,x in row.items():
    z=(v.get(k,0)-q*x)%prime
    if z:v[k]=z
    else:v.pop(k,None)
   for d,x in rep.items():
    z=(combo.get(d,0)+q*x)%prime
    if z:combo[d]=z
    else:combo.pop(d,None)
  if not v:ps.append(h);used.update(combo)
 return [h for h in ds if h in used],ps

import itertools
start=time.monotonic();results=[];referenceP=G.profile(G.build(base,reference));best=score(referenceP,99)
cases=[]
for count in [1,2,3]:
 for ids in itertools.combinations(range(len(reference['kernel'])),count):
  for seed in range(3):cases.append((ids,seed))
for ci,(released,seed)in enumerate(cases):
 if time.monotonic()-start>120:break
 rng=random.Random(ci+19000);sel=dict(gauge=reference['gauge'],kernel=[copy.deepcopy(c)for i,c in enumerate(reference['kernel'])if i not in released]);avail=set(initial);P=Counter(baseP);n=0
 for c in sel['kernel']:
  hs=c['donors']+c['pivots'];avail-=set(hs);n+=len(c['pivots']);P[1]+=len(c['donors'])
  for h in hs:
   k=len(first[h]);P[k]-=1
   if k>1:P[k-1]+=1
 priority={h:(len(first[h])*(seed!=2)+rng.random())for h in initial}
 while True:
  opts=[]
  for e,hs in groups.items():
   key=hs&avail
   if len(key)<2:continue
   ds,ps=split(sorted(key,key=priority.get))
   if not ps:continue
   delta=Counter()
   for h in ds+ps:
    k=len(first[h]);delta[k]-=1
    if k>1:delta[k-1]+=1
   delta[1]+=len(ds)
   dc=72*sum(f(r)*x for r,x in delta.items())+phi[n+len(ps)]-phi[n]
   if dc<0:opts.append((-dc*(1+(rng.random()-.5)*(.0 if seed==0 else .5)),e,ds,ps,delta))
  if not opts:break
  _,e,ds,ps,delta=max(opts,key=lambda z:z[0]);sel['kernel'].append(dict(E=[e],donors=ds,pivots=ps));avail-=set(ds+ps);P.update(delta);n+=len(ps)
 value=score(P,n);z=dict(case=ci,released=released,seed=seed,pivots=n,entropy=value,status='MODULAR_NOMINATION_ONLY')
 if value<best-1e-7:
  try:
   w=G.build(base,sel);assert dict(G.profile(w))=={r:x for r,x in P.items()if x}
  except AssertionError as err:z.update(status='EXACT_REJECT',error=repr(err));results.append(z);continue
  best=value;z['status']='EXACT_STRUCTURAL_ONLY';z['profile']=dict(G.profile(w));(here/f'SELECTION-{ci}.json').write_text(json.dumps(sel,indent=2)+'\n');(here/f'WORD-{ci}.json.gz').write_bytes(G.dump(w));print('BETTER',z,flush=True)
 results.append(z)
(here/'SCREEN.json').write_text(json.dumps(dict(results=results,best_entropy=best,reference_entropy=score(referenceP,99),elapsed=time.monotonic()-start,scope='Bounded released-kernel neighborhood; exact structural rebuild only for improving nominations, no physical or global admission.'),indent=2)+'\n');print('DONE',len(results),best,flush=True)
