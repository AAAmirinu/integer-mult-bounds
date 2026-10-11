"""Rebuild the bit template and run the exact checks in a new output folder."""
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1]
ENV = os.environ.copy()
ENV.pop('PYTHONOPTIMIZE', None)
ENV['PYTHONDONTWRITEBYTECODE'] = '1'


def source_tree():
    return {str(p.relative_to(PACKAGE)): sha(p)
            for folder in (HERE, PACKAGE / 'data/bit')
            for p in sorted(folder.rglob('*')) if p.is_file()}


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(script, *arguments):
    print('bit: ' + script, flush=True)
    result = subprocess.run([sys.executable, '-B', str(HERE / script), *map(str, arguments)],
                            capture_output=True, text=True, env=ENV)
    if result.returncode:
        sys.stderr.write(result.stdout + result.stderr)
        raise subprocess.CalledProcessError(result.returncode, result.args)
    return result.stdout


def main():
    if sys.flags.optimize:
        raise RuntimeError('Run the verifier without Python optimization.')
    out = Path(sys.argv[1]).resolve()
    if out == PACKAGE or PACKAGE in out.parents:
        raise ValueError('The output folder must be outside the source package.')
    before = source_tree()
    out.mkdir(parents=True, exist_ok=True)
    for entry in read(HERE / 'SOURCES.json')['files']:
        assert sha(PACKAGE / entry['file']) == entry['sha256'], entry['file']
    shutil.copyfile(PACKAGE / 'data/bit/word.json.gz', out / 'word.json.gz')
    word = out / 'word.json'
    word.write_bytes(gzip.decompress((out / 'word.json.gz').read_bytes()))
    local = out / 'local'
    run('local.py', out / 'word.json.gz', local)
    run('geometry.py', '--word', out / 'word.json.gz', '--out', out)
    run('emit.py', '--word', out / 'word.json.gz', '--local-check', local,
        '--out', out, '--isometries', local / 'isometries.json',
        '--selection', PACKAGE / 'data/bit/selection.json')
    run('check_word.py', word, '--out', out / 'word-check.json')
    run('check_records.py', word, local / 'records', out / 'records-check.json')
    run('check_global106.py', out, out / 'records-check.json', out / 'word-check.json',
        out / 'global-check.json', word)
    routes = json.loads(run('check_routes.py', '--base', out, '--word', word))
    (out / 'routes-check.json').write_text(json.dumps(routes, indent=2) + '\n')
    run('check_controls.py', word, local / 'records', out / 'controls-check.json')
    audit = read(out / 'global-check.json')
    assert audit['status'] == 'PASS_INDEPENDENT_LOCAL_AND_GLOBAL_AUDIT_ROUTES_SEPARATE'
    assert routes['status'] == 'PASS_INDEPENDENT_EXACT_SIGNED_OWNER_ROUTES'
    controls = read(out / 'controls-check.json')
    assert controls['status'] == 'PASS_INDEPENDENT_BOUNDARY_CONTROLS'
    audit['status'] = 'PASS_INDEPENDENT_ELEVEN_STAGE_HOSTING_AUDIT'
    audit['routes'] = routes
    audit['local_boundary_controls'] = controls['rejected']
    audit['receipt_hashes'] = {name: sha(out / name) for name in
                             ('word-check.json', 'records-check.json', 'global-check.json',
                              'routes-check.json', 'controls-check.json')}
    audit['audit_source_hashes'] = {name: sha(HERE / name) for name in
                                  ('check_word.py', 'check_records.py', 'check_global106.py',
                                   'check_routes.py', 'check_controls.py', 'replay.py')}
    audit['scope'] = ('Exact local word and records; both orientations; unbanked global columns; '
                      'signed schedule; owner routes; geometry; child profile; and physical prefix. '
                      'Complete-cover hosting, compiler, and all-size analytic interfaces remain '
                      'conditional assumptions. No C++ replay is claimed.')
    (out / 'AUDIT.json').write_text(json.dumps(audit, indent=2) + '\n')
    assert source_tree() == before, 'The source files changed during replay.'
    (out / 'SOURCE-READ-ONLY.json').write_text(json.dumps(before, indent=2) + '\n')
    print(json.dumps({'status': audit['status'], 'output': str(out),
                      'emitted_events': audit['emitted_events'],
                      'hosted_residuals': audit['hosted_residuals'],
                      'physical_prefix_bits': audit['physical_prefix_bits']}, indent=2))


if __name__ == '__main__':
    main()
