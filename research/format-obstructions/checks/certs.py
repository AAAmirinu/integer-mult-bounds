"""Theorems A, B, C on gcert/1 certificates (one invocation, window F_2^h, standard dot product).

For a gcert/1 file:
  * gx.check1 (Sussman's reference checker, label half + exact scalar half) must accept it;
  * Thm A: replay the gates and carry, for every register, the set of x-sources whose content entered it along
    drop-free paths ("taint"; the scatter cut, a drop to frame 0, passes no taint). At EVERY gate each newly
    received source port must lie in the gate frame (exact F_2 reduction);
  * Cor A1: the lossless set of every target y_S (its final taint) is orthogonal to q_S, and does not contain S;
  * Thm B data: N(S) = span{q_T : T in taint(y_S)} and its rank; every y reads every total (co-read);
  * Thm C: for every retained total, A_k = span of the ports of its taint; copy price paid = dim f_k; lower bound =
    rank of the pairing A_k x span(readers).
"""
import gzip
import json
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "gx"))
sys.path.insert(0, str(ROOT / "checks"))
import gx  # noqa: E402  (Jacob Sussman's reference checker, vendored unchanged)
from f2 import dot, pairing_rank, rank  # noqa: E402


def load(path):
    path = str(path)
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as f:
        return json.load(f)


def replay(c, gate_check=True):
    """Taint replay (Thm A). Returns (taint, tot_taint, tot_frame, stats)."""
    h, v, R = c["h"], c["v"], c["R"]
    nreg = 2 * v + R
    ports = c["ports"]
    fr = [tuple(f) for f in c["frames"]]
    taint = [(1 << r) if r < v else 0 for r in range(nreg)]
    stats = dict(gate_checks=0, violations=0, pairs=0)

    def portlist(bits):
        while bits:
            low = bits & -bits
            yield ports[low.bit_length() - 1]
            bits ^= low

    def run(gates):
        for g in gates:
            regs, pairs, _ = gx.gate_regs(g)
            for t, s, co in pairs:
                stats["pairs"] += 1
                new = taint[s] & ~taint[t]
                if gate_check and new:
                    for q in portlist(new):
                        stats["gate_checks"] += 1
                        if gx.reduce(q, fr[g[1]]) != 0:
                            stats["violations"] += 1
                taint[t] |= taint[s]

    run(c["A"])
    ret = sorted(c["ret"])
    tot_taint = {k: taint[s] for k, s, f in ret}
    tot_frame = {k: f for k, s, f in ret}
    run(c["B"])
    return taint, tot_taint, tot_frame, stats


def analyse(path, gate_check=True):
    c = load(path)
    t0 = time.monotonic()
    gx.check1(c, scalar=True)
    t_check = time.monotonic() - t0
    h, v, R = c["h"], c["v"], c["R"]
    ports = c["ports"]
    fr = [tuple(f) for f in c["frames"]]
    t0 = time.monotonic()
    taint, tot_taint, tot_frame, stats = replay(c, gate_check)
    t_replay = time.monotonic() - t0
    coread_all = True
    for t in range(v):
        ks = {k for k, co in gx.scat_row(c, t) if co != 0}
        if ks != set(tot_taint):
            coread_all = False

    def portlist(bits):
        out = []
        while bits:
            low = bits & -bits
            out.append(ports[low.bit_length() - 1])
            bits ^= low
        return out

    perp_ok, self_hit = True, False
    ranks, degs = [], []
    for S in range(v):
        tb = taint[v + S]
        self_hit |= bool(tb >> S & 1)
        Ts = [T for T in range(v) if tb >> T & 1]
        degs.append(len(Ts))
        perp_ok &= all(dot(ports[T], ports[S]) == 0 for T in Ts)
        ranks.append(rank([ports[T] for T in Ts]))
    lb = paid = 0
    for k in sorted(tot_taint):
        A = portlist(tot_taint[k])
        lb += pairing_rank(A, ports)
        paid += len(fr[tot_frame[k]])
    res = dict(file=Path(str(path)).name, h=h, v=v, R=R, cst=c["cst"], check1="PASS",
               thmA_gate_checks=stats["gate_checks"], thmA_violations=stats["violations"],
               incap_perp=perp_ok, self_lossless=self_hit, incap_deg=[min(degs), max(degs)],
               N_rank=[min(ranks), max(ranks)], coread_all=coread_all, window_rank=rank(ports),
               copy_lb=lb, copy_paid=paid, seconds=dict(check1=round(t_check, 1), replay=round(t_replay, 1)))
    return res, c, taint


def controls(c, taint):
    """Negative controls on the small certificate c (p = 3)."""
    import copy
    v = c["v"]
    ports = c["ports"]
    out = {}
    # (1) cyclically shifted labels: the lossless sets are no longer orthogonal -> the Cor A1 test fires
    sh = ports[1:] + ports[:1]
    bad = sum(1 for S in range(v) for T in range(v)
              if taint[v + S] >> T & 1 and dot(sh[T], sh[S]))
    out["shifted_labels_nonorthogonal_pairs"] = bad
    assert bad > 0, "control failed: shifted labels still orthogonal"
    # (2) a corrupted port that still passes E0 (odd weight, distinct): gx.check1 rejects it at E1 and the taint replay
    #     reports source ports outside the gate frame
    used = set(ports)
    mask = next(m for m in range(3, 1 << c["h"]) if not bin(m).count("1") & 1 and (ports[0] ^ m) not in used
                and (ports[0] ^ m) > 0)
    c2 = copy.deepcopy(c)
    c2["ports"][0] ^= mask
    try:
        gx.check1(c2, scalar=True)
        raise AssertionError("control failed: gx.check1 accepted a corrupted port")
    except AssertionError as e:
        if "control failed" in str(e):
            raise
        out["corrupted_port_check1_rejects"] = str(e).split(":")[0]
    _, _, _, st = replay(c2, True)
    out["corrupted_port_replay_violations"] = st["violations"]
    assert st["violations"] > 0, "control failed: replay saw no violation for a corrupted port"
    return out


FILES = {"p3": "gcert1-p3-cone-R16.json", "p10": "gcert1-p10-anneal-mw-flow.json.gz", "p11": "gcert1-p11-pr193.json.gz"}


def stage(name):
    """One certificate: gx.check1, Thm A/B/C data, and (for the small one) the negative controls."""
    res, c, taint = analyse(ROOT / "inputs" / FILES[name], gate_check=True)
    if name == "p3":
        res["controls"] = controls(c, taint)
    return res
