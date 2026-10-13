# Composite cyclic inverses: exact certificates and modular lifting

**Independent verification and a composite-family extension; no new κ.**
This package studies the q-Pochhammer cyclic kernel from Ali Romman's
[#621](https://github.com/CrocSwap/integer-mult-bounds/pull/621). Small
integral Bézout certificates and a modular lifting argument establish
unit-circle nonvanishing for every primitive root choice at these radices:

| Infinite family, a>=1 | Condition on the prime p | Seed certificate denominator |
|---|---|---:|
| r=2*p^a | p not in {2,3} | 3 |
| r=3*p^a | p not in {3,43} | 43 |
| r=4*p^a | p not in {2,37} | 37 |

The general sufficient condition is: a seed certificate
`A f_s+B f_s*=d` with coefficients in Z[v] lifts to `r=s*p^a` whenever
p does not divide s*d. The proof reduces the integral tail-product kernel
to `z^(r-s) f_s`, and its reciprocal to `f_s*`, modulo p. Coprimality then
lifts back to characteristic zero. [LIFTING.md](LIFTING.md) proves this
for **all exponents**; the finite replay is an implementation check.
Excluded primes limit this modular argument, not the characteristic-zero
conclusion. No result for all composite radices is claimed.

Writing n=r-1, D=phi(r), H=2^r-1, the norm/cofactor and Fourier arguments
in #621 give the admitted families the explicit bounds

    delta_r = 1 / (2*r*n*H^(n*D-1)),
    |P_r(z)| >= delta_r                         for |z|=1,
    ||P_r(tau Z_L^w)^-1||_infinity
        <= delta_r^-1 + 2*n*H/(r*delta_r^2).

The inverse bound is uniform in L>=1, integer stride w and |tau|=1;
its logarithm is O(r^2 phi(r)), hence O(r^3). These loose analytic
bounds do not supply an efficient rounded implementation or a combined
precision guard.

## Stronger fixed-radix certificates

Six separate integer certificates cover all non-prime-power radices
between 3 and 18. They yield substantially sharper bounds than the general
formula, including cases excluded by a particular seed's lifting route:

| Radix r | Primitive embeddings | Certified circle bound | Certified inverse ∞-norm bound |
|---:|---:|---:|---:|
| 6 | 2 | ≥ 2^-5 | ≤ 2^16 |
| 10 | 4 | ≥ 2^-8 | ≤ 2^27 |
| 12 | 4 | ≥ 2^-9 | ≤ 2^30 |
| 14 | 6 | ≥ 2^-10 | ≤ 2^33 |
| 15 | 8 | ≥ 2^-13 | ≤ 2^41 |
| 18 | 6 | ≥ 2^-11 | ≤ 2^41 |

The dyadic bounds are rounded outward from exact rational bounds in
[EXPECTED.json](EXPECTED.json). [PROOF.md](PROOF.md) explains why the
identities cover every primitive embedding and the entire unit circle,
and repeats the inherited all-length Fourier transfer.

## Reproduce without third-party packages

Run from the repository root with Python 3.11+:

```sh
python3 -B -I -O research/composite-cyclic-bezout/verify.py --check research/composite-cyclic-bezout/EXPECTED.json
python3 -B -I -O research/composite-cyclic-bezout/verify_lifting.py --check research/composite-cyclic-bezout/LIFTING-EXPECTED.json
python3 -B -I research/composite-cyclic-bezout/test_verify.py
python3 -B -I research/composite-cyclic-bezout/test_lifting.py
```

The first two commands report:

```text
PASS: 6 identities, 30 primitive embeddings, 39 negative controls
PASS: 3 exact seeds, 54 modular lifts, 3 excluded-prime witnesses, 173 controls
```

verify.py reconstructs cyclotomic polynomials by exact integer division,
checks prefix/tail identities, and checks Bézout identities using integer
polynomial multiplication and reduction. It imports neither SymPy nor a
#621 checker, and does not trust stored kernel coefficients, bounds,
resultants or the generator. verify_lifting.py reuses that independent
arithmetic for its seeds and computes in `(F_p[v]/Phi_s(v))[z]` for the
finite diagnostics, even when Phi_s is reducible modulo p. It checks the
cyclotomic and tail-product reductions and constructs an explicit lifted
modular Bézout identity. All checks remain active under optimized Python.

Mutations test corrupted identities, missing or duplicate cases, omitted
shifts, incorrectly shifted reciprocals and invalid admission. Excluded-prime
witnesses show genuine modular common factors at (s,p)=(2,3),(3,43),(4,37);
they do not assert a complex-unit-circle counterexample. The focused tests
also check external corrupted-certificate CLI failure.

## Optional deterministic regeneration

Only nomination needs SymPy 1.14.0; the two checkers do not:

```sh
python3 -m venv /tmp/composite-cyclic-env
/tmp/composite-cyclic-env/bin/python -m pip install -r research/composite-cyclic-bezout/requirements-generate.txt
/tmp/composite-cyclic-env/bin/python -B -I research/composite-cyclic-bezout/generate.py --output /tmp/composite-cyclic-certificate.json
cmp research/composite-cyclic-bezout/CERTIFICATE.json /tmp/composite-cyclic-certificate.json
/tmp/composite-cyclic-env/bin/python -B -I research/composite-cyclic-bezout/generate.py --lifting-seeds --output /tmp/composite-lifting-seeds.json
cmp research/composite-cyclic-bezout/LIFTING-SEEDS.json /tmp/composite-lifting-seeds.json
```

The generator applies extended Euclid in Q(u)[z] and clears denominators.
The certificate generator is outside the checking trust boundary. The
written all-exponent proof is not generated by this program.

## Scope and provenance

Base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`. The selected conditional
bound remains κ = 51110230636731/31250000000000000 (#626/#543).
This package changes no supplier, selected certificate or `upstream/` file.

#621 proves a uniform prime-power theorem and supplies the kernel,
reciprocal method, norm/cofactor estimates and Fourier transfer used here.
The added result is a seed-certificate lifting mechanism for specified
composite families, plus six direct composite certificates and a separate
checker. #628 concerns rounded prime-power inversion and restoration;
concurrent #668 audits prime-power resultants with split-prime CRT. Neither
is certified or used as a dependency here. No paid coefficient preparation,
precision/error propagation, scratch restoration, tape scheduling or
integer-multiplication improvement is claimed.

The exact certificates and written proof establish the stated properties
subject to ordinary mathematical review and checker trust. This is not a
proof-assistant formalization or a full multiplication-theorem audit.
[SOURCE.json](SOURCE.json) pins the base and inherited source bytes;
[CLAIM.md](CLAIM.md) and [CONTINUATION.md](CONTINUATION.md) record seed **82**,
task selection, overlap checks and results. [VALIDATION.md](VALIDATION.md)
records execution evidence. Attribution and substantial AI assistance,
including separate agent reviews, are in [NOTICE.md](NOTICE.md).
