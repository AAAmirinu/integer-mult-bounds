# Independent execution receipts

The macOS and Linux receipts come from fresh complete invocations of
`research/e8-gauge-moment-hosting/verify.py`, with Python 3.14.8, actual Boost
multiprecision headers, and unchanged inherited source packages. The result
files are compared in full. The receipts retain the raw timing-dependent
parent hashes; the deterministic result normalizes only the inherited bit
geometry timer, as documented by the verifier.

The additional `preop-bounds.json` records a separate replay of #484's
headline local program. `checked_physics.py` wraps its integer-vector
operations with conservative bounds **before** each addition, multiplication,
shift, and Fourier primitive. The original post-operation guards also stay
active. Both orientations passed on 806 basis columns and eight dense dirty
columns; the largest intermediate bound was 377,135,104 (29 bits). This is
the supplied full-program sample, not exhaustive enumeration of its entire
409,600-dimensional input space. The source operators and the unmodified
512-column instance checks are covered separately by the parent receipts.

To reproduce this additional check after a fresh main run:

```sh
python -B research/e8-gauge-moment-hosting-validation/checked_physics.py \
  research/e8-complex-gauge-kernel/code/lemmaG \
  /absolute/verified-output/parent484 /absolute/new/preop-check
```

Its recorded input gzip hashes came from the earlier Python 3.12 replay;
that run passed the operator checks but failed the parent's final compressed
byte comparison. Changing only the gzip OS header from 3 to 255 yields the
published byte hashes. The complete release runs use Python 3.14 and pass
the unchanged parent comparison, including all four variants.
