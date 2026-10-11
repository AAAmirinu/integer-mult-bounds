"""Four additional grouped promotions; discovery inspired by PR409.
OpenAI Codex; frozen raw206 input. Requires full downstream stage integration.
"""
from pathlib import Path
import json,copy,hashlib,importlib.util,sys
sys.dont_write_bytecode=True
from fractions import Fraction as Q
s=importlib.util.spec_from_file_location('Re',Path(__file__).resolve().parents[1]/'frames/reconstruct.py');Re=importlib.util.module_from_spec(s);s.loader.exec_module(Re)
source,root=map(Path,sys.argv[1:3]);assert not root.exists();root.mkdir(parents=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='39c360dd4fc763b7fccff7ec5e2a3e8b50ae90e50d8ac50e062315253c2b411b'
b=json.loads(source.read_text());c=copy.deepcopy(b)
pl=json.loads((Path(__file__).resolve().parent/'selection.json').read_text());assert pl['basis']==[48];oldext=set(dict(b['ext']));newp={x['pivot'] for x in pl['pivots']};donors=set(pl['donors']);assert not oldext&(newp|donors) and not newp&donors
E=pl['basis'];f=next(i for i,e in enumerate(c['frames']) if len(e)==len(E) and Re.inside(E,e));head=[]
for pp in pl['pivots']:
 p=pp['pivot'];assert c['start'][p]==0;c['start'][p]=f;c['ext'].append([p,f])
 for d,a in sorted(pp['coefficients'].items(),key=lambda x:int(x[0])):
  d=int(d);a=Q(a)
  for _ in range(abs(a.numerator)):head.append(['in',f,d,[[p,1 if a>0 else -1,a.denominator]]])
c['ext'].sort();c['A']=head+c['A'];Re.rehist_and_audit(c)
for tag in ['whole','before_snapshot']:
 old=copy.deepcopy(b);new=copy.deepcopy(c)
 if tag=='before_snapshot':
  for z in [old,new]:z['B']=[];z['scat']['table']=[[] for _ in range(z['v'])]
 wanted=Re.replay(old);actual=Re.replay(new)
 for g in reversed(head):
  d=g[2];p,a,z=g[3][0];q=Q(a,z)
  for row in wanted:
   v=row.get(p,Q(0))+q*row.get(d,Q(0))
   if v:row[p]=v
   else:row.pop(p,None)
 assert actual==wanted,tag
 if tag=='whole':assert all(p not in actual[t] for p,_ in c['ext'] for t in range(c['v'],2*c['v']))
blob=json.dumps(c,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(blob).hexdigest()=='f93a32af6badb9e7e9ef9134a5f5ba928927c5cff621cab7855d2b8ad1545b66';(root/'candidate.json').write_bytes(blob)
a=Re.histogram(c);a.subtract(Re.histogram(b));delta={r:v for r,v in a.items() if v}
receipt=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),candidate_sha256=hashlib.sha256(blob).hexdigest(),gauges=len(c['ext']),new_gates=len(head),selection=pl,local_delta=delta,paid_profile=dict(Re.histogram(c)),all1021raw_and_snapshot_columns_right_multiplied_by_literal_prepended_word=True,all_gauged_response_columns_zero=True)
(root/'RECEIPT.json').write_text(json.dumps(receipt,indent=2));(root/'SELECTION.json').write_text(json.dumps(pl,indent=2));print(json.dumps(receipt,indent=2))
