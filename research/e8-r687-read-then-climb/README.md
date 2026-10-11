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

Every copied symbol has exactly two parent rules, and their frames meet only in the symbol's own frame. So the copies are fixed
by the DAG; frames, D-levels and mixing have no slack. (The two parent rules are pair ⊂ two L's, L ⊂ two M's, M ⊂ two top rules.)

## What is new
1. **Read-then-climb.** PR #370 puts every rule built from sources in phase A, before the scatter. Low reads at a symbol's own
   frame come after the scatter, so such a read can never share a register with a rule that uses the same symbol at a larger frame.
   Here a rule that reads a low-read symbol moves to phase B. Its register is read at F_u first, then climbs to the rule's frame.
   That is one chain where #370 needs two (`code/hier_word_rtc.py`; only the phase rule changes).
2. **Coset-split π-pairings.** In the tuned #370 parameters, both π-cosets of every block use the same pairing partition. So 28
   M sums are read at their own D5 frame by all four targets, and 140 are read only through rules. Shifting one coset's pairing
   spreads the D5 slots: 56 M sums are read at their own frame by two targets each. With read-then-climb each such M needs one
   chain, so M copies drop 140 → 112. An exhaustive per-block search over pairings × l5 and pairings × folds (raw R is
   block-separable) finds no better setting.
3. Stacked: the 2-term cancelling re-expressions of PR #463 (11 rules), then PR #443's reuse and #436's retime. The result is
   R = 687, followed by PR #450 mixing.
4. **Exact kernel pivots.** PR #443's shared-donor kernel needs a pivot selection: each helper whose first frame contains frame
   lines joins one rank-1 entrance class, and a class with members S yields |S| − rank(resp(S)) pivots. Maximising the pivots is
   therefore a min-sum-rank list partition over a linear matroid. `code/exactgen.py` solves it exactly per connected component,
   using block DP over span states and an exhaustive search over the coupling elements. The certificates computed by `verify.py`:
   - **R687: maximum 101** (components 190/26/12 give 78 + 15 + 8). The frozen selection attains it; parity leaves 100 rank-1
     pivots. PR #463's greedy search found 71.
   - **R715: maximum 112** (components 208/28/14 give 87 + 16 + 9). This closes the [112, 177] interval left open in our draft #485.
   `code/kernel_exact.py` is PR #463's kernel step with the greedy search replaced by the frozen selection, checked entry by entry. `code/mix_target.py` generalises the mixing to words
   whose phase B also holds helper rules: prefixes are compared per (register, version), and mix gates are placed by position.
   On words without B rules it makes the same choices as before.

## Copies: a lower bound (scope stated exactly)
- **Lemma (transversal cover; any legal word in this format).** Take a register chain holding u, and let G be the frame of its
  first use. Every target fed through that chain satisfies G ⊆ HYP[t], because frames only climb and reads happen in a common
  frame. Hence χ(u) ≥ the least number of proper sections G^⊥ (G ⊋ F_u) covering u's downstream targets. Targets reached through
  uses at F_u itself are excluded from this count. For u a source, this is PR #463's carrier lemma.
- **Theorem (the PR #370 pair ⊂ L ⊂ M lattice; any ls/pair/l5/fold flags; frame-pair D4 sums).**
  - (M) An M sum feeds 4 targets in its 3-dimensional F_M^⊥, and any 3 of them are independent. So one section holds ≤ 2 of
    them, and χ(M) ≥ 2 unless ≥ 2 readers read M at F_M. Each target has a single 5-dimensional flag level, so M copies ≥ 168 − 112/2 = 112.
    If all rules run in phase A (PR #370), low reads follow every rule use, and M copies ≥ 140.
  - (L) An L feeds 8 targets spanning F_L^⊥ (dimension 5), with ≤ 6 in any section, and no flag level of dimension 3. So L ≥ 168.
    D4(c) adds a third, incomparable reader to two L's per block: +28.
  - (pairs) 336 pair reads land on pairwise-incomparable L frames, and every cw source has 3 chains. So pair copies plus cw
    carriers ≥ 392.
  - Lattice copies ≥ 448, or ≥ 476 with the D4 assembly. With all phases A the bound is ≥ 504 (R715 has 528). R687 has 500.
  - `code/copy_bound.py` recomputes every χ by exact Dilworth and evaluates the lemma per symbol. R687: copies 500, bound 464.
    Under PR #370's phases the same DAG needs 556 copies. R715: 528, bound 492.
- **No bound on copies alone holds outside a fixed DAG.** The downstream target set is a property of the DAG, and copies trade
  one-for-one against fresh recomputation and cancellation. Only R (copies + fresh) could carry a design-free bound. None is known
  beyond PR #463's 240 carriers and #370's 240 hyperplane helpers.

## Checks (verify.py)
- PR #443's parent verifier.
- Hierarchy legality and the read-then-climb compile, regenerating the word byte for byte.
- Copy anatomy and the bound.
- PR #370's independent all-column checker and mutants.
- Exact pivot certificates (R687 = 101, R715 = 112), and the kernel from the frozen exact selection (PR #443 exact replay and
  interface check, regenerated byte for byte).
- Mixing regenerated byte for byte, and the relaxed all-column checker on both the kernel and the mixed word.
- C++ cohort legality; five- and eleven-stage formal columns (R = 687); record mutants; Gram.
- Mix check with 4 mutants.
- Eleven-stage geometry, parent template and audit.
- Whole-residual hosting with the frozen selection (`--discover-check` recomputes it with HiGHS), then the hosted audit.
- Assembly: both rational moments, invoice, bootstrap and 47 strict inequalities.

## Scope
Conditional, like its parents: the inherited compiler, dirty-helper, precision and analytic assumptions, plus PR #450's Lemma M
for target mixing. No cross-copy hosting lemma is used. No unconditional theorem or Lean proof is claimed.

