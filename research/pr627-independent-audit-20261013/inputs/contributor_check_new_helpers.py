"""Focused raw-word controls for both factored helpers; unchanged native auditor.
Jeremy Diviney with OpenAI Codex assistance; Apache-2.0.
"""
import argparse,contextlib,copy,gzip,hashlib,importlib.util,json,tempfile
from pathlib import Path
if not __debug__:raise RuntimeError('Assertions required; run without -O')
ap=argparse.ArgumentParser(description=__doc__)
for key in ('package','word','routing','out'):ap.add_argument('--'+key,type=Path,required=True)
a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
s=importlib.util.spec_from_file_location('audit',a.package/'code/hpe_audit_and_transport.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
w=json.load(gzip.open(a.word));d=json.loads((a.package/'data/FACTORED-END.json').read_text());results=[];mutations=[]
def drop(z,i):
 z['cleanup'].pop(i);z['early_cleanup']=[[j-(j>i),f]for j,f in z['early_cleanup']if j!=i]
for k,item in enumerate(d['helpers']):
 h=str(item['helper']);gate=d['additional_forward_insertions'][k][1];indices=[i for i,g in enumerate(w['A'])if g==gate];assert len(indices)==1;ai=indices[0]
 tail=d['extra_tail'][3*k:3*k+3];indices=[i for i in range(len(w['cleanup'])-2)if w['cleanup'][i:i+3]==tail];assert len(indices)==1;ci=indices[0]
 # The recorded prefix is second-helper eight gates followed by first-helper ten.
 lo,hi=(8,18)if k==0 else(0,8)
 assert any(g[1]==int(h)for g in w['A'][lo:hi])
 for name,mut in [
  ('premix_omitted',lambda z,lo=lo,hi=hi:z.__setitem__('A',z['A'][:lo]+z['A'][hi:])),
  ('absorption_omitted',lambda z,i=ai:z['A'].pop(i)),
  ('first_accumulator_gate_omitted',lambda z,i=ci:drop(z,i)),
  ('last_helper_tail_gate_omitted',lambda z,i=ci+2:drop(z,i)),
  ('end_dropped',lambda z,h=h:z['helper_final'].pop(h)),
  ('end_wrong_frame',lambda z,h=h:z['helper_final'].__setitem__(h,[])),
  ('tail_moved_to_full',lambda z,i=ci+2:z.__setitem__('early_cleanup',[x for x in z['early_cleanup']if x[0]!=i]))]:mutations.append((h+'_'+name,mut))
for name,mut in [('positive',None)]+mutations:
 z=copy.deepcopy(w)
 if mut:mut(z)
 with tempfile.TemporaryDirectory(prefix='intmult-two-factored-control-')as td:
  tmp=Path(td);raw=tmp/'WORD.json.gz';raw.write_bytes(gzip.compress(json.dumps(z,sort_keys=True,separators=(',',':')).encode(),mtime=0))
  with(a.out/(name+'.log')).open('w')as f,contextlib.redirect_stdout(f):
   try:m.run(raw,a.routing,tmp/'audit')
   except AssertionError as e:
    assert mut is not None;results.append(dict(name=name,status='REJECTED',reason=str(e)[:1000]));print('EXPECTED REJECTION',str(e)[:1000])
   else:assert mut is None,'malformed word accepted: '+name
 print('PASS',name,flush=True)
(a.out/'CONTROLS.json').write_text(json.dumps(dict(status='PASS_FOCUSED_TWO_HELPER_CONTROLS',input_content_sha256=hashlib.sha256(gzip.decompress(a.word.read_bytes())).hexdigest(),positive_pass=True,rejected=results),indent=2)+'\n')
