"""Independent integer read-back of a fixed whole-residual packing.

No emitter, optimizer, or bank-tiling imports. Apache-2.0.
Chafreaky with OpenAI Codex assistance.
"""
import copy
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

load = lambda p: json.loads(gzip.decompress(p.read_bytes())) if p.suffix == '.gz' else json.loads(p.read_text())
ROOT = Path(__file__).resolve().parents[1]


def profile(selection, word, windows, original):
    widths = Counter(9 - len(word['frames'][f]) for f in word['start'][240:])
    assert widths == {9: 438, 8: 104, 7: 14, 5: 4}
    left = Counter({(s, w): n for s in range(9) for w, n in widths.items()})
    copies = Counter()
    paid = Counter({int(r): 72 * n for r, n in word['local_profile'].items()})
    for i, pattern, count in selection:
        assert isinstance(count, int) and count > 0 and i in windows
        pair, rank, allowed = windows[i]
        assert len({s for s, w in pattern}) == len(pattern)
        used = 0
        for s, w in pattern:
            assert s in allowed and w in widths
            left[s, w] -= count
            used += w
        assert used <= rank
        copies[i] += count
        if used < rank:
            paid[rank - used] += 8 * count
    assert copies == {i: 120 for i in windows} and min(left.values()) >= 0
    for e in original['idle_children']:
        if e['child'] not in windows and e['rank']:
            assert e['replicas'] == 8
            paid[e['rank']] += 8
    # All eight replicas have the same unhosted list. Each remaining helper
    # therefore contributes one bank, eight residuals of width w, and its pad.
    for (stage, width), count in left.items():
        if count:
            paid[73 - 8 * width] += count
    live = 7680 + sum(left.values())
    assert 73 * live - sum(r * n for r, n in paid.items()) == 2496
    return paid, left, live


def main(parent, candidate, output):
    word = load(parent / 'split-centres/CANONICAL-WORD.json.gz')
    original = load(parent / 'split-centres/GLOBAL-TEMPLATE.json.gz')
    old = load(parent / 'hosted/GLOBAL-TEMPLATE.json.gz')
    new = load(candidate / 'hosted/GLOBAL-TEMPLATE.json.gz')
    assert old['hosting']['windows'] == new['hosting']['windows']
    windows = {int(i): x for i, x in new['hosting']['windows'].items()}
    selection = load(ROOT / 'data/SELECTION.json')['nine-gauge-moment']['patterns']
    paid, left, live = profile(selection, word, windows, original)
    audit = load(candidate / 'AUDIT.json')
    assert audit['complex_profile'] == {str(r): n for r, n in sorted(paid.items())}
    assert audit['complex_live'] == live == 7746 and max(paid) == 8
    assert sum(left.values()) == 66 and all(w == 9 for (s, w), n in left.items() if n)
    assert new['hosting']['banks'] == [sum(n for (ss, w), n in left.items() if ss == s) for s in range(9)]
    assert new['local_programs'] == old['local_programs']
    for call in new['calls']:
        for h, (owner, route) in enumerate(call['owners'][240:]):
            if owner >= 7680:
                assert word['start'][240 + h] == 0 and len(route) == 2 and route[0] == 2
    baseline = load(parent / 'hosted/HOSTED.json')['global_profile']
    delta = {r: paid[r] - baseline.get(str(r), 0) for r in set(paid) | set(map(int, baseline))}
    delta = {r: n for r, n in delta.items() if n}
    assert delta == {1: 66, 5: -528, 6: 528, 9: -66}
    rejected = []
    def reject(name, mutate):
        bad = copy.deepcopy(selection)
        mutate(bad)
        try:
            profile(bad, word, windows, original)
        except (AssertionError, KeyError, IndexError, ValueError):
            rejected.append(name)
        else:
            raise AssertionError('accepted ' + name)
    pos = next(i for i, (_, p, n) in enumerate(selection) if p)
    reject('same invocation twice on a family', lambda a: a[pos][1].append(a[pos][1][0]))
    reject('nonexistent entrance width', lambda a: a[pos][1][0].__setitem__(1, 6))
    reject('stage outside the window', lambda a: a[pos][1][0].__setitem__(0, 99))
    reject('missing physical copy', lambda a: a[pos].__setitem__(2, a[pos][2] - 1))
    reject('extra physical copy', lambda a: a[pos].__setitem__(2, a[pos][2] + 1))
    result = dict(status='PASS_INDEPENDENT_MOMENT_PACKING_COUNTS', live=live, banks=66,
                  banks_per_stage=new['hosting']['banks'], all_entering_helpers_hosted=True,
                  profile=dict(sorted(paid.items())), delta_from_pr484=delta,
                  hosted_residuals=audit['complex_hosted_residuals'], maxchild=max(paid),
                  mutations_rejected=rejected,
                  selection_sha256=hashlib.sha256((ROOT / 'data/SELECTION.json').read_bytes()).hexdigest())
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(result['status'], live, max(paid), flush=True)


if __name__ == '__main__':
    main(*map(Path, sys.argv[1:]))
