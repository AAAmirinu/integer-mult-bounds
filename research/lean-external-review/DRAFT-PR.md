Title: Check one literal PR442 invocation with multi-host Lean certificates

Upstream has incorporated #442 and the #509/#516 abstract stream-model
results. This contribution checks concrete obligations for one literal PR442
R747 invocation (stage 2, replica 0, pair 0 at
`4e16d001d505d4f21dd2bcfc44591f9be4c279bd`).

Task A generalizes the hosting contract to multiple hosts and recovers the
single-host theorems. Task B connects its 19,002-instruction word to that
contract, with Lean certificates for scalar endpoints, concrete ownership,
coordinate identities and COPY/ERASE guards, for arbitrary dirty Boolean
helpers and one explicitly clean, restored private temporary.

Merged #516 already proves abstract realization for arbitrary global state
under hypotheses. The contribution here is checking selected concrete
invocation obligations in Lean; it is not the first arbitrary-state theorem.
The [overlap review](https://github.com/cheesegrader/integer-mult-bounds/blob/lean/pr442-invocation-review/research/lean-external-review/MERGED-OVERLAP.md) covers
incorporated #509/#516 and draft #528.

Main declarations include `MultiHosting.multi_hosting`,
`MultiHosting.SingleHost.whole_hosting_recovered`,
`MultiHosting.SingleHost.physical_whole_hosting_recovered`,
`SourceInvocation.actualContract`, `selected_call_completion`,
`selected_native_completion`, `selected_native_realization`, and
`selected_temporary_restoration` (the latter names are in `SourceInvocation`).

The package is being ported to the project's exact Lean 4.21.0 / Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3` setup. Full fresh replay and CI
runtime qualification are pending; historical Lean 4.33 passes do not
establish this port. FrameGeometry now passes under the revised timing gate;
OwnershipData now passes after same-content partitioning and lookup flattening.
No full-port PASS is claimed.
The intended reproduction command after the documented
pinned dependency setup is:

```sh
make formal-pr442-verify
```

The ordinary Lake build uses no external resource overrides, extra compiler
flags or environment settings. The permanent audits retain 931 Task B
declarations, including `SourceInvocation.actualContract`, and 21 Task A
declarations. The port covers 66 original contribution files; nine unchanged
archived third-party snapshots are excluded from this build and its audits.
Certificate partitioning adds independent modules without changing theorem
statements. The full package must qualify below an approximately 30-minute
projection on a slower four-core runner before it is reported ready.
The differential test is delegated separately and is not a reported check here.

The exact upstream base is `db0e57bc7f36b5ac0fc844ad7ce1396165ee6647`.

Scope limits:

- One complete invocation; cross-invocation disjointness is not exercised.
- Pending ranges 15..21 and 1..28 are hand-supplied. Lean checks target-mask
  containment; nothing binds them to the source schedule.
- Explicit input embeddings, an invertible chart and `2 ≠ 0`; extraction is
  externally checked Python. Original-bank outputs remain auxiliary state.
- No full sweep, later scheduling, global-allocation equivalence, costs,
  all-size compilation, analytic transfer or κ result. PR448's gain remains
  unestablished. PR493 → PR472 → PR442 is provenance only.

Original construction and predecessor credits remain in the source notices.
Prepared with substantial OpenAI Codex assistance. The human participant
initiated and coordinated the effort and does not claim independent derivation
or personal checking of the mathematics. Agent reviews are not human audits.

No attribution requested; please don't add this account to CONTRIBUTORS.

Questions for maintainers:

1. Do the literal source binding, slot isometries, native operations and private
   initialization faithfully represent this invocation?
2. Is retaining all host/data/exterior outputs with explicit auxiliary bank
   outputs the right boundary for later scheduling proofs?
3. Where should these concrete certificates integrate with #509/#516 and #528?
4. The Lean 4.21 port is in progress. Once its fresh replay and CI budget pass,
   does the proposed Lake package and formal CI target fit the project layout?
