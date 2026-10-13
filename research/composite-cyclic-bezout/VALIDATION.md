# Validation receipt

Executed on 2026-10-12 America/Los_Angeles (2026-10-13 UTC), on macOS
14.4.1 arm64. Base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`.
This is local contributor validation with substantial OpenAI Codex assistance,
not independent human review or a full multiplication-theorem audit.

## Completed package checks

- Standard-library verifier: **6 identities, all 30 primitive embeddings
  covered symbolically, 39 rejected mathematical/coverage controls**.
- Public `-B -I -O --check EXPECTED.json` command passed under Python
  **3.9.6, 3.11.13 and 3.13.4**, with identical deterministic receipt bytes.
- **8 original focused tests** passed under each of those Python versions. They cover
  explicit cyclotomic formulas, conjugation, integer polynomial division,
  acceptance of an alternative valid scaled witness, outward dyadic bounds,
  corrupted-certificate CLI failures with and without optimization, malformed
  domain/encoding rejection, and full receipt recomputation.
- Fresh regeneration using Python 3.9.6 and, after the continuation,
  Python 3.11.13 / SymPy 1.14.0 / mpmath 1.3.0:
  `CERTIFICATE.json` reproduced byte for byte and the independently checked
  receipt matched `EXPECTED.json` exactly.
- The predecessor's standard-library `verify.py` reproduced
  `research/prime-power-cyclic-inverse/EXPECTED.json` byte for byte.
- `python3 -B scripts/verify_selected_result.py` passed: selected κ,
  source inventory and proof supplements retain their pinned content.
- `upstream/`, selected certificates, supplier code and root Makefile were
  unchanged. Only this new package and its scoped workflow are submitted.

## Continued modular lifting checks

- The exact seed identities at s=2,3,4 have denominators 3,43,37.
  The public isolated, optimized lifting check from the README passed on
  **Python 3.9.6,
  3.11.13 and 3.13.4** with identical receipt bytes: **54 admitted finite
  lifts, three excluded-prime common-factor witnesses and 173 rejected
  mutation/admission controls**.
- **8 additional focused tests** passed on all three versions (16 tests
  total). They cover excluded primes, exponent guards, division with
  reducible cyclotomic coefficient rings, reciprocal degree loss, rejection
  through the positive validation paths, and externally corrupted seed
  certificates under normal and optimized Python.
- Fresh `generate.py --lifting-seeds` with Python 3.11.13 / SymPy 1.14.0
  reproduced LIFTING-SEEDS.json byte for byte. The original six-certificate
  regeneration also remained byte-identical after adding this option.
- A separate Codex agent reviewed the all-exponent proof in LIFTING.md,
  including exact residue order, common-root integrality, Sylvester degree
  loss, and the inherited norm/cofactor exponents; no mathematical errors
  were found. A second agent reviewed the checker and improved the real
  rejection controls and negative-exponent guard. These are AI reviews,
  not independent human review or proof-assistant verification.
- Documentation links and whitespace checks pass. All inherited source
  pins still pass; the selected record and upstream content are unchanged.

## Broader repository verification

The initial sprint did not run root `make verify`. The continuation started
it with Python 3.11.13, NumPy 2.2.6, SciPy 1.15.3, SymPy 1.14.0, mpmath 1.3.0
and installed Boost headers in an isolated temporary environment:

```sh
env PATH=/tmp/integer-mult-full-venv/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin BOOST_INCLUDE=/opt/homebrew/include CPATH=/opt/homebrew/include make verify
```

The initial invocation passed the community/producer groups, earlier gen4
construction, selected #543+#626 cold replay, historical certificates,
ternary and research audits, and skip-strips checks. It then exited **2**
in `skip-suffix-producer`: Apple clang rejected the existing `-fopenmp`
option. This was a local compiler configuration failure, not a certificate
failure. No repository source or expected artifact was changed to resolve it.

The already installed **libomp 19.1.5** was used through a temporary CXX
adapter. It forwards arguments to `/usr/bin/clang++`, translates `-fopenmp`
to `-Xpreprocessor -fopenmp`, and adds the installed runtime's include/library
paths, rpath and `-lomp`. An OpenMP compile/run smoke check passed. The failed
stage and every remaining target were then resumed, preserving the completed
prefix of the original run:

```sh
env PATH=/tmp/integer-mult-full-venv/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin BOOST_INCLUDE=/opt/homebrew/include CPATH=/opt/homebrew/include CXX=/tmp/integer-mult-openmp-cxx make skip-suffix-verify verify-clones verify-positive verify-joint verify-pair verify-tests
```

The resumed command exited **0**, completing **all 84 test modules in
isolated interpreters** and all patch-application checks. Together, the
initial run and resumed tail cover every component of the root verification
sequence. Verification completed at 2026-10-13 **04:42 UTC**.

The cold selected-composition replay separately returned
`PASS_REBUILT_PR543_PR626_COMPOSITION` with exact
κ = `51110230636731/31250000000000000`. All six steps passed: bit543,
declarations, complex626, independent-owner, helper-interface and bindings.
Its inherited all-size, realization, hosting, precision/tape and analytic
assumptions remain conditional; finite replay does not discharge them.

Local console-log digests (run identification, not mathematical admission):

- Initial run, exit 2 at the OpenMP compiler flag:
  `d3fca41f0dd3b013c04b0f22144083c3d8639613a2fb345c948faab891d64460`.
- Resumed tail, exit 0:
  `8da6eaa07cdf6897776fe82357241f499d5e2a97096ab00fbb9bd026e87f7fc7`.

After regeneration, Git showed no changed files outside this research
package and its scoped workflow. The workflow requests Linux Python
3.11/3.14 checks, but GitHub reported no remote check results at handoff.

## Exact artifacts

- CERTIFICATE.json SHA256: `09623c781498d9c7df554f7e8f6e6c684cf3d9073db4198a4d647dcd2b6d4ab1`
- EXPECTED.json SHA256: `a33ed6b23d43562032fd88ef9969fae069e4817c17c81ab33000fb12fea1c928`
- LIFTING-SEEDS.json SHA256: `63fd8312f93d01818a9f43608f26844c2f1b65ab944a609f07994c4e766e02bb`
- LIFTING-EXPECTED.json SHA256: `4c8aa560141f9b03b42953f2b8ab35bce5866ee90f40e93743543f90fc2319f3`

These hash immutable submitted artifacts. Admission itself reconstructs and
checks every proof-relevant identity rather than accepting an artifact hash.
A reader can replace the certificate with a different valid witness.

## Live overlap check

The initial packaging refreshed **484 open PRs through #664**.
New #661 concerns fixed-order R420 frame optimality, #662 accelerates Clifford
checks, and #663 audits PR628 dirty restoration/leaf counts. Their stated
scopes do not duplicate the six non-prime-power Bézout certificates here.
#621 has no review comments in the inspected issue-comment endpoint; its
retained review and exact source head remain the dependencies. The repository
has no pinned coordination issue, so the claim and result are recorded locally.

The continuation refreshed **500 open PRs through #680**. New #673 develops
a multiway dirty-echo schedule and phase-alias repair based on #628 and
explicitly distinguishes this composite-nonvanishing package. #668 uses
split-prime CRT for prime-power resultants through 27; it supplies no
composite seed-lifting mechanism. The other new entries concern decoder
obstructions, local XOR circuits, owner maps, exponential intervals, supplier
boundaries, bit moments, selector batching and fixed Clifford words. No
overlapping composite lifting claim was identified. Upstream still points
to the recorded base and the pinned-issue list remains empty.

At final handoff, **533 open PRs through #714** were refreshed. #692 concerns
weighted-stride closure and bilinear duality and explicitly distinguishes
this composite-lifting result; #695 consolidates selected Linux replay
evidence. Later additions concern other suppliers, local circuits, moment
or wrapper audits, tooling, and dirty-call scheduling. No duplicate
composite seed-lifting mechanism was identified. The upstream base is still
`66849e1475c930fd7732b1a0067ffee7e1e95f60`; there is still no pinned issue.
