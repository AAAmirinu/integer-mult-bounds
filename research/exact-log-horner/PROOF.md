# Exact endpoint-preserving integer Horner evaluation

## 1. Computational setting

The retained engine prices a finite histogram by enclosing

\[
 M(s)=\sum_{(t,c)}\frac{tc}{mW}\exp\bigl(s\log(m/t)\bigr).
\]

Some calls add a separately priced bad-residue surcharge. Counts and the validity
of the physical construction are inputs to this computation, not consequences
of this note. The selected assembly retains the surcharge for the bit supplier
and its conservative complex check, and omits it for the reviewed native
complex check. Those distinctions are unchanged here.

The engine reduces each logarithm to arguments in [1,2]. Its `log_unit` uses an
80-term rational atanh series. The expensive reference expression separately
constructs 80 rational powers and sums them. We change only how that *same
rational polynomial* is evaluated, leaving its remainder and every downstream
operation unchanged. No input-dependent result cache is introduced.

## 2. Original enclosure

For an exact rational x in [1,2], let z=(x-1)/(x+1)=a/b in lowest terms, b>0.
Then 0<=z<=1/3. The original lower and upper endpoints are

\[
 L_0=2\sum_{j=0}^{79}\frac{z^{2j+1}}{2j+1},\qquad
 U_0=L_0+\frac{2z^{161}}{161(1-z^2)}.
\]

These enclose log(x). In fact, the omitted positive tail is
2 sum_{j>=80} z^(2j+1)/(2j+1), bounded above by replacing every denominator
with 161 and summing a geometric series. At x=1 both endpoints are exactly zero.

## 3. Homogenized polynomial

Set

\[
 D=\operatorname{lcm}(1,3,5,\ldots,159),\qquad c_j=D/(2j+1).
\]

All c_j are integers. Define the homogeneous integer polynomial

\[
 N(a,b)=\sum_{j=0}^{79}c_j a^{2j}b^{2(79-j)}.
\]

Then, by multiplying out each summand,

\[
 \boxed{L_0=\frac{2aN(a,b)}{Db^{159}}},\qquad
 \boxed{U_0-L_0=\frac{2a^{161}}{161b^{159}(b^2-a^2)}}.
\]

The second identity follows directly from
z^161/(1-z^2)=a^161/[b^159(b^2-a^2)]. It is an equality, not a new approximation.
Every denominator is nonzero throughout the stated domain.

## 4. Horner recurrence and loop invariant

Initialize N_79=c_79. For j=78,...,0 evaluate

\[
 N_j=a^2N_{j+1}+c_jb^{2(79-j)}.
\]

Induction gives

\[
 N_j=\sum_{k=j}^{79}c_k a^{2(k-j)}b^{2(79-k)}.
\]

Thus N_0=N(a,b). In the implementation, `b_power` starts at b^2 and is
multiplied by b^2 after each of the 79 iterations. On exit it equals b^160;
its exact integer quotient by b is b^159. The final `Fraction` constructors
therefore return exactly L_0 and U_0. The zero numerator case requires no
separate shortcut and introduces no division by a.

This proves endpoint equality for **every exact rational x in [1,2]**. It is a
written algebraic proof of this kernel identity, not a formalized proof and not
a claim inferred from the finite regression grid.

## 5. Consequences and boundaries

For Fraction arguments x>=1, the unchanged `log_bounds` range reduction gives
the same k and reduced rational argument. Both its reduced logarithm and its
log(2) enclosure therefore remain identical. Its outward rounding at 10^-30
is unchanged. The twelve-term exponential and its tail are unchanged, as are
all histogram weights, final outward rounding, and surcharge additions.
Consequently, whenever the original exact-rational moment evaluation is in its
admitted domain, its lower and upper rational outputs remain identical.
Acceptance, rejection, and inconclusive cases based on those outputs are
therefore unchanged; this is stronger than merely keeping the same sign in
six examples.

The optimized standalone function explicitly rejects floating-point, string,
and other non-exact inputs. It accepts Fraction inputs and exact integer
endpoints 1 and 2. The equivalence claim concerns the original engine's
Fraction-valued arithmetic, not undocumented float behavior. No claim is made
about passing plain large integers to the original `log_bounds`, whose own
`/=` operation can enter floating-point arithmetic; that caller is unmodified.

The optimization replaces repeated rational powers/additions with 79 integer
Horner updates, two final Fraction constructions, and their final addition.
D and its coefficients are input-independent module constants. Large integer
sizes still depend on the input; empirical speedups are measurements, not a
claimed asymptotic complexity improvement. Import/setup time is excluded from
the reported warmed measurements, and no full replay speedup is established.

Supplier reconstruction, all 47 outer inequalities, the second rational engine,
source/compiler interfaces, common-label and mutable-basis realization, whole-
call hosting, precision/tape/exact recovery, analytic transfer and the complete
multiplication theorem are outside this contribution. No selected kappa changes.
