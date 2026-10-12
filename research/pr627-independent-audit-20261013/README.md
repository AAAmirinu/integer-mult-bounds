# Independent scoped review of PR627

PR627 at `f95308a9afa5adc071fe75c8cd7feec172503d4f` passes a fresh independent
execution of its strict 64-stage pipeline. It reproduces the conditional
finite-construction value
`408937459514291/250000000000000000 = 0.001635749838057164`, with no reused
baseline or provider locals. The run took 339.21 seconds on macOS with Python
3.14. All 51 receipt artifact hashes and 64 raw stage-log hashes were checked.
No substantive new construction or admission defect was found in this scope.

The final convenience wrapper was subsequently executed end to end in a second
fresh directory. Its strict replay passed all 64 stages in 337.80 seconds and
reproduced the same mathematical result; the separate owner checker and all
18 focused controls also passed. The two executions are recorded separately.

This is an exact-head audit, not a change to the repository's selected result.
The separately observed newer PR629 is outside this audit; no latest-frontier
or optimality claim is made. The new value exceeds the retained PR626 value
`0.001635527380375392` by `0.000000222457681772` (about 0.013602%).

## What was independently checked

The source comparison binds the downloaded GitHub commit archive and package
manifest. All 22 files in `code/` plus `verify.py` are byte-identical to the
retained PR623 predecessor. Source definitions are unchanged. WITNESS inputs
and EXPECTED outputs agree with SPEC, including the new recipe hash and the
EXPECTED-to-WITNESS hash. Dispatch triples are compared independently of their
serialization order; the separate call order agrees exactly.

Both raw helpers 581 and 590 now end at their specified dimension-seven
frames. The two absorptions write only dead data registers at their existing
frames. Each three-gate cleanup tail forms its linear combination before the
accumulator climbs. The inherited constructor checks this placement, the frame
chains and retained ends. The exact native auditor then checks arbitrary dirt,
target responses, both orientations, cone conditions, wrapper ordering and
paid profiles. The fresh pipeline also checks exact phase edges, physical
ownership, moment engines and all 47 outer inequalities.

The deterministic generator reproduces the exact decompressed recipe and raw
word. Its predecessor input was reconstructed from the retained PR623 recipe
on the freshly rebuilt identical hyperplane-ended input; this is not described
as a second full PR623 replay. The profile delta is `{1:+2, 2:+2, 5:-2}`, all
inherited ends are preserved, and the two width reductions free 256 units
across 64 JP8 calls. The owner exporter reproduces all 16,519 recorded moves
and the exact decompressed owner payload.

The independent checker in `check_native_owners.py` counts the actual native
forward and backward programs, derives each width from its endpoint frames,
checks all 35,424 roles, windows, families and disjoint compact intervals, and
recomputes the entire paid profile. Rank mass remains 520,704 and deficit
remains 2,560. It independently encloses the candidate moment below one using
the separate rational interval engine retained from Chafik Boukhalfa's PR626.
Four deliberate width, range, uniqueness and profile corruptions are rejected.

The contributor's focused 14 raw-word corruptions were rerun with a positive
control. Four additional controls remove each middle accumulator addition or
flip each final helper-write sign. All four are rejected at the arbitrary-dirt
endpoint check. These supplement the 38 inherited JP8 cold-end controls and
the complete strict replay; contributor validation receipts are not counted
as independent execution.

## Evidence and reproduction

`SOURCE.json`, `CORRESPONDENCE.json`, `EXPORTS.json`, `INDEPENDENT-OWNERS.json`,
`OWNER-CONTROLS.json`, `WRAPPER-GUARD-CONTROLS.json` and `VERIFIED.json` record
the scoped checks. The
`evidence/` directory contains the fresh result, receipt, stage list, top-level
log, all focused-control logs and a complete replay archive. The separate
`evidence/wrapper-run/` receipts, stage logs and focused-control evidence record
the later end-to-end wrapper execution.
`inputs/pr627-package.tar.gz` preserves the reviewed package bytes, including
its original notices; its SHA-256 is recorded in `VERIFIED.json`. `SHA256SUMS.json`
binds every retained file other than itself.

From the repository root, with Python 3.10 or newer:

```sh
PYTHON=python3 sh research/pr627-independent-audit-20261013/run_replay.sh /tmp/pr627-fresh-review
```

The script checks the frozen archive SHA-256 before extracting or executing
its code, checks package/source pins and runs the fresh full replay, separate
owner/moment check and 18 focused native controls. It uses the exact pinned
`larger_gain` source retained under `complex-k492-owner-repair/vendor`; the
top-level `research/larger-gain` manifest differs. The executed audit commands
used `/opt/homebrew/bin/python3` (3.14). An initial Python 3.9 attempt stopped
on the unsupported `Path.write_text(newline=...)` API and was discarded; the
successful run used a fresh output directory. The final convenience script was
then executed in a second fresh directory. Its archive and Python-version
guards also rejected corrupt input and Python 3.9 before creating a work
directory, including with `PYTHONOPTIMIZE=1`.

This audit did not rerun the whole repository `make verify` suite or Linux CI.
The PR543 bit supplier is cited and repriced rather than rebuilt. All-size
compilation, common-label and mutable-source realization, whole-call hosting,
precision/tape/exact recovery, analytic transfer and bit H1–H5 remain inherited
assumptions. This finite certificate is not an unconditional multiplication
theorem, a complete Lean formalization or a practical runtime result.

## Attribution

Jeremy Diviney contributed the two factored cold ends, deterministic generator,
owner repacking and original contributor controls in PR627, with OpenAI Codex
assistance. The construction retains Jeremy Kothe's PR622/PR623 K-triangle
line, DreamingOfClouds' cold-helper construction, the cumulative supplier and
verification lineage in the package notices, and eumemic's PR543 bit source.
The separate interval engine is retained from Chafik Boukhalfa's PR626.
Chi Zhao prepared this independent audit and additional checks with substantial
OpenAI Codex assistance. Apache-2.0; original notices remain in the frozen input
archive.
