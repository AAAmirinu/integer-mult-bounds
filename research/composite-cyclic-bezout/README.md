# Exact cyclic-inverse certificates at six composite radices

**Independent verification / finite extension; no new κ.** Exact integer
Bézout identities certify that the q-Pochhammer kernel from Ali Romman's
[#621](https://github.com/CrocSwap/integer-mult-bounds/pull/621) has no
unit-circle zeros at radices **6, 10, 12, 14, 15, 18**, for **every primitive
root choice**. These are all non-prime-power radices between 3 and 18.
The identities give explicit lower bounds on the entire unit circle;
they are not sampled evaluations. The inherited Fourier argument then
bounds the inverse of `P(tau Z_L^w)` for every length L, integer stride w,
and unit scalar tau.

| Radix r | Primitive embeddings | Certified circle bound | Certified inverse ∞-norm bound |
|---:|---:|---:|---:|
| 6 | 2 | ≥ 2^-5 | ≤ 2^16 |
| 10 | 4 | ≥ 2^-8 | ≤ 2^27 |
| 12 | 4 | ≥ 2^-9 | ≤ 2^30 |
| 14 | 6 | ≥ 2^-10 | ≤ 2^33 |
| 15 | 8 | ≥ 2^-13 | ≤ 2^41 |
| 18 | 6 | ≥ 2^-11 | ≤ 2^41 |

These deliberately loose dyadic bounds follow from the exact rational
bounds in [EXPECTED.json](EXPECTED.json). No optimal conditioning claim
is made. [PROOF.md](PROOF.md) explains why a symbolic identity at each
radix covers all its primitive embeddings, the circle, and cyclic lengths.

## Reproduce

From the repository root, with Python 3.11+ and **no third-party packages**:

```sh
python3 -B -I -O research/composite-cyclic-bezout/verify.py --check research/composite-cyclic-bezout/EXPECTED.json
```

Expected output:

```text
PASS: 6 identities, 30 primitive embeddings, 39 negative controls
```

The checker constructs cyclotomic polynomials by exact integer division,
reconstructs every kernel coefficient from tail products, checks every
prefix/tail identity, and verifies the supplied Bézout coefficients using
integer polynomial multiplication and reduction. It imports neither SymPy
nor either #621 checker, and does not trust stored kernel coefficients,
bounds, resultants, floating-point calculations, or the generator.
All checks remain active under optimized Python.

Six mutations per radix break a Bézout coefficient, the denominator,
conjugation, reciprocal reversal, a kernel coefficient, or the second
Bézout term. Three further controls reject missing/duplicate radices and
a false witness for a polynomial with a unit-circle root. Those controls
exercise the identities directly, without relying on hash failures.

Focused verifier tests (including external corrupted-certificate rejection):

```sh
python3 -B -I research/composite-cyclic-bezout/test_verify.py
```

Optional deterministic certificate regeneration uses **SymPy 1.14.0**:

```sh
python3 -m venv /tmp/composite-cyclic-env
/tmp/composite-cyclic-env/bin/python -m pip install -r research/composite-cyclic-bezout/requirements-generate.txt
/tmp/composite-cyclic-env/bin/python -B -I research/composite-cyclic-bezout/generate.py --output /tmp/composite-cyclic-certificate.json
cmp research/composite-cyclic-bezout/CERTIFICATE.json /tmp/composite-cyclic-certificate.json
python3 -B -I -O research/composite-cyclic-bezout/verify.py --certificate /tmp/composite-cyclic-certificate.json --check research/composite-cyclic-bezout/EXPECTED.json
```

The generator uses SymPy's extended Euclidean algorithm over Q(u)[z] and
clears denominators. The independent checker only needs the resulting
83 KB [CERTIFICATE.json](CERTIFICATE.json). Regeneration takes about one
minute on the author's machine; checking takes less than one second.

## Scope, provenance and overlap

Base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`. At that base the selected
conditional bound remains κ = 51110230636731/31250000000000000 (#626/#543).
This package does not modify it, any supplier, or `upstream/`.

#621 establishes a uniform theorem for **prime powers**, with exact
examples at orders 3,4,5,7,8,9,11. It explicitly leaves other composites
outside its claim. Here, six separate certificates fill that finite gap;
there is no extrapolation to other radices or growing-family conditioning.
#628 concerns rounded prime-power inversion, dirty restoration and routing.
This package supplies no rounded implementation and does not certify #628.
No copied-information, helper, recurrence, or multiplication improvement is
claimed. A complete paid program, coefficient preparation, precision/error
propagation, scratch restoration and tape scheduling remain outside scope.

The finite certificates plus the written argument prove the stated fixed
radix properties subject to the usual exact-arithmetic checker trust. This
is not a Lean formalization or a formal verification of integer multiplication.
The Fourier/Parseval transfer is inherited mathematical analysis, not a new
finite-program verification.

[SOURCE.json](SOURCE.json) pins the base, #621 head and inspected source
bytes; [CLAIM.md](CLAIM.md) records seed **82**, task selection and overlap
checks; [VALIDATION.md](VALIDATION.md) records execution evidence.
Attribution and substantial AI assistance are in [NOTICE.md](NOTICE.md).
