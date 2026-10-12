# External review: one literal PR442 R747 invocation

**Lean 4.21 port in progress. The full fresh build and CI runtime qualification
are pending.** This local port branch has not replaced the public PR #540
branch. The historical Lean 4.33 receipts remain archived evidence, not proof
that the current sources pass on Lean 4.21.

Task A generalizes the hosting contract to multiple hosts and recovers the
previous single-host theorems. Task B connects that framework to the literal
PR442 forward invocation at stage 2, replica 0, pair 0, commit
`4e16d001d505d4f21dd2bcfc44591f9be4c279bd`: 19,002 events and 987 live
Boolean payload streams, with one explicitly initialized clean temporary.

The human participant initiated and coordinated this AI-assisted verification
effort and does not claim independent derivation or personal checking of the
mathematics. Codex agents developed proofs, checks and review materials;
agent reviews are not human audits.

## Scope

The statements quantify over arbitrary dirty helper payloads, an address
field with `2 ≠ 0`, and an invertible invocation chart. The comparison retains
every affected host/data stream and the exterior of the active owners;
original-bank outputs are threaded as auxiliary state. Lean checks scalar
endpoints, concrete ownership, coordinate transformations and chronological
COPY/ERASE guards for this invocation.

The multi-host theorem is applied to **one complete invocation**.
Cross-invocation disjointness is not exercised. Pending-coordinate ranges
15..21 and 1..28 are hand-supplied: Lean checks target-mask containment, but
nothing binds those choices to the source schedule. Completion performs the
remaining pending swaps immediately. Python extraction is reproducibly
checked, not a formally verified compiler; input embeddings remain explicit.

No full cover sweep, later recursive schedule, arbitrary global allocation
equivalence, physical cost bill, all-size compiler, analytic transfer or κ
result is proved. PR448's split-helper gain remains unestablished.

## Package and toolchain

The exact upstream base is `db0e57bc7f36b5ac0fc844ad7ce1396165ee6647`.
The port targets upstream `formal/lean` exactly:

- Lean 4.21.0, compiler commit `6741444a63eec253a7eae7a83f1beb3de015023d`.
- Mathlib `308445d7985027f538e281e18df29ca16ede2ba3`, with all transitive
  revisions fixed by `research/lean-multi-host-source/lake-manifest.json`.
- Source `set_option maxHeartbeats` and `maxRecDepth` declarations are allowed.
  No raised OS/Lean stack, build flags or environment overrides are required
  or accepted by the verification route.

The historical count of 75 Lean files means **66 contribution files plus nine
archived third-party overlap snapshots**. Those nine snapshot files remain
byte-for-byte unchanged and are inventory-hashed, but are excluded from this
port's builds, CI and axiom audit. The 66 contribution files comprise 64
compilable modules and two audit scripts. Certificate partitioning adds 83
support modules, giving 147 Lake module roots. Both original audit scripts
are run separately because each is named `Audit.lean`.

Every local dependency is included, particularly `CoordinateSwap.lean`,
`Hosting.lean` and `PhysicalHosting.lean` in
`research/lean-whole-residual-hosting/`. The permanent Task B audit still
contains the same 931 declarations, including `SourceInvocation.actualContract`;
Task A contains 21. Separate audits cover the earlier contribution files.
No theorem statement is intentionally changed by the port.

## Reproduction

See [BUILD.md](BUILD.md) for exact commands, including the upstream CI entry
point. The current verification route uses ordinary `lake build` and
`lake env lean`, a fresh local build directory, and pinned public dependencies.
There is no resume option. The differential test is separate work delegated
to another verifier and is not part of this port's reported checks.

[VALIDATION.md](VALIDATION.md) distinguishes current pending evidence from
historical passes. [MERGED-OVERLAP.md](MERGED-OVERLAP.md) records the incorporated
#442/#509/#516 comparison and draft #528; its historical port estimate predates
this in-progress implementation. [DRAFT-PR.md](DRAFT-PR.md) retains the proposed
technical pitch and maintainer questions.

## Review and delivery

The original public review is [PR #540](https://github.com/CrocSwap/integer-mult-bounds/pull/540),
on branch `lean/pr442-invocation-review`. This port is on a separate local
branch and must not be described as published before approval.

After committing a completed package, `export_review.py --output-dir` produces
a cumulative patch, portable archive, commit IDs and checksums. Apply only
that cumulative patch once to the exact upstream base above; do not combine
it with historical patches. `validate_delivery.py --delivery-dir ... --receipt ...`
checks archive hashes and isolated patch application. An archive already
contains the complete sources and needs no patch. Export validation requires
a current, complete fresh receipt; it does not turn pending checks into passes.
No export command pushes, publishes or opens a PR.
