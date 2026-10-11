"""The p = 3 toy: the one place where a read-discipline change beats gx's E2 (all targets at frame 0 at the scatter).

Instance: inputs/gcert1-p3-cone-R16.json (paired cube p = 3, h = 6, v = 8, R = 16, cst = 18), accepted by gx.check1.
Its 8 ports span W of dimension 4, and the window form restricted to W is DEGENERATE: W^perp (dim 2) lies in W.
Modified rule E2': the scatter is done in cuts. At a cut, all targets stand at ONE common frame g contained in every
target's final q^perp (so g <= W^perp), and copying total k costs d(f_k, g) = dim f + dim g - 2 dim(f cap g).
Exact checks (all F_2 / integer): every register chain is nested, equal frames at every gate, targets stay inside
q^perp and avoid q, the block-mass identity, the scalar half (gates and coefficients unchanged), and the exhaustive
optimum over all chains of cut frames. Control: a cut frame outside the radical is rejected.
"""
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "gx"))
sys.path.insert(0, str(ROOT / "checks"))
import gx  # noqa: E402
from certs import load  # noqa: E402
from f2 import dot, rank  # noqa: E402


def span(gens):
    b = []
    for u in gens:
        for x in b:
            if u ^ x < u:
                u ^= x
        if u:
            b.append(u)
            b.sort(reverse=True)
    return tuple(b)


def inside(a, b):
    return all(gx.reduce(u, b) == 0 for u in a)


def run():
    c = load(ROOT / "inputs" / "gcert1-p3-cone-R16.json")
    gx.check1(c)
    h, v, R = c["h"], c["v"], c["R"]
    nreg = 2 * v + R
    ports = c["ports"]
    fr = [tuple(f) for f in c["frames"]]
    assert not c["ext"]

    def d(f, g):
        both = span([x for x in range(1, 1 << h) if gx.reduce(x, f) == 0 and gx.reduce(x, g) == 0])
        return len(f) + len(g) - 2 * len(both)

    # geometry of the ports: W = span, W^perp, radical
    W = span(ports)
    perpW = [x for x in range(1 << h) if all(dot(x, q) == 0 for q in ports)]
    rad_nonzero = sorted(x for x in perpW if x)
    assert len(W) == 4 and len(perpW) == 4 and all(gx.reduce(x, W) == 0 for x in perpW)   # W^perp lies in W: radical
    L = 0b111100
    assert L in rad_nonzero and all(dot(L, q) == 0 for q in ports)

    cur = [fr[s] for s in c["start"]]
    mass = 0

    def climb(r, f):
        nonlocal mass
        if cur[r] != f:
            assert inside(cur[r], f), ("not nested", r)
            mass += len(f) - len(cur[r])
            cur[r] = f

    for g in c["A"]:
        regs, _, _ = gx.gate_regs(g)
        for r in regs:
            climb(r, fr[g[1]])
    tot = {k: (s, fr[f]) for k, s, f in c["ret"]}
    for k, (s, f) in tot.items():
        assert cur[s] == f
    assert all(cur[v + t] == () for t in range(v))
    old_cst = sum(len(f) for _, f in tot.values())
    assert old_cst == c["cst"] == 18
    cut1 = [k for k in tot if gx.reduce(L, tot[k][1]) != 0]     # totals not containing l: read at g = 0
    cut2 = [k for k in tot if gx.reduce(L, tot[k][1]) == 0]     # totals containing l: read at g = <l>
    cst = sum(d(tot[k][1], ()) for k in cut1)
    for t in range(v):
        climb(v + t, span([L]))                                 # the targets climb to the common frame l
    cst += sum(d(tot[k][1], span([L])) for k in cut2)
    for g in c["B"]:
        regs, _, _ = gx.gate_regs(g)
        f = span(list(fr[g[1]]) + [L])
        for r in regs:
            climb(r, f)
    for r in range(nreg):
        fin = fr[c["final"][r]]
        climb(r, span(list(fin) + ([L] if r >= v else [])) if r < v or r >= 2 * v else fin)
    for t in range(v):
        assert inside(cur[v + t], fr[c["final"][v + t]]) and gx.reduce(ports[t], cur[v + t]) != 0
    assert mass == R * h + 2 * v * (h - 1), mass
    gx.scal(c)                                                   # scalar half: gates and coefficients unchanged

    # exhaustive optimum over all chains of cut frames inside W^perp (targets only climb between cuts)
    subs = [()] + [span([x]) for x in rad_nonzero] + [span(rad_nonzero)]
    subs = [s for i, s in enumerate(subs) if s not in subs[:i]]
    def leq(a, b):
        return inside(a, b)
    best, best_chain = None, None
    old_format = None
    for n in range(1, len(subs) + 1):
        for chain in itertools.combinations(subs, n):
            if not all(leq(a, b) or leq(b, a) for a in chain for b in chain):
                continue
            total = sum(min(d(f, g) for g in chain) for _, f in tot.values())
            if chain == ((),):
                old_format = total
            if best is None or total < best:
                best, best_chain = total, chain
    assert old_format == 18 and best == 16 == cst, (old_format, best, cst)

    # control: a common frame not inside W^perp would put a target outside q^perp
    not_rad = [x for x in range(1, 1 << h) if x not in rad_nonzero]
    ctrl = all(any(dot(x, q) for q in ports) for x in not_rad)
    assert ctrl, "control failed"
    # Thm C bound for this instance (degenerate span): lower bound of the pairing ranks
    lb = sum(len(f) - 1 for _, f in tot.values())
    # on the nondegenerate families the gain is zero: W^perp = 0 forces g = 0 (window_rank = h in certs.py)
    return dict(h=h, v=v, R=R, old_cst=old_cst, new_cst=cst, optimum_over_cut_chains=best, old_format_optimum=old_format,
                cut1=sorted(cut1), cut2=sorted(cut2), line=bin(L), radical_nonzero=[bin(x) for x in rad_nonzero],
                port_span_dim=len(W), moves_old=R * h + 2 * v * (h - 1) + old_cst, moves_new=mass + cst,
                thmC_per_total_bound=lb, D_old=4 * v - 5 * old_cst, D_new=4 * v - 5 * cst,
                cut_outside_radical_rejected=ctrl)
