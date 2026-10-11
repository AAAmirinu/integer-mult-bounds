# Radical idea C (63/69/73/74): population search over the p = 10 design on PR #325's word

Base: PR #325 package, physical kappa = 7.696840e-04 (reproduced locally with DESIGN "none" on the package copy /tmp/radical/C/base/pkg325, before and after the knob patch). Plain annealing reference on #315's word: +0.0046%.

## What was run

- 30 Daytona sandboxes (python:3.11-slim, 1 cpu, 3 GB), launched 15:00, polled every 15 min (poll.py: migrant / archive / observation exchange), stopped ~17:35 EDT. One physical_eval = ~170 s on a sandbox (76-130 s locally).
- evolve.py (15 islands, seeds 100-114): (mu+lambda) = (8+8), tournament-3 parents, uniform per-plane crossover (p=0.8, order from one parent) + 1-3 mutate_local steps (p=0.7); top-4 global elites injected every generation as migrants.
- elites.py (8 workers, seeds 200-207): MAP-Elites, descriptor (R // 10, entrances // 10), mutation only (1-3 steps), parent uniform over cells (25% best cell); global archive merged each poll.
- bo.py (7 workers, seeds 300-306, ~1 h): GP/EI over IMB_PLAIN in 5..12, IMB_TRIAL_A in [1e-4, 5e-3] (log), tiering key {dim, asc, late, early, dimlate, flat}, bank-parity drop {last, first, maxdim, mindim, earlydonor, latedonor}, recipient ranks {17, 16-17, 17-18, 16-18}; observations shared between workers. Knobs are read from the environment by the patched producer copy (paired_cube_bit_word.py PLAIN / select_gauges trial_a, make_physical.py tiered / parity / --ranks).
- order.py (the 7 BO sandboxes repurposed at 16:05 after BO converged): (8+8) evolution of the plane creation order only (OX crossover, swap / insertion mutation) seeded from the best design.

## Results

| method | evaluations (failed) | best kappa | gain over 7.69684e-4 |
|---|---|---|---|
| evolve | 780 (0) | 7.701695e-04 | +0.0631% |
| elites | 460 (0) | 7.701695e-04 | +0.0631% |
| bo | 147 (0) | 7.697107e-04 | +0.0035% |
| order | 308 (0) | 7.701695e-04 | +0.0631% |
| all | 1695 (0) | 7.701695e-04 | +0.0631% |

Distinct kappa values seen: 453. Most frequent values: 7.701695e-04 (+0.0631%, x423), 7.701632e-04 (+0.0623%, x4), 7.700752e-04 (+0.0508%, x2), 7.699553e-04 (+0.0352%, x2), 7.699512e-04 (+0.0347%, x14), 7.699451e-04 (+0.0339%, x3).

### Top 3 designs (all three on the same plateau; re-priced locally with /tmp/radical/C/physical_eval.py, knobs at default)

1. kappa(sandbox) = 7.701695e-04, kappa(local) = 0.000770169498765529, R = 8100, entrances = {'16': 1200}, literal stock = 658800, found by evolve_114; file best/top1.json; change vs #325 design: pos0: ['G', 1, 2, 1]; pos2: ['A', 2, 1]; pos5: ['A', 0, 0]; pos8: ['A', 1, 0]
2. kappa(sandbox) = 7.701695e-04, kappa(local) = 0.000770169498765529, R = 8100, entrances = {'16': 1200}, literal stock = 658800, found by evolve_114; file best/top2.json; change vs #325 design: pos0: ['G', 1, 2, 0]; pos8: ['A', 2, 0]; pos9: ['A', 2, 1]; pos11: ['A', 0, 0]
3. kappa(sandbox) = 7.701695e-04, kappa(local) = 0.000770169498765529, R = 8100, entrances = {'16': 1200}, literal stock = 658800, found by evolve_100; file best/top3.json; change vs #325 design: pos0: ['G', 1, 2, 1]; pos2: ['A', 2, 1]; pos5: ['G', 0, 1, 0]; pos6: ['A', 0, 0]; pos8: ['A', 1, 0]

The simplest plateau member is the single transposition found first by elites_200/203 at their first mutation (best/top1_transposition.json: move ['A', 0, 0] from position 0 to position 11, so ['G', 1, 2, 0] is created first); local re-price 7.701695e-4, parity fusion 361920 ADDs / 410370 records vs 350640 / 399140 on #325.
### BO over the producer knobs (idea 69)

141 distinct knob settings priced (0 failed), shared between the 7 workers. Only two knobs move kappa at all:
- PLAIN (plain-span threshold, 8 in the producer): PLAIN 6: -0.0187%, 7: -0.0061%, 8: 0, 9: +0.0021%, 10/11: +0.0035%, 12: +0.0063% (BO only sampled 5..12; locally PLAIN 14 = PLAIN 12 and PLAIN 16 collapses to 7.4438e-4 with entrances 480).
- the tiering key of the carrier matching: 'dim' (#325) and 'dimlate' are identical, 'late' -0.006%, 'flat' (plain Hopcroft-Karp) -0.17%, 'asc'/'early' -0.21%.
trial_a (select_gauges, 1e-4..5e-3), the bank-parity drop policy (no pair is ever dropped on this word, dropped = 0) and the recipient ranks ({17}, {16,17}, {17,18}, {16,17,18}) never changed kappa within a (PLAIN, tier) group: 0 of 49 groups had more than one distinct value (to 1e-18).
Composition with the best design (local): top1 + PLAIN 12 = 7.701858e-4 (+0.0652%), top1 + PLAIN 10 = 7.701637e-4, top1 + PLAIN 14 = 7.701858e-4.

### The +0.063% plateau

The best value 7.701695e-4 is reached by moving a G plane to the front of the design list (the #325 list creates ['A', 0, 0] first): in the 308 order-island evaluations (trees unchanged), 214 of the 248 permutations with a ['G', 1, 2, *] plane first sit exactly on the plateau, the rest fall to 7.69908e-4 or below, and no permutation with an A plane first exceeds 7.69955e-4. R, entrances and literal stock never move (8100 / {16: 1200} / 658800) - the gain is histogram shape through the node-interning / compile order. Five plateau designs also carry one neutral tree change; every tree change that was not neutral lost between 0.0008% and 6% (the (R, entrances) archive of MAP-Elites filled 20 cells, all of them below the base except the base cell). Nothing beat the plateau in the ~1250 evaluations after it was found at evaluation 2-8 of three independent workers.

## Verdict

Population methods did beat plain annealing on this word: +0.0631% over #325 (+0.0652% with PLAIN = 12), reproduced locally, vs +0.0046% from annealing on #315's word. But the gain is not a population effect: it is one coordinate (plane creation order) that the annealer's own swap move covers, found by three independent workers within their first 8 evaluations and then reached by 423 of 1695 evaluations; crossover (idea 63), MAP-Elites (73), the island exchange and the order-only islands (74-style) added nothing beyond it in ~1250 further evaluations, and BO (69) only found PLAIN (+0.0035..0.0063%) and that the tiering must stay 'dim'. Verdict: promising as a word (best/top1_transposition.json is a legal design - a reordering of #325's list - worth +0.063%, +0.065% with PLAIN = 12 in paired_cube_bit_word.py); dead as a methodology claim - the design space (12 planes x 15 trees + their order) plateaus within ten evaluations and every operator then stalls, so the next lever is a larger genome (cube_orient_p10.json: 120 cubes x 6 orientations, untouched here) rather than a better optimiser over this one.

## Files
- /tmp/radical/C/{common,evolve,elites,bo,order,poll,launch,finalize}.py, run_c.sh; registry.json (30 sandboxes, all deleted), poll.log / poll_history.jsonl (10 cycles), sb/<worker>/log.jsonl (every evaluation), evolve_pool.json / elites_pool.json / sb/bo_*/obs_out_final.json (designs and observations), best/top{1,2,3}.json, best/top1_transposition.json, base/pkg325 (package copy with the env-knob patch: IMB_PLAIN, IMB_TRIAL_A, IMB_TIER, IMB_PARITY, IMB_RANKS).
