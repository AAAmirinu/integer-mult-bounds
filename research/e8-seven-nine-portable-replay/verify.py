#!/usr/bin/env python3
"""Replay the frozen seven/nine composition from a clean checkout, offline.

Default: fresh candidate reconstruction/export, exact signed source and both
frame ledgers, all local/reflected charts, full seven-stage IR and idle links,
all-port rational routes, finite bill, complex supplier and exact assembly.
--quick: integrity, source reconstruction and historical assembly only.
No proof receipt's recorded workstation location is opened.
"""
import argparse,gzip,hashlib,importlib.util,json,os,shutil,subprocess,sys,tarfile,tempfile,time
from pathlib import Path
assert __debug__, 'Assertions required: do not use -O'
assert sys.version_info >= (3,11)
sys.dont_write_bytecode=True

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def write(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def manifest(root,strict=False):
 p=root/'MANIFEST.sha256';assert p.is_file(),('missing manifest',p)
 rows={}
 for line in p.read_text().splitlines():
  if not line.strip():continue
  h,name=line.split(None,1);name=name.strip().removeprefix('./');q=root/name
  assert name not in rows and q.resolve().is_relative_to(root.resolve()) and not q.is_symlink()
  assert q.is_file() and sha(q)==h,('manifest mismatch',q)
  rows[name]=h
 if strict:
  files={str(f.relative_to(root)) for f in root.rglob('*') if f.is_file() and f!=p and '__pycache__' not in f.parts}
  assert files==set(rows),('manifest coverage mismatch',sorted(set(rows)-files),sorted(files-set(rows)))
 return len(rows)

def extract(src,dst):
 dst.mkdir()
 with tarfile.open(src,'r:gz') as t:
  for m in t.getmembers():
   assert (dst/m.name).resolve().is_relative_to(dst.resolve()) and (m.isfile() or m.isdir()),('unsafe tar member',m.name)
  t.extractall(dst)

def normalized_signed(x):
 x=dict(x);x.pop('seconds');x['input_sha256']={Path(k).name:v for k,v in x['input_sha256'].items()};return x

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('package',type=Path);ap.add_argument('--work',type=Path);ap.add_argument('--quick',action='store_true');a=ap.parse_args()
 pkg=a.package.resolve();manifest(pkg,strict=True)
 work=a.work.resolve() if a.work else Path(tempfile.mkdtemp(prefix='e8-seven-nine-portable-')).resolve()
 if a.work:assert not work.exists();work.mkdir(parents=True)
 assert not work.is_relative_to(pkg)
 logs=work/'logs';logs.mkdir();ext=work/'extract';ext.mkdir();checks=[];started=time.monotonic()
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 for key in ('PYTHONOPTIMIZE','PR315','CX_SOURCE_PINS','CX_PINS','CX_RECORD','CX_RECEIPT','B3_OUT'):env.pop(key,None)
 def run(tag,argv,cwd=None):
  log=logs/(tag+'.txt');print('CHECK',tag,flush=True);t=time.monotonic()
  with log.open('w') as f:r=subprocess.run([sys.executable,'-B']+list(map(str,argv)),cwd=cwd or work,env=env,stdout=f,stderr=subprocess.STDOUT)
  checks.append(dict(stage=tag,returncode=r.returncode,seconds=time.monotonic()-t,log_sha256=sha(log)))
  write(work/'PROGRESS.json',dict(checks=checks))
  assert r.returncode==0,(tag,r.returncode,str(log))
 def equal(generated,pinned):assert Path(generated).read_bytes()==Path(pinned).read_bytes(),('replayed bytes differ',generated,pinned)
 for n in ['pr376-source','pr377-source','candidate','signed']:extract(pkg/'source'/(n+'.tar.gz'),ext/n)
 for f in ext.rglob('MANIFEST.sha256'):manifest(f.parent)
 source=ext/'pr376-source/research';parent=source/'e8-bit-seven-stage';reuse=source/'e8-bit-helper-reuse';cand=ext/'candidate';sig=ext/'signed';cxsource=ext/'pr377-source/nine-stage-complex-e8'
 # Validate full PR377 source enumeration even in quick mode.
 cm=read(cxsource/'MANIFEST.json');actual={str(f.relative_to(cxsource)):sha(f) for f in cxsource.rglob('*') if f.is_file() and f!=cxsource/'MANIFEST.json'};assert actual==cm['files']
 pin=read(reuse/'SOURCE.json');assert sha(parent/'MANIFEST.sha256')==pin['parent']['manifest_sha256']
 for name,h in pin['parent']['files'].items():assert sha(parent/name)==h
 assert sha(reuse/'frame-selection.json')==pin['frame_selection_sha256'] and sha(reuse/'reuse-selection.json')==pin['reuse_selection_sha256']
 frame=load('source_frame',reuse/'frame_replay.py');helpers=load('source_reuse',reuse/'reuse_replay.py');select=load('source_B',cand/'reconstruct.py')
 original=(parent/pin['word']).read_bytes();frames=read(reuse/'frame-selection.json');reuse_witness=read(reuse/'reuse-selection.json')
 retimed=frame.reconstruct(original,frames);base=helpers.reconstruct(retimed,reuse_witness)
 assert hashlib.sha256(base).hexdigest()==read(reuse/'EXPECTED.json')['word_sha256']
 assert base==(cand/'frozen376.json').read_bytes()==gzip.decompress((pkg/'source/base376-word.json.gz').read_bytes())
 controls=frame.negative_controls(original,frames)+helpers.negative_controls(retimed,reuse_witness)
 word=select.reconstruct(base,read(cand/'B-SELECTION.json'));assert word==gzip.decompress((cand/'candidate-word.json.gz').read_bytes())
 run('B-reconstruction',[cand/'reconstruct.py',cand/'frozen376.json',cand/'B-SELECTION.json',cand/'reproduced-word.json.gz'])
 equal(cand/'reproduced-word.json.gz',cand/'candidate-word.json.gz');equal(sig/'word.json.gz',cand/'candidate-word.json.gz')
 assert sha(pkg/'source/base376-word.json.gz')=='afc06ddb9dbba1eeb59f83eb03c36421d6cc439ca261ab4c58e9074e023cc7d8'
 assert sha(pkg/'source/parent376-finite.json')=='73e8cb0e54100152363f3456775467924e1c2819a9bc2e9fad1d29de555f630d'
 assert read(pkg/'source/parent376-finite.json')==read(reuse/'EXPECTED.json')['finite']
 pricing=parent/'code/pricing';checkers=parent/'code/bit/checkers'
 fresh_complex=work/'complex';records=work/'records';lowering=work/'lowering';ind=work/'independent';ind.mkdir()
 signed_result=pkg/'proof/signed/RESULT-PORTABLE.json';finite=pkg/'proof/finite.json'
 if not a.quick:
  run('candidate-export',[parent/'code/bit/export_records.py',cand/'candidate-word.json.gz',records])
  for n in ['249-records.bin','249-states.json','frames.json']:
   equal(records/n,cand/'records'/n);equal(records/n,sig/'records'/n)
  run('candidate-checkword',[parent/'code/bit/independent/checkword.py',cand/'candidate-word.json.gz',pricing])
  run('candidate-word-mutations',[parent/'code/bit/independent/mutate.py',cand/'candidate-word.json.gz',pricing])
  run('both-frame-ledgers',[cand/'audit.py'])
  run('candidate-gram',[checkers/'gram_frames.py',records,'--gram','e8ham','--h','8','--positive'])
  run('candidate-geometry',[checkers/'geometry_k.py','3',cand/'candidate-word.json.gz'])
  run('candidate-banks',[checkers/'tile_k.py',records,'3','8','7'])
  run('candidate-price',[checkers/'certify_bit_k.py',records,'999240641319551/1000000000000000000','3','8','7',work/'price.json'])
  price=read(work/'price.json');oldprice=read(pkg/'proof/price/kappa.json');price.pop('word');oldprice.pop('word');assert price==oldprice
  run('signed-source',[sig/'audit_signed_source.py'],sig)
  for n in ['signed-records.bin','decoder-and-dirt.json']:equal(sig/n,pkg/'proof/signed'/n)
  portable=normalized_signed(read(sig/'RESULT.json'));assert portable==read(signed_result)
  signed_result=work/'SIGNED-PORTABLE.json';write(signed_result,portable)
  run('all-local-reflected-charts',[pkg/'code/local_charts.py','--output',ind,'--frames',records/'frames.json','--charts',pkg/'proof/charts/ALL-CHARTS.json'])
  equal(ind/'LOCAL-CHARTS.json',pkg/'proof/independent/LOCAL-CHARTS.json')
  run('seven-stage-lowering',[pkg/'code/lower_and_bank7.py','--records',records,'--charts',pkg/'proof/charts','--price',pkg/'proof/price/kappa.json','--output',lowering])
  for n in ['GLOBAL-PROGRAM.bin','BANK-SLOTS.json','LOWERING-BANKS.json']:equal(lowering/n,pkg/'proof/lowering'/n)
  run('all-idle-gap-links',[pkg/'code/idle_links.py','--output',ind,'--geometry',checkers/'geometry_k.py','--word',cand/'candidate-word.json.gz'])
  equal(ind/'IDLE-GAP-LINKS.json',pkg/'proof/independent/IDLE-GAP-LINKS.json')
  run('independent-IR',[pkg/'code/check_ir.py','--output',ind,'--lowering',lowering,'--charts',pkg/'proof/charts/ALL-CHARTS.json','--records',records])
  for n in ['RESULT.json','DATA-FAMILY-MAP.json']:equal(ind/n,pkg/'proof/independent'/n)
  finite=work/'FINITE.json'
  run('fresh-finite-and-routes',[pkg/'code/finite.py','--parent',parent,'--word',cand/'candidate-word.json.gz','--base-word',pkg/'source/base376-word.json.gz','--priced',pkg/'proof/price/kappa.json','--lowering',lowering/'LOWERING-BANKS.json','--raw-records',records/'249-records.bin','--signed-records',sig/'signed-records.bin','--signed-result',signed_result,'--parent-finite',pkg/'source/parent376-finite.json','--output',finite])
  equal(finite,pkg/'proof/finite.json')
  run('fresh-complex-supplier',[cxsource/'verify.py','--work',fresh_complex])
  vc=read(fresh_complex/'VERIFICATION.json');assert vc['source_manifest_sha256']==sha(cxsource/'MANIFEST.json')
  for name,h in vc['receipt_sha256'].items():assert sha(fresh_complex/'work/complex-nine-native'/name)==h
 else:
  # Historical assembly is explicitly limited to quick mode; full mode never
  # overlays the supplier's freshly emitted receipts with archived ones.
  fresh_complex.mkdir();shutil.copytree(cxsource/'work',fresh_complex/'work')
  shutil.copytree(pkg/'proof/complex/cp312/work',fresh_complex/'work',dirs_exist_ok=True)
  shutil.copy(pkg/'proof/complex/cp312/VERIFICATION.json',fresh_complex/'VERIFICATION.json')
 assembled=work/'ASSEMBLY.json'
 run('exact-assembly',[pkg/'code/assemble.py','--parent',parent,'--priced',pkg/'proof/price/kappa.json','--finite',finite,'--complex-proof',fresh_complex,'--output',assembled])
 equal(assembled,pkg/'proof/assembly/ASSEMBLY.json');exact=read(assembled)
 assert exact['kappa']=='124243257674225949446409/125000000000000000000000000' and exact['adjacent_grid_rejected'] and exact['complex_leaf_cap_rejected']
 out=dict(status='PASS_PORTABLE_E8_SEVEN_NINE_QUICK_INTEGRITY' if a.quick else 'PASS_FRESH_PORTABLE_E8_SEVEN_NINE_COMPLETE_REPLAY',quick=a.quick,python=sys.version,checks=checks,source_mutation_controls=controls,package_manifest_sha256=sha(pkg/'MANIFEST.sha256'),candidate_sha256=sha(cand/'candidate-word.json.gz'),assembly_sha256=sha(assembled),kappa=exact['kappa'],seconds=time.monotonic()-started,scope='Finite reproducible composition under inherited compiler, chart, bank, precision/recovery and analytic interfaces; no new all-size compiler or Lean multiplication proof.')
 if not a.quick:out['fresh_complex_verification_sha256']=sha(fresh_complex/'VERIFICATION.json');out['fresh_signed_result_sha256']=sha(sig/'RESULT.json');out['fresh_finite_sha256']=sha(finite)
 write(work/'VERIFICATION.json',out);print(out['status'],flush=True)
if __name__=='__main__':main()
