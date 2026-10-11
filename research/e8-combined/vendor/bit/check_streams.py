#!/usr/bin/env python3
"""Build and check both local streams, including a private COPY register."""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys
from check_exact import row_space


def check(c):
    v = c['v']
    n = 2*v + c['R']
    frames = [row_space(c['lines'][i] for i in ids) for ids in c['frames']]
    zero = next(i for i, f in enumerate(frames) if not f)
    cur = list(c['start'])
    records = []

    def move(r, frame):
        if frames[cur[r]] != frames[frame]:
            records.append(('move', r, cur[r], frame))
        cur[r] = frame

    def gates(phase):
        for frame, dst, sources in c[phase]:
            for r in [dst] + sources:
                move(r, frame)
            records.extend(('add', dst, src, frame) for src in sources)

    gates('D')
    gates('A')
    for k, source in enumerate(c['ret']):
        records.append(('copy', source, cur[source], zero))
        records.extend(('add', v+t, n, zero) for t, row in enumerate(c['scatter']) if k in row)
        records.append(('erase', source, cur[source], zero))
    gates('B')
    gates('C')
    for r, frame in enumerate(c['final']):
        move(r, frame)
    result = {}
    for reverse in (False, True):
        current = list(c['final'] if reverse else c['start']) + [None]
        values = [{r} for r in range(n)] + [set()]
        norm = [1]*n + [0]
        maximum = 1
        center = None
        histogram = Counter()
        copies = adds = 0
        dimension = lambda f: 8-len(frames[f]) if reverse else len(frames[f])
        for kind, a, b, frame in reversed(records) if reverse else records:
            if kind == 'move':
                before, after = (frame, b) if reverse else (b, frame)
                assert frames[current[a]] == frames[before]
                rank = dimension(after) - dimension(before)
                assert rank > 0
                current[a] = after
                histogram[rank] += 1
            elif kind == 'add':
                assert frames[current[a]] == frames[current[b]] == frames[frame]
                assert a != center and a != n and a != b
                if b == n:
                    assert center is not None
                values[a].symmetric_difference_update(values[b])
                norm[a] += norm[b]
                maximum = max(maximum, norm[a])
                adds += 1
            elif kind == ('erase' if reverse else 'copy'):
                assert center is None and not values[n] and current[n] is None
                assert frames[current[a]] == frames[b]
                center = a
                current[n] = frame
                values[n] = set(values[a])
                norm[n] = norm[a]
                rank = abs(dimension(b) - dimension(frame))
                assert rank == 8
                histogram[rank] += 1
                copies += 1
            else:
                assert kind == ('copy' if reverse else 'erase') and center == a
                assert frames[current[a]] == frames[b] and frames[current[n]] == frames[frame]
                assert values[n] == values[a]
                values[n] = set()
                norm[n] = 0
                current[n] = None
                center = None
        assert center is None and not values[n] and current[n] is None
        want_frames = c['start'] if reverse else c['final']
        assert all(frames[current[r]] == frames[want_frames[r]] for r in range(n))
        assert all(values[r] == ({r, r-v} if v <= r < 2*v else {r}) for r in range(n))
        result['reverse' if reverse else 'forward'] = dict(columns=n, copies=copies, adds=adds,
            row_l1_bound=maximum, histogram=dict(sorted(histogram.items())))
    assert result['forward']['histogram'] == result['reverse']['histogram']
    cf, cb = result['forward']['row_l1_bound'], result['reverse']['row_l1_bound']
    result['nine_stage_prefix_bits'] = ((1 << 18)*cf**5*cb**4).bit_length()
    result['eleven_stage_prefix_bits'] = ((1 << 18)*cf**6*cb**5).bit_length()
    result['records'] = len(records)
    result['all_checks_pass'] = True
    return result


if __name__ == '__main__':
    path = Path(sys.argv[1])
    raw = path.read_bytes()
    c = json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)
    result = check(c)
    result['word_sha256'] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, indent=2))
