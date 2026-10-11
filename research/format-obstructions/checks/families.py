"""Port-family data for Thm B (neighbourhood rank), Thm C (copy lower bound) and the clique bound.

paired_bit(p)   paired cube, bit side: Q labels t_T (indicators of the 3-subset), form x^T (I - J/9) y, so
                form(S, T) = |S cap T| - 1 and 'in-cap' = |S cap T| = 1.
e8_bitdual()    120 E8 root lines in Q^8 with the E8 form; in-cap = orthogonal roots; F_2 decoder M = (J + Gram) mod 2
                = U U^T for the 9-bit words U (isomorphism search), its copy lower bound sum_i rank_Q Gram[S_i, S_i].
e8_complex(u)   the unique h = 9 complex labelling (from sat_e8.uniqueness_h9): neighbourhood ranks.
incap_omega     clique numbers of the paired-cube in-cap graphs by exact max-clique search.
p10_clique      the explicit 20-clique of the complex in-cap graph of the p = 10 program, checked inside the program's
                own realised lossless graph.
A neighbourhood N(S) of rank h - 1 equals q_S^perp, which is nondegenerate (its complement q_S is), so its form rank
equals its dimension; we assert this wherever the table uses it.
"""
import itertools
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "checks"))
from certs import load, replay  # noqa: E402
from f2 import dot, span_basis  # noqa: E402


def qrank(rows):
    M = [[Fr(x) for x in r] for r in rows]
    rk = 0
    ncol = len(M[0]) if M else 0
    for col in range(ncol):
        piv = next((i for i in range(rk, len(M)) if M[i][col] != 0), None)
        if piv is None:
            continue
        M[rk], M[piv] = M[piv], M[rk]
        for i in range(len(M)):
            if i != rk and M[i][col] != 0:
                f = M[i][col] / M[rk][col]
                M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
        rk += 1
    return rk


def paired_bit(p):
    P = [frozenset(2 * i + b for i, b in zip(I, bb)) for I in itertools.combinations(range(p), 3)
         for bb in itertools.product((0, 1), repeat=3)]
    h = 2 * p
    T = P[0]
    nb = [S for S in P if len(S & T) == 1]
    form = lambda S, U: Fr(len(S & U)) - Fr(len(S) * len(U), 9)   # noqa: E731
    assert all(form(S, T) == 0 for S in nb) and form(T, T) == 2
    r = qrank([[1 if i in S else 0 for i in range(h)] for S in nb])
    assert r == h - 1                       # N = U^perp, nondegenerate
    return dict(p=p, h=h, v=len(P), incap_deg=len(nb), N_rank=r)


def _e8_roots():
    Rt = []
    for i, j in itertools.combinations(range(8), 2):
        for si in (2, -2):
            for sj in (2, -2):
                r = [0] * 8
                r[i] = si
                r[j] = sj
                Rt.append(tuple(r))
    for s in itertools.product((1, -1), repeat=8):
        if s.count(-1) % 2 == 0:
            Rt.append(s)
    lines, seen = [], set()
    for r in Rt:
        if tuple(-x for x in r) in seen:
            continue
        seen.add(r)
        lines.append(r)
    return lines


def e8_bitdual():
    import networkx as nx
    lines = _e8_roots()
    v = len(lines)
    assert v == 120
    G = [[sum(a * b for a, b in zip(x, y)) // 4 for y in lines] for x in lines]
    assert all(G[i][i] == 2 for i in range(v))
    nb_ranks = set()
    for a in range(v):
        nb = [lines[b] for b in range(v) if b != a and G[a][b] == 0]
        nb_ranks.add((len(nb), qrank(nb)))
    off = [[(G[i][j] % 2 == 1) for j in range(v)] for i in range(v)]
    lab9 = [frozenset(t) for t in itertools.combinations(range(9), 3)] + \
           [frozenset(range(9)) - frozenset(p) for p in itertools.combinations(range(9), 2)]
    G9 = nx.Graph()
    G9.add_edges_from((i, j) for i in range(v) for j in range(i + 1, v) if len(lab9[i] & lab9[j]) % 2 == 0)
    Goff = nx.Graph()
    Goff.add_edges_from((i, j) for i in range(v) for j in range(i + 1, v) if off[i][j])
    iso = next(nx.algorithms.isomorphism.GraphMatcher(Goff, G9).isomorphisms_iter())
    U = [[1 if i in lab9[iso[s]] else 0 for i in range(9)] for s in range(v)]
    ok = all((sum(U[i][t] * U[j][t] for t in range(9)) % 2) == ((1 + G[i][j]) % 2) for i in range(v) for j in range(v))
    assert ok
    lb, betas = 0, []
    for t in range(9):
        S = [s for s in range(v) if U[s][t]]
        b = qrank([[G[a][c] for c in S] for a in S])      # pairing rank span(src) x span(readers), src = readers = S
        betas.append(b)
        lb += b
    assert sorted(nb_ranks) == [(63, 7)]
    return dict(v=v, h=8, neighbourhood=sorted(nb_ranks), decoder_equals_UUt=ok, totals=9, betas=betas,
                copy_lb=lb)


def e8_complex(u):
    from e8lib import NB, V
    ranks = set()
    for S in range(V):
        N = span_basis([u[T] for T in NB[S]])
        assert all(dot(x, u[S]) == 0 for x in N)
        ranks.add(len(N))
    assert ranks == {8}
    return dict(v=V, h=9, incap_deg=56, N_rank=8)


def incap_omega(p, kind):
    import networkx as nx
    P = [frozenset(2 * i + b for i, b in zip(I, bb)) for I in itertools.combinations(range(p), 3)
         for bb in itertools.product((0, 1), repeat=3)]
    pred = (lambda j: j == 1) if kind == "bit" else (lambda j: j in (0, 2))
    G = nx.Graph()
    G.add_nodes_from(range(len(P)))
    G.add_edges_from((a, b) for a in range(len(P)) for b in range(a + 1, len(P)) if pred(len(P[a] & P[b])))
    t0 = time.monotonic()
    cl, w = nx.max_weight_clique(G, weight=None)
    return dict(p=p, h=2 * p, kind=kind, omega=w, seconds=round(time.monotonic() - t0, 1))


def p10_clique(path):
    """5 pairwise-disjoint transversal 4-sets from the K5 stars, all 4 triples each: 20 ports, pairwise even overlap."""
    c = load(path)
    h, v = c["h"], c["v"]
    assert h == 20
    ports = c["ports"]
    index = {q: i for i, q in enumerate(ports)}
    E = list(itertools.combinations(range(5), 2))
    assert len(E) == 10
    sets = [[2 * i + (0 if e[0] == x else 1) for i, e in enumerate(E) if x in e] for x in range(5)]
    tri = [sum(1 << c_ for c_ in t) for s in sets for t in itertools.combinations(s, 3)]
    assert len(tri) == 20 and len(set(tri)) == 20
    T = [index[q] for q in tri]                                  # all 20 are ports of the program
    assert all(dot(a, a) == 1 for a in tri)
    assert all(dot(a, b) == 0 for a, b in itertools.combinations(tri, 2))
    taint, _, _, _ = replay(c, gate_check=False)
    realised = all(taint[v + S] >> Tt & 1 for S in T for Tt in T if S != Tt)
    assert realised
    return dict(size=len(T), orthonormal=True, all_pairs_lossless_in_program=realised, window_dim=h,
                label_dim_sum_le=h)
