"""Exact discovery of target re-syntheses (own code, new in this package).

Under #390's dirty-preconditioned bracket only the clean x-part of each target, and the y->y identity block, must be
kept: the helper response B*A^-1*h is precancelled from the actual word.  So y_i's B-phase feeds can be replaced by ANY
exact rational combination of available tokens whose frames form a nested chain from frame 0 to y_i's final frame.
A token is a register value held over a maximal position window [a, b) at a fixed version and frame: x/helper registers
(clean x-row), and other targets y_j whose y-row is exactly e_j (restore minus setup gives y_j's B-phase prefix).
Positions: p means 'after gate p-1'.  For each target we enumerate chains of 1-3 frames (nested in the final frame,
dims strictly increasing) whose climb partition beats the current one under phi = sum r*ln r (unbalanced/merged climbs
are cheaper under the concave moment), find split positions by an exact breakpoint scan (rank tests mod 2^61-1), then
solve exactly over Q preferring non-y tokens and the latest windows.
A target read by an existing restore gate (a #398 donor) is not redesigned: its value at the read must be unchanged."""
import math, os, sys
from fractions import Fraction as Q
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sinks as SK
P = (1 << 61) - 1
GKEY = 10000


def regs(g): return [g[2]] + [x[0] for x in g[3]] + (list(g[4]) if g[0] == 'out' else [])


def adds(g):
    if g[0] == 'out': return [(t, g[2], Q(a, b)) for t, a, b in g[3]]
    return [(g[2], s, Q(a, b)) for s, a, b in g[3]]


def axpy(d, src, q):
    for k, x in list(src.items()):
        z = d.get(k, 0) + q * x
        if z: d[k] = z
        else: d.pop(k, None)


def windows(c, gauged=()):
    """gauged: helpers whose dirt column must stay out of every target (#401's exterior-gauged pivots, K_p = 0);
    their dirt is tracked as extra coordinates GKEY + p next to the 120 clean x coordinates."""
    v = c['v']; n = 2 * v + c['R']; nA = len(c['A']); G = c['A'] + c['B']; NG = len(G)
    val = [({r: Q(1)} if r < v else {GKEY + r: Q(1)} if r in gauged else {}) for r in range(n)]; yv = [({r: Q(1)} if v <= r < 2 * v else {}) for r in range(n)]
    cur = list(c['start']); ver = [0] * n; op = [(0, 0, cur[r], dict(val[r]), dict(yv[r])) for r in range(n)]
    W = [[] for _ in range(n)]; scat = [{k: Q(a, b) for k, a, b in row} for row in c['scat']['table']]; ysc = None
    def roll(r, p):
        a, ve, f, x, y = op[r]
        if p > a: W[r].append((a, p, ve, f, x, y))
        op[r] = (p, ver[r], cur[r], dict(val[r]), dict(yv[r]))
    for t, g in enumerate(G):
        if t == nA:
            tot = [(dict(val[s]), dict(yv[s])) for _, s, _ in sorted(c['ret'])]
            for yy in range(v):
                for k, q in scat[yy].items(): axpy(val[v + yy], tot[k][0], q); axpy(yv[v + yy], tot[k][1], q)
            for yy in range(v, 2 * v): ver[yy] += 1; roll(yy, t)
            ysc = [dict(val[yy]) for yy in range(v, 2 * v)]
        ch = set()
        for r in set(regs(g)):
            if cur[r] != g[1]: cur[r] = g[1]; ch.add(r)
        if g[0] == 'out':
            sx, sy = dict(val[g[2]]), dict(yv[g[2]])
            for tt, s, q in adds(g): axpy(val[tt], sx, q); axpy(yv[tt], sy, q); ver[tt] += 1; ch.add(tt)
        else:
            for tt, s, q in adds(g): axpy(val[tt], val[s], q); axpy(yv[tt], yv[s], q); ver[tt] += 1; ch.add(tt)
        for r in ch: roll(r, t + 1)
    for r in range(n): roll(r, NG + 1)
    return W, val, ysc


def modvec(x): return {k: (q.numerator * pow(q.denominator, P - 2, P)) % P for k, q in x.items()}


class Basis:
    def __init__(s): s.b = {}
    def red(s, x):
        x = dict(x)
        while x:
            p = min(x)
            if p not in s.b: return x
            c = x[p]
            for k, vv in s.b[p].items():
                z = (x.get(k, 0) - c * vv) % P
                if z: x[k] = z
                else: x.pop(k, None)
        return x
    def add(s, x):
        x = s.red(x)
        if x: p = min(x); inv = pow(x[p], P - 2, P); s.b[p] = {k: vv * inv % P for k, vv in x.items()}
    def copy(s): b = Basis(); b.b = dict(s.b); return b


phi = lambda part: sum(r * math.log(r) for r in part)


class Search:
    def __init__(s, w, gauged=()):
        s.w = w; v = s.v = w['v']; n = s.n = 2 * v + w['R']; F = s.F = w['frames']; s.dim = [len(f) for f in F]
        s.nA = len(w['A']); s.NG = s.nA + len(w['B'])
        s.W, s.val, s.ysc = windows(w, set(gauged))
        s.SP = []
        for f in F:
            p = {}
            for x in f:
                while x:
                    k = x.bit_length() - 1
                    if k in p: x ^= p[k]
                    else: p[k] = x; break
            s.SP.append(p)
        s.TOK = defaultdict(list); s.YTOK = defaultdict(list)
        for r in range(n):
            for a, b, ve, f, x, y in s.W[r]:
                if b <= s.nA + 1: continue
                if v <= r < 2 * v:
                    if y != {r: Q(1)}: continue
                    d = s.prefix(r, x)
                    if d: s.YTOK[f].append((max(a, s.nA + 1), b, r, d, modvec(d)))
                elif x: s.TOK[f].append((max(a, s.nA + 1), b, r, x, modvec(x)))
        s.read = set()   # targets read as a y-source by an existing gate (restores/setups)
        for g in w['B']:
            for t, src, q in adds(g):
                if v <= src < 2 * v: s.read.add(src)
    def prefix(s, r, x):
        y = s.ysc[r - s.v]; d = {k: x.get(k, 0) - y.get(k, 0) for k in set(x) | set(y)}
        return {k: q for k, q in d.items() if q}
    def sub(s, a, b):
        p = s.SP[b]
        for x in s.F[a]:
            while x:
                k = x.bit_length() - 1
                if k not in p: return False
                x ^= p[k]
        return True
    def walk(s, i):
        fr = [0]
        for g in s.w['B']:
            if i in regs(g) and g[1] != fr[-1]: fr.append(g[1])
        if s.w['final'][i] != fr[-1]: fr.append(s.w['final'][i])
        return tuple(s.dim[fr[k + 1]] - s.dim[fr[k]] for k in range(len(fr) - 1))
    def toks(s, f, i): return s.TOK[f] + [t for t in s.YTOK[f] if t[2] != i]
    def feasible(s, chain, T, i):
        L = len(chain); TS = [s.toks(f, i) for f in chain]
        if L == 1:
            B = Basis()
            for t in TS[0]: B.add(t[4])
            return () if not B.red(T) else None
        pts = sorted({t[0] for t in TS[0]} | {t[1] - 1 for t in TS[-1]} | {t[0] for ts in TS for t in ts})
        def rec(l, lo, B):
            if l == L - 1:
                B = B.copy()
                for t in TS[l]:
                    if t[1] - 1 >= lo: B.add(t[4])
                return () if not B.red(T) else None
            for tau in [p for p in pts if p >= lo]:
                B2 = B.copy()
                for t in TS[l]:
                    if t[0] <= tau and t[1] - 1 >= lo: B2.add(t[4])
                r = rec(l + 1, tau, B2)
                if r is not None: return (tau,) + r
            return None
        return rec(0, s.nA + 1, Basis())
    def target(s, i): return s.prefix(i, s.val[i])
    def options(s, i):
        cur = s.walk(i); T = modvec(s.target(i)); Fi = s.w['final'][i]; pc = phi(cur); dim = s.dim
        nest = [g for g in range(len(s.F)) if 0 < dim[g] < dim[Fi] and s.sub(g, Fi) and s.toks(g, i)]
        out = []
        if s.feasible([Fi], T, i) is not None: out.append(((dim[Fi],), [Fi], ()))
        for g in nest:
            part = (dim[g], dim[Fi] - dim[g])
            if phi(part) <= pc + 1e-9: continue
            r = s.feasible([g, Fi], T, i)
            if r is not None: out.append((part, [g, Fi], r))
        if len(cur) >= 3:
            for g1 in nest:
                for g2 in nest:
                    if dim[g1] >= dim[g2] or not s.sub(g1, g2): continue
                    part = (dim[g1], dim[g2] - dim[g1], dim[Fi] - dim[g2])
                    if phi(part) <= pc + 1e-9: continue
                    r = s.feasible([g1, g2, Fi], T, i)
                    if r is not None: out.append((part, [g1, g2, Fi], r))
        out = [o for o in out if phi(o[0]) > pc + 1e-9]
        out.sort(key=lambda z: -phi(z[0]))
        return cur, out
    def design(s, i, chain, taus, noy):
        v = s.v; T = s.target(i); L = len(chain); bounds = [s.nA + 1] + list(taus) + [s.NG + 1]; cands = []
        for l, f in enumerate(chain):
            lo, hi = bounds[l], bounds[l + 1]
            for t in s.TOK[f] + ([] if noy else [t for t in s.YTOK[f] if t[2] != i]):
                a, b = t[0], t[1]
                if (b - 1 >= lo) if l == L - 1 else (a <= hi and b - 1 >= lo): cands.append((l, f, t))
        cands.sort(key=lambda z: (v <= z[2][2] < 2 * v, -z[2][0]))
        sol = SK.solve(T, [((l, f, t[2], t[0], t[1]), t[3]) for l, f, t in cands])
        if sol is None: return None
        out = []
        for (l, f, src, a, b), q in sol.items():
            pos = max(a, bounds[l]); assert pos <= b - 1 and (l == L - 1 or pos <= bounds[l + 1])
            out.append((pos, f, src, q))
        return sorted(out)
    def discover(s):
        """best option per target; returns (designs, report).  Excludes targets read by an existing y-source gate and
        designs whose y-donor is itself redesigned."""
        rep = {}; designs = {}
        for i in range(s.v, 2 * s.v):
            cur, out = s.options(i)
            if not out: continue
            part, chain, taus = out[0]
            dl = s.design(i, chain, taus, True); y = False
            if dl is None: dl = s.design(i, chain, taus, False); y = True
            donors = sorted({src for _, _, src, _ in dl if s.v <= src < 2 * s.v})
            rep[i] = dict(current=cur, new=part, chain=chain, taus=list(taus), ydonors=donors, read_by_existing_gate=i in s.read)
            if i not in s.read: designs[i] = dl
        for i in list(designs):
            if any(j in designs for _, _, j, _ in designs[i] if s.v <= j < 2 * s.v): del designs[i]
        return designs, rep
