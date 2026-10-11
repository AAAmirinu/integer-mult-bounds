"""Replay twelve exact early-reset helper reuses of the PR433 bit word.

Prepared with OpenAI Codex assistance; Apache-2.0. Inherited source notices
apply. PR433 is due to icekylinx with Codex assistance, building on ai-nanachi's
PR426 word, Dylan Crow's PR370 format and Jacob Sussman's E8 framework.
This file certifies a local scalar word; global pricing is a separate check.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

assert __debug__, 'Assertions must remain enabled'
BASE_SHA = '015811014644ed62acba1da590d9cf6ebdfe834d89867f8ce2b68722609072ea'
OUTPUT_SHA = 'fc5b2fb84dbbdbcf9b1bb36ebf768f31130dd5a93edec3d12f52c8e4be66ce48'


def encode(c):
    return json.dumps(c, sort_keys=True, separators=(',', ':')).encode()


def transform(old, z, mutation=None):
    c = copy.deepcopy(old)
    v, n = c['v'], 2*c['v']+c['R']
    r, s = z['retired_helper'], z['new_helper']
    assert 2*v <= r < n and 2*v <= s < n and r != s
    assert r not in c['ret'] and s not in c['ret']
    gates = c['A']+c['B']
    uses = lambda q: [i for i, (_, d, ss) in enumerate(gates) if q == d or q in ss]
    assert max(uses(r)) == z['reset_after_step'] < min(uses(s)) == z['new_step']
    assert z['reset_after_step'] == z['reset_after_gate'] + (len(c['A']) if z['reset_part'] == 'B' else 0)
    assert z['reset_size'] == len(z['reset_donors'])
    assert r not in z['reset_donors'] and s not in z['reset_donors']
    # Check the reset identity in the actual current clean-source basis.
    rows = [(1 << i) if i < v else 0 for i in range(n)]
    for _, d, ss in gates[:z['reset_after_step']+1]:
        for q in ss:
            rows[d] ^= rows[q]
    residual = rows[r]
    for q in z['reset_donors']:
        residual ^= rows[q]
    assert residual == 0
    reset = [z['frame'], r, z['reset_donors']]
    if mutation == 'late':
        offset = z['new_step']
        part = 'A' if offset < len(c['A']) else 'B'
        if part == 'B':
            offset -= len(c['A'])
        c[part].insert(offset, reset)
    elif mutation != 'omit':
        c[z['reset_part']].insert(z['reset_after_gate']+1, reset)
    physical = [q for q in range(n) if q != s]
    index = {q: j for j, q in enumerate(physical)}
    alias = lambda q: index[r if q == s else q]
    for part in ('A', 'B'):
        c[part] = [[f, alias(d), [alias(q) for q in ss]] for f, d, ss in c[part]]
    c['R'] -= 1
    c['start'] = [c['start'][q] for q in physical]
    c['final'] = [c['final'][q] for q in physical]
    c['ret'] = [index[q] for q in c['ret']]
    full = c['final'][0]
    c['C'] = [[full, d, ss] for _, d, ss in reversed(c['A']+c['B']) if d >= 2*v]
    # Recompute, rather than inherit, the entire helper-dirty compensation.
    dirty = [(1 << q) if q >= 2*v else 0 for q in range(n-1)]
    def run(gs):
        for _, d, ss in gs:
            assert d not in ss and len(ss) == len(set(ss))
            for q in ss:
                dirty[d] ^= dirty[q]
    run(c['A'])
    retained = [dirty[q] for q in c['ret']]
    for t, ss in enumerate(c['scatter']):
        for j in ss:
            dirty[v+t] ^= retained[j]
    run(c['B'])
    zero = c['start'][v]
    c['D'] = []
    for t in range(v):
        bits = dirty[v+t]
        ss = [q for q in range(2*v, n-1) if bits >> q & 1]
        assert bits == sum(1 << q for q in ss)
        if ss:
            c['D'].append([zero, v+t, ss])
    return c


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--selections', type=Path, default=Path(__file__).with_name('selections.json'))
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    raw = a.source.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == BASE_SHA
    old = json.loads(raw)
    selections = json.loads(a.selections.read_bytes())
    assert len(selections) == 12
    from local_audit import audit
    receipts = []
    c = old
    for i, z in enumerate(selections):
        c = transform(c, z)
        result = audit(c)
        result['round'] = i
        receipts.append(result)
    for field in ('lines', 'frames', 'form', 'coords', 'h', 'v'):
        assert c[field] == old[field]
    blob = encode(c)
    assert hashlib.sha256(blob).hexdigest() == OUTPUT_SHA
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out/'bit-source-centres.json').write_bytes(blob)
    (a.out/'CONSTRUCTION.json').write_text(json.dumps(dict(
        status='PASS_TWELVE_EARLY_RESETS_LOCAL_WORD',
        source_sha256=BASE_SHA, output_sha256=OUTPUT_SHA,
        selections_sha256=hashlib.sha256(a.selections.read_bytes()).hexdigest(),
        unchanged_geometry_fields=['lines', 'frames', 'form', 'coords', 'h', 'v'],
        old_R=old['R'], new_R=c['R'], rounds=receipts), indent=2)+'\n')
    print('PASS', c['R'], OUTPUT_SHA)


if __name__ == '__main__':
    main()
