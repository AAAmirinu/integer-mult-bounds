"""Build and check the finite complex supplier in a separate directory."""
from pathlib import Path
import gzip
import hashlib
import json
import os
import subprocess
import sys

from phase_audit import schedule_check

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
DATA = PACKAGE / 'data/complex'


def replay(out):
    out = Path(out).resolve()
    if out == PACKAGE or PACKAGE in out.parents:
        raise ValueError('The output directory must be outside the source package.')
    out.mkdir(parents=True, exist_ok=True)
    local = out / 'split-centres'
    local.mkdir(exist_ok=True)
    (local / 'FULL-WORD.json.gz').write_bytes((DATA / 'FULL-WORD.json.gz').read_bytes())
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0')
    env.pop('PYTHONOPTIMIZE', None)
    checks = []

    def run(name, args):
        print('RUN complex', name, flush=True)
        log = out / (name + '.log')
        with log.open('w') as stream:
            subprocess.run([sys.executable, '-B', str(HERE / (name + '.py')),
                            *map(str, args)], cwd=out, env=env,
                           stdout=stream, stderr=subprocess.STDOUT, check=True)
        checks.append(name)
        print('PASS complex', name, flush=True)

    for name, args in [('scalar', []), ('programs', []), ('phases', []),
                       ('adapters', [local]), ('local_audit', [local])]:
        run(name, args)
    geometry = out / 'geometry'
    geometry.mkdir(exist_ok=True)
    run('data_phases', [local / 'CANONICAL-WORD.json.gz', geometry / 'DATA-PHASES.json'])
    seed = json.loads((DATA / 'schedule.json').read_text())
    seed['exact_data_phase_recipe_sha256'] = hashlib.sha256(
        (geometry / 'DATA-PHASES.json').read_bytes()).hexdigest()
    assert schedule_check(seed) == (11, 12, 13)
    raw = json.dumps(seed, sort_keys=True, separators=(',', ':')).encode()
    (geometry / 'GLOBAL-TEMPLATE.json.gz').write_bytes(gzip.compress(raw, mtime=0))
    target = out / 'complex'
    run('emit', [geometry, local, target])
    run('audit', [geometry, local, target])
    receipt = dict(status='PASS_FRESH_COMPLEX_CONSTRUCTION', checks=checks,
                   finite_schedule=[11, 12, 13],
                   scope='Exact finite word, scalar columns, phases, adapters, schedule, owners and emitted cost profile. All-size compilation and cover contracts remain assumptions.')
    (out / 'REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt


if __name__ == '__main__':
    replay(sys.argv[1])
