# format-obstructions

**Exact bounds on window width, copy cost and label dimension (no new κ).** This package states and proves three
theorems about frames and gates (A: drop-free contributions force orthogonal labels; B: stage windows add up; C: a drop
that reaches the readers costs the pairing rank), a clique bound on the label dimension, and a simulation theorem for
PR #425's mutable-basis words (S). Everything that can be checked exactly is checked by one offline driver on pinned
inputs: Sussman's `gx.check1` programs, #425's own word, and exact SAT instances on the E8 in-cap graph.
[PROOF.md](PROOF.md) has the statements, the proofs and the scope of each.

## Scope

- **Model.** Registers stand at frames (subspaces of a label space), climb by nested steps, drop at a price
  d(f, g), and gates add registers that stand at one common frame. Sources start at their label, targets stay inside
  their label's orthogonal. This is the content of the rules E0–E3 of `gx.check1` and of the common-label rule of
  #425's conjugation lemma.
- **Checked semantics.** `gx.check1` (gcert/1, vendored unchanged from Jacob Sussman) on three programs: the p = 3 toy,
  the p = 10 complex program of #327 and the p = 11 program of #193; and #425's mutable-basis semantics on its own
  920-register word.
- **Not covered.** No bit word is replayed (the bit words use the community's paired-cube checker). No Lean. The multi-stage
  statements use hypotheses about the layout that are read from upstream, not re-derived: (B1)–(B2) of Theorem B and
  (P1)–(P2) of Theorem P (PROOF.md §3, §7).

## Results

| | statement | status |
|---|---|---|
| **Thm A** | A contribution of x_T that reaches a register by a drop-free path forces the register's frame to contain U_T. So a lossless x_T → y_S route needs U_T ⊥ U_S, and there is no lossless x_S → y_S route. | proved; replay of every gate of three programs, 0 violations (1.08 M and 2.06 M gate checks at p = 10, 11) |
| **Thm B** | For a pair a with stages j = 1..s: k_a + Σ_j rk C_j ≤ m (C_j = span of the labels of a's correctors in stage j). With corrector rank h − 1 this gives m ≥ 1 + s(h − 1). | proved under the layout hypotheses (B1)–(B2); rank h − 1 measured on the p = 10, 11 complex programs, the bit paired cubes p = 4, 5, 10, 11, the E8 bit dual (7) and the E8 complex labelling (8); #425's word has m = 73 = 1 + 9·8, so the bound is attained |
| **Thm C** | The drops that carry a total gathered from sources P to readers Q cost at least rk(U(P) × U(Q)), whatever the tree of copies, frames and drops. | proved; the star copy meets it exactly on the p = 10 (360), p = 11 (440) programs, on #425's centres (72, 57 gathered sources per centre). For the E8 bit dual the package computes the bound 72, which equals the copy loss #370 reports (not replayed) |
| **Toy** | The p = 3 program (degenerate port span) admits a split scatter, cst 18 → 16 (exhaustive optimum 16). | exact; gain needs a degenerate port span, 0 on the nondegenerate families |
| **Clique bound** | If every pair in a set K has a drop-free route, the labels on K are orthogonal and nondegenerate: Σ_K k_T ≤ r. | proved; ω = p (bit) and 8, 8, 12, 12 (complex, p = 4..7); 20 ports pairwise lossless inside the p = 10 program, so k = 1; ω = 8 on the E8 in-cap graph |
| **E8 labels** | The h = 9 labelling of the E8 in-cap graph is unique (Sussman's). No k = 2 labelling exists in dimension r ≤ 17 (r = 16: 255 plane-type patterns, r = 17: 256, all UNSAT). | exact SAT (CaDiCaL) with calibrations and a positive control; for the full in-cap graph only |
| **Thm P** | For **fixed-role B₂ windows over F₂** (one helper set, same program, same slots in every stage, slot-carried pairs spanning) the cross-Gram of two stage windows is zero, so m ≥ s·h. | proved under (P1)–(P2); computed on the complex p = 10 and #193 programs only (399/400 and 483/484). **Compressed windows circumvent it**: #425's nine-stage complex word has m = 73 = 1 + 9·8 < 81, at the Theorem B bound. #386's bit word (m = 64) has a ℚ form; Theorem P is not claimed for it. Not a general obstruction. |
| **Prop. N** | A non-nested step of rank r on a register that must still reach its sink costs 2r over the nested chain; a copy of rank r is charged r. | proved; pricing context for the p = 10 bit word: ≈ −0.49 % for a rank-1 register descent in each of the five stages (the fourth digit is a modelling choice) against −0.2457 % for a rank-1 copy in each stage |
| **Thm S** | A mutable-basis word with b_x modified sources and b_y read targets is simulated, in the immutable-source / no-target-read format, with R + b_x + b_y helpers. | proved; exact on #425's word (680 + 112 + 112 = 904), with controls. A bound on helper count, not on price. |
| #425 | Thms A and C and the clique bound hold on #425's word, and its width attains Theorem B. | replay: 0 violations, centre copies 72 = 72 (57 gathered sources per centre), all 120 targets at frame 0 at the cut, rank 8 for every target |

## What this means for the swarm

A–C and the clique bound bound **m and the copy rank**, the label dimension for a given in-cap graph, and (through the
five-stage ledger D ≤ N_data·k, read from upstream) **D**. They do
**not** bound the helper count R, nor the idle and stock costs (the block profile of the helpers), which is where
#425, #433 and #442 gained (#425, the one replayed here, keeps m at the Theorem B width and the copy rank at the
Theorem C bound). In the
formats covered here a further κ gain therefore has to come from R or the stock, or from a new port family whose
corrector rank is below h − 1 with a cheap decoder (the only family-dependent term of Theorem B). Nothing here is
a statement about the size of R.

## Verify

    python -m pip install -r research/format-obstructions/requirements.txt   # python-sat 1.9.dev15, networkx 3.7, mpmath 1.3.0, numpy 2.3.5
    python3 -B research/format-obstructions/verify.py --output /tmp/format-obstructions-out   # Python 3.11+, tested 3.12

No network; `-O` is refused. The driver checks the sha256 pins of `SOURCE.json`, runs 91 independent tasks in a
process pool (`--jobs N`, default the core count), compares the facts with `expected.json`, and requires an unchanged
tree. Runtime: about 90 s wall on 12 cores, about 15 CPU-minutes in total (the CaDiCaL instances are 70 % of it).
It runs:

- `gx.check1` (with the exact scalar identity) on the three programs; the taint replay of Theorem A at every gate;
  Cor. A1, the corrector ranks of Theorem B and the copy bounds of Theorem C;
- the p = 3 toy (nestedness, equal frames, scalar half, exhaustive optimum);
- Theorem P (rank of the cross-Gram constraints), the forced-copy count and the contamination scan;
- #425's word: frame and taint replay, scalar identity over ℚ, the Theorem S conversion and its replay;
- the pinned pricer on the p = 10 bit histogram (root, pivot-free variants, copy and descent units);
- the neighbourhood ranks, the E8 bit-dual decoder, the clique numbers, the 20-clique;
- the SAT checks: uniqueness at h = 9, k = 2 at r = 16 and 17.

**Negative controls.** Shifted labels (12 non-orthogonal lossless pairs) and a corrupted port (`gx.check1` rejects it at
E1; 14 replay violations); a toy cut frame outside the radical; the immutable/no-target-read detector flags 1,640
source modifications and 112 target reads on #425's word as written and 0 on the converted word; omitting the K part
of #425's preconditioner and the compensation of the converted word are rejected; k = 1 at r = 8 UNSAT and r = 9 SAT,
h = 8 UNSAT, and the k = 2 encoder at r = 18 accepts the direct sum of two k = 1 solutions.

## Not checked, or checked only in part

- The bit side: Theorem P (stated for F₂ windows) and the copy/overlap measurements were computed on complex programs;
  the pricing context uses the p = 10 bit histogram. No bit certificate is replayed, and nothing is claimed about
  Theorem P for ℚ forms. The bit and E8 rows of the Theorem B table are in-cap neighbourhoods of the family, not replayed
  correctors.
- The layout hypotheses (B1)–(B2), (P1)–(P2) and the width m = 64 (#386) are taken from upstream. They were read against
  Sussman's `Work/Bridge/Net.lean`, `Work/BridgeGeom/Stage.lean` and `Work/BridgeGeom/Net.lean` (f010392c), whose
  statements are consistent with them; **this was read, not formally verified.** Two points are open: whether the
  backward stages 1 and 3 count as "the same program", and whether the stage-j target frames lie in ι_j(q_S)^⊥.
- The Theorem S simulation was replayed by the detector of `checks/mutable425.py`, not by `gx.check1`.
- `inputs/pricing/hist_p10b.json` is a copy of the five-stage histogram that #325's verification writes to `math.json` (a
  run output at head 0eca9340, not a committed file); the pricing numbers are pricer-model outputs for the p = 10 bit
  word, not theorems.
- The overlap measurements are for one program and 1,160 candidate directions.
- `inputs/gcert1-p3-cone-R16.json` is a local research program that is not published upstream.

## Files

`verify.py`, `expected.json`, `SOURCE.json`, `requirements.txt`, `PROOF.md`, `NOTICE`; `checks/` (`certs.py`, `toy.py`,
`pivots.py`, `mutable425.py`, `pricing.py`, `families.py`, `sat_e8.py`, `e8lib.py`, `f2.py`); `gx/gx.py` (Sussman,
unchanged); `inputs/` (three gcert/1 programs, `pr425/FULL-WORD.json.gz`, `pricing/cost.py`, `pricing/hist_p10b.json`).
`.github/workflows/format-obstructions.yml` runs the driver on Python 3.12.
