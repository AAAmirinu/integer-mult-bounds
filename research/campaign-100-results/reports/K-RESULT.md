# K-packing: kernel-entrance packing at scale (RADICAL-IDEAS 13, 67, 71) on the #325 word

Setup. /tmp/radical/K/pkg = #320's transcript-stage package with #325's word installed (bitword/selected/bit,
all five producer data files, and #325's producer .py files -- #325 changed paired_cube_bit_word.py (cube
orientation, symmetric G plane) and make_physical.py (Kuhn augmentation), so both were copied). Discovery pipeline
re-run in record mode (/tmp/p10b_run.py): descent 480 gates phi -637.17; target squares 120 groups phi -456.00
(same counts as on #320's word); dump at `target`; census: 6,900 plain helpers (dims 1,2,3,5,6,8,10,12; #320's word
had 6,960, dims 1-15); lines.py 5: 18,453 lines; planes.py 15: 7,045 rank 2-10 intersections. H.pkl/L.pkl/P.pkl in
/tmp/radical/K. Pools total 369 entrance lines ever used; a packing has ~1,340 entries, rank ~1,455 (trim5 -> 1,450).

The README's "16 seeds x 400 restarts" conflates two tools: closure_pack.py is ONE noisy greedy pass per SEED
(11 s locally, 16-25 s on a Daytona CPU), the 400-restart loop belongs to the older pack_restarts.py (families).
So "restart" below = one closure_pack pass with a fresh seed. Library form: /tmp/radical/K/coll/packlib.py
(reproduces closure_pack.py bit-for-bit: seed 5, NOISE 0.3 -> phi -2379.780 both ways); driver coll/run_pack.py
(modes plain / tabu / learned); registry of the 35 sandboxes: registry.json; per-sandbox K5.json + phi lists in
results/; local baseline packings baseline/K_<seed>.json; local noise sweeps noise/out_*.json; collect.py -> collect.txt.

## Baseline: 400 restarts of the README recipe (EXCLUDE 7 sinks, ORDERS 4, NT 3, NOISE 0.3, seeds 1..400), local

best phi -2388.990 (3 of 400 seeds), mean -2383.24, sd 1.23, worst -2379.25; only 15 distinct phi values in 400
runs; 249/400 land on the modal packing -2383.710. Best-of-first-k: k=1 -2379.31, 16 -2384.60, 100 -2388.99,
400 -2388.99. (So on this word the README's one-seed number would be about -2380 to -2384 and a 16-seed best
-2384.6; the whole 400-seed window is 9.7 phi wide.) Note: the closure on #325's word is worth phi -2384 against
-1,601 on #320's word -- #325's word has far more rank-1 entrance structure (1,289 rank-1 entries vs 1,047 total).

## Daytona: 35 sandboxes x 2.25 h (plain 20 / tabu 10 / learned 5), then 10 re-purposed to high noise x 1.5 h

Total 11,962 plain/learned restarts + 4,569 tabu iterations + 824 local high-noise restarts (+72 sweep runs).

| method | NOISE | sandboxes | restarts | best phi | mean phi | distinct outcomes |
| --- | --- | --- | --- | --- | --- | --- |
| plain | 0.1 | 4 | 1,992 | -2388.990 | -2383.57 | 10 |
| plain | 0.2 | 4 | 1,467 | -2388.990 | -2383.53 | 12 |
| plain | 0.3 | 3 | 1,089 | -2388.990 | -2383.50 | 11 |
| plain | 0.4 | 3 | 1,067 | -2389.883 | -2383.58 | 19 |
| plain | 0.5 | 3 | 1,032 | -2389.883 | -2383.56 | 26 |
| plain | 0.6 | 3 | 1,207 | -2392.809 | -2383.72 | 25 |
| plain, all <= 0.6 | | 20 | 7,854 | -2392.809 | -2383.6 | 31 (5,677 of 7,854 = modal -2383.710) |
| tabu (pivot-level, T=3, ruin 1%) | 0.1-0.6 | 10 | 4,569 iters | -2383.710 (= its seed start) | -2350.5 | walk never improves |
| learned (fit every 200, top 10%, beta 0.15-0.6) | 0.2-0.4 | 5 | 1,662 | -2389.883 | -2383.5 | 5-13; mean not shifted |
| plain high noise | 2 / 3 / 5 / 8 / 12 | 2 each | 2,446 | -2393.886 (3, 5, 8) | -2385.4 | 44-81 per sandbox |
| plain high noise, local | 10 / 20 | 2 cores | 812 | -2393.886 (both) | -2385.2 | 112 / 121 |

Best packing of the whole experiment: phi -2393.886 (1,336 entries, rank 1,455; trim5 -> 1,332 entries, rank 1,450,
phi -2393.142), reached independently by 5 series (NOISE 3, 5, 8 on Daytona; 10 and 20 locally), 9 hits in 3,246
high-noise runs (P ~ 0.3 % per restart), never beaten in the last ~1.5 h on 12 series: a hard plateau. Saved as
/tmp/radical/K/best_K5.json; frozen with build_shared_kernel_selection.py -> kernel-selection_best.json
(delta {1: +2591, 2: -531, 3: -915, 4: +50, 5: -52, 6: -12, 7: +6, 8: +7, 10: -20}).

Versus the single-400-restart baseline (-2388.990): +4.9 phi (+4.7 after trim5). Versus the modal packing: +10.2.
Versus #320's "25 phi seed-to-seed spread": the entire observed range across ~16,000 runs is 22 phi
(-2371.6 worst at NOISE 30 to -2393.9), and the improvement from 100x more restarts is 4.9 phi. Restarts at
NOISE <= 0.3 are nearly wasted: 10-15 distinct outcomes, best -2388.99 found by seed ~100 and never again
improved in 4,500 further runs. The ONLY lever that moved the best was the noise amplitude (the README's 0.3 is
far too timid: NOISE 3-20 doubles the width of the outcome distribution and reaches -2393.9 within ~200 runs).

Structure of the spread (why tabu and learning cannot help): the best (-2393.7) and the modal (-2383.7) packings
share 1,222 of ~1,340 entries and 1,277 of 1,339 pivots and use exactly the same 369 lines; the phi difference is
confined to 12 lines (largest single line +5.39, next +2.87, +2.70, ...). Ruin-and-rebuild without tabu returns
the identical packing (8/8 iterations, to 1e-12): each entry is the unique positive closure of its pivot on its line,
so forbidding an entry (pivot-level tabu, with aspiration against the line's best value) just loses its ~2.5 phi and
nothing replaces it (mean -2350.5 = -2383.7 + 13 tabu entries x 2.5); line-level tabu is worse (-1,800). Tabu is
dead on this landscape. The learned restart distribution (per-line and per-pivot inclusion frequencies of the top
10 %, used to bias heap priority and the in-line cost order) does not shift the mean at beta 0.15-0.6 and found
nothing beyond what plain NOISE 0.4 found, because the top 10 % at NOISE <= 0.4 are all the same modal packing.

## phi -> kappa on this word (and why none of it matters here)

Pricing: price_sel.py applies a selection's exact histogram delta (same accounting as trim5.py; verified equal to
the kernel_transform output for two packings) to the parity+descent+target word (pdt.pkl) and prices it with the
#325 chain (J's price_hist.py, deficit 2040 fixed, W_lit moves); pdtk_best.pkl is the full kernel-stage word built
with build_word_stages.py from kernel-selection_best.json and prices identically.

- parity word (#325 as shipped): J 483,908.5, bit root 7.702769e-4, kappa 7.69684039e-4 (bit-binding).
- + descent + target: J 482,814.9, root 7.718733e-4, kappa 7.71277969e-4 (+1.594e-6 for 1,093.6 phi = 1.46e-9
  kappa/phi here, not 6.3e-10: the moment root is steeper at this ledger).
- + kernel, baseline best packing (phi -2388.4 trimmed): root(bit) 7.753707e-4, kappa 7.72117724e-4.
- + kernel, best packing (phi -2393.1 trimmed): root(bit) 7.753777e-4, kappa 7.72117724e-4 -- identical.
- + kernel, a one-seed packing (phi -2379.4): kappa 7.72117724e-4 -- identical.

The complex side root b = 772714351296671e-18 (math_check.py / PROOF.md in both #320 and #325) caps the chain at
kappa 7.7211772e-4; on #325's word the bit root crosses b after only ~400 kernel entries (phi ~ -600: prefix 200
-> kappa 7.71925e-4 bit-binding; prefix 400, phi -841 -> root 7.73102e-4 > b, capped). Everything beyond -- the
remaining ~1,800 phi of the packing, the 4.9 phi from 16,000 restarts, and the whole 22 phi window -- is worth
exactly 0 kappa under the current certificate. For the record, in bit-binding units 4.9 phi ~ 7e-9 kappa and the
whole window ~ 3e-8.

## Verdict

Dead. 100x more restarts moved the kernel packing by 4.9 phi over a single 400-restart run (and 10 phi over the
modal one-seed result), far inside the 25 phi spread #320 quoted; tabu (pivot- and line-level) never improved on
its starting seed, and the learned restart distribution matched plain restarts. The one actionable finding is
mechanical: raise closure_pack's NOISE from 0.3 to ~5 (outcome space 15 -> 100+ distinct packings, best -2393.9
instead of -2389.0 within ~200 restarts), and the exact structure (369 lines, 12 contested lines) suggests a
small exact optimisation would close the last few phi. But on #325's word the kernel stage is already capped by the
complex-side root (kappa 7.7211772e-4 from ~400 entries on), so no packing improvement can move kappa until the
complex certificate (b = 7.727e-4) is raised -- that, not packing, is the binding constraint for this word.
All 35 sandboxes deleted (registry.json, deleted: true).
