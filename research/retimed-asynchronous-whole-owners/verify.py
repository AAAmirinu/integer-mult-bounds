"""Fresh retimed local physics and asynchronous whole-owner composition.

The unchanged PR493 bit operator is a pinned dependency; its published profile
is repriced, not reconstructed here. No cached complex receipts are accepted.
"""
from pathlib import Path
import argparse, concurrent.futures, gzip, hashlib, json, os
import shutil, subprocess, sys, threading, time

if not __debug__:raise RuntimeError('Assertions must remain enabled')
if sys.version_info[:2] not in [(3,13),(3,14)]:
    raise RuntimeError('Use Python 3.13 or 3.14 for pinned gzip byte anchors')
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('out',type=Path)
args=parser.parse_args();OUT=args.out.resolve()
assert not OUT.exists() and not OUT.is_relative_to(ROOT)
PARENT=ROOT/'vendor/pr505'
CPKG=ROOT/'vendor/complex/e8-complex-gauge-kernel'
CODE=CPKG/'code';LG=CODE/'lemmaG'
SEL=CPKG/'data/selections/gauge80-kernel42.json'
def read(p):
    raw=p.read_bytes()
    return json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def integrity():
    actual={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*')
            if p.is_file() and p!=ROOT/'MANIFEST.json' and '__pycache__' not in p.parts}
    assert actual==read(ROOT/'MANIFEST.json'),'complete source manifest'
    for name,record in read(ROOT/'SOURCE.json')['files'].items():
        assert sha(ROOT/name)==record['sha256'],name
integrity();OUT.mkdir(parents=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',
         OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
env.pop('PYTHONOPTIMIZE',None)
steps=[];lock=threading.Lock()
def run(name,script,*argv,cwd=None,extra=None):
    start=time.monotonic();log=OUT/(name+'.log');print('RUN',name,flush=True)
    with log.open('w',encoding='utf-8',newline='\n') as stream:
        p=subprocess.run([sys.executable,'-B',str(script),*map(str,argv)],cwd=cwd,
                         env=env|dict(extra or {}),stdout=stream,stderr=subprocess.STDOUT)
    with lock:
        steps.append(dict(name=name,exit_code=p.returncode,seconds=round(time.monotonic()-start,3),log_sha256=sha(log)))
        (OUT/'STEPS.json').write_text(json.dumps(steps,indent=2)+'\n')
    assert p.returncode==0,(name,log.read_text()[-6000:])
    print('PASS',name,flush=True)

try:
    var=OUT/'gauge80-kernel42';var.mkdir()
    shutil.copytree(PARENT/'inputs/work',var/'work')
    for name in ['sc_base','split-centres']:(var/name).mkdir()
    bit=read(PARENT/'inputs/PR493-EXPECTED.json')['eleven']
    (var/'BIT-PRICE.json').write_text(json.dumps({'lower':bit['bit_lower'],'scope':'PR493 pinned published supplier'})+'\n')
    run('transfer',ROOT/'code/build_retimed.py',CPKG,PARENT/'inputs/BASE-WORD.json.gz',
        ROOT/'data/PR495-FULL-WORD.json.gz',OUT/'transfer')
    shutil.copyfile(OUT/'transfer/RETIMED-BASE.json.gz',var/'sc_base/FULL-WORD.json.gz')
    shutil.copyfile(OUT/'transfer/FULL-WORD.json.gz',var/'split-centres/FULL-WORD.json.gz')
    run('word-controls',CODE/'controls_gk.py',var/'split-centres/FULL-WORD.json.gz',var/'WORD-CONTROLS.json')
    run('selection-controls',CODE/'controls_sel.py',var/'sc_base/FULL-WORD.json.gz',SEL,var/'SELECTION-CONTROLS.json')
    run('pipeline-controls',CODE/'controls_pipeline.py',var,SEL,var/'PIPELINE-CONTROLS.json')
    run('scalar',CODE/'audit_gk.py',cwd=var)
    run('programs',CODE/'emit_gk.py',cwd=var)
    anchor=read(ROOT/'data/PR502-RESULT.json')
    assert sha(var/'split-centres/CANONICAL-WORD.json.gz')==anchor['canonical_word_sha256']
    assert sha(var/'split-centres/LOCAL-PROGRAMS.json.gz')==anchor['local_program_sha256']
    run('phases',PARENT/'vendor/complex/split-centres-global/code/complex_phases_full.py',cwd=var)
    run('wrappers',CODE/'adapters_gk.py',var/'split-centres/CANONICAL-WORD.json.gz',var/'split-centres/RESIDUAL-ADAPTERS.json',var/'LEMMA-A.json',cwd=var)
    run('integrate',CODE/'integrate_gk.py',cwd=var)
    run('scalar-readback',CODE/'replay_gk.py',cwd=var)
    plan=OUT/'ASYNC-RETIMED.json'
    run('plan-transfer',ROOT/'code/build_plan.py',CPKG,PARENT/'inputs/BASE-WORD.json.gz',
        var/'split-centres/FULL-WORD.json.gz',PARENT/'inputs/ASYNC-3.json',plan,OUT/'PLAN-TRANSFER.json')
    host=var/'hosted';audit=OUT/'admission';audit.mkdir()
    run('async-emit',PARENT/'code/emit_async.py',CPKG,var,PARENT/'inputs/ASYNC-OWNERS.json.gz',plan,host)
    run('async-controller',PARENT/'code/audit_async.py',var,host,audit/'ASYNC-AUDIT.json')
    controller=read(audit/'ASYNC-AUDIT.json')
    assert controller['complete_invocations']==72 and controller['complex_hosted_residuals']==40320
    assert len(controller['mutations_rejected'])==19

    lemma=OUT/'lemmaG';lemma.mkdir()
    extra=dict(LG_BASE=str(OUT),PYTHONPATH=str(LG))
    run('gaussian-selftest','-c','import lg_phys as P; from gd import selftest; assert selftest(P.ce)==19',extra=extra)
    run('common-labels',LG/'run_labels.py','gauge80-kernel42',cwd=lemma,extra=extra)
    labels=read(lemma/'LABELS-gauge80-kernel42.json')['gauge80-kernel42']
    assert all(labels[o]['n_label_violations']==0 and not labels[o]['scalar_violations'] for o in ['forward','backward'])
    assert labels['calls']['n']==72 and labels['calls']['ok']
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(run,name,ROOT/'code/guarded_lemma.py',CPKG,script,'gauge80-kernel42',cwd=lemma,extra=extra)
                 for name,script in [('all-instance-columns','lg_instances.py'),('whole-program','lg_e2e.py')]]
        for future in futures:future.result()
    instances=read(lemma/'INSTANCES-gauge80-kernel42.json')
    assert all(not instances[k]['failures'] for k in ['I-tr','I-comp','I-centre','I-helper'])
    assert instances['I-tr']['transitions']==2945
    assert instances['I-helper']['entering_helpers']==122 and instances['I-helper']['columns_each']==512
    e2e=read(lemma/'E2E-gauge80-kernel42.json')
    assert e2e['status']=='PASS' and not e2e['failures'] and e2e['columns']==806 and e2e['dense']==8
    run('lemma-controls',ROOT/'code/lg_mutants_retimed.py',cwd=lemma,extra=extra)
    controls=read(lemma/'MUTANTS.json')
    assert len(controls)==14 and all(c['rejected'] for c in controls)
    run('finite-invoice',PARENT/'code/audit_async_invoice.py',audit,var,host)
    run('exact-assembly',PARENT/'code/assemble.py',audit,var,host,PARENT/'inputs/PR493-EXPECTED.json')
    assembly=read(audit/'EXACT-ASSEMBLY.json');owners=read(audit/'OWNERS-AND-PROFILE.json')
    result={k:assembly[k] for k in ['complex_lower','next_b_rejected','bit_lower','kappa','kappa_decimal',
            'binding_component','strict_outer_constraints','outer_controls','bootstrap','external_row_allowance',
            'bit_charged_three_level_coefficient_bits']}
    result.update(status='PASS_FRESH_RETIMED_ASYNCHRONOUS_WHOLE_OWNER',
                  global_profile=owners['paid_profile'],live=owners['live'],physical=owners['physical'],
                  canonical_word_sha256=sha(var/'split-centres/CANONICAL-WORD.json.gz'),
                  local_program_sha256=sha(var/'split-centres/LOCAL-PROGRAMS.json.gz'),
                  asynchronous_template_sha256=read(host/'HOSTED.json')['template_sha256'],
                  global_prefix_bits=read(audit/'GLOBAL-PREFIX.json')['global_prefix_bits'],
                  source_manifest_sha256=sha(ROOT/'MANIFEST.json'),
                  bit_scope='Pinned PR493 operator reused; its published profile is independently repriced by both moment engines.')
    for key,value in read(ROOT/'EXPECTED.json').items():assert result[key]==value,(key,result.get(key),value)
    integrity()
    (OUT/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    names=['RESULT.json','transfer/TRANSFER.json','PLAN-TRANSFER.json','admission/ASYNC-AUDIT.json',
           'admission/PREFIX-AND-INVOICE.json','admission/EXACT-ASSEMBLY.json','admission/GLOBAL-PREFIX.json',
           'lemmaG/INSTANCES-gauge80-kernel42.json','lemmaG/E2E-gauge80-kernel42.json',
           'lemmaG/PREOP-GUARDS-lg_instances.json','lemmaG/PREOP-GUARDS-lg_e2e.json','lemmaG/MUTANTS.json']
    (OUT/'RECEIPT.json').write_text(json.dumps(dict(status=result['status'],python=sys.version.split()[0],
         steps=steps,artifacts={name:sha(OUT/name) for name in names}),indent=2)+'\n')
    print(result['status'],'kappa',result['kappa_decimal'],flush=True)
except BaseException as error:
    (OUT/'FAILURE.json').write_text(json.dumps(dict(error=repr(error),steps=steps),indent=2)+'\n')
    raise
