# I-matching: is the (carrier / reuse) matching a lever? — RESULT

Ideas 34, 40, 44, 74 of RADICAL-IDEAS.md. Baseline: PR #325 package (p = 10), κ = 7.69684039383334e-4,
reproduced first through the unmodified copy at /tmp/radical/I/pkg with /tmp/p10job/physical_eval.py (DESIGN 'none', 77 s).
All numbers below are exact physical κ from that pricing path (physical_eval_I.py = physical_eval.py + saving the arcs/pairs).
Total: 202 physical evaluations (15 + 6 Daytona sandboxes, all deleted) + ~70 local virtual-ledger searches.

## 1. Where the matching is chosen (two different matchings)

**(A) Carrier matching** — `bitword/producer/paired_cube_bit_word.py::compile_word`, lines ~498–512, frozen in
`data/arcs_p10.json` (`[[node-1, usecode], ...]`, usecode = `['op', target-1, slot]` or `['root', j]`).
Bipartite graph **donors × uses**: left = the 11,460 addition nodes x (in `order`); right = the 26,540 *uses* u = (target t,
operand y) of every node; edge x→u iff y ∈ args[x], t is later than x in `order` (or a root), and `useann[u] ⊆ initial[x]`
(frame containment). An arc x→u lets x's register carry y into t: R = donors + q − |arcs| (each arc saves one register), and
the ledger moves −[h−rd] −[rv] −[rt−rv] +[rt−rd]; also `ann[x]` is joined with `ann[t]`, which shifts ranks upstream (second
order). Plain Hopcroft–Karp in the adjacency order; `regenerate --solve-matching` re-solves it from scratch, so every
physical_eval run goes through this code.
Graph facts (p = 10): 8,580 edges only; 6,020 donors have ≥ 1 edge and **every one of them is matched in every maximum
matching** (|max matching| = 6,020; 6,060 eligible uses, 40 left over). The only freedom is *which use* each of the 2,280
donors with 2–4 edges takes; 960 arcs go to root uses; HK gives 820 targets with both operands carried (indeg 2).

**(B) Reuse (compensated pair) matching** — `make_physical.py` lines 169–174 (`tiered(adj, ...)`, README items 3–4).
Bipartite graph **recipients × donors**: 960 rank-17 gauge recipients × 1,096 eligible donor roles (ungauged, non-root,
non-source, last op before the read, end frame inside the gauge frame), 19,616 edges. Donor end-frame dimension e ∈
{3 (480 donors), 7, 8, 9, 11, 12, 13, 14, 15, 17 (436)}. Tiered augmentation = matroid greedy by e: matches all 616 donors
with e ≥ 7 plus 344 of the 480 e = 3 donors (all 960 recipients). Plain HK (#315 style) matches only 324 e = 17 donors.

## 2. What was run and the exact numbers

### (a) Random maximum carrier matchings (idea 40-lite) — shuffle donor order + adjacency, HK; 40 seeds (+10 joint with random reuse)
| | n | min | median | max |
|---|---|---|---|---|
| carrier random (`cr_s1..50`) | 40 | 7.694633e-4 (−0.0287%) | 7.695281e-4 (−0.0203%) | 7.695831e-4 (−0.0131%) |
| carrier random + reuse tiered-random (`joint_`) | 10 | 7.694816e-4 (−0.0263%) | 7.695308e-4 (−0.0199%) | 7.695713e-4 (−0.0146%) |
sd across random carrier matchings = 3.05e-8 (0.004%). **All 50 random maximum matchings are below #325's HK matching**: the
adjacency-order HK happens to be a good one (it is exactly the min-Σrt matching, see (b)).

### (b) Min-cost matchings with first-order donor costs
κ-exact weights: finite differences of the pricing block (moment.certify on the baseline five-stage histogram, 100 climbs per
rank so the integer width is exact) give droot/climb = −2.906e-10 · r·ln(100/r) to within 0.02% for every r = 1..20
(`kappa_weights.json`). So **J(r) = r ln(100/r) is the κ-exact weight**; no separate run needed.
Per-edge cost of arc (x,u) = −[J(h−rd)+J(rv)+J(rt−rv)−J(rt−rd)] with ranks from the HK compile; solved with
`scipy.sparse.csgraph.min_weight_full_bipartite_matching` (every edge-bearing donor is coverable, so a full matching exists).
| variant | κ | vs #325 | virtual J100 (ledger Σ H[r]·J(r)) |
|---|---|---|---|
| #325 HK (baseline) | 7.69684039383334e-4 | 0 | 470883.1 |
| **`cw_J` min-cost, κ-exact weights** | **7.69746927489015e-4** | **+6.29e-8 (+0.0082%)** | 470866.8 (optimum) |
| `cw_J` self-consistent, 2 / 3 iterations | 7.69746927489015e-4 | +0.0082% | 470866.8 |
| `cw_J` with m = 60 (virtual) weights | 7.69746927489015e-4 | +0.0082% | 470866.8 |
| `cw_J` + noise 0.05 / 0.5 (30 samples) | 7.697001e-4 … **7.697572e-4** | +0.0021% … **+0.0095%** (best `cwJn_s20`) | 470919–470972 |
| prefer low-rank targets (`cw_rt`), root uses, low position, large use frame | 7.69684039383334e-4 | 0 (identical to HK) | 470883.1 |
| prefer high-rank targets (`cw_-rt`) / `-dim` | 7.694531e-4 | −0.030% | 471150.9 |
| anti-J (`cw_-J`, worst first-order) | 7.693661e-4 | −0.041% | 471170.6 |
| J + triangle bonus β = 0.5 / 2 / 5 | +0.0082% / +0.0022% / +0.0022% | | |
Local search on the exact virtual ledger (`ledger_search.py`, 2-swap moves, 0.03 s per evaluation): from HK, from `cw_J`, and from
26 random matchings it **always converges to J100 = 470866.797** (22 distinct matchings; from HK it reproduces `cw_J`'s arcs
byte-for-byte). 19 of those distinct virtual-optimal matchings were priced physically: **all give κ = 7.69746927489015e-4 to 15
digits**. The virtual ledger optimum is 16.3 J units below HK; random matchings are +120…+200 above. Over all 102 carrier
variants corr(virtual J100, κ) = −1.000 (slope −1.29e-9 κ per J unit; −0.61 within the random cloud alone, where the reuse
e-histogram and the descent layer add ±0.003% scatter).

Reuse tier boundaries (idea 74) — `make_physical` tiers with custom thresholds (carrier = HK):
| tiers | e=3 donors matched | κ | vs #325 |
|---|---|---|---|
| exact e tiers (#325), {≥7}, {17,12,8,7} | 344 | 7.69684039383334e-4 | 0 |
| {≥8}, {17,8}, {15,8}, {17,15,8} | 350 | 7.696754e-4 | −0.0011% |
| {≥12}, {≥14}, {17,14} | 404 | 7.695815e-4 | −0.013% |
| {≥15}, {17,15} | 414 | 7.695194e-4 | −0.021% |
| {≥17} | 448 | 7.692897e-4 | −0.051% |
| plain HK (#315 style) + 9 random HK | 480 | 7.682287e-4 … 7.683044e-4 | −0.189% … −0.179% |
Min-cost reuse matchings with per-edge terms (e + time gap, ± last-op time) all equal the tiered result exactly. Any
per-donor weight gives the matroid-greedy = tiered matching, so no cross-entropy over boundaries can beat {≥7 first}: the
boundary space is exhausted by the 12 runs above. The tier effect is −0.18% for plain HK, i.e. the whole "tiered" part of
#325's gain is confirmed and is already maximal.

### (c) Spectral / short-cycle criterion (idea 34) — on the carrier reuse graph (operand edges ∪ arc edges, 12,420 nodes, one component)
Over the 45 random carrier matchings (graph_stats.py; `spectral_rows.json`):
| statistic | range | corr with κ (random) | corr with κ (all 73 carrier variants) |
|---|---|---|---|
| algebraic connectivity λ₂ (normalized Laplacian) | 0.0202448–0.0202543 | −0.11 | −0.10 |
| triangles | 5,240–5,260 | **+0.79** | **+0.97** |
| 4-cycles | 2,797–2,834 | +0.65 | +0.94 |
| targets receiving both operand arcs (indeg 2) | 800–820 | +0.79 | +0.97 |
| Σ target ranks of arcs | 90,960–91,000 | −0.79 | −0.97 |
| arc-forest mean depth | 1.558–1.565 | −0.22 | +0.42 |
The Fiedler value is constant to 5e-7 and uninformative. Short cycles correlate with κ in the **opposite** direction from
idea 34: every arc x→t with y ∈ args[x] ∩ args[t] closes a triangle, and *more* triangles (both operands of a target carried,
lower target ranks) is better. The right criterion is the first-order ledger (min Σ J), which HK and `cw_J` already maximize
on indeg-2 (820). Spectral idea: dead.

### (d) Steiner-like constraint (idea 44) — each target (or each value) covered by at most one arc
| constraint | |arcs| | R (virtual) | κ |
|---|---|---|---|
| none (#325) | 6,020 | 9,060 (physical R 8,100) | 7.69684e-4 |
| ≤ 1 arc per target (3 orderings) | 5,220 | 9,860 (physical R 8,900) | 7.2233e-4 … 7.2247e-4 (**−6.15%**) |
| ≤ 1 arc per value (3 orderings) | 4,580 | 10,500 (physical R 9,540) | 6.8981e-4 … 6.9010e-4 (**−10.4%**) |
Duplicate carriers are exactly the valuable arcs (the 820 indeg-2 targets). Forbidding them shrinks the matching and costs
registers. Dead.

### Reuse matching re-pairings
40 distinct tiered-random pairings (each replaces ~100 of the 960 donors within the tiers and permutes all pairs) give κ =
7.69684039383334e-4 **identical to 15 digits**: the physical price depends only on the donor e-histogram, not on who pairs
with whom. There is nothing to search inside the tiered class.

## 3. Verdict
**The matching is not a lever worth 0.1%.** The whole reachable range is −0.19% (plain HK reuse, i.e. #315) to **+0.0095%**
(κ = 7.697572e-4, `cwJn_s20`) over #325; the deterministic, reproducible gain is **+0.0082%** (κ = 7.69746927489015e-4) from
replacing Hopcroft–Karp in `compile_word` by the min-cost full matching with the κ-exact first-order weights
J(r) = r ln(100/r) (`scipy...min_weight_full_bipartite_matching`, or equivalently the 2-swap local search on the exact virtual
ledger, which converges to the same unique optimum value from every start). That gain is free, provable (still a maximum
matching, R unchanged at 8,100, stock 658,800, 1,200 rank-16 entrances, no dropped pairs) and should be additive with design /
module changes, but it is 12× below the 0.1% bar. The reuse (tiered) matching of #325 is already optimal in its class (every
boundary change loses, every per-edge cost reproduces it, re-pairings are κ-invariant), the spectral criterion is
uninformative (λ₂ constant, short cycles correlate the wrong way), and Steiner constraints are catastrophic (−6%/−10%).
Promising only as a free +0.008% add-on; dead as a research direction.

## Artifacts (/tmp/radical/I)
- `pkg/` = #325 package copy with the pluggable producers (`bitword/producer/matchlib.py`, patched `paired_cube_bit_word.py`
  and `make_physical.py`; env `IMB_MATCH` JSON selects the mode; default behaviour = #325 byte-identical, baseline reproduced).
- `best_arcs_p10_cwJ.json` (κ 7.69746927489015e-4, the virtual-ledger optimum) and `best_arcs_p10_cwJn_s20.json`
  (κ 7.6975717e-4): drop-in `data/arcs_p10.json` replacements (then re-pin). To regenerate: `IMB_MATCH='{"carrier":{"mode":"weighted","w":"J"}}'`.
- `results/`, `results2/` (per-run json + `.arcs.json` + `.pairs.json` + stats), `analysis.txt` (all 202 κ values),
  `spectral_rows.json`, `kappa_weights.json`, `ledger_search.py` (0.03 s exact virtual-ledger evaluator + local search),
  `graph_stats.py`, `kappa_weights2.py`, `run_batch.py`, `dt_launch.py`, `dt_collect.py`, `cfgs/`.
