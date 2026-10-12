"""Exact flow upper bounds for #109's labelled motif networks read as undirected multiple-unicast instances.

Instance: the scalar exchange network of `03-motifs.tex` (every role demanded: X_a -> Y_a, Y_a -> X_a,
scratch -> scratch), every wire edge subdivided into (orthogonal-residual rank) unit edges, zero-rank
interior edges contracted, one extra unit pendant edge at every source and sink.
Coding rate 1 (the scalar network itself, one symbol per unit edge).
Flow bound (LP dual with unit lengths): lambda <= |E| / sum_w dist(w), and
dist(w) >= d(src label, sink label) + 2, d(A,B) = dim A + dim B - 2 dim(A cap B) (subspace metric),
which is m for every role (U_a vs U_a^perp, 0 vs F, 0 vs F).
For the bit network the frames are rational matrices M_v and the metric is rank(M - M'); the paper proves
M_sink(rho w) - M_source(w) = I_m, so again dist >= m.
"""
from fractions import Fraction as F
from math import comb

h = 100; v = comb(h, 3); N = v**3; m = h**3; I = 3 * v**2
PAPER_ETA = {"bit": F(339, 22587335000000), "complex": F(73, 19906842167500)}
for name, z, c in (("bit", 3 * comb(h - 3, 2), h), ("complex", comb(h - 3, 3) + 3 * (h - 3), h + 1)):
    W = 2 * N + I * (v * z + c)
    L = I * c * h
    # bit: rational-rank ledger W m - N + 2L (Prop. bit-motif-interface; metric = rank distance of the
    # frame matrices, endpoint difference I_m on every role); complex: W m - 2N + 2L (Prop. complex-motif-interface;
    # metric = subspace distance of the binary labels, = m on every role)
    s = W * m - (N if name == "bit" else 2 * N) + 2 * L
    eta = F(W * m - s, W * m)
    lam = F(s + 2 * W, W * m + 2 * W)
    assert eta == PAPER_ETA[name] and lam < 1, name
    print(f"{name}: W={W} s={s} eta={eta} (paper: bit 339/22587335000000, complex 73/19906842167500)")
    print(f"   lambda_flow <= {float(lam):.18f}  (1 - lambda = {float(1 - lam):.3e});  coding = 1")

print("PASS paper eta reproduced exactly; flow bound < 1 on both motif networks")

# [conjecture, not checked] community ledgers per forward invocation (form N = R*h + 2v(h-1) + cst; naive (R+2v)h)
for name, R, h_, v_, cst in (("gcert1-p11-pr193 (h=22)", 9412, 22, 1320, 440),
                             ("R560 E8 word (m=9)", 560, 9, 120, 72),
                             ("PR425 R680 word (m=9)", 680, 9, 120, 72)):
    naive = (R + 2 * v_) * h_
    s_ = R * h_ + 2 * v_ * (h_ - 1) + cst
    print(f"{name}: s={s_} naive={naive} saving={naive - s_} (=2v-cst={2*v_-cst}) eta={float(F(naive - s_, naive)):.5f}"
          f"  -> implied gap ratio {float(F(naive, s_)):.5f} if routed as an exchange with d=m per role")
