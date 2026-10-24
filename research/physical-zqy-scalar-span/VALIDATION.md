# Validation scope

Python 3.12.14, standard library only, macOS arm64. No dependency install,
Lean, Docker, selected cold replay or unrelated historical suite was run.

## Mathematical checks

- Exact source-bound native rows, all full-frame history versions and rational
  ranks: 4,891 /546, 5,019 /554 and 4,968 /554. Non-Y projection ranks match.
- The actual width-one operator rank is 214, with the exact four-term relation
  and a separate nonzero Gaussian-integer minor. Physical quotient projection
  lower bounds match exact rational upper bounds; no modular nonmembership
  shortcut is used.
- Width-two 215-by-215 Gram determinant is 298401053 modulo 1000000009.
  Every literal operator has zero-state coefficient one. The written
  contraction proof covers every larger width.
- Independent Clifford phase audit: 147,456 native columns, 36,864 product
  columns; wrong-phase and backward-direction controls.
- Fixed Z-ABI bank: 1,012 distinct left maps, 59 provider operators, 59,708
  pairwise distinct products and exact zero anchors. Exact signed F9 kernel
  checks authenticate physical/logical left multiplication. The written
  separating-functional proof has the explicit guard f>=59,707.
- Additional exact width-one Fraction audit passes without modular rank
  inference; its portable optional script and separate receipt are included.
  It ran in 90.663 seconds after import adaptation and 105.727 seconds after
  final whitespace normalization. Internal audit is distinct
  from external scientific acceptance; see INTERNAL-REVIEW.md.

All six registered normal/optimized commands PASS. The primary normal and
optimized mathematical runs took 134.403 and 157.388 seconds respectively.
Phase and fixed-ABI replays also PASS in both modes. Publication byte/export
transport checks are recorded separately in the pull request after commit. Individual commands use explicit
exceptions; mathematical checks are not disabled by `-O`. The retained
Clifford engine has its own assertion-based internals, while the audit's
literal column comparisons and negative controls remain explicit.

Development record: the first registered attempt rejected the result's JSON
key representation after completing its mathematical checks. Integer relation
indices are now serialized as strings. The revised result compares identically;
this repair changes no rank, source operator or scientific conclusion.

## Limits

No runtime measurement here is a physical fixed-tape benchmark. The frozen
source words and inherited Clifford realization are reused, not readmitted as
a new complete native supplier. No new paid or productive profile, exponent,
precision/tape/stock/compiler funding or multiplication theorem is claimed.
The finite ABI theorem is not arbitrary monomial group/module closure and
makes no enlarged-family small-width exclusion.
