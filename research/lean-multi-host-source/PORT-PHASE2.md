# Lean 4.21 port: candidate awaiting fresh validation

This is a local port of `c4b1560a569f54064608bf88440f9e492c03fba3`,
on `lean/pr442-lean421-probe`. The public review branch and PR #540 are
unchanged. All development module probes pass. Full fresh validation and CI qualification
are still pending.

The exact target is upstream `formal/lean` at
`db0e57bc7f36b5ac0fc844ad7ce1396165ee6647`: Lean 4.21.0, compiler commit
`6741444a63eec253a7eae7a83f1beb3de015023d`, and Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3`. All nine Lake dependency pins
match that upstream manifest. Ordinary Lake commands use no externally
raised stack, compiler flags or environment tuning. Source heartbeat and
recursion options are retained as permitted.

## Inventory and preservation

The 66 original contribution files comprise 64 compiled modules and two
separate `Audit.lean` scripts. Certificate partitioning adds 89 modules,
for 153 compiled modules and a 141-module Task B closure. The nine archived
third-party snapshots are unchanged evidence, excluded from Lake roots,
CI compilation and axiom audits. Task B retains its original 931-declaration
inventory, including `SourceInvocation.actualContract`; Task A retains 21.
The other inventories contain 47, 422 and 15 declarations.

The lexical preservation check compares all 1,388 original named theorem
headers and active variable contexts across moved declarations. It finds no
changed, missing or added theorem statements and confirms all nine archive
hashes. This is a static source comparison, not elaborated-type equality;
name resolution and changed definition bodies still require separate review
and Lean checking. Generators separately check the embedded literal data.

## Mechanical changes

- MatrixData and FrameTraceLiterals use 39 support modules to avoid deep
  literal elaboration under the default stack.
- FrameData has 944 frame and 3,357 transition certificates in 15 frame and
  27 transition batches, with shared definitions and lookup. This adds
  44 modules. All existing names, types and literal witnesses are preserved.
- OwnershipData has a common core, an inverse table, four certificate groups
  and its original facade: six added modules. The inverse tree is represented
  by 510 named subtrees of at most 64 leaves each. Exact expansion reproduces
  every original branch and leaf. The twelve ParentOwnershipData lookup
  tables use the same verified flattening transformation.
- Generated certificate bodies use `decide +kernel`, ordinary kernel
  evaluation without duplicate tactic reduction. No native evaluation is used.
- FrameGeometry keeps large lookup tables abstract in two transition proofs.
  FrameLabelData and FrameTraceRoutes check existing chunks before flattening.
  SourceFramed derives its endpoint identity on an arbitrary store before
  applying it to the literal execution. SourceInvocationComparison selects
  outputs on schematic functions and rewrites whole-function wrappers before
  projecting the same literal folds. This avoids kernel conversion that would
  evaluate an entire execution beneath a payload projection.
  Other changes make beta reduction
  explicit or prevent eager unfolding during proof elaboration.

## Development measurements

These are incremental probes, not the final fresh package build. Compiler
process durations are sampled at approximately 0.1-second intervals where
available. The old 4.33 runner produced `.olean` files directly; ordinary Lake
also requests generated C. Ratios compare required workflows as well as
compiler versions.

| Probe | Lean 4.21 seconds | Lean 4.33 seconds | Measurement |
| --- | ---: | ---: | --- |
| FrameData split group | 645.939 | 2007.143 | Lake wall; common core reused |
| FrameGeometry | 12.2 | 5.729 | Compiler |
| FrameLabelData | 11.5 | 13.925 | Compiler |
| FrameTraceRoutes | 5.1 | 8.066 | Compiler |
| FrameMoveData | 84.5 | 87.031 | Compiler |
| FrameTraceCheckpoints | 146.1 | 104.650 | Compiler |
| OwnershipData split group | 13.080 | 23.158 | Lake wall; common core reused |
| SourceFramed | 2.528 | 7.365 | Lake wall |
| ParentOwnershipData | 65.372 | 58.768 | Lake wall |
| SourceInvocationComparison | 17.688 | 82.726 | Lake wall |
| SourceWord | 154.946 | 43.316 | Lake wall; 300-second cap |

The monolithic OwnershipData attempt exceeded 300 compiler seconds. An
isolated inverse-table diagnostic was deliberately stopped after 90 seconds;
it had no certificate proofs. This identified data processing as a bottleneck
without separating elaboration from C generation. After flattening, that
table compiled in about six seconds and all ownership certificates passed.

Historical `phase2-results/` describes the earlier snapshot at commit
`553ac9c37e2de0e2792d3bf5364c7b073fc633fc`, including the superseded
17.187-second FrameGeometry gate. Its source hashes and stop status are
historical, not current validation. Resumed evidence belongs in
`phase2-resumed-results/`; no historical receipt is reanchored as a fresh pass.

## Remaining validation gates

A new clean checkout must compile all local modules from an empty local
Lake build directory, run all five audits, check source extraction and
package integrity, and record installed toolchain/dependency/artifact hashes.
External pinned dependency artifacts may be reused with fingerprints.
The official Mathlib cache endpoint is blocked in this environment; that
restriction does not authorize network bypass or special compiler settings.

For historical modules above 60 seconds, the compiler limit is three times
the 4.33 baseline. Smaller modules have a 300-second limit, except ownership
work has an authorized 900-second per-module limit. The final timing model
uses a four-core runner at 1.5 times measured compute time, with a further
20 percent safety margin and explicit setup/dependency allowance. Completion
requires a total projection under about 30 minutes within upstream's
45-minute hard limit. A component timing alone cannot establish that result.

The differential test is delegated to an independent Claude run. It is
neither a reported pass nor a blocker for this port. No mathematical scope,
full-sweep claim, cost statement or κ result is added.
