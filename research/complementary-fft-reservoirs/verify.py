#!/usr/bin/env python3
"""Replay finite controls for the conditional complementary-reservoir FFT."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

assert __debug__, 'verification requires assertions'
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT/'code'))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())


def integrity():
    actual = {p.relative_to(ROOT).as_posix(): sha(p) for p in ROOT.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts and p.name != 'MANIFEST.json'}
    assert actual == read(ROOT/'MANIFEST.json')
    for name, digest in read(ROOT/'SOURCE.json')['files'].items():
        assert sha(REPO/name) == digest, name


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=Path)
    out = ap.parse_args().output.resolve()
    assert not out.exists() and not out.is_relative_to(ROOT)
    integrity()
    from operators import run as operators
    from capacity import run as capacity
    out.mkdir(parents=True)
    op, cap = operators(), capacity()
    result = dict(status='PASS_CONDITIONAL_COMPLEMENTARY_FFT_CONTROLS',
                  shapes=op['shape_count'], basis_columns=op['basis_columns'],
                  polynomial_entries=op['polynomial_entries'],
                  common_field_layouts=cap['literal_layout_count'],
                  top_field_layouts=cap['top_layout_count'],
                  operator_mutations=op['mutations_rejected'],
                  capacity_mutations=cap['mutations_rejected'],
                  parameter_witnesses=len(cap['parameter_witnesses']),
                  retained_strict_expressions=44,
                  maximum_global_routes=5,
                  precision_controls=cap['precision_inequalities_checked'],
                  unchanged_reference_kappa=cap['unchanged_kappa'],
                  new_kappa_claim=False,
                  scope='Finite operator, layout and arithmetic evidence for the written conditional transfer; not an all-size machine execution or a new multiplication exponent.')
    assert result == read(ROOT/'EXPECTED.json')
    integrity()
    for name, value in [('OPERATORS.json', op), ('CAPACITY.json', cap), ('RESULT.json', result)]:
        (out/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    receipt = dict(status=result['status'], python=sys.version.split()[0],
                   manifest_sha256=sha(ROOT/'MANIFEST.json'), source_sha256=sha(ROOT/'SOURCE.json'),
                   result_sha256=sha(out/'RESULT.json'), operators_sha256=sha(out/'OPERATORS.json'),
                   capacity_sha256=sha(out/'CAPACITY.json'))
    (out/'RECEIPT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
