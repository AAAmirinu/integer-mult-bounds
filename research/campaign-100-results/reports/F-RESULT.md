# F-structure: structural analyses of the #325 word (ideas 14, 41, 36, 22, 12)

Word: parity-fused word of PR #325's package, built with a /tmp copy of `imb-retime2/build_word_stages.py`
(patched to set `word_pins.RECORD = {}`): `/tmp/radical/F/p325.pkl` — 399,140 records (350,640 ADD, 48,460 MOVE,
20 COPY, 20 ERASE), 10,020 registers (1,920 sources, 8,100 helpers of which 1,200 entrances at dim 16), 13,866
registered frames of Q^20 (12,885 used), form G = 9I − J. `kappa_shape.py` on the pickle reproduces the pinned
κ = 7.69684039383334e-4 (bit root 7.70276909563042e-4), J = 483,908.49. All scripts/logs are in /tmp/radical/F.

## (a) Idea 14 — automorphism group of the word (auto_a.py, auto_a2.py, auto_bliss.py, auto_frames.py)

Coloured graph: 841,266 nodes (10,021 registers coloured source/helper/temp, 399,140 gate nodes coloured by op and
coefficient, 350k operand-role nodes, 12,885 frame nodes coloured by dim, init/final role nodes), 3,968,428 edges
including the full containment relation among used frames (2,331,708 strict pairs). Category labels and initial dims
were dropped in a second ("coarse", 32 colours) run so the colouring cannot break symmetry artificially.

- 1-WL colour refinement is stable after 6 rounds with 837,426 classes: every register (10,021/10,021) and every
  frame (12,885/12,885) is a singleton. The only non-singleton classes are 960 triples of literally identical
  records `(1, src, temp, +1, ZERO, center)` (the 3× centre copy), i.e. 2,880 gate nodes + their role nodes.
- bliss (igraph 1.0, coarse colouring): |Aut| = 6^960 exactly (748 digits), 1,920 generators, every generator only
  swaps two identical centre records. Modulo identical records the automorphism group is **trivial**.
- Gate orbits = number of distinct records = 397,220 (399,140 − 1,920). Register orbits 10,021, frame orbits 12,885.
- Frame containment poset alone (no gates): |Aut| = 2^1123 — only "twin" swaps of frames with identical
  containment pattern (960 pairs of dim-19 frames, 104 pairs of dim 10/12/14), all distinguished once gates are added.

Verdict: **dead**. The expected S_p × orientation × Z_2-pairing symmetry (hyperoctahedral, 2^10·10! ≈ 3.7e9 on the
960 weight-3 chi vectors) is completely broken by the design (annealed pair module, frozen matching, local trees,
cube orientation). There is no symmetry to reduce by: the exact search space is the full 397,220 distinct gates.

## (b) Idea 41 — transposed word (transpose_b.py, kappa_shape_T.py)

Implemented at record level: records reversed, ADD a += c·b → b += c·a, MOVE b→c → c*→b*, COPY/ERASE swapped,
every frame f replaced by its G-dual f* = G^{-1}·span(A[f]) (basis 11A − (A1)1^T, annihilator 9B − (B1)1^T), so
dim f* = 20 − dim f, containment reverses, and nondeg(f*) ⇔ the package's own nondeg(f) (the (9−h)AA^T + ss^T
formula is exactly the G-dual Gram). Checks passed: 300/300 sampled dual frames nondegenerate; MOVE replay with
exact containment and rank bookkeeping; `<y, L x> = <L^T y, x>` mod 2^31−1 on random vectors (2 trials) so the
transposed word really computes the transpose map.

- Paid histogram of the transposed word = forward histogram exactly
  {1:21400, 2:9149, 3:6065, 4:1359, 5:1092, 6:1006, 7:640, 8:164, 9:293, 10:248, 11:80, 12:1006, 13:2, 14:344,
  16:960, 17:2536, 18:980}; per-register climb sequences are the forward sequences reversed for all 10,020 registers;
  J = 483,908.486 both; kappa_shape κ = 7.69684039383334e-4 both (identical Hn, literal stock 658,800).
- Why, by construction: a register's chain F_0 ⊂ … ⊂ F_k becomes F_k* ⊂ … ⊂ F_0* with dim F_i* − dim F_{i+1}* =
  dim F_{i+1} − dim F_i, so the multiset of climbs per register is invariant. This is the `reflected == census`
  assertion of transport_transform.py (reflected histogram over annihilator dimensions). The only things that change
  are the endpoints: the 1,200 entrance helpers (start dim 16) become helpers that *end* at dim-4 frames and the 960
  chi-line sources end at dim 19 — gauges {16:1200} → {} — but kappa_shape adds and subtracts gauges, so the priced
  literal histogram is unchanged. (The five-stage bank layout has no "exit gauge", so the transposed word is not
  even a legal five-stage word without re-deriving the kernel stage; and if it were, it would price identically.)

Verdict: **dead**. Transposition cannot change the histogram, J or κ of a paired-cube word.

## (c) Idea 36 — coordinate / character alignment of the frames (frames_c.py)

Cover data: chi = 960 weight-3 0/1 vectors (one per source pair), cov = 3·chi − 1 ∈ {2,−1}^20. Of the 12,885 used
frames (dims: 1:960, 2:1440, 3:1440, 5:940, 6:180, 7:520, 8:279, 10:359, 12:275, 13:500, 14:352, 15:698, 16:120,
17:1440, 18:1460, 19:1920, plus ZERO/FULL):

- coordinate subspaces: 2 (ZERO, FULL) = 0.016%; 91.4% of ADD gates sit at ZERO/FULL (dirty reads/centres), the
  other 8.6% at non-coordinate frames.
- spanned by the cov ({2,−1}) vectors they contain: 2 (ZERO, FULL).
- spanned by the chi vectors they contain: 7,998 = 62.1% (all frames of dims 1,2,3 and 19; 940/940 of dim 5,
  180/180 dim 6, 520/520 dim 7, 279/279 dim 8, 217/359 dim 10, 80/275 dim 12, 20/1460 dim 18; none of dims 13–17).
- spanned by {0,±1} vectors: 12,885 = 100% (exhaustive meet-in-the-middle for |U ∩ {0,±1}^20| ≤ 3e5, random
  sampling otherwise; no undetermined cases).
- containing even one full-support ±1 vector (a Z_2^20 character): 0 of 12,883 proper frames (parity obstruction:
  every annihilator has an odd number of odd entries, e.g. (1,−2,1,−2,1,1,…)). Character frames do not exist here.
- complexity: integerized RREF basis max|entry| 1: 6,501 (50.5%), 2: 5,798 (45.0%), 3: 460 (3.6%), 4: 125 (1.0%);
  bit length ≤ 3 everywhere; RREF denominators 1: 12,140, 2: 702, 3: 42; producer's stored bases have |entry| ≤ 4,
  annihilators ≤ 6.

Verdict: **dead / no leverage**. The frames are already as "Boolean" as the geometry allows ({0,±1} bases, entries
≤ 4, denominators ≤ 3), so nondegeneracy checks are already cheap; the literal character-frame proposal is
incompatible with the weight-3 cover and the form 9I − J (no proper frame contains a sign vector).

## (d) Idea 22 — intermediate frames over Q vs F_3, F_5, F_7, Q(i) (fields_d.py)

Sample: 200 random registers (of 9,540 with a chain step of gap ≥ 2) → 492 steps a ⊂ b with gap ≥ 2 (gap hist
2:173, 3:110, 4:24, 5:16, 6:16, 7:9, 8:3, 9:4, 10:7, 11:2, 12:22, 14:10, 16:16, 17:52, 18:28). Candidate
intermediates = a + (b ∩ f) and (a + f) ∩ b for f over the neighbouring frames descent uses (prev/next frames of the
partner register at every shared gate, the gate frame, and the chi lines of the sources read; 46.4 generators per step
on average), kept if a ⊊ c ⊊ b, de-duplicated by RREF; nondegeneracy = det of 9I − J Gram ≠ 0 in the field.

| field | distinct candidates | nondegenerate | note |
| --- | --- | --- | --- |
| Q | 2,670 | 2,670 (100%) | **no lattice-generated candidate is degenerate over Q** |
| Q(i) | 2,670 | 2,670 | identical by construction: meets/joins of rational frames commute with field extension (checked in the Q^40 embedding, 74/74 dims = 2× rational) and the Gram determinant is the same rational number |
| F_7 | 2,670 | 2,626 (−1.6%) | 11 steps lose candidates, 0 gain |
| F_5 | 2,670 | 2,234 (−16.3%) | 37 steps lose, 0 gain |
| F_3 | 4,153 (dimension jumps in 134 steps, 2 frames drop rank) | 0 | 9I − J ≡ −J (rank 1) mod 3: everything degenerate |

80 of 492 steps have no strict intermediate from the lattice in any field. No field admits strictly more
nondegenerate intermediate frames than Q; over Q nondegeneracy never binds for these candidates — what limits descent
is the lattice (which frames exist between a and b), not the field.

Verdict: **dead**. Number fields add nothing (same subspaces, same determinants); finite fields only lose.

## (e) Idea 12 — entrance census beyond lines/planes (entrance_e.py, full_e.py, make_new_pool.py, overlap_e.py)

Post-target word of #320's package dumped with `/tmp/p10b_run.py PKG discovery/dump_at.py PKG /tmp/radical/F/D target`
(404,945 records, 13,607 frames), `coll/census.py` → 6,960 eligible helpers (first-frame dims 1:3240, 2:1080, 3:2180,
5:260, 6:40, 8:20, 10:40, 12:80, 15:20), 3,920 distinct first frames; `coll/lines.py` → 24,203 lines (23,963 with
≥ 2 helpers), `coll/planes.py` → 10,541 rank 2–14 intersections (reproduces the README exactly).

Read vectors = the weight-3 lines of the sources a helper dirty-reads (mean 44.7 distinct reads per helper, all of odd
multiplicity). Sample of 300 helpers, then exhaustive over all 6,960 (cheap, because so few reads are inside):

- mean number of read lines inside the helper's first frame: 0.87; 45% of helpers have none inside, 0% have all
  inside. Exhaustive (first-frame dim, #reads inside): (1,1):2880, (2,2):480, (3,4):380, (5,8):80, every other helper 0.
  When reads are inside they span the first frame (dim = rank in all 3,820 cases).
- nondegenerate rank-k subsets of inside reads (all helpers): k=2: 5,000, k=3: 6,000, k=4: 5,120, k=5: 2,560; no
  degenerate subset at all. Distinct subspaces: rank 2: 3,476 (2,260 already in the 10,541 pool), rank 3: 3,276
  (460 in pool), rank 4: 1,584 (120 in pool), rank 5: 80 (all in pool). Every one is shared by ≥ 2 helpers
  (member-count 2–8, they are the helpers sharing the same first frame).
- so a full rank-3..8 read-span census adds **5,496** new shared candidates (rank 2: 1,216, rank 3: 2,816, rank 4:
  1,464; rank ≥ 5: 0) on top of 10,541 (+52%), all inside the dim-3/5 first frames of 460 helpers (6.6%).
  Sample-only extrapolation agreed (≈4.5k rank-3 and ≈3.0k rank-4 subsets).
- Direct test: `closure_pack.py` with the README settings (EXCLUDE=…, ORDERS=4 NT=3 NOISE=0.3) on H+L+P versus
  H+L+P+NEW: seed 5 → 390 positive-closure entrances, 1,050 entries, φ −1602.03 in both; seed 11 → 1,048 entries,
  φ −1579.48 in both; the selections are identical. None of the 5,496 new subspaces has a positive closure: their
  member helpers are exactly the first-frame groups whose F2 responses are independent, so no pivot/donor
  representation exists. (Aside: 40 nondegenerate dim-3 first frames shared by ≥ 2 helpers are absent from the
  pairwise-intersection pool; they are included in NEW and also give nothing.)

Verdict: **dead** for the read-spanned census: the entrance constraint (subspace inside the first frame) is so
restrictive that a "GPU exhaustive" rank 3–8 census is a 40-second CPU job, and its 5,496 extra candidates change the
shared-donor packing by exactly 0 φ. Any remaining entrance gain must come from candidates not spanned by read
vectors (lines/intersections of first frames, which the pool already has) or from changing the first frames.

## Overall

All five structural analyses close their ideas on #325's word: no symmetry (trivial Aut), transposition is a
histogram identity, frames are already {0,±1}-aligned with no character frames possible, other fields add no
nondegenerate intermediates, and the extended entrance census adds candidates but zero packing value.
