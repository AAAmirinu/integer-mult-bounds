# Complementary reservoirs and routed top bits

The current compact FFT individually processes the axes used for its dirty
control fields. This creates the `c>q` reservation condition. Its extra top
bits also carry an `O(Vd)` bill.

This conditional construction removes both costs:

- Transform one half of the Fourier axes while the other half supplies
  complete dirty reservoirs; then exchange their roles.
- Route each exceptional top-bit round into a virtual chunk layout filled
  with existing unselected slots and apply the same fast core there.
- Use at most five global coordinate routes for an entire FFT, rather than
  one route per Fourier round. No Fourier axis is enlarged and no coordinate
  is added; the original temporary complete-zero-row padding is retained.

The resulting transform cost is
`O(V [p^tau polylog(p) + ell d^lambda_prime])`, under the source-pinned
compact-core, arbitrary-router, semantic-guard and synthetic-transform
contracts. The proof supplies complete-field capacity, chronology, opposite
normalization, precision and fixed-tape cost arguments. See [PROOF.md](PROOF.md).

**There is no new kappa claim.** Gaussian and scalar costs still bound the
current composition. This removes two implementation costs that would
otherwise remain even if those separate costs were improved.

Run with Python 3.11+ and only the standard library:

```sh
python -B research/complementary-fft-reservoirs/verify.py /absolute/new/output
```

The verifier checks 33 actual polynomial Fourier shapes against the closed
formula, 429 basis columns, 98,080 exact polynomial entries, real pass-layout
permutations, normalized opposite compositions, 84 complete common-field
layouts, 168 top-field layouts, and seven mutation controls. Four parameter
rows set c below q while retaining all 44 other strict expressions from the
reference assembly. Compressed rational/integer certificates provide eventual
capacity cutoffs, including the address-volume assumption for top layouts.

Tiny operator controls do not instantiate the large compact compiler;
capacity controls are separate, and the all-size transfer is the written
conditional argument. These checks do not measure a complete multiplier's
tape time. The unchanged #472 exponent appears only as an arithmetic reference.
They do not replace its source-bound supplier or release certificate.

All dependencies are pinned by exact file hashes and commit in SOURCE.json.
No pinned source is modified. New implementation and proof by chafreaky with
OpenAI Codex assistance; retained source attribution is in NOTICE.md and the
source texts. No literature priority or Lean certification is claimed.
