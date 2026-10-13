# Why the integer reconstruction is exact

This note justifies the reconstruction bound used by `verify.py`. It does
not replace Ali Romman's uniform inverse proof in #621, prove its analytic
transfer by enumeration, or construct a paid inverse program.

Use that proof's notation: `r = ell^a >= 3`, `n = r-1`,
`D = phi(r) = (ell-1)s`, and `s = r/ell`. For a primitive `r`-th root `u`,
let

```
a_j = product_(k=j+1)^(r-1) (1-u^k)
f(z) = sum_(j=0)^n a_j z^j
f*(z) = sum_(j=0)^n conjugate(a_(n-j)) z^j.
```

The columns of `S` are `f, zf, ..., z^(n-1)f, f*, zf*, ...,
z^(n-1)f*`, in increasing coefficient order. The object checked is
`R = det(S)`, with `b = adj(S)e_0` and `S b = R e_0`.
All entries, `R`, and all components of `b` belong to `Z[u]`.

For every complex embedding, the sum of the absolute values of the
coefficients of either polynomial is at most `H = 2^r - 1`.
Hadamard therefore bounds `|sigma(R)| <= H^(2n)` and every cofactor
by `H^(2n-1)`. Put `B = H^(2n)`; the same `B` bounds each embedding
of every reconstructed object.

We need a bound on **canonical integer coefficients**, not just complex
absolute values. Write an object as

```
x = sum_(i=0)^(D-1) c_i u^i,     c_i in Z.
```

The prime-power cyclotomic relation is
`Phi_r(X) = 1 + X^s + ... + X^((ell-1)s)`. For `i = t + k s`,
where `0 <= t < s` and `0 <= k < ell-1`, the omitted index in the
same residue class is `j = t + (ell-1)s`. The root-of-unity trace is

```
Tr(u^m) = D       if r divides m,
          -s     if s divides m but r does not,
          0      otherwise.
```

This follows by subtracting the sum over the nonprimitive roots from the
sum over all `r`-th roots. In particular,

```
Tr(x u^(-i)) - Tr(x u^(-j)) = r c_i.
```

Both traces have absolute value at most `D B`, since every embedding of
the root factor has modulus one. Hence

```
|c_i| <= (2D/r) B < 2B.
```

The checker conservatively uses the integer bound `C = 2B` for `R`
and every component of `b`. A CRT modulus `M > 2C` uniquely determines
all their coefficients in `[-C,C]`. No heuristic stopping criterion,
floating calculation, presumed coefficient size, or comparison to the
old certificate is used to terminate reconstruction.

# Split-field evaluations

Each auxiliary prime `p` is proved prime by trial division and satisfies
`p = 1 mod r`. An element `omega` is checked to have exact order `r`:
`omega^r = 1` and `omega^(r/ell) != 1`. The primitive powers of `omega`
are the `D` distinct roots of `Phi_r` in `F_p`.

At all those roots, the checker forms `S` directly from evaluated tail
products. Gaussian elimination yields its determinant and the adjugate
column. For a singular evaluation it computes cofactors as minor
determinants instead; a vanishing determinant at an auxiliary prime is
never discarded. Every evaluation checks `S b = R e_0`. Lagrange
interpolation uniquely recovers the degree-below-`D` coefficient vectors
modulo `p`, and checks its values at all `D` points. These are precisely
the reductions of the canonical integer vectors. CRT and the bound above
then reconstruct the exact integer vectors.

The reconstructed data receives additional exact checks in
`Z[X]/Phi_r(X)`, without finite-field division:

- conjugation fixes `R`;
- evaluating `R` at `X=1` modulo `ell` gives `(-1)^(n*n)`;
- multiplying the reconstructed cofactors by the independently formed
  integral coefficients gives the complete Bezout identity;
- fraction-free Bareiss elimination on multiplication by `R` gives its
  integer field norm, with every integer division checked for exactness;
- this norm is a positive square and matches the product of determinant
  evaluations at every auxiliary prime.

All primitive root choices are covered simultaneously by the embeddings
used for interpolation. If the kernel uses `u^k` instead of `u`, its
resultant is the Galois substitution `R(u^k)`. The historical eight
examples are compared using this substitution, including powers 2 and 4.

# Coverage and limits

The completed finite domain is the ten explicitly listed radices in
`verify.py`. These checks corroborate algebraic identities used in #621;
they do not enumerate all prime powers or independently prove the uniform
circle/Fourier bounds. They do not cover other composite radices, numerical
rounding, preparation costs, scratch restoration, common-label compilation,
fixed tapes, or the multiplication theorem. No kappa improvement follows.

The trace calculation, interpolation, CRT, Hadamard inequality, and Bareiss
determinant method are standard. This contribution claims independent
implementation and additional finite evidence, not new versions of those
mathematical tools. Kernel and predecessor attribution are in `NOTICE.md`.
