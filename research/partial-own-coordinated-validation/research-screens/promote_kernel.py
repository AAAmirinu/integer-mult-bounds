from pathlib import Path
from collections import Counter
import copy,gzip,json,sys
root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'e8-partial-async-release/research/partial-own-asynchronous-whole-owners/vendor/pr507/vendor/complex/e8-complex-gauge-kernel/code'));import gk_word as G
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
base=read(here/'construction/RETIMED-BASE.json.gz');sel=read(here/'construction/SELECTION.json');cols=G.responses(base);first=G.first_frames(base);sp={h:G.span(F)for h,F in first.items()};candidates=[];eligible=[]
for ci,c in enumerate(sel['kernel']):
 for p in c['pivots']:
  rel=G.solve_relation(cols,c['donors'],p);common=sp[p].copy()
  for d in rel:common&=sp[d]
  E=G.basis(sorted(common-{0}));assert G.span(c['E'])<=common
  if len(E)>len(c['E']):eligible.append(dict(group=ci,pivot=p,E=list(E),donors=sorted(rel)))
for z in eligible:
 changed=copy.deepcopy(sel);changed['kernel'][z['group']]['pivots'].remove(z['pivot']);changed['kernel'].append(dict(E=z['E'],donors=z['donors'],pivots=[z['pivot']]))
 try:w=G.build(base,changed)
 except AssertionError as e:candidates.append(dict(**z,status='STRUCTURAL_REJECT',error=repr(e)));continue
 out=here/'promotions';out.mkdir(exist_ok=True);(out/f"SELECTION-{z['pivot']}.json").write_text(json.dumps(changed,indent=2)+'\n');(out/f"WORD-{z['pivot']}.json.gz").write_bytes(G.dump(w));candidates.append(dict(**z,status='STRUCTURAL_ONLY',profile=dict(G.profile(w)),widths=dict(Counter(G.widths_of(w)))))
(here/'PROMOTION-SCREEN.json').write_text(json.dumps(dict(status='EXACT_CURRENT_RELATION_INTERSECTION_SCREEN',eligible=eligible,candidates=candidates,scope='Fixed current donor relations, single pivot promotion only; not a global maximum.'),indent=2)+'\n');print('ELIGIBLE',len(eligible),'PASS',sum(z['status']=='STRUCTURAL_ONLY'for z in candidates),flush=True)
