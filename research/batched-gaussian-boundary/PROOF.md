# Batched boundary inverses for the retained Gaussian phase cells

This is a conditional refinement of one Gaussian cost row. It retains the
phase-cell matrix, interior Gohberg–Semencul maps, normalizations, prime
intervals, error interface, microbox construction and arbitrary-source router.
Those all-size interfaces remain assumptions. It does not prove a complete
integer-multiplication theorem or a new kappa. Finite checks below test the
new block program and its interface; they do not prove the tape transfer.

The source reports and implementations are pinned in SOURCE.json. The
seven-product square multiplication is Strassen's established algorithm,
not a new identity: V. Strassen, *Gaussian elimination is not optimal*,
Numerische Mathematik 13 (1969), 354–356, DOI 10.1007/BF02165411.
The [primary paper](https://courses.grainger.illinois.edu/cs357/su2013/Honors/Strassen.pdf)
was inspected on 2026-10-11. The contribution here is its application across
right-hand sides of the retained boundary inverse, with rounded-block
residual bounds and a paid small-field layout.

## 1. Scope and resulting row

Use p>100, d=Theta(p^epsilon), u=Theta(p^r),
w=ceil(sqrt(16p/u))+2, and the eventual cutoffs in the phase-cell report.
In particular u*d<=p, d>4w+2, 0<r<1, and the source cell lengths and
principal-window assumptions are unchanged. Tp=Theta(n).

Let omega=log_2(7). The boundary and coupling factor w^2 can be replaced by
w^(omega-1) when the many independent lines of the tensor are batched.
The complete bulk Gaussian application then costs

```
O(Tp * [p^tau polylog(p) + d polylog(p)
        + d p^delta + w^(omega-1) p^delta
        + d w^(omega-1) p^delta/L]) + n^o(1),
```

where L is the retained dyadic microbox length, L>=p^8. All constants may
depend on the fixed positive delta. This includes expansion, compression,
couplings, table traffic, grouping, cropping, and returns. It replaces only
the inverse-boundary terms of the pinned bulk row.

For an entirely rational exponent allowance, 7^16<2^45, so omega<45/16.
The boundary exponent is at most 29(1-r)/32+delta, giving margin

```
new_boundary = (3+29r)/32 - delta
old_boundary = r - delta
new_boundary-old_boundary = 3(1-r)/32 > 0.
```

The Gaussian local margin 1-epsilon-delta, gamma_sublinear condition
epsilon+r<1, small_field_exposure, balanced-prefix cost, compact FFT and
supplier conditions remain. In particular the current assembly has
1-epsilon-delta>minimum and r-delta>minimum; raising only the latter
cannot raise that assembly's selected minimum. No kappa gain is claimed.

## 2. Block the existing triangular factors

The source Schur matrix S on m=O(s*w/d) boundary vertices is circular-banded
with scalar half bandwidth v<=2w. For principal microboxes the count is
m=O(L*w/d+w), with the inherited endpoint treatment. Setup rounds S to the
P-grid, P=32768p, retaining positive diagonal, row gap >=1/(16p), and row
norm <2. Write the rounded matrix as A+U_border V, where A omits wrap
entries. The original Woodbury setup supplies

```
A=L_tri U_tri,
Z=A^-1 U_border,
K=I+VZ,
S^-1 B = X-Z K^-1 V X,   X=A^-1 B.
```

These symbols distinguish triangular factors from the microbox length L
and border injection. The inherited bounds are

```
||L_tri|| <=65p^2, ||L_tri^-1|| <32p,
||U_tri|| <2,     ||U_tri^-1|| <=1040p^3,
||A^-1|| <=16p, ||V|| <2, ||Z|| <=16p, ||K^-1|| <=33p.
```

Choose h=2^ceil(log_2(max(1,v))), so v<=h<2v<=4w<=4p eventually.
Partition each triangular factor into contiguous h-row blocks, retaining
a shorter last block. A scalar-band-v triangular matrix is block
bidiagonal. For a lower factor its equations are

```
D_i Y_i + E_i Y_(i-1) = B_i,
C_i=D_i^-1, F_i=-C_i E_i,
Y_i=C_i B_i+F_i Y_(i-1).
```

The upper solve uses the next block and the reverse order. All C_i and
F_i are computed exactly in setup, then rounded entrywise toward zero to
P fractional bits. There is no online inversion. The diagonal block of a
triangular inverse equals the inverse of its diagonal block; therefore
||C_i|| is bounded by the corresponding full triangular inverse norm.
Also ||F_i||<=||C_i||*||E_i||. All stored coefficients have polynomial
magnitude and O(p) bits.

Process h independent right-hand sides together. Zero-pad a final short
row block and, if needed, the final short RHS batch for matrix products;
discard only those known padding coordinates. A block update uses two
h-square products and additions, costing O(h^omega p^(1+delta)) bits.
There are O(m/h) updates in each of two triangular solves. Thus the cost
per batch is O(m h^(omega-1) p^(1+delta)), and amortized per real line is
O(m h^(omega-2) p^(1+delta)). Section 5 supplies full batches with at most
constant padding overhead; this is not a speedup asserted for one RHS.

## 3. Exact multiplication followed by one rounding

Use the ordinary seven-product Strassen recurrence over signed dyadics.
No rounding occurs inside its recursive products or additions. Coefficients
and RHS entries have P fractional bits and polynomial integer magnitudes.
Each leaf input is a signed sum of at most h original values; intermediate
products and recombinations have at most polynomial-in-h amplification.
Consequently all working numerators have O(P+log h+log p)=O(p) bits and
at most 2P fractional bits. Round each completed block-update entry once.
For a completed rectangular Woodbury product, accumulate its constant
number of square tiles exactly before rounding once per output entry.

The scalar multiplication count at h=2^k is exactly 7^k; additions are
6(7^k-h^2). This identity and every tested product are checked against an
independent cubic matrix multiplication. The established unconditional
short integer multiplier, also used by the source's local convolutions,
gives the stated bit cost. This use does not assume the multiplication
improvement being researched.

For a fixed-tape realization, store the depth-first recursion stack and its
bounded number of pending operand/result arrays on a fixed set of tapes.
At a node, split, add, copy, reset and recombine sequentially in O(h^2 p)
bit movement. The seven children are visited in fixed order; pending
arrays are passed over or copied at their charged node volume. The work
recurrence is 7T(h/2)+O(h^2 p), besides leaf multiplication. Its sum is
O(h^omega p^(1+delta)); the logarithmic-depth control records and rewinds
are included (or absorbed in delta). A separate tape per recursion level
or random access to stored submatrices is not required.

## 4. Rounding bound independent of the number of blocks

All matrix norms in this section are row-sum norms. For an RHS batch use
the maximum absolute entry; multiplication by a coefficient matrix is
bounded by its row-sum norm, independently of the number of RHS columns.
Put eta=2^-P and M=2^16 p^4. M exceeds every exact triangular norm,
inverse norm, diagonal inverse and transfer-block norm above, as well as
the Woodbury norms. Each h-wide rounded coefficient row changes by at
most h*eta<=4p*eta.

Let T denote one exact triangular factor, B_0=max(1,||B||_max), and Y the
computed block solution. Multiply its block recurrence by the *exact*
D_i. Since D_i C_i=I and D_i F_i+E_i=0, its original-system residual is

```
||T Y-B||_max <= 4p M eta (B_0+||Y||_max+1).
```

This is a maximum over block rows, not a sum over the line. The factor
inverse bound and 8p M^2 eta<1/2 imply ||Y||_max<=3M B_0. Hence

```
||Y-T^-1 B||_max <=32p M^3 eta B_0.
```

Composing forward and backward solves gives
||computed_X-A^-1 B||_max<=128p M^4 eta B_0 and
||computed_X||_max<=9M^2 B_0. These generous constants are uniform in m.

The wrap rank is at most 2v<=4w. V has support only on the first and last
v original boundary coordinates: do not scan a dense m-wide V for each
row. Gather those two known groups in ordered passes. Compute VX, K^-1VX,
and ZK^-1VX by h-square tiling, with at most two tiles across each short
dimension and O(m/h) row tiles for Z. Ragged physical endpoints remain
the original endpoints, not the end of a fictitious padded matrix.
Coefficient row perturbations are at most 4p eta for these three maps.
Combining their polynomial norms with the triangular error gives the
deliberately loose uniform bound

```
||computed_S_inverse(B)-S^-1 B||_max
  < 2^200 p^40 eta B_0.
```

For example the propagated triangular contribution is at most
256p M^7 eta B_0. Each additional rounded map has error bounded by its
row perturbation times the preceding magnitude, plus eta; three such
terms and the final subtraction are below 2^12 p M^7 eta B_0, which is
2^124 p^29 eta B_0 <2^200 p^40 eta B_0. Including the source's S-rounding
perturbation of 640p^3 eta fits this allowance as well.

Both original coupling matrices have only O(w^2) nonzeros per cell. Each
connects that cell's two boundary groups to O(w) nearby interior indices,
and never to another cell's interior. Compile these small rectangular
pages in setup; apply each to the same h RHS using padded square products.
Coefficient rounding and once-per-output rounding have the same errors as
the original exact dot products: the multiplication algorithm changes
neither their rounded coefficients nor their exact products.

Use the pinned GS interior error LA=2^(32p)*p^8*eta and the new allowance
SB=2^200*p^40*eta. The source's fixed-depth Schur composition is bounded by

```
1024p^2 LA +512p^2 SB +2048p^4 eta
  <2^(64p)*p^64*eta,   p>100.
```

The remaining H-to-N perturbation, normalization and disk rounding are
unchanged. Thus P=32768p still gives the original scalar accuracy and
tensor error interface. This proof retains u*d<=p; batching does not
reduce the phase-cell similarity exponent F_j or allow less precision.

## 5. Pay for RHS grouping, pages and returns

Use the source's bulk microbox layout, already obtained by its constant
number of large router calls. Its local fields have length L or L+2A,
where A=4096p^3 and L>=p^8; intermediate completed core fields are padded
back to L. The coarse labels remain in their existing order. A fixed
coarse tuple and axis i determine one scalar operator page, independent
of all the other local coordinates. Therefore other local coordinates
are legitimate independent RHS, including when their values are dirty
intermediate data. No equality or duplication of their values is used.

Eventually D=d-1>=2. Choose one other local axis. Pad only THAT field to
its next power of two, less than twice its current length. Since its
length is >=L and h<=4p, its dyadic size is divisible by h and at least h.
Use its low log_2(h) bits as the RHS batch coordinate. All other coordinates
index batches. The page and coarse index i are the same for all h lines
in one batch. Remove this single-field padding after the axis, before
choosing the next axis; it never accumulates as a 2^D volume factor.

Expose the current local axis next to the h RHS coordinate, with layout
[other batch coordinates][axis row][RHS]. Moving only polynomial-length
local fields by the retained stable binary split/interleave routine costs
O(log p) times their complete record volume, independent of the length
of any spectator prefix/suffix crossed. It is applied separately within
each unchanged coarse fiber. All records have O(p) bits. Return by the
reverse moves with the correct current field lengths, charging both
directions. The finite layout tests execute stable splits and their
inverse chunk merges, including zeros, tails and non-power-of-two source
fields; they are not a simulation of all tensor routing.

For each batch, stream phase cells in order, retaining its h RHS original
data, first local inverses and boundary RHS. The unchanged local GS work
can be performed line by line inside that batch using additional short
field transposes. Their cost and returns are O(L*h*p*polylog p), absorbed
by the d local term. Coupling pages are in cell order. The forward and
backward boundary passes retain only the neighboring h-by-h solution
block on work tapes; storing the entire intermediate boundary stream
and reversing its direction costs its bit volume. Gather wrap endpoints
with ordered scans, and stream Z row blocks for the final correction.
Merge boundary and interior outputs in their inherited order.

Factor pages contain O((L+L*w^2/d+w^2)*p) bits, as before. They are scanned
and reset once per RHS batch, not once per scalar line for the boundary
tables. Their boundary traffic amortizes to O((L*w/d+w)*p) per line,
below the new O((L*w^(omega-1)/d+w^(omega-1))*p^(1+delta)) arithmetic,
since omega>2. Local GS pages may still be scanned once per line and
cost O(Lp), already charged. The source's outer coarse-page catalogue
scans and polynomial setup are retained and absorbed by complete local
microbox volume; there is no random page lookup or new coarse permutation.

An m-row boundary solve costs O(m*h^(omega-2)*p^(1+delta)) per line;
the two coupling passes cost O((L/d+1)*h^(omega-1)*p^(1+delta)). Since
m=O(L*w/d+w) and h=Theta(w), both are within

```
O((L*w^(omega-1)/d+w^(omega-1))*p^(1+delta)) per line.
```

Adding the original O(L*p^(1+delta)) local work, summing the O(T/L)
lines per axis and d axes, and adding the grouping and source routing
costs yields Section 1. Online records and recursive work use a fixed
number of tapes. Exact rational block inverses and their possibly long
determinants are setup only: polynomial work in the source axis size and
p remains n^o(1), just as for the existing Schur construction.

## 6. Evidence and remaining obligations

The executable producer uses the seven-product recurrence, rounded
diagonal inverses and transfer blocks, two blocked triangular solves,
the actual supported V contraction, and tiled K/Z products. The independent
reference uses dense rational Gauss–Jordan inversion and cubic products.
Tests include ragged blocks, equality at the minimum cyclic dimension,
empty wrap support, signed coefficients, near-singular wrapped pairs,
and actual Gaussian phase-cell Schur matrices. Complete Schur comparisons
use the new rounded boundary/coupling program with an **exact dense local
inverse reference**. They do not rerun the inherited GS rounding proof.

Mutation controls deliberately change a transfer sign, remove Woodbury,
permute border rows, transpose a diagonal inverse, and permute RHS rows.
The package records their nonzero discrepancies, exact arithmetic counts,
and source hashes. Full outputs must agree across the stated interpreters.

Weakest steps remain the written all-size fixed-tape and bulk-layout
transfer, inherited analytic Gaussian and normalized-map interfaces,
and the general assembly/compiler contracts. No Lean proof, numerical
runtime speedup, optimality, or new integer-multiplication exponent is
claimed. This row refinement must not be promoted by simply deleting
unrelated assembly guards.
