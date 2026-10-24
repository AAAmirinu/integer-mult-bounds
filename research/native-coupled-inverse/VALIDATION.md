# Validation record

Canonical source base: `1ec1119972c9aefe42525172d07b332fcff81cb4`.
Pending provider: PR5402 at `3348fccea855082786d5f0fc5558b73d4974e745`.
Environment: CPython 3.12.13, macOS arm64, standard library only.

The author replay passed the frozen provider's 641-column and 1,240 physical
binding checks. The new verifier passed both full inverse compositions on
632 original columns, all owned-zero checks, unchanged paid counts, the
separate inverse endpoint formula, 464 boundary adjoints, inverse child
phases for ranks 1 through 9, and three semantic rejection controls.

The registered normal and isolated optimized Python 3.12 replays passed.
All eight archived source files also matched their exact Git blobs at the
pinned PR5402 head. Publication/export checks are recorded below after
execution. Hosted CI is separate.

No complete caller, full multiplier, selected cold replay, full recursive
compiler or outer admission, independent human review, or formal proof-kernel
check was run. This package gives no new kappa.
