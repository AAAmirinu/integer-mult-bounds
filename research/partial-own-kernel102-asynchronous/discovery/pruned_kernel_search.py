"""Bounded modular nomination; exact response construction checks every candidate."""
from pathlib import Path
from collections import Counter
import copy,gzip,json,random,sys,time,math
root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'e8-partial-async-release/research/partial-own-asynchronous-whole-owners/vendor/pr507/vendor/complex/e8-complex-gauge-kernel/code'));import gk_word as G
base=json.load(gzip.open(root/'resume-20261011/partial-collapse/construction/RETIMED-BASE.json.gz'));reference=json.loads((here/'KERNEL92-SELECTION.json').read_text());cols=G.responses(base);first=G.first_frames(base);prime=1000003;mod=[{t:int(x.numerator)*pow(int(x.denominator),-1,prime)%prime for t,x in c.items()}for c in cols]
initial=set(range(560))-set(map(int,reference['gauge']));groups={e:{h for h in initial if e in G.span(first[h])}for e in range(1,512)};groups={e:hs for e,hs in groups.items()if len(hs)>1};cache={}
def split(hs):
 basis={};ds=[];ps=[];used=set()
 for h in hs:
  v=dict(mod[h]);combo={}
  while v:
   t=min(v)
   if t not in basis:
    q=pow(v[t],-1,prime);rep={j:-c*q%prime for j,c in combo.items()};rep[h]=q
    basis[t]=({k:x*q%prime for k,x in v.items()},rep);ds.append(h);break
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
start=time.monotonic();results=[];best=92
for seed in range(120):
 if time.monotonic()-start>90:break
 rng=random.Random(seed);avail=set(initial);selection=dict(gauge=reference['gauge'],kernel=[]);alpha=[0,.15,.3,.5][seed%4]
 while True:
  choices=[]
  for e,hs in groups.items():
   key=tuple(sorted(hs&avail))
   if len(key)<2:continue
   if key not in cache:
    ds,ps=split(key);cache[key]=(len(ds),len(ps))
   nd,np=cache[key]
   if np:choices.append((np/(max(nd,1)**alpha)*(1+(rng.random()-.5)*(.05 if seed<30 else .3)),e,key))
  if not choices:break
  _,e,key=max(choices);hs=list(key);rng.shuffle(hs);ds,ps=split(hs);selection['kernel'].append(dict(E=[e],donors=ds,pivots=ps));avail-=set(ds+ps)
 n=sum(len(c['pivots'])for c in selection['kernel'])
 # Every candidate is exact checked; no modular false dependence is accepted.
 try:w=G.build(base,selection)
 except AssertionError as e:results.append(dict(seed=seed,pivots=n,status='EXACT_REJECT',reason=repr(e)));continue
 profile=dict(G.profile(w));result=dict(seed=seed,pivots=n,status='EXACT_STRUCTURAL_ONLY',profile=profile,widths=dict(Counter(G.widths_of(w))));results.append(result)
 if n>=best:
  (here/f'PRUNED-SELECTION-{seed}.json').write_text(json.dumps(selection,indent=2)+'\n');(here/f'PRUNED-WORD-{seed}.json.gz').write_bytes(G.dump(w));print('CANDIDATE',seed,n,profile,flush=True);best=max(best,n)
(here/'PRUNED-KERNEL-SCREEN.json').write_text(json.dumps(dict(results=results,best_incumbent_pivots=best,best_nominated_pivots=max(r['pivots']for r in results),seconds=time.monotonic()-start,scope='All donor and pivot roles may change; fixed collapsed gauges and retimed scalar base. Modular search nominations undergo exact G.build relation/frame checks. No fresh scalar/Gaussian/physical or global owner admission yet.'),indent=2)+'\n');print('DONE',len(results),best,flush=True)
