# Kernel composition and residual bank routes

## Local transformation

Use the pinned R740 word of PR #436. For each selected pivot p, the witness lists
an entrance E and donors D with response(p) = XOR of response(d) for d in D.
E lies inside the first nonzero frame of the pivot and every donor. Retained
copy rows are excluded; pivots and donors are disjoint; a donor serves one E.

Start p at E and remove its frame-zero target correction. Before the original
A word add p into every donor at E. After the original C word add p into those
donors again at the full frame. The response identity makes the missing target
correction exactly equal to the propagated donor correction; the last additions
restore arbitrary donor dirt. The literal full replay checks every column, each
nested frame and each integer source-span inclusion. The frozen input and output
hashes bind this transformation to PR #436. Three construction mutations fail.

The selection has 115 pivots and entrance rank 136. Forward and reflected local
streams have the same paid histogram:

```
{1:2445, 2:1058, 3:315, 4:442, 5:38, 8:9}
```

Both orientations restore all 980 input columns and erase each private copy.
The cancellation-free nine-stage prefix bound requires 123 bits.

## Exact residual routes and bank ownership

A helper starting at E and ending at the full eight-space has residual width
8 - dim(E). Every distinct E has a stored integer 8-by-8 matrix N satisfying
N N^T = 4 I. The first dim(E) rows span precisely E, checked on every root of E.
Thus N/2 is an orthogonal coordinate change taking E-perp to its residual
coordinate block. Here all entries of N are even and the matrix reduces to I
by at most seven row swaps. We replay every elementary factor. No new bad
address primes are introduced.

Extend this eight-dimensional coordinate change by identity on the 56 exterior
coordinates. A coordinate permutation sends its residual block into the
assigned bank interval. This is an explicit isometry for I_64/2, valid for every
inherited odd address prime. Reversal has residual projector I-P_E as well.
The common exterior window cancels from the endpoint difference.

The exact tiler assigns all eight replicas of each helper to disjoint intervals
in 723 banks. Every bank coordinate occurs once, with no padding. The independent
audit checks every interval, frame identifier, isometry and stage owner; wrong
frames, altered bases, omitted route factors and reused slots are rejected.
Arbitrary bank dirt follows from the retained injective-owner cover construction
and the local arbitrary-column identity. Full cover enumeration remains an
inherited interface, not a finite enumeration performed by this package.

The live stock is 64·120 + 9·723 = 14,187. Relative to the parent, paid rank
falls by 72·136 = 9,792 and live stock by 9·17 = 153. Since 64·153 = 9,792,
the rank deficit stays 2,496. The 72 emitted local invocations restore all 7,620
unbanked scalar columns. Their 53,280 helper owner assignments are independently
checked. All 18 omitted bridge-shear controls fail.

## Finite invoice and strict assembly

The largest child has dimension 42: 2·42² < 64² gives two-level halving.
The new route cost is conservatively charged with 144 extra elementary factors
per helper routing, exceeding seven local swaps plus 64 coordinate swaps.
All other costs are recalculated from the emitted program. The prefix is
charged at 128 bits; the two-level coefficient fits the retained 512-bit budget.
The row coefficient remains 18,355 < 20,161.

Both independent rational moment engines certify
c = 1135215296333206583339 / 10^24, with the inherited 10^-16 bad-branch allowance.
The cited complex supplier is b = 1183986549206329 / 10^18 from PR #433.
With eta = beta = 10^-18 and s = min(c, (1-beta)b) - 10^-24, retain six ordinary
bootstrap levels a_(j+1) = (1-s)s + s a_j, starting at 384599/10^10.
The largest admitted 10^-18 grid saving is
56696402193643 / 50000000000000000. All 47 strict outer inequalities pass;
the next grid point and invalid eta/beta controls fail.

The unchanged parent complex-interface assumptions and all-size assembly
obligations listed in the README are not discharged by these finite checks.
