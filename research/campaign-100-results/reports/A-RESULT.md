# A-kappa-of-p: κ as a function of the cube size p (RADICAL-IDEAS 16, with 15/72-lite restrictions)

Everything under /tmp/radical/A: `build_p.py P OUT [--annealed] [--orient] [--pm pm.json] [--qmod q.json] [--tag T]`
(copies #325's package, installs modules + the cube-local design renamed `local_design_pP.json`, patches
MODULES/QMODULES/MERGE, regenerate.py P, word_pins.P, runs `regenerate.py --work --solve-matching --emit`, installs the
emitted word and prices it with `price.py` = the shape-aware pricing block of /tmp/p10job/physical_eval.py in terms of h, v).
Per-build artefacts: `out/pkg_<tag>/` (package with the word installed), `out/result_<tag>.json`, `out/regen_<tag>.log`,
`out/price_<tag>.log`; `summarize.py` prints the full table (32 builds). Modules: `mods/`, restriction tool `restrict.py`.
All builds ran locally (p=8: 20 s, p=10: 75 s, p=11: 130 s, p=12: ~5 min, p=13: 7.5 min, p=14: 13 min, < 1 GB); no Daytona needed.

## Producer at other p: what had to change

* Generic modules: `restricted_pairs(p-1)` from w320 modules.py plus a **greedy star root** (sum of all inputs built by a
  largest-first disjoint cover of existing module nodes, then a chain of adds) to meet the pm_p10.json contract
  (`len(roots) = C(p-1,2)+1`, last root = star(2i+bit) = the copied centre); `all_but_one(p-2)` (pinned_all_but_one contract:
  `input_count == n == len(roots)`, `args[:n] == [None]*n`). Only `input_count/args/roots` are read by the producer.
* The cube-local design of #325 (12 plane recipes) is accepted unchanged at every p (checked: the producer's
  `local_design()` only uses 3-bit selectors; decoder identity and G-nondegeneracy pass at p=8..14).
* Cube orientation skipped (cube_orient_p10.json removed) except for the #325 reproduction; at p=10 it is worth
  +6.6e-7 (generic modules) / +1.8e-6 (annealed modules).
* **p = 9 cannot use a 60-replica bank**: the bank rule needs `60*width ≡ 0 mod m=90`, i.e. `width ≡ 0 mod 3`; dropping an
  h-3 = 15-rank pair changes width by 3, so make_physical's drop loop can never fix the residue (it asserted). Allowing
  rank-14 recipients (`--ranks 15,14`) does not help (no rank-14 gauge is chain-top, recipient candidates stay = v). I priced
  p=9 with **90 replicas** (`REPLICAS=90`; the moment root is invariant under the replica count, only divisibility
  changes). p=15 (h=30) has the same obstruction. The drop loop was also made residue-aware (identical behaviour at other p).
* moment.certify's bisection ceiling `hi=.003` left as is (all roots < 0.001); patched to .05 in the copies anyway.

## Calibration at p = 10 (same design, no orientation unless stated)

| modules | orient | R | entrances | stock | bit root | κ | J_phys |
|---|---|---|---|---|---|---|---|
| generic restricted_pairs(9)+star, all_but_one(8) | no | 10709 | {16:1182, 17:29} | 814725 | 6.418232e-4 | **6.414115e-4** | 589949 |
| generic | yes | 10680 | {16:1190} | 814080 | 6.424888e-4 | 6.420763e-4 | 589291 |
| generic pairs restricted from restricted_pairs(10)+star (coord 9 deleted) | no | 10294 | {16:1182, 17:54} | 788550 | 6.666957e-4 | 6.662516e-4 | 566234 |
| #325 annealed pm_p10 + qmod_p10 | no | 8425 | {16:1200, 17:325} | 661725 | 7.684783e-4 | 7.678882e-4 | 485149 |
| #325 annealed + cube_orient_p10 (= PR #325) | yes | 8100 | {16:1200} | 658800 | 7.702769e-4 | **7.696840e-4** (reproduced exactly) | 483909 |

Annealing gain at p=10: **+1.265e-4 in κ** (R 10709 → 8425, J_phys −104 800, slope ≈ 1.2e-9 κ per unit J_phys;
J_five slope ≈ 2.4e-10). The third row shows that the *generic* module quality alone moves κ by 2.5e-5 at fixed p
(the PR117 specialisation at n = 9 is a poor module; the restriction of the n = 10 one is better with 235 instead of 273 adds).

J definitions: J_phys = Σ r·ln(m/r) over the physical paid climbs per invocation incl. the h centre copies (descent.py's
objective); J_five = Σ r·ln(m/r) over the five-stage histogram per invocation (×5 paid climbs + 2v idle at each of
(2h-2, h-1, 2h+2, 4) + bundled entrances 5a).

## κ(p) with the generic modules (same module construction and design at every p; cube orientation off)

| p | h | v | m | deficit | R | R/v | entrances (rank: count) | literal stock (60 repl.) | bit root | capped | κ | J_phys | J_phys/v | J_five |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 16 | 448 | 80 | 672 | 4564 | 10.19 | {12:536, 13:68} | 353925 | 5.970781e-4 | no | 5.967218e-4 | 207774 | 463.8 | 1124537 |
| 9 | 18 | 672 | 90 | 1248 | 7040 | 10.48 | {14:812, 15:62} | 814030 (90 repl.; 60-repl. width not integral) | 6.533101e-4 | no | 6.528835e-4 | 353040 | 525.4 | 1908532 |
| 10 | 20 | 960 | 100 | 2040 | 10709 | 11.15 | {16:1182, 17:29} | 814725 | 6.418232e-4 | no | 6.414115e-4 | 589949 | 614.5 | 3175601 |
| 11 | 22 | 1320 | 110 | 3080 | 14548 | 11.02 | {15:2, 16:18, 18:1626, 19:28} | 1107540 | 6.581701e-4 | no | 6.577372e-4 | 867187 | 657.0 | 4675374 |
| 12 | 24 | 1760 | 120 | 4400 | 20968 | 11.91 | {17:2, 18:8, 20:2176} | 1571235 | 6.080137e-4 | no | 6.076442e-4 | 1347924 | 765.9 | 7230596 |
| 13 | 26 | 2288 | 130 | 6032 | 25965 | 11.35 | {19:2, 20:10, 22:2832, 23:17} | 1961790 | 6.299614e-4 | no | 6.295648e-4 | 1775778 | 776.1 | 9566932 |
| 14 | 28 | 2912 | 140 | 8008 | 34891 | 11.98 | {24:3622, 25:3} | 2605905 | 5.814735e-4 | no | 5.811356e-4 | 2564403 | 880.6 | 13760910 |

No bit root reaches the complex cap 7.72714e-4 (κ at the cap = 7.721177e-4); nothing is capped.
Dropped pairs for bank divisibility: p=8 0, p=9 0, p=10 1, p=11 4, p=12 0, p=13 11, p=14 3.

κ(p) is **not monotone**: odd p beat both even neighbours (9 > 10, 11 > 12, 13 > 14) and the generic optimum is p = 11
(6.577e-4), with p = 9 second (6.529e-4) and p = 10 third (6.414e-4). The zigzag is a module artefact, not geometry: the
p = 10 word with a pair module restricted from the n = 10 generic module scores 6.66e-4, above both p = 9 and p = 11.
Smoothing that out, the generic κ(p) is flat at ≈ 6.5–6.7e-4 over p = 9..11 and falls off on both sides
(p = 8: 5.97e-4; p = 12: 6.08e-4; p = 13: 6.30e-4; p = 14: 5.81e-4). R/v and J_phys/v grow with p (10.2 → 12.0, 464 → 881),
i.e. the per-source ledger gets worse with p while the five-stage layout (m = 5h, deficit 4v−5h(h−2)) favours larger h;
the two effects cancel around p = 10–11.

## Best available annealed modules at each p (restrictions of the pinned annealed modules; 15/72-lite)

A pair module at cube size p can be restricted to p−1 by deleting one coordinate (keep the pairs not containing it; images
by support hash-consing; every surviving root keeps its contract, including the star) — the trick that produced qmod_p10
from the gen5 qmod_p12. Sources: #325's pm_p10/qmod_p10 (→ p = 9, → p = 8 twice), the gen4 annealed pair_module_p12 (55
inputs + star) / qmod_p12 from /private/tmp/imbwork/w325/research/five-stage-gen4-banks (→ p = 11; and used directly at
p = 12 although they were annealed against a different ("seed-4") local design). All 9 (p=9) / 11 (p=11) / 8 (p=8)
deleted-coordinate choices were built; the all-but-one restriction choice is irrelevant (< 4e-9 at p = 9).

| p | modules | best coord | R | entrances | stock | bit root | κ | J_phys | vs generic |
|---|---|---|---|---|---|---|---|---|---|
| 8 | pm_p10 restricted twice (4 then 5), qmod_p10 restricted twice | r4r5 | 4056 | {12:536, 13:144} | 319740 | 6.505294e-4 | 6.501065e-4 | 189274 | +5.3e-5 (range 6.41–6.50e-4) |
| 9 | pm_p10 restricted, qmod_p10 restricted | coord 4 | 6056 | {14:840, 15:212} | 712260 (90 repl.) | 7.247665e-4 | **7.242416e-4** | 315356 | +7.1e-5 (range 7.11–7.24e-4) |
| 10 | #325 annealed (no orient / orient) | – | 8425 / 8100 | | 661725 / 658800 | 7.684783e-4 / 7.702769e-4 | **7.678882e-4 / 7.696840e-4** | 485149 / 483909 | +1.265e-4 |
| 11 | gen4 pair_module_p12 restricted, qmod_p12 restricted | coord 2 | 12430 | {18:1650, 19:242} | 969060 | 7.300059e-4 | **7.294734e-4** | 775049 | +7.2e-5 (range 7.18–7.29e-4 over the 11 coords, see summarize.py) |
| 12 | gen4 annealed pair_module_p12 + qmod_p12 (foreign design) | – | 16434 | {20:2200, 21:290} | 1283215 | 7.262549e-4 | 7.257278e-4 | 1112224 | +1.18e-4 |

With the best available annealed modules the ranking becomes p = 10 (7.697e-4) > p = 11 (7.295e-4) > p = 12 (7.257e-4)
> p = 9 (7.242e-4) > p = 8 (6.501e-4); p = 13/14 have no annealed modules (generic 6.30e-4 / 5.81e-4). These are lower
bounds for p ≠ 10: a restricted module inherits only part of the anneal (at p = 10 restriction of a generic module was worth
+2.5e-5 vs +1.27e-4 for a native anneal), and the p = 12 modules were tuned for another design.

## Verdict

κ(p) is **not monotone and p = 10 is already the optimum that matters**. With identical generic modules the intrinsic curve is a
flat plateau over p = 9..11 (6.4–6.7e-4, the ±2e-5 zigzag is PR117-module quality, not geometry) and falls off at p ≤ 8 and
p ≥ 12; with the best annealed modules available p = 10 leads by ≥ 4e-5 over every other p. More important: #325's bit root
7.7028e-4 is only 2.44e-6 (0.32 %) below the complex cap 7.72714e-4 (κ at the cap 7.721177e-4 vs 7.696840e-4), so no cube
size can gain more than +2.4e-6 in κ; p = 9 or 11 would have to close a 4.0e-5 / 4.5e-5 gap AND then be capped at the same
value as a capped p = 10. To beat p = 10, p = 9/11 would need a native anneal of their modules (28-/45-input pair module and
7-/9-input all-but-one module) against the #325 design plus their own design/orientation search, worth at most the p = 10
anneal gain scaled (+1.3e-4 on 6.5e-4 generic ≈ 7.8e-4 — which would also hit the cap), i.e. the best case is a tie at the
cap after a full re-anneal costing the same effort as the p = 10 campaign; p = 8 (6.50e-4 best) and p ≥ 12 (≤ 7.26e-4 with
foreign-design annealed modules, generic ≤ 6.30e-4 for 13/14, worse R/v and J/v) are dead. Recommendation: **dead as a
lever** — stay at p = 10 and spend effort on the last 2.4e-6 to the complex cap (or on the complex side), not on p. If a
second base word is ever wanted for diversity, p = 11 (not 9: 60-replica bank incompatible, m = 90 needs 90 replicas) is the
only candidate, starting from the restricted gen4 modules (7.295e-4).
