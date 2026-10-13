#!/usr/bin/env python3
"""Reproduce the fixed-order R420 B-frame bound, both engines and controls.

Copyright 2026 yuj1r0. Substantial OpenAI Codex assistance; Apache-2.0.
"""
import argparse
import copy
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import check

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORD = 'research/e8-bit-r420/data/bitE8mut-r420.json.gz'
PREDECESSOR = 'research/e8-bit-r420/code/xcheck.py'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_pins(inputs, root=ROOT):
    for path, expected in inputs.items():
        require(hashlib.sha256((root / path).read_bytes()).hexdigest() == expected,
                'source pin mismatch: ' + path)


def check_certificate(expected, actual):
    require(expected == actual, 'certificate differs from fresh exact calculation')


def must_reject(callback, reason):
    try:
        callback()
    except ValueError:
        return
    raise ValueError('negative control accepted: ' + reason)


def controls(word, report, cert, inputs):
    names = []
    unit = [[int(i == j) for j in range(8)] for i in range(8)]
    u = check.basis([unit[0], unit[1]])
    v = check.basis([[a+b for a,b in zip(unit[0], unit[2])],
                     [a-b for a,b in zip(unit[1], unit[2])]])
    intersection = check.perp(check.join((check.perp(u), check.perp(v))))
    expected = check.basis([[a+b for a,b in zip(unit[0], unit[1])]])
    require(intersection == expected, 'exact intersection lost a non-generator direction')
    names.append('rational_intersection_without_shared_generators')
    require(not check.included(check.basis([unit[0]]), check.basis([unit[1]])),
            'same rank mistaken for containment')
    names.append('same_rank_unequal_subspaces')
    require(check.majorizes((3,1), (2,2)) and not check.majorizes((2,2), (3,1)),
            'majorization direction reversed')
    require(not check.majorizes((3,), (2,)), 'unequal mass allowed')
    names.append('concavity_direction_and_equal_mass')

    # Exhaust all three-event interval lists of ranks 0..3. The second
    # method enumerates literal rank paths, rather than partition states.
    intervals = [(a,b) for a in range(4) for b in range(a,4)]
    for limits in itertools.product(intervals, repeat=3):
        brute = set()
        for ranks in itertools.product(range(4), repeat=3):
            path = (0, *ranks, 3)
            if all(a <= x <= b for (a,b),x in zip(limits,ranks)) and all(a<=b for a,b in zip(path,path[1:])):
                brute.add(tuple(sorted((b-a for a,b in zip(path,path[1:]) if b>a), reverse=True)))
        require(sorted(brute) == check.partitions(0,3,list(limits)), 'tiny exhaustive path discrepancy')
    names.append('1000_interval_domains_against_literal_path_enumeration')

    # Actual R420 gate chosen from the OS assignment seed: promote the
    # target-8 d-single read from dimension 2 to its legal upper space, 3.
    frames = [check.basis(word['lines'][i] for i in frame) for frame in word['frames']]
    _, upper = check.rank_bounds(word, frames)
    mutant = copy.deepcopy(word)
    roots = [i for i,row in enumerate(word['lines']) if check.included(check.basis([row]), upper[8])]
    require(check.basis(word['lines'][i] for i in roots) == upper[8], 'control upper frame is not root-generated')
    mutant['frames'].append(roots)
    mutant['B'][8][0] = len(mutant['frames'])-1
    check.paid_profile(mutant)  # It must remain a genuinely legal schedule.
    bad = check.analyze(mutant)
    require({r['register'] for r in bad['gap_registers']} == {13,128}, 'worse legal schedule not detected')
    names.append('legal_rank3_promotion_detects_source13_and_target128_gaps')

    # Removing a mandatory rank-2 read from target 8's relaxed constraints
    # must expose the spuriously attractive unsplit rank-7 path.
    target = next(row for row in report['records'] if row['register'] == 128)
    weakened = list(target['intervals'])
    weakened[0] = (0, weakened[0][1])
    alternatives = check.partitions(0,7,weakened)
    require((7,) in alternatives and not check.majorizes(target['baseline_partition'],(7,)),
            'omitted mandatory-read bound not detected')
    names.append('omitted_mandatory_target_read_exposes_rank7_gap')

    mutant = copy.deepcopy(word)
    mutant['B'][8][0] = next(i for i,space in enumerate(frames) if not space)
    must_reject(lambda: check.analyze(mutant), 'frame below mandatory source space')
    names.append('illegal_zero_frame_rejected')
    mutant = copy.deepcopy(word)
    mutant['C'][0][0] = word['B'][8][0]
    must_reject(lambda: check.analyze(mutant), 'changed cleanup boundary')
    names.append('nonfull_cleanup_rejected')

    for field in ('total_partitions', 'variable_rank_mass'):
        mutant = copy.deepcopy(cert)
        mutant[field] += 1
        must_reject(lambda: check_certificate(mutant,cert), field)
        names.append('corrupted_' + field + '_rejected')
    mutant = copy.deepcopy(cert)
    mutant['gate_rank_intervals']['2:3'] -= 1
    must_reject(lambda: check_certificate(mutant,cert), 'omitted gate')
    names.append('omitted_gate_certificate_rejected')
    mutant = dict(inputs)
    mutant[WORD] = '0' * 64
    must_reject(lambda: check_pins(mutant), 'source pin')
    names.append('incorrect_source_pin_rejected')
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='write full fresh report to a new file')
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error('--output must name a new file')
    pins = json.loads((HERE / 'SOURCES.json').read_text())
    check_pins(pins['inputs'])
    baseline = subprocess.run([sys.executable,'-B',str(ROOT/PREDECESSOR),str(ROOT/WORD)],
                              capture_output=True,text=True)
    require(baseline.returncode == 0, 'predecessor replay failed:\n' + baseline.stdout + baseline.stderr)
    print('PASS_PINNED_R420_LABELS_FRAMES_660_COLUMNS_AND_H1_H5')
    word = json.loads(gzip.decompress((ROOT/WORD).read_bytes()))
    report = check.analyze(word)
    require(not report['gap_registers'], 'rank relaxation has a gap')
    cert = check.certificate(word,report)
    check_certificate(json.loads((HERE/'CERTIFICATE.json').read_text()), cert)
    names = controls(word,report,cert,pins['inputs'])
    with tempfile.TemporaryDirectory(prefix='r420-frame-bound-') as tmp:
        path = Path(tmp)/'report.json'
        path.write_text(json.dumps(report)+'\n')
        audit = subprocess.run([sys.executable,'-B',str(HERE/'audit.py'),'--primary-report',str(path)],
                               capture_output=True,text=True)
        require(audit.returncode == 0, 'independent audit failed:\n' + audit.stdout + audit.stderr)
        print(audit.stdout.strip())
    print('PASS_CONTROLS',len(names))
    print('PASS_FIXED_ORDER_B_FRAME_BOUND gates=837 registers=660 partitions=918 gaps=0')
    if args.output:
        result = dict(certificate=cert, report=report, controls=names,
                      predecessor_stdout=baseline.stdout, independent_stdout=audit.stdout)
        with args.output.open('x') as output:
            output.write(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print('REJECT:',error,file=sys.stderr)
        sys.exit(1)
