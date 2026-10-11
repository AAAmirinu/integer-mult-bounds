# R687: read-then-climb — fewer copies in the E8 bit word

**Bit supplier (exact; eleven stages; PR #442 whole-residual hosting with no cross-family split; target mixing):
c = 65771650815860982499/(5·10²²) ≈ 1.315433·10⁻³.** That is +2.358% over the R715 bit supplier (1.285129·10⁻³, PR #463),
from the same pipeline and hosting rule:
- read-then-climb with coset-split pairings gives 1.303868·10⁻³ (+1.458%);
- an exact maximum pivot selection for the kernel then adds +0.887%.

The compositions are in `research/e8-r687-tensor-complex`. Paired here with PR #442's complex supplier, κ is complex-bound, as
it was for R715.

## The copy term
In PR #370's compile, R = 9 totals + carriers + **copies** + fresh. Copies = Σ_u (χ(u) − 1), where χ(u) is the number of nested register
chains needed to read symbol u. On R715 they are 528 of the 839 raw helpers. Before reuse:

| | raw R | carriers | copies (pairs / L / M / other) | fresh | after reuse |
|---|---|---|---|---|---|
| R715 | 839 | 240 | 528 (184 / 196 / 140 / 8) | 62 | 715 |
| R687 | 811 | 240 | 500 (184 / 196 / 112 / 8) | 62 | 687 |

Most copied symbols (427 of 467 on R687) have exactly two rule parents whose frames meet only in the symbol's own frame: a pair
in two L's, an L in two M's, an M in two top rules. The exceptions are the 28 L's that also build D4(c) (three parents), 10
pair and 8/4 sums with 3–4 parents, one 9/4 sum whose parents meet above its frame, and one 16/6 sum with two deliveries and no
rule parent. Given the DAG, the copies still depend on the phase rule: the R687 DAG needs 556 copies under PR #370's phases and
500 with read-then-climb.

## What is new
1. **Read-then-climb.** PR #370 puts every rule built from sources in phase A, before the scatter. Low reads at a symbol's own
   frame come after the scatter, so such a read can never share a register with a rule that uses the same symbol at a larger frame.
   Here a rule that reads a low-read symbol moves to phase B. Its register is read at F_u first, then climbs to the rule's frame.
   That is one chain where #370 needs two (`code/hier_word_rtc.py`; only the phase rule changes).
2. **Coset-split π-pairings.** In the tuned #370 parameters, both π-cosets of every block use the same pairing partition. So 28
   M sums are read at their own D5 frame by all four targets, and 140 are read only through rules. Shifting one coset's pairing
   spreads the D5 slots: 56 M sums are read at their own frame by two targets each. With read-then-climb each such M needs one
   chain, so M copies drop 140 → 112. A per-block search over two slices of the flags (9 pairings × 16 l5 with folds fixed,
   and 9 pairings × 256 folds with l5 = 0; raw R is block-separable) on the hierarchy before the re-expressions found no setting
   with lower raw R. That search was run outside this package and is not re-run by `verify.py`.
3. Stacked: the 2-term cancelling re-expressions of PR #463 (11 rules), then PR #443's reuse and #436's retime. The result is
   R = 687, followed by PR #450 mixing.
4. **Exact kernel pivots.** PR #443's shared-donor kernel needs a pivot selection: each helper whose first frame contains frame
   lines joins one rank-1 entrance class, and a class with members S yields |S| − rank(resp(S)) pivots. Maximising the pivots is
   therefore a min-sum-rank list partition over a linear matroid. `code/exactgen.py` solves it exactly per connected component,
   using block DP over span states and an exhaustive search over the coupling elements. This is a computer-assisted exhaustive
   search. Its scope: the maximum over PR #443-format selections on the **retimed** pre-kernel word (PR #436 retime, 6 sweeps), with
   coordinate entrances (any rank reduces to one frame line per class) and one class per donor.
   - **R687: maximum 101** (components 190/26/12 give 78 + 15 + 8). The frozen selection attains it; parity leaves 100 rank-1
     pivots. PR #463's greedy search found 71.
     - By default, `verify.py` recomputes the lower bounds (upper bound 102 pivots) and checks the witness.
     - It also checks the pinned exhaustive log `data/pivot-certificate-r687.txt`: sum-rank 111 is refuted on the 190-element
       component, so 101 is the maximum.
     - `--certificate` reruns the refutation (about 30 min on a loaded 12-core machine).
   - **R715: maximum 112** (components 208/28/14 give 87 + 16 + 9). This equals the exact maximum claimed in our draft #485,
     recomputed here by a second solver. The log is pinned (`data/pivot-certificate-r715.txt`, 73 min on a loaded machine) and is
     not rerun by `verify.py`.
   `code/kernel_exact.py` is PR #463's kernel step with the greedy search replaced by the frozen selection, checked entry by entry. `code/mix_target.py` generalises the mixing to words
   whose phase B also holds helper rules: prefixes are compared per (register, version), and mix gates are placed by position.
   On words without B rules it makes the same choices as before.

## Copies: a lower bound (scope stated exactly)
- **Lemma (transversal cover; any legal word in this format).** Take a register chain holding u, and let G be the frame of its
  first use. Every target fed through that chain satisfies G ⊆ HYP[t], because frames only climb and reads happen in a common
  frame. Hence χ(u) ≥ the least number of proper sections G^⊥ (G ⊋ F_u) covering u's downstream targets. Targets reached through
  uses at F_u itself are excluded from this count. For u a source, this is PR #463's carrier lemma.
- **Theorem (hand proof).** Scope: the PR #370 pair ⊂ L ⊂ M lattice with frame-pair D4 sums. Assumptions:
  - rule gates execute at the hierarchy's frames (used in the pair and D4 steps);
  - each target reads along one nested chain, so it has at most one dimension-5 frame;
  - the 168 M frames are distinct.

  The steps:
  - (M) An M sum feeds 4 targets in its 3-dimensional F_M^⊥, and any 3 of them are independent, so one section holds ≤ 2 of
    them. A chain that starts with low reads at F_M can then climb and serve one section. So χ(M) = 1 needs ≥ 2 readers at F_M.
    With one dimension-5 frame per target, at most 112/2 = 56 M's reach χ = 1, so M copies ≥ 112.
    If all rules run in phase A (PR #370), low reads follow every rule use, so χ(M) = 1 needs all 4 readers at F_M: M copies ≥ 140.
  - (L) An L feeds 8 targets spanning F_L^⊥ (dimension 5), with ≤ 6 in any section, and no target has a dimension-3 flag level.
    So χ(L) ≥ 2 and L copies ≥ 168. Building D4(c) from L's adds a third, incomparable reader to two L's per block: +28.
  - (pairs) The 336 pair reads land on pairwise-incomparable L frames, so pair copies = 336 − n_p, where n_p is the number of
    distinct pairs. Each pair takes one chain from each of its two cw sources, and distinct pair frames are incomparable, so
    2·n_p ≤ Σ χ(s) over the cw sources. At the carrier bound (3 chains per source, met by R715 and R687), n_p ≤ 168, so
    **pair copies ≥ 168**. Without that assumption, pair copies + cw carriers ≥ 392.
  - Total: lattice copies ≥ 112 + 168 + 168 = 448, or ≥ 476 with the D4 assembly. With all phases A the bound is ≥ 504 (R715 has
    528). R687 has 500.
- **Machine-checked per DAG** by `code/copy_bound.py` (exact Dilworth recount plus the lemma), for each DAG and its #370
  low-read assignment (the own-frame targets depend on `choose_low`). `verify.py` runs it on both pinned hierarchies:
  - R687: copies 500, lemma bound 464; under PR #370's phases the same DAG needs 556.
  - R715: copies 528, lemma bound 492.

  These per-DAG figures use the lemma only. The +28 D4(c) Dilworth step is not in `copy_bound.py`, so they sit below 476.
- **No bound on copies alone holds outside a fixed DAG.** The downstream target set is a property of the DAG, and copies trade
  one-for-one against fresh recomputation and cancellation. Only R (copies + fresh) could carry a design-free bound. None is known
  beyond PR #463's 240 carriers and #370's 240 hyperplane helpers.

## Checks (verify.py)
- PR #443's parent verifier.
- Hierarchy legality and the read-then-climb compile, regenerating the word byte for byte.
- Copy anatomy and the bound.
- PR #370's independent all-column checker and mutants.
- Copy anatomy and bound on both pinned hierarchies (R687 and R715).
- Pivot lower bounds and the witness for R687 = 101, plus the pinned refutation log (`--certificate` reruns it).
- The kernel from the frozen exact selection (PR #443 exact replay and interface check, regenerated byte for byte).
- Mixing regenerated byte for byte, and the relaxed all-column checker on both the kernel and the mixed word.
- C++ cohort legality; five- and eleven-stage formal columns (R = 687); record mutants; Gram.
- Mix check with 4 mutants.
- Eleven-stage geometry, parent template and audit.
- Whole-residual hosting with the frozen selection (`--discover-check` recomputes it with HiGHS), then the hosted audit.
- Assembly: both rational moments, invoice, bootstrap and 47 strict inequalities.

## Scope
Conditional, like its parents: the inherited compiler, dirty-helper, precision and analytic assumptions.
- From PR #450 only Lemma M (bit labels) is used; #450's cross-copy hosting is not.
- #450's B-constancy step does not apply, because phase B holds 100 helper rules. The mixer's scalar identity is checked exactly
  on all 927 columns instead, together with the mix_check mutants.

No unconditional theorem or Lean proof is claimed.

