"""OpenAI Codex2026-10-11: source-pinned joint gate frame-block retiming.
Scalar instructions/order and entrance spaces remain fixed.
"""
import sys
sys.dont_write_bytecode=True
import argparse,json,hashlib,copy
from pathlib import Path
import common as C
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('selection',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args();sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(args.source)=='a1b680be1fda1d0120d349f8962a053697b2b6abe8a6ffc437ac91be21b338d0';b=json.loads(args.source.read_text());c=copy.deepcopy(b);plans=json.loads(args.selection.read_text())
for p in plans:
 g=c[p['part']][p['index']];assert g[1]==p['old']
 if p['new']>=len(c['frames']):
  assert p['new']==len(c['frames']);c['frames'].append(p['basis'])
 else:assert c['frames'][p['new']]==p['basis']
 g[1]=p['new']
C.rehist_and_audit(c);assert C.replay(c)==C.replay(b)
# Independently retain the exact pre-snapshot row operator.
z=copy.deepcopy(c);w=copy.deepcopy(b)
for q in [z,w]:q['B']=[];q['scat']['table']=[[] for _ in range(q['v'])]
assert C.replay(z)==C.replay(w)
assert c['start']==b['start'] and c['ext']==b['ext'] and c['final']==b['final']
cur=c['start'][:]
for g in c['A']:
 for r in C.gate_roles(g):cur[r]=g[1]
assert all(cur[r]==f for _,r,f in c['ret'])
for part in ['A','B']:assert [[g[0]]+g[2:] for g in c[part]]==[[g[0]]+g[2:] for g in b[part]]
blob=json.dumps(c,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(blob).hexdigest()=='6217b9ecb79d342c4cb07ac60967bdfdc01c96133ff4a60223d53e5420847e9b';assert not args.output.exists();args.output.mkdir(parents=True);(args.output/'candidate.json').write_bytes(blob);h=C.histogram(c);h.subtract(C.histogram(b));delta={r:n for r,n in h.items() if n};assert sum(r*n for r,n in delta.items())==0
out=dict(status='PASS_BLOCK_FRAME_RETIMING',source_sha256=sha(args.source),candidate_sha256=hashlib.sha256(blob).hexdigest(),selection=plans,local_delta=delta,scalar_words_unchanged=True,raw_columns_unchanged=True,pre_snapshot_columns_unchanged=True,fixed_snapshot_labels=True,entrance_dimensions=391)
(args.output/'RECEIPT.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
