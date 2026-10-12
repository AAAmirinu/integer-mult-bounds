# Lean 4.21 port: stopped at the performance gate

This branch is a local port of the contribution at
`c4b1560a569f54064608bf88440f9e492c03fba3`. It has not been pushed. The
original review branch and PR #540 are unchanged. This document does not yet
claim a complete port, fresh full build, or CI pass.

Compilation stopped on 2026-10-12 at the requested three-times-baseline gate.
The ordinary `lake build FrameGeometry` target did not finish within 17.187
seconds (three times its recorded Lean 4.33 module time of 5.729 seconds).
The harness terminated the process group at 17.199 seconds. Its log contains
replayed dependency reports but no FrameGeometry success or compiler error.
This is a Lake-target wall timeout, not a measured isolated Lean compiler
duration or evidence that the theorem is false. There was no retry after
this stop condition. Further compilation requires a decision on this blocker.

The saved evidence is in [phase2-results/](phase2-results/). These are bounded
development probes, not fresh full-package receipts. In particular:

| Check | Lean 4.21 seconds | Lean 4.33 baseline seconds | Result |
| --- | ---: | ---: | --- |
| FrameData split certificate group | 645.939 | 2007.143 | Group built; common core reused |
| CoordinateSwap Lake target | 1.017 | 0.458 | PASS |
| AddressPairs Lake target | 0.866 | 0.418 | PASS |
| EndpointInterpretation corrected proof | 1.171 | 1.971 | PASS after one default-stack failure |
| FrameGeometry Lake target | 17.199 | 5.729 | Terminated at 17.187-second cap |

FrameData's result includes rebuilding all 42 certificate batches, the lookup
and facade, with the common core already available. Its seven public theorem
reports use only `propext`. It is useful performance evidence, but differs from
the old single-module measurement and does not establish a full-package speedup.
EndpointInterpretation's proof fix locally prevents eager unfolding of
`evalRow` and `Tree.tabulate`; it changes no theorem statement or external setting.

No complete fresh Task A/Task B receipt exists for this port, and the 931- and
21-declaration audits have not run for the full current package. The 30-minute
CI qualification remains open. Applying the stated 1.5-times slowdown and
20% margin to the FrameData group alone gives 19.38 minutes; remaining modules,
audits, setup and dependency preparation must still be measured and included.
This partial calculation is not a total CI projection.

Possible next steps are a bounded default-setting diagnostic to isolate the
FrameGeometry compiler time from Lake overhead, followed if necessary by
proof-body optimization, or retaining the already checked Phase 1 package as
the limited deliverable. Neither option permits weakening a theorem, raising
external resource limits, or claiming the unfinished full port has passed.

The target is upstream `formal/lean` at
`db0e57bc7f36b5ac0fc844ad7ce1396165ee6647`: Lean 4.21.0, compiler commit
`6741444a63eec253a7eae7a83f1beb3de015023d`, and Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3`. All nine Lake dependency revisions
match the upstream manifest. Only ordinary Lake compilation is accepted:
no externally raised stack limits, additional compiler options, or environment
tuning. Existing source heartbeat and recursion options are permitted.

## Inventory

The earlier count of 75 Lean files consists of 66 contribution files and nine
archived third-party snapshots. The nine files under
`review-receipts/external-overlap/raw/` remain byte-for-byte unchanged. They
are review evidence, excluded from Lake roots, CI compilation and axiom audits.
Two of the contribution files are distinct `Audit.lean` scripts; they must be
run separately, not merged into one module name.

The original Task B inventory remains 931 named declaration closures,
including `SourceInvocation.actualContract`. Task A has its separate inventory
of 21 declarations. These counts must not be confused with module counts or
compiler-generated auxiliary proof declarations.

## Certificate structure and permitted proof changes

FrameData's 944 frame certificates and 3,357 transition certificates are split
into 15 independent frame batches and 27 independent transition batches.
Shared definitions precede the frame batches; a shared frame lookup precedes
the transition batches. The existing `FrameData` import remains the facade.
There are 44 added modules. Every existing declaration name and type, every
literal witness, and the seven public theorem statements are preserved.

Generated certificate proof bodies use `decide +kernel`. Lean 4.21 documents
this tactic as checking the decidable proposition in the kernel once, avoiding
the duplicate reduction performed by ordinary `decide`. This is a source proof
change, not an external compilation option. It does not use native evaluation.
The same substitution is used in the generated port, frame-trace, ownership,
parent-ownership and move-check certificates. The permanent axiom audits must
still allow only `propext`, `Classical.choice` and `Quot.sound`.

FrameGeometry also makes the beta reduction before `Matrix.map_mul` explicit,
matching the proof adjustment established in the Phase 1 PortGeometry probe.
No mathematical scope is added.

## Validation gates

Development probes and incremental builds do not count as the final fresh
build. The final run must start with an empty local Lake build directory, use
ordinary `lake build` and `lake env lean` audits, fingerprint the toolchain and
dependencies, and recheck source extraction and package integrity.

Compare module port performance against isolated 4.33 module timings. Use the
complete parallel build for the CI projection. The planning model assumes
four cores, a runner 1.5 times slower than this machine, and a further 20%
safety margin, with setup and audit costs included explicitly. A projection
above about 30 minutes blocks completion under the requested 45-minute CI
budget; it is not a passing result.

The differential test is explicitly deferred to an independent Claude run on
the ported branch. It is not part of this port's validation claim or a blocker
for this phase.
