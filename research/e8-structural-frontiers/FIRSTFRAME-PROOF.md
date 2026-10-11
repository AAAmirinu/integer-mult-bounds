# A necessary bound for a fixed first-frame family

This is a conditional negative lemma for a precisely restricted supplier family.
It does not assert a lower bound on integer multiplication or a global barrier
to improving κ. The `relaxed` root below is an upper-bound benchmark, not an
achieved supplier.

Fix the source-bound R779 word, its original first required helper frames,
240 data endpoint rank differences8, eight copied rank9 centers per local
invocation, the existing nine-stage geometry, eight replicas per stage,
final helper dimension9, and width73 complete residual banks. There are72
local invocations and7680 fixed data families. Every permitted entrance on
helper r has dimension d_r≤f_r, where f_r is the dimension of its **original**
first required frame. The remaining helper residual rank is required to be
s_r=9-d_r; complete banks contain these residual axes with paid padding.

A different scalar donor chronology is allowed in this family only when these
specified firstframes, helper residual ranks, data/center semantics and
geometry remain intact. New main-word chronologies that change firstframes,
copy-free centers, collective off-diagonal helper endpoints whose residual
rank is no longer the sum of9-d_r, new data endpoints, or new bank semantics
are outside the lemma.

The exact source census is

| f_r |1|2|3|4|5|6|7|
|---:|---:|---:|---:|---:|---:|---:|---:|
| count |257|185|147|35|43|109|3|

Consequently Σf_r=2098 and Σ(9-f_r)=4913. The script derives the first
required frame directly from the chronological source word, validates every
F2 frame basis rank, verifies data/helper endpoint dimensions and the eight
retained center dimensions. It does not trust the exploratory firstframe
screen output to obtain these numbers.

Put m=73 and φ_b(r)=(r/m)^(1-b), 0<b<1. Concavity and φ_b(0)=0 imply that
splitting a fixed total helper rank cannot lower its paid cost:
Σ_j φ_b(r_j)≥φ_b(Σ_j r_j)=φ_b(s_r). Grant each helper its maximal entrance
for free and omit response, cleanup, scalar, adapter, phase and fallback costs.
The fixed data/center lower histogram is

    H_D = {8:23040, 9:576, 16:3840, 32:3840, 48:3840}.

Here 72·240 local data endpoints contribute rank8 children, 72·8 copied
centers contribute rank9, and the retained geometric children contribute1920
copies of each rank in [16,8,32,8,48,8,48,32,16]. This geometry is an explicit
hypothesis of the lemma.

For any integer bank count B per stage, capacity requires

    73B ≥ 8 Σ_r s_r.

The padding rank per stage is P=73B-8Σ_r s_r. Its cost is at least P/73,
because φ_b(r)≥r/73 even if arbitrary rank73 or fractional padding is granted.
For the total stock W=7680+9B and fixed data numerator A_D(b), this gives

    paid numerator - W
      ≥ A_D(b) - 7680 + 72 Σ_r g_b(s_r),
    g_b(r) = φ_b(r) - r/73.

The bank count B has canceled. This is why the argument covers **every** B;
it does not compare539 mixed-rank banks with the earlier396 full-rank
endpoint bound.

At b=1/499, the exact rational outward intervals certify
`g_b(r+1).lower-g_b(r).upper>0` for r=0,...,8. Since s_r≥9-f_r and s_r≤9,

    paid numerator - W
      ≥ A_D(b)-7680 +72 Σ_r g_b(9-f_r).

Equivalently, let H=H_D+72·{9-f_r}_r and permit fractional effective stock

    W_eff = 7680 +72·4913/73 = 914376/73.

Then the right side equals W_eff·(Moment(H,m,W_eff,b)-1). At b=1/499 its
exact moment lower endpoint is

    26977617261418862023450643799713090411411389767428014955159063864265
    /26959946667150639794667015087019630673637144422540572481103610249216
    > 1.

Thus this fixed family cannot achieve the coarse saving b=1/499 required
even by the ideal κ=1/500 outer cap. Positive fallback was omitted, which
only strengthens the relaxation.

For context, the relaxed root is rigorously bracketed by

    0.001616652184482181225180 < b_relaxed < 0.001616652184482181225181.

The same nine exact g-monotonicity inequalities are checked at the upper
grid point. Its relaxed moment is already strictly above1. Since each actual
family moment increases with b, every admitted member has coarse saving
strictly below that upper grid point. Its ideal nominal κ ceiling is therefore
below approximately0.001614042838601308599. This is a ceiling, not a newly
achieved exponent. The additional539-bank, one rank43 padding child per
stage check is optional evidence and is not used for the all-B proof.

Reproduce with Python's standard library only:

    python -B research/e8-structural-frontiers/verify.py /fresh/output

Dependencies are the unchanged gzip R779 certificate and the unchanged exact
`moment.py` engine. `SOURCE-PINS.json` and `MANIFEST.json` binds the script,
source, engine, proof and result by SHA256. The engine uses exact rational
Mercator/exponential bounds with outward224-bit dyadic rounding; Decimal
only proposes the root grid bracket, which exact inequalities then verify.
