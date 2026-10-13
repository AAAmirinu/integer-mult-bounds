# Sprint claim

- Track: independent verification; assignment seed **83**, drawn with the
  operating system's randomness by `secrets.randbelow(100)`.
- Base: `17ce0c79b7b51c2634b439ea5a2b754f09909693`.
- Object: the nonzero conjugate-reciprocal Sylvester determinant and its
  integral norm in Ali Romman's incorporated #621 prime-power inverse proof.
- Method: a new implementation using only split finite fields, evaluation,
  interpolation, and bounded integer CRT reconstruction; no imports from
  either existing cyclotomic-field checker. Check all primitive powers for
  radices 3, 4, 5, 7, 8, 9, 11, 16, 25, and 27. Seed 83 chooses the first
  split-prime search interval. Stop each reconstruction only after its CRT
  modulus exceeds a proved coefficient bound.
- Deliverable: an additive, standard-library verification package with exact
  determinants/norms, a reconstruction-bound argument, source pins, and
  negative controls. No new kappa or paid inverse program is claimed.
- Expected finish: 2026-10-13 03:38 UTC (20:38 America/Los_Angeles on Oct 12).
  Reserve the last 15 minutes for checks, overlap refresh, and handoff.

Three candidates considered: (1) this resultant identity; (2) K-triangle
dirty-input restoration; (3) star-decoder puncture thresholds. The selected
construction already has exact, local, and independent mod-p K-triangle
checks. #631 already supplies exhaustive flat/reader evidence for punctures.
For #621, the existing rational-field and SymPy checkers use nine inputs
through radix 11; this package changes both arithmetic method and coverage.
#628 independently develops rounded/dirty inverse programs and certificates
through radix 16. Its scope is credited but differs from exact resultant CRT.

At selection, all 478 open PRs were inspected by title; relevant #628/#630/
#631/#647/#657 bodies and #621/#628 comment timelines were inspected.
The central ledger marks #621 incorporated. No open sprint coordination
issue was found: the issue-only search returned only #650, a request to
enable Discussions. This claim is therefore recorded locally. No workers
are delegated. Prior negative results are left closed; this is a finite
identity check, not a reopened optimization search.

## Result update — 2026-10-13 03:15 UTC

Completed independent verification: ten radices through 27, all 80 primitive
embeddings, 193 split-prime runs, 2,918 determinant/adjugate evaluations, eight
exact predecessor matches, and eight negative controls. The proof establishes
a conservative bound for exact integer CRT reconstruction. Six additional
tests pass; Python 3.9/3.11/3.13 reproduce the same certificate. No new kappa.
The selected binding and original primary replay pass; the historical gen4
target passes. The broad suite stops at missing Boost headers in the unchanged
selected bit supplier. See [validation](VALIDATION.md).

Final overlap refresh inspected arrivals through #662: #661's fixed-order bit
frames and #662's Clifford performance work are disjoint. #628 remains at
`0768f97d06c623b8211e651543c66135796b62bf`; its rounded inverse work is credited.
The latest upstream changes only CONTRIBUTING.md.

Result: [review branch](https://github.com/swbiggart/integer-mult-bounds/tree/research/prime-power-resultant-crt-seed83/research/prime-power-resultant-crt).
The user supplied a fork; publication uses its existing SSH access. This is the
only result update to the local claim. No separate coordination issue or swarm
was created.
