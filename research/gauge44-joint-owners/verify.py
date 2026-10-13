"""Admit the frozen joint-call owners with PR645's unchanged physical verifier.

Python 3.11+; standard library only. The optimizer is not part of admission.
By default this also rebuilds Gauge44's scalar word, native ledgers and phases.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PARENT_MANIFEST = 'ad36e2c9802a8da4a4c70180eeb710d9f314b1e8cc521b5749d3fbebc299e932'
KAPPA = json.loads((HERE / 'data/SPEC.json').read_text())['expected']['kappa_decimal']


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if not __debug__:
        raise RuntimeError('Assertions are required; do not use python -O.')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--main', type=Path, required=True)
    ap.add_argument('--parent', type=Path, required=True,
                    help='research/gauge44-global from pinned PR645')
    ap.add_argument('--pr635', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True,
                    help='New output directory outside the input checkouts')
    ap.add_argument('--local', type=Path,
                    help='Optional already rebuilt native Gauge44 directory, including phases')
    a = ap.parse_args()
    main_root, parent, pr635, out = [p.resolve() for p in
                                    (a.main, a.parent, a.pr635, a.out)]
    assert not out.exists()
    assert not any(out.is_relative_to(p) for p in (main_root, parent, pr635, HERE))
    own_manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    actual = {p.relative_to(HERE).as_posix(): sha(p) for p in HERE.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p != HERE / 'MANIFEST.json'}
    assert actual == own_manifest, 'Submitted package inventory or hashes changed'
    assert sha(parent / 'MANIFEST.json') == PARENT_MANIFEST, 'Unexpected PR645 package'
    out.mkdir(parents=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
               PYTHONINTMAXSTRDIGITS='0')
    for key in ('PYTHONOPTIMIZE', 'WITNESS_DISCOVER', 'WITNESS_RECORD'):
        env.pop(key, None)
    steps = []

    def run(name, script, *args):
        started = time.monotonic()
        log = out / (name + '.log')
        with log.open('w') as stream:
            result = subprocess.run([sys.executable, '-B', str(script), *map(str, args)],
                                    env=env, stdout=stream, stderr=subprocess.STDOUT)
        steps.append(dict(name=name, exit_code=result.returncode,
                          seconds=round(time.monotonic()-started, 3), log_sha256=sha(log)))
        (out / 'STEPS.json').write_text(json.dumps(steps, indent=2) + '\n')
        if result.returncode:
            raise RuntimeError(name + '\n' + log.read_text()[-6000:])
        print('PASS', name, flush=True)

    run('parent-manifest', parent / 'verify_manifest.py')
    if a.local:
        local = a.local.resolve()
    else:
        run('local-rebuild', parent / 'construction/reproduce.py', '--main', main_root,
            '--pr635', pr635, '--out', out / 'local-rebuild', '--until', 'phases')
        local = out / 'local-rebuild/local'
        run('independent-scalar', parent / 'independent/audit_local.py', '--main', main_root,
            '--word', out / 'local-rebuild/cold44/FULL-WORD.json.gz',
            '--output', out / 'INDEPENDENT-SCALAR.json')
    run('owners', HERE / 'audit_owners.py', '--package', parent,
        '--baseline-owners', HERE / 'data/PR649-OWNERS.json.gz',
        '--nomination', HERE / 'data', '--output', out / 'OWNERS-AUDIT.json')
    run('independent-owners', HERE / 'independent_owners.py', '--main', main_root,
        '--parent', parent, '--owners', HERE / 'data/OWNERS.json.gz',
        '--out', out / 'INDEPENDENT-OWNERS.json', '--mutation-controls',
        '--compare', 'PR649='+str(HERE / 'data/PR649-OWNERS.json.gz'))
    staged = out / 'staged-parent'
    run('prepare', HERE / 'prepare.py', '--parent', parent,
        '--candidate', HERE / 'data', '--out', staged)
    shutil.copyfile(HERE / 'data/SPEC.json', staged / 'data/SPEC.json')
    shutil.copyfile(HERE / 'data/UPSTREAM-PINS.json', staged / 'data/UPSTREAM-PINS.json')
    shutil.copyfile(HERE / 'code/assemble.py', staged / 'code/assemble.py')
    # The physical controller, phase and invoice checkers remain byte-identical.
    # The one explicit adapter selects and pins the stronger cited PR589 bit
    # supplier while retaining exact moment checks and all outer constraints.
    unchanged = {p.relative_to(parent).as_posix(): sha(p)
                 for p in parent.rglob('*.py') if '__pycache__' not in p.parts
                 and p.relative_to(parent).as_posix() != 'code/assemble.py'}
    assert all(sha(staged / rel) == digest for rel, digest in unchanged.items())
    assert sha(staged / 'code/assemble.py') == sha(HERE / 'code/assemble.py')
    run('global-strict', staged / 'verify_global.py', '--main', main_root,
        '--local', local, '--work', out / 'global')
    run('independent-price', HERE / 'code/price_profile.py', '--main', main_root,
        '--profile', HERE / 'data/PROFILE.json', '--output', out / 'PRICE.json')
    admitted = json.loads((out / 'global/REPLAY.json').read_text())
    price = json.loads((out / 'PRICE.json').read_text())
    assert admitted['status'] == 'PASS_GAUGE44_STRICT_GLOBAL_REPLAY'
    assert admitted['kappa_decimal'] == KAPPA
    assert price['prices']['native']['outer_with_pr589']['kappa_decimal'] == KAPPA
    receipt = dict(status='PASS_JOINT_OWNER_STRICT_GLOBAL_ADMISSION',
                   kappa_decimal=KAPPA, parent_pr=645,
                   parent_commit='638a5171dd1aca89ff50d07dcbe288b567769804',
                   parent_manifest_sha256=PARENT_MANIFEST,
                   owners_sha256=sha(HERE / 'data/OWNERS.json.gz'),
                   unchanged_verifier_python_files=unchanged,
                   assembly_adapter_sha256=sha(HERE / 'code/assemble.py'),
                   rebuilt_local=a.local is None, steps=steps,
                   scope='Joint-call ownership improves PR649 under the unchanged physical interfaces of PR645. Complete controller, invoice, exact moments and outer assembly replayed. Local word and phases rebuilt unless --local is supplied. The stronger PR589 bit supplier is cited unchanged, with fresh exact profile repricing; no unconditional theorem or complete Lean proof.')
    (out / 'REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(receipt['status'], KAPPA)


if __name__ == '__main__':
    main()
