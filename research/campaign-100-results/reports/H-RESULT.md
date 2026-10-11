# H-small-exact — idea 15: solve tiny cube sizes exactly, read off the optimum's structure

Scripts and data: /tmp/radical/H (build_small.py, price.py, wlib.py, exact_cpsat.py, apply_moves.py, structure.py,
dt_run.py; out/ holds the p = 5, 6, 7 packages, pickled words, moves files and logs).

## 1. Small-p words with #325's producer and the generic w320 modules

build_small.py = copy of the #325 package (bitword/producer/paired_cube_bit_word.py + regenerate.py --solve-matching
--emit), MODULES/QMODULES/MERGE tables, regenerate.P and word_pins.P patched to p, generic modules
restricted_pairs(p-1) + greedy star root (the pm_p10 centre-sharing contract) and all_but_one(p-2) (needs p >= 5),
#325's cube-local design local_design_p10.json reused unchanged (it is a per-cube plane recipe, p-independent),
cube_orient dropped (default orientation), moment.certify bisection ceiling raised .003 -> .02.
price.py = the pricing block of /tmp/p10job/physical_eval.py (prepare -> physical527 -> parity_transform in record
mode, shape-aware five-stage ledger, moment.certify, outer chain), p-generic through word_pins.shape(); it reproduces
#325's kappa = 7.69684039e-4 exactly at p = 10 (out/price_p10_ref.json).

The generator's geometry (ports = triples of coordinate pairs, v = 8 C(p,3), H0 = (I - J/9)/2, target cap
ker(3 chi_T - 1)) runs unchanged at p = 5, 6, 7; decoder identity, matching, gauges, make_physical, descent.py and the
whole admission pipeline (prepare/physical527/parity) pass. What changes with p is the physical layer:

| p | h | v | five-stage deficit 4v-5h(h-2) | virtual R | gauges | reuse pairs | physical R | kappa (producer word) | J_rec |
|---|---|---|---|---|---|---|---|---|---|
| 5 | 10 | 80 | **-80** | 660 | 0 | 0 | 660 | none (no positive root: rank mass exceeds the stock) | n/a |
| 6 | 12 | 160 | 40 | 1524 | 0 | 0 | 1524 | **1.33611920e-4** (root 1.33630e-4) | 54949.52 |
| 7 | 14 | 280 | 280 | 2870 | 510 (4 pairs dropped for bank parity) | 190 (rank 11) | 2680 | **4.70539263e-4** (root 4.70761e-4) | 109117.53 |
| 10 (#325) | 20 | 960 | 2040 | 9300 | 1200 | 1200 | 8100 | 7.69684039e-4 (root 7.70277e-4) | 483291.16 |

J_rec = sum over paid climbs r of r ln(5h/r) of the physical-record chains (the descent4s.py objective; centre copies
excluded). kappa(p) with the generic modules: p = 5 is below the five-stage threshold (deficit negative, the layout
cannot be priced at all), p = 6 is barely above it (deficit 40, no gauge passes the PR144 selection criterion, so no
reuse pairs), p = 7 is the first size with the full physical structure (gauges + late reuse). kappa rises steeply:
1.34e-4 (6) -> 4.71e-4 (7) -> 7.70e-4 (10). The smallest *working* p is therefore 6, and the exact optimisation was
done there (and, since it was cheap, repeated at p = 7 and on the #325 p = 10 word itself).

## 2. Exact joint frame assignment (CP-SAT)

Model (exact_cpsat.py; identical legality to descent4s.py in the tooling dir): the pickled post-parity word
(build_word_stages parity stage, pins recorded); every ADD gate except the copy windows / centre-copy reads picks a
frame g with prev_a, prev_b ⊆ g ⊆ next_a, next_b on its two register chains, the chi-span of its integer source
support inside g, g nondegenerate for G = I - J/9 and prime-witness residual < 2^80; cost = J_rec.
Candidate universe: per gate the interval [LB, UB] (LB = transitive join of the predecessors' LB and the span,
UB = transitive meet of the successors' UB), filled by the local join/meet closure (join(LB, c_a, c_b) over the
predecessors' candidates, meet(UB, c_a', c_b') over the successors') iterated to a fixed point, degenerate members
replaced by their one-row repairs. Since the cost is concave in the dimension, in any single-gate-optimal assignment
every gate sits at the join of its predecessors (+ span) or the meet of its successors, so this universe contains the
global optimum up to the nondegeneracy repairs. Robustness check at p = 6: adding every frame of the original word
inside [LB, UB] (+488 candidates) gives the same proven optimum.
CP-SAT: Boolean x[gate, frame], exactly-one, nesting as x[g,f] -> OR of x[g',f'] over f' ⊇ f, integer dim per gate,
one AddElement per chain pair with the 10^6-scaled r ln(m/r) table, hint = current frames. (A pairwise
local-polytope formulation was also tried: far weaker bound, dropped.)

| p | gates | movable | free (LB != UB) | candidates | status | J producer | J descent4s (12 rounds) | J CP-SAT | lower bound | gap |
|---|---|---|---|---|---|---|---|---|---|---|
| 6 | 27376 | 26872 | 3090 | 13340 | **OPTIMAL** (82 s, 2 workers) | 54949.52 | 54724.36 | **54690.04** | 54690.04 | 0 |
| 7 | 62608 | 61740 | 4747 | 12576 | FEASIBLE (1500 s local 2 workers, then 3600 s Daytona 4 cpu/8 GiB: same incumbent) | 109117.53 | 108882.87 | **108879.24** | 108825.8 | 53 (0.05 %) |
| 10 | 350680 | 347760 | 17960 | 49507 | FEASIBLE (1500 s, 2 workers, started from descent4s) | 483291.16 | 482653.99 | **482570.75** | 481863.7 | 707 (0.15 %) |

Exact kappa of each word (apply_moves.py -> kappa_shape.py, same ledger as price.py):

| p | producer | descent4s | CP-SAT | CP-SAT - producer | CP-SAT - descent4s |
|---|---|---|---|---|---|
| 6 | 1.33611920e-4 | 1.34116352e-4 | **1.34193525e-4** (proven optimum of the model) | +5.82e-7 (+0.44 %) | +7.7e-8 (+0.06 %) |
| 7 | 4.70539263e-4 | 4.71469704e-4 | **4.71484092e-4** | +9.45e-7 (+0.20 %) | +1.4e-8 |
| 10 | 7.69684039e-4 | 7.70612425e-4 | **7.70733743e-4** | +1.05e-6 (+0.14 %) | +1.2e-7 |

So at the exact instance (p = 6) the producer's own descent.py leaves 0.44 % of kappa on the table, concave descent
(descent4s) recovers 87 % of that gap, and the true optimum of the frame-assignment layer is only 0.06 % above
descent4s. The p = 7 and p = 10 bounds say the same: whatever remains above the CP-SAT incumbent is at most
0.05 % / 0.15 % of J (about 1e-7 / 1e-6 of kappa at p = 10, i.e. below what a single structural change elsewhere
in the word is worth).

## 3. Structure of the exact optimum (the design template)

Position of the free gates (p = 6 optimum): 1171 at LB, 1740 at UB, 179 strictly between (producer: 1339 / 1454 / 297).
The optimum is extremal almost everywhere; the strictly-between frames are joins/meets of neighbouring gates'
frames (107 new dim-7 frames and 18 dim-9 frames at p = 6 that do not occur in the producer word).

Moves of the optimum relative to the producer word, p = 6 (415 gates), with the same pattern at p = 7 and p = 10:
1. **partner_mix at the delivery cap.** The partner-pair mix gate (carrier += passive, category partner_mix) moves
   from the dim-2 mix frame <chi_c, chi_d> to the receivers' cap (dim h-2): 80/80 pairs at p = 6, 140/140 at p = 7,
   480/480 at p = 10. Source chains become (h-3, 2) instead of (1, h-4, 2) / (1, h-2): both members of the pair pay one
   climb of h-3 and the carrier's extra climb disappears (-1.2 J per pair at p = 6). descent4s finds this one too; the
   producer's descent.py cannot (it runs on the virtual word where the kchron mix frames are fixed).
2. **Target-suffix lift to the cap (coordinated two-gate move).** The last side-root read of a target and the
   partner delivery after it both move to the target cap (dim h-1): side_root 9/10 -> 11 (80 gates) and
   partner_delivery 10 -> 11 (40) at p = 6; target chains (9,1,1)/(10,1) become (11,) / (9,2). The root/carrier register
   pays +1 on its last climb (+1.4 J), the target saves a climb (-3.4 J). descent4s misses it because the first gate
   of the pair alone is uphill (+1.39) — this is the only genuinely non-greedy motif in the optimum and, with the
   forward_gate 5->7 re-splits that it enables (78 gates), the bulk of the 0.06 % gap at p = 6 (302/3090 free gates
   differ between descent4s and the optimum). At p = 7/10 the analogous gates are already at UB and no gain remains.
3. **Cleanup/undo gates at the cap instead of the full frame** (cleanup_gate / partner_cleanup h -> h-2: 44 gates at
   p = 6, 119 at p = 7, 302 at p = 10) and **unbalanced helper climbs** (forward_gate 5->7, 6->9, 13->12, 15->14, 10->8,
   ...): by concavity of r ln(m/r) an unequal split (2,4) is cheaper than (3,3); these are the strictly-between
   frames. Each is worth 0.3-2 J; together they are the CP-SAT-minus-descent4s difference at p = 7 and p = 10.
4. Nothing moves at chain ends: all moved gates are interior ('middle' 100 %), operand kinds help/help and src/src
   (plus tgt/help, tgt/src for item 2). No gauge, root, source, copy or target frame changes (they are fixed in the
   model), and the climb histogram keeps the same support (ranks 1..h-1); the optimum only re-partitions climbs.

Template for p = 10: (1) is already in descent4s; (2) = add a "lift the target suffix to the cap" two-gate move
(side-root read + following delivery) to the descent move set; (3) = run exact_cpsat.py itself — at p = 10 it is
cheap (3 min closure + 25 min CP-SAT on 2 cores gives kappa 7.70733743e-4 on the #325 word, +1.05e-6 over the pinned
word, +1.2e-7 over descent4s), and the remaining proven headroom of the whole frame-assignment layer is <= 0.15 % of J.

## 4. Verdict

**Dead as a source of large gains, useful as a closure result.** Solving the gate-frame assignment exactly at the
smallest priceable size (p = 6, 3090 free gates, CP-SAT optimal in 82 s) shows the optimum is 0.44 % of kappa above
the producer's descent.py and only 0.06 % above concave descent (descent4s); at p = 7 and on the #325 p = 10 word the
CP-SAT bounds cap the remaining frame-assignment headroom at 0.05 % and 0.15 % of J. The optimum's structure is
"every gate at an extreme of its interval, climbs merged or unbalanced", with one non-greedy motif (target-suffix lift
to the cap, item 2). p = 5 cannot be priced at all (five-stage deficit -80), so the "p = 4 exhaustive search" of
idea 15 is moot: the layout has no certificate below p = 6. Side products: kappa(p) for the generic modules
(p = 6: 1.336e-4, p = 7: 4.705e-4, vs 7.697e-4 at p = 10 — the curve is steep, agent A's p = 8..13 map should be read
against these), and a ready retimed #325 word (out/exact_p10.json moves, kappa 7.70734e-4 under the descent4s legality
rules — needs installation through the gen5 descent stage/verifier to become a package).
