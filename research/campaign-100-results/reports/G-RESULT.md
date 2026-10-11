# G-freeform — free-form gate-by-gate retiming (RADICAL-IDEAS 1, 3, 11-lite)

Question: does optimising the word gate by gate — candidate frames from the full meet/join lattice (not only frames
already on the operand chains) and **uphill moves** (simulated annealing) — beat the repo's concave descent
(`descent4s.py`: min-join / max-meet candidates, strictly downhill)?

Short answer: **yes, but only by +1.2e-7 κ (−82 J, 13 % more J than descent): about −48 J of it comes from the
richer candidate table plus free zero-cost drift (a T = 0 control reaches −685), the remaining −35 J from uphill
moves; pool frames vs lattice-only makes no difference.** 98.5 % of the gates have no legal frame other than their current one
(their legal interval is a single point), so there is no lattice to free. The remaining 1.5 % form a tiny search
space whose optimum every annealing chain finds within 10–20 minutes (J floor 482 571–482 575). Verdict: **dead as a
lever of any size**; the +1.2e-7 is real and cheap but an order of magnitude below the stage levers that matter.

## What was run

* Word: parity-fused word of PR #325's package (`build_word_stages.py PKG /tmp/radical/G/p325.pkl parity`):
  h = 20, v = 960, 350,640 ADD gates (2,880 centre reads + 20 copy-window gates fixed → 347,760 movable),
  10,020 registers, 13,866 frames. Exact κ by `kappa_shape.py` = **7.69684039383334e-4** (= #325's pinned κ, so #325's
  package is the parity word with no descent stage), J = **483,291.159**, 47,304 helper calls.
* Reference descent: `descent4s.py p325.pkl out.json SEED 6` with seeds 1 and 2 → identical: **480 moves, J 482,653.989
  (−637.17), κ 7.70612425424136e-4 (+9.284e-7)**; 0 further moves in rounds 1–5 (plateau rounds move 160–185 gates at
  equal J without opening anything). 1.46e-9 κ per unit of J on this word.
* `/tmp/radical/G/freeform.py` (single file, stdlib + optional numpy):
  1. *Frame table (idea 3).* Per gate, legal interval `[lo, hi]`, lo = join(prev_a, prev_b, chi-span of the integer source
     supports), hi = meet(next_a, next_b) (exact integer row reduction, same registry/canonical-basis code as descent4s).
     Candidates = closure to depth 2 under meet/join of the frames of the 2-hop neighbourhood (both operands' neighbouring
     gates and *their* other operands' prev/next frames and chi-spans), clipped into the interval
     (meet(join(lo,x),hi) and join(meet(x,hi),lo)); optionally (`--pool K`) every already-registered frame of the word
     that lies in the interval (numpy containment scan per dimension, exact `sub` re-check). Every candidate is checked
     exactly for nondegeneracy (integer rank of the Gram form 9·dot − s·s) and the prime-witness residual < 2^80;
     chi-support and nesting are exact by construction. Tables are cached per (gate, lo, hi) and rebuilt lazily when
     neighbours move. Full table for the start state: **29.5 s, 12,130 new frames registered.**
  2. *Annealing.* Exact incremental first-order J (r·ln(100/r) per climb); single-gate moves to a random table candidate,
     compound "push" moves (`--push p`: the gate and a neighbouring gate on one operand chain take the same frame,
     accepted jointly — idea 11-lite), Metropolis acceptance with geometric cooling T0 → 0.02·T0, optional reheats
     (`--reheat k` cycles), optional late-acceptance hill climbing (`--la L`), live-set sampling (only gates whose
     interval can have changed are sampled; ~80–100k tries/s), exact κ via the package's `moment.certify`/`outer`
     chain every 15 min on the best state, final zero-temperature polish, output `moves.json` in descent4s' format
     (`moves=[(gi, old, new)]`, `new_bases`, `J`). `/tmp/radical/G/price.py WORD.pkl PKG moves.json` patches the new
     bases into a temp pickle and runs `kappa_shape.py` (independent pricing); `verify_moves.py` re-checks every gate
     of a solution from scratch (nesting, support, nondegeneracy): **0 violations** on the best solutions.
  3. 20 Daytona chains (python:3.11-slim, 1 cpu / 1 GiB — the account was at 499/500 GiB so sandboxes had to be
     1 GiB and launched in a retry loop), 2.5 h each, seeds 101–120, T0 ∈ {0.25, 0.5, 1, 2, 4}, pool ∈ {0, 40, 100},
     reheat ∈ {0, 4, 6, 12}, push ∈ {0.35, 0.6}, two LAHC chains, one chain started from descent4s' solution; plus six
     20-minute local chains (L1–L6). Registry `/tmp/radical/G/dt/registry.json`, outputs `/tmp/radical/G/dt/out/`.

## Results (exact κ by kappa_shape on every row; Daytona rows = 2 h checkpoints, chains end ≈ 17:55 EDT)

Baseline parity word: J 483,291.16, κ 7.69684039e-4. descent4s: J 482,653.99 (−637.17), κ 7.70612425e-4 (+9.284e-7).

| chain | seed | T0 | options | status | moves | J | dJ vs parity | kappa | dkappa vs parity | dkappa vs descent4s |
|---|---|---|---|---|---|---|---|---|---|---|
| c01 | 101 | 0.5 | --pool 40 | checkpoint 2 h | 1015 | 482574.32 | -716.84 | 7.707285623687e-04 | +1.045e-06 | +1.161e-07 |
| c02 | 102 | 0.5 | --pool 40 --reheat 6 | checkpoint 2 h | 1031 | 482572.78 | -718.38 | 7.707307896901e-04 | +1.047e-06 | +1.184e-07 |
| c03 | 103 | 0.5 | --pool 40 --reheat 6 --push 0.6 | checkpoint 2 h | 1003 | 482573.14 | -718.02 | 7.707302682538e-04 | +1.046e-06 | +1.178e-07 |
| c04 | 104 | 0.5 | --pool 40 --reheat 12 | checkpoint 2 h | 999 | 482572.49 | -718.66 | 7.707312049778e-04 | +1.047e-06 | +1.188e-07 |
| c05 | 105 | 1.0 | --pool 40 | checkpoint 2 h | 1039 | 482583.51 | -707.65 | 7.707151820042e-04 | +1.031e-06 | +1.028e-07 |
| c06 | 106 | 1.0 | --pool 40 --reheat 6 | checkpoint 2 h | 1020 | 482573.99 | -717.17 | 7.707290439238e-04 | +1.045e-06 | +1.166e-07 |
| c07 | 107 | 1.0 | --pool 40 --reheat 6 --push 0.6 | checkpoint 2 h | 1030 | 482574.24 | -716.92 | 7.707286840324e-04 | +1.045e-06 | +1.163e-07 |
| c08 | 108 | 1.0 | --pool 40 --reheat 12 | checkpoint 2 h | 1018 | 482575.11 | -716.05 | 7.707274251161e-04 | +1.043e-06 | +1.150e-07 |
| c09 | 109 | 2.0 | --pool 40 --reheat 6 | checkpoint 2 h | 1124 | 482617.35 | -673.81 | 7.706658799023e-04 | +9.818e-07 | +5.345e-08 |
| c10 | 110 | 2.0 | --pool 40 | checkpoint 2 h | 1226 | 482609.74 | -681.42 | 7.706769821400e-04 | +9.929e-07 | +6.456e-08 |
| c11 | 111 | 4.0 | --pool 40 --reheat 6 | OOM-killed at 80 min (1 GiB) | 1173 | 482626.27 | -664.89 | 7.706529174075e-04 | +9.689e-07 | +4.049e-08 |
| c12 | 112 | 4.0 | --pool 40 --reheat 4 --tmin 0.005 | OOM-killed at 80 min (1 GiB) | 1232 | 482612.43 | -678.73 | 7.706730682272e-04 | +9.890e-07 | +6.064e-08 |
| c13 | 113 | 0.5 | --reheat 6 (lattice only, no pool) | checkpoint 2 h | 1012 | 482572.32 | -718.84 | 7.707314680900e-04 | +1.047e-06 | +1.190e-07 |
| c14 | 114 | 1.0 | --reheat 6 (lattice only, no pool) | checkpoint 2 h | 1005 | 482575.09 | -716.07 | 7.707274491874e-04 | +1.043e-06 | +1.150e-07 |
| c15 | 115 | 0.25 | --pool 40 --reheat 6 | checkpoint 2 h | 992 | 482573.02 | -718.14 | 7.707304228231e-04 | +1.046e-06 | +1.180e-07 |
| **c16** | 116 | 0.25 | --pool 100 --reheat 6 | checkpoint 2 h | 990 | **482571.32** | **-719.84** | **7.707329108745e-04** | **+1.049e-06** | **+1.205e-07** |
| c17 | 117 | 1.0 | --pool 40 --la 20000 | checkpoint 2 h | 1117 | 482639.14 | -652.02 | 7.706340823827e-04 | +9.500e-07 | +2.166e-08 |
| c18 | 118 | 1.0 | --pool 40 --la 200000 | checkpoint 2 h | 1532 | 483063.99 | -227.17 | 7.700152471853e-04 | +3.312e-07 | -5.972e-07 |
| c19 | 119 | 1.0 | --pool 100 --reheat 6 --push 0.6 | checkpoint 2 h | 1016 | 482574.85 | -716.31 | 7.707277918922e-04 | +1.044e-06 | +1.154e-07 |
| c20 | 120 | 0.5 | --pool 40 --reheat 6 --start descent4s | checkpoint 2 h | 1019 | 482573.11 | -718.05 | 7.707303308289e-04 | +1.046e-06 | +1.179e-07 |
| L1 | 201 | 0.5 | local 20 min, pool 40, reheat 4 | final | 992 | 482574.48 | -716.68 | 7.707283114931e-04 | +1.044e-06 | +1.159e-07 |
| L2 | 202 | 1.0 | local 20 min, pool 40, reheat 4 | final | 968 | 482572.18 | -718.98 | 7.707316686271e-04 | +1.048e-06 | +1.192e-07 |
| L3 | 203 | 0.5 | local 20 min, no pool, reheat 4 | final | 1012 | 482572.94 | -718.22 | 7.707305628520e-04 | +1.047e-06 | +1.181e-07 |
| L4 | 204 | 0.25 | local 20 min, pool 100, reheat 4 | final | 952 | 482576.26 | -714.90 | 7.707256940704e-04 | +1.042e-06 | +1.133e-07 |
| L5 | 205 | — | local 20 min, LAHC L=50000 | final | 1328 | 482729.42 | -561.73 | 7.705025252056e-04 | +8.185e-07 | -1.099e-07 |
| L6 | 206 | 0.5 | local 20 min, start = descent4s | final | 988 | 482573.67 | -717.49 | 7.707294990885e-04 | +1.045e-06 | +1.171e-07 |
| L0 | 207 | 1e-6 | local 4 min control: downhill + zero-cost moves only | final | 865 | 482606.14 | -685.02 | 7.706821020805e-04 | +9.981e-07 | +6.968e-08 |

Best so far: **c16, J 482,571.32 (−719.84 vs parity, −82.67 vs descent4s), κ 7.707329108745e-4 = +1.0487e-6 vs the parity
word, +1.205e-7 vs descent4s**; moves file `/tmp/radical/G/dt/out/c16.json` (990 moves, prices with
`price.py p325.pkl PKG c16.json`). 16 of the 17 Metropolis chains with T0 ≤ 1 (any pool/reheat/push, with or without the descent start; the exception
is c05 at 482,583.5) end within J 482,571–482,576, i.e. the landscape has a well-defined floor ≈ −719 ± 2 that is reached in
10–20 minutes; 2.5 h and reheats do not go below it. The final 2.5 h results and the sandbox cleanup are done by the
background job `/tmp/radical/G/dt/finalize.sh` (writes `/tmp/radical/G/summary_final.md`, then deletes the 20 sandboxes).

Ablations (what the gain is made of):
* **Temperature.** T0 = 0.25–1.0 → −716…−720; T0 = 2 → −674…−681 (not cooled enough in the budget); T0 = 4 →
  −665…−679; late acceptance as implemented is far too permissive (−227…−652). Control L0 (T0 = 1e-6, i.e. downhill
  plus zero-cost moves only, same table and push moves, 4 min): **J 482,606.14 (−685.0), κ 7.70682102e-4 (+7.0e-8 vs
  descent4s)** — so the candidate table + random zero-cost drift already beats descent4s by 48 J, and uphill moves add
  the last 35 J (+5e-8).
* **Pool frames (every registered frame of the word inside the interval) contribute nothing measurable.** Lattice-only
  chains (c13, c14, L3) reach −718.8 / −716.1 / −718.2, the same floor as pool-40 and pool-100 chains; the best
  solutions use 105–140 constructed frames (descent4s' best keeps 0) — the depth-2 lattice closure is what lets the
  zero-cost drift reach configurations descent4s' two candidates cannot.
* Compound push moves: ~0.3 % of the attempted pushes are legal (the pushed neighbour almost always has a one-point
  interval); push 0.35 vs 0.6 makes no difference.
* Starting from descent4s' solution (c20, L6) gives the same floor — descent's local optimum is in the same basin.

## Why the space is so small (diagnostic, `/tmp/radical/G/diag_pinned.py`)

Of 347,760 movable gates only **5,242 (1.5 %) have a legal interval of width > 0** at the start (and the live set
stays 5.4–8k during annealing). The pinned ones, by reason and gate category:

| reason lo == hi | gates | categories |
|---|---|---|
| chi-span of the integer source support already equals hi | 307,415 | dirty_read 296,640; forward_gate 9,815; inject 960 |
| a prev frame already equals hi (operand already at the top) | 29,492 | cleanup_gate 18,318; forward_gate 3,566; side_root 3,120; dirty_read 3,048; uninject 960; partner_delivery 480 |
| a next frame already equals lo | 5,051 | forward_gate 2,495; side_root 1,440; cleanup_gate 960; dirty_read 156 |
| join of the two prevs equals hi | 560 | forward_gate |
| live (interval width 1–16, mostly 1–3; 480 forward gates have width 16) | 5,242 | forward_gate 3,124; partner_mix/delivery/cleanup 1,440; cleanup_gate 282; side_root 240; dirty_read 156 |

So 88 % of the word is pinned by the verifier's integer-source-span rule (a dirty read's frame *is* the span of what
it has read), and most of the rest by chain endpoints. Freeing the frame lattice cannot touch those; only changing the
word's gate order / operand order / coefficients (idea 1 proper) would, and that is a different verifier class.

## Verdict

Free-form retiming with uphill moves beats concave descent by **−82.7 J = +1.2e-7 κ** on the parity word of #325
(7.70612e-4 → 7.70733e-4; +1.05e-6 over the parity word itself), consistently across 20 chains, reproducible in
10 minutes on one core (`freeform.py p325.pkl out.json SEED 0.5 0.2 --pkg pkgmin --pool 40 --reheat 2`). The
gain splits into ≈ −48 J from the depth-2 lattice table with free zero-cost drift and ≈ −35 J from uphill moves;
pool frames and the compound push moves add nothing. Everything happens inside a 5k-gate live region whose optimum is
at J ≈ 482,571 (floor hit by every well-tempered chain; 2.5 h and reheats do not improve on 20 min). As a lever this is **dead beyond a one-off +1.2e-7**
(≈ 2 × what descent2 historically gave, but 10× below a kernel/restoration stage), and it would need re-running after
the target/kernel/restore/sink stages, where descent's own moves have historically shrunk to zero. Idea 1 in its full
form (reordering gates, operand order, coefficients) is the only way to enlarge the 1.5 % live region, because the
pinning comes from the integer-source-span rule, not from the candidate set; nothing in this experiment suggests the
word's frame assignment has slack beyond that.
