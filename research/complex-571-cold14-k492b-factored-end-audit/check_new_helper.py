"""Focused independent raw-word controls for the new factored helper, not admission code.
Uses the unchanged native auditor. Jeremy Diviney/OpenAI Codex assisted.
"""
import contextlib,copy,gzip,hashlib,importlib.util,json,tempfile
from pathlib import Path
import argparse
if not __debug__:raise RuntimeError('Assertions required; run without -O')
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--package',type=Path,required=True)
ap.add_argument('--word',type=Path,required=True)
ap.add_argument('--routing',type=Path,required=True)
ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args();p=a.package;src=a.word;routing=a.routing;out=a.out;out.mkdir(parents=True,exist_ok=False)
s=importlib.util.spec_from_file_location('audit',p/'code/hpe_audit_and_transport.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);w=json.load(gzip.open(src));plan=json.loads((p/'data/FACTORED-END.json').read_text());results=[]
def drop(w,i):
 w['cleanup'].pop(i);w['early_cleanup']=[[j-(j>i),f]for j,f in w['early_cleanup']if j!=i]
def without_premix(w):w['A']=w['A'][len(plan['premix']):]
mutations=[('new_premix_omitted',without_premix),('new_absorption_omitted',lambda w:w['A'].pop(2249)),('first_accumulator_gate_omitted',lambda w:drop(w,120)),('last_helper_tail_gate_omitted',lambda w:drop(w,122)),('new_helper_end_dropped',lambda w:w['helper_final'].pop('590')),('new_helper_end_wrong_frame',lambda w:w['helper_final'].__setitem__('590',[384,72,40,24,4,2,1])),('new_tail_moved_to_full',lambda w:w.__setitem__('early_cleanup',[x for x in w['early_cleanup']if x[0]!=122]))]
for name,mut in [('positive',None)]+mutations:
 z=copy.deepcopy(w)
 if mut:mut(z)
 with tempfile.TemporaryDirectory(prefix='intmult-factored-control-')as tmp:
  tmp=Path(tmp);raw=tmp/'WORD.json.gz';raw.write_bytes(gzip.compress(json.dumps(z,sort_keys=True,separators=(',',':')).encode(),mtime=0))
  with (out/(name+'.log')).open('w')as f,contextlib.redirect_stdout(f):
   try:m.run(raw,routing,tmp/'audit')
   except AssertionError as e:
    assert mut is not None;results.append(dict(name=name,status='REJECTED',reason=str(e)[:1000]));print('EXPECTED REJECTION',str(e)[:1000])
   else:assert mut is None,'malformed new-helper word accepted: '+name
 print('PASS',name,flush=True)
(out/'CONTROLS.json').write_text(json.dumps(dict(status='PASS_FOCUSED_NEW_HELPER_CONTROLS',input_content_sha256=hashlib.sha256(gzip.decompress(src.read_bytes())).hexdigest(),positive_pass=True,rejected=results),indent=2)+'\n')
