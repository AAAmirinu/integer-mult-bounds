"""Greedy width-73 bank patterns for a residual inventory {rank: count} (own code). Reproduces #404's and #409's published patterns for their inventories."""
def patterns(q):
    q = dict(q); n9, n8, n7, n5, n4 = (q.get(k, 0) for k in (9, 8, 7, 5, 4)); assert set(q) <= {9, 8, 7, 5, 4}
    pats = []
    def add(cnt, **kw):
        if cnt > 0: pats.append(dict(count=cnt, **kw))
    d = min(n7, n4); add(d, r4=1, r7=1, r8=1, r9=6); n7 -= d; n4 -= d; n8 -= d; n9 -= 6 * d
    add(n7, r7=1, r8=6, r9=2); n8 -= 6 * n7; n9 -= 2 * n7; n7 = 0
    add(n5, r5=1, r8=4, r9=4); n8 -= 4 * n5; n9 -= 4 * n5
    add(n4, r4=1, r8=3, r9=5); n8 -= 3 * n4; n9 -= 5 * n4
    a = n8 // 8; add(a, r8=8, r9=1); n8 -= 8 * a; n9 -= a
    assert n8 >= 0 and n9 >= 0, (n8, n9)
    extra = []
    if n8: extra.append(dict(count=1, r8=n8, r9=(73 - 8 * n8) // 9)); n9 -= (73 - 8 * n8) // 9
    a = n9 // 8; n9 -= 8 * a
    pats = [dict(count=a, r9=8, padding=1)] + [dict(p, padding=0) for p in pats]
    for e in extra: pats.append(dict(e, padding=73 - 8 * e['r8'] - 9 * e['r9']))
    if n9: pats.append(dict(count=1, r9=n9, padding=73 - 9 * n9))
    for p in pats: assert sum(int(k[1:]) * v for k, v in p.items() if k.startswith('r')) + p['padding'] == 73
    return pats
