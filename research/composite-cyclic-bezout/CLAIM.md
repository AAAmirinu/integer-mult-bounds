# Sprint claim — independent verification

- Assignment seed: **82**, generated with Python `secrets.randbelow(100)`
  (operating-system randomness) on 2026-10-13 UTC.
- Track: independent verification or formalization (75–84).
- Exact base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`.
- Selected frontier at base: #626/#622/#623 with #543,
  κ = 51110230636731/31250000000000000.
- Started: 2026-10-13 03:04 UTC. Expected finish: 03:44 UTC.
- Object: the q-Pochhammer cyclic kernel of Ali Romman's #621,
  restricted to the non-prime-power radices 6, 10, 12, 14, 15, 18.
- Method: exact cyclotomic polynomial Bezout certificates for the kernel
  and its conjugate reciprocal, checked by a separate rational polynomial
  implementation. Include mutations that break conjugation or an identity.
- Deliverable: a finite, source-pinned nonvanishing certificate or precise
  obstruction, with one reproducible verification command. No new κ claim.

## Candidate selection and overlap

Three candidates were considered in this order:

0. Independent R420 bit scalar-boundary verification. Existing #612 and
   the retained independent bit engine already cover closely related checks.
1. Exact non-prime-power cyclic-kernel certificates beyond #621's theorem.
   Selected by seed 82 modulo 3 = 1, subject to the overlap check below.
2. K492 cold-helper/owner interface verification. The selected replay already
   includes independent owner/moment checking, and #633 audits factored ends.

Read CONTRIBUTING.md, the selected result, current status, central PR ledger,
the selected K492 construction/review, and preserved negative-result index.
The #621 theorem explicitly claims no non-prime-power result. Its two engines
cover orders 3,4,5,7,8,9,11; they do not certify the composite orders here.
#628 supplies rounded prime-power inversion, including dense and stride checks;
this experiment does not duplicate or certify its rounded implementation.
The prime-subset and other preserved search exclusions concern different
network/side-circuit models, not these polynomial identities.

All open PR metadata was inspected at claim time, including #628 and #634;
no non-prime-power cyclic Bezout contribution was identified. GitHub's
pinnedIssues query returned an empty list, so this claim is local per the
sprint instructions; no reservation issue was opened.

Reserve the final quarter of the work window for verification and handoff.
Prepared for Jason Willems (@at1as) with substantial OpenAI Codex assistance.

## Result — 2026-10-13 03:22 UTC

Completed: six exact Bézout identities establish unit-circle nonvanishing
for radices 6, 10, 12, 14, 15, 18, symbolically covering all 30 primitive
embeddings. The inherited Fourier argument gives explicit all-length
inverse bounds for these fixed radices. No new κ or general-composite
claim. All six nominated radices completed; no search was left pending.
The independent checker rejects 39 mathematical/coverage controls; eight
focused tests pass. Three Python versions give identical receipts, and
fresh SymPy regeneration reproduces the certificate bytes. See
[VALIDATION.md](VALIDATION.md) for the exact scope of execution.

Submitted one focused contribution:
[PR #666](https://github.com/CrocSwap/integer-mult-bounds/pull/666),
initial implementation commit `237d7fda614174e0784cbb2a8c22dfe4015efc94`.
The PR's base matches the recorded base exactly. GitHub reported no check
results at this handoff; local verification and remote CI remain distinct.
No pinned coordination issue existed, so this is the single local claim
result update. No other PR was opened or modified, and nothing was merged.

## Authorized continuation

The same PR now includes the specified infinite composite families proved
in [LIFTING.md](LIFTING.md), with the original six certificates unchanged.
See [CONTINUATION.md](CONTINUATION.md) for the extended claim, completed
result and final verification handoff. No new κ or all-composite theorem.
