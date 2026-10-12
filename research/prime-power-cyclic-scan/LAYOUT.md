# Arbitrary stride: an explicit reduction with a permutation charge

The neighboring inverse can be applied to U=tau Z_L^w after routing its
cycles into contiguous order. This extends correctness to arbitrary w;
it does not make the tape cost of that routing disappear.

Normalize w modulo L. Let d=gcd(L,w), ell=L/d, and v=w/d. For ell>1,
let v_inv be the inverse of v modulo ell. Every index has a unique form
i=a+d s with0<=a<d and0<=s<ell. Give its record the key

    (a,t), t=v_inv s mod ell.

Sorting by this key places each cycle in the order
i=a+t w mod L. Consequently i-w is the preceding record in that cycle.
For ell=1, including w=0, use t=0. This case requires no modular inverse.
Execute the neighboring inverse separately on each contiguous cycle.
The full operator is block diagonal under this permutation, so the
same infinity-norm error bound holds; errors do not add across cycles.
Restore original order by a second sort on i.

## Charge on a fixed number of sequential tapes

Attach O(log L)-bit keys and indices to O(B)-bit numerical words,
B=O(p+r^4), with any phase-representation cost added as in PROOF.md.
A bottom-up merge sort uses at most ceil(log2 L) passes, each reading
and writing O(L) records. Four sequential work tapes and O(B+log L)
buffer state suffice for the usual alternating-run merge. Both sorts
therefore cost

    O(L(B+log L) log L)

bit movement/comparison work. Initial modular reduction and inversion
must also be paid according to the length of the supplied w and L.
Key generation need not do a large multiplication for every record:
in original order, increment a and advance t by v_inv only when a wraps;
in cycle order, advance i by w modulo L. These bounded integer updates
cost O(log L) per record.

After the first permutation, remove routing metadata from the numerical
scan stream and retain cycle delimiters. Regenerate original-index keys
after the factors using the known cycle enumeration. This avoids carrying
O(log L)-bit keys through every scalar scan. Each factor still scans
O(L) values across all cycles. The total conservative bit bound is

    soft-O((Lr+r^3)B) + O(L(B+log L) log L),

plus the initial input-description arithmetic. Storage includes the
O(L(B+log L))-bit sorting records and the preparation space in PROOF.md.
The implementation below checks routing and merge-pass counts on Python
lists; it is not an implementation of the four physical work tapes.

## Why this does not settle the required transform layout

If B is of order p and log L is of order p, these two generic sorts can
cost O(Lp^2). They can reintroduce the precision-sized traffic factor
that the stable scans removed from the arithmetic inverse. The full
application must show that cycles are already contiguous, amortize a
common permutation, exploit special strides, or charge this cost in its
actual recurrence. RAM access to arbitrary indices is not such a proof.

## Evidence

`python3 -I -O -B check_layout.py --out LAYOUT-CHECK-fresh.json` checks
every step from-2L through2L for lengths1 through64. It verifies the
bijection and actual cyclic predecessor relation. It also runs the
rounded mixed-root radix9 inverse with a nontrivial rational unit phase
through both merge sorts, including zero, negative and non-coprime
strides. Small cases are compared against a direct global dense solve;
all execution cases check the expanded global polynomial residual.
Controls that omit the modular inverse or use the wrong stride fail.

This is a constructive layout option with its cost exposed, not a new
kappa claim or a claim that the application's layout requirement is met.
