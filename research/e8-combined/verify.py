"""Rebuild both finite suppliers and check their conditional composition."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from check_outer import check as check_outer
from costs import compose

HERE = Path(__file__).resolve().parent


def public_certificate(result):
    return {key: value for key, value in result.items()
            if key not in ('strict_outer_constraints', 'bootstrap')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--write-certificate', action='store_true')
    args = parser.parse_args()
    if not __debug__:
        parser.error('Run Python without -O or PYTHONOPTIMIZE.')
    out = args.output.resolve()
    if out == HERE or HERE in out.parents:
        parser.error('--output must be outside the source package.')
    if out.exists() and any(out.iterdir()):
        parser.error('--output must name an empty or new directory.')
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0')
    env.pop('PYTHONOPTIMIZE', None)
    for name in ('bit', 'complex'):
        subprocess.run([sys.executable, '-B', str(HERE/'vendor'/name/'replay.py'),
                        str(out/name)], cwd=out, env=env, check=True)
    result = compose(out/'bit', out/'complex/complex')
    result['independent_outer_check'] = check_outer(result)
    result['input_sha256'] = {
        str(path.relative_to(HERE)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((HERE/'data').rglob('*')) if path.is_file()
    }
    (out/'RESULT.json').write_text(json.dumps(result, indent=2)+'\n')
    certificate = public_certificate(result)
    if args.write_certificate:
        (HERE/'certificate.json').write_text(json.dumps(certificate, indent=2)+'\n')
    else:
        expected = json.loads((HERE/'certificate.json').read_text())
        assert certificate == expected, 'The fresh certificate differs.'
    print(json.dumps({key: result[key] for key in
                      ('status', 'kappa_decimal', 'gain_percent', 'binding_component')},
                     indent=2))


if __name__ == '__main__':
    main()
