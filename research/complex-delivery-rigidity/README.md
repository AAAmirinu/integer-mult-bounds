# The complex delivery layer is rigid: target hosting and raw-face sharing closed exactly

Research note and tools. Prepared by **higherbeing** with Claude Code (Anthropic) assistance. Apache-2.0. This note makes no κ
claim; it records two exact negative results about the complex local word that the current frontier (#622–#645 lineage) is built
on, with the scripts that prove them from pinned repository files.

## Summary

The K-triangle word (#622, 492 helpers per call) delivers each target's cross-block content through 8-sums `M = f + f'` of face
packets. Per Hamming block it spends 8 *slot copies* on the two non-selected partitions and 0 copies on the selected partition
(#531's raw-half reads plus the pair butterfly). Slot copies and the in-place mixing of the 8-sums are about 15 % of the local
rank mass, so they are the natural target for any "shared delivery" redesign: let one register, or a target itself, serve several
consumers. Two mechanisms were proposed for this (my #520 §3 "group delivery" and the output-borrowing idea in #571's open list).
Both are closed here:

1. **No target can host a face or 8-sum for other targets** (the "output borrowing" form). A target's cap contains an 8-sum's span
   exactly when it consumes it; the only consumers with consistent coefficient ratios are in the *opposite* tetrad; and a target's
   own-row frame lies only in *same-tetrad* caps. Since the own read cannot be moved later (fact F4 below), every cross-tetrad
   target-to-target read is frame-illegal, and same-tetrad sharing is the butterfly the word already performs, once per target.
2. **No read order of face registers removes the slot copies** (the "global face-level schedule" form). A register read by target
   `x` carries `x`'s frame to all later readers, so a later reader must have `x`'s frame inside its cap. The census over all 168
   (key, consumer block) incidences shows: a target's frame after the butterfly, or after its own row plus the selected faces, is
   inside the caps of *no* consumer group (0 of 1344 cases each); only the bare own-row frame is ever tolerated, and for the 112
   non-selected incidences that happens for 64 of 896 foreign targets, leaving 96 incidences with no tolerated foreign target at
   all. So raw reads can serve the selected partition (what #531 uses: 56 of the 160 tolerated selected cases) and nothing else.

Consequence: under the hub's rules (monotone frames, a target's frame inside `u_t^⊥`, helpers never reading targets, the own row
read first) the delivery layer of this word family is at its floor. Gains must come from other layers; the same night #646
measured that removing 12 more helpers by skeleton atoms *lowers* κ and #645 gained 0.8 % in the factory/dirt-propagation layer.

## Setting

All objects are read off the pinned constructor `research/complex-571-cold14-k492/code/construct_k_triangle.py` run on the
pinned inputs `research/direct-delivery504-global/inputs/hamming/` (first with an empty triangle schedule, which reproduces
RAW504, then with `TRI-SCHEDULE.json`, which gives the 492-helper word). `code/instrument_constructor.py` executes the unchanged
file with a role dump appended, so every register's role is exact: for each of the 14 blocks the 8 source lines, 16 module
registers, 2 tetrads, 12 keys `(pair, ε)`, the face packets each block produces for its two consumer blocks, the 8-sums, the slot
copies, the own rows, the 12 target pairs with their 2×2 matrices, and the selected partition.

Notation. Block `c` is a 4-set of coordinates; its 12 keys are `(p, ε)` for the six pairs `p ⊂ c` and `ε = ±1`; the 8-sum
`M_{c,p,ε}` is the sum of the two faces `(p, ε)` produced by the other two blocks containing `p`, so it spans 8 sources. A target
`t` of block `c` consumes key `(p, ε)` iff `σ_t[p_0]σ_t[p_1] = ε`. Its *cap* is the hyperplane `u_t^⊥` (its final frame); its *own
row* is the dim-2 register it reads first.

## Result 1: target hosting is closed

Facts, each checked on all 14 blocks (`code/blockdata.py`, `results/blocks.json`, `results/blockdata.log`):

- **F1 (cap = consumption).** `span(M_{c,p,ε}) ⊆ cap(t)` iff `t` consumes `(p, ε)`: 112 of 112 targets, no exception and no
  partial case (every source of a non-consumed 8-sum is orthogonal to `t`). Every 8-sum spans dim 5; every target consumes 6 of
  its block's 12 keys.
- **F2 (shared keys).** Two targets of one block share 2 keys if they lie in the same tetrad (both pairs of exactly one
  partition) and 3 keys if they lie in opposite tetrads (one pair per partition). 28 pairs per block: 12 same-tetrad, 16 cross.
- **F3 (coefficient ratios).** The coefficient of `M_{c,p,ε}` in target `t`'s output is `∓σ_t[p_0]·α_{p,ε}/2`, so for two consumers
  `x, z` the ratio on a shared key is `σ_x[p_0]σ_z[p_0]`. For a cross-tetrad pair the sign difference `σ_xσ_z` has weight 1 and
  is constant on the three coordinates of the shared pairs, so the ratios agree on all 3 shared keys; for a same-tetrad pair it has
  weight 2 and the two shared keys have opposite ratios. One register with the ratios of `x` can therefore serve `z` iff they are in
  opposite tetrads (the 2×2 mixes and the butterfly exist precisely because same-tetrad sharing needs two registers).
- **F4 (own row).** Each target's own-row frame (dim 2) lies in the caps of its 4 same-tetrad targets and in no other cap of
  the block (`own in caps of 4/8` for all 112). Own registers are never written after their last target read, so in content terms
  the read could move later; but the module's next read of the register lifts its frame to dim 3 (96 cases), 5 (8) or 6 (8), and in
  all 112 cases that frame leaves the target's cap (`results/own_deferral.json`). The own read must stay first.

Putting F1–F4 together: a target that holds anything has its own-row atom in its frame; a cross-tetrad reader would need that atom
inside its cap (F4: never); same-tetrad readers share two keys with opposite ratios (F3), which is a 2×2 mix, i.e. the existing
butterfly, and after it the frame holds the selected keys, which the other two same-tetrad partners do not consume (F2), so it can
happen once. Hence no target can act as a shared register beyond what the word already does.

**Copy floor at the 8-sum level.** `code/order_model.py` (CP-SAT, exact atom flow through shared registers: a read merges the
frames of both operands and every atom in a target's frame must lie in its cap) gives for block `(0,1,2,3)`: with pure single-key
registers and at most 1 register per key, infeasible (0.7 s); at most 2 per key with the butterfly, infeasible (2 s); at most 3 per
key, 20 copies with bound 12 after 240 s (`results/order_*.log`), against the 8 copies the word uses. The word beats the pure
model with its 2×2 mixes, and under mixes each unshared partition costs exactly one copy per key (each 2-key register is private
to the pair that agrees on that partition), so 8 per block is the floor for every design that shares one partition per target —
and F1–F4 show one partition is the most a target can share.

## Result 2: raw-face sharing across blocks is closed

`results/read_audit.json`: in the raw word every target gate is inside the target's cap (0 violations); 120 registers are read
by more than one target and **none of them by two targets of the same block** (88 by two, 32 by three, all cross-block). The
word's only sharing is #531's trick: a face packet produced for consumer block `b` is read raw by a target of block `c` while
that target's frame is still just its own row, and then merged by `b`.

`code/tolerance.py` (`results/tolerance.json`, `results/tolerance.log`) asks, for each of the 168 (key, consumer-block)
incidences and each of the 12 targets consuming that key (4 own-block, 8 foreign), whether the target's frame at stage S1 (own row,
dim 2), S2 (own row + the four selected faces, dim 7) or S3 (after the butterfly, dim 7) is inside the caps of all 4 consumers:

| incidence | target | S1 tolerated | S2 tolerated | S3 tolerated |
| --- | --- | ---: | ---: | ---: |
| selected (56) | foreign (448) | 160 | 0 | 0 |
| selected (56) | own-block (224) | 0 | 0 | 0 |
| non-selected (112) | foreign (896) | 64 | 0 | 0 |
| non-selected (112) | own-block (448) | 0 | 0 | 0 |

Per non-selected incidence: 96 have no tolerated foreign target at any stage, 16 have four at S1 only. Any read after the first raw
face read, and any read after the butterfly, is therefore terminal and private, and the 112 slot copies cannot be replaced by raw
reads in any order (a target spending its S1 budget on non-selected faces would also lose its butterfly, F2). This closes the
"group delivery" direction of #520 §3 as a whole and not only per block.

## What this leaves

Delivery (this note), skeleton atoms (#646's measurement: 480 helpers, κ falls), and owner maps (#639, #644 ceilings) are at
their floors for this word family. The layers that still pay are the factory and its dirt propagation together with cold ends
(#604, #617, #629, #637, #645), and the bit side (8 % headroom since #555). Rule-level changes (a deferrable own row, or a
target frame not bounded by `u_t^⊥`) would reopen delivery, but they are format changes, not constructions.

## Reproduction

From the repository root, standard library only (`order_model.py` needs `ortools` and is skipped when it is absent):

```sh
sh research/complex-delivery-rigidity/reproduce.sh /tmp/delivery-rigidity
```

It rebuilds both words through the pinned constructor, writes `ROLES.json`, and regenerates every file in `results/`.
`results/census504.json` is a register census of RAW504 (frame chains, Φ by class with `r·ln(73/r)` per climb, reader classes).

## Credits

icekylinx (#425, #433, #531 construction and the SAME504 factory; #523, #535), jeremykothe2 (#622 K-triangle constructor and
schedule, #591–#601 hyperplane ends), DreamingOfClouds (#604 cold ends, #599), DominikScholz (#571 packet-factory floor and the
open list this answers), chafreaky, eumemic and the #446 authors. The constructor is executed unchanged from the pinned #622
package. All analysis code here was written with Claude Code (Anthropic) assistance and is released under Apache-2.0.
