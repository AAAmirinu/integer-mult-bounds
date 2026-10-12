# Uniform rounded cyclic inversion, with charged preparation and layout

This package advances the inversion step following PR621's circle bound.
It gives a uniform algorithm in the standard bit model for a prime-power
kernel applied to neighboring cyclic shifts. It makes **no new integer
kappa, complex b, BIT c, full multiplication, or practical-speedup claim**.

The main result in [PROOF.md](PROOF.md) uses precision `p+O(r^4)`, independent
of cyclic length `L`, and `O(r)` sequential array passes. With conservative
exact factor-product verification, its bit bound is
`soft-O((Lr+r^3)(p+r^4))`. Approximate factor preparation uses Pan's published
theorem, and elementary-function preparation uses standard fast algorithms.
Those worst-case algorithms are not implemented by the exploratory root
nomination script. Exact rational phases and certified approximations of
unit phases have explicit error and preparation budgets.

The package separates four claims and their evidence:

- [SCAN-PROOF.md](SCAN-PROOF.md): two rounded scans solve a stable first-order
  periodic factor, with error independent of cycle length.
- [CERTIFICATE-PROOF.md](CERTIFICATE-PROOF.md): ten exact factor certificates
  through radix 16, including inner roots and an irrational unit phase, each
  achieving error at most `2^-128` for every cycle length.
- [PROOF.md](PROOF.md): the general preparation, stability and precision
  argument, using the explicitly cited standard factorization theorem.
- [LAYOUT.md](LAYOUT.md): arbitrary strides via two charged merge sorts.
  Their `O(L(B+log L)log L)` cost can become `O(Lp^2)` when `B` and `log L`
  scale with `p`; this is not a free tape permutation.

The reference verifier uses exact rational and outward interval arithmetic.
It does not trust floating roots, use a hidden numerical library, or reuse
historical workspace artifacts. `nominate.py` only generates candidates;
verification imports neither that script nor its numerical root finder.

## Replay

Python 3.11 or newer, standard library only:

```sh
bash research/prime-power-cyclic-scan/verify.sh /tmp/cyclic-scan-fresh
```

The output directory must be empty. The wrapper checks complete source
hash coverage, replays all certificates under isolated optimized Python,
requires byte-identical deterministic outputs, rechecks source pins, and
writes every stage log plus `RECEIPT.json`.

Coverage includes 108 generic scan cases, 480 mixed-factor cases with 240
independent dense comparisons, 345 budget instances, 8384 stride mappings,
43 routed executions, and 22 malformed or corrupted controls in total.
Small samples support the reference implementation; the written arguments
and exact certificates establish the stated all-length bounds.

The remaining application work includes the transform's complete layout
and phase collection, composition through its recursion and precision
guard, normalization, and dirty-scratch restoration. The sorting route
does not by itself meet a faster application's I/O target. Source and
assistance attribution are in [NOTICE.md](NOTICE.md) and [SOURCE.json](SOURCE.json).
