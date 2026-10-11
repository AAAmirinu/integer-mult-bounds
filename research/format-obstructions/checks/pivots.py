"""Section 7 of PROOF.md: the 2K block pivots of a shared-helper B_K layout (F_2 windows, gcert/1 programs).

thm_P (exact).  A helper set that runs the SAME gcert/1 program on the SAME slots in every stage: a slot never drops,
so after stage j its frame contains iota_j(q_T) for every source T it touched (Thm A); when it writes y_S in stage
j' > j its frame lies inside iota_j'(q_S)^perp. With K = iota_j^T iota_j' (h x h over F_2) this gives
q_T^T K q_S = 0 for every slot-carried pair (T in taint(z), S in writes(z)). The condition is linear in K; we compute
the rank of {q_T (x) q_S}. Rank h^2 means K = 0, i.e. the stage windows are pairwise orthogonal and m >= s*h.

copy_count (exact, over ALL odd a, b in F_2^h).  Model of ONE overlap w between the helper windows of two stages,
w = iota_{j-1}(e) = iota_j(e') with e.e = e'.e' = 1: a retained total whose frame is not inside e^perp carries w into
stage j; in stage j such a total pays one extra copy rank unless e' lies in its frame. Hence the forced extra copy
rank per overlap is >= (#totals) - (max #totals inside some e^perp) - (max #frames containing some e').

overlap_scan (exact on the candidates).  The same model on the helper side: slots whose last frame is not inside e^perp
carry w; their forward closure through the gates contaminates registers, and a contaminated target y_S needs
e'.q_S = 0. Candidates: the h unit vectors and the 1,140 weight-3 vectors (h = 20), not all directions.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "gx"))
sys.path.insert(0, str(ROOT / "checks"))
import gx  # noqa: E402
from certs import load  # noqa: E402
from f2 import dot, span_basis  # noqa: E402


def _taint_and_writes(c):
    h, v, R = c["h"], c["v"], c["R"]
    nreg = 2 * v + R
    taint = [(1 << r) if r < v else 0 for r in range(nreg)]
    writes = {}
    for g in c["A"] + c["B"]:
        regs, pairs, _ = gx.gate_regs(g)
        for t, s, co in pairs:
            taint[t] |= taint[s]
            if 2 * v <= s and v <= t < 2 * v:
                writes.setdefault(s, set()).add(t - v)
    return taint, writes


def thm_P(path):
    c = load(path)
    gx.check1(c, scalar=False)
    h, v, R = c["h"], c["v"], c["R"]
    ports = c["ports"]
    taint, writes = _taint_and_writes(c)

    def kron(a, b):
        out = 0
        for i in range(h):
            if a >> i & 1:
                out |= b << (h * i)
        return out

    def rank_of(only_orth, cap):
        basis, used = [], 0
        for z in sorted(writes):
            Ts = [T for T in range(v) if taint[z] >> T & 1]
            for S in writes[z]:
                for T in Ts:
                    if only_orth and dot(ports[T], ports[S]):
                        continue
                    vec = kron(ports[T], ports[S])
                    used += 1
                    for b_ in basis:
                        if vec ^ b_ < vec:
                            vec ^= b_
                    if vec:
                        basis.append(vec)
                        basis.sort(reverse=True)
                        if len(basis) == cap:
                            return len(basis), used
        return len(basis), used

    # (a) pairs with q_T . q_S = 0 only: their tensors lie in the trace hyperplane (tr M = sum_i M_ii = q_T . q_S)
    r_orth, used_orth = rank_of(True, h * h)
    # (b) all slot-carried pairs
    r_all, used_all = rank_of(False, h * h)
    assert r_orth == h * h - 1 and r_all == h * h, (r_orth, r_all)       # K = lambda * I from (a); K = 0 from (b)
    # cross-cube slots (descriptive; paired-cube ports only)
    cube = [frozenset(i // 2 for i in range(h) if q >> i & 1) for q in ports]
    written = sorted({S for z in writes for S in writes[z]})
    written_rank = len(span_basis([ports[S] for S in written]))
    assert written_rank == h                 # the slot-written targets' ports span the window
    cross = sum(1 for z in range(2 * v, 2 * v + R) if len({cube[T] for T in range(v) if taint[z] >> T & 1}) > 1)
    return dict(file=Path(str(path)).name, h=h, slots=R, writer_slots=len(writes),
                rank_orthogonal_pairs_only=r_orth, rank_all_carried_pairs=r_all, h_squared=h * h,
                K_solution_dim=h * h - r_all, slot_written_targets_port_rank=written_rank, K_zero_gives_m_ge="s*h, under (P1)-(P2)", cross_cube_slots=cross)


def copy_count(path):
    c = load(path)
    h = c["h"]
    fr = [tuple(f) for f in c["frames"]]
    F = [fr[f] for k, s, f in sorted(c["ret"])]
    best_nc = best_in = 0
    for a in range(1, 1 << h):
        if not (bin(a).count("1") & 1):
            continue
        nc = sum(1 for f in F if all(not dot(b, a) for b in f))
        ins = sum(1 for f in F if gx.reduce(a, f) == 0)
        best_nc = max(best_nc, nc)
        best_in = max(best_in, ins)
    return dict(totals=len(F), frame_dims=sorted({len(f) for f in F}), max_noncarrier_totals=best_nc,
                max_totals_containing_b=best_in, forced_extra_copy_per_overlap=len(F) - best_nc - best_in)


def overlap_scan(path):
    c = load(path)
    h, v, R = c["h"], c["v"], c["R"]
    nreg = 2 * v + R
    ports = c["ports"]
    fr = [tuple(f) for f in c["frames"]]
    gates = [("A", g) for g in c["A"]] + [("B", g) for g in c["B"]]
    regsets = [gx.gate_regs(g)[0] for _, g in gates]
    last = {}
    for i, (_, g) in enumerate(gates):
        for r in regsets[i]:
            if r >= 2 * v:
                last[r] = g[1]
    slots = sorted(last)

    def carriers(e):
        return {z for z in slots if any(dot(b, e) for b in fr[last[z]])}

    def closure(C):
        bad = set(C)
        for i, (_, g) in enumerate(gates):
            rs = regsets[i]
            if any(r in bad for r in rs):
                bad.update(rs)
        return bad

    odd = [e for e in range(1, 1 << h) if bin(e).count("1") & 1]
    cand = [1 << i for i in range(h)] + [e for e in odd if bin(e).count("1") == 3][:2000]
    recs = []
    for e in cand:
        C = carriers(e)
        bad = closure(C)
        ys = [r - v for r in bad if v <= r < 2 * v]
        recs.append((len(C), len(bad), len(ys), len(span_basis([ports[S] for S in ys]))))
    return dict(h=h, slots=R, slots_with_gates=len(slots), registers=nreg, candidates=len(cand),
                min_carriers=min(r[0] for r in recs), min_contaminated_registers=min(r[1] for r in recs),
                min_contaminated_targets=min(r[2] for r in recs), min_port_rank_of_contaminated=min(r[3] for r in recs))
