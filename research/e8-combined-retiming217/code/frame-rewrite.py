"""Frozen PR376 frame rewrite after the newly reconstructed shared/dual witness."""
from pathlib import Path
import argparse,json,copy,hashlib,importlib.util
ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args()
assert not args.output.exists();source=args.source.read_bytes();assert hashlib.sha256(source).hexdigest()=='51278e6f2810c0008101d5f8e018220f4a5b57fc41e40be40ffcf22fe0d349ac'
p=Path(__file__).resolve().parents[1]/'frames/reconstruct.py';s=importlib.util.spec_from_file_location('frames',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
c=json.loads(source);b=copy.deepcopy(c);hits=[(part,i) for part in ['A','B'] for i,g in enumerate(b[part]) if g==['in',203,201,[[491,1,2]]]];assert len(hits)==1
part,i=hits[0];b[part][i][1]=942;trans=m.rehist_and_audit(b);assert m.replay(c)==m.replay(b)
h0=m.histogram(c);h1=m.histogram(b);delta={r:h1[r]-h0[r] for r in h0.keys()|h1.keys() if h1[r]!=h0[r]};assert delta=={1:-2,2:1}
blob=json.dumps(b,sort_keys=True,separators=(',',':')).encode();digest=hashlib.sha256(blob).hexdigest();assert digest=='c224f54268b37b610f663661634933387b2ba7f59f4d650f9aa6f5aaccfce9f6'
args.output.mkdir(parents=True);(args.output/'candidate.json').write_bytes(blob)
(args.output/'RECEIPT.json').write_text(json.dumps(dict(status='PASS_PR376_FRAME_COMPOSITION_EXACT_COLUMNS_AND_NESTED_PATHS',source_sha256=hashlib.sha256(source).hexdigest(),candidate_sha256=digest,raw_columns=1021,nested_transitions=trans,histogram_delta=delta,edit_location=hits,credit='PR376@7aa9d9f0247bb60c0519704bbca18990011e2a37',scope='Finite construction; complete changed scalar/phase/global admission and conditional pricing follow separately.'),indent=2))
print('PASS final candidate',digest)
