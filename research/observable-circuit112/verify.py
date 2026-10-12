"""Offline full reconstruction of the observable/circuit 112-port derivative."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,json,gzip,hashlib,os,sys,shutil,subprocess,time
if not __debug__:raise RuntimeError('Assertions must remain enabled; optimized Python is unsupported')
sys.dont_write_bytecode=True;sys.set_int_max_str_digits(0)
P=Path(__file__).resolve().parent;a=argparse.ArgumentParser();a.add_argument('--work',type=Path,required=True);args=a.parse_args();W=args.work.resolve()
assert W!=P and P not in W.parents and not W.exists()
mf=P/'MANIFEST.json'
assert mf.is_file() and (P/'EXPECTED.json').is_file(), 'Required manifest or expected result is missing'
if mf.exists():
 m=json.loads(mf.read_text(encoding='utf-8'));assert m['format']=='sha256-lf-text-v1'
 for name,z in m['files'].items():
  f=P/name;assert P in f.resolve().parents;d=f.read_bytes();assert z['mode']in['lf-text','raw'];d=d.replace(b'\r\n',b'\n')if z['mode']=='lf-text'else d;assert hashlib.sha256(d).hexdigest()==z['sha256'],name
W.mkdir(parents=True);V=P/'vendor/base120';C=V/'vendor/complex';G=C/'e8-complex-gauge-kernel';B=W/'source120/base';B.mkdir(parents=True);A=W/'audit';A.mkdir();L=W/'local112';N=W/'base112';H=W/'hosted'
shutil.copytree(V/'inputs/work',B/'work')
for f in (B/'work').rglob('*'):
 if f.is_file()and f.suffix in {'.json','.txt','.md','.py','.sh'}:f.write_bytes(f.read_text(encoding='utf-8').encode('utf-8'))
bit=json.loads((V/'inputs/PR493-EXPECTED.json').read_text());(B/'BIT-PRICE.json').write_text(json.dumps({'lower':bit['eleven']['bit_lower'],'scope':'Unchanged cited PR493 bit supplier'}))
env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',TEMP=str(W),TMP=str(W));env.pop('PYTHONOPTIMIZE',None);steps=[]
def run(name,script,*argv):
 t=time.monotonic();print('RUN',name,flush=True)
 with (W/(name+'.log')).open('w',encoding='utf-8',newline='\n')as log:r=subprocess.run([sys.executable,'-B',str(V/'code/run_portable.py'),str(script),*map(str,argv)],cwd=B,env=env,stdout=log,stderr=subprocess.STDOUT)
 steps.append(dict(stage=name,exit=r.returncode,seconds=time.monotonic()-t));(W/'STEPS.json').write_text(json.dumps(steps,indent=2)+'\n')
 if r.returncode:print((W/(name+'.log')).read_text(encoding='utf-8')[-6000:]);raise SystemExit(r.returncode)
 print('PASS',name,flush=True)
run('01-factory',V/'code/construct_partial.py',B/'work/complex-network/hamming',B/'partial-base')
run('02-kernel92-ancestry',V/'code/build_kernel92.py',G/'code',B/'partial-base/FULL-WORD.json.gz',V/'inputs/KERNEL84-SELECTION.json',V/'inputs/RETIME-FRAMES.json.gz',V/'inputs/KERNEL92-SELECTION.json',B/'reference-kernel92')
run('03-pair35-ancestry',V/'code/build_pair35.py',V/'code/construct_partial.py',B/'work/complex-network/hamming',G/'code',B/'partial-base/FULL-WORD.json.gz',B/'reference-kernel92/RETIMED-BASE.json.gz',V/'inputs/PAIR-SPEC.json',V/'inputs/PAIR-SELECTION.json',B/'reference-pair35')
run('04-ranksector-ancestry',V/'code/build_ranksector.py',B/'work/complex-network/hamming',G/'code',B/'reference-pair35/factory/FULL-WORD.json.gz',B/'reference-pair35/RETIMED-BASE.json.gz',V/'inputs/PAIR-SPEC.json',V/'inputs/PAIR-SELECTION.json',B/'reference-ranksector')
run('05-lemma1-circuit-retirement',P/'code/build_circuit_retirement.py',G/'code',B/'reference-ranksector',P/'inputs/SELECTION.json',B/'retired')
run('06-lemma2-observable-slice',P/'code/slice_reversible.py',B/'retired/FULL-WORD.json.gz',B/'sliced')
run('07-install-sliced-word',P/'code/install_sliced_word.py',G/'code',B/'retired',B/'sliced',B/'split-centres')
run('08-exact-scalar-controls',V/'code/audit_kernel_scalar.py',B/'split-centres/FULL-WORD.json.gz',B/'split-centres/SELECTION.json',A/'KERNEL-SCALAR.json')
run('09-scalar',G/'code/audit_gk.py')
run('10-emit-source120',G/'code/emit_gk.py')
run('11-source-phases',C/'split-centres-global/code/complex_phases_full.py')
run('12-source-wrappers',G/'code/adapters_gk.py',B/'split-centres/CANONICAL-WORD.json.gz',B/'split-centres/RESIDUAL-ADAPTERS.json',B/'LEMMA-A.json')
run('13-source-integration',G/'code/integrate_gk.py')
run('14-source-replay',G/'code/replay_gk.py')
run('15-lemma3-isolated-restriction',P/'code/build_port112.py',B/'split-centres',L)
run('16-exact-word-transport',P/'code/audit_port112_transport.py',L)
run('17-emit-local112',P/'code/emit_local112.py',L)
run('18-independent-local112',P/'code/audit_local112.py',L)
run('19-local112-phases',P/'code/phases_local112.py',L,C/'split-centres-global/vendor')
run('20-local112-wrappers',G/'code/adapters_gk.py',L/'CANONICAL-WORD.json.gz',L/'RESIDUAL-ADAPTERS.json',L/'LEMMA-A.json')
run('21-restrict-global',P/'code/restrict_global.py',B,L,N)
run('22-independent-global',P/'code/audit_global_restriction.py',B,N,A/'GLOBAL-RESTRICTION-AUDIT.json')
run('23-lemma4-emit-whole-owners',P/'code/emit_async.py',G,N,P/'inputs/OWNERS.json.gz',P/'inputs/PLAN.json',H)
run('24-independent-whole-owners',P/'code/audit_async.py',N,H,A/'ASYNC-AUDIT.json')
run('25-independent-raw112',P/'code/audit_112_independent.py','--original-base',B,'--local',L,'--owners',P/'inputs/OWNERS.json.gz','--out',A)
run('26-actual-prefix-invoice',P/'code/audit_async_invoice.py',A,N,H)
run('27-two-moments-assembly',P/'code/assemble.py',A,N,H,V/'inputs/PR493-EXPECTED.json')
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
x=read(A/'EXACT-ASSEMBLY.json');h=read(H/'HOSTED.json');own=read(A/'OWNERS-AND-PROFILE.json');raw=read(A/'INDEPENDENT112-RAW-AUDIT.json');assert h['global_profile']==own['paid_profile']==raw['paid_profile']
assert len(x['strict_outer_constraints'])==47 and all(Q(v)>0 for v in x['strict_outer_constraints'].values())
assert raw['whole_owner_roles']==40320 and raw['no_emitter_or_hosting_checker_imported']and raw['no_nominated_profile_or_windows_used']
for key in ['live','physical','rank_mass','deficit']:assert h[key]==raw[key]
assert len(steps)==27 and all(s['exit']==0 for s in steps)
result=dict(status='PASS_FOUR_LEMMA_OBSERVABLE_CIRCUIT112',kappa=x['kappa'],kappa_decimal=x['kappa_decimal'],complex_lower=x['complex_lower'],bit_lower=x['bit_lower'],template_sha256=x['complex_template_sha256'],global_profile=h['global_profile'],live=h['live'],physical=h['physical'],deficit=h['deficit'],stages=steps,strict_constraints=47,whole_owner_roles=40320,scope='Finite conditional construction, four mathematical lemma applications and complete independent replay. Unchanged PR493 bit operator and inherited all-size compiler/common-label/Lemma A/restored-row/precision/tape/analytic-transfer interfaces remain dependencies. No new Lean certification or unconditional multiplication theorem.',package_manifest_sha256=hashlib.sha256(mf.read_bytes()).hexdigest()if mf.exists()else None)
expected=P/'EXPECTED.json'
if expected.exists():
 e=read(expected)
 for key in ['kappa','complex_lower','bit_lower','template_sha256','global_profile']:assert result[key]==e[key],key
(W/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['kappa_decimal'],flush=True)
