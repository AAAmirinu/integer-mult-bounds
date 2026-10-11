"""Replay a saved idle-axis hosting selection with the standard library. The search solver is excluded."""

from collections import Counter, defaultdict

def windows(schedule):
    """schedule: ordered events dict(kind='local',stage,pair) | dict(kind='bridge',dst,src) | dict(kind='idle',pair,rank,idx).
    Returns {idx: (pair, rank, frozenset(stages))} - stages whose invocation lies strictly between the last touch of
    the pair and the idle child."""
    last = {}; out = {}; locals_ = []
    for pos, e in enumerate(schedule):
        k = e['kind']
        if k == 'local':
            locals_.append((pos, e['stage'], e['pair'])); last[e['pair']] = pos
        elif k == 'bridge':
            last[e['dst']] = pos; last[e['src']] = pos
        elif k == 'idle':
            p = e['pair']; lo = last.get(p, -1)
            st = frozenset(s for q, s, pp in locals_ if lo < q < pos and pp != p)
            out[e['idx']] = (p, e['rank'], st)      # an idle child acts on other coordinates (or the other member): not a touch
    return out


def expand(win, ys, zs, helpers, V2):
    """helpers: {stage: [(helper, width), ...]} for ONE replica; returns list of
    (idx, copy, offset, width, stage, helper) and the remainder rank of every (idx, copy).
    Copies of a piece are the 2V (side, port) data families; residuals packed from offset 0 in decreasing width."""
    pool = defaultdict(list)                    # (stage, width) -> helpers
    for s, hs in helpers.items():
        for h, w in hs: pool[s, w].append(h)
    for k in pool: pool[k].sort()
    need = defaultdict(list)                    # (idx, width) -> stages multiset in deterministic order
    for (idx, w, s), cnt in sorted(zs.items()): need[idx, w] += [s] * cnt
    out = []; rem = {}
    for idx in sorted(win):
        pats = sorted([(pat, cnt) for (i, pat), cnt in ys.items() if i == idx], key=lambda t: (-sum(t[0]), t[0]))
        copy = 0; ptr = Counter()
        r = win[idx][1]
        for pat, cnt in pats:
            for _ in range(cnt):
                off = 0
                for w in sorted(pat, reverse=True):
                    s = need[idx, w][ptr[idx, w]]; ptr[idx, w] += 1
                    h = pool[s, w].pop(0)
                    out.append((idx, copy, off, w, s, h)); off += w
                rem[idx, copy] = r - off; copy += 1
        while copy < V2: rem[idx, copy] = r; copy += 1
    return out, rem


def load_selection(path, key):
    import json
    from pathlib import Path
    d = json.loads(Path(path).read_text())[key]
    ys = {(i, tuple(pat)): n for i, pat, n in d['patterns']}
    zs = {(i, w, s): n for i, w, s, n in d['stages']}
    return ys, zs, d['proxy_saving']
