# Batched Gaussian boundary solves

The retained phase-cell inverse solves the same banded boundary system for
many independent tensor lines. Grouping h right-hand sides, with h a power
of two comparable to the boundary width w, turns the two triangular solves,
Woodbury correction and local couplings into short square matrix products.
Exact Strassen products, rounded only at completed output boundaries, give
a conditional boundary factor `w^(log_2(7)-1)` in place of `w^2`.

With the exact inequality `7^16 < 2^45`, the Gaussian boundary margin can
be conservatively raised from `r-delta` to `(3+29r)/32-delta`. The precision
remains O(p), including a residual bound independent of the number of cells.
The [proof](PROOF.md) pays for batch grouping, sparse coupling pages, table
scans, cyclic endpoints, zero padding and returns on fixed tapes.

**No new kappa is claimed.** Per-axis Gaussian work, small-field exposure,
normalization and all supplier/assembly obligations remain. The current
selected minimum is unchanged when only this boundary row is raised.

Run with Python 3.11+ and the standard library:

```sh
python -B research/batched-gaussian-boundary/verify.py /absolute/new/output
```

The finite checks execute the new blocked program and compare it with
independent dense rational inverses. They cover signed cyclic systems,
near-singular wrapped pairs, ragged blocks, minimum cyclic dimensions,
empty wrap support, Gaussian-derived Schur systems, exact multiplication
counts, stable split/interleave layouts and six deliberately broken solves.
Complete Schur comparisons use the new rounded boundary and coupling maps
with an exact dense local inverse reference; they do not execute a full
Gaussian or multiplication tape machine. The all-size claim remains the
written conditional transfer, not an inference from finite tests or timings.

SOURCE.json pins all imported implementation files and the source reports.
The phase-cell, Schur and bulk microbox construction is inherited from the
RaD/hipotures reports retained in `references/semantic-bulk/rad20/`, with the
underlying Gaussian interfaces credited there. The seven-product identity
is Strassen's. New batching, accounting, proof and controls by chafreaky
with OpenAI Codex assistance. Apache-2.0.
