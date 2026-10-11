"""Source-bound gauge-collapse experiment on PR507's partial-own kernel84.
No addition of separately priced gains; reconstruct the whole selected word.
"""
from pathlib import Path
from collections import Counter
import copy,gzip,hashlib,json,sys
source,oldbase,selection_path,out=map(Path,sys.argv[1:]);assert not out.exists();out.mkdir(parents=True)
sys.path.insert(0,str(source/'code'));import gk_word as G
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
original=read(oldbase/'sc_base/FULL-WORD.json.gz');current=read(oldbase/'split-centres/FULL-WORD.json.gz');sel=read(selection_path)
base=copy.deepcopy(original)
prefix=len(current['A'])-len(original['A']);assert prefix==671
for part in ['A','B']:
 events=current[part][prefix:]if part=='A'else current[part]
 assert [e[:-1]for e in events]==[e[:-1]for e in original[part]],part
 base[part]=copy.deepcopy(events)
base['cleanup']=[G.inverse(e,G.FULL)for e in reversed(base['A']+base['B'])if not G.V<=e[1]<2*G.V]
rebuilt=G.build(base,sel)
assert rebuilt==current,'Rebuilt baseline must match every parsed field of the verified word'
changed=copy.deepcopy(sel)
for h in ['540','541','542','543']:
 assert len(changed['gauge'][h])==4 and G.span([408,102])<=G.span(changed['gauge'][h])
 changed['gauge'][h]=[408,102]
word=G.build(base,changed);before=G.profile(current);after=G.profile(word)
assert changed['kernel']==sel['kernel']
assert sum(len(c['pivots'])for c in changed['kernel'])==84
for key in ['ports','centers','center_frames','cut','B','precondition','root_lines','scatter']:
 assert word[key]==current[key],key
delta={r:after[r]-before[r]for r in set(before)|set(after)if after[r]!=before[r]}
target_delta={t:[len(E),len(word['target_levels'].get(t,[]))]for t,E in current['target_levels'].items()if E!=word['target_levels'].get(t,[])}
assert delta=={2:-16,4:4,6:4}
assert Counter(G.widths_of(word))==Counter({9:396,8:146,7:18})
receipt=dict(status='STRUCTURAL_CONSTRUCTION_ONLY',baseline_reconstruction_all_fields_equal=True,preserved_kernel_pivots=sum(len(c['pivots'])for c in sel['kernel']),body_frame_transfer_prefix=prefix,delta=delta,target_delta=target_delta,widths=dict(sorted(Counter(G.widths_of(word)).items())),local_profile=dict(sorted(after.items())),source_word_sha256=hashlib.sha256((oldbase/'split-centres/FULL-WORD.json.gz').read_bytes()).hexdigest(),word_sha256=hashlib.sha256(G.dump(word)).hexdigest(),scope='Full exact structural reconstruction; scalar, Gaussian, guarded physical, placement and assembly gates remain.')
(out/'RETIMED-BASE.json.gz').write_bytes(G.dump(base));(out/'FULL-WORD.json.gz').write_bytes(G.dump(word));(out/'SELECTION.json').write_text(json.dumps(changed,sort_keys=True,indent=2)+'\n');(out/'CONSTRUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps(receipt,indent=2))
