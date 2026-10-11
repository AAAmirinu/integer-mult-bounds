"""Independent exact local projector and both reflected chart identities. OpenAI Codex, Apache-2.0."""
import json,hashlib
from pathlib import Path
import sympy as s
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--frames',type=Path,required=True);ap.add_argument('--charts',type=Path,required=True);a=ap.parse_args();P=a.output;P.mkdir(exist_ok=True);F=a.frames;C=a.charts;fs=json.loads(F.read_text())['frames'];charts=json.loads(C.read_text());I=s.eye(8);Z=s.zeros(8);proj={}
for k,f in fs.items():
 B=s.Matrix(f['B'])if f['B']else s.zeros(0,8);A=s.Matrix(f['A'])if f['A']else s.zeros(0,8);Q=B.T*(B*B.T).inv()*B if B.rows else Z
 assert Q*Q==Q and Q.trace()==f['dim']and A*Q==s.zeros(A.rows,8)
 proj[int(k)]=Q
for n,c in enumerate(charts):
 a,b=proj[c['before']],proj[c['after']];r=c['rank'];D=b-a;Q=s.Matrix(c['basis']);J=s.Matrix(c['inverse']);E=s.diag(*([1]*r+[0]*(8-r)))
 assert a*b==b*a==a and D*D==D and D.trace()==r
 assert Q*J==J*Q==I and Q*E*J==D
 reflected=(I-a)-(I-b);assert reflected==D and Q*E*J==reflected
 if n%800==0:print(n,'PASS',flush=True)
# Equal-rank valid matrix from another frame must not validate this gap.
c1=charts[1];bad=next(c for c in charts if c['rank']==c1['rank']and proj[c['after']]-proj[c['before']]!=proj[c1['after']]-proj[c1['before']]);Q=s.Matrix(bad['basis']);J=s.Matrix(bad['inverse']);E=s.diag(*([1]*c1['rank']+[0]*(8-c1['rank'])));assert Q*E*J!=proj[c1['after']]-proj[c1['before']]
r=dict(status='PASS_INDEPENDENT_EXACT_ALL_LOCAL_AND_REFLECTED_CHART_IDENTITIES',frames=len(fs),charts=len(charts),frames_sha256=hashlib.sha256(F.read_bytes()).hexdigest(),charts_sha256=hashlib.sha256(C.read_bytes()).hexdigest(),same_rank_wrong_frame_chart_rejected=True,AI='OpenAI Codex, Apache-2.0.');(P/'LOCAL-CHARTS.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
