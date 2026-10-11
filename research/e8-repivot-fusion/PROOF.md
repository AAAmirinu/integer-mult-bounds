# Why the word computes #404's operator, and what is re-opened

Notation: x (120 sources), h (781 helpers), y (120 targets). The word is gcert/1 (A, scatter, B).

**1. Gauges.** M is #398's raw operator. #404's selection gives, per plan, relations ρ_p = e_p + Σ_d c_{p,d} e_d with K ρ_p = 0, where K is the target-by-helper response. No pivot is a donor anywhere, so N = Σ c_{p,d} e_d e_pᵀ has N² = 0 and S = I + N. The unit shears h_d += c·h_p at the entrance frame realise S, and M_new = M · diag(I, I, S). `entrance404.py` re-implements this together with #404's 124/125 recovery and #376's frame edit, and must hit #404's two frozen hashes.

**2. Re-pivoting.** In one plan, let p be a pivot and x a donor of ρ_p with c_{p,x} ≠ 0. Set ρ′_x = ρ_p / c_{p,x}, and for every other pivot q of the plan set ρ′_q = ρ_q − c_{q,x} ρ′_x. Then:
- the new rows span the same space, which `fusion404.py` checks by exact rank;
- each new row is unit at its own pivot and zero at the plan's other pivots, and K ρ′ = 0;
- if x is a donor in no other plan and p a pivot in no other plan, the global "no pivot is a donor" condition survives.

Hence S′ = I + N′, N′² = 0, M_ours = M · diag(I, I, S′), and all 194 pivot columns of the target rows are zero. This is checked on all 1,021 columns. The x and y input columns are untouched, so the x→(x, y) rows equal #404's word. Pivot dimensions per entrance space are unchanged, so the residual inventory {4:120, 5:216, 7:72, 8:1144, 9:4696} and #404's bank patterns are unchanged.

**3. Sixths.** gxcore keeps every entry, including the gauged-dirt replay (E7), in units of 1/6.
- A donor d carries dirt c_{p,d} of each pivot p, in units of 1.
- A sink uncompute s −= (1/4)·d therefore stays in sixths only if every c_{p,d} is even. After the swaps, 1019 and 1020 carry coefficients −2 and −2.
- The same-frame solution for each sink is unique in the donor's coefficient. Removing that donor makes the target unreachable, which `find(…, exclude)` checks.
- So for 324, whose donor 1018 carries 941's unit dirt, no gate decomposition (±1/2, ±1/3 or shift/restore) can keep sixths. The final entry of 324 on key 941 is −1/4 for any decomposition with the same net map.

**4. Fusion.** The sinks' clean x-rows are zero after their last Y-influence, and the paid histogram is unchanged. Under #390's bracket a zero-row helper needs no final repair, so its final climb absorbs its bank's rank-1 padding (`climb_pad72`). Section F places all 16 occurrences in distinct rank-1-padded banks.

**5. Re-synthesis.** This is as in our #402: deliveries of present tokens at their frames, with the full raw operator identical (checked).

**6. Price.** We use #404's profile: 72 local invocations, idle children, 394 rank-1 paddings per stage less 16 fused, live 14,322 and m = 73. The engines are PR #315's with the 10⁻¹⁶ fallback, and the bootstrap is #392's six levels. Control: #404's b and κ are reproduced from our emission of #404's own word.

## Re-opened

- Phase admission of the four re-pivoted entrance tokens.
- Owner placement of the 16 fused slots.
- The fused final climbs.
- The 177/220 target edges and the scalar invoice.

## Inherited, not re-run

#404/#401's normalisation, phases, routes and invoice, and the bit component via receipts; #398/#376's reconstruction; #392's bootstrap; #377's and #352's interfaces.
