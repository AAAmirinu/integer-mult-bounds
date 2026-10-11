"""Pricing context for the pivots (PROOF.md section 7) and for non-nested chains (section 8), with the pinned pricer.

Pricer: inputs/pricing/cost.py (solve_moment), PR #346 (Louis Harrison) from PR #310 (Dylan Crow, utcorvusvolat-dotcom),
vendored unchanged. Input: the normalised five-stage histogram of PR #325's p = 10 bit word (hist_p10b.json: m = 100,
W = 131,760 = 12 * 10,980, deficit D = 24,480; every count is 12 x a per-invocation count) and its pinned bit root
385138454781521/(5 * 10^17).

 * baseline: the pricer reproduces the pinned root.
 * pivot-free variants (m = 96 = 1 + 5 (h - 1)): each helper wire loses 4 levels (4 blocks of rank r -> r - 1), the
   pair-1 end idle block goes 2h+2 -> 2h-2 and the pair-2 end idle block of rank 4 disappears. Four ways of choosing
   which helper blocks shrink bracket the gain. 'forced copies': 40 extra copy rank per unit (4 overlaps x 10, see
   pivots.copy_count), modelled as 40 x 12 blocks of rank 18 becoming rank 19.
 * non-nested chain (section 8): one rank-1 copy in each of the five stages, per 12-normalised unit, is +60 blocks of rank 1 (5 stages
   x 12); a rank-1 register descent is a single non-nested step of frame-lemma rank d = 2, +60 blocks of rank 2.
These are pricer-model outputs for the p = 10 bit word, not theorems.
"""
import collections
import importlib.util
import json
import sys
from pathlib import Path

from mpmath import mp, mpf

ROOT = Path(__file__).resolve().parent.parent


def run():
    spec = importlib.util.spec_from_file_location("cost", ROOT / "inputs" / "pricing" / "cost.py")
    C = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("cost", C)
    spec.loader.exec_module(C)
    mp.dps = 40
    d = json.load(open(ROOT / "inputs" / "pricing" / "hist_p10b.json"))
    H0 = collections.Counter({int(k): v for k, v in d["histogram"].items()})
    W = mpf(d["W"])
    m0 = d["m"]
    v12 = 960 * 12
    Rs = d["W"] - 4 * v12
    mass0 = sum(r * n for r, n in H0.items())
    D0 = d["W"] * m0 - mass0
    assert (m0, d["W"], D0, d["deficit"]) == (100, 131760, 24480, 24480)
    a0 = C.solve_moment(H0, W, m0)
    num, den = d["bit_root"].split("/")
    pinned = mpf(int(num)) / mpf(int(den))
    # the pinned value is the certified grid point (step 1/den = 2e-18) at or just below the root
    assert 0 <= a0 - pinned < mpf(1) / int(den), (a0, pinned)
    out = dict(m=m0, W=d["W"], D=D0, root=format(float(a0), ".12e"), pinned_root=format(float(pinned), ".12e"))

    def variant(shrink, extra_copy=0):
        H = collections.Counter(H0)
        H[42] -= 2 * v12
        H[38] += 2 * v12
        H[4] -= 2 * v12
        for r, cnt in shrink:
            H[r] -= cnt
            if r > 1:
                H[r - 1] += cnt
        assert all(c >= 0 for c in H.values())
        if extra_copy:
            H[18] -= extra_copy
            H[19] += extra_copy
        m = 96
        return W * m - sum(r * n for r, n in H.items()), C.solve_moment(H, W, m)

    def spread(ranks):
        need = 4 * Rs
        res = []
        for r in ranks:
            take = min(need, H0[r] - (2 * v12 if r in (4,) else 0))
            res.append((r, take))
            need -= take
            if not need:
                break
        assert need == 0
        return res

    rows = {}
    for name, shrink in (("rank-1 blocks removed", [(1, 4 * Rs)]), ("blocks 2->1", [(2, 4 * Rs)]),
                         ("mid blocks shortened", spread([3, 4, 5, 6, 7, 8, 9, 10, 12, 14])),
                         ("largest blocks shortened", spread([19, 18, 17, 16, 14, 12, 11, 10]))):
        D, a = variant(shrink)
        D2, a2 = variant(shrink, extra_copy=40 * 12)
        assert D == D0
        rows[name] = dict(zero_cost_percent=format(float((a / a0 - 1) * 100), "+.2f"),
                          with_40_forced_copy_percent=format(float((a2 / a0 - 1) * 100), "+.2f"))
    out["pivot_free_m96"] = rows

    def delta(H):
        return format(float((C.solve_moment(H, W, m0) / a0 - 1) * 100), "+.4f")
    Hc = collections.Counter(H0)
    Hc[1] += 60
    Hd = collections.Counter(H0)
    Hd[2] += 60
    out["per_stage_rank1_copy_percent"] = delta(Hc)
    out["per_stage_rank1_register_descent_percent"] = delta(Hd)
    return out
