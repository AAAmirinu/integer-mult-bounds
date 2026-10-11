# R685: the D4(c) sums from their pairs, and two redundant copies deleted

**Bit supplier (exact; eleven stages; PR #442 whole-residual hosting with no cross-family split; target mixing):
c = 661777032472911750807/(5·10²³) ≈ 1.323554·10⁻³.** That is +0.62% over the R687 bit supplier of our draft #504 (1.315433·10⁻³), +1.51% over R687 with the greedy kernel
(1.303868·10⁻³), and +2.99% over R715 (1.285129·10⁻³, PR #463), all from the same pipeline and hosting rule. The word has 685 helpers (R687: 687).
Paired with PR #442's complex supplier κ stays complex-bound (1.265849·10⁻³, as for R715 and R687); the bit-only κ is 1.321805·10⁻³.

The word is a follow-up on #504 (R687, read-then-climb, exact pivots); everything else in the pipeline is #504's, unchanged and pinned.

## What changed (three steps, all reproduced by `verify.py`)
1. **Inline.** In the R687 hierarchy each of the 14 D4(c) sums (8 lines, dim 4) is built from two L's. 28 of the L's are therefore read three times
   (two M's and the D4(c) sum), and the three readers need three register chains. Here each D4(c) sum is built from its four pairs directly, so no L has a
   third reader: χ = 3 → 2 for 28 L's, 28 L copies fewer (471 copies by the Dilworth recount against the 464 bound; 500 on R687; the emitted word has 472 copies and 241 carriers, one carrier traded for a copy). One 12-line sum also reads two
   source lines instead of one pair. 15 rules change their kid lists (`data/inline-kids.json`); every new kid list is the old one with some kids replaced by their own
   kids, so contents and frames are unchanged (checked). Raw R goes 811 → 782.
2. **Optimal chains.** PR #370's compile2 assigns register chains greedily. The chains here are an optimum of the exact path-cover ILP over the read events of the
   inlined DAG (`code/chain_model.py`, HiGHS; 772 helper registers, pinned in `data/chains-inline.json`, recomputed objective-for-objective by `--discover-check`).
   They are handed to compile2 through one replaced statement. Between equal-cost optima the choice moves c by several tenths of a percent (measured by the
   sections scout on R687), so the chains are part of the word and pinned. Then #370's fullword, #443's reuse and #436's retime, unchanged: **R = 687 again**.
   Reuse recovers as many registers fewer as the inline saved in the raw word (see Findings), so the gain is in the climbs and the kernel:
   five-stage saving 1.001418·10⁻³ → 1.006976·10⁻³ (+0.56%).
3. **Two copy deletions.** `code/copy_sweep.py` replays the raw word exactly (every register's x-part at every gate) and tests, for every copy, whether each of its
   reads can instead take a set of up to three other registers whose x-parts XOR to the copy's content, legal at that read's own frame (frames only climb and a gate has one
   frame, so the register must be at a frame inside the gate frame now and inside its next frame later). Exactly three copies qualify after the inline: two D4(c) copies
   (class 8/4) and the 16/6 sum with two deliveries. The two D4(c) copies are deleted (their reads take other registers; the dirt compensation and cleanup are rebuilt exactly by #443's
   reuse step), and reuse and retime run again: **R = 685**, five-stage saving 1.008233·10⁻³ (+0.125%). The 16/6 copy is redundant too, but deleting it removes no
   register (reuse already recovers it) and leaves the pivot bound at 101, so it stays.

**Exact kernel pivots.** The inlined word has 233 pivot candidates; the sum-rank lower bounds give at most 101 pivots (sum-rank 118 on the 218-element component, 1 on the other nontrivial
component). The pinned selection (`data/pivot-selection.json`, seeded annealing, reproduced by `code/select_pivots.py`) attains 101, so 101 is the maximum for #443-format selections on this
retimed word with coordinate entrances (the scope of #504); parity leaves 100 rank-1 pivots. No exhaustive refutation is needed: the witness meets the bound.
The kernel is #504's `kernel_exact.py` on that selection; mixing is #504's `mix_target.py`.

| word | R | five-stage saving | s=11, greedy kernel (#463) | s=11, exact pivots |
|---|---|---|---|---|
| R687 (#504) | 687 | 1.001418·10⁻³ | 1.303868·10⁻³ | 1.315433·10⁻³ |
| R684: R687 + 3 word-level copy deletions | 684 | 1.003262·10⁻³ | 1.303938·10⁻³ | 1.317462·10⁻³ |
| inline only (28 L copies) | 687 | 1.006976·10⁻³ | 1.309219·10⁻³ | 1.322341·10⁻³ |
| **R685 (this package)** | **685** | **1.008233·10⁻³** | 1.309099·10⁻³ | **1.323554·10⁻³** |

All s = 11 values are eleven-stage, whole-residual (PR #442 rule), target-mixed bit values from the same assembly code. The exact-pivot column uses a seeded-annealing selection
at the exact maximum (seed 3 for the R684 and inline-only rows, seed 1 for R685; #504's row is its frozen selection). Other annealing seeds at the same pivot count move c by about ±0.05%
(R687: 1.31490–1.31525·10⁻³ over four seeds against 1.31543·10⁻³ for #504's frozen selection; R685: 1.32319–1.32355·10⁻³ over five seeds).
So the figure above rests on a best-of-seeds selection, like #504's.

## Why the register count stops at 685 (findings)
- **The inline saves raw registers that reuse had been recycling.** The 28 L copies are born at A3 frames and leave dead pair slots; the D5 births (M copies) are the only births that can take those
  slots, through F2-dependent dead twins. Removing an L copy removes one such slot: raw R falls by 29 and reuse falls with it (reuse saves 74 of 112 M births instead of 102). Raw R is the wrong
  objective at this level; the five-stage and s = 11 values are what move.
- **Six copies of D4(c) sums remain on the inlined DAG (the transversal-cover bound is 3); two are deleted above, the other four are hosts.** Each is read by a dim-6 rule and is the register that rule is built in. The sweep finds no alternative source for their content
  (up to three registers by `verify.py`; up to six in a larger run outside the package) at any legal frame. Inlining a D4(c) sum into any one of its consumers (73 single moves at the hierarchy level, exact chains, each recompiled and priced at five stages) never raises the saving: 63 lower it, 10 leave it unchanged. So R681 (all six gone) is not
  reachable by these moves.
- **The clearing gap is structural.** For the R687 raw word, the time-only floor is 509 registers and the frame-only slot-recycling floor 510; reuse reaches 687. Of 321 births that see a
  frame-compatible dead slot, reuse clears 115. 196 of the 206 failures are L-copy births that see exactly one dead pair slot at the L's frame. Clearing it (or building the copy on it) needs the complementary pair, which is
  held only by the pair's other chain (its next frame is the other L's, incomparable) or by the sources (their next read, a dim-6 top, does not contain the L frame). Both break nesting. Reuse with live
  helpers and sources as eliminators, with retargeting, with randomised relation choice (36 runs) and with an order hill-climb (20k evaluations) all stay at 687; ignoring only the live-chain frame windows (not legal)
  would reach 590.
- **Exact twins are all chains.** On R687 (raw word and final) the symbolic replay lists 893 overlapping pairs of registers with equal x-parts (500 rule/copy, 240 source/carrier, 120 carrier/carrier, 33 copy/copy).
  Merging a later twin's reads into the earlier register is frame-legal in none of them; there are no recomputations (a content formed again after its holder was destroyed).
  This is the transverse-chain structure behind the copy lower bound of #504, seen at the level of the emitted word.

The exploratory scripts behind these counts are not part of the package and `verify.py` does not rerun them (as with #504's flag search); it reruns the copy sweep that selects the deletions
and reports its classes in `EXPECTED.json` (`build.deletions.removable_by_class`).

## Checks (verify.py)
`--light` (about 3 minutes, no C++):
- Package integrity; the five upstream packages pinned in `SOURCE.json`, including #504 at head 35057a6.
- The word rebuilt from #504's frozen hierarchy (inline, pinned chains, deletions), byte for byte; `--discover-check` recomputes the chains.
- Copy anatomy and bound on the inlined DAG.
- PR #370's independent all-column checker and mutants on the word.
- The pivot upper bound, the witness, and the seeded annealing reproducing the pinned selection.
- The kernel rebuilt from the frozen exact selection (PR #443 exact replay and interface check), mixing regenerated, both byte for byte; the relaxed all-column checker on the kernel and mixed words.

Default (FULL) adds PR #443's parent verifier (`--quick` skips its historical regressions), the complex upstream (`--complex-upstream=DIR` reuses a verified one), C++ cohort legality, five- and eleven-stage
formal columns (R = 685), record mutants, Gram, the mix check with 4 mutants, eleven-stage geometry, parent template and audit, whole-residual hosting with the frozen selection
(`--discover-check` recomputes it with HiGHS), the hosted audit, and the assembly (both rational moments, invoice, bootstrap, 47 strict inequalities), compared with `EXPECTED.json`.

## Scope
Conditional, like its parents: the inherited compiler, dirty-helper, precision and analytic assumptions; #504's scope for the pivot maximum; the frozen HiGHS hosting selection; from PR #450 only Lemma M. No
unconditional theorem or Lean proof is claimed. The complex supplier is PR #442's; compositions with #471 and #484 are not rerun here (the bit side binds #484's figure only if c exceeds its complex b, and
that composition needs #504's `e8-r687-tensor-complex` wrapper pointed at this word).
