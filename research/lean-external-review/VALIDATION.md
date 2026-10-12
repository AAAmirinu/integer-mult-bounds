# Validation of the Lean 4.21 port

Exact upstream base: `db0e57bc7f36b5ac0fc844ad7ce1396165ee6647`.
The port is isolated from `lean/pr442-invocation-review` and PR #540.

## Current status: stopped; full verification pending

The Phase 2 probe stopped at the user-specified performance gate:
`lake build FrameGeometry` was terminated at 17.199 seconds after reaching
the 17.187-second cap (three times its 5.729-second historical module time).
There is no FrameGeometry PASS. Lake overhead and compiler time were not
separately measured. No compilation was retried after this stop condition.
See [the Phase 2 report](../lean-multi-host-source/PORT-PHASE2.md) and its
saved probe evidence. The successful split FrameData group is a bounded
development result, not a full fresh Task B replay.

The complete fresh Lean 4.21 package build, all audits and final CI runtime
qualification are **not yet reported as passed**. The target versions are
Lean 4.21.0 (`6741444a63eec253a7eae7a83f1beb3de015023d`) and Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3`, exactly matching upstream
`formal/lean`. The canonical completed receipt will be
`validation/lean421-fresh.json`, bound directly to the current
`../lean-multi-host-source/port-manifest.json`.

The earlier [Phase 1 results](../lean-multi-host-source/PORT-PHASE1.md)
cover a bounded subset only. They establish neither the full package nor
its final CI runtime. Further isolated module probes likewise do not
replace a complete fresh build.

The full run must compile all 147 local module roots without reusing local
artifacts, then check the original 931 Task B declarations, 21 Task A
declarations and three legacy contribution audits. Installed Lean, Mathlib,
transitive dependencies and artifact fingerprints must be recorded. Ordinary
Lake commands must work with the inherited default external settings.
Source heartbeat/recursion options remain permitted.

The contribution comprises 66 original Lean files (64 compiled modules and
two separately invoked audit scripts), with 83 additional modules from
same-content certificate partitioning. Nine archived third-party overlap
snapshots account for the remainder of the historical 75-file count. They
remain unchanged and inventory-hashed, but are outside this port's build,
CI and axiom inventory. The differential test is delegated separately and
is not a claimed result of this validation.

The runtime projection must account for a four-core GitHub runner slower than
this machine, using a stated slowdown and safety margin. The planning model
uses 1.5 times measured time plus a further 20% margin. The package will not be
reported complete if the resulting projection exceeds approximately 30
minutes; the upstream formal job's hard timeout remains 45 minutes.
Dependency-cache setup assumptions and any source-build fallback must be
reported explicitly.

## Historical Lean 4.33 evidence

`validation/task-a.json`, `validation/task-b.json`, their logs and
`validation/run-metadata.json` are retained at their original paths for
historical comparison. **They are not receipts for the current port.**
The 4.33 run completed Task B at 2026-10-12 03:19:37 UTC, compiling six Task A
modules and 52 Task B modules fresh and auditing 21 and 931 declarations.
It used Lean `d8b18978322de05a8f3dba51ef03cf5461676c17` and Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`.

That recorded fresh run fingerprinted the installed Lean distribution,
Mathlib, its eight dependencies and their artifacts before and after
compilation. Earlier historical Task B builds had not fingerprinted installed
Mathlib/dependency libraries. The later 4.33 fresh run records its own
libraries; it neither authenticates the earlier bytes nor establishes the
4.21 port. No historical receipt is reanchored as current verification.

## Integrity and limitations

The strict package verifier checks current file hashes, the canonical port
manifest and a matching fresh receipt. It fails when the current receipt is
absent. Preparation mode `--allow-pending-port` reports `PENDING_PORT`.
These checks inspect recorded evidence; they do not run Lean or authenticate
the origin of the receipt. [BUILD.md](BUILD.md) describes fresh reproduction.

Only standard Lean axioms are permitted. A count of named axiom reports is
not a count of new mathematical ideas. A project build against fingerprinted
public dependencies does not claim a fresh Mathlib rebuild or a
`leanchecker --fresh` audit of every imported constant.

Source fidelity, comparison boundaries and integration still require
maintainer review. Hand-supplied pending ranges remain unbound to the source
schedule; cross-invocation disjointness is not exercised. Full cover sweeps,
later scheduling, global allocation equivalence, costs, all-size compilation,
analytic transfer and κ remain outside the mathematical scope.
