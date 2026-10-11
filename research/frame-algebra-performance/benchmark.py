"""Sequential full A/B replay; retain every source/output pin and command log."""
import argparse
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys

from common import ROOT, SOURCE, sha, verify_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--repetitions', type=int, default=1)
    parser.add_argument('--cxx', default=None)
    parser.add_argument('--boost-include', default=None)
    args = parser.parse_args()
    source = verify_source(args.source)
    output = args.output.resolve()
    if args.repetitions < 1:
        parser.error('repetitions must be positive')
    if output.exists() or output.is_relative_to(ROOT) or output.is_relative_to(source):
        parser.error('output must be fresh and outside both packages')
    output.mkdir(parents=True)
    results = dict(reference=[], fast=[])
    for i in range(args.repetitions):
        # Alternate order across repetitions to reduce systematic warm-cache bias.
        for mode in (('reference', 'fast') if i % 2 == 0 else ('fast', 'reference')):
            destination = output/(mode+'-'+str(i+1))
            command = [sys.executable, '-B', str(ROOT/'run.py'), str(source),
                       str(destination), '--mode', mode]
            for flag, value in (('--cxx', args.cxx), ('--boost-include', args.boost_include)):
                if value is not None:
                    command += [flag, value]
            subprocess.run(command, check=True)
            report = json.loads((destination/'REPLAY.json').read_text())
            if report['status'] != 'PASS_FULL_SHIPPED_PR364_REPLAY':
                raise ValueError('replay did not pass')
            results[mode].append(report)
        a, b = results['reference'][-1], results['fast'][-1]
        for key in ('outputs', 'pricing', 'implementation_sha256', 'source_metadata_sha256'):
            if a[key] != b[key]:
                raise ValueError('A/B mismatch: '+key)
    before, after = (statistics.median(r['seconds'] for r in results[m]) for m in ('reference', 'fast'))
    result = dict(status='PASS_EXACT_AB_REPLAY', source_commit=SOURCE['commit'],
                  source_metadata_sha256=sha(ROOT/'SOURCE.json'),
                  implementation_sha256=sha(ROOT/'exact_rows.py'),
                  platform=platform.platform(), repetitions=args.repetitions,
                  reference_median_seconds=before, fast_median_seconds=after,
                  speedup=before/after, time_saved_percent=100*(1-after/before), runs=results)
    (output/'BENCHMARK.json').write_text(json.dumps(result, indent=2)+'\n')
    print(f'PASS: {before:.2f}s -> {after:.2f}s; {before/after:.2f}x', flush=True)


if __name__ == '__main__':
    main()
