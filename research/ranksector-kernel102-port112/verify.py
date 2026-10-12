"""Offline fresh suppliers, rank-sector kernel102 and112-port whole-owner admission.
Prepared by OpenAI Codex; no optimizer and no cached supplier outputs.
"""
from pathlib import Path
from fractions import Fraction
import argparse,gzip,hashlib,json,os,subprocess,sys,time

if not __debug__:raise RuntimeError('Assertions must remain enabled')
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
 prior=dep/'retimed/gauge80-kernel42'
 construction=OUT/'construction';variant=OUT/'coordinated/gauge80-kernel42'
 run('construct-coordinated',ROOT/'code/construct_collapse.py',p507/'vendor/complex/e8-complex-gauge-kernel',prior,p507/'data/KERNEL-SELECTION.json',ROOT/'data/KERNEL102-SELECTION.json',ROOT/'data/PAIR-SPEC.json',construction)
 run('independent-all-kernel-corrections',ROOT/'code/audit_kernel_scalar.py',construction/'FULL-WORD.json.gz',construction/'SELECTION.json',OUT/'KERNEL-SCALAR.json')
 scalar=read(OUT/'KERNEL-SCALAR.json');assert scalar['kernel_pivots']==102 and scalar['columns_each_orientation']==800
 assert len(scalar['controls'])==102 and scalar['word_sha256']==sha(construction/'FULL-WORD.json.gz')
 run('fresh-coordinated-local',ROOT/'code/rebuild_collapse.py',p507,prior,construction,variant)
 localreceipt=read(variant/'RECEIPT.json');assert localreceipt['status']=='PASS_FRESH_PARTIAL_OWN_KERNEL102_GAUGE_COLLAPSE_LOCAL'
 assert all(s['exit_code']==0 for s in localreceipt['steps'])
 for file,digest in localreceipt['artifacts'].items():assert sha(variant/file)==digest
 expected=read(ROOT/'EXPECTED.json')
 anchors={}
 for key,file in [('parent120_canonical_sha256','CANONICAL-WORD.json.gz'),('parent120_program_sha256','LOCAL-PROGRAMS.json.gz')]:
  anchors[key]=hashlib.sha256(gzip.decompress((variant/'split-centres'/file).read_bytes())).hexdigest()
  assert anchors[key]==expected[key],key
 bit=read(dep/'bit/RESULT.json');cited=read(p505/'inputs/PR493-EXPECTED.json')['eleven']
 assert Fraction(bit['bit_lower'])==Fraction(cited['bit_lower'])
 assert bit['bit_profile']==cited['profile']and bit['bit']==cited['bit']
 assert bit['emitted_program_sha256']==cited['emitted_program_sha256']
 freshbit=OUT/'FRESH-BIT-INPUT.json'
 freshbit.write_text(json.dumps({'eleven':dict(bit_lower=bit['bit_lower'],profile=bit['bit_profile'],bit=bit['bit'],emitted_program_sha256=bit['emitted_program_sha256'])},sort_keys=True,indent=2)+'\n')
 plan=read(ROOT/'data/PLAN.json');sourceplan=read(ROOT/'references/PR508-ORDER.json')
 assert plan['order']==sourceplan['order']and plan['windows']==sourceplan['windows']
 audit=OUT/'admission';audit.mkdir();host=OUT/'hosted';local112=OUT/'local112';base112=OUT/'base112'
 r523=ROOT/'references/pr523';G=p507/'vendor/complex/e8-complex-gauge-kernel'
 run('restrict-local112',r523/'build_port112.py',variant/'split-centres',local112)
 run('exact-word-transport112',r523/'audit_port112_transport.py',local112)
 run('emit-local112',r523/'emit_local112.py',local112)
 run('independent-local112',r523/'audit_local112.py',local112)
 run('literal-guarded-program-projection',ROOT/'code/audit_program_projection.py',variant,local112,audit/'PROGRAM-PROJECTION.json')
 run('exact-local-phases112',r523/'phases_local112.py',local112,p507/'vendor/complex/split-centres-global/vendor')
 run('residual-wrappers112',G/'code/adapters_gk.py',local112/'CANONICAL-WORD.json.gz',local112/'RESIDUAL-ADAPTERS.json',local112/'LEMMA-A.json')
 run('restrict-global112',r523/'restrict_global.py',variant,local112,base112)
 run('independent-global-restriction',ROOT/'code/audit_global_restriction.py',variant,base112,audit/'GLOBAL-RESTRICTION-AUDIT.json')
 for key,file in [('canonical_word_sha256','CANONICAL-WORD.json.gz'),('local_program_sha256','LOCAL-PROGRAMS.json.gz')]:
  anchors[key]=hashlib.sha256(gzip.decompress((local112/file).read_bytes())).hexdigest()
  assert anchors[key]==expected[key],key
 run('emit-asynchronous',r523/'emit_async.py',G,base112,ROOT/'data/OWNERS.json.gz',ROOT/'data/PLAN.json',host)
 run('independent-controller',r523/'audit_async.py',base112,host,audit/'ASYNC-AUDIT.json')
 run('independent-raw-reconstruction',ROOT/'code/audit_112_independent.py','--original-base',variant,'--local',local112,'--owners',ROOT/'data/OWNERS.json.gz','--out',audit)
 run('finite-invoice',ROOT/'code/audit_async_invoice.py',audit,base112,host)
 run('two-exact-engines-and-outer',r523/'assemble.py',audit,base112,host,freshbit)
 a=read(audit/'EXACT-ASSEMBLY.json');h=read(host/'HOSTED.json');inv=read(audit/'PREFIX-AND-INVOICE.json');prefix=read(audit/'GLOBAL-PREFIX.json')
 result={k:a[k]for k in ['complex_lower','next_b_rejected','bit_lower','kappa','kappa_decimal','binding_component','bit_charged_three_level_coefficient_bits','external_row_allowance','strict_outer_constraints','outer_controls','bootstrap']}
 raw=read(audit/'INDEPENDENT112-RAW-AUDIT.json')
 assert raw['paid_profile']==h['global_profile'] and (raw['whole_owner_roles'],raw['live'],raw['physical'],raw['deficit'])==(40320,7168,7738,2560)
 assert inv['global_prefix_bits']==prefix['global_prefix_bits']==210 and inv['charged_prefix_bits']==512
 result.update(status='PASS_FRESH_RANKSECTOR_KERNEL102_PORT112',**anchors,
               asynchronous_template_sha256=h['template_sha256'],global_profile=h['global_profile'],live=h['live'],physical=h['physical'],
               dependency_exact_math_sha256=sha(dep/'EXACT-MATH.json'),source_manifest_sha256=sha(ROOT/'MANIFEST.json'),
               bit_scope='PR493 operator freshly reconstructed by the portability-fixed PR507 dependency; actual bit profile, invoice and program hash bound to the asynchronous assembly.',
               complex_scope='Fresh PR522 rank-sector factory with kernel102, guarded120 physics and literal disjoint112 projection, exact phases, whole owners, independent raw global and finite invoice replay. Inherited all-size and analytic conditions remain.')
 for key,value in expected.items():assert result[key]==value,(key,result.get(key),value)
 (OUT/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 integrity()
 files=['admission/PROGRAM-PROJECTION.json','admission/GLOBAL-RESTRICTION-AUDIT.json','admission/INDEPENDENT112-RAW-AUDIT.json','local112/RESTRICTION.json','local112/TRANSPORT.json','local112/INDEPENDENT-LOCAL-REPLAY.json','local112/CLIFFORD-REVIEW.json','KERNEL-SCALAR.json','construction/CONSTRUCTION.json','coordinated/gauge80-kernel42/RECEIPT.json','coordinated/gauge80-kernel42/lemmaG/PREOP-GUARDS-lg_instances.json','coordinated/gauge80-kernel42/lemmaG/PREOP-GUARDS-lg_e2e.json','coordinated/gauge80-kernel42/lemmaG/MUTANTS.json','RESULT.json','FRESH-BIT-INPUT.json','dependency/RECEIPT.json','dependency/EXACT-MATH.json','dependency/RELEASE-ADMISSION.json','dependency/TOOLCHAIN.json','dependency/partial-algebra/ALGEBRA.json','dependency/PARTIAL-FRAME-REVIEW.json','dependency/retimed-guarded/PREOP-GUARDS-lg_instances.json','dependency/retimed-guarded/PREOP-GUARDS-lg_e2e.json','admission/ASYNC-AUDIT.json','admission/OWNERS-AND-PROFILE.json','admission/GLOBAL-PREFIX.json','admission/PREFIX-AND-INVOICE.json','admission/EXACT-ASSEMBLY.json']
 (OUT/'RECEIPT.json').write_text(json.dumps(dict(status=result['status'],python=sys.version.split()[0],steps=steps,source_manifest_sha256=sha(ROOT/'MANIFEST.json'),artifacts={f:sha(OUT/f)for f in files}),indent=2)+'\n')
 print(result['status'],'kappa',result['kappa_decimal'],flush=True)
except BaseException as e:
 (OUT/'FAILURE.json').write_text(json.dumps(dict(error=repr(e),steps=steps),indent=2)+'\n');raise
