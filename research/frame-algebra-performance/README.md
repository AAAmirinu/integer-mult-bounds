# Faster exact frame algebra

PR364's transcript verifier spends most of its time computing rational frame
ranks and canonical row-space keys. `exact_rows.py` supplies the same exact
results using arbitrary-precision integer elimination, reducing Fraction
allocation and normalization inside the elimination loops.

The packaged local full-verifier replay took **227.54 → 64.48 seconds (3.53×)**.
Its four transcript stages took **200.98 → 39.08 seconds (5.14×)**; the rest took
26.57 and 25.40 seconds respectively. A separate kernel profile attributed 33.66 of 40.78 seconds
to 42,627 rank calls. These are single-host, single-pair wall-time measurements,
not mathematical-search throughput or a community-wide speed guarantee.

This package makes that experiment reproducible and provides a standard-library
utility for other construction/search code. The pinned upstream package is
PR364 at `f8c6a47abfec24b87cb1eb0a138dd73dfce2abe4`, directory
`research/w3-design-t-staged-p10b-reorder-mc`. SOURCE.json lists all 64 file hashes.

## Use the utility

Python 3.11 or newer, no third-party dependencies:

```sh
PYTHONPATH=research/frame-algebra-performance python -B - <<'PY'
from fractions import Fraction
from exact_rows import rank_q, key_of
matrix = [[1, 2], [Fraction(3, 7), Fraction(6, 7)]]
assert rank_q(matrix) == 1
assert key_of(matrix) == ((Fraction(1), Fraction(2)),)
PY
```

Both functions accept equally sized rows of integers or Fraction-compatible
values, do not mutate their inputs, and handle empty/zero-width matrices.
`key_of` returns the unique reduced row-echelon matrix as tuples of Fractions,
omitting zero rows, compatible with PR364's basis-key comparisons. Ragged matrices
raise ValueError. There are no floating-point or modular acceptance shortcuts.

To integrate it into another live codebase, replace its rank and canonical-RREF
helpers with these functions and retain that codebase's full validation. Changes
to frozen certificate packages require new manifests and dependency pins. The
adapter below keeps the original frozen package untouched.

## Why it is exact

Clear denominators independently in each input row. With a nonzero pivot p and
entry q to eliminate, let g = gcd(p, q), and replace the target row by
`(p/g) * target - (q/g) * pivot_row`. Its target-row multiplier is nonzero, so
this is an invertible row operation over Q. Dividing a nonzero row by its gcd is
also an invertible scaling; zero rows are left alone. Forward elimination counts
exact pivots for rank. Eliminating above and below pivots, followed by exact
Fraction normalization of each pivot, produces the canonical RREF. No bound on
integer size or denominator truncation is imposed.

## Differential tests

```sh
python -B research/frame-algebra-performance/test_rows.py -v
```

The suite compares the unchanged pinned Fraction helpers against the new utility
on 600 seeded rectangular/rational/singular matrices plus edge and large-integer
cases. It checks invariance under invertible row operations, input preservation,
generator inputs, and rank changes when dependencies are perturbed.

The 245 KB offline fixture covers every B/A pair in all five transcript snapshots:
69,857 original frame entries, 33,235 distinct B/A/Gram rank matrices and 13,847
distinct basis keys. All are compared exactly, including Gram nondegeneracy under
the source's `G = I - J/9`. Fixture and reference hashes are checked first.
`check_fixture.py /path/to/reference-replay` rebuilds the entire offline corpus
from the pinned full outputs and compares its decompressed bytes. CI also runs
this provenance check after the original full replay.

## Full shipped-verifier A/B replay

Requires bash, numpy 2.3.5, mpmath 1.3.0, a C++17 compiler and Boost headers.
The source and output paths must have no whitespace, as required by the original
shell verifier. Use fresh directories outside this package:

```sh
python -m pip install numpy==2.3.5 mpmath==1.3.0
python -B research/frame-algebra-performance/fetch_source.py /tmp/pr364-source
python -B research/frame-algebra-performance/benchmark.py /tmp/pr364-source /tmp/frame-replay
```

Use `--copy-from /existing/pinned/package` with the fetch command to copy and
validate an existing source without downloading. The benchmark accepts `--cxx`
and `--boost-include`, or the CXX/BOOST_INCLUDE environment variables. For medians,
use `--repetitions 3`; repetitions alternate reference/fast execution order.

For one fast replay:

```sh
python -B research/frame-algebra-performance/run.py /tmp/pr364-source /tmp/frame-fast --mode fast
```

`run.py` invokes the original full `verify.sh`, including its PR346 reconstruction
control. In fast mode, an external PYTHON launcher substitutes only `rank_q` and
`key_of` when invoking the original `stages.py`. Original source pins are checked
before and after. Every original stage assertion remains enabled, including frame
validity, nondegeneracy, source spans, COPY/ERASE lifecycle, all formal F2 columns,
official C++ legality/column checks, tiling, complex supplier and exact pricing.
The four mandatory transcript invocations are counted explicitly.
`check_refusals.py /path/to/pinned/source` verifies that tampered source bytes,
an existing output directory and Python `-O` are rejected before replay starts.

All 15 word/state/frame outputs in TT/K/KR/KRO/F must match the pinned original
snapshots byte for byte. Both modes must return exactly the same pricing receipt
after normalizing only its output-directory field, including
`kappa = 201219842699733/250000000000000000`.

Each run retains console.log, command timings, all original verifier outputs and
REPLAY.json. BENCHMARK.json records every run, medians, implementation/source
hashes, exact output hashes and pricing. Failed subprocesses do not produce a PASS
receipt. Successful arithmetic alone is never treated as completed admission.

## Scope and evidence

The complete shipped PR364 script starts with a pinned staged word; its optional
earlier producer regeneration is outside this benchmark. PR364 explicitly leaves
native bank/projector charts, geometry admission, finite invoice and prime/finite
obligations open. A successful replay retains that scope and all inherited
interfaces; this optimization establishes no new kappa or unconditional theorem.

`evidence/local-full-replay.json` records the packaged implementation's successful
full A/B replay, bound to its exact implementation/source hashes. Machine-specific
paths are normalized for publication. The earlier exploratory prototype timing
is retained separately in `initial-prototype-summary.json`.
Dedicated CI runs the offline suite on Python 3.11/3.14 and the complete A/B
verifier on Python 3.13. Local measurements use fresh output directories, without
saved PASS receipts or compiled binaries; the operating-system file cache is not
flushed. The benchmark does not enforce a speed threshold on shared CI machines.

See NOTICE.md and the retained original notice for construction/source credits.
