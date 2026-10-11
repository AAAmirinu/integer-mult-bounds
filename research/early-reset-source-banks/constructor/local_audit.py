"""Independent all-column scalar and two-orientation frame audit.

Prepared with OpenAI Codex assistance; Apache-2.0.
"""
import argparse
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

assert __debug__, 'Assertions must remain enabled'


def rank(rows):
    pivots = {}
    for row in rows:
        row = list(map(Q, row))
        for j, b in sorted(pivots.items()):
            x = row[j]
            if x:
                row = [p-x*q for p, q in zip(row, b)]
        j = next((j for j, x in enumerate(row) if x), None)
        if j is not None:
            x = row[j]
            pivots[j] = [q/x for q in row]
    return len(pivots)


def audit(c):
    v, n = c['v'], 2*c['v']+c['R']
    frames = [set(f) for f in c['frames']]
    dim = [rank([c['lines'][j] for j in f]) for f in frames]
    assert len(frames) == 944 and c['h'] == 8
    assert len(c['start']) == len(c['final']) == n
    state = [1 << i for i in range(n)]
    cur = c['start'][:]
    hist = Counter()
    trace = []
    def move(q, f):
        old = cur[q]
        assert frames[old] <= frames[f], ('frame', q, old, f)
        if f != old:
            trace.append(('move', q, old, f))
            if dim[f] > dim[old]:
                hist[dim[f]-dim[old]] += 1
            cur[q] = f
    def run(gs):
        for f, d, ss in gs:
            assert 0 <= d < n and all(0 <= q < n for q in ss)
            assert d not in ss and len(ss) == len(set(ss))
            for q in [d]+ss:
                move(q, f)
            for q in ss:
                state[d] ^= state[q]
                trace.append(('add', d, q, f))
    run(c['D'])
    run(c['A'])
    assert all(dim[cur[q]] == 8 for q in c['ret'])
    assert all(dim[cur[q]] == 0 for q in range(v, 2*v))
    totals = [state[q] for q in c['ret']]
    assert len(totals) == 9
    for j, q in enumerate(c['ret']):
        trace.append(('copy', q, cur[q]))
        hist[dim[cur[q]]] += 1
        for t, ss in enumerate(c['scatter']):
            assert len(ss) == len(set(ss))
            if j in ss:
                state[v+t] ^= totals[j]
                trace.append(('scatter', v+t, q))
        trace.append(('erase', q, cur[q]))
    run(c['B'])
    run(c['C'])
    for q, f in enumerate(c['final']):
        move(q, f)
    expected = [1 << i for i in range(n)]
    for t in range(v):
        expected[v+t] ^= 1 << t
    assert state == expected, ('scalar', next((i for i in range(n) if state[i] != expected[i]), None))
    # Reverse every emitted operation; charge each former erase as the copy.
    # The scalar endpoint shear is self-inverse in F2, including all dirt.
    reverse = [1 << i for i in range(n)]
    rhist = Counter()
    labels = c['final'][:]
    for e in reversed(trace):
        if e[0] == 'move':
            _, q, old, new = e
            assert labels[q] == new and frames[old] <= frames[new]
            labels[q] = old
            if dim[new] > dim[old]:
                rhist[dim[new]-dim[old]] += 1
        elif e[0] == 'add':
            _, d, q, f = e
            assert labels[d] == labels[q] == f
            reverse[d] ^= reverse[q]
        elif e[0] == 'scatter':
            _, d, q = e
            reverse[d] ^= reverse[q]
        elif e[0] == 'erase':
            _, q, f = e
            assert labels[q] == f
            rhist[dim[f]] += 1
        else:
            assert e[0] == 'copy'
    assert labels == c['start'] and reverse == expected
    assert rhist == hist
    assert sum(r*k for r, k in hist.items()) == 8*n-168
    return dict(status='PASS_ALL_COLUMNS_AND_BOTH_FRAME_LEDGERS',
                R=c['R'], columns=n, operations=len(trace),
                forward_profile=dict(sorted(hist.items())),
                reverse_profile=dict(sorted(rhist.items())),
                exact_rational_frame_ranks=len(dim))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--selections', type=Path, default=Path(__file__).with_name('selections.json'))
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    from construct import BASE_SHA, OUTPUT_SHA, encode, transform
    raw = a.source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BASE_SHA
    c = json.loads(raw)
    controls = []
    for i, z in enumerate(json.loads(a.selections.read_bytes())):
        for mode in ('omit', 'late'):
            altered = transform(c, z, mutation=mode)
            try:
                audit(altered)
            except AssertionError as exc:
                assert not (mode == 'late' and i == 1), 'This delay is a valid positive control'
                controls.append(dict(round=i, mutation=mode, rejected=str(exc)))
            else:
                controls.append(dict(round=i, mutation=mode, accepted=True))
                assert mode == 'late' and i == 1, 'Unexpectedly accepted mutation'
        c = transform(c, z)
    result = audit(c)
    assert hashlib.sha256(encode(c)).hexdigest() == OUTPUT_SHA
    for name, phase in [('omit dirty compensation', 'D'), ('omit helper cleanup', 'C')]:
        altered = copy.deepcopy(c)
        altered[phase] = []
        try:
            audit(altered)
        except AssertionError as exc:
            controls.append(dict(mutation=name, rejected=str(exc)))
        else:
            raise AssertionError('Accepted mutation: '+name)
    result['source_sha256'] = BASE_SHA
    result['output_sha256'] = OUTPUT_SHA
    result['mutation_controls'] = controls
    a.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
