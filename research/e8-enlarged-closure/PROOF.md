# Why the word computes its operator, and what is re-opened (§§1–6: our #407, run here as a control; §§7–10: this package)

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

# This package: sequential groups and enlarged entrances (`compose410.py`)

**7. Enlargement (#410).** A pivot p with relation ρ_p moves to a one-pivot group on an entrance E′ ⊋ E. E′ lies in the first frames of p and of every donor of ρ_p. S is unchanged as a matrix, so M_ours is unchanged on all columns. Only p's start frame and the donors' entrance visits change: a donor now visits nested spaces E ⊂ E′ in increasing dimension, because the unit shears are sorted by entrance dimension. `gx.check1` E1 checks every step for nesting.

For 1020 (re-pivoted to 1001 in our base), the relation ρ′_{1001} = ρ_{1020}/c has the same roles, so E′ is admissible for it. The inventory moves to {4:736, 5:608} from {4:120, 5:216}.

**8. Sequential groups (#409).** The ten new pivots P are not gauged in the base, and they are donors only of older (#404) groups. Their 55 unit shears h_d += c·h_p are prepended to A, and no source p ∈ P is written by an earlier entrance gate (checked).

The chronological product therefore has no cross terms from later updates reading earlier writes. The realised prefix equals the literal right-multiplication of M by each shear in order. `compose410.py` checks this on all 1,021 columns and the retained totals, exactly as #409 states it. It needs no N² = 0 assumption.

Re-pivoting a #409 group is §2 applied to the group's relations. Exact rank equality checks that the span is unchanged.

**9. Sixths.** With 1010 or 910 as pivots, a half coefficient of a promoted pivot's unit dirt meets a later /2 gate (gxcore E5 at 204 and 275). Pivoting on 739 and 531 removes this, and gxcore passes on the whole word.

**10. Price.** The profile uses 32 replicas (288 invocations), 2,943 banks per stage, 1,495 rank-1 paddings less 64 fused, live 57,207 and m = 73, with an exact deficit of 312 per replica. The engines and bootstrap are as in §6. Controls: #409's (32 replicas), #408's (64) and #410's (16) b and κ are reproduced from our emission of their own words with their own published patterns.

# This package: grouped and frame-closure promotions and the target-124 prefix (`compose416.py`)

**11. Promotions.** Each new pivot p ∈ {766, 917, 627, 948, 892, 669, 644, 947} has a relation ρ_p = e_p + Σ c_{p,d} e_d with K ρ_p = 0 on #412's gauged word. Its donors are not gauged, and its pivot is no donor of any plan. The 48 unit shears are prepended to A, so the chronological product is the literal right-multiplication. `compose416.py` checks this on all 1,021 columns and the retained totals, and checks that all 212 gauged response columns are zero.

The 947 row is #416's 821 relation re-solved on our word (the system is unique on its donor set) and divided by its 947 coefficient −½. This gives the same span with integral coefficients.

**12. Frame closure.** A donor may now visit an entrance space that its old frame chain does not contain. Following #416, every later gate whose frame does not contain its operands' current frames is raised to the reduced-echelon span of them, and this is propagated. Scalar operations are unchanged. Every path stays nested and ends at its prescribed final frame (gx E1 checks every step). Reverting any of the 5 raised frames fails E1.

**13. Target-124 prefix.** Let t = 124, and let r be its first positive-frame read (B1262: 171 −= 124 at frame 723). Its earlier B writes W (B867, B1260) are replaced by source-touching empty markers, so no helper walk changes, and by deliveries d_j of helper values available at their current frames: 563 at 336 at slot 11 and 253 at 723 at slot 499. These are chosen so that Σ q_j·prot(h_j) = Σ_W q·prot(src), where prot keeps the x, y and gauged columns.

Between the deliveries and r, t is not read. So t's value at r, and with it every later y and helper row, is unchanged on the protected columns. Only the ungauged columns of y124 and y171 change. Our emitter's old-response precancellation is computed from the actual word, so it absorbs them, and both orientations pass on all live columns.

E5 (x-content in sixths) holds because both coefficients are halves on integral x-content. E4 is untouched because both sources are helpers.

**14. Price.** As in §10, with 32 replicas, 2,939 banks per stage, 1,459 rank-1 paddings less 64 fused, live 57,171.

# This package: #420/#421 gauges, entrance enlargements and the target-125 prefix (`compose423.py`)

**15. Further promotions (#420, #421).** Pivots 672 ([48]; ρ = e_672 + e_345 − e_673), 435 ([304,111]; ρ = e_435 + e_421) and 367 ([259,246]; ρ = e_367 + e_257) are eumemic's relations, used unchanged; on our word each satisfies Kρ = 0 (the 215 gauged response columns are zero, and gx E7 passes). They join §11's prefix as literal shears, so §11's operator identity is checked again with 52 shears on all 1,021 columns. Frame closure (§12) raises 10 gate frames; reverting any one fails E1.

**16. Enlargement of start frames (#423).** For a gauged p with entrance space E, starting p at E′ = E + ⟨u⟩ changes no scalar instruction: p is zero before its first gate in both orientations, and its shears h_d += c·h_p run at p's new start frame. Gate frames that no longer contain their operands' current frames are raised to the span (closure, as in §12; 29 frames). The full raw operator and retained totals are unchanged on all 1,021 columns (checked), and gx E1 checks every nested path and final endpoint. Thirteen of #423's fourteen enlargements transfer (661, 695, 834, 835, 846, 851, 852, 858, 861, 863, 941, and the joint 914/960 → [48,12]). #423's 785 is not a gauge on our word. Our screen of all 819 one-dimension enlargements of the remaining gauges inside their first gate frames found one that adds: 838 [204] → [304,204] (+1.63·10⁻⁸). Reverting any raised frame fails E1.

**17. Target-125 prefix.** As in §13, every B write into y125 before its first positive-frame read (B1270) becomes a source-touching empty marker. Three deliveries replace them: helper 563/2 at frame 336 (slot 13), and helper 367/2 at frame 904 and −helper 251/2 at frame 724 (slot 975). At slot 975, 367 is still in its interval at frame 485 → 904, and the delivery gate at 904 moves it there early. Its next touch is already at 904, so its climb partition is unchanged. The protected x, y and gauged columns of every row are unchanged (checked); only y125's and y172's ungauged dirt changes, and the emitter recomputes it. All coefficients are halves on integral helper rows, so every entry stays in sixths (gxcore passes). 125's chain goes (3,3,1,1) → (2,4,1,1).

**18. Price.** As in §14 with 64 replicas (576 invocations): inventory {9:36224, 8:9536, 7:1536, 5:1152, 4:1536}, 5,859 banks per stage, 2,747 rank-1 paddings less 128 fused, live 114,171, deficit 312 per replica (checked). The replica sweep gives 16 → 1.018468e-3, 32 → 1.018488e-3, and 128 equal to the 64-replica value. The bit side is #404's pinned c ≈ 1.021539e-3 > b.

**19. Target 144 (negative result, exploration only).** We searched exact prefixes for every target whose pre-cut writes are helper-sourced. Deliveries come from any helper or x register, at the frame of the source's current touch interval or of its next touch (so no source changes its climb partition). We allowed any number of deliveries, up to four frame groups, and shift/restore among same-frame sources (the §3 trick). The test per chain is exact: rational solvability plus an integer-lattice condition, namely that each frame group's x/gauged total lies in (1/6)ℤ, solved by Hermite normal form.

For 144, only (3,4,1) via frames 311 → 935 and (4,3,1) via 551 → 935 are rationally solvable, and both fail the lattice condition. The reason is simple. Every source available at frame 935 satisfies x₆ = x₁₂/2, while the needed total has x₁₂ = x₆ = −½. Whatever is delivered before the final group must therefore carry x₆ = −¼, which no sixths entry gives.

Target (y) sources cannot help either. 144 already reads y into 208, so it is a pivot of a y→y pair, and a y-read into 144 would fail gx/gxcore E4.

Across all targets, 125 is the only new feasible form, and 144 is the only one blocked solely by sixths.

## Re-opened by §§15–17

- The phases of the 3 new gauges and the 14 enlarged entrance tokens, and of the 39 raised frames.
- The 125 target edges with their changed ungauged dirt.
- The 128 fused slots' owner placement at 64 replicas. The bank assignment is checked here: distinct rank-1-padded banks, padding on coordinate 72.
