#!/usr/bin/env python3
"""Check a bitE8/1 word with exact row spaces and explicit F2 column sets."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from functools import cache
import gzip
import hashlib
import json
from pathlib import Path


def row_space(rows):
    return _row_space(tuple(tuple(row) for row in rows))


@cache
def _row_space(rows):
    basis = {}
    for row in rows:
        row = list(map(Q, row))
        for p, b in sorted(basis.items()):
            a = row[p]
            row = [x - a * y for x, y in zip(row, b)]
        p = next((j for j, x in enumerate(row) if x), None)
        if p is None:
            continue
        a = row[p]
        row = tuple(x / a for x in row)
        for k, b in list(basis.items()):
            a = b[p]
            basis[k] = tuple(x - a * y for x, y in zip(b, row))
        basis[p] = row
    return tuple(b for _, b in sorted(basis.items()))


@cache
def contains(basis, row):
    row = list(map(Q, row))
    for b in basis:
        p = next(j for j, x in enumerate(b) if x)
        a = row[p]
        row = [x - a * y for x, y in zip(row, b)]
    return not any(row)


def determinant(rows):
    a = [list(map(Q, r)) for r in rows]
    result = Q(1)
    for j in range(len(a)):
        k = next((k for k in range(j, len(a)) if a[k][j]), None)
        if k is None:
            return Q(0)
        if k != j:
            a[k], a[j] = a[j], a[k]
            result = -result
        pivot = a[j][j]
        result *= pivot
        for k in range(j + 1, len(a)):
            coefficient = a[k][j] / pivot
            a[k] = [x - coefficient * y for x, y in zip(a[k], a[j])]
    return result


def check(c):
    assert c['format'] == 'bitE8/1' and c['form'] == '<x,y>/2'
    assert c['v'] == 120 and c['h'] == 8
    v, n = c['v'], 2 * c['v'] + c['R']
    roots = [tuple(r) for r in c['lines']]
    assert len(roots) == v and all(len(r) == 8 for r in roots)
    assert all(type(x) is int for r in roots for x in r)
    dot = lambda a, b: sum(x*y for x, y in zip(a, b))
    assert all(dot(r, r) == 4 for r in roots)
    assert all(dot(a, b) in (-2, 0, 2) for j, a in enumerate(roots) for b in roots[j+1:])
    full = row_space(roots)
    assert len(full) == 8
    signed_roots = set(roots) | {tuple(-x for x in r) for r in roots}
    assert len(signed_roots) == 240
    assert all(tuple(x - dot(a, b)//2*y for x, y in zip(a, b)) in signed_roots
               for a in signed_roots for b in roots)
    frames = []
    for ids in c['frames']:
        assert len(ids) == len(set(ids)) and all(type(i) is int and 0 <= i < v for i in ids)
        frames.append(row_space(roots[i] for i in ids))
    support = [{i for i, r in enumerate(roots) if contains(b, r)} for b in frames]
    assert len(c['start']) == len(c['final']) == n
    assert all(type(f) is int and 0 <= f < len(frames) for f in c['start'] + c['final'])
    current = list(c['start'])
    assert all(frames[current[r]] == row_space([roots[r]]) for r in range(v))
    assert all(not frames[current[r]] for r in range(v, 2*v)), 'targets start at zero'
    entrance_ranks = [len(frames[current[r]]) for r in range(2*v, n)]
    assert all(rank < 8 for rank in entrance_ranks), 'each helper has a nonzero residual'
    for r in range(2*v, n):
        b = frames[current[r]]
        assert all(sum(x != 0 for x in row) == 1 for row in b), ('non-coordinate helper entrance', r)
    values = [{r} for r in range(n)]
    integer_support = [{r} if r < v else set() for r in range(n)]
    histogram = Counter()
    z_failures = []
    support_checks = 0
    common_gates = 0
    used_frames = set(c['start']) | set(c['final'])
    phase_states = {}

    def move(r, f):
        old, new = frames[current[r]], frames[f]
        assert all(contains(new, row) for row in old), ('frame not nested', r, current[r], f)
        if old != new:
            assert len(new) > len(old)
            histogram[len(new) - len(old)] += 1
        current[r] = f

    def check_source(r, f, phase, gate):
        nonlocal support_checks
        active = {x for x in values[r] if x < v}
        assert active <= support[f], ('source support', phase, gate, r, sorted(active - support[f]))
        support_checks += 1
        missing = integer_support[r] - support[f]
        if missing:
            z_failures.append(dict(phase=phase, gate=gate, register=r, outside=sorted(missing)))

    def run(phase):
        nonlocal common_gates
        for j, (f, dest, sources) in enumerate(c[phase]):
            assert type(f) is int and 0 <= f < len(frames)
            assert v <= dest < n and len(sources) == len(set(sources))
            assert dest not in sources and all(type(s) is int and 0 <= s < n for s in sources)
            for r in [dest] + sources:
                move(r, f)
            used_frames.add(f)
            common_gates += 1
            for s in sources:
                if s < v or s >= 2*v:
                    check_source(s, f, phase, j)
                values[dest].symmetric_difference_update(values[s])
                integer_support[dest].update(integer_support[s])
            if dest >= 2*v:
                check_source(dest, f, phase, j)
        phase_states[phase] = dict(nonzero_frames=sum(bool(frames[f]) for f in current[v:]),
                                   dirty_helpers=sum(values[r] != {r} for r in range(2*v, n)))

    assert all(v <= dest < 2*v and not frames[f] for f, dest, sources in c['D']), 'zero-frame target preconditioner'
    run('D')
    assert current == c['start'], 'D must keep all entrance frames'
    run('A')
    retained = c['ret']
    assert len(retained) == len(set(retained))
    assert all(type(r) is int and 2*v <= r < n for r in retained)
    assert all(not frames[current[r]] for r in range(v, 2*v))
    copies = [set(values[r]) for r in retained]
    copy_ranks = [len(frames[current[r]]) for r in retained]
    assert all(r == 8 for r in copy_ranks)
    assert len(c['scatter']) == v
    for t, row in enumerate(c['scatter']):
        assert len(row) == len(set(row)) and all(type(k) is int and 0 <= k < len(copies) for k in row)
        for k in row:
            values[v+t].symmetric_difference_update(copies[k])
    histogram.update(copy_ranks)
    run('B')
    run('C')
    for r, f in enumerate(c['final']):
        move(r, f)
    assert all(frames[current[r]] == full for r in list(range(v)) + list(range(2*v, n)))
    for t in range(v):
        b = frames[current[v+t]]
        assert len(b) == 7 and all(dot(roots[t], row) == 0 for row in b)
    assert all(values[r] == {r} for r in range(v)), 'source columns not restored'
    assert all(values[r] == {r} for r in range(2*v, n)), 'helper columns not restored'
    assert all(values[v+t] == {v+t, t} for t in range(v)), 'wrong target columns'
    grams = {}
    for f in sorted(used_frames):
        b = frames[f]
        d = determinant([[Q(dot(x, y), 2) for y in b] for x in b])
        assert d > 0
        grams[f] = str(d)
    mass = sum(r*m for r, m in histogram.items())
    expected_mass = 8*c['R'] - sum(entrance_ranks) + sum(copy_ranks) + 2*v*7
    assert mass == expected_mass, ('local rank mass', mass, expected_mass)
    assert not z_failures, ('integer source support', z_failures[:5])
    return dict(R=c['R'], columns=n, gates={p:len(c[p]) for p in 'DABC'},
                exact_columns_pass=True, rational_frames_pass=True, f2_source_support_pass=True,
                source_support_checks=support_checks, common_frame_gates=common_gates,
                retained_registers=retained, retained_ranks=copy_ranks, local_histogram=dict(sorted(histogram.items())),
                local_rank_mass=mass, entrance_rank_total=sum(entrance_ranks),
                entrance_rank_counts=dict(sorted(Counter(entrance_ranks).items())), phase_states=phase_states,
                used_frames=len(used_frames), gram_determinants=grams,
                integer_support_failure_count=len(z_failures), integer_support_failure_examples=z_failures[:5])


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('word', type=Path)
    p.add_argument('--out', type=Path)
    args = p.parse_args()
    raw = args.word.read_bytes()
    c = json.loads(gzip.decompress(raw) if args.word.suffix == '.gz' else raw)
    result = check(c)
    result['word_sha256'] = hashlib.sha256(raw).hexdigest()
    text = json.dumps(result, indent=2) + '\n'
    if args.out:
        args.out.write_text(text)
    else:
        print(text, end='')
