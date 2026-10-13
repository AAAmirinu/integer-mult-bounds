"""Replay the owner delta using every PR656 verifier and constructor unchanged.

Standard library only; Python 3.11+ with assertions enabled. The optional search
is never imported. Prepared by Jeremy Diviney with OpenAI Codex assistance.
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def baseline_snapshot(parent, local, global_work, out):
    """Give the independent auditor fresh baseline evidence, not historical #645 files."""
    paths = {
        'data/PLAN.json': parent / 'data/PLAN.json',
        'data/OWNERS.json.gz': parent / 'data/OWNERS.json.gz',
        'evidence/local/CANONICAL-WORD.json.gz': local / 'CANONICAL-WORD.json.gz',
        'evidence/global/GLOBAL-TEMPLATE.json.gz': global_work / 'global/hosted/GLOBAL-TEMPLATE.json.gz',
        'evidence/global/HOSTED.json': global_work / 'global/hosted/HOSTED.json',
        'evidence/audit/OWNERS-AND-PROFILE.json': global_work / 'global/audit/OWNERS-AND-PROFILE.json',
    }
    for relative, source in paths.items():
        target = out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return {relative: sha(source) for relative, source in paths.items()}


def main():
    if not __debug__:
        raise RuntimeError('Assertions are required; do not use python -O.')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--main', type=Path, required=True)
    ap.add_argument('--parent', type=Path, required=True, help='Pinned PR656 research/gauge44-layered-b')
    ap.add_argument('--pr635', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--local', type=Path, help='Optional rebuilt layered local directory, including phases')
    a = ap.parse_args()
    main_root, parent, pr635, out = [p.resolve() for p in (a.main, a.parent, a.pr635, a.out)]
    assert not out.exists() and not any(out.is_relative_to(p) for p in (main_root, parent, pr635, HERE))
    actual = {p.relative_to(HERE).as_posix(): sha(p) for p in HERE.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p != HERE / 'MANIFEST.json'}
    assert actual == read(HERE / 'MANIFEST.json'), 'Package inventory or hashes changed'
    sources = read(HERE / 'SOURCES.json')
    assert sha(parent / 'MANIFEST.json') == sources['parent_manifest_sha256'], 'Unexpected PR656 package'
    assert sha(parent / 'data/OWNERS.json.gz') == sha(HERE / 'data/PR656-OWNERS.json.gz')
    out.mkdir(parents=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1', PYTHONINTMAXSTRDIGITS='0')
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
        dump(out / 'STEPS.json', steps)
        if result.returncode:
            raise RuntimeError(name + '\n' + log.read_text()[-6000:])
        print('PASS', name, flush=True)

    run('parent-manifest', parent / 'verify_manifest.py')
    if a.local:
        local = a.local.resolve()
    else:
        run('word', parent / 'construction/reproduce.py', '--main', main_root,
            '--pr635', pr635, '--out', out / 'word', '--until', 'word')
        run('layers-and-native', parent / 'construction/layers/reproduce_layers.py',
            '--main', main_root, '--pr635', pr635, '--word-dir', out / 'word', '--out', out / 'layered')
        local = out / 'layered/local'
        run('independent-scalar', parent / 'independent/audit_local.py', '--main', main_root,
            '--word', out / 'layered/layers/FULL-WORD.json.gz', '--output', out / 'INDEPENDENT-SCALAR.json')
    run('baseline-strict', parent / 'verify_global.py', '--main', main_root,
        '--local', local, '--work', out / 'baseline')
    assert read(out / 'baseline/REPLAY.json')['kappa_decimal'] == '0.001654108529511355'
    snapshot = baseline_snapshot(parent, local, out / 'baseline', out / 'baseline-snapshot')
    run('owners', HERE / 'audit_owners.py', '--package', parent,
        '--baseline-owners', HERE / 'data/PR656-OWNERS.json.gz',
        '--nomination', HERE / 'data', '--output', out / 'OWNERS-AUDIT.json')
    run('independent-owners', HERE / 'independent_owners.py', '--main', main_root,
        '--parent', out / 'baseline-snapshot', '--owners', HERE / 'data/OWNERS.json.gz',
        '--out', out / 'INDEPENDENT-OWNERS.json', '--mutation-controls')
    staged = out / 'staged-parent'
    run('prepare', HERE / 'prepare.py', '--parent', parent, '--candidate', HERE / 'data', '--out', staged)
    shutil.copyfile(HERE / 'data/SPEC.json', staged / 'data/SPEC.json')
    unchanged = {p.relative_to(parent).as_posix(): sha(p) for p in parent.rglob('*.py')
                 if '__pycache__' not in p.parts}
    assert all(sha(staged / rel) == digest for rel, digest in unchanged.items())
    changed = {p.relative_to(parent).as_posix() for p in parent.rglob('*')
               if p.is_file() and '__pycache__' not in p.parts and sha(p) != sha(staged / p.relative_to(parent))}
    assert changed == {'data/PLAN.json', 'data/OWNERS.json.gz', 'data/SPEC.json'}
    run('global-strict', staged / 'verify_global.py', '--main', main_root,
        '--local', local, '--work', out / 'global')
    run('independent-price', staged / 'independent/price_profile.py', '--main', main_root,
        '--profile', HERE / 'data/PROFILE.json', '--output', out / 'PRICE.json')
    run('packing-ceiling', HERE / 'packing_ceiling.py', '--parent', staged, '--main', main_root,
        '--out', out / 'ceiling')
    admitted = read(out / 'global/REPLAY.json')
    kappa = read(HERE / 'data/SPEC.json')['expected']['kappa_decimal']
    assert admitted['status'] == 'PASS_GAUGE44_STRICT_GLOBAL_REPLAY' and admitted['kappa_decimal'] == kappa
    assert read(out / 'PRICE.json')['prices']['native']['outer_with_bit']['kappa_decimal'] == kappa
    receipt = dict(status='PASS_LAYERED_JOINT_OWNER_STRICT_ADMISSION', kappa_decimal=kappa,
                   parent_head=sources['parent_head'], parent_manifest_sha256=sources['parent_manifest_sha256'],
                   owner_sha256=sha(HERE / 'data/OWNERS.json.gz'),
                   unchanged_verifier_python_files=unchanged, baseline_snapshot=snapshot,
                   rebuilt_local=a.local is None, steps=steps,
                   scope='Conditional finite owner witness under the unchanged PR655/656 local construction, '
                         'controller and admission interfaces. PR589 bit circuit cited unchanged and its '
                         'profile repriced; no unconditional theorem, full Lean proof or packing optimality claim.')
    dump(out / 'REPLAY.json', receipt)
    print(receipt['status'], kappa)


if __name__ == '__main__':
    main()
