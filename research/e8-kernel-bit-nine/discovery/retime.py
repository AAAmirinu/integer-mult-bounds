"""Retiming / descent on a bitE8/1 word: move gate frames inside their feasible interval
[close(LB_g | prev frames of participants), rootspan(AND of next frames)] to merge climbs (fewer, larger children).
Pinned: D gates (frame 0), y at frame 0 at the scatter, retained totals at FULL at COPY, start and final frames.
LB_g = x-support of non-target operands (source-span rule), integer support.
Greedy best-improvement sweeps scored by the linearized moment term r (m/r)^a (a = current c), exact re-price at end.
usage: retime.py IN.json.gz OUT.json.gz [sweeps] [seed]
Chafik Boukhalfa (chafreaky) with Anthropic Claude assistance; Apache-2.0."""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code'))
from e8core import *


class Model:
    def __init__(self, c, L=None):
        self.c = c; self.L = L or Lat(c['lines']); L = self.L
        self.v = v = c['v']; self.n = n = 2 * v + c['R']
        masks = to_masks(c, L)
        # global gate list: (phase, idx, frame mask, dst, srcs)
        self.gates = []
        for ph in ('D', 'A', 'B', 'C'):
            for k, (f, d, s) in enumerate(c[ph]): self.gates.append([ph, masks[f], d, list(s)])
        nA = len(c['D']) + len(c['A'])
        # per-register occurrence lists: entries are ('g', gate index) or ('p', fixed mask) pins, in time order
        occ = [[('p', masks[c['start'][r]])] for r in range(n)]
        pos = 0
        for gi, g in enumerate(self.gates):
            if gi == nA:  # scatter point
                for t in range(v): occ[v + t].append(('p', 0))
                for q in c['ret']: occ[q].append(('p', (1 << v) - 1))
            for x in [g[2]] + g[3]: occ[x].append(('g', gi))
        for r in range(n): occ[r].append(('p', masks[c['final'][r]]))
        self.occ = occ
        # position of each gate in each participant's list
        self.where = [dict() for _ in self.gates]
        for r in range(n):
            for i, (kind, x) in enumerate(occ[r]):
                if kind == 'g': self.where[x][r] = i
        self.pinned = [g[0] == 'D' for g in self.gates]
        self.lb = self._lower_bounds()

    def _lower_bounds(self):
        v, n = self.v, self.n
        sup = [1 << i if i < v else 0 for i in range(n)]  # +1 adds only: integer support = OR of supports
        lb = []
        for g in self.gates:
            ph, m, d, srcs = g; need = 0
            for s in srcs:
                sup[d] |= sup[s]
                if s < v or s >= 2 * v: need |= sup[s]
            if d >= 2 * v: need |= sup[d]
            lb.append(need)
        # check the integer-coefficient claim: every ADD is +1 so supports never cancel
        return [self.L.close(x) if x else 0 for x in lb]

    def fr(self, r, i):
        kind, x = self.occ[r][i]
        return x if kind == 'p' else self.gates[x][1]

    def interval(self, gi):
        g = self.gates[gi]; lo = self.lb[gi]; hi = (1 << self.v) - 1
        for r, i in self.where[gi].items():
            lo |= self.fr(r, i - 1); hi &= self.fr(r, i + 1)
        lo = self.L.close(lo)
        if lo & ~hi: return None
        return lo, self.L.close(hi) if hi != (1 << self.v) - 1 else hi

    def hist(self):
        H = Counter(); d = self.L.dim
        for r in range(self.n):
            prev = None
            for i in range(len(self.occ[r])):
                f = self.fr(r, i)
                if prev is not None and f != prev:
                    assert prev & ~f == 0, ('nest', r, i)
                    H[d(f) - d(prev)] += 1
                prev = f
        for q in self.c['ret']: H[8] += 1
        return H

    def to_word(self):
        c = dict(self.c); L = self.L
        fl = list(c['frames']); key = {}
        for k, fr in enumerate(fl): key.setdefault(sum(1 << i for i in fr), k)
        def fid(m):
            if m not in key:
                key[m] = len(fl); fl.append([i for i in range(self.v) if m >> i & 1])
            return key[m]
        out = {ph: [] for ph in ('D', 'A', 'B', 'C')}
        for ph, m, d, s in self.gates: out[ph].append([fid(m), d, list(s)])
        c.update(out); c['frames'] = fl
        return c


def sweep(M, a, rng, m=40, order=None):
    d = M.L.dim
    phi = lambda r: 0.0 if r == 0 else r * math.exp(a * math.log(m / r))
    gain = 0.0; moved = 0
    idx = list(range(len(M.gates))); rng.shuffle(idx)
    for gi in idx:
        if M.pinned[gi]: continue
        iv = M.interval(gi)
        if iv is None: continue
        lo, hi = iv; old = M.gates[gi][1]
        if lo == hi == old: continue
        parts = [(M.fr(r, i - 1), M.fr(r, i + 1)) for r, i in M.where[gi].items()]
        cands = {lo, hi}
        for p, q in parts:
            if lo & ~p == 0 and p & ~hi == 0: cands.add(p)
            if lo & ~q == 0 and q & ~hi == 0: cands.add(q)
        def score(F):
            dF = d(F); s = 0.0
            for p, q in parts: s += phi(dF - d(p)) + phi(d(q) - dF)
            return s
        base = score(old); best, bs = old, base
        for F in cands:
            if F == old: continue
            sF = score(F)
            if sF < bs - 1e-12: best, bs = F, sF
        if best != old:
            M.gates[gi][1] = best; gain += base - bs; moved += 1
    return moved, gain


if __name__ == '__main__':
    c = load_word(sys.argv[1]); sweeps = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
    M = Model(c); p0 = price_word(c); a = float(p0['c']); print('start c', p0['c'], float(p0['c']), dict(sorted(p0['H'].items())))
    assert M.hist() == p0['H'], (M.hist(), p0['H'])
    for s in range(sweeps):
        mv, g = sweep(M, a, rng)
        print('sweep', s, 'moved', mv, 'phi gain %.4f' % g, dict(sorted(M.hist().items())), flush=True)
        if mv == 0: break
    w = M.to_word(); p = price_word(w)
    print('end c', p['c'], float(p['c']), 'delta %.6e' % float(p['c'] - p0['c']))
    for nm, b in (('b2', B2), ('b3', B3)):
        k, bd = kappa(p['c'], b); print(nm, 'kappa', k, float(k), bd)
    save_word(w, sys.argv[2])
