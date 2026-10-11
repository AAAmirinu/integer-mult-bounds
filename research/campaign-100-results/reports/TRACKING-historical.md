# Radical-ideas campaign, wave 1 (launched 2026-10-10 ~18:55 UTC) — 12 parallel agents
| agent | ideas | result file |
|---|---|---|
| A-kappa-of-p | 16, 15-lite, 72-lite (κ at p=8,9,11,12,13) | /tmp/radical/A/RESULT.md |
| B-certificate-whatif | 8, 18, 20, 21, 26, 28, 29, 46, 47, 48, 51, 54 | /tmp/radical/B/RESULT.md |
| C-evolution | 63, 69, 73, 74 (30 sandboxes) | /tmp/radical/C/RESULT.md |
| D-surrogate | 55, 61, 91 | /tmp/radical/D/RESULT.md |
| E-module-sat | 5, 37, 88 | /tmp/radical/E/RESULT.md |
| F-structure | 12, 14, 22, 36, 41 | /tmp/radical/F/RESULT.md |
| G-freeform | 1, 3, 11 (20 sandboxes) | /tmp/radical/G/RESULT.md |
| H-small-exact | 15 (p=5,6,7 exact) | /tmp/radical/H/RESULT.md |
| I-matching | 34, 40, 44, 74 (15 sandboxes) | /tmp/radical/I/RESULT.md |
| J-arith | 25, 38, 39, 56 | /tmp/radical/J/RESULT.md |
| K-packing | 13, 67, 71 (35 sandboxes) | /tmp/radical/K/RESULT.md |
| L-design-enum | 2 (20 sandboxes) | /tmp/radical/L/RESULT.md |
| M-math | memos for 18, 20, 23, 26, 28, 49, 50, 53, 59, 60, 97 | /tmp/radical/M/RESULT.md |
Not launched in wave 1: pure-proof items (19, 30, 52, 57, 58, 98, 99, 100), blocked (9: the complex supplier recipe is unpublished), months-scale (4, 10, 62, 75), new-architecture items needing a new generator (17, 24, 27, 31–33, 35, 42, 43, 45, 76–87), enablers (89, 90, 92–96), 6, 7, 64–66, 68, 70.

## Wave-1 results
- J-arith (25/38/39/56): 38, 56, 39 dead (all removable/odd gates at rank 0; histogram invariant). 25: centre mass is the lever — deficit = 4v−5ℓ, ℓ = Σ centre dims, ≈ +1.9e-6 κ per unit of centre mass removed (uncapped; complex cap binds after ~1.3 units → #327's cap matters). Point-star centres have rank exactly h−2; lower ℓ needs a new decoder. WAVE-2 TARGET: decoder with centre span < h−2.
- B-certificate-whatif: dead ≤3e-12: 8/46/47/48/54/28/51/52; Gram form not a pricing lever. Complex cap: ceiling 7.72118e-4 now, 7.78990e-4 with #327 centre-sharing (headroom +0.32% → +1.21% bit root). Sensitivity +3.8e-7 κ per unit of deficit. ℓ=h(h−3): +3.8e-5; merged idle boundaries: +2.1e-5…+3.0e-5; 4-stage 2+2 completion: κ≈1.2e-3 (+4e-4) if PR234's three-XOR swap can be replaced. M-math redirected to derive-or-refute 18/21/26.
- D-surrogate (55/61/91): κ depends on the paid-climb histogram only (entrances cancel). Surrogate: R² 0.986 overall but coin-flip at <0.002% — coarse filter only; not enough to drive millions of steps. J vs κ: Spearman −0.9999995, sign agreement 287,660/287,669 — J is exact for ranking; scale is dκ/dJ = −1.39e-9 (not 6.3e-10); curvature-corrected weights w_r = r(e^{aL_r}−1) fix the 9 near-ties. Exact κ from histogram now 25 ms (exact) / 50 µs (float) / 11 µs incremental sign test (/tmp/radical/D/kap/). Caveat: Wn = W_lit//5 formula is only exact when mass ≡ 0 mod 5. Module-annealer κ bookkeeping was noisy (20/172 re-evaluate differently).
- F-structure (12/14/22/36/41): all dead on #325's word. |Aut| trivial modulo identical centre records; transposition is a histogram identity; frames already {0,±1}-spanned, no character frames possible (parity obstruction); nondegeneracy never binds over Q and no field (Q(i), F_3/5/7) adds intermediates; exhaustive rank-2–4 read-span census adds 5,496 candidates but closure packing is byte-identical (0 φ).
- L-design-enum (2): dead. #325 uses ONE design for all 120 cubes; design space 15^12 per cube; #325's is the unique 24-node (minimum) all-face-diagonal design and the only one with Δregisters=0; per-cube cost is NOT additive (joint gain 0.05–0.24× predicted, arc matching couples 10–18 cubes). Design is frozen; lever = modules/matching (8 arcs per cube effect).
- I-matching (34/40/44/74): dead as research direction. 202 physical evals. Random max matchings all below HK (−0.013…−0.029%); κ-exact min-cost carrier matching (J weights are exactly the κ weights, droot/climb = −2.906e-10·r·ln(100/r)) gives a free deterministic +6.29e-8 (+0.0082%), best noisy +0.0095%; drop-in arcs at /tmp/radical/I/best_arcs_p10_cwJ.json. Tier boundaries exhausted (#325's tiered reuse is optimal in class). Spectral: dead; Steiner (no duplicate carriers): −6…−10%.
- E-module-sat (5/37/88): dead as stated — fewer additions makes κ much worse (pair 244-add AG(2,3) module: −1.06e-4; all-but-one 18-add optimum: −4.5e-5). κ prices R = additions + roots − carrier arcs; per-instance arcs = max matching with nested vertex covers (millisecond proxy in pair_proxy_anneal2.score). pm_p10: 92 uncarried vs structural floor ~70 → at most ~440 registers ≈ +2e-5 left in the pair module (needs richer moves). qmod_p10 is already optimal (uncarried = #roots). Node order alone worth 9 arcs/instance.
- A-kappa-of-p (16): dead as a lever. κ(p) with generic modules: p=8 5.97e-4, 9 6.53e-4, 10 6.41e-4, 11 6.58e-4, 12 6.08e-4, 13 6.30e-4, 14 5.81e-4 (zigzag = PR117 module quality; smoothed plateau 6.4–6.7e-4 over p=9..11). Module annealing is worth +1.27e-4 at p=10 (generic 6.41e-4 → 7.68e-4), orientation +1.8e-6. With restricted annealed modules: p=9 7.24e-4, p=11 7.29e-4, p=12 7.26e-4 vs p=10 7.70e-4. p=9/15 need 90 replicas (60·width ≢ 0 mod 90). p=11 is the only alternative base candidate. Tooling: /tmp/radical/A/build_p.py.
- M-math: 18 (4-stage 2+2 completion) REFUTED (k_min = 2P+1, exhaustive F2/F3 confirms; only loophole a two-sided local word = new generator, plausibility ~0.02). 21 (merged idle) REFUTED (idle multiset {h−1, 2h−2} forced by bridge placement). 26 (ℓ=h(h−3)) OPEN: stars are the row-space minimum; open lemma: for every factorisation B = G Fᵀ, Σ dim span(supp f_j) ≥ h(h−2)? Decisive at p=5..7 by finite rank-minimisation, 1–2 weeks; +3.8e-5 uncapped, plausibility ~0.15. 20 = new decoder family I − J/s² (needs generator). 60 open (frame lemma). 59 legal in proof up to h temporaries, only global_lowering.py:247 forbids; no value found. 23/49/50/53/97/28 dead. Ranking: 26 > 20 > 60 > 18-loophole > 59.

## Wave 2 (launched ~20:35 UTC)
| N-centre-lemma | idea 26/20: decide "Σ dim span(supp f_j) ≥ h(h−2) for every factorisation B = G Fᵀ" at p=5..7 by exact/heuristic search; also I−J/s² decoders | /tmp/radical/N/RESULT.md |
| O-pair-module | pair module search on the uncarried-node objective (floor ~70 vs 92; ≈+2e-5 ceiling), CP-SAT LNS + structural moves, 25 sandboxes | /tmp/radical/O/RESULT.md |
- H-small-exact (15): dead for large gains; closure result. p=5 not priceable (deficit −80); p=6 κ 1.336e-4, p=7 4.705e-4 (generic modules). Exact CP-SAT frame assignment: p=6 OPTIMAL (+0.44% over producer, +0.06% over descent4s); p=7 gap 0.05%; p=10 on #325: CP-SAT 7.70734e-4 vs descent4s 7.70612e-4 vs base 7.69684e-4 (+1.05e-6 over base; bound gap 0.15%). Frame-assignment layer is within ≤0.15% of optimal after concave descent. Template: partner_mix lift to cap, target-suffix lift (2-gate uphill motif), cleanup gates at cap h−2. Retimed #325 moves: /tmp/radical/H/out/exact_p10.json.
- N-centre-lemma (26/20): lemma holds at p=5,6,7 (min centre mass = h(h−2) in every method: SA ~3e8 proposals, CP-SAT over structured candidates, exact enumeration in the star span); no counterexample; any counterexample must leave the star span. Proof sketch via clique conditions + restriction identity; two inequalities remain. Idea 20 (port size s≠3) dead: only s=3 gives positive deficit. Demote 26 to "very likely true, ≤5%".
- G-freeform (1/3/11): dead beyond a one-off. Only 1.5% of gates (5,242/347,760) have a non-trivial legal interval — pinned by the verifier's integer-source-span rule, not by the candidate set. Free-form SA beats descent4s by −83 J = +1.2e-7 κ (7.70733e-4 on the parity word, same floor as H's CP-SAT), reproducible in 10 min; larger lattice/compound moves add nothing. Only gate/operand reordering could enlarge the live region. Sandboxes: finalize.sh deletes at ~17:55 EDT; fallback: python /tmp/radical/G/dt/collect.py --fetch --delete.
- C-evolution (63/69/73/74): 1,695 physical evals on 30 sandboxes. Best κ 7.701695e-4 = +0.0631% over #325 — a pure reordering of #325's 12-entry design list (move ['A',0,0] to the end; /tmp/radical/C/best/top1_transposition.json), found within 10 evals by every method, plateau afterwards. BO: PLAIN=12 +0.0063% (tiering must stay 'dim'); composition top1 + PLAIN 12 = 7.701858e-4 (+0.0652%). Dead as methodology; next genome = cube_orient_p10.json (120 cubes × 6 orientations), untouched.
- K-packing (13/67/71): dead. ~16,000 packing runs on #325's word: 100× restarts +4.9 φ (inside #320's 25-φ spread), tabu never leaves its start, learned +0.9. Only noise amplitude matters (NOISE≈5 instead of 0.3 reaches −2393.9 in ~200 restarts). CRUCIAL: on #325's word the kernel stage crosses the complex cap after ~400 entries — descent+target+any packing all price to exactly 7.72117724e-4 (the cap). The whole stage stack on #325 is cap-bound without #327's supplier. Frozen kernel for #325: /tmp/radical/K/kernel-selection_best.json (1,332 entries, φ −2393).
- O-pair-module: dead. 92 uncarried is a strict local optimum under SA, CP-SAT LNS (3,353 rounds, 35 sandboxes) and targeted neighbourhoods; floor sharpened to 71 + small nodes (gap ≤ 21 nodes ≈ +2.3e-5 in principle, no constructive design found). pm_p10 stays the best module.

## New-architecture campaign (launched 2026-10-11 ~00:55 UTC) — ARCHITECTURES-100.md
| agent | architectures | result |
|---|---|---|
| S-synth | generic word synthesizer (gating tool) | /tmp/radical/S/RESULT.md, ARCH-SPEC.md |
| T1 | 1–10 port geometries A | /tmp/radical/T1/RESULT.md |
| T2 | 11–20 port geometries B | /tmp/radical/T2/RESULT.md |
| T3 | 21–30 decoders A | /tmp/radical/T3/RESULT.md |
| T4 | 31–40 decoders B + centres A | /tmp/radical/T4/RESULT.md |
| T5 | 41–50 centres B + algebra A | /tmp/radical/T5/RESULT.md |
| T6 | 51–60 algebra B | /tmp/radical/T6/RESULT.md |
| T7 | 61–70 module algebra | /tmp/radical/T7/RESULT.md |
| T8 | 71–80 global layouts | /tmp/radical/T8/RESULT.md |
| T9 | 81–90 hybrids | /tmp/radical/T9/RESULT.md |
| T10 | 91–100 searched architectures | /tmp/radical/T10/RESULT.md |
| Q-complex | stage stack / modules on #346's complex word (binding side) | /tmp/radical/Q/RESULT.md |
Leader at launch: #346 (LJH-217) 7.92580e-4 — complex binds, bit root 1.07% above cap. P-compose stopped (its design-order lever +0.044% bit-side recorded in /tmp/radical/P/RESULT.md).
