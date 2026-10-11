from pathlib import Path
import json,copy,importlib.util,hashlib,sys
sys.dont_write_bytecode=True
from fractions import Fraction as Q
spec=importlib.util.spec_from_file_location('Re',Path(__file__).resolve().parents[1]/'frames/reconstruct.py');Re=importlib.util.module_from_spec(spec);spec.loader.exec_module(Re)
src,root=map(Path,sys.argv[1:3]);assert not root.exists();root.mkdir(parents=True)
assert hashlib.sha256(src.read_bytes()).hexdigest()=='bea60fc0f66caf105dbd5637a01f8eab30d923afef27cba6f2207cb36ca547f3'
b=json.loads(src.read_text());c=copy.deepcopy(b)
p=760;entry=[240];cm={896:Q(-1),998:Q(-1),955:Q(-2),898:Q(-1),1003:Q(-1),836:Q(-1)}
f=next(i for i,e in enumerate(c['frames']) if len(e)==1 and Re.inside(entry,e));assert c['start'][p]==0
c['start'][p]=f;c['ext']=sorted(c['ext']+[[p,f]])
head=[]
for d,q in sorted(cm.items()):
 for _ in range(abs(q.numerator)):head.append(['in',f,d,[[p,1 if q>0 else -1,q.denominator]]])
c['A']=head+c['A'];Re.rehist_and_audit(c)
a=Re.replay(b);z=Re.replay(c)
for t in range(len(a)):
 row=dict(a[t]);q=row.get(p,Q(0))+sum(q*a[t].get(d,Q(0)) for d,q in cm.items())
 if q:row[p]=q
 else:row.pop(p,None)
 assert row==z[t],t
assert all(r not in z[t] for r,_ in c['ext'] for t in range(120,240))
blob=json.dumps(c,sort_keys=True,separators=(',',':')).encode();assert hashlib.sha256(blob).hexdigest()=='39c360dd4fc763b7fccff7ec5e2a3e8b50ae90e50d8ac50e062315253c2b411b';(root/'candidate.json').write_bytes(blob)
receipt={'source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(blob).hexdigest(),'pivot':p,'entry_basis':entry,'entry_frame':f,'coefficients':{d:str(q) for d,q in cm.items()},'head':head,'gauges':len(c['ext']),'raw_columns':len(a),'new_operator_equals_previous_times_literal_shear':True,'all_gauged_target_responses_zero':True,'paid_profile':Re.histogram(c)}
(root/'RECEIPT.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
