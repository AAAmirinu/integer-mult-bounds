"""Run PR364's full frozen verifier in reference or exact-integer mode."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time

from common import ROOT, SOURCE, sha, verify_outputs, verify_source


def main():
    if not __debug__:
        raise RuntimeError('verification requires assertions enabled')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mode', choices=('reference', 'fast'), default='fast')
    parser.add_argument('--cxx', default=os.environ.get('CXX', 'c++'))
    parser.add_argument('--boost-include', default=os.environ.get('BOOST_INCLUDE', '/usr/include'))
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    start = time.perf_counter()
    source = verify_source(args.source)
    output = args.output.resolve()
    if output.exists() or output.is_relative_to(ROOT) or output.is_relative_to(source):
        parser.error('output must be a fresh directory outside both packages')
    # The original shell verifier expands these paths without quoting.
    if any(c.isspace() for p in (str(source), str(output)) for c in p):
        parser.error('the original shell verifier requires source/output paths without whitespace')
    output.mkdir(parents=True)
    env = dict(os.environ, PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1',
               OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               CXX=args.cxx, BOOST_INCLUDE=args.boost_include,
               FRAME_ALGEBRA_SOURCE=str(source), FRAME_ALGEBRA_MODE=args.mode,
               FRAME_ALGEBRA_COMMAND_LOG=str(output/'commands.jsonl'))
    env.pop('PYTHONOPTIMIZE', None)
    command = ['bash', str(source/'verify.sh'), str(output)]
    with tempfile.TemporaryDirectory(prefix='frame-algebra-') as temporary:
        launcher = Path(temporary)/'python'
        launcher.write_text('#!/bin/sh\nexec '+shlex.quote(sys.executable)+' -B '+
                            shlex.quote(str(ROOT/'python_dispatch.py'))+' "$@"\n')
        launcher.chmod(0o700)
        env['PYTHON'] = str(launcher)
        begin = time.perf_counter()
        with (output/'console.log').open('w') as log:
            process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                log.write(line)
                log.flush()
                if args.verbose or line.startswith(('==', 'PASS conditional')):
                    print(line, end='', flush=True)
            status = process.wait()
        verifier_seconds = time.perf_counter()-begin
    verify_source(source)
    report = dict(mode=args.mode, returncode=status, source_commit=SOURCE['commit'],
                  source_files_unchanged=True, source_files_checked=len(SOURCE['files']),
                  implementation_sha256=sha(ROOT/'exact_rows.py'),
                  source_metadata_sha256=sha(ROOT/'SOURCE.json'),
                  verifier_seconds=verifier_seconds, python=sys.version,
                  command=command, cxx=args.cxx, boost_include=args.boost_include,
                  scope='Full shipped PR364 verifier; native admission obligations remain open.')
    if status == 0:
        report['outputs'], report['pricing'] = verify_outputs(output)
        rows = [json.loads(line) for line in (output/'commands.jsonl').read_text().splitlines()]
        calls = [row for row in rows if str(source/'code/stages.py') in row['original_command']]
        if [row['original_command'][3] for row in calls] != ['kernel', 'retime', 'reorder', 'reorder']:
            raise ValueError('the four mandatory transcript stages were not all run')
        if any(row['returncode'] != 0 for row in rows):
            raise ValueError('a verifier command failed')
        if args.mode == 'fast' and any(str(ROOT/'stage_adapter.py') not in row['executed_command'] for row in calls):
            raise ValueError('fast adapter did not execute every transcript stage')
        report['transcript_seconds'] = sum(row['seconds'] for row in calls)
        report['transcript_stages'] = calls
        report['status'] = 'PASS_FULL_SHIPPED_PR364_REPLAY'
    else:
        report['status'] = 'FAIL'
    report['seconds'] = time.perf_counter()-start
    (output/'REPLAY.json').write_text(json.dumps(report, indent=2)+'\n')
    print(args.mode, report['status'], f"{report['seconds']:.2f}s", flush=True)
    return status


if __name__ == '__main__':
    sys.exit(main())
