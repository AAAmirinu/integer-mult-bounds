# J-arith: arithmetic-level ideas 38, 56, 39, 25 on the #325 word (p = 10, h = 20, v = 960)

Baseline (parity word, /tmp/radical/J/p325.pkl, built with build_word_stages.py ... parity, 12.9 s):
47,324 paid climbs, rank mass 179,640 (incl. 20 centre copies x 18 = 360), J = 483,908.5, W_lit = 658,800,
deficit 2,040, bit root 7.702769e-4, kappa = 7.69684039e-4 (bit-binding; complex cap kappa = 7.7211772e-4).
Pricing: /tmp/radical/J/price_hist.py (the kappa_shape.py chain on an arbitrary per-word histogram, W_lit held
at the baseline 658,800 = the bank-family count, so the deficit m*W - mass moves with the mass; the
`deficit_fixed` variant moves W instead). Scripts: census_a.py (38), idea56.py (56), idea39.py (39),
idea25.py + idea25_geo.py (25).

## Finding that frames all four items: every removable addition sits at frame rank 0

Producer coefficients: {-2: 578,560, -3: 960, -1: 320,040, +1: 29,640}. Gate frame rank by coefficient:
all 578,560 c = -2 gates and all 960 c = -3 gates are at frame ZERO (rank 0); the only gates at nonzero frames
are c = +-1 (forward/cleanup gates, side roots, injections, partner mixes/deliveries, gauge reads at 16/17).
Consequently the climb histogram is IDENTICAL whether one keeps the odd gates (F2), the non-multiples of 3 (F3),
the non-multiples of 6, or every gate (integer): 47,324 climbs, mass 179,640, same histogram, same kappa.
The parity transform's `removed_even_adds` = 578,560 has zero kappa content; it only lowers the finite bill
(literal_unit_additions, row L1 norms in finite_check.py / scalar_check.py).

## (a) Idea 38, signed digits / coefficient 3

- Where the 960 coefficient-3 gates come from: all are category `dirty_read` (scalar/word.py line 108, the
  D0 "initial correction" read of an ungauged dirty role), target register a (each of the 960 targets exactly
  once) reading one distinct dirty register b (960 distinct b, each read once with -3 and twice with -1), at
  frame rank 0. The integer decoder (check_decoder over Z instead of F2) gives every target
  x_T = 3*e_T + 2*(384 other sources): the "3" is the target's own source appearing in its three point stars,
  and the -3 read is the integer compensation of that multiplicity.
- Does the integer replay need the 3? `reorder_transform.integer_replay` (mod 2^61-1) is only a before/after
  consistency check of a reordering, not a decoder check. The verified claim (scalar_check.replay_projection)
  is F2 only (`if c&1: columns[a]^=columns[b]`); the magnitude enters only `norms` (row L1 pins) and
  literal_unit_additions = 352,560 = 349,680 + 3*960 (finite_check's constant < 2^80). The producer's
  `m.replay('token')` (exact integer mode of scalar/word.py) does need the 3 to restore y == want over Z, but
  that is producer evidence, not the certificate.
- Climbs saved if 3 -> +-1: 0. The gate count, frames and climbs are unchanged (one gate either way), and the
  gate is at rank 0 anyway. kappa delta = 0 exactly. Only the finite bill moves (1,920 fewer literal unit
  additions). Verdict: dead for kappa.

## (b) Idea 56, mod-3 / mod-6 fusion

| scheme | kept additions | removed | climbs | mass | kappa |
|---|---:|---:|---:|---:|---|
| F2 (current, c odd) | 350,640 | 578,560 | 47,324 | 179,640 | 7.696840e-4 |
| F3 (c != 0 mod 3) | 928,240 | 960 | 47,324 | 179,640 | 7.696840e-4 |
| Z/6 (c != 0 mod 6) | 929,200 | 0 | 47,324 | 179,640 | 7.696840e-4 |

- Decoder identity: mod 2 fails at 0 targets; mod 3 fails at 960/960 (x_T = 3e_T + 2*others = 2*others mod 3);
  mod 6 fails at 960/960. F3 replay of the physical records: all 960 targets end at the wrong value (sources and
  dirty registers do restore). So a characteristic-3 word would compute a different operator; the point-star
  decoder is intrinsically a mod-2 object (each target lies in 3 stars, each other source in 2 channels).
- Even if it held, mod-3 fusion removes only the 960 rank-0 gates, histogram change = none. Verdict: dead.

## (c) Idea 39, tree accumulation

Census (per register, climbs = positive-rank steps of the needs chain incl. the final climb):

| role | regs | climbs | mass | climb-count distribution | J now | J if one climb |
|---|---:|---:|---:|---|---:|---:|
| source | 960 | 2,400 | 18,240 | {2: 480, 3: 480} | 37,066.6 | 30,291.7 |
| target | 960 | 3,360 | 18,240 | {3: 480, 4: 480} | 39,585.8 | 30,291.7 |
| dirty | 8,100 | 41,544 | 142,800 | {3: 1816, 4: 2558, 5: 354, 6: 1264, 7: 974, 8: 648, 9: 386, 10: 66, 11: 34} | 406,638.8 | 237,553.0 |

Target climbs by (category, rank): side_root 1 x 2040, dirty_read 16 x 480 (gauge reads), dirty_read 17 x 360,
dirty_read 1 x 360, side_root 17 x 120. Dirty climbs are dominated by forward_gate ranks 1/2/3 (11,800 / 7,087 /
4,119), cleanup_gate 1/3/2, side_root 1 (2,400), cleanup_gate 17 (1,096), forward_gate 12 (980).
Most common multi-climb rank sequences: (1,1,17,1) x960, (1,1,2) x720, (2,1,17) x616, (1,16,2) x480, (1,18) x480,
(17,1,1) x480, (16,1,1,1) x480, ...

First-order upper bound (every register climbs once, entrance -> final; "reads grouped at the max read frame"
gives the same number because every register's last read is already at its final frame): J 483,908 -> 298,754,
dJ = -185,155 (J-proxy +1.17e-4 kappa; the exact chain saturates the complex cap at kappa 7.7211772e-4,
dkappa = +2.43e-6). This bound is not approachable:
- the mass is a telescoping invariant (every register climbs from its entrance to FULL/cap), so grouping only
  changes the split of each register's climb; but a read at frame f needs BOTH operands at f, so moving t's
  reads later forces every partner s_i up to the max frame, i.e. the saving on t is paid by the s_i;
- temporaries cannot carry partial sums: a COPY (op 2) places the temporary at ZERO paying dimf of the copied
  register's frame, the temporary can never leave ZERO (ERASE asserts state == ZERO, chains are nested), only
  one lifetime is open at a time, and a temporary is readable only by registers at ZERO, where reads are free
  anyway. So a tree of partial sums would have to live in ordinary dirty registers, whose climbs are priced
  identically: extra temporaries cost dimf(frame) each and save nothing;
- what IS legal (sharing climbs between a partial-sum register and its readers) is exactly what the stage tooling
  (restorations/sinks/kernels/targets) already searches.
Verdict: dead as an arithmetic lever; the census is the useful by-product (dirty registers with 6-11 climbs,
3,372 of them, carry most of the splitting loss).

## (d) Idea 25, centre design

Pricing (histogram arithmetic, idle ranks, gauges and W_lit unchanged; deficit = m*W - mass recomputed):

| design | centre mass l | deficit | bit root | kappa | dkappa | dJ |
|---|---:|---:|---|---|---|---:|
| h centres rank h-2 (baseline) | 360 | 2,040 | 7.70277e-4 | 7.696840e-4 | 0 | 0 |
| h centres rank h-3 (17 x 20) | 340 | 2,140 | 8.08013e-4 | 7.721177e-4 (complex cap) | +2.43e-6 capped (+3.8e-5 uncapped) | -14.9 |
| h centres rank h-4 (16 x 20) | 320 | 2,240 | 8.45750e-4 | complex cap | +2.43e-6 capped (+7.5e-5 uncapped) | -30.9 |
| 2h centres rank h-4 (16 x 40) | 640 | 640 | 2.41590e-4 | 2.415317e-4 | -5.28e-4 | +555.5 |
| 2h centres rank h-3 (17 x 40) | 680 | 440 | 1.66102e-4 | 1.660739e-4 | -6.04e-4 | +587.6 |
| h centres rank h-1 (19 x 20) | 380 | 1,940 | 7.32540e-4 | 7.320037e-4 | -3.77e-5 | +13.8 |

(With `deficit_fixed` instead, i.e. W absorbing the mass change, the same designs move kappa by only
+2.2e-8 / +4.5e-8 / -8.1e-7 / -8.5e-7 / -2.0e-8: the histogram shape alone is a tiny effect; the lever is the
deficit.) Why: the five-stage deficit 4v - 5l is literally m*W - mass with l = sum of centre frame dims
(compile_word: `ell += geo.dim(U)` for centre roots; moment.price asserts
mass = h*R + 2v(h-1) + l - gauges and m*W - mass = 4v - 5l), and the moment root is ~ deficit / J_five, so each
unit of centre rank mass removed is worth ~ +5 deficit ~ +0.25% root ~ +1.9e-6 kappa — the bit root passes the
complex cap after about 1.3 units; beyond that the complex supplier (COMPLEX_B) would have to be improved too.
Doubling the centre count is catastrophic for the same reason (deficit 640). Whether the five-stage completion
proof accepts an l other than h(h-2) is a separate question (word_pins.shape() hard-codes ell = h*(h-2)); the
bank identity itself is telescoping and would follow.

Geometry (producer finish(): `cen[2i+bit] = outs[-1]`, the centre-sharing pair module's extra root = sum of all
its inputs = star(2i+bit); compile_word: centre frame U = spans[node] = join of the source spans of the star,
`require(r == rt, 'centre frame')`): the star of a coordinate c is the 144 triples containing c; the span of
their labels chi_S (indicators in Q^20) has rank exactly h-2 = 18 for every c (verified numerically for c = 0,
1, 7): the partner coordinate of c never occurs (one linear condition) and the vectors satisfy
x_c = (sum of the other coordinates)/2 (a second one). A part of the star using coordinate set U outside pair(c)
has rank |U| - (components of its a-b graph) + 1 (verified on 400 random parts), so any split of the star into
k >= 2 registers costs strictly more than 18 in total: split by the bit of the lower other pair 17+17 = 34, by
selector parity 18+17 = 35, by touching pair 1 or not 17+16 = 33, two pair-halves + cross 8+10+17 = 35, best of
500 random 2-splits 36, 3-splits 52. No rank-(h-3) star and no pair of rank-(h-4) half-stars exists for the
point-star decoder; a smaller l requires a different decoder (not point stars), i.e. a new generator architecture
(ideas 42-45), not a centre-frame change.

## Verdict

38: dead (coefficient magnitude never enters the climb census; the 960 c = 3 gates are rank-0 D0 reads).
56: dead (mod-3 decoder identity fails at every target; mod-3/6 fusion would remove at most the 960 rank-0
gates; all 578,560 even gates are rank-0 too, so no fusion scheme can change the histogram).
39: dead as an arithmetic rewrite (temporaries are ZERO-bound and single-lifetime; the mass is telescoping;
the 185,155-J "one climb per register" bound is not approachable); climb census recorded above.
25: geometrically blocked but by far the highest-leverage quantity found: kappa ~ deficit/J with deficit =
4v - 5l, l = 360 = sum of centre frame dims; -1 unit of l ~ +1.9e-6 kappa (uncapped), -20 units already pins
kappa at the complex cap (+2.43e-6). Needs X: a decoder whose copied nodes span less than h-2 (not a point
star), plus a generalized shape()/completion for l != h(h-2), plus a better complex supplier to lift the cap.
