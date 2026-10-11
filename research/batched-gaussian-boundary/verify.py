#!/usr/bin/env python3
"""Source-bound exact controls for batched Gaussian boundary inverses."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

assert __debug__, 'verification requires assertions'
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT/'code'))
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def integrity():
    actual = {p.relative_to(ROOT).as_posix(): sha(p) for p in ROOT.rglob('*')
              if p.is_file() and p.name != 'MANIFEST.json' and '__pycache__' not in p.parts}
    assert actual == read(ROOT/'MANIFEST.json')
    for name, digest in read(ROOT/'SOURCE.json')['files'].items():
        assert sha(REPO/name) == digest, name


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=Path)
    out = ap.parse_args().output.resolve()
    assert not out.exists() and not out.is_relative_to(ROOT)
    integrity()
    from check import run
    checked = run()
    assert checked == read(ROOT/'EXPECTED.json')
    summary = dict(cyclic_systems=len(checked['cyclic_cases']),
                   gaussian_systems=len(checked['gaussian_cases']),
                   inverse_entries=sum(x['entries'] for x in checked['cyclic_cases']+checked['gaussian_cases']),
                   complete_schur_entries=sum(x['compared_entries'] for x in checked['complete_schur']),
                   strassen_entries=sum(x['entries'] for x in checked['strassen']),
                   layouts=checked['layouts'], mutants=len(checked['rejected_mutants']),
                   scalar_exponent_upper=checked['scalar_exponent_upper'],
                   boundary_exponent=checked['boundary_exponent'], kappa_claim=None)
    integrity()
    out.mkdir(parents=True)
    for name, value in [('CHECKS', checked), ('RESULT', summary)]:
        (out/(name+'.json')).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    receipt = dict(status='PASS_BATCHED_GAUSSIAN_BOUNDARY_CONTROLS', python=sys.version.split()[0],
                   manifest_sha256=sha(ROOT/'MANIFEST.json'), source_sha256=sha(ROOT/'SOURCE.json'),
                   checks_sha256=sha(out/'CHECKS.json'), result_sha256=sha(out/'RESULT.json'))
    (out/'RECEIPT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
