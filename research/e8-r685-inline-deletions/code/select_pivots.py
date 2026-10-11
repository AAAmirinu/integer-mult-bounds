"""Pivot selection by seeded annealing over the rank-1 axis-class assignment (PR #443 kernel format), from code/pivot_data.py output.
Every candidate carrier h joins one of the frame lines in its list fl[h]; a class with members T yields |T| - rank_F2 resp(T) pivots (donors = a greedy
F2 basis of the class, pivots = the other members, each written over the basis).  The annealer is the one of research/e8-r715-kernel-cap/select_kernel.py
(xorshift64*, bit-for-bit reproducible on any platform), restated on the pivot-data file.  The selection is a WITNESS: the exact maximum is bounded
above by code/exactgen.py (lower bounds on the sum-rank), see verify.py.  The parity step (an even entrance-rank total) is applied by kernel_exact.py.
usage: select_pivots.py PIVOT_DATA.json OUT_SELECTION.json SEED ITERS
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
import sys, json, math

class XS:
    M = (1 << 64) - 1
    def __init__(s, seed): s.x = (seed * 0x9E3779B97F4A7C15 + 0x1234567) & s.M or 1; [s.next() for _ in range(8)]
    def next(s):
        x = s.x; x ^= x >> 12; x ^= (x << 25) & s.M; x ^= x >> 27; s.x = x
        return (x * 0x2545F4914F6CDD1D) & s.M
    def below(s, n): return ((s.next() >> 11) * n) >> 53
    def unit(s): return (s.next() >> 11) / float(1 << 53)

def rank_f2(vs):
    b = []
    for y in vs:
        for x in b: y = min(y, y ^ x)
        if y: b.append(y); b.sort(reverse=True)
    return len(b)

def anneal(C, resp, axes, FRAMEL, seed, iters, T0=0.6, Tmin=0.03):
    rng = XS(seed)
    a = {h: axes[h][rng.below(len(axes[h]))] for h in C}
    cls = {i: [h for h in C if a[h] == i] for i in FRAMEL}
    rk = {i: rank_f2([resp[h] for h in cls[i]]) for i in FRAMEL}
    cur = sum(rk.values()); best, ba = cur, dict(a); movable = [h for h in C if len(axes[h]) > 1]
    for it in range(iters):
        T = T0 * (1 - it / iters) + Tmin
        h = movable[rng.below(len(movable))]; old = a[h]; alt = [i for i in axes[h] if i != old]; new = alt[rng.below(len(alt))]
        cls[old].remove(h); cls[new].append(h)
        ro, rn = rank_f2([resp[x] for x in cls[old]]), rank_f2([resp[x] for x in cls[new]])
        c2 = cur - rk[old] - rk[new] + ro + rn
        if c2 <= cur or rng.unit() < math.exp((cur - c2) / T):
            cur = c2; rk[old], rk[new] = ro, rn; a[h] = new
            if cur < best: best, ba = cur, dict(a)
        else: cls[new].remove(h); cls[old].append(h)
    return best, ba

def entries(FRAMEL, resp, a):
    sel = []
    for i in FRAMEL:
        mem = sorted(h for h in a if a[h] == i)
        ind, bl = [], []
        for h in mem:
            y, cm = resp[h], {h}
            for bv, bs in bl:
                if y >> (bv.bit_length() - 1) & 1: y ^= bv; cm = cm ^ bs
            if y: bl.append((y, cm)); bl.sort(key=lambda z: -z[0]); ind.append(h)
        bl = []
        for h in ind:
            y, cm = resp[h], {h}
            for bv, bs in bl:
                if y >> (bv.bit_length() - 1) & 1: y ^= bv; cm = cm ^ bs
            bl.append((y, cm)); bl.sort(key=lambda z: -z[0])
        indset = set(ind)
        for p in mem:
            if p in indset: continue
            y, cm = resp[p], set()
            for bv, bs in bl:
                if y >> (bv.bit_length() - 1) & 1: y ^= bv; cm = cm ^ bs
            assert y == 0
            sel.append([[i], p, sorted(cm)])
    return sel

if __name__ == '__main__':
    data, out, seed, iters = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    D = json.load(open(data)); resp = {int(k): v for k, v in D['resp'].items()}; fl = {int(k): v for k, v in D['fl'].items()}
    C = D['C']; best, a = anneal(C, resp, fl, D['FRAMEL'], seed, iters)
    sel = entries(D['FRAMEL'], resp, a)
    assert len(sel) == len(C) - best
    json.dump(sel, open(out, 'w'))
    print(json.dumps(dict(seed=seed, iters=iters, candidates=len(C), pivots=len(sel))))
