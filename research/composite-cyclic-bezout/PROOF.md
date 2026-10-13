# Certificate-assisted nonvanishing at radices 6, 10, 12, 14, 15, 18

Let r belong to S = {6, 10, 12, 14, 15, 18}. Let u be any primitive
r-th root of unity, n = r−1, and

    h_j = 1 / product_(s=1)^j (1−u^s),
    P(z) = sum_(j=0)^n h_j z^j,
    f(z) = r P(z).

Every denominator is nonzero. Evaluating
`(x^r−1)/(x−1) = product_(s=1)^(r−1) (x−u^s)` at x=1 gives
`product_(s=1)^(r−1)(1−u^s)=r`. Consequently

    f(z) = sum_(j=0)^n a_j z^j,
    a_j = product_(s=j+1)^n (1−u^s).

This identity holds for every r≥2, without a prime-power hypothesis.
Each a_j is an algebraic integer. The independent checker constructs these
tail products and separately checks that each a_j times its corresponding
prefix product equals r in Z[u].

## The exact obligation

Define the conjugate reciprocal

    f*(z) = z^n conjugate(f(1/conjugate(z)))
          = sum_(j=0)^n conjugate(a_(n−j)) z^j.

For each r, CERTIFICATE.json supplies a positive integer d and two
polynomials A, B of z-degree less than n, with coefficients in Z[u], such that

    A(z) f(z) + B(z) f*(z) = d.                         (1)

Every coefficient is represented in the power basis
`1,u,...,u^(phi(r)−1)`, as signed decimal integers. Both dimensions of the
nested arrays are in ascending order: outer z-powers, inner u-powers.
No numerical embedding is used. The verifier reconstructs Phi_r from
`x^r−1 = product_(s|r) Phi_s(x)` and checks (1) by polynomial multiplication
and reduction modulo Phi_r. Neither a field inverse nor a gcd is needed
to **check** the certificate.

The generator uses extended Euclid in Q(u)[z] and clears rational
denominators. Its algebra system is not part of the independent checking
path. A nonconstant gcd would have stopped this nomination method; that did
not occur at any of the six stated radices. These six identities alone imply nothing about an untested radix.
[LIFTING.md](LIFTING.md) supplies a separate symbolic extension from three
small seed certificates to specified infinite families.

## Why all primitive choices are covered

Every primitive root u is a root of Phi_r. Substitution in the quotient
ring identity therefore gives (1) at **every** primitive embedding. Under
each such substitution, the automorphism `u -> u^(r−1)` used by the checker
is complex conjugation. Thus the polynomial labelled f* is the actual
conjugate reciprocal at that embedding, not just at one chosen root.
The respective numbers of embeddings are 2, 4, 4, 6, 8, 6, totalling 30.

Write the coefficients of A and B in that power basis and let

    C = sum of the absolute values of all those integer coefficients.

For |u|=|z|=1, the triangle inequality gives `|A(z)|+|B(z)| <= C`.
Also `|f*(z)|=|f(z)|` on |z|=1. Applying (1),

    0 < d <= (|A(z)|+|B(z)|)|f(z)| <= C |f(z)|.

It follows, for every primitive u and every |z|=1, that

    |P(z)| >= delta := d/(r C) > 0.                    (2)

The verifier recomputes d, C and the rational delta for each case; stored
bounds are never inputs to the identity check. The dyadic bounds in the
README are rounded outward by exact integer/rational comparisons.
In particular, there is no unit-circle root. This is stronger than
nonvanishing at any finite collection of cyclic eigenvalues.

## Inherited all-length inverse bound

This step repeats the Fourier argument of Ali Romman's #621 with the new
certificate-derived delta. It is not a new analytic theorem or a paid
implementation. Tail products give, for every primitive embedding,

    sum_j |a_j| <= H := 2^r−1,
    |P'(exp(it))| <= nH/r.

For `g(t)=1/P(exp(it))`, (2) gives

    |g(t)| <= delta^-1,
    |g'(t)| <= nH/(r delta^2).

Let c_k be its Fourier coefficients, with average-integral normalization.
Parseval applied to g', Cauchy–Schwarz, and
`sum_(k!=0) k^-2 <= 4` imply

    sum_k |c_k| <= delta^-1 + 2nH/(r delta^2) =: M.      (3)

In particular the Fourier series is absolutely convergent; it represents
g and its product with P has Fourier coefficients those of the constant
one. If U = tau Z_L^w, where |tau|=1, L≥1 and w is any integer, then each
integer power of U has induced infinity norm one. The matrix series
`sum_k c_k U^k` converges absolutely, has norm at most M, and multiplying
by P(U) gives the identity. Therefore

    ||P(tau Z_L^w)^-1||_infinity <= M.

No coprimality condition on w and L is required. This includes w=0 and
negative strides. Exact rational M values and outward dyadic bounds appear
in EXPECTED.json. Finite products inherit the product of these bounds by
submultiplicativity; conjugation by a unit diagonal preserves the norm.
These analytic consequences use only the explicit fixed-radix certificates
and the inherited Fourier argument, not the prime-power ideal argument.

## Limits and attribution

The prime-power proof in #621 has a uniform dependence on the radix.
The six literal certificates here give stronger fixed-radix bounds.
The separate lifting proof in LIFTING.md supplies a uniform estimate for
three specified composite families, not all composites. The bounds are sufficient, not optimal. This proves
no running-time, precision, preparation, reversible restoration, or tape
claim, and gives no new integer-multiplication exponent. The finite checker
is not a proof assistant or a formal verification of the full theorem.

Ali Romman supplies the kernel-conditioning problem, conjugate-reciprocal
approach and Fourier transfer. The kernel comes from the OpenAI exact-DFT
preprint and classical q-Pochhammer/Newton factorization; see the retained
source references and NOTICE.md. Prepared for Jason Willems with substantial
OpenAI Codex assistance. Apache-2.0; no literature-priority claim.
