"""Rebuild both suppliers, replay the new packing, and certify the assembly.

Usage: python -B research/e8-gauge-moment-hosting/verify.py NEW_ABSOLUTE_OUT
Python 3.13 or 3.14 is required by the unchanged PR484 gzip-byte receipts.
Apache-2.0. Chafreaky with OpenAI Codex assistance.
"""
import hashlib
import gzip
import json
import os
import subprocess
import sys
import time
from pathlib import Path

assert __debug__
assert (3, 13) <= sys.version_info[:2] <= (3, 14), 'Use Python 3.13 or 3.14 for the unchanged PR484 gzip-byte receipts'
ROOT = Path(__file__).resolve().parent
R = ROOT.parent
out = Path(sys.argv[1]).resolve()
assert len(sys.argv) == 2 and not out.exists() and not out.is_relative_to(R)
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def inventory(path):
    return {p.relative_to(path).as_posix(): sha(p) for p in sorted(path.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts}


def integrity():
    actual = inventory(ROOT)
    actual.pop('MANIFEST.json')
    assert actual == read(ROOT / 'MANIFEST.json')
    for name, expected in read(ROOT / 'SOURCE.json')['packages'].items():
        assert inventory(R / name) == expected['files'], name


integrity()
out.mkdir(parents=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0', PYTHON=sys.executable)
env.pop('PYTHONOPTIMIZE', None)
steps = []


def run(name, command, cwd=None):
    start = time.monotonic()
    log = out / (name + '.log')
    print('RUN', name, flush=True)
    with log.open('w') as f:
        result = subprocess.run(list(map(str, command)), cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError((name, result.returncode, log.read_text()[-5000:]))
    steps.append(dict(name=name, seconds=round(time.monotonic() - start, 2), log_sha256=sha(log)))
    print('PASS', name, flush=True)


def py(name, script, *args, cwd=None):
    run(name, [sys.executable, '-B', script, *args], cwd)


try:
    parent = out / 'parent484'
    bit = out / 'parent493'
    package = R / 'e8-complex-gauge-kernel'
    code = package / 'code'
    py('full-parent484-all-variants', package / 'verify.py', parent, '--all')
    parent_receipt = read(parent / 'RECEIPT.json')
    assert parent_receipt['status'] == 'PASS_FULL_COMPLEX_GAUGE_KERNEL_COMPOSITION'
    run('full-parent493-bit', ['bash', R / 'e8-bit-carrier-skeleton/verify.sh', bit])
    bit_result = read(bit / 'RESULT.json')
    variant = parent / 'gauge80-kernel42'
    candidate = out / 'candidate'
    candidate.mkdir()
    py('new-hosting', code / 'hosted_gk.py', variant / 'split-centres', candidate / 'hosted',
       '--one-helper-per-family', '--selection', ROOT / 'data/SELECTION.json', '--key', 'nine-gauge-moment', cwd=variant)
    py('independent-hosting-audit', code / 'audit_hosted_gk.py', variant / 'split-centres', candidate / 'hosted',
       candidate / 'AUDIT.json', '--one-helper-per-family', cwd=variant)
    py('independent-selection-counts', ROOT / 'code/check_selection.py', variant, candidate, candidate / 'COUNTS.json')
    bits = [dict(label='PR493 R489 source-carrier word, freshly replayed', c=bit_result['bit_lower'],
                 charged_two_level_coefficient_bits=bit_result['bit']['charged_three_level_coefficient_bits'],
                 row_coefficient=bit_result['bit']['row_coefficient'], source='parent493/RESULT.json from this run')]
    (out / 'BITS.json').write_text(json.dumps(bits, indent=2) + '\n')
    py('two-moments-finite-invoices-outer', code / 'assemble_gk.py', parent / 'p442/parent/changed',
       variant / 'split-centres', candidate / 'hosted', candidate / 'AUDIT.json', out / 'BITS.json', candidate / 'RESULT.json')
    result = read(candidate / 'RESULT.json')
    counts = read(candidate / 'COUNTS.json')
    audit = read(candidate / 'AUDIT.json')
    supplier, = result['suppliers']
    assert len(supplier['strict_outer_constraints']) == 47
    # PR493 binds a geometry file containing a wall-clock timer into its
    # template. Keep that raw binding in the receipt; normalize ONLY that
    # measured timer for a deterministic operator-template fingerprint.
    blob = lambda x: json.dumps(x, sort_keys=True, separators=(',', ':')).encode()
    bit_template = json.loads(gzip.decompress((bit / 'bit/GLOBAL-TEMPLATE.json.gz').read_bytes()))
    assert hashlib.sha256(blob(bit_template)).hexdigest() == bit_result['bit_template_sha256']
    assert bit_template['geometry_sha256'] == sha(bit / 'bit/GEOMETRY.json')
    geometry = read(bit / 'bit/GEOMETRY.json')
    measured_seconds = geometry.pop('seconds')
    assert isinstance(measured_seconds, (int, float)) and measured_seconds >= 0
    bit_template['geometry_sha256'] = hashlib.sha256(blob(geometry)).hexdigest()
    bit_operator_hash = hashlib.sha256(blob(bit_template)).hexdigest()
    summary = dict(status='PASS_FRESH_GAUGE_MOMENT_HOSTING_COMPOSITION', kappa=supplier['kappa'],
                   kappa_decimal=supplier['kappa_decimal'], complex_lower=result['complex_lower'],
                   bit_lower=supplier['bit_lower'], binding_component=supplier['binding_component'],
                   complex=result['complex'], complex_template_sha256=result['complex_template_sha256'],
                   bit_operator_template_sha256=bit_operator_hash, counts=counts,
                   baseline_complex_lower=parent_receipt['complex_lower'],
                   baseline_complex_cap_kappa_decimal=parent_receipt['complex_cap_kappa_decimal'],
                   strict_outer_constraints=supplier['strict_outer_constraints'], outer_controls=supplier['outer_controls'],
                   hosting_mutations_rejected=audit['mutations_rejected'],
                   hosting_controls_not_applicable=audit['controls_not_applicable'],
                   source_manifest_sha256=sha(ROOT / 'MANIFEST.json'), source_inventory_sha256=sha(ROOT / 'SOURCE.json'),
                   scope='Conditional inherited all-size compiler, mutable-basis and whole-owner hosting interfaces; finite exact replay, not an unconditional theorem.')
    for key, expected in read(ROOT / 'EXPECTED.json').items():
        assert summary[key] == expected, (key, summary[key], expected)
    integrity()
    (out / 'RESULT.json').write_text(json.dumps(summary, indent=2) + '\n')
    receipt = dict(status=summary['status'], kappa=summary['kappa'], python=sys.version.split()[0],
                   result_sha256=sha(out / 'RESULT.json'), source_manifest_sha256=summary['source_manifest_sha256'],
                   parent484_receipt_sha256=sha(parent / 'RECEIPT.json'), parent493_result_sha256=sha(bit / 'RESULT.json'),
                   bit_template_sha256=bit_result['bit_template_sha256'], bit_geometry_sha256=sha(bit / 'bit/GEOMETRY.json'),
                   bit_fingerprint_omits_only_geometry_field='seconds', steps=steps)
    (out / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2), flush=True)
except BaseException as error:
    (out / 'FAILURE.json').write_text(json.dumps(dict(error=repr(error), completed=steps), indent=2) + '\n')
    raise
