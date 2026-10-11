# L-design-enum: exhaustive enumeration of the cube-local design (idea 2)

Baseline: PR #325 package, κ = 7.69684039e-4 (bit root 7.70277e-4, literal stock 658800, physical R = 8100,
entrances {16: 1200}). Reproduced exactly on this machine (82 s) and in a Daytona sandbox (148 s) with
/tmp/p10job/physical_eval.py before any experiment.

Tooling written (all under /tmp/L): `pkg0/` = copy of #325 whose producer accepts **per-cube** designs
(`{'global': [...], 'cubes': {'<cube index>': [...]}}`, cube index = position in `combinations(range(10),3)`;
the original producer applies ONE design list to all 120 cubes — there was no per-cube freedom in #325);
`physical_eval_ledger.py` = physical_eval.py + per-cube attribution of every paid climb (physical register ->
role -> first node written into that role -> support -> cube; sources/targets by index) and per-cube
J = Σ 5·r·ln(100/r); `enum2.py` (frontier DP over the 15^12 designs), `mk24b.py` (all 24-node designs),
`dt_launch.py` / `dt_poll.py` (Daytona). 31 sandboxes used in two batches, all deleted.

## 1. Encoding and size of the space

* A cube has 12 "planes" (4-subsets of its 8 sources): 6 faces A(i,a) and 6 "G planes" {s_j ^ s_k = m}. The
  design gives each plane a full binary tree over its 4 members (3-bit leaves); sums are interned, so a pair
  node (unordered pair of sources) is shared by every plane that uses it. Two distinct planes meet in <= 2
  sources, so triples are never shared. The 28 pairs of the cube are 12 edges (each in 3 planes: 2 faces + 1 G),
  12 face diagonals (in exactly 2 planes: 1 face + 1 G) and 4 body diagonals (in the 3 G planes).
* Trees per plane: 15 (the (2·4-3)!! = 15 full binary trees on 4 labelled leaves, mirror images identified;
  `anneal_shape_lib.all_trees` enumerates exactly these). Per-cube design space = **15^12 = 129 746 337 890 625**
  (the DP over all of them confirms the count). Plane *order* in the list is a further 12! tie-break
  freedom (node numbering), used by the annealer's swap move.
* Nodes per cube (= distinct pairs + triples + 12 roots), exact distribution over all 15^12 designs
  (frontier DP, 29 s): 24: 11 471; 25: 820 416; 26: 2.71e7; 27: 5.63e8; 28: 8.26e9; 29: 8.93e10; 30: 7.15e11;
  31: 4.00e12; 32: 1.46e13; 33: 3.29e13; 34: 4.24e13; 35: 2.80e13; 36: 7.08e12. **#325's design has 24 nodes
  (the minimum): all 12 planes balanced, all 12 pair nodes face diagonals, each used exactly twice.** It is the
  unique all-face-diagonal design (each face and each G plane contains exactly one face-diagonal matching).
* Symmetry: under the cube's 48-element group (S3 on positions × Z2^3 bit flips) Burnside gives
  **2 703 052 593 360** design classes; under the 16-element stabiliser of position 0 (position 0 is special:
  face0 root) 8 109 150 919 650; under flips only 1.62e13. So symmetry buys a factor <= 48 — the space is
  astronomically large and exhaustive enumeration is only possible inside a node-count class
  (24-node class: 11 471 designs, enumerated completely below).
* Cube classes under the word's symmetry: **120 of 120 cubes are inequivalent.** The pair module's 36 inputs
  have 36 distinct tree signatures (depth/ancestor structure), so each cube's 3 face planes land in
  pairwise-distinct module positions; the all-but-one module has 2 input classes. Combined neighbourhood type
  (3 pair-module positions + 3 abo positions + orientation) is distinct for every cube. Orientation classes
  (cube_orient_p10.json): 68 cubes in order (0,1,2), 27 in (1,2,0), 25 in (2,0,1). Per-cube baseline J
  ranges 11 241 .. 17 237 (mean 15 030, all 120 values distinct); cube-attributed J is 75 % of the total
  (2.416e6; global/module registers 6.13e5).

## 2. Locality / additivity test (physical κ, 31 + 2 + 7 evaluations)

10 random cubes {6, 9, 12, 19, 41, 46, 50, 68, 83, 105}; for each, 3 single-cube alternatives: a1 = one plane's
tree replaced by a random other tree; a2 = all 12 trees random; a3 = same trees, plane order shuffled.
Δκ relative to 7.69684039e-4 (sandbox base reproduced to all digits); dR = extra physical registers:

| cube | a1 (one tree) | a2 (12 random trees) | a3 (order only) |
|---|---|---|---|
| 6 | −9.43e-8 (R+2) | −7.89e-7 (R+14) | +1.85e-8 (R+0) |
| 9 | −9.43e-8 (R+2) | −7.51e-7 (R+13) | +1.85e-8 (R+0) |
| 12 | −2.25e-7 (R+4) | −6.40e-7 (R+11) | +2.1e-9 (R+0) |
| 19 | +3.9e-9 (R+0) | −7.44e-7 (R+13) | +2.79e-8 (R+0) |
| 41 | −2.13e-7 (R+4) | −8.18e-7 (R+14) | +1.23e-8 (R+0) |
| 46 | −9.43e-8 (R+2) | −8.15e-7 (R+14) | +1.23e-8 (R+0) |
| 50 | −1.04e-7 (R+2) | −6.46e-7 (R+11) | +1.23e-8 (R+0) |
| 68 | −2.03e-7 (R+4) | −5.62e-7 (R+10) | +1.3e-8 (R+0) |
| 83 | +1.08e-8 (R+0) | −8.18e-7 (R+14) | −1.4e-9 (R+0) |
| 105 | 0 (R+0) | −7.10e-7 (R+12) | +2.0e-9 (R+0) |

Every extra physical register costs ≈ 5e-8 (dR dominates); the only positive single-cube changes are
order shuffles / register-neutral tree swaps worth 2e-9 .. 2.8e-8 (0.0003–0.004 % of κ).

Joint application of the best single-cube changes:

| joint design | predicted (sum of singles) | measured | ratio |
|---|---|---|---|
| top 3 (c19_a3, c6_a3, c9_a3) | +6.48e-8 | **+1.56e-8** | 0.24 |
| all 9 positive changes | +1.166e-7 | **+5.96e-9** | 0.05 |

**Not additive.** The ledger attribution shows why: a single-cube change touches the climbs of 10–18 *other*
cubes plus the global (module/gauge) registers through the carrier matching (arcs) and the gauge chains.
Example c19_a3: ΔJ(cube 19) = −1015, ΔJ(other cubes) = +380, ΔJ(global) = +538, total −96. The order-shuffle
"gains" are redistributions of climbs that other cubes partly undo when applied together.

What *is* exact: κ is a linear functional of the total first-order ledger J (five-stage-weighted
Σ 5·r·ln(100/r) over paid climbs). Over the 7 ledger-instrumented evaluations (c6_a2, c9_a2, c12_a1, c41_a1,
c19_a3, c6_a3, c83_a1; ΔJ from −96 to +2721) the least-squares slope is Δκ = −2.901e-10 · ΔJ_total and every
point is reproduced to 3–4 significant digits (e.g. −7.893e-7 vs −7.892e-7, +2.783e-8 vs +2.788e-8). So J_total
is an exact proxy, but J_total is not a sum of independent per-cube terms.

## 3. Exhaustive pricing of the 24-node class (11 471 designs, 96 physical runs, 20 sandboxes)

Each run installs a different 24-node candidate into each of the 120 cubes (120 candidates per run) and the
per-cube ledger prices each candidate in its cube (Δregisters, ΔJ_cube relative to the same cube's baseline).
All 11 471 candidates were priced. Result: **exactly one candidate (index 10542 = the #325 design, run e87
cube 102) has Δregisters = 0 and ΔJ_cube = 0; all 11 470 others add 2–14 physical registers per cube**
(distribution: +2: 2, +3: 30, +4: 172, +5: 376, +6: 1545, +7: 2166, +8: 3993, +9: 1645, +10: 1109, +11: 250,
+12: 157, +13: 19, +14: 6) and ΔJ_cube >= +108 (mean +221 at +3 registers, +1467 at +8, +3049 at +14).
Cross-check with the virtual producer (--solve-matching, 27 s): any single non-baseline 24-node candidate in one
cube loses exactly 8 carrier arcs (R 9060 -> 9068, arcs 6020 -> 6012) — the face-diagonal pairs are the only
pair nodes whose coordinate cover (5 of 6 cube coordinates) gives frames that admit the arcs; edge pairs
(cover 4) and body-diagonal pairs (cover 6) do not. Whole-word runs with 120 changed cubes: κ 7.219e-4 ..
7.408e-4 (−3.7 % .. −6.2 %), R 8673 .. 9060.

Best design from the enumeration = the baseline itself: κ = 7.69684e-4, gain 0.000 %. The only improvements
found anywhere are the non-additive order-shuffle effects: best single +2.79e-8 (+0.0036 %), best joint
+1.56e-8 (+0.0020 %), i.e. at the level of annealer tie-break noise, and C-evolution's population search
already samples this move.

## Verdict

Dead as a global optimiser, but it closes the question. The cube-local design of #325 is **exactly optimal
within the node-minimal class** (unique 24-node, all-face-diagonal design; every one of the other 11 470
24-node designs and every random tree change costs >= 2 physical registers ≈ 1e-7 each), and the per-cube
cost is **not additive** (joint gain 5–24 % of the sum of single-cube gains; each single-cube change
perturbs 10–18 other cubes through the arc matching), so exhaustive per-cube search cannot be a valid global
optimiser even in principle. The one reusable product is the ledger proxy: κ is linear in the five-stage
ledger J to 4 digits (slope −2.90e-10 per unit of 5-weighted J), so any future search can be scored by the
ledger J without the moment certificate. Remaining design freedom (plane order, register-neutral tree swaps)
is worth <= 3e-8 and is already covered by the annealer's swap move; the design should be considered frozen
and effort moved to the modules / matching, which is where the 8-arcs-per-cube effect actually lives.
