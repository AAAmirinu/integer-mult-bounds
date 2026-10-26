# Complete retained-copy and R22 composition

The released PR5774 retained-copy word composes with Joel Pulikkan's original
R22 block. The complete conditional saving is **κ = .00312204390**, an increase
of **.00000012263** over PR5774's .00312192127. This is a small complete gain.
The selected frontier remains unchanged, and the same five framework assumptions
remain. No large uniform word or rounded multiplier is materialized.

The result uses the exact released sources. PR5774 supplies thirteen retained
native conversions and seventeen changed helper targets. PR5739/5756 supplies
the R22 block and its rank-four basis. This package claims their complete
composition, not either source mechanism.

## Exact compatibility

The source word is PR5774 at
`7d6ec0cdef31d0c37b7d2563e709979caa0d5eae`. The R22 edit list is PR5739 at
`b93d749a0a895d260e87887170af5162bda461a4`. All eight literal source runs occur
exactly once and do not overlap. Helper741 has the expected input chart477,
and helper405 has the expected output chart477. The source already has chart1090
with exactly the R22 basis `[265,194,164,75]`; the constructor reuses it after
an exact equality check. It does not append a conflicting chart number.

`construct.py` applies every published edit and records its source position and
old/new hashes in HUNKS.json. All INIT, COPY and CLEAR events remain byte-equal
and in the same order. The public and owned label counts do not change.

Some scalar operations are reordered inside the large R22 block. Therefore
compatibility must not be justified by an unchanged scalar-event order.
`compatibility.py` instead computes the exact rational transfer matrix of each
old and new edit. They agree on all affected fields. The largest matrix is9×9;
the other scalar edit is2×2. The remaining edits contain only native moves.
No edit contains a COPY, INIT or CLEAR event. Since the edits are disjoint,
equal scalar transfers preserve the logical state at every external COPY.
Thus all thirteen retained copies read the same logical source values for
arbitrary inputs. COMPATIBILITY.json records the matrices and copy events.
A wrong scalar coefficient fails this check. Native frame validity and absolute
phases are checked separately by the complete replay.

## Complete changed invoice

The composition has767 arbitrary public inputs and22 owned labels, for789 scalar
input columns. It retains24 owned lifetimes, peak12 live owned fields and scalar
allowance224294. Its local profiles are:

| Kind | Exact profile |
| --- | --- |
| Paid | 2232 H1 + 454 H2 + 496 H3 + 97 H4 + 158 H5 + 7 H6 + 10 H7 |
| Helpers | 24 H1 + 5 H2 + 4 H3 + 104 H4 + 7 H5 + 7 H7 + 20 H8 + 388 H9 |

Relative to PR5774, the paid change is `H1+H4-H5`, and the productive change
is `-H1+H4+H5-H8`. The complete caller has18 local invocations,15 query shears
and3120 whole idle jobs. It has **13390 productive fields,66852 paid calls and
rank-mass surplus760**. Every retained copy, native query, main adapter, helper
normalizer, owned lifetime, route, scalar operation, boundary and idle remains
charged. The copied price implementation has only four explicit literal edits,
listed in PRICING-EDITS.json; the verifier checks them against the exact source.

Both rational moment engines pass. The raw crossing is strictly inside
`(.00312204392514,.00312204392515)`, and the derivative is negative throughout
the retained BIT range. The published saving leaves between2.514e-11 and
2.515e-11 below that raw ceiling. The tested saving is .003122043905. The source
16/17 completion, offset1/7 and decay125/128 remain feasible. The finite compiler,
all54 strict outer rows and all4 functional conditions pass. These checks price
the changed whole invoice; the source κ values are not added together.

## Scope of further optimization

PR5772 proves that the original fixed R22 block uses the best canonical chart
through the relevant exponent range. This composition keeps its exact block
interfaces. Joint changes to retained copies, source versions or other contact
charts are different contracts and remain open. The theorem does not claim an
optimum over all retained-copy words or arbitrary Clifford block assignments.

At submission, the second102-operation block in Discussion5125 is a separate
reserved contribution. An exact public artifact was requested for a stronger
composition. It is not reconstructed from its local finding. The asynchronous
hub and nonnested retained-copy work in Discussion5600 and the global owned-frame
search in5593 are separate. A newer compatible released artifact needs a fresh
source and overlap check plus a complete replay.

## Verification and provenance

Run `python3.12 -B scripts/research_package.py --package
research/p104-copy-block-composition`. The package registers normal and optimized
runs of the full verifier and the small compatibility verifier. VALIDATION.md
records the executed commands and the exact source/export boundaries.

The full verifier authenticates the complete19-file PR5774 export and every
nested source manifest before import. It checks all622521 scalar endpoint
coefficients, separate transpose columns, owned lifetimes,2923 distinct native
maps with absolute phases,208 main adapters,1118 helper normalizers, the complete
physical caller, both moment engines, finite compiler and every outer predicate.
The source local/native/caller engines are unchanged. Nine changed-word,
caller and invoice controls reject; the native phase control also rejects.

Frozen source bytes and notices are retained unchanged in this branch's own
history. Original source heads, blob IDs and SHA256 hashes remain explicit in
SOURCES.json. A clean scientific replay needs neither an unmerged source branch
nor network access. The optional full-history ancestry preflight is not run in
this shallow checkout. Hosted CI and independent scientific acceptance remain
separate from author-side checks and archive publication.

## Open next questions

1. Can another released block or changed contract compose with this word?
   Check the exact source interfaces and live claims, then price the full caller.
2. Can an independent reviewer accept the copy lifetimes, both R22 helper
   endpoints, scalar-transfer proof, complete invoice and inherited assumptions?

Ali Romman with substantial OpenAI Codex assistance. No subagents. Apache-2.0.
Credit PR5774, Joel Pulikkan/GamingPuzzled PR5739/5756, PR5751, flyingviper PR5718,
Cinna Davis, Jacob Alan Sussman, zxv, Cao Yifan and every retained P104/native/BIT
predecessor in NOTICE and the frozen source archive. No merge, closure or
selected-frontier change is performed.
