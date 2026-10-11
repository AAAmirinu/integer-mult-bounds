"""Fresh whole-owner retiming composition; no cached supplier receipts accepted.
Prepared by OpenAI Codex. Apache-2.0.
"""
import argparse
import concurrent.futures
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import threading
import time

if not __debug__:
    raise RuntimeError('assertions must remain enabled')
if sys.version_info[:2] not in [(3, 13), (3, 14)]:
    raise RuntimeError('Use Python 3.13 or 3.14 for the pinned gzip byte anchors')
ROOT = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('out', type=Path)
p.add_argument('--boost-include', type=Path, required=True)
p.add_argument('--cxx', default='c++')
a = p.parse_args()
OUT = a.out.resolve()
assert not OUT.exists() and not OUT.is_relative_to(ROOT)
PARENT = ROOT / 'vendor/pr496'
CPKG = PARENT / 'vendor/complex/e8-complex-gauge-kernel'
CODE = CPKG / 'code'
LG = CODE / 'lemmaG'
SEL = CPKG / 'data/selections/gauge80-kernel42.json'


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrity():
    files = {str(x.relative_to(ROOT)): sha(x) for x in ROOT.rglob('*')
             if x.is_file() and x != ROOT / 'MANIFEST.json' and '__pycache__' not in x.parts}
    assert files == read(ROOT / 'MANIFEST.json'), 'complete root manifest'
    for name, digest in read(ROOT / 'SOURCE.json')['files'].items():
        assert sha(ROOT / name) == digest, name


integrity()
OUT.mkdir(parents=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0',
           PYTHON=sys.executable, BOOST_INCLUDE=str(a.boost_include), CXX=a.cxx,
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1')
env.pop('PYTHONOPTIMIZE', None)
steps, lock = [], threading.Lock()


def run(name, script, *args, cwd=None, extra=None):
    log = OUT / (name + '.log')
    print('RUN', name, flush=True)
    start = time.monotonic()
    with log.open('w') as f:
        result = subprocess.run([sys.executable, '-B', str(script), *map(str, args)],
                                cwd=cwd, env=env | dict(extra or {}), stdout=f, stderr=subprocess.STDOUT)
    with lock:
        steps.append(dict(name=name, exit_code=result.returncode,
                          seconds=round(time.monotonic() - start, 3), log_sha256=sha(log)))
        (OUT / 'STEPS.json').write_text(json.dumps(steps, indent=2) + '\n')
    assert result.returncode == 0, (name, log.read_text()[-6000:])
    print('PASS', name, flush=True)


try:
    # This runs both unchanged suppliers, the original pooled witness, all its
    # finite accounting and controls, and the real Boost arbitrary-int probe.
    run('complete496', PARENT / 'verify.py', OUT / 'parent496',
        '--boost-include', a.boost_include, '--cxx', a.cxx)
    CHANGED = OUT / 'parent496/complex/p442/parent/changed'
    VAR = OUT / 'gauge80-kernel42'
    VAR.mkdir()
    shutil.copytree(CHANGED / 'work', VAR / 'work')
    shutil.copyfile(CHANGED / 'BIT-PRICE.json', VAR / 'BIT-PRICE.json')
    for name in ['sc_base', 'split-centres']:
        shutil.copytree(CHANGED / 'split-centres', VAR / name)
    run('transfer', ROOT / 'code/build_retimed.py', CPKG,
        CHANGED / 'split-centres/FULL-WORD.json.gz',
        ROOT / 'data/PR495-FULL-WORD.json.gz', OUT / 'transfer')
    shutil.copyfile(OUT / 'transfer/RETIMED-BASE.json.gz', VAR / 'sc_base/FULL-WORD.json.gz')
    shutil.copyfile(OUT / 'transfer/FULL-WORD.json.gz', VAR / 'split-centres/FULL-WORD.json.gz')
    run('word-controls', CODE / 'controls_gk.py', VAR / 'split-centres/FULL-WORD.json.gz', VAR / 'WORD-CONTROLS.json')
    run('selection-controls', CODE / 'controls_sel.py', VAR / 'sc_base/FULL-WORD.json.gz', SEL, VAR / 'SELECTION-CONTROLS.json')
    run('pipeline-controls', CODE / 'controls_pipeline.py', VAR, SEL, VAR / 'PIPELINE-CONTROLS.json')
    for name, script in [('scalar', 'audit_gk.py'), ('programs', 'emit_gk.py')]:
        run(name, CODE / script, cwd=VAR)
    run('phases', CPKG.parent / 'split-centres-global/code/complex_phases_full.py', cwd=VAR)
    run('wrappers', CODE / 'adapters_gk.py', VAR / 'split-centres/CANONICAL-WORD.json.gz',
        VAR / 'split-centres/RESIDUAL-ADAPTERS.json', VAR / 'LEMMA-A.json', cwd=VAR)
    run('integrate', CODE / 'integrate_gk.py', cwd=VAR)
    run('scalar-readback', CODE / 'replay_gk.py', cwd=VAR)
    run('base-host', CODE / 'hosted_gk.py', VAR / 'split-centres', VAR / 'hosted',
        '--one-helper-per-family', '--selection', CPKG / 'data/SELECTION.json', '--key', 'complex-gauge80-kernel42', cwd=VAR)
    run('base-host-audit', CODE / 'audit_hosted_gk.py', VAR / 'split-centres', VAR / 'hosted',
        VAR / 'HOSTING-AUDIT.json', '--one-helper-per-family', cwd=VAR)
    run('base-host-controls', CODE / 'controls_hosting.py', VAR, CPKG / 'data/SELECTION.json',
        'complex-gauge80-kernel42', VAR / 'HOSTING-CONTROLS.json')

    lemma = OUT / 'lemmaG'
    lemma.mkdir()
    extra = dict(LG_BASE=str(OUT), PYTHONPATH=str(LG))
    run('gaussian-selftest', '-c', 'import lg_phys as P; from gd import selftest; assert selftest(P.ce)==19', extra=extra)
    run('common-labels', LG / 'run_labels.py', 'gauge80-kernel42', cwd=lemma, extra=extra)
    labels = read(lemma / 'LABELS-gauge80-kernel42.json')['gauge80-kernel42']
    assert all(labels[o]['n_label_violations'] == 0 and not labels[o]['scalar_violations']
               for o in ['forward', 'backward'])
    assert labels['calls']['n'] == 72 and labels['calls']['ok']
    # Every potentially overflowing operation is bounded with Python integers
    # before the unchanged exact Gaussian-dyadic simulator executes it.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(run, name, PARENT / 'code/guarded_lemma.py', CPKG, script,
                               'gauge80-kernel42', cwd=lemma, extra=extra)
                   for name, script in [('all-instance-columns', 'lg_instances.py'), ('whole-program', 'lg_e2e.py')]]
        for future in futures:
            future.result()
    instances = read(lemma / 'INSTANCES-gauge80-kernel42.json')
    assert all(not instances[k]['failures'] for k in ['I-tr', 'I-comp', 'I-centre', 'I-helper'])
    assert instances['I-tr']['transitions'] == 2945
    assert instances['I-helper']['entering_helpers'] == 122 and instances['I-helper']['columns_each'] == 512
    e2e = read(lemma / 'E2E-gauge80-kernel42.json')
    assert e2e['status'] == 'PASS' and not e2e['failures']
    assert e2e['columns'] == 806 and e2e['dense'] == 8
    run('lemma-controls', ROOT / 'code/lg_mutants_retimed.py', cwd=lemma, extra=extra)
    mutants = read(lemma / 'MUTANTS.json')
    assert len(mutants) == 14 and all(m['rejected'] for m in mutants)

    host = OUT / 'pooled'
    run('pooled-emit', PARENT / 'code/emit_pooled.py', CPKG, VAR, PARENT / 'data/COLORED-OWNERS.json.gz', host)
    run('pooled-controller', PARENT / 'code/audit_pooled.py', VAR, host, OUT / 'HOSTING-AUDIT.json')
    run('serial-pool', PARENT / 'code/finite_serial_pool.py', OUT / 'FINITE-SERIAL-POOL.json')
    bit = OUT / 'parent496/bit/RESULT.json'
    admission = OUT / 'admission'
    run('physical-admission', PARENT / 'code/audit484/audit_pooled_candidate.py', '--parent', VAR,
        '--hosted', host, '--bit-result', bit, '--phases', VAR / 'work/complex-nine-native/DATA-PHASES.json',
        '--controller-audit', OUT / 'HOSTING-AUDIT.json', '--out', admission)
    run('independent-composition', PARENT / 'code/review_composition.py', admission, CHANGED,
        VAR / 'split-centres', VAR / 'hosted', host, bit, OUT / 'COMPOSITION-REVIEW.json')
    assembly = read(admission / 'EXACT-ASSEMBLY.json')
    owner = read(admission / 'OWNERS-AND-PROFILE.json')
    result = {k: assembly[k] for k in ['complex_lower', 'next_b_rejected', 'bit_lower', 'kappa',
              'kappa_decimal', 'bit_charged_three_level_coefficient_bits', 'external_row_allowance',
              'binding_component', 'strict_outer_constraints', 'outer_controls', 'bootstrap']}
    result.update(status='PASS_FRESH_RETIMED_GAUGE_POOLED_WHOLE_OWNER',
                  global_profile=owner['paid_profile'], live=owner['live'], physical=owner['physical'],
                  canonical_word_sha256=sha(VAR / 'split-centres/CANONICAL-WORD.json.gz'),
                  local_program_sha256=sha(VAR / 'split-centres/LOCAL-PROGRAMS.json.gz'),
                  pooled_template_sha256=read(host / 'HOSTED.json')['template_sha256'],
                  global_prefix_bits=read(admission / 'GLOBAL-PREFIX.json')['global_prefix_bits'],
                  source_manifest_sha256=sha(ROOT / 'MANIFEST.json'))
    for key, value in read(ROOT / 'EXPECTED.json').items():
        assert result[key] == value, (key, result.get(key), value)
    integrity()
    (OUT / 'RESULT.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    artifacts = ['parent496/RECEIPT.json', 'transfer/TRANSFER.json', 'HOSTING-AUDIT.json',
                 'COMPOSITION-REVIEW.json', 'admission/ADMISSION.json', 'admission/GLOBAL-PREFIX.json',
                 'lemmaG/LABELS-gauge80-kernel42.json',
                 'lemmaG/INSTANCES-gauge80-kernel42.json', 'lemmaG/E2E-gauge80-kernel42.json',
                 'lemmaG/PREOP-GUARDS-lg_instances.json', 'lemmaG/PREOP-GUARDS-lg_e2e.json',
                 'lemmaG/MUTANTS.json', 'RESULT.json']
    receipt = dict(status=result['status'], artifacts={f: sha(OUT / f) for f in artifacts},
                   python=sys.version.split()[0], steps=steps)
    (OUT / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(result['status'], 'kappa', result['kappa_decimal'], flush=True)
except BaseException as error:
    (OUT / 'FAILURE.json').write_text(json.dumps(dict(error=repr(error), steps=steps), indent=2) + '\n')
    raise
