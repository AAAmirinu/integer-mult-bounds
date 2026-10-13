# Validation receipt

Executed on 2026-10-12 America/Los_Angeles (2026-10-13 UTC), on macOS
14.4.1 arm64. Base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`.
This is local contributor validation with substantial OpenAI Codex assistance,
not independent human review or a full multiplication-theorem audit.

## Completed checks

- Standard-library verifier: **6 identities, all 30 primitive embeddings
  covered symbolically, 39 rejected mathematical/coverage controls**.
- Public `-B -I -O --check EXPECTED.json` command passed under Python
  **3.9.6, 3.11.13 and 3.13.4**, with identical deterministic receipt bytes.
- **8 focused tests** passed under each of those Python versions. They cover
  explicit cyclotomic formulas, conjugation, integer polynomial division,
  acceptance of an alternative valid scaled witness, outward dyadic bounds,
  corrupted-certificate CLI failures with and without optimization, malformed
  domain/encoding rejection, and full receipt recomputation.
- Fresh regeneration using Python 3.9.6 / SymPy 1.14.0 / mpmath 1.3.0:
  `CERTIFICATE.json` reproduced byte for byte and the independently checked
  receipt matched `EXPECTED.json` exactly.
- The predecessor's standard-library `verify.py` reproduced
  `research/prime-power-cyclic-inverse/EXPECTED.json` byte for byte.
- `python3 -B scripts/verify_selected_result.py` passed: selected κ,
  source inventory and proof supplements retain their pinned content.
- `upstream/`, selected certificates, supplier code and root Makefile were
  unchanged. Only this new package and its scoped workflow are submitted.

The root `make verify` and cold selected-supplier replay were not run: this
additive, standalone arithmetic package does not change their inputs or
construction. The relevant new obligations, predecessor replay and selected
source integrity were checked. The workflow requests Linux Python 3.11/3.14
checks; a requested workflow is not evidence of a completed remote run.

## Exact artifacts

- CERTIFICATE.json SHA256: `09623c781498d9c7df554f7e8f6e6c684cf3d9073db4198a4d647dcd2b6d4ab1`
- EXPECTED.json SHA256: `a33ed6b23d43562032fd88ef9969fae069e4817c17c81ab33000fb12fea1c928`

These hash immutable submitted artifacts. Admission itself reconstructs and
checks every proof-relevant identity rather than accepting an artifact hash.
A reader can replace the certificate with a different valid witness.

## Live overlap check

Immediately before packaging, all **484 open PRs through #664** were refreshed.
New #661 concerns fixed-order R420 frame optimality, #662 accelerates Clifford
checks, and #663 audits PR628 dirty restoration/leaf counts. Their stated
scopes do not duplicate the six non-prime-power Bézout certificates here.
#621 has no review comments in the inspected issue-comment endpoint; its
retained review and exact source head remain the dependencies. The repository
has no pinned coordination issue, so the claim and result are recorded locally.
