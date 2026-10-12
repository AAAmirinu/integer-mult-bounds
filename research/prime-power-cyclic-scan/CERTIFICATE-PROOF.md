# Mixed-direction finite certificates for cyclic kernel inversion

The reference program certifies ten prime-power kernel/embedding cases,
through radix 16, including kernels whose inverse needs both scan
directions. Each certificate proves absolute error at most 2^-128 for
every cyclic length L>=1 and every input of infinity norm at most 1.
The supplied factors use at most1024 fractional bits; arithmetic rounds
to768 fractional bits. Integer magnitude bits are additional.

This is a clean-array, neighboring-shift primitive. It does not establish
a new multiplication exponent, an arbitrary-stride tape program, dirty
scratch restoration, or the complexity of the exploratory root finder.

## Kernel enclosure independent of the root finder

For zeta=exp(2 pi i k/r), the exact kernel has

    P_j = (1/r) product_(s=j+1)^(r-1)(1-zeta^s).

The checker verifies that r is a prime power and k is primitive. It
encloses pi using Machin's identity and alternating-series bounds for
arctan(1/5) and arctan(1/239). For completeness, the identity follows
from tan(4 arctan(1/5))=120/119 and
tan(4 arctan(1/5)-arctan(1/239))=1, with the angle in (0,pi/2).
Multiplying by4 gives pi=16 arctan(1/5)-4 arctan(1/239).

The reduced angle lies in[-pi,pi]. The checker encloses its complex
exponential with the Taylor series and the conservative tail bound
128*4^(N+1)/(N+1)!, using |angle|<=4 and exp(4)<128. Every interval
operation rounds outward to a1536-bit dyadic grid. Taking powers and
backward products gives enclosures of all P_j. Correlations may widen
these boxes but cannot invalidate containment.

Two independent algebraic crosschecks cover the Gaussian radix4
coefficients and the radix8 coefficients in Q(sqrt(2),i). The latter
uses a separate4096-bit rational enclosure of sqrt(1/2), verified by
squaring. Its coefficient boxes must lie inside the trigonometric boxes.

## Factor certificate

The complex/Decimal script merely nominates dyadic roots rho_j. The
checker forms Q(z)=(1/r) product_j(z-rho_j) exactly and obtains an upper
bound epsilon on ||P-Q||_1 from the coefficient boxes. It classifies
the dyadic rho by comparing its squared modulus with1, and verifies
the claimed margin beta for rho (inner) or1/rho (outer).

Let A=r beta^(-(r-1)). Since

    (U-rho)^-1 = -rho^-1 (I-rho^-1 U)^-1       for an outer rho,
    (U-rho)^-1 = (I-rho U^-1)^-1 U^-1         for an inner rho,

we have ||Q(U)^-1||<=A for every unit-gauged cyclic shift U=tau S.
The checker proves epsilon A<1. A Neumann perturbation bound gives

    ||P(U)^-1-Q(U)^-1|| <= A^2 epsilon/(1-A epsilon).

This proves admissibility of the approximate factorization without
assuming any true-root correspondence or trusting decimal residuals.
It also accommodates repeated roots if nominated factors meet the same
coefficient and margin checks.

## Execution and rounding

Start with r times the input. An outer factor scans with coefficient
tau/rho and multiplies the result by -1/rho. An inner factor scans in
the opposite direction with coefficient rho/tau, performs the unit
cyclic shift, and multiplies by tau^-1. Every final scalar multiplication
is rounded to the working grid. Its modulus is at most1.

The single-factor rounding lemma fromSCAN-PROOF.md
therefore applies with per-stage bound7(B+1)u/beta^3, including the
final scalar multiplication, for u=2^-768. The checker uses

    E_0=0, A_0=r,
    E_j=E_(j-1)/beta+7(A_(j-1)+E_(j-1)+1)u/beta^3,
    A_j=A_(j-1)/beta.

It verifies the final sum of rounding and coefficient-perturbation
errors is at most2^-128. All inequalities are exact rational comparisons
and are independent of cycle length.

The reference tests exact phases1, i, and3/5+4i/5. It also constructs
an exactly rational unit sigma approximating tau=exp(2 pi i/7): a
certified chart has real coordinate at least1/2, its stereographic
parameter is rounded to1024 bits, and sigma is reconstructed by
(1-t^2+2it)/(1+t^2), with the chart rotation restored.
The exact enclosure proves |tau-sigma|<=nu<2^-1020. Its error is charged:

    ||P(tau S)-Q(sigma S)||
      <= epsilon + nu sum_j j |Q_j|.

The checker uses this larger perturbation in the same inverse bound and
again proves a2^-128 target. The irrational phase itself is not treated
as exactly rational, and its preparation is not assumed error-free.

## Evidence and reproduction

    python3 -I -O -B check.py --out CHECK-fresh.json

The finite suite covers six lengths1,2,3,8,17,64, both directions, four
phases, and ten kernel/embedding cases:480 cases. Half have independent
exact Gaussian elimination of the expanded cyclic matrix. All cases
check the expanded polynomial residual. Seven negative controls cover
a unit root, omitted factor, invalid embedding, insufficient precision,
false margin, omitted inner shift, and nonunit phase.

The inner-factor counts are1,2,3,4 at embedding1 of radices9,11,13,16;
the other listed cases have no inner factors. The certificates, rather
than these counts or the finite sample sizes, establish the all-length
error bounds. Fresh optimized-isolated execution must reproduce CHECK.json.

An initial run passed through radix9 but hit Python's4300-digit display
limit while serializing a rational bound for radix11. The explicit
serialization limit was increased to100000 digits; no mathematical
threshold was relaxed. Decimal root nominations and exact Fraction
arithmetic are reference tools, not a fast production implementation.

The general growing-radix argument is in
PROOF.md. Its standard factorization
algorithm is distinct from the exploratory nomination script here.
PR621, its exact-DFT source, and standard recursive-filter methods retain
their attribution. The code and explicit error-budget composition here
were prepared with OpenAI Codex for chafreaky; no priority claim is made.
