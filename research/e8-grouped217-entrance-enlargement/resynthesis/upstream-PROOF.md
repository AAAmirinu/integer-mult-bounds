# Why the re-synthesised word computes #401's operator, and what is re-opened

Notation: x (120 sources), h (781 helpers), y (120 targets). The main word is gcert/1 (A, scatter, B).

**1. #401's word.** `entrance.py` registers #401's 26 entrance frames, starts each of the 119 pivots at its frame, and prepends the 240 unit shears h_d += c·h_p. The result equals #401's frozen candidate byte for byte (sha256). `resynth401.py` checks M₄₀₁ = M₃₉₈ · diag(I_X, I_Y, S) on all 1,021 columns, and that all 119 gauged response columns are zero.

**2. Tokens and windows.** For every register r, a window is a maximal position interval in which r has a fixed version and frame. A gate inserted in that window that reads r adds r's value at that version. It touches r only at a frame r already holds, so r's walk is unchanged.

**3. A re-synthesis.** Let y_i's B-phase feeds be replaced by deliveries y_i += q_k·t_k, with each token t_k read inside its window at its frame.
- When t_k = y_j (a restore), a setup y_i −= q_k·y_j is placed at the start of B, at frame 0, where y_j still holds its dirty value plus its scatter part.
- Restore minus setup then delivers exactly y_j's B-phase prefix. This requires y_j's y-row to be exactly e_j at the read, which is checked.
- Every original feed gate of y_i becomes a source-touching empty marker, which is #398's form.
- The new value of y_i equals the old one exactly, on every input column, when Σ q_k·t_k matches y_i's B-phase prefix in the clean x-part and in every helper-dirt column.
- Our discovery solves only the x-part together with the 119 gauged dirt columns (#401's K_p = 0). It accepts a design only if the replay shows full equality.

Here the full raw operator of the re-synthesised word is identical to #401's on every register and column. So M, K, the gauged zero columns and the retained totals are all unchanged.

**4. Frames and price.** The frames of y_i's deliveries form a nested chain 0 ⊂ 892 ⊂ F_i, where F_i is y_i's unchanged final frame. Every delivery is at a common exact frame label (validate). The paid local events are y_i's climbs (6, 2) instead of (3, 5), and nothing else changes: helper walks, centres, banks and residuals are untouched. The profile change is 72 × {2:+2, 3:−2, 5:−2, 6:+2}. Rank mass is unchanged, so the deficit stays 2,496.

**5. Bracket.** We emit with #390's dirty-preconditioned bracket:
1. Precancel y −= B·A⁻¹·h and prewhiten h ← A⁻¹h at the common old frame. A includes #401's entrance shears.
2. Run the main word.
3. Repair N_r·x at FULL.

`validate` replays all 1,021 live columns in both orientations: (x, h, y) → (x, h, y + x) forward and (x − y, h, y) backward, with private work erased.

On #401's unmodified word this reproduces #401's 24-digit coarse root and κ exactly. The bracket swap therefore does not change the profile.

Because the full raw operator is unchanged, #401's own bracket (complete old response K, main, complete cleanup, two-sided R₀⁻¹/L⁻¹ entrance adapters) also realises the invocation for our word unchanged. Its endpoint premise is a property of that operator and of the helper subword, and both are untouched.

**6. Price.** The κ uses #401's profile formula: 72 local invocations, idle children, 482 rank-1 and one rank-10 padding per stage, live 14,412 and m = 73. Both PR #315 engines are used with the 10⁻¹⁶ fallback, and #392's six bootstrap levels with 47 strict constraints, rejecting the next grid point. The bit side is #401's pinned coarse bound c ≈ 1.021539e-3 > b, so the complex side binds.

## Re-opened

- Gaussian-phase compilation of the changed target edges (0→892, 892→179 and 892→222). The general Clifford compiler admits any nested pair, but #401's receipts do not cover these edges.
- The scalar invoice: 10 helper→target deliveries, 2 target restores and 2 setups per invocation, against #401's reserve (row coefficient 15,445 < 20,161).

## Inherited, not re-run

- #401's entrance-chart phases, two-sided adapters, bank routes, owner injectivity, invoice and bit component (via its receipts).
- #398/#376's reconstruction.
- #392's bootstrap.
- #377's and #352's all-size interfaces.
