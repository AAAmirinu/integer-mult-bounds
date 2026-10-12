#!/usr/bin/env python3
"""Loss-chain decomposition of published supplier profiles (note 4).

For a paid profile {rank r: count n} with block size m, live stock W and deficit D = mW - sum r n,
the supplier saving a is the root of the moment equation
    sum_r (r n_r / (m W)) (m/r)^a = 1            (without the 1e-16 bad-class term, which only lowers a)
With p_r = r n_r/(mW), delta = D/(mW) and L_ent = sum_r p_r ln(m/r) / (1 - delta) = ln m - E[ln r],
    a ~= delta / L_ent = (1/m) (D/W) / L_ent      (first order; x^a >= 1 + a ln x makes it an upper bound
                                                    up to the 1/(1-delta) normalisation)
and kappa ~= a/(1+a) through the outer assembly.

Usage: python loss_chain.py REPO_ROOT
Two rows are read from main (the selected complex supplier and the best merged bit supplier); the
historical rows are histograms copied from the packages named next to them.
"""
import json, sys
from math import log
from fractions import Fraction as F
from pathlib import Path

HISTORICAL = {
    # research/community-pr279-audit/certificate.json (merged gen4, kappa 7.2357e-4)
    'gen4 bit (#276 + #279)': dict(m=120, W=256607, H={1:2402880,2:1133460,3:598080,4:226680,5:159360,6:85020,7:69180,8:39720,9:25980,10:63420,11:25860,12:65160,13:28020,14:86580,15:4500,16:55920,17:16680,18:48000,19:10380,20:52800,21:402720,22:41040,23:42240,46:42240,50:42240}),
    # PR #501 head 1dc0564, research/r489-pooled-retimed-complex/EXPECTED.json
    'complex #501 (R560, 9 stages)': dict(m=73, W=7680, H={1:172056,2:19008,3:42032,4:6048,5:22496,6:6624,7:1800,8:4120}, published=F(1345325487149526878087, 10**24)),
    'bit #493 (R489, 11 stages)': dict(m=78, W=9600, H={1:105600,2:130560,4:19680,6:14400,7:7680,8:1584,48:2,56:2628}, published=F(391360506745414227149, 25*10**22)),
}

def from_main(root):
    rows = {}
    cx = json.loads((root / 'research/complex-571-hpeq5/data/EXPECTED.json').read_text())['global']
    rows['complex, selected main (#596; R504 lineage)'] = dict(
        m=73, W=cx['live'], H={int(k): v for k, v in cx['global_profile'].items()}, published=F(cx['complex_lower']),
        deficit=cx['deficit'])
    bt = json.loads((root / 'research/e8-bit-p111-tuned/tune/EXPECTED.json').read_text())['nine']
    rows['bit, best merged (#589; p111 R439, 9 stages)'] = dict(
        m=64, W=bt['bit']['live'], H={int(k): v for k, v in bt['profile'].items()}, published=F(bt['bit_lower']),
        rank_mass=bt['bit']['rank_mass'])
    return rows

def solve(H, m, W):
    f = lambda a: sum(r*n/(m*W)*(m/r)**a for r, n in H.items()) - 1
    lo, hi = 0.0, 0.05
    for _ in range(200):
        mid = (lo+hi)/2
        (lo, hi) = (mid, hi) if f(mid) < 0 else (lo, mid)
    return lo

def analyse(name, m, W, H, published=None, deficit=None, rank_mass=None):
    mass = sum(r*n for r, n in H.items()); D = m*W - mass
    if deficit is not None: assert D == deficit, (name, D, deficit)
    if rank_mass is not None: assert mass == rank_mass, (name, mass, rank_mass)
    delta = D/(m*W)
    Elnr = sum(r*n*log(r) for r, n in H.items())/mass
    Lent = log(m) - Elnr
    a = solve(H, m, W); first = delta/Lent
    if published is not None:
        rel = abs(a/float(published) - 1)
        assert rel < 1e-8, (name, a, float(published))
    print(f"{name:46s} 1/m={1/m:.4e}  D/W={D/W:.4f}  L_ent={Lent:.3f} (ln m {log(m):.3f} - E ln r {Elnr:.3f})"
          f"  delta/L_ent={first:.6e}  root a={a:.6e} (x{a/first:.5f})  a/(1+a)={a/(1+a):.6e}"
          + (f"  [published {float(published):.6e}]" if published is not None else ''))
    return dict(m=m, DW=D/W, Lent=Lent, a=a)

if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
    rows = dict(HISTORICAL); rows.update(from_main(root))
    out = {k: analyse(k, **v) for k, v in rows.items()}
    print("PASS every root matches its published value to < 1e-8 relative; deficits and rank masses match")
    a0, a1 = out['gen4 bit (#276 + #279)'], out['complex, selected main (#596; R504 lineage)']
    print("factor ratios gen4 bit -> selected complex: 1/m x%.3f, D/W x%.3f, 1/L_ent x%.3f, root x%.3f"
          % (a0['m']/a1['m'], a1['DW']/a0['DW'], a0['Lent']/a1['Lent'], a1['a']/a0['a']))
