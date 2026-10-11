# R687 compositions: read-then-climb bit supplier with PR #484's and PR #471's complex suppliers

The bit supplier is `research/e8-r687-read-then-climb`: R = 687 with read-then-climb phases, coset-split π-pairings and exact
kernel pivots. It is priced at eleven stages with PR #442 whole-residual hosting. **c = 65771650815860982499/(5·10²²) ≈ 1.315433·10⁻³**.

| complex supplier | b | κ | binds |
|---|---|---|---|
| **#484** (our draft; gauge80 + kernel42; conditional on its Lemmas A and G), cited from its pinned full-run result | 663394767670133/(5·10¹⁷) ≈ 1.326790·10⁻³ | **≈ 1.313705·10⁻³** | bit |
| #471 (Dugongue), rerun unchanged; #471's own assembler | 1305231506267591/10¹⁸ | 1303530097714685/10¹⁸ ≈ 1.303530·10⁻³ | complex |

How these compare with other published results:
- **With #484:** +1.32% over #483 (1.296607·10⁻³, the best bit-bound whole-residual κ before #493).
- **Below #493.** #493 (eumemic) posts a 489-helper bit word, c ≈ 1.565·10⁻³, which no longer binds. #493 with #484 gives
  1.325031·10⁻³, which is 0.86% above our #484 figure.
- **With #471:** κ equals #471's complex cap, the same value #493 reports with #471.
- **What this PR is.** A method and knowledge PR: the copy anatomy and lower bound, read-then-climb, and exact pivot certificates.
  It is not a κ record.

## Why the levers do not stack on #493
#493's word is a hand-built D4-quad skeleton generated from a plan, not a compiled pair ⊂ L ⊂ M hierarchy:
- 240 carriers plus 240 cell registers;
- each cell is delivered to its two quads;
- butterflies at the quad frames, then tops at the D6s.

Read-then-climb acts only where a symbol is low-read at its own frame and also consumed by a rule at a larger frame. That is the
M level of the #370 lattice, and #493 has no such level. Exact pivots and the hosting re-solve could still add bit-side saving. But
#493's c is already 18% above every whole-residual complex b, so they cannot change κ.

## Files
- `code/complex471.py` runs #471's complex supplier unchanged. It replays the exact command sequence of #471's verify.py without
  that file's bit part.
  - Integrity is checked against #471's MANIFEST. That manifest also lists a `.gitattributes` which is absent from the PR's git
    tree, probably a web upload of a dotfile. The entry may be absent (recorded in the RECEIPT); when present it is hash-checked.
- `compose.py` runs #471's `code/assemble.py` unchanged, with its bit inputs replaced by the R687 supplier's eleven-stage outputs:
  - two moments per supplier;
  - #471's bit invoice (product-bound prefix, row bound) and its complex stock, router and literal invoices;
  - six bootstrap levels;
  - 47 strict inequalities;
  - next-grid and parameter controls.
- `compose484.py` is #484's own per-supplier outer assembly (`assemble_gk.py`). It takes #484's pinned b and complex row
  coefficient and the R687 bit fields (c, charged coefficient 576 bits, row coefficient 28,416).
- `evidence/`:
  - the bit supplier's eleven-stage GLOBAL, AUDIT and a geometry summary, from the bit package's own run;
  - #471's complex GLOBAL and AUDIT from `code/complex471.py`;
  - #484's full-run RESULT and RECEIPT, from a run at #484 head d30a05f (manifest 435fb2f2…, pinned in SOURCE.json and
    asserted by `compose484.py`).

## Verification
`python -B research/e8-r687-tensor-complex/verify.py /abs/out --light` runs in minutes:
- package and upstream integrity;
- the bit word regenerated from its frozen hierarchy (byte check);
- the copy anatomy and bound;
- mixing regenerated (byte check);
- the relaxed all-column checker on the mixed word;
- both compositions on the pinned evidence.

Without `--light`, the FULL run:
- the bit package's full `verify.py`: PR #443 parent, PR #442 complex upstream, pivot certificates, all local, formal and
  eleven-stage checks, hosting and audits;
- #471's complex supplier rerun;
- both compositions on the fresh outputs;
- equality of the fresh outputs with `evidence/`.

#484 stays cited in both modes. Its own package verifies it.

## Scope
Conditional, like every parent. The #484 figure also carries #484's Lemmas A and G. No cross-copy or cross-family split is used.
No unconditional theorem or Lean proof is claimed.
