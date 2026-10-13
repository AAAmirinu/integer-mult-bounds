# Independent integer CRT check of the prime-power resultant

This package independently corroborates one algebraic identity in Ali
Romman's incorporated #621 inverse proof: its conjugate-reciprocal
Sylvester determinant, complete Bezout identity, prime-ideal residue,
and exact integer norm. It uses split finite fields and bounded CRT,
with a separate integer quotient-ring replay and Bareiss norm calculation.
No predecessor verifier or symbolic-mathematics library is imported.

The completed finite domain is `r = 3,4,5,7,8,9,11,16,25,27`, with **80
primitive embeddings**. All eight published determinant/norm examples
match exactly, including their nontrivial primitive powers. Radices 16,
25 and 27 extend #621's exact-resultant replay domain. Adjacent #628 has
rounded kernel certificates through radix 16; this package adds a different
method and the two higher odd prime-power cases, rather than claiming
radix 16 was previously unchecked in every context.

The contribution is **independent verification**, with no new kappa.
The selected conditional result at the exact base commit
`17ce0c79b7b51c2634b439ea5a2b754f09909693` was
`51110230636731/31250000000000000 = 0.001635527380375392`, #626 with #543.
This package does not modify that record. `SOURCE.json` pins the immutable
predecessor inputs; selected-record/review context hashes are informational
snapshots, so a future selected result does not invalidate this replay.

## Reproduce

Python 3.9 or later; standard library only. From the repository root:

```sh
python3 -B research/prime-power-resultant-crt/verify.py --check research/prime-power-resultant-crt/RESULTS.json
```

Expected final line:

```
PASS 80 primitive embeddings; 8 predecessor matches; 8 negative controls
```

`RESULTS.json` records exact determinant coefficients and norms, every
split prime/root, evaluated and interpolated data digests, cofactor digest,
the coefficient bound, and the completed CRT modulus. Full Bezout
coefficients are regenerated and checked before success, rather than
assumed from a digest. No timestamps or machine-dependent values enter
the certificate. To write a fresh receipt, use `--output /tmp/new-file.json`;
the output must not already exist. The same checks remain active with
`-I -O`.

Additional proof-bound and failure-mode checks:

```sh
python3 -B research/prime-power-resultant-crt/test_verify.py
```

These compare two determinant engines and the adjugate column against
the independent permutation/minor formula, including singular matrices
with nonzero adjugates. They exhaust the trace dual-basis identity on the
entire radix domain and reject underfilled/corrupted CRT and source pins.
The scientific replay's eight controls include a unit-circle common
root, missing conjugation, changed resultant/cofactor, a nonsplit field,
and a non-prime-power radix. Rejection of radix six is a scope guard,
not evidence that its kernel is singular.

## Reconstruction and scope

See `PROOF.md` for the canonical coefficient bound. The stopping rule is
`M > 4 (2^r-1)^(2(r-1))`, where `M` is the product of auxiliary split
primes. Seed 83 chooses the initial prime search interval and is recorded
in `CLAIM.md`; it does not substitute for distinct mathematical coverage.
Every primitive embedding is used at every auxiliary prime. Singular
modular determinants are retained and handled by exact cofactor minors.

The finite replay does not formally prove the uniform inverse theorem,
analytic Fourier estimates, rounding, paid coefficient preparation,
restoration, tape/compiler interfaces, or integer multiplication. It
does not search for improved suppliers or rule them out. The additional
bound argument justifies the exactness of this finite reconstruction.

`VALIDATION.md` records completed checks and limitations. `NOTICE.md`
credits predecessor and concurrent work and discloses substantial OpenAI
Codex assistance. The scientific changes stay inside this new package;
one scoped workflow replays it on Linux/Python 3.11 and 3.13 without external
Python dependencies. `upstream/` and selected-frontier files are unchanged.
