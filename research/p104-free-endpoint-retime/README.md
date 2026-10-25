# Free helper endpoints on the P104 word (conditional kappa .0030814243)

Complete conditional kappa **.0030814243** (**+3.99e-5**, +1.31% over
[PR5551](https://github.com/CrocSwap/integer-mult-bounds/pull/5551)'s .0030415312). The claim is
tested at .0030814205; the exact raw crossing lies in
(15407121669/5000000000000, 308142433381/100000000000000) = (.00308142433380, .00308142433381).
A supporting word that needs only free helper *start* frames reaches **.0030768801** (+3.54e-5);
its exact crossing lies in (76922002003/25000000000000, 307688008013/100000000000000) = (.00307688008012, .00307688008013), tested at .0030768795.

**Conditional on** (a) the five framework assumptions retained by PR5544/5545/5551; (b) the validity
of PR5551, which is unreproduced at the time of writing; (c) **free helper START frames and free
helper FINAL frames**. For (c): the verifier checks only that each helper's initial frame is strictly
nested in its final frame and that the native boundary map has rank equal to the dimension gap; only
the X-initial and Y-final frames are literal (the 104 ports). The canonical-start rule exists only
in the #4610 compact-width verifier. Unmodified PR5544/5545 already has mid-frame helper starts
(23 distinct start frames, dimensions 0, 1, 4, 5) and mixed finals (18 distinct, dimensions 4, 5, 8, 9).
The headline word needs both (c)-starts and (c)-finals; the supporting word needs (c)-starts only. The
selected record is not changed; no independent human or proof-kernel acceptance is claimed.

## What the edit is (and is not)
This is **not** an unchanged circuit. Relative to PR5551's pinned word (`inputs/pr5551-WORD.json.gz`):
- The scalar program is identical: the same 21,686 ADD/COPY/SCALE/INIT/CLEAR events in the same order
  with the same registers and coefficients (no register merge or reordering).
- Only frame labels and MOVE stops change. The solve chose the subspace at every ADD-chart cluster
  subject to the verifier's nesting laws (an exact-lattice CP-SAT retime), and **170 stops became
  redundant and are deleted** (3,624 -> 3,454 MOVEs; 25,310 -> 25,140 events). The supporting word
  deletes 141 stops (3,483 MOVEs).
- Headline word: 168 helper start spans and 23 helper final spans differ from PR5551's (22 of the
  finals move from dimension 8 to 9); 607 scalar-event frame labels and 607 kept MOVE stops are
  relabelled (149 of those stops belong to main registers, whose intermediate frames move together with a
  helper in a shared ADD chart). Supporting word: 169 helper starts differ, 0 finals.
- All 208 main registers (104 X sources, 104 Y targets) keep identical initial and final spans, so the
  literal ports, the caller and the controller are untouched.
- Productive fields stay 12,814 and the rank-mass surplus stays 760; the credited helper profile moves
  (rank 9: 294 -> 425, rank 8: 122 -> 14, rank 7: 24 -> 0) and paid calls fall 69,912 -> 66,852
  (headline) / 67,374 (supporting).

## Files
- `WORD.json.gz` (headline, free starts + finals) and `WORD-STARTS-ONLY.json.gz` (supporting).
- `retime.py`: the CP-SAT solve is multi-worker and not byte-reproducible, so instead of a generator
  this exact stdlib checker proves a candidate is a legal retime of the pinned word: identical scalar
  program, MOVEs a subsequence of the pinned MOVEs, all 208 main endpoint spans unchanged, 104 ports
  and live list equal. Nesting, ownership, the common-chart frame law and rank = dimension gap are then
  enforced by the unmodified PR5545 `local.py` replay and `native()`.
- `pricing.py`, `pricing-starts-only.py`: PR5551's `pricing.py` (`inputs/pr5551-pricing.py`) with ONLY
  literal changes: the KAPPA/TESTED claim line, the call census 69912 -> 66852 / 67374, and the
  `kappa_decimal` label. `LITERAL-CHANGES.diff` shows them; `verify.py` re-applies the substitutions
  and checks byte equality. No `local.py` change is needed (735 public inputs), so the unmodified
  PR5545 `local.py` from the byte-pinned capsule is used.
- `verify.py` / `verify.sh` (stdlib, Python 3.12): `--part headline` and `--part starts-only`, each
  about 6 minutes: retime legality, replay, transposed columns, native maps, physical caller, pricing
  with both moment engines, all 54 strict + 4 functional outer checks, exact crossing interval.
- `inputs/pr5545-source-closure.tar.gz`, `inputs/pr5551-WORD.json.gz`, `inputs/pr5551-pricing.py`:
  PR5551's byte-pinned inputs (`SOURCES.json`).

## Independent audit
An internal AI audit (separate read-only Claude agent) reproduced an earlier version of this retime on
PR5545's word through the real replay/native/pricing stack, found helper credit and main endpoints
sound, and rated maintainer intent for free helper frames as unresolved, which is why this is
conditional. The PR5551-based words here are checked by `verify.py`; they have not had a separate audit.

## Credits
Builds on PR5551 (thu-nmrc) and the P104 word line of PR5544/5545 (aliromman; lineage
PR2305/2152/2219). The idea of a fresh helper starting at a non-canonical frame follows the
hand-off precedent of PR5472 (GamingPuzzled). All predecessor credit is retained.

Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.

## Open next questions

- Are free helper start frames (non-canonical, mid-frame) admissible in the P104 caller contract? Both words depend on it; the supporting word depends on nothing else.
- Are free helper final frames admissible? The finals-free gain is the difference between the two words (.0030814243 vs .0030768801).
- Can the retime be reproduced by a deterministic single-threaded solve, so a generator can replace the checker?
- Independent reproduction of PR5551, on which this package builds. Interaction with hand-off words such as PR5553 is not tested here.
