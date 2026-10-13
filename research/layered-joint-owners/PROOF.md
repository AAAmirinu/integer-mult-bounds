# Fixed-provider joint owner improvement

The local word, its 492 helper residual widths, all 72 indivisible calls, the
literal controller, every admissible whole-family window and the bit supplier
are unchanged from pinned PR656. These interfaces are independently replayed;
they are not replaced by the optimizer's constraints.

## Nomination and literal admission

Choose a set of calls and release their present footprints. Group eligible
families by remaining capacity and eligibility bitmask. For each bucket, a
nonnegative integer variable counts families receiving a tuple of widths,
one width or zero per selected call, with sum no greater than capacity.
Bucket equalities preserve the number of families. Per-call equalities
preserve each helper width multiplicity. The tuple enforces at most one helper
from any selected call in a family. Existing calls outside the selected set
retain their family and width.

After solving, expand integer counts back to the literal family catalogue,
assign distinct helpers with the required widths, and compact each family's
disjoint offsets. Explicit checks cover every helper, call, family formula,
capacity, idle window, active-data exclusion, and full footprint. The physical
verifier then derives the actual frames and 73-column charts, checks the
controller, phases and finite invoice, and admits the exact moment and outer
parameters. A solver success alone establishes none of these physical claims.

## Exact improvement for every native exponent

Let `x` and `y` be old and new idle-remainder vectors, zero-padded to the same
family catalogue. They have equal total rank. The submitted map satisfies

`sum_i max(y_i-k,0) >= sum_i max(x_i-k,0)`

for every integer `k` from 0 to 48, with at least one strict inequality.
Coordinates are integers in `[0,48]`, so the difference of these stop-loss
functions is affine between consecutive integers and zero beyond this range.
Thus the same inequality holds at every real threshold. It is the usual
equal-mass majorization condition: `y` majorizes `x` and is not a permutation.

For every `0 < b < 1`, `r -> r^(1-b)` is strictly concave on the nonnegative
axis. Majorization therefore strictly reduces its sum. The normalized native
moment is `73^(b-1)/7168` times the sum of `r^(1-b)` over all paid children.
The local contribution is fixed, so the new owner map strictly lowers this
moment throughout that interval. The exact rational moment engines certify
the new root bracket, and the unchanged outer admission separately certifies
the stated κ. No conservative-surcharge claim is inferred solely from
majorization; the complete conservative profile is separately priced.

The total paid rank remains 520,704, so `73*7168 - 520704 = 2560` is unchanged.
`audit_owners.py` and `independent_owners.py` check these integers without
importing the optimizer. The latter derives windows from the freshly replayed
literal schedule and phase recipe and reconstructs the actual chart columns.
These are code-independent checks, not a claim of review by a separate person.

## A ceiling on this owner-only search

Keep the local paid profile and controller capacities fixed. The local profile
is `{1:2542, 2:414, 3:434, 4:154, 5:56, 8:8}` per call. The idle rank is

`520704 - 72*(2542 + 2*414 + 3*434 + 4*154 + 5*56 + 8*8) = 115200`.

Every idle remainder has dimension at most `C=48`. For `0<p<1` and `0<=r<=C`,

`r^p >= r*C^(p-1)`,

with equality only for `r=0` or `r=C`. Summing gives the smallest possible idle
moment after relaxing all placement constraints: 2,400 dimension-48 remainders
and zeros. No assertion that an actual assignment realizes it is needed.

`packing_ceiling.py` constructs that relaxed profile. The unchanged independent
pricing program proves a rational root bracket with both exact moment engines.
If `u` is its certified upper endpoint, every assignment using this fixed
provider has complex saving below `u`. The retained outer transfer has
`κ < b/(1+b)`, an increasing function of `b`, so `u/(1+u)` is an upper bound
for every such owner assignment. The exact fraction and a decimal rendering
are emitted in `CEILING.json`; the approximate ceiling is 0.001654249113130438.
It constrains this fixed construction only, and makes no optimality claim
for the submitted map or bound on different multiplication constructions.
