# Modular lifting from an integral seed certificate

## Statement

Use the kernel f_r=r P_r and its conjugate reciprocal f_r* defined in
[PROOF.md](PROOF.md). Let s>=2. Suppose that, in Z[v,z]/(Phi_s(v)),

    A(v,z) f_s(v,z) + B(v,z) f_s*(v,z) = d,             (1)

where A,B have **integral** coefficients and d is a nonzero integer.
For every prime p not dividing s*d and every integer a>=1, set r=s*p^a.
Then f_r and f_r* have no common root, for every primitive complex r-th
root u. In particular P_r has no unit-circle zero.

The three independently checked seeds in LIFTING-SEEDS.json give:

| Seed s | d | Admitted family, a>=1 | Excluded primes in this argument |
|---:|---:|---|---|
| 2 | 3 | r=2*p^a | 2, 3 |
| 3 | 43 | r=3*p^a | 3, 43 |
| 4 | 37 | r=4*p^a | 2, 37 |

These are sufficient conditions. An excluded prime is **not** a
characteristic-zero counterexample. In particular the separate finite
certificates still cover r=6 and r=18 even though the seed-2 route excludes
p=3; the seed-3 route also covers r=6. No theorem for all composite radices
is claimed. Rational seed coefficients would require clearing and excluding
their denominators as well; (1) has already done so.

## Cyclotomic reduction

Since p does not divide s, the cyclotomic factorization gives

    Phi_(s*p^a)(x) = Phi_s(x^(p^a)) / Phi_s(x^(p^(a-1))).

For example this follows by classifying the orders of roots of the two
polynomials; the numerator has the denominator's roots plus exactly the
primitive s*p^a-th roots. Reducing the polynomial identity modulo p and
using the Frobenius identity yields, after cancellation in F_p[x],

    Phi_r(x) = Phi_s(x)^(p^(a-1)*(p-1))  (mod p).       (2)

The polynomial x^s-1 is separable modulo p. Its cyclotomic factors are
therefore pairwise coprime, so every root of Phi_s modulo p has exact
multiplicative order s.

Choose a prime ideal over p in a number field containing a primitive
r-th root u. Its residue v is a root of Phi_r, hence by (2) a primitive
s-th root in the residue field. This permits reduction of all integral
coefficients and of (1).

## Tail products and the reciprocal

The coefficient of z^j in f_r is

    product_(k=j+1)^(r-1) (1-u^k).

If j<r-s, its reduction contains the factor 1-v^(r-s)=0. If
j=r-s+t with 0<=t<s, periodicity v^s=1 turns the remaining product into
the coefficient of z^t in f_s. Thus

    f_r(v,z) = z^(r-s) f_s(v,z)  (mod p).              (3)

To form the reciprocal, first apply u -> u^-1 to every coefficient,
then reverse the full r coefficients. The same tail-product calculation
with v^-1 gives

    f_r*(v,z) = f_s*(v,z)  (mod p),                    (4)

with **no shift** on the right. Its constant term is 1. This substitution
is defined before reduction; it does not assert that v -> v^-1 is an
automorphism of an individual residue field or cyclotomic factor.

Equation (1) reduces to a nonzero scalar d modulo p. Therefore f_s and
f_s* are coprime over the residue field. Since f_s*(0)=1, it is also
coprime to z. Equations (3) and (4) consequently have no common zero.

## Lift back to characteristic zero

If f_r and f_r* had a common root alpha, choose a number field containing
u and alpha. The polynomial f_r is monic with algebraic-integer
coefficients, so alpha is an algebraic integer. Reduce the ring of integers
at a prime ideal over p. The image of alpha would be a common zero of
(3) and (4), contradicting their coprimality. This proves the statement
for any primitive complex choice of u. A unit-circle root of f_r would
also be a root of its actual conjugate reciprocal, so none exists.

For the quantitative argument below, the original 2(r-1) square Sylvester
matrix also remains nonsingular after reduction. Its first polynomial
stays monic of degree n=r-1, even though its second polynomial drops to
degree s-1. If A_0 f_r+B_0 f_r*=0 with both multiplier degrees below n,
coprimality implies f_r divides B_0, forcing B_0=0 and then A_0=0.
Thus the coefficient map is injective between equal finite dimensions.
Degree loss in the reciprocal does not invalidate this determinant claim.

## Uniform quantitative consequence inherited from #621

Put n=r-1, D=phi(r), and H=2^r-1. The preceding argument supplies the
nonzero resultant needed by Ali Romman's [#621](https://github.com/CrocSwap/integer-mult-bounds/pull/621).
The rest of its norm/cofactor proof does not require r to be a prime power.
For clarity, the estimates are repeated here.

At every embedding, the sum of absolute coefficients of either polynomial
is at most H, so the Sylvester determinant R satisfies |sigma(R)|<=H^(2n).
Its nonzero integral norm has absolute value at least 1. Since r>=3,
the chosen embedding and its distinct complex conjugate have equal
modulus, giving

    |R| >= H^(-n*(D-2)).

The adjugate matrix gives A_0 f_r+B_0 f_r*=R, where the 2n coefficients
are cofactors of absolute value at most H^(2n-1). On the unit circle this
implies

    |P_r(z)| >= delta_r := 1 / (2*r*n*H^(n*D-1)).       (5)

The Fourier/Parseval argument in PROOF.md then gives, for every L>=1,
integer w and |tau|=1,

    ||P_r(tau Z_L^w)^-1||_infinity
        <= delta_r^-1 + 2*n*H/(r*delta_r^2).            (6)

The logarithm of this upper bound is O(r^2 phi(r)), hence O(r^3), along
each admitted family. This dependence is very loose. It is not an
O(p polylog p) precision guard or a paid implementation. At the six
certified fixed radices, the direct rational bounds in EXPECTED.json
are substantially sharper and remain unchanged.

## What the executable checks establish

verify_lifting.py verifies (1) for s=2,3,4 with the separate integer
arithmetic engine in verify.py. It then checks 54 admitted instances with
r<=512 over the stated prime/exponent grid, including (2), literal tail
products (3)-(4), and an explicit modular Bezout identity for the lifted
pair. It computes in (F_p[v]/Phi_s(v))[z], without assuming this coefficient
ring is a field. Polynomial division uses only an invertible scalar
leading coefficient. For the lifted identity it uses z*U=1-f_s* and
U^(r-s) modulo f_s* to absorb the shift.

The finite checks test the implementation; they do not prove all exponents.
The symbolic argument above supplies that conclusion. Neither checker is
a proof assistant or a formal verification of the full multiplication
construction.

The excluded-prime diagnostics find actual common factors after reduction:

| s | p | Primitive residue v | Common factor of f_s and f_s* modulo p |
|---:|---:|---:|---|
| 2 | 3 | 2 | z+2 |
| 3 | 43 | 6 | z+24 |
| 4 | 37 | 6 | z^2+24*z+15 |

The last factor need not have a root in F_37; a nonconstant factor suffices
over its algebraic closure. These witnesses demonstrate the limitation of
this modular route only. See LIFTING-EXPECTED.json for the deterministic
receipt, including rejected corruptions and admission controls.

Prepared with substantial OpenAI Codex assistance, including a separate
agent review of the written reasoning. No independent human review or
literature-priority claim. Apache-2.0. The kernel, reciprocal method,
norm/cofactor estimate and Fourier transfer retain #621's attribution;
this contribution adds the seed-certificate lifting mechanism and checks.
