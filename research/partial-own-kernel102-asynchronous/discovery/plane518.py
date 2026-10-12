"""Exact-response screen for rank-two kernel entrances on PR518."""
from pathlib import Path
from collections import defaultdict,Counter
import gzip,itertools,json,sys
root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'resume-20261011/pr518/research/nodal-pair-async/vendor/complex/e8-complex-gauge-kernel/code'));import gk_word as G
w=json.load(gzip.open('/private/tmp/pr518-macos-fresh/base/split-centres/RETIMED-BASE.json.gz'));sel=json.loads((root/'resume-20261011/pr518/research/nodal-pair-async/inputs/PAIR-SELECTION.json').read_text());first=G.first_frames(w);cols=G.responses(w);prime=1000003
mod=[{t:int(x.numerator)*pow(int(x.denominator),-1,prime)%prime for t,x in c.items()}for c in cols]
groups=defaultdict(set)
for h in range(560):
 if str(h)in sel['gauge']:continue
 points=sorted(G.span(first[h])-{0})
 for a,b in itertools.combinations(points,2):groups[tuple(sorted((a,b,a^b)))].add(h)
records=[]
for E,hs in sorted(groups.items()):
 if len(hs)<2:continue
 basis={};donors=[];pivots=[]
 for h in sorted(hs,key=lambda x:(len(first[x]),x)):
  v=dict(mod[h])
  while v:
   t=min(v)
   if t not in basis:
    q=pow(v[t],-1,prime);basis[t]={k:x*q%prime for k,x in v.items()};donors.append(h);break
   q=v[t]
   for k,x in basis[t].items():
    z=(v.get(k,0)-q*x)%prime
    if z:v[k]=z
    else:v.pop(k,None)
  if not v:pivots.append(h)
 if pivots:
  relations={h:G.solve_relation(cols,donors,h)for h in pivots};assert all(z is not None for z in relations.values());used=set().union(*(set(z)for z in relations.values()));ds=[h for h in donors if h in used]
  test=dict(gauge=sel['gauge'],kernel=[dict(E=list(E[:2]),donors=ds,pivots=pivots)]);word=G.build(w,test)
  z=dict(E=E,donors=ds,pivots=pivots,profile=dict(G.profile(word)),widths=dict(Counter(G.widths_of(word))));records.append(z);print('PLANE',E,len(ds),len(pivots),flush=True)
(here/'PLANE518-SCREEN.json').write_text(json.dumps(dict(planes=len(groups),shared_planes=sum(len(hs)>1 for hs in groups.values()),dependent=records,scope='All rank-two planes contained in first frames of the 480 nongauged helpers, modular independence certificates over F1000003 or exact rational dependence and exact G.build for surviving planes; arbitrary-dirt and physical admission separate.'),indent=2)+'\n');print('DONE',len(groups),len(records),flush=True)
