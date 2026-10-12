"""Reconstruct the coordinated rank-two gauge collapse after PR502 body retiming.
Apache-2.0. Prepared with OpenAI Codex assistance.
Usage: python -B build_rank2_collapse.py GK_CODE RETIMED_BASE BASELINE_SELECTION OUTPUT
The body retiming must be independently source-bound by its retained constructor.
"""
from pathlib import Path
import json,gzip,sys,hashlib,copy
from collections import Counter
if not __debug__:raise RuntimeError('Assertions must remain enabled')
code,base_path,sel_path,out=map(Path,sys.argv[1:]);assert not out.exists();sys.dont_write_bytecode=True;sys.path.insert(0,str(code));import gk_word as g
base=json.loads(gzip.decompress(base_path.read_bytes()));s=json.loads(sel_path.read_bytes());before=g.build(base,s);old=copy.deepcopy(s)
for h in ('540','541','542','543'):
 assert len(s['gauge'][h])==4
 assert g.span([408,102])<=g.span(s['gauge'][h])
 s['gauge'][h]=[408,102]
word=g.build(base,s);H0=g.profile(before);H=g.profile(word);delta={r:H[r]-H0[r]for r in set(H)|set(H0)if H[r]!=H0[r]}
assert delta=={2:-16,4:4,6:4},delta
changed={int(t):(len(E),len(word['target_levels'].get(t,[])))for t,E in before['target_levels'].items()if E!=word['target_levels'].get(t,[])}
assert changed=={81:(4,2),82:(4,2),84:(4,2),87:(4,2)},changed
assert Counter(g.widths_of(word))=={7:18,8:104,9:438}
assert old['kernel']==s['kernel']
for field in ('B','cut','ports','centers','center_frames','precondition'):assert word[field]==before[field],field
# Two inherited discovery floats differ in the independently reconstructed base;
# optional top-level R duplicates report.R. Every other field remains hash-bound.
normalized=copy.deepcopy(word)
assert normalized.get('R', normalized['report']['R']) == normalized['report']['R'] == 560
normalized.pop('R',None)
for key in ('complex_coarse_float','gain_percent_float'):
    normalized['report'].pop(key,None)
semantic_sha=hashlib.sha256(json.dumps(normalized,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert semantic_sha=='879c0e6ade3f1c84a515609a848dc917bddd1c1499e0cc37b2862809dfb8655b'
raw=g.dump(word)
out.mkdir(parents=True);(out/'FULL-WORD.json.gz').write_bytes(raw);(out/'SELECTION.json').write_text(json.dumps(s,indent=2)+'\n')
receipt=dict(status='PASS_EXACT_COORDINATED_GAUGE_RECONSTRUCTION',source_hashes={'retimed_base':hashlib.sha256(base_path.read_bytes()).hexdigest(),'baseline_selection':hashlib.sha256(sel_path.read_bytes()).hexdigest(),'gk_word.py':hashlib.sha256((code/'gk_word.py').read_bytes()).hexdigest(),'gk_common.py':hashlib.sha256((code/'gk_common.py').read_bytes()).hexdigest()},word_sha256=hashlib.sha256(raw).hexdigest(),normalized_word_sha256=semantic_sha,normalization_ignored_metadata=['optional redundant R','report.complex_coarse_float','report.gain_percent_float'],changed_target_dimensions=changed,local_profile=dict(H),delta=delta,widths=dict(Counter(g.widths_of(word))),scope='Exact local construction and frame nesting. Scalar, Gaussian phase, physical ownership, prefix and outer assembly independently required.')
(out/'CONSTRUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'])
