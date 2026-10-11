from pathlib import Path
from collections import Counter,defaultdict
from fractions import Fraction as Q
import copy,gzip,json,sys,time
root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent
source=root/'e8-partial-async-release/research/partial-own-asynchronous-whole-owners/vendor/pr507/vendor/complex/e8-complex-gauge-kernel'
sys.path.insert(0,str(source/'code'));import gk_word as G
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
base=read(here/'construction/RETIMED-BASE.json.gz');sel=read(here/'construction/SELECTION.json');col=G.responses(base);first=G.first_frames(base)
used={h for c in sel['kernel']for h in c['donors']+c['pivots']}|set(map(int,sel['gauge']));free=set(range(560))-used
spans={h:G.span(first[h])for h in first};oldD=defaultdict(set)
for c in sel['kernel']:
 assert len(c['E'])==1
 oldD[c['E'][0]].update(c['donors'])
rows=[];candidates=[]
for e in range(1,512):
 eligible=sorted(h for h in free if e in spans[h]);basis={};ds=[];ps=[]
 # Independent anchors first, then free columns; record new dependencies.
 for h in sorted(oldD[e])+eligible:
  v=dict(col[h])
  while v:
   t=min(v)
   if t not in basis:
    q=v[t];basis[t]={k:x/q for k,x in v.items()};ds.append(h);break
   q=v[t]
   for k,x in basis[t].items():
    z=v.get(k,Q(0))-q*x
    if z:v[k]=z
    else:v.pop(k,None)
  if not v and h in free:ps.append(h)
 rows.append(dict(direction=e,eligible=len(eligible),old_donors=len(oldD[e]),rank=len(ds),new_pivots=ps))
 if not ps:continue
 # Select exact independent donor set; old redundant donors may be omitted only
 # from this new class. Their original classes are retained unchanged.
 change=copy.deepcopy(sel);change['kernel'].append(dict(E=[e],donors=ds,pivots=ps))
 try:w=G.build(base,change)
 except AssertionError as ex:
  candidates.append(dict(direction=e,pivots=ps,status='STRUCTURAL_REJECT',reason=repr(ex)));continue
 out=here/'extra-kernel';out.mkdir(exist_ok=True);(out/f'SELECTION-{e}.json').write_text(json.dumps(change,indent=2)+'\n');(out/f'WORD-{e}.json.gz').write_bytes(G.dump(w))
 candidates.append(dict(direction=e,pivots=ps,status='STRUCTURAL_ONLY',local_profile=dict(G.profile(w)),widths=dict(Counter(G.widths_of(w)))))
 print('CANDIDATE',e,len(ps),candidates[-1]['status'],flush=True)
report=dict(status='EXACT_AVAILABLE_COLUMN_SCREEN',free_helpers=len(free),directions=rows,candidates=candidates,scope='Additional kernels using currently unassigned helpers and same-line existing donors only. Existing pivots/gauges fixed. No global maximality or physical admission claimed.')
(here/'EXTRA-KERNEL-SCREEN.json').write_text(json.dumps(report,indent=2)+'\n');print('DONE',len(candidates),flush=True)
