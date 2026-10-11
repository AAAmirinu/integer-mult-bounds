"""Exact SAT checks on the E8 in-cap graph (CaDiCaL through python-sat).

Model. An 'in-cap labelling' of a graph H on the 120 E8 lines assigns to each line T a nondegenerate k-dimensional
subspace A_T of (F_2^r, standard dot product), with A_S orthogonal to A_T for every edge {S, T} of H. H below is the
E8 non-orthogonal graph (3360 edges, degree 56, clique number 8): the pairs the E8 decoder leaves to lossless
helpers. By Cor. A1 of PROOF.md every such pair needs orthogonal labels.

Reduction (WLOG, argued in PROOF.md section 6): fix an 8-clique C of H. Its labels are pairwise orthogonal and
nondegenerate, so they form an orthogonal direct sum, and the window splits along them. For k = 1 the 8 labels are
orthonormal and can be taken to be e_1..e_8; for k = 2 each plane is the standard I_2 or the hyperbolic H plane and
the window form is the sum of the 8 plane forms and I on the complement (any non-alternating form of that rank is
isometric to I_r). Every other line T then has A_T supported on the blocks of the clique members not adjacent to T,
plus the complement coordinates.

 (a) uniqueness_h9: k = 1, r = 9, with distinct labels (E0 of gx.check1): exactly ONE labelling, enumerated to
     exhaustion, and it is Sussman's (u_S . u_T = 1 on every E8-orthogonal pair, 0 on every in-cap pair).
 (b) k2_planes: k = 2, r = 16 and 17: UNSAT for every plane-type pattern of the clique (any port type).
Controls: k = 1, r = 8 is UNSAT and r = 9 SAT (calibration); the k = 2 encoder at r = 18 accepts the direct sum of
two copies of the k = 1 solution (positive control).
"""
import itertools
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e8lib import G, NB, ORTH_PAIRS, V  # noqa: E402
from f2 import dot, span_basis  # noqa: E402


# ----------------------------------------------------------------------------------------------------------------
# (a) k = 1: the admissible labellings at h = 9 (from the local research file satlab.py)
CL = [119, 118, 102, 98, 79, 72, 37, 34]   # an 8-clique (Hamming indices) of the in-cap graph


class Model:
    """CNF of: u: lines -> F_2^h, u.u = 1, u_S.u_T = 0 on in-cap pairs, labels distinct; CL = e_1..e_8."""

    def __init__(s, h):
        s.h = h
        s.nv = 0
        s.cl = []
        s.T = s.var()
        s.cl.append([s.T])
        s.u = [[None] * h for _ in range(V)]
        for S in range(V):
            for k in range(h):
                if S in CL:
                    s.u[S][k] = s.T if k == CL.index(S) else -s.T
                elif k < 8 and G[S][CL[k]] != 0:
                    s.u[S][k] = -s.T
                else:
                    s.u[S][k] = s.var()
        for S in range(V):
            if S not in CL:
                s.bil_eq(S, S, 1)
        for S in range(V):
            for T in NB[S]:
                if S < T:
                    s.bil_eq(S, T, 0)
        for S in range(V):
            for T in range(S + 1, V):
                ds = [s.xor2(s.u[S][k], s.u[T][k]) for k in range(h)]
                ds = [x for x in ds if x != -s.T]
                s.cl.append(ds)

    def var(s):
        s.nv += 1
        return s.nv

    def and2(s, a, b):
        if a == -s.T or b == -s.T:
            return -s.T
        if a == s.T:
            return b
        if b == s.T:
            return a
        y = s.var()
        s.cl += [[-y, a], [-y, b], [y, -a, -b]]
        return y

    def xor2(s, a, b):
        if a == -s.T:
            return b
        if b == -s.T:
            return a
        if a == s.T:
            return -b
        if b == s.T:
            return -a
        y = s.var()
        s.cl += [[-y, a, b], [-y, -a, -b], [y, -a, b], [y, a, -b]]
        return y

    def xor_eq(s, lits, c):
        lits = [x for x in lits if x != -s.T]
        n_t = sum(1 for x in lits if x == s.T)
        lits = [x for x in lits if x != s.T]
        c ^= n_t & 1
        if not lits:
            if c:
                s.cl.append([])
            return
        acc = lits[0]
        for x in lits[1:]:
            acc = s.xor2(acc, x)
        s.cl.append([acc] if c else [-acc])

    def bil_eq(s, S, T, c):
        s.xor_eq([s.and2(s.u[S][k], s.u[T][k]) for k in range(s.h)], c)

    def labels(s, m):
        out = []
        for S in range(V):
            x = 0
            for k in range(s.h):
                lit = s.u[S][k]
                b = (lit == s.T) if abs(lit) == s.T else ((m[abs(lit) - 1] > 0) == (lit > 0))
                if b:
                    x |= 1 << k
            out.append(x)
        return out


def uniqueness_h9():
    from pysat.solvers import Cadical153
    t0 = time.monotonic()
    m = Model(9)
    sol = Cadical153(bootstrap_with=m.cl)
    free = [m.u[S][k] for S in range(V) for k in range(9) if abs(m.u[S][k]) != m.T]
    sols = []
    while sol.solve():
        mod = sol.get_model()
        sols.append(m.labels(mod))
        sol.add_clause([-x if (mod[abs(x) - 1] > 0) == (x > 0) else x for x in free])
        assert len(sols) <= 5, "more than 5 solutions"
    sol.delete()
    assert len(sols) == 1, len(sols)
    u = sols[0]
    # independent verification of the labelling, not through the CNF
    assert all(dot(u[S], u[S]) == 1 for S in range(V))
    assert all(dot(u[S], u[T]) == 0 for S in range(V) for T in NB[S])
    assert len(set(u)) == V
    assert all(dot(u[a], u[b]) == 1 for a, b in ORTH_PAIRS)       # Sussman's Gram: 1 on all 3780 E8-orthogonal pairs
    # neighbourhood rank (Thm B data): u_S is orthogonal to N(S) and u_S.u_S = 1, so rank N(S) <= 8
    ranks = {len(span_basis([u[T] for T in NB[S]])) for S in range(V)}
    # controls: h = 8 admits no labelling (calibration); the same CNF with the distinctness clauses is satisfiable at 9
    t8 = Model(8)
    s8 = Cadical153(bootstrap_with=t8.cl)
    unsat8 = not s8.solve()
    s8.delete()
    assert unsat8, "control failed: an h = 8 labelling exists"
    return dict(solutions=len(sols), gram_is_sussman=True, labels_distinct=True, incap_degree=56,
                neighbourhood_ranks=sorted(ranks), h8_control_unsat=unsat8, vars=m.nv, clauses=len(m.cl),
                seconds=round(time.monotonic() - t0, 1)), u


# ----------------------------------------------------------------------------------------------------------------
# (b) k-dimensional planes on the full in-cap graph (from the local research files plsat.py and plsat2.py)
def _graph():
    adj = [set(NB[a]) for a in range(V)]
    return adj


def max_clique8(adj):
    import networkx as nx
    g = nx.Graph()
    g.add_nodes_from(range(V))
    g.add_edges_from((a, b) for a in range(V) for b in adj[a] if a < b)
    best = max(nx.find_cliques(g), key=len)
    return sorted(best)


class PlaneModel:
    """k-dim planes, form I_r, clique C fixed to coordinate blocks. usage as plsat.py (local research)."""

    def __init__(s, k, r, adj, C, dist=False):
        s.k, s.r, s.nv, s.cl = k, r, 1, [[1]]
        s.T = 1
        n = len(adj)
        s.n = n
        idx = {c: i for i, c in enumerate(C)}
        s.vec = {}
        for T in range(n):
            for j in range(k):
                if T in idx:
                    s.vec[T, j] = [s.T if t == k * idx[T] + j else -s.T for t in range(r)]
                else:
                    allowed = set(range(k * len(C), r))
                    for c, i in idx.items():
                        if c not in adj[T]:
                            allowed |= set(range(k * i, k * i + k))
                    s.vec[T, j] = [s.new() if t in allowed else -s.T for t in range(r)]
        for T in range(n):
            if T in idx:
                continue
            for a in range(k):
                for b in range(a, k):
                    s.bil(s.vec[T, a], s.vec[T, b], 1 if a == b else 0)
        ne = 0
        for S in range(n):
            for T in adj[S]:
                if S < T:
                    for a in range(k):
                        for b in range(k):
                            s.bil(s.vec[S, a], s.vec[T, b], 0)
                    ne += 1
        s.ne = ne
        if dist:
            assert k == 1
            for S in range(n):
                for T in range(S + 1, n):
                    d = [s.xor2(x, y) for x, y in zip(s.vec[S, 0], s.vec[T, 0])]
                    d = [x for x in d if x != -s.T]
                    if s.T in d:
                        continue
                    s.cl.append(d)

    def new(s):
        s.nv += 1
        return s.nv

    def and2(s, a, b):
        T = s.T
        if a == -T or b == -T:
            return -T
        if a == T:
            return b
        if b == T:
            return a
        y = s.new()
        s.cl += [[-y, a], [-y, b], [y, -a, -b]]
        return y

    def xor2(s, a, b):
        T = s.T
        if a == -T:
            return b
        if b == -T:
            return a
        if a == T:
            return -b
        if b == T:
            return -a
        y = s.new()
        s.cl += [[-y, a, b], [-y, -a, -b], [y, -a, b], [y, a, -b]]
        return y

    def xorl(s, lits):
        acc = -s.T
        for x in lits:
            acc = s.xor2(acc, x)
        return acc

    def bil(s, u, w, c):
        terms = [s.and2(a, b) for a, b in zip(u, w)]
        terms = [t for t in terms if t != -s.T]
        acc = s.xorl(terms)
        if acc == s.T:
            if c == 0:
                s.cl.append([])
        elif acc == -s.T:
            if c == 1:
                s.cl.append([])
        else:
            s.cl.append([acc] if c else [-acc])

    def labels(s, mod):
        val = lambda x: (x == s.T) if abs(x) == s.T else (mod[abs(x) - 1] > 0) == (x > 0)   # noqa: E731
        return {T: [sum(1 << t for t, x in enumerate(s.vec[T, j]) if val(x)) for j in range(s.k)]
                for T in range(s.n)}


def calibrations():
    """Controls of the encoders: k = 1 (r = 8 UNSAT, r = 9 SAT, rank 9) and the k = 2 positive control at r = 18."""
    cal, C, L1 = _k1_calibration()
    cal["k2_positive_control"] = _k2_positive_control(C, L1)
    return cal


def _k1_calibration():
    """k = 1: r = 8 UNSAT, r = 9 SAT (rank 9, verified independently)."""
    from pysat.solvers import Solver
    adj = _graph()
    C = max_clique8(adj)
    out = {}
    for r in (8, 9):
        m = PlaneModel(1, r, adj, C, dist=False)
        with Solver(name="cadical195", bootstrap_with=m.cl) as sol:
            ok = sol.solve()
            if ok:
                L = {T: x[0] for T, x in m.labels(sol.get_model()).items()}
                assert all(dot(L[T], L[T]) == 1 for T in range(V))
                assert all(dot(L[S], L[T]) == 0 for S in range(V) for T in adj[S])
                out[f"r{r}"] = dict(sat=True, rank=len(span_basis(list(L.values()))))
                sol1 = L
            else:
                out[f"r{r}"] = dict(sat=False)
    assert out["r8"] == dict(sat=False) and out["r9"] == dict(sat=True, rank=9)
    return out, C, sol1


def _k2_positive_control(C, L1):
    """The k = 2 encoder at r = 18 accepts the direct sum of two copies of a k = 1, r = 9 labelling."""
    from pysat.solvers import Solver
    adj = _graph()
    m = PlaneModel(2, 18, adj, C)

    def emb(x, copy):
        y = 0
        for t in range(9):
            if x >> t & 1:
                c = 2 * t + copy if t < 8 else 16 + copy
                y |= 1 << c
        return y

    L2 = {T: [emb(L1[T], 0), emb(L1[T], 1)] for T in range(V)}
    # independent check of the direct sum: planes nondegenerate (I_2), orthogonal on all in-cap edges
    assert all(dot(L2[T][0], L2[T][0]) == 1 and dot(L2[T][1], L2[T][1]) == 1 and dot(L2[T][0], L2[T][1]) == 0
               for T in range(V))
    assert all(dot(a, b) == 0 for S in range(V) for T in adj[S] for a in L2[S] for b in L2[T])
    assume = []
    for T in range(V):
        for j in range(2):
            for t, lit in enumerate(m.vec[T, j]):
                bit = L2[T][j] >> t & 1
                if abs(lit) == m.T:
                    assert (lit > 0) == bool(bit), "direct sum violates the support rule of the encoder"
                else:
                    assume.append(lit if bit else -lit)
    with Solver(name="cadical195", bootstrap_with=m.cl) as sol:
        ok = sol.solve(assumptions=assume)
    assert ok, "control failed: encoder rejects the r = 18 direct sum"
    return dict(r18_direct_sum_accepted=True, vars=m.nv, clauses=len(m.cl))



# any-type k = 2 encoder, one pattern of clique plane types (from plsat2.py)
_STATE = {}


def _init():
    if not _STATE:
        adj = _graph()
        _STATE["adj"] = adj
        _STATE["C"] = max_clique8(adj)


class AnyTypePlanes:
    def __init__(s, r, pat):
        adj, C = _STATE["adj"], _STATE["C"]
        idx = {c: i for i, c in enumerate(C)}
        s.r = r
        s.nv, s.cl, s.T, s.pat = 1, [[1]], 1, pat
        s.vec, s.tau = {}, {}
        for T in range(V):
            if T in idx:
                i = idx[T]
                s.vec[T, 0] = [s.T if t == 2 * i else -s.T for t in range(r)]
                s.vec[T, 1] = [s.T if t == 2 * i + 1 else -s.T for t in range(r)]
            else:
                al = set(range(16, r))
                for c, i in idx.items():
                    if c not in adj[T]:
                        al |= {2 * i, 2 * i + 1}
                for j in range(2):
                    s.vec[T, j] = [s.new() if t in al else -s.T for t in range(r)]
                s.tau[T] = s.new()
                p, q = s.vec[T, 0], s.vec[T, 1]
                s.eq(s.form(p, p), -s.tau[T])      # tau = 0: plane I_2 (p.p = q.q = 1, p.q = 0)
                s.eq(s.form(q, q), -s.tau[T])      # tau = 1: hyperbolic plane (p.p = q.q = 0, p.q = 1)
                s.eq(s.form(p, q), s.tau[T])
        for S in range(V):
            for T in adj[S]:
                if S < T:
                    for a in range(2):
                        for b in range(2):
                            s.eq(s.form(s.vec[S, a], s.vec[T, b]), -s.T)

    def new(s):
        s.nv += 1
        return s.nv

    def and2(s, a, b):
        T = s.T
        if a == -T or b == -T:
            return -T
        if a == T:
            return b
        if b == T:
            return a
        y = s.new()
        s.cl += [[-y, a], [-y, b], [y, -a, -b]]
        return y

    def xor2(s, a, b):
        T = s.T
        if a == -T:
            return b
        if b == -T:
            return a
        if a == T:
            return -b
        if b == T:
            return -a
        y = s.new()
        s.cl += [[-y, a, b], [-y, -a, -b], [y, -a, b], [y, a, -b]]
        return y

    def form(s, u, w):
        terms = []
        for t in range(s.r):
            if t < 16 and s.pat[t // 2] == "H":
                terms.append(s.and2(u[t], w[t ^ 1]))
            else:
                terms.append(s.and2(u[t], w[t]))
        acc = -s.T
        for x in terms:
            acc = s.xor2(acc, x)
        return acc

    def eq(s, a, b):
        x = s.xor2(a, b)
        if x == s.T:
            s.cl.append([])
        elif x != -s.T:
            s.cl.append([-x])


def _solve_patterns(args):
    from pysat.solvers import Solver
    r, pats = args
    _init()
    out = {}
    for pat in pats:
        f = AnyTypePlanes(r, pat)
        with Solver(name="cadical195", bootstrap_with=f.cl) as sol:
            out[pat] = sol.solve()
    return out


def k2_tasks(r, n_chunks=32):
    """Split the plane-type patterns of the clique into chunks (one CaDiCaL instance per pattern)."""
    assert r in (16, 17)
    pats = ["".join(b) for b in itertools.product("IH", repeat=8)]
    if r == 16:
        pats.remove("H" * 8)     # an alternating window form is not the dot product
    return [(r, pats[i::n_chunks]) for i in range(n_chunks)], len(pats)


def k2_solve(args):
    return _solve_patterns(args)


def k2_collect(r, parts, npats):
    res = {}
    for part in parts:
        res.update(part)
    assert len(res) == npats
    assert sum(res.values()) == 0, f"k = 2 planes found at r = {r}"
    return dict(r=r, patterns=npats, sat=0)


def e8_clique_facts():
    """Clique structure of the in-cap graph: omega = 8, 8640 maximal cliques of size 8 (each is an orthonormal basis)."""
    import networkx as nx
    adj = _graph()
    g = nx.Graph()
    g.add_nodes_from(range(V))
    g.add_edges_from((a, b) for a in range(V) for b in adj[a] if a < b)
    sizes = {}
    for q in nx.find_cliques(g):
        sizes[len(q)] = sizes.get(len(q), 0) + 1
    assert max(sizes) == 8
    return dict(vertices=V, edges=g.number_of_edges(), degree=56, omega=max(sizes), maximal_cliques_by_size=
                {str(k): sizes[k] for k in sorted(sizes)})
