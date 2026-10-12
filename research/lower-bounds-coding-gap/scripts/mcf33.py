"""Independent exact max-concurrent-flow for the dysfunctor 33-vertex instance.

Reads the edge table printed by the upstream checker,
    python scripts/verify-network-coding-33.py --print-edges   (dysfunctor/network-coding-counterexample @ 2ad45b0),
from the file given as the first argument (nothing from that repository is vendored here),
solves the edge-formulation concurrent-flow LP with HiGHS (scipy) and with OR-Tools GLOP,
then certifies the optimum exactly with a rational dual (edge lengths) and a rational primal.
Demands: x_ab: s_ab -> t_ab (1 unit each, 6 pairs) and O -> Z (24 units), as in the upstream default.
"""
import re, sys, os
from fractions import Fraction
from collections import defaultdict
import heapq
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

E = []
for line in open(sys.argv[1]):
    m = re.match(r"^\s+(\S+)-(\S+)\s+capacity (\d+)\s*$", line)
    if m:
        E.append((m.group(1), m.group(2), int(m.group(3))))
V = sorted({u for u, _, _ in E} | {v for _, v, _ in E})
assert len(V) == 33 and len(E) == 91 and sum(c for *_, c in E) == 149
idx = {v: i for i, v in enumerate(V)}
dem = [(f"s{a}{b}", f"t{a}{b}", 1) for a in (1, 2, 3) for b in (1, 2)] + [("O", "Z", 24)]
K, n, m = len(dem), len(V), len(E)

# variables: f[k, e, dir] (2 arcs per edge) then lambda
nv = K * m * 2 + 1
L = nv - 1
var = lambda k, e, d: (k * m + e) * 2 + d
# flow conservation: for each k, node v: out - in = lambda*d_k*(v==s) - lambda*d_k*(v==t)
Aeq = lil_matrix((K * n, nv)); beq = np.zeros(K * n)
for k, (s, t, d) in enumerate(dem):
    for e, (u, v, c) in enumerate(E):
        iu, iv = idx[u], idx[v]
        Aeq[k * n + iu, var(k, e, 0)] += 1; Aeq[k * n + iv, var(k, e, 0)] -= 1
        Aeq[k * n + iv, var(k, e, 1)] += 1; Aeq[k * n + iu, var(k, e, 1)] -= 1
    Aeq[k * n + idx[s], L] -= d
    Aeq[k * n + idx[t], L] += d
Aub = lil_matrix((m, nv)); bub = np.array([c for *_, c in E], float)
for e in range(m):
    for k in range(K):
        Aub[e, var(k, e, 0)] = 1; Aub[e, var(k, e, 1)] = 1
cost = np.zeros(nv); cost[L] = -1
res = linprog(cost, A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=beq, bounds=(0, None), method="highs")
print("HiGHS lambda* =", -res.fun, Fraction(-res.fun).limit_denominator(10000))

# OR-Tools GLOP as a second solver
from ortools.linear_solver import pywraplp
S = pywraplp.Solver.CreateSolver("GLOP")
f = {(k, e, d): S.NumVar(0, S.infinity(), "") for k in range(K) for e in range(m) for d in (0, 1)}
lam = S.NumVar(0, S.infinity(), "lam")
for e, (u, v, c) in enumerate(E):
    S.Add(sum(f[k, e, d] for k in range(K) for d in (0, 1)) <= c)
for k, (s, t, d) in enumerate(dem):
    bal = defaultdict(int)
    for x in V:
        expr = 0
        for e, (u, v, c) in enumerate(E):
            if u == x: expr += f[k, e, 0] - f[k, e, 1]
            if v == x: expr += f[k, e, 1] - f[k, e, 0]
        rhs = (lam * d if x == s else 0) - (lam * d if x == t else 0)
        S.Add(expr == rhs)
S.Maximize(lam); S.Solve()
print("GLOP  lambda* =", lam.solution_value())

# exact dual certificate: unit lengths. lambda <= sum c_e l_e / sum d_k dist_l(s_k,t_k)
adj = defaultdict(list)
for u, v, c in E:
    adj[u].append(v); adj[v].append(u)
def dist(s, t):
    D = {s: 0}; Q = [(0, s)]
    while Q:
        d0, x = heapq.heappop(Q)
        if x == t: return d0
        if d0 > D[x]: continue
        for y in adj[x]:
            if D.get(y, 10**9) > d0 + 1:
                D[y] = d0 + 1; heapq.heappush(Q, (d0 + 1, y))
ub = Fraction(sum(c for *_, c in E), sum(d * dist(s, t) for s, t, d in dem))
print("exact dual (unit lengths) upper bound:", ub, "distances", [dist(s, t) for s, t, _ in dem])

# exact primal: rationalise the HiGHS flow, repair conservation by path decomposition, rescale
x = res.x
lam_lb = None
paths = []
for k, (s, t, d) in enumerate(dem):
    # build arc flows, decompose greedily into s-t paths (floating), then use exact arithmetic on path amounts
    arc = defaultdict(float)
    for e, (u, v, c) in enumerate(E):
        a, b = x[var(k, e, 0)], x[var(k, e, 1)]
        if a - b > 1e-12: arc[(u, v, e)] += a - b
        elif b - a > 1e-12: arc[(v, u, e)] += b - a
    out = defaultdict(list)
    for (u, v, e), val in arc.items(): out[u].append((v, e))
    total = 0.0
    while True:
        # DFS for a path along positive arcs
        path, node, seen = [], s, {s}
        while node != t:
            nxt = [(v, e) for v, e in out[node] if arc[(node, v, e)] > 1e-10 and v not in seen]
            if not nxt: break
            v, e = max(nxt, key=lambda ve: arc[(node, ve[0], ve[1])])
            path.append((node, v, e)); seen.add(v); node = v
        if node != t or not path: break
        amt = min(arc[a] for a in path)
        for a in path: arc[a] -= amt
        paths.append((k, [e for *_, e in path], Fraction(amt).limit_denominator(10**6)))
        total += amt
load = defaultdict(Fraction); got = defaultdict(Fraction)
for k, es, amt in paths:
    got[k] += amt
    for e in es: load[e] += amt
scale = max(load[e] / E[e][2] for e in load)
lam_lb = min(got[k] / dem[k][2] for k in range(K)) / scale
print("exact primal lower bound:", lam_lb, float(lam_lb))
assert ub == lam_lb == Fraction(149, 150), (ub, lam_lb)
print("PASS max concurrent flow of the 33-vertex instance = 149/150 exactly (rational primal and dual)")
