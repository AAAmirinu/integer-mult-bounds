# Validation on the current upstream base

Exact upstream base: `db0e57bc7f36b5ac0fc844ad7ce1396165ee6647`.
Local review branch: `lean/pr442-invocation-review`.
The previous branch remains at `377012d9e1d350c29fc47669e82415249429f60c`.

All 75 included Lean source files are byte-for-byte unchanged from that prior
contribution. The permanent Task B declaration inventory now additionally names
`SourceInvocation.actualContract`, bringing it to 931 entries. No proof was
edited to pass a build.

## Current build status

**Fresh Task A and Task B replays: PASS.** Task B completed at
2026-10-12 03:19:37 UTC.

| Check | Current result | Evidence |
| --- | --- | --- |
| Task A | PASS: six modules freshly compiled, zero reused; 21 axiom reports | [fresh receipt](validation/task-a.json), [log](validation/task-a.log) |
| Task B | PASS: 52 modules freshly compiled, zero reused, zero legacy reused; 931 axiom reports including `SourceInvocation.actualContract` | [fresh receipt](validation/task-b.json), [log](validation/task-b.log) |
| Source extraction | PASS: six input hashes and all 19,002 events in order | [source receipt](validation/source-binding.json) |
| Package and delivery | Checked separately from Lean compilation; consult the separate receipts for their results | [package receipt](package-validation.json) and exported delivery receipt |

Task A started on 2026-10-12 and completed with `lean -t 0`. Task B started
after Task A passed. Both use Lean 4.33.0 at
`d8b18978322de05a8f3dba51ef03cf5461676c17`; Task B uses Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d` and its pinned manifest.

The unchanged Task B runner fingerprinted the installed Lean distribution,
Mathlib, all eight manifest dependencies, and their artifacts before compilation,
and recorded the same fingerprint afterward. Its completed fresh receipt
binds the current manifest, every module's source and artifacts, ordered
local dependency hashes, and all 931 axiom reports. The `actualContract`
report lists only `propext`, `Classical.choice`, and `Quot.sound`.

Task A accepts only `propext` and `Quot.sound`; Task B additionally permits
`Classical.choice`. These reports are transitive axiom inventories; a count
of named reports is not a count of new mathematical ideas.

## Integrity checks

```sh
python3 research/lean-external-review/verify_package.py
python3 research/lean-multi-host-source/check_sources.py
```

The ordinary verifier checks the package, manifested sources, source binding,
and both current fresh receipts. It requires direct manifest matches, complete
axiom inventories, and fresh Task B compilation with no reused modules.
These integrity checks inspect recorded evidence; they do not themselves run
Lean or authenticate the origin of the recorded build.

Current evidence is directly bound to current manifests. The earlier
metadata-reanchoring helper and receipt are no longer part of this delivery's
verification path. Original `replay-result.json` files and older review
receipts remain historical context; their 930-entry Task B inventories and
legacy reuse do not establish the current 931-entry result.

The old Task B compilation did not fingerprint its installed external libraries.
The completed current fresh build records those hashes for the new run.
It does not repair the historical receipt or authenticate earlier library bytes.
No project compiled module was reused in the current run. Installed public
Lean/Mathlib dependencies are fingerprinted; rebuilding Mathlib itself is not
claimed by the project replay. Nor is this a `leanchecker --fresh` audit of
every constant in the complete imported Lean/Std/Mathlib environment.

## Delivery and review limits

The exporter creates one patch from the exact upstream base above. Validation
unpacks the archive, checks file hashes and source regeneration, then applies
that patch to an isolated base tree and requires the committed result tree.
Delivery validation uses the ordinary strict checks, requiring both fresh
proof receipts. Its exported receipt records the result separately from the
Lean compilation receipts.

The historical `make gen4-bank-verify` PASS and timed-out `make verify` sweep
were on the older base. They have not been rerun on this upstream base and are
not current integration evidence. No upstream generator or `upstream/` input
was changed.

See [MERGED-OVERLAP.md](MERGED-OVERLAP.md) for the incorporated #442/#509/#516
comparison, draft #528, and the toolchain mismatch. The current changes do not
prove source scheduling of the hand-supplied pending ranges or exercise
cross-invocation disjointness. Full cover sweeps, later scheduling, global
allocation equivalence, costs, all-size compilation, analytic transfer and κ
remain outside scope.

The fresh project proof builds are complete. Maintainer review is still needed
for source fidelity, the comparison boundary, and integration with the
incorporated formal packages; a successful build does not settle those questions.
