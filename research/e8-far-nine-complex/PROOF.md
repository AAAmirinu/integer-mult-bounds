# Why the swapped unit prices as claimed

**1. #377's profile rule.** #377's `complex_candidate.py` builds its paid histogram as `H[r] += L*T*n` over every block and rank of the certificate's `blocks` field. It adds `2*v*T` children for each nonzero idle rank in `[16,8,32,8,48,8,48,32,16,0]` and `L*R` rank-1 paddings. Its `global_nine.py` asserts that the emitted local `climb`/`center` events reproduce the same profile. Here L = 9, T = 8, v = 120 and R = 783. `code/nine.py` rebuilds this profile from Sussman's certificate and checks equality with #377's `GLOBAL-REVIEW.json` for every rank.

**2. What the certificate enters.** Outside the pooled local histogram, #377's construction reads the following from the local word:
- h = 9, v = 120, R = 783 and cst = 72 (stock, banks, deficit);
- the ports (data routes ρ_{s,q}, U_q, the terminal X_q);
- the start/final frames and retained totals (data levels and endpoint adapters);
- the invocation theorem, which depends on the operator and the dirty-gate block structure.

#378's certificate keeps all of these, and `cxop.py` checks that the full rational operator on all 1,023 registers and the 8 retained totals are identical. The idle advances, banks, padding, bridges, exchange and cover correction δ(g) depend only on (h, v, R, k, L, T, m) and on the ports, so they are unchanged.

**3. Same stock and deficit.** W = 8vT + LR = 14,727 and the deficit is m·W − mass = T(2kv − L·cst) = 2,496. Both are unchanged, because the local rank mass is N-determined: its per-invocation total is 9,039 on both certificates. The largest child is still 48, so the halving degree is 2, and #377's row and induction numbers (49B, 15,445) are unchanged.

**4. Price.** b is the largest 10⁻¹⁸ grid point below the exact moment root. Both rational engines of PR #315 compute it, with the 10⁻¹⁶ fallback; the next grid point is excluded. Applied to #377's own profile, the same procedure returns #377's b, 999240641319551/10¹⁸, exactly.

**5. Assembly.** PR #315's `outer.assembly`, with the bit c = 251726760077483/(2.5·10¹⁷) (#382) and this b, gives κ = 998634656132003/10¹⁸. It is complex-bound, all 47 strict constraints are positive, and κ + 10⁻¹⁸ is rejected. With #377's b the same call returns #382's κ = 998243154231047/10¹⁸.

**Lean.** Only the five-stage B₂ unit theorem of this certificate is kernel-checked (`wht_main_block_B2Ge8FRx`, exponent 1 − 8766835/10¹⁰, `lean/LEAN-B2-E8FR.txt`); the nine-stage pricing above has no Lean proof.

**Open.** The finite checks that #377 ran on Sussman's specific gates are not re-run for the new gates; the README lists them.
