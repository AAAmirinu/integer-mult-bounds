# Independent helper splits and the complete cost

This proof changes the helper input and output contract of the exact PR5601
word. Five fixed PR5602 boundary relations remove five paid H5 calls. Nine
independent target splits then retain all remaining calls. Every main endpoint
and chronological owned path is preserved. Scalar identities are rational;
the native check supplies exact phases and the rule for every positive width.

## 1. A split criterion

Let a group of helpers have the same initial chart U and final chart V.
The complete source word returns each of these helpers unchanged in normalized
coordinates and has no helper contribution to any other output.
Let F be a strict intermediate chart, with U contained in F and F contained
in V. At one chronological cut, let P be the scalar prefix matrix and S the
scalar suffix matrix. The matrices include every public input and output.
Owned fields follow the source initialization and erasure contract.

Suppose a row a and a column b use only fields at chart F. Suppose c and d
use only the specified helper group, and

```math
aP=c,\qquad Sb=d,\qquad ab=cd=1.
```

Choose a helper role p at F. There are invertible scalar matrices G and J
with

```math
e_p^T G=c,\quad Gd=e_p,\qquad e_p^T J=a,\quad Jb=e_p.
```

Here G acts only on helpers with boundary charts U and V. J acts only on
fields at F. The construction emits these matrices as ADD and dyadic-unit
SCALE operations. Its row and column elimination uses the unit pairings.
The emitted program and its inverse are explicit; no dense matrix operation
is assigned zero implementation cost.

Apply G inverse at the input. At the cut, apply J. Role p then contains the
independent coordinate t=c h. Retain p as an output at F. Introduce one new
independent input z at F. Use its new role in place of p in J inverse and in
the complete suffix. Finally apply G at V, with the same role substitution.
The suffix state changes by b(z-a P h), so its helper output is

```math
h+d(z-ch).
```

The final change of basis gives

```math
G[h+d(z-ch)]=Gh+e_p(z-t).
```

Thus the former p coordinate is replaced by the independent z coordinate;
all other helper coordinates and every main output retain their required
values. The old t coordinate has already been returned at F. This replaces
one U-to-V target by a U-to-F target and an F-to-V target.

This uses a new input, not two outputs computed from one input. It does not
assume a helper is zero. The early output is a public field and stays live
until the caller returns. The successor input is public from the start and
is first used at the cut. No new COPY, CLEAR or owned lifetime is introduced.
The source's owned erasures remain charged under the inherited contract.

All three basis changes use common physical charts. They therefore commute
with the relevant chart operator. Native normalization gives ranks
`dim(F)-dim(U)` and `dim(V)-dim(F)` with their exact phases. Scalar coefficients
stay outside the tensor substitution. The frame induction applies at every
positive width; it is not a test at width one alone.

## 2. Five released boundary relations

The input is PR5601 at `8f7e870b22885a367b347dc12791da98fd53f83d`.
The retained PR5602 constructor and witness come from
`6c224aa720203c4f4615e6538d8038a275387db8`. No coefficient, helper, frame,
cancellation vector or output vector in those relations changes. Only the
chronological cut indices change, with explicit event anchors in `BOUNDARIES.json`.

For a forward boundary relation, the complete prefix gives a helper input
combination after cancellation by coframed fields. A scalar input basis
makes this combination one independent input. The helper has no later source
read, so it can finish at that frame. The reverse relations supply the
corresponding early-input rule. The source constructor uses an algebraic
transpose to derive that rule; it does not execute the owned program backward.
The final program restores the eight COPY opcodes. Its complete subsequence
of operations involving owned fields equals the original chronological
subsequence, byte for byte, before the independent splits rename owned roles.

The five fixed relations use helpers 652, 341, 596, 668 and 684. Each replaces
one H9 helper target by H4 and removes one paid H5. The complete arbitrary-input
interface is checked after every relation. The sixth PR5602 relation uses a
frame-597 contact absent from the PR5565 cascade; it is not used.

## 3. Nine independent splits

After those five changes, the first split uses the cut after zero-based
event 12504, chart 306 of dimension four, and pivot 259. Its helper group
has initial chart 3 (dimension zero) and final chart 127 (dimension nine).
With e_r the coordinate at role r, the exact vectors are

```math
a=e_{261}^T+(e_{256}^T+e_9^T)/2+2e_{259}^T,\qquad b=e_{259}/2,
```

```math
c=2(e_{259}^T+e_{61}^T+e_{265}^T),
```

```math
d=(e_{262}-e_{270}+e_{265}+e_{264}-e_{256}-e_{271}+e_{263})/2.
```

The complete prefix gives aP=c; the complete suffix gives Sb=d.
Both pairings are one. The boundary basis has 14 scalar events and the
local basis has four. With their inverses, this adds 30 ADDs and six dyadic
SCALEs. It replaces one H9 target by independent H4 and H5 targets.
`SPLITS.json` gives every subsequent cut and all four exact vectors.

`check_cut` reconstructs each prefix functional and propagates each suffix
column. It checks zero support on every other input and output. Full row
replay checks each intermediate construction. A separate dense-integer
transpose replay checks all 565,504 entries of the final 752 by 752 interface.

The nine splits are two H9 to H4+H5, five H9 to H2+H7, and two H9 to H1+H8.
They add nine independent inputs. The source's 735 public fields become 744,
with 536 helpers and 208 main fields. Eight owned lifetimes remain, with
one live at a time. The source has 25,132 events; the boundary step has
25,137; the final word has 25,393. The split step adds 256 scalar events.
The new local helper profile is

```text
{1:2, 2:5, 4:91, 5:6, 7:5, 8:16, 9:411}.
```

The verifier replays the retained PR5580 and PR5565 words. It checks the
PR5565 paid delta `-8H1-H3-2H4+4H5` and helper delta `-H8+H9`, then the
PR5601 paid delta `-2H2+2H3-2H4+H5` and helper delta `H4-H5`. These are
credited source changes, not new discoveries in this package.

For 0<t<1, define `g(a,b)=a^t+b^t-(a+b)^t`. Strict concavity gives g(a,b)>0.
Against the consumed PR5601 word, the complete target-minus-paid moment
increases by

```math
18[7g(4,5)+5g(2,7)+2g(1,8)].
```

Five g(4,5) terms come from the fixed boundary relations; two come from
independent splits. All new target credits and removed paid calls are
counted in the final invoice. The two complete rank masses both change;
their difference stays 760. The old components' reported kappa gains are
not added.

## 4. Native maps and the caller

The exact signed-Pauli and phase verifiers check every paid chart change,
every helper target and every main adapter. The local replay checks a strict
nested chart relation on each public move and the source's descending owned
moves. Each helper target is strictly productive.

Cinna Davis's p16/a7 controller and Ali Romman's all-forward implementation
from PR5544 remain literal inputs. All 18 full calls use the new local word
with fresh independent helpers. Sixteen backward main interfaces use the
retained signed exchanges and central-square translations. These wrappers
act only on the main pair. They do not alter a new helper output.

The physical caller check retains all 104 central ports, 7,488 boundary
contacts, 53,248 central-square column checks, 3,328 main Gaussian targets,
15 thin query sites and 3,120 whole idle jobs. It checks native routes,
spectators, exact phases and every whole target. The complete counts are

```text
paid calls:         66618
productive fields:  12976 = 18*536 + 32*104
rank mass surplus:  760
maximum target:     145
maximum paid rank:  72
```

The invoice is counted twice, once from literal events and once from the
controller path lengths. Input and output normalizers, added scalar basis
operations, routes, owned allocation and erasure, queries and idles are all
included. The new independent field count enters the completion-tail bound.
It is not left at the old 12,814 value.

## 5. Strictification, compiler and outer transfer

Two independent rational interval engines evaluate the complete moments.
The exact raw crossing is in (0.00310261511129, 0.00310261511130).
`RESULT.json` gives its rational endpoints and the strict tested margin. The claimed kappa is 0.00310261 and the tested saving is
0.0031026105. Their gap funds the finite compiler and outer parameters. An exact negative
derivative bound on [0,0.0034] makes this crossing the raw ceiling for this
fixed invoice under the retained BIT cap. It is not a global optimum.

Power 1024, cutoff 17, target floor 18 and tail offset 1/5 are retained.
The extra independent fields require a different tail bound: both charged
tail ratios are below 39/40, and `(39/40)^128 < 1/16`. Eight such blocks still
give the retained `2^-32` remainder. The fixed reserve is `10^-10`.
The complete normalized cost is strictly less than one. The old cutoff 20
fails and is retained as a control.

The compiler checks its finite integer threshold, initial range, shifted
exits, complement capacity, logarithm power 1024 and predecessor integer point. The old logarithm
power 1000 does not meet the new complement-capacity inequality.
The ordinary BIT saving remains 0.0034. All 54 strict outer conditions and
four functional conditions are checked with exact rational arithmetic.
The scalar growth bound uses fewer than 26,000 local operations and the
retained per-operation bound. The native growth bound uses the actual sum
of local paid ranks. The complete ordinary-work allowance remains below
`10^9`; the local scalar and route allowance remains below `10^7` per call.

## 6. Scope of acceptance

The five selected framework assumptions remain: native implementation at
all widths, owned erasure, uniform compiler closure, precision and tape
cost, and analytic integer recovery. The source helper-endpoint contract
also remains. This package proves the new finite interface, the chart
identities and every new numerical condition within that framework.

The enormous uniform word and complete rounded multiplier are not
materialized. These are author-side checks by the same AI-assisted author.
They are not independent human acceptance or a proof-kernel theorem.
The final exact discovery screen tests 47 boundary groups and finds no
further candidate in its finite basis-pair class. It does not prove a maximum
over bases, cuts, scalar programs,
frames, controllers or multiplication algorithms.
