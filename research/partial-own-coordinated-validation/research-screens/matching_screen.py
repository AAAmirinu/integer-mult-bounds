from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import copy,gzip,json,subprocess,sys
root=Path(__file__).resolve().parents[2];here=Path(__file__).resolve().parent
package=root/'e8-partial-async-release/research/partial-own-asynchronous-whole-owners/vendor/pr507';source=package/'vendor/complex/e8-complex-gauge-kernel';sys.path.insert(0,str(source/'code'));import gk_word as G
input=Path('/private/tmp/partial-async-macos314-fresh/dependency/retimed/gauge80-kernel42/work/complex-network/hamming');old=json.loads((here/'construction/SELECTION.json').read_text());read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes());results=[]
for a in range(3):
 for b in range(3):
  out=here/f'matching-{a}{b}';out.mkdir();script=out/'construct.py';code=(package/'code/construct_partial.py').read_text().replace('(1,1)[parity]',f'({a},{b})[parity]');assert code!=(package/'code/construct_partial.py').read_text()or(a,b)==(1,1)
  # Do not preserve baseline discovery-only annotations on changed constructions.
  code=code.replace("'complex_coarse_float':0.0011839865492062449,'baseline_b':0.000999388595603943,", "'baseline_b':0.000999388595603943,").replace("'gain_percent_float':18.471088665039947,", "'matching_choice':[%d,%d],"%(a,b));script.write_text(code)
  with (out/'construct.log').open('w')as f:r=subprocess.run([sys.executable,'-B',str(script),str(input),str(out/'base')],stdout=f,stderr=subprocess.STDOUT)
  if r.returncode:results.append(dict(matching=[a,b],status='CLEAN_CONSTRUCTION_FAILED'));continue
  base=read(out/'base/FULL-WORD.json.gz');sel=copy.deepcopy(old);sel['kernel']=sel['kernel'][:12];col=G.responses(base);first=G.first_frames(base)
  try:G.build(base,sel)
  except AssertionError as e:results.append(dict(matching=[a,b],status='OLD42_STRUCTURAL_REJECT',reason=repr(e)));continue
  used=set(map(int,sel['gauge']))|{h for c in sel['kernel']for h in c['donors']+c['pivots']};available=set(range(560))-used;spans={h:G.span(F)for h,F in first.items()}
  for turn in range(30):
   options=[]
   for e in range(1,512):
    hs=sorted(h for h in available if e in spans[h]);basis={};ds=[];ps=[]
    for h in hs:
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
     if not v:ps.append(h)
    if ps:options.append((len(ps),-len(ds),-e,ds,ps))
   if not options:break
   _,_,neg,ds,ps=max(options);e=-neg;sel['kernel'].append(dict(E=[e],donors=ds,pivots=ps));available-=set(ds+ps)
  try:w=G.build(base,sel)
  except AssertionError as e:results.append(dict(matching=[a,b],status='GREEDY_STRUCTURAL_REJECT',reason=repr(e)));continue
  (out/'SELECTION.json').write_text(json.dumps(sel,indent=2)+'\n');(out/'WORD.json.gz').write_bytes(G.dump(w));result=dict(matching=[a,b],status='CLEAN_BASE_AND_SELECTED_STRUCTURAL_ONLY',pivots=sum(len(c['pivots'])for c in sel['kernel']),profile=dict(G.profile(w)),widths=dict(Counter(G.widths_of(w))));results.append(result);print(result,flush=True)
(here/'MATCHING-SCREEN.json').write_text(json.dumps(dict(results=results,scope='Fresh exact clean scalar bases plus structural/profile checks only; new dirty, retiming, Gaussian and physical admission absent. Greedy kernel selection is not optimal.'),indent=2)+'\n')
