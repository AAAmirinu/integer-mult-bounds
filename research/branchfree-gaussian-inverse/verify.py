#!/usr/bin/env python3
"""Source-bound exact controls for a branch-free Gaussian interior inverse."""
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
    summary = dict(exact_cases=len(checked['identities']),
                   exact_ldl_entries=sum(x['ldl_entries'] for x in checked['identities']),
                   exact_inverse_entries=sum(x['inverse_entries'] for x in checked['identities']),
                   rounded_cases=len(checked['rounded']),
                   rounded_entries=sum(x['entries'] for x in checked['rounded']),
                   full_schur_cases=len(checked['complete_schur']),
                   full_schur_entries=sum(x['entries'] for x in checked['complete_schur']),
                   tensor_entries=sum(x['entries'] for x in checked['tensor_and_weighted']['tensor_identities']),
                   weighted_factor_entries=sum(x['entries'] for x in checked['tensor_and_weighted']['weighted_factors']),
                   joint_kernel_guard_entries=checked['tensor_precision_guard']['dense_toy']['operator_entries'],
                   joint_kernel_symbolic_rows=len(checked['tensor_precision_guard']['symbolic_rows']),
                   mutants=len(checked['rejected_mutants']), scope=checked['scope'], kappa_claim=None)
    integrity()
    out.mkdir(parents=True)
    for name, value in [('CHECKS', checked), ('RESULT', summary)]:
        (out/(name+'.json')).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    receipt = dict(status='PASS_BRANCHFREE_GAUSSIAN_INVERSE', python=sys.version.split()[0],
                   manifest_sha256=sha(ROOT/'MANIFEST.json'), source_sha256=sha(ROOT/'SOURCE.json'),
                   checks_sha256=sha(out/'CHECKS.json'), result_sha256=sha(out/'RESULT.json'))
    (out/'RECEIPT.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
