#!/usr/bin/env python3
"""Independent exact audit of the fixed-order R420 phase-B rank relaxation.

Usage: python3 -I audit.py [--primary-report PRIMARY_REPORT.json]

This file imports no repository module. Unlike check.py's rank/partition dynamic
program, it enumerates ordered compositions of each register's total rank
increase and checks whether their cuts can occur at that register's gate visits.
All linear algebra is exact over Q; intersections use orthogonal complements.
Prepared with OpenAI Codex assistance. Copyright 2026 yuj1r0.
Licensed under Apache-2.0 (repository LICENSE).
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import gzip
import hashlib
from itertools import accumulate
import json
from pathlib import Path

SOURCE_SHA256 = '9721a3819efd68307f66f00d84a952eb28eb7c3ad2ce79653ce295c98a764784'
DIMENSION = 8


def require(condition, message):
    if not condition:
        raise ValueError(message)


@lru_cache(None)
def echelon(rows):
    """Insert rows one at a time, keeping a canonical reduced rational basis."""
    pivots = []
    for original in rows:
        row = list(map(Fraction, original))
        for pivot, existing in pivots:
            coefficient = row[pivot]
            if coefficient:
                row = [a - coefficient * b for a, b in zip(row, existing)]
        if not any(row):
            continue
        pivot = next(i for i, value in enumerate(row) if value)
        coefficient = row[pivot]
        row = [value / coefficient for value in row]
        pivots = [(p, tuple(a - previous[pivot] * b for a, b in zip(previous, row)))
                  for p, previous in pivots]
        pivots.append((pivot, tuple(row)))
        pivots.sort()
    return tuple(row for _, row in pivots)


@lru_cache(None)
def span(spaces):
    return echelon(tuple(row for space in spaces for row in space))


@lru_cache(None)
def orthogonal(space):
    pivot_columns = [next(i for i, value in enumerate(row) if value) for row in space]
    rows = []
    for free in range(DIMENSION):
        if free in pivot_columns:
            continue
        row = [Fraction(int(i == free)) for i in range(DIMENSION)]
        for pivot, equation in zip(pivot_columns, space):
            row[pivot] = -equation[free]
        rows.append(tuple(row))
    return echelon(tuple(rows))


@lru_cache(None)
def intersection(spaces):
    return orthogonal(span(tuple(orthogonal(space) for space in spaces)))


def compositions(total):
    """All ordered positive compositions, encoded by the cuts between unit ranks."""
    if total == 0:
        yield ()
        return
    for cuts in range(1 << (total - 1)):
        parts = []
        previous = 0
        for position in range(1, total):
            if cuts & (1 << (position - 1)):
                parts.append(position - previous)
                previous = position
        yield tuple(parts + [total - previous])


def fits_visits(parts, start, intervals):
    """A gate visit can realize no jump or exactly the next composition part.

    The fixed final boundary likewise realizes at most one remaining jump.
    Intermediate ranks cannot be skipped, because every composition part is a
    distinct positive jump in the normalized event schedule.
    """
    ranks = list(accumulate(parts, initial=start))
    possible = {0}
    for low, high in intervals:
        following = set()
        for used in possible:
            if low <= ranks[used] <= high:
                following.add(used)
            if used < len(parts) and low <= ranks[used + 1] <= high:
                following.add(used + 1)
        possible = following
        if not possible:
            return False
    return len(parts) in possible or len(parts) - 1 in possible


def feasible_partitions(start, end, intervals):
    require(start <= end, 'rank decreases between fixed boundaries')
    return sorted({tuple(sorted(parts, reverse=True))
                   for parts in compositions(end - start)
                   if fits_visits(parts, start, intervals)})


def majorizes(left, right):
    if sum(left) != sum(right):
        return False
    size = max(len(left), len(right))
    a = list(accumulate(left + (0,) * (size - len(left))))
    b = list(accumulate(right + (0,) * (size - len(right))))
    return all(x >= y for x, y in zip(a, b))


def self_checks():
    require(feasible_partitions(0, 3, []) == [(3,)], 'final boundary check')
    require(feasible_partitions(0, 3, [(1, 2)]) == [(2, 1)], 'single visit check')
    require(feasible_partitions(0, 3, [(1, 2), (1, 2)]) == [(1, 1, 1), (2, 1)],
            'two-visit cut check')
    require(feasible_partitions(0, 3, [(2, 2), (1, 1)]) == [], 'descent rejection')
    require(majorizes((3, 1), (2, 2)) and not majorizes((2, 2), (3, 1)),
            'majorization direction check')
    require(not majorizes((3,), (2,)), 'unequal mass rejection')
    axes = [tuple(int(i == j) for i in range(DIMENSION)) for j in range(3)]
    first, second = echelon(tuple(axes[:2])), echelon(tuple(axes[1:]))
    require(intersection((first, second)) == echelon((axes[1],)), 'exact intersection check')
    require(orthogonal(orthogonal(first)) == first, 'double complement check')


def audit(word):
    frames = [echelon(tuple(tuple(word['lines'][i]) for i in frame)) for frame in word['frames']]
    current = [frames[i] for i in word['start']]
    for phase in ('D', 'A'):
        for frame, destination, sources in word[phase]:
            for register in [destination] + sources:
                current[register] = frames[frame]
    # Scatter changes values only, so these are the frames entering B.
    entry = current[:]
    final = [frames[i] for i in word['final']]
    lower_bounds = []
    for _, destination, sources in word['B']:
        registers = [destination] + sources
        lower = span(tuple(current[r] for r in registers))
        lower_bounds.append(lower)
        for register in registers:
            current[register] = lower
    current = final[:]
    upper_bounds = []
    for _, destination, sources in reversed(word['B']):
        registers = [destination] + sources
        upper = intersection(tuple(current[r] for r in registers))
        upper_bounds.append(upper)
        for register in registers:
            current[register] = upper
    upper_bounds.reverse()
    intervals = [[] for _ in entry]
    visits = [[] for _ in entry]
    for gate, lower, upper in zip(word['B'], lower_bounds, upper_bounds):
        frame, destination, sources = gate
        actual = frames[frame]
        require(span((lower, actual)) == actual and span((actual, upper)) == upper,
                'baseline frame lies outside propagated bounds')
        for register in [destination] + sources:
            intervals[register].append((len(lower), len(upper)))
            visits[register].append(len(actual))
    records = []
    profile = Counter()
    choices = Counter()
    for register in range(len(entry)):
        start, end = len(entry[register]), len(final[register])
        ranks = [start] + visits[register] + [end]
        require(all(a <= b for a, b in zip(ranks, ranks[1:])), 'baseline rank descent')
        baseline = tuple(sorted((b - a for a, b in zip(ranks, ranks[1:]) if b > a), reverse=True))
        candidates = feasible_partitions(start, end, intervals[register])
        require(baseline in candidates, f'baseline absent for register {register}')
        require(all(majorizes(baseline, other) for other in candidates),
                f'rank relaxation has a gap at register {register}')
        profile.update(baseline)
        choices[len(candidates)] += 1
        records.append(dict(register=register, start_rank=start, final_rank=end,
                            intervals=intervals[register], baseline_partition=baseline,
                            relaxed_partitions=candidates))
    result = dict(gates=len(word['B']), registers=len(entry),
                  gate_rank_intervals=dict(sorted(Counter(f'{len(a)}:{len(b)}'
                      for a, b in zip(lower_bounds, upper_bounds)).items())),
                  b_and_exit_profile=dict(sorted(profile.items())),
                  total_partitions=sum(len(record['relaxed_partitions']) for record in records),
                  gap_registers=[], records=records)
    require(result['gate_rank_intervals'] == {'2:3': 120, '3:4': 10, '4:4': 457,
                                            '4:5': 10, '6:6': 120, '7:7': 120},
            'unexpected interval census')
    require(profile == {1: 720, 2: 451, 5: 120}, 'unexpected paid B/exit profile')
    require(choices == {1: 420, 2: 222, 3: 18}, 'unexpected partition census')
    require(result['total_partitions'] == 918, 'unexpected partition total')
    return result


def compare(primary, independent):
    # JSON roundtrip normalizes tuples and integer dictionary keys.
    independent = json.loads(json.dumps(independent))
    for key in ('gates', 'registers', 'gate_rank_intervals', 'b_and_exit_profile',
                'total_partitions', 'gap_registers'):
        require(primary[key] == independent[key], f'primary report mismatch: {key}')
    primary_records = {record['register']: record for record in primary['records']}
    require(len(primary_records) == len(primary['records']) == len(independent['records']),
            'primary report duplicate/missing registers')
    for expected in independent['records']:
        actual = primary_records[expected['register']]
        for key, value in expected.items():
            require(actual[key] == value, f'primary register {expected["register"]}: {key}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--primary-report', type=Path)
    args = parser.parse_args()
    self_checks()
    source = Path(__file__).resolve().parents[2] / 'research/e8-bit-r420/data/bitE8mut-r420.json.gz'
    compressed = source.read_bytes()
    require(hashlib.sha256(compressed).hexdigest() == SOURCE_SHA256, 'source pin mismatch')
    result = audit(json.loads(gzip.decompress(compressed)))
    if args.primary_report:
        compare(json.loads(args.primary_report.read_text()), result)
    summary = {key: value for key, value in result.items() if key != 'records'}
    summary.update(source_sha256=SOURCE_SHA256, independent_audit='PASS',
                   primary_report_compared=bool(args.primary_report))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
