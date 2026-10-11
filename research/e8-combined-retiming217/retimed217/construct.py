import sys
sys.dont_write_bytecode=True
"""Apply eleven new fixed-scalar gate frame retimings; PR376 stays downstream.
OpenAI Codex,2026-10-11. Scalar order,coefficients and entrance dimensions fixed.
"""
import argparse,json,hashlib,copy
from pathlib import Path
import common as C
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('selection',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(args.source)=='7cacea6505d1bde3913268f00a9bb450a03c1d15fec81f500195c14f5e03fb7e'
b=json.loads(args.source.read_text());c=copy.deepcopy(b);plans=json.loads(args.selection.read_text())
for p in plans:
 g=c[p['part']][p['index']];assert [g[0]]+g[2:]==p['scalar_group'];assert g[1]==p['old_frame'];assert c['frames'][p['new_frame']]==p['new_basis'];g[1]=p['new_frame']
C.rehist_and_audit(c)
cur=c['start'][:]
for g in c['A']:
 for r in C.gate_roles(g):cur[r]=g[1]
assert all(cur[r]==f for _,r,f in c['ret'])
assert C.replay(c)==C.replay(b)
x=copy.deepcopy(c);y=copy.deepcopy(b)
for z in [x,y]:z['B']=[];z['scat']['table']=[[] for _ in range(z['v'])]
assert C.replay(x)==C.replay(y)
for part in ['A','B']:assert [[g[0]]+g[2:] for g in c[part]]==[[g[0]]+g[2:] for g in b[part]]
assert c['start']==b['start'] and c['ext']==b['ext'] and c['final']==b['final']
h=C.histogram(c);h.subtract(C.histogram(b));delta={r:n for r,n in h.items() if n};assert sum(r*n for r,n in delta.items())==0
blob=json.dumps(c,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(blob).hexdigest()=='3c2c7470ed3c1af2a7a94e32435065bdfef88838303ee1be9d716989b9ffb507';assert not args.output.exists();args.output.mkdir(parents=True);(args.output/'candidate.json').write_bytes(blob)
receipt=dict(status='PASS_FIXED_SCALAR_GATE_FRAME_RETIMING',source_sha256=sha(args.source),candidate_sha256=hashlib.sha256(blob).hexdigest(),selection=plans,local_delta=delta,all1021raw_columns_unchanged=True,scalar_words_unchanged=True,entrance_dimensions=391,fixed_snapshot_labels=True)
(args.output/'RECEIPT.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
