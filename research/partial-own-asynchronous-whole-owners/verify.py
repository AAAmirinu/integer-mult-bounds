"""Offline fresh suppliers, partial-own physics and asynchronous owner admission.
Prepared by OpenAI Codex; no optimizer and no cached supplier outputs.
"""
from pathlib import Path
from fractions import Fraction
import argparse,gzip,hashlib,json,os,subprocess,sys,time

assert __debug__
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('out',type=Path)
parser.add_argument('--boost-include',type=Path,required=True);parser.add_argument('--cxx',default='c++')
args=parser.parse_args();OUT=args.out.resolve()
assert sys.version_info[:2]==(3,14),'Use Python 3.14, as required by the pinned supplier'
assert not OUT.exists()and not OUT.is_relative_to(ROOT)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def integrity():
 inventory={str(p.relative_to(ROOT)):sha(p)for p in ROOT.rglob('*')if p.is_file()and p!=ROOT/'MANIFEST.json'and '__pycache__'not in p.parts}
 assert inventory==read(ROOT/'MANIFEST.json'),'Complete package manifest'
 for f,z in read(ROOT/'SOURCE.json')['files'].items():assert sha(ROOT/f)==z['sha256'],f
integrity();OUT.mkdir();steps=[]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1');env.pop('PYTHONOPTIMIZE',None)
def run(name,script,*argv):
 t=time.monotonic();log=OUT/(name+'.log');print('RUN',name,flush=True)
 with log.open('w')as f:r=subprocess.run([sys.executable,'-B','-u',str(script),*map(str,argv)],env=env,stdout=f,stderr=subprocess.STDOUT)
 steps.append(dict(name=name,exit_code=r.returncode,seconds=round(time.monotonic()-t,3),log_sha256=sha(log)))
 (OUT/'STEPS.json').write_text(json.dumps(steps,indent=2)+'\n')
 assert r.returncode==0,(name,log.read_text()[-6000:]);print('PASS',name,flush=True)

try:
 dep=OUT/'dependency';p507=ROOT/'vendor/pr507';p505=ROOT/'vendor/pr505'
 run('fresh-both-suppliers-and-partial-own',p507/'verify.py',dep,'--boost-include',args.boost_include,'--cxx',args.cxx)
 receipt=read(dep/'RECEIPT.json');assert receipt['status']=='PASS_FRESH_R489_PARTIAL_OWN_KERNEL84_WHOLE_COMPLEX'
 assert receipt['exact_math_sha256']==sha(dep/'EXACT-MATH.json')
 variant=dep/'retimed/gauge80-kernel42';expected=read(ROOT/'EXPECTED.json')
 anchors={}
 for key,file in [('canonical_word_sha256','CANONICAL-WORD.json.gz'),('local_program_sha256','LOCAL-PROGRAMS.json.gz')]:
  anchors[key]=hashlib.sha256(gzip.decompress((variant/'split-centres'/file).read_bytes())).hexdigest()
  assert anchors[key]==expected[key],key
 bit=read(dep/'bit/RESULT.json');cited=read(p505/'inputs/PR493-EXPECTED.json')['eleven']
 assert Fraction(bit['bit_lower'])==Fraction(cited['bit_lower'])
 assert bit['bit_profile']==cited['profile']and bit['bit']==cited['bit']
 assert bit['emitted_program_sha256']==cited['emitted_program_sha256']
 freshbit=OUT/'FRESH-BIT-INPUT.json'
 freshbit.write_text(json.dumps({'eleven':dict(bit_lower=bit['bit_lower'],profile=bit['bit_profile'],bit=bit['bit'],emitted_program_sha256=bit['emitted_program_sha256'])},sort_keys=True,indent=2)+'\n')
 plan=read(ROOT/'data/PLAN.json');sourceplan=read(ROOT/'references/PR473-ORDER.json')
 assert plan['order']==sourceplan['order']and plan['windows']==sourceplan['windows']
 audit=OUT/'admission';audit.mkdir();host=OUT/'hosted'
 run('emit-asynchronous',ROOT/'code/emit_partial_async.py',p507/'vendor/complex/e8-complex-gauge-kernel',variant,ROOT/'data/OWNERS.json.gz',ROOT/'data/PLAN.json',host)
 run('independent-controller',p505/'code/audit_async.py',variant,host,audit/'ASYNC-AUDIT.json')
 run('finite-invoice',p505/'code/audit_async_invoice.py',audit,variant,host)
 run('two-exact-engines-and-outer',p505/'code/assemble.py',audit,variant,host,freshbit)
 a=read(audit/'EXACT-ASSEMBLY.json');h=read(host/'HOSTED.json');inv=read(audit/'PREFIX-AND-INVOICE.json');prefix=read(audit/'GLOBAL-PREFIX.json')
 result={k:a[k]for k in ['complex_lower','next_b_rejected','bit_lower','kappa','kappa_decimal','binding_component','bit_charged_three_level_coefficient_bits','external_row_allowance','strict_outer_constraints','outer_controls','bootstrap']}
 result.update(status='PASS_FRESH_PARTIAL_OWN_ASYNCHRONOUS_WHOLE_OWNER',**anchors,
               asynchronous_template_sha256=h['template_sha256'],global_profile=h['global_profile'],live=h['live'],physical=h['physical'],
               dependency_exact_math_sha256=sha(dep/'EXACT-MATH.json'),source_manifest_sha256=sha(ROOT/'MANIFEST.json'),
               bit_scope='PR493 operator freshly reconstructed by the portability-fixed PR507 dependency; actual bit profile, invoice and program hash bound to the asynchronous assembly.',
               complex_scope='Fresh partial-own factory/kernel84 scalar, frame, guarded physical and whole-owner asynchronous controller/invoice replay; inherited all-size and analytic conditions remain.')
 for key,value in expected.items():assert result[key]==value,(key,result.get(key),value)
 (OUT/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 integrity()
 files=['RESULT.json','FRESH-BIT-INPUT.json','dependency/RECEIPT.json','dependency/EXACT-MATH.json','dependency/RELEASE-ADMISSION.json','dependency/TOOLCHAIN.json','dependency/partial-algebra/ALGEBRA.json','dependency/PARTIAL-FRAME-REVIEW.json','dependency/retimed-guarded/PREOP-GUARDS-lg_instances.json','dependency/retimed-guarded/PREOP-GUARDS-lg_e2e.json','admission/ASYNC-AUDIT.json','admission/OWNERS-AND-PROFILE.json','admission/GLOBAL-PREFIX.json','admission/PREFIX-AND-INVOICE.json','admission/EXACT-ASSEMBLY.json']
 (OUT/'RECEIPT.json').write_text(json.dumps(dict(status=result['status'],python=sys.version.split()[0],steps=steps,source_manifest_sha256=sha(ROOT/'MANIFEST.json'),artifacts={f:sha(OUT/f)for f in files}),indent=2)+'\n')
 print(result['status'],'kappa',result['kappa_decimal'],flush=True)
except BaseException as e:
 (OUT/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps),indent=2)+'\n');raise
