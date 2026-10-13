#!/usr/bin/env python3
"""Exact fixed-order phase-B rank relaxation; prepared with OpenAI Codex assistance.

Copyright 2026 yuj1r0. Licensed under Apache-2.0 (repository LICENSE).
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import gzip
import hashlib
import json


def basis(rows):
    rows = [list(map(Fraction, row)) for row in rows if any(row)]
    pivot = 0
    for col in range(8):
        found = next((j for j in range(pivot, len(rows)) if rows[j][col]), None)
        if found is None:
            continue
        rows[pivot], rows[found] = rows[found], rows[pivot]
        scale = rows[pivot][col]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for j in range(len(rows)):
            if j != pivot and rows[j][col]:
                scale = rows[j][col]
                rows[j] = [a - scale * b for a, b in zip(rows[j], rows[pivot])]
        pivot += 1
        if pivot == 8:
            break
    return tuple(tuple(row) for row in rows[:pivot])


@lru_cache(None)
def join(spaces):
    return basis(row for space in spaces for row in space)


@lru_cache(None)
def perp(space):
    pivots = [next(i for i, value in enumerate(row) if value) for row in space]
    rows = []
    for free in range(8):
        if free in pivots:
            continue
        row = [Fraction(0)] * 8
        row[free] = Fraction(1)
        for p, v in zip(pivots, space):
            row[p] = -v[free]
        rows.append(row)
    return basis(rows)


def included(left, right):
    return len(join((left, right))) == len(right)


def registers(gate):
    return (gate[1], *gate[2])


def boundaries(word):
    current = list(word['start'])
    for section in ('D', 'A'):
        for f, t, sources in word[section]:
            for r in (t, *sources):
                current[r] = f
    # The fixed C suffix is entirely at the full frame on z registers;
    # targets do not occur there. Thus the first suffix frame is the final
    # frame in this particular word. Check this restriction explicitly.
    v = word['v']
    for f, t, sources in word['C']:
        if len(word['frames'][f]) != v:
            raise ValueError('cleanup is not at the full frame')
        if any(v <= r < 2 * v for r in (t, *sources)):
            raise ValueError('cleanup touches a target')
        if any(word['final'][r] != f for r in (t, *sources)):
            raise ValueError('cleanup/final boundary mismatch')
    return current, word['final']


def rank_bounds(word, frames):
    starts, ends = boundaries(word)
    lower = [frames[f] for f in starts]
    lows = []
    for gate in word['B']:
        regs = registers(gate)
        value = join(tuple(lower[r] for r in regs))
        lows.append(value)
        for r in regs:
            lower[r] = value
    upper_perps = [perp(frames[f]) for f in ends]
    highs = [None] * len(word['B'])
    for i in reversed(range(len(word['B']))):
        regs = registers(word['B'][i])
        value = join(tuple(upper_perps[r] for r in regs))
        highs[i] = perp(value)
        for r in regs:
            upper_perps[r] = value
    for i, (low, high) in enumerate(zip(lows, highs)):
        if not included(low, frames[word['B'][i][0]]) or not included(frames[word['B'][i][0]], high):
            raise ValueError(('baseline outside bounds', i))
    return lows, highs


def partitions(start, end, intervals):
    states = {(start, ())}
    for low, high in (*intervals, (end, end)):
        next_states = set()
        for previous, parts in states:
            for rank in range(max(previous, low), high + 1):
                new = parts + ((rank - previous,) if rank > previous else ())
                next_states.add((rank, tuple(sorted(new, reverse=True))))
        states = next_states
    return sorted(parts for rank, parts in states if rank == end)


def majorizes(left, right):
    if sum(left) != sum(right):
        return False
    return all(sum(left[:k]) >= sum(right[:k]) for k in range(1, max(len(left), len(right)) + 1))


def analyze(word):
    frames = [basis(word['lines'][i] for i in frame) for frame in word['frames']]
    lows, highs = rank_bounds(word, frames)
    starts, ends = boundaries(word)
    visits = [[] for _ in starts]
    for i, gate in enumerate(word['B']):
        for r in registers(gate):
            visits[r].append(i)
    gaps = []
    records = []
    profile = Counter()
    for r in list(range(8, len(starts))) + list(range(8)):
        lo, hi = len(frames[starts[r]]), len(frames[ends[r]])
        intervals = [(len(lows[i]), len(highs[i])) for i in visits[r]]
        old_ranks = [lo] + [len(frames[word['B'][i][0]]) for i in visits[r]] + [hi]
        original = tuple(sorted((b-a for a,b in zip(old_ranks, old_ranks[1:]) if b>a), reverse=True))
        candidates = partitions(lo, hi, intervals)
        profile.update(original)
        bad = [parts for parts in candidates if not majorizes(original, parts)]
        record = dict(register=r, start_rank=lo, final_rank=hi, intervals=intervals,
                      baseline_partition=original, relaxed_partitions=candidates)
        records.append(record)
        if bad:
            gaps.append(dict(register=r, baseline=original, undominated=bad))
    return dict(gates=len(word['B']), registers=len(starts),
                gate_rank_intervals=dict(sorted(Counter(f'{len(a)}:{len(b)}' for a,b in zip(lows,highs)).items())),
                b_and_exit_profile=dict(sorted(profile.items())),
                total_partitions=sum(len(r['relaxed_partitions']) for r in records),
                gap_registers=gaps, records=records)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def paid_profile(word):
    """Recount all positive climbs, including fixed C/final tails and COPYs."""
    frames = [basis(word['lines'][i] for i in frame) for frame in word['frames']]
    current = list(word['start'])
    counts = Counter()

    def climb(register, frame):
        old = current[register]
        if not included(frames[old], frames[frame]):
            raise ValueError(('illegal climb', register, old, frame))
        rank = len(frames[frame]) - len(frames[old])
        if rank:
            counts[rank] += 1
        current[register] = frame

    for section in ('D', 'A', 'B', 'C'):
        if section == 'B':
            counts.update(len(frames[current[r]]) for r in word['ret'])
        for f, t, sources in word[section]:
            for register in (t, *sources):
                climb(register, f)
    for r, f in enumerate(word['final']):
        climb(r, f)
    return dict(sorted(counts.items()))


def certificate(word, report):
    types = Counter()
    for row in report['records']:
        key = (tuple(row['baseline_partition']), tuple(map(tuple, row['relaxed_partitions'])))
        types[key] += 1
    full = paid_profile(word)
    variable = report['b_and_exit_profile']
    fixed = {k: full.get(k, 0) - variable.get(k, 0) for k in sorted(set(full) | set(variable))}
    fixed = {k: v for k, v in fixed.items() if v}
    if any(value < 0 for value in fixed.values()):
        raise ValueError('negative fixed-exterior count')
    result = {k: v for k, v in report.items() if k not in ('records', 'gap_registers')}
    result.update(
        schema='r420-phase-b-frame-bound/1',
        status='PASS_FIXED_ORDER_B_FRAME_BOUND' if not report['gap_registers'] else 'RELAXATION_GAP',
        input_canonical_sha256=hashlib.sha256(canonical(word)).hexdigest(),
        all_register_paths_sha256=hashlib.sha256(canonical(report['records'])).hexdigest(),
        gap_registers=report['gap_registers'],
        fixed_exterior_profile=fixed,
        full_local_profile=full,
        full_rank_mass=sum(k * count for k, count in full.items()),
        variable_rank_mass=sum(k * count for k, count in variable.items()),
        partition_types=[dict(count=n, baseline_partition=old, relaxed_partitions=parts)
                         for (old, parts), n in sorted(types.items())],
    )
    return json.loads(json.dumps(result))
