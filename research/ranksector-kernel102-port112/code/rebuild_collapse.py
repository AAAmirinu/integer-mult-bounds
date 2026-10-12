"""Fresh scalar/phase/guarded local admission for the coordinated kernel102 word."""
from pathlib import Path
import concurrent.futures,hashlib,json,os,shutil,subprocess,sys,time,threading
package,parent,construction,out=map(lambda p:Path(p).resolve(),sys.argv[1:5])
source=package/'vendor/complex/e8-complex-gauge-kernel';code=source/'code'
assert not out.exists();out.mkdir(parents=True)
assert json.loads((parent/'RECEIPT.json').read_text())['status']=='PASS_FRESH_PARTIAL_OWN_KERNEL_RETIMED_COMPLEX_WORD'
shutil.copytree(parent/'work',out/'work');shutil.copyfile(parent/'BIT-PRICE.json',out/'BIT-PRICE.json')
(out/'sc_base').mkdir();(out/'split-centres').mkdir();(out/'lemmaG').mkdir()
shutil.copyfile(construction/'RETIMED-BASE.json.gz',out/'sc_base/FULL-WORD.json.gz')
shutil.copyfile(construction/'FULL-WORD.json.gz',out/'split-centres/FULL-WORD.json.gz')
selection=construction/'SELECTION.json';steps=[];lock=threading.Lock()
env=dict(os.environ,PYTHONPATH=str(code),PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');env.pop('PYTHONOPTIMIZE',None)
def run(name,script,*argv,cwd=None,extra=None):
 t=time.monotonic();log=out/(name+'.log');print('RUN',name,flush=True)
 with log.open('w')as f:r=subprocess.run([sys.executable,'-B',str(script),*map(str,argv)],cwd=cwd or out,env=env|dict(extra or{}),stdout=f,stderr=subprocess.STDOUT)
 with lock:
  steps.append(dict(name=name,exit_code=r.returncode,seconds=time.monotonic()-t,log_sha256=hashlib.sha256(log.read_bytes()).hexdigest()));(out/'STEPS.json').write_text(json.dumps(steps,indent=2)+'\n')
 assert r.returncode==0,(name,log.read_text()[-5000:]);print('PASS',name,flush=True)
try:
 run('selection-controls',Path(__file__).resolve().parent/'selection_controls.py',code,out/'sc_base/FULL-WORD.json.gz',selection,out/'CONTROLS-SELECTION.json')
 run('word-controls',code/'controls_gk.py',out/'split-centres/FULL-WORD.json.gz',out/'CONTROLS-WORD.json')
 run('pipeline-controls',code/'controls_pipeline.py',out,selection,out/'CONTROLS-PIPELINE.json')
 run('scalar',code/'audit_gk.py')
 run('programs',code/'emit_gk.py')
 run('phases',source.parent/'split-centres-global/code/complex_phases_full.py')
 run('wrappers',code/'adapters_gk.py',out/'split-centres/CANONICAL-WORD.json.gz',out/'split-centres/RESIDUAL-ADAPTERS.json',out/'LEMMA-A.json')
 run('integrate',code/'integrate_gk.py')
 run('scalar-readback',Path(__file__).resolve().parent/'replay_kernel.py')
 run('common-labels',code/'lemmaG/run_labels.py','gauge80-kernel42',cwd=out/'lemmaG',extra={'LG_BASE':str(out.parent)})
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
  futures=[pool.submit(run,s,package/'code/guarded_lemma.py',source,s+'.py','gauge80-kernel42',cwd=out/'lemmaG',extra={'LG_BASE':str(out.parent)})for s in ['lg_instances','lg_e2e']]
  for f in futures:f.result()
 run('lemma-controls',package/'code/retimed_lemma_mutants.py',source,out.parent,cwd=out/'lemmaG')
 files=['split-centres/FULL-WORD.json.gz','split-centres/CANONICAL-WORD.json.gz','split-centres/LOCAL-PROGRAMS.json.gz','split-centres/LOCAL-CHECKS.json','split-centres/RESIDUAL-ADAPTERS.json','lemmaG/INSTANCES-gauge80-kernel42.json','lemmaG/E2E-gauge80-kernel42.json','lemmaG/MUTANTS.json','lemmaG/PREOP-GUARDS-lg_instances.json','lemmaG/PREOP-GUARDS-lg_e2e.json']
 (out/'RECEIPT.json').write_text(json.dumps(dict(status='PASS_FRESH_PARTIAL_OWN_KERNEL102_GAUGE_COLLAPSE_LOCAL',steps=steps,artifacts={f:hashlib.sha256((out/f).read_bytes()).hexdigest()for f in files},scope='Fresh changed local word scalar, common labels, phases, wrappers, guarded physics and controls. Uses module workspace freshly rebuilt by this package. No new global allocation or assembly admission.'),indent=2)+'\n')
except BaseException as e:
 (out/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps),indent=2)+'\n');raise
