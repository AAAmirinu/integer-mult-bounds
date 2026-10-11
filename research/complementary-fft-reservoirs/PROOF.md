# Complementary reservoirs and routed top bits for the tensor FFT

## Claim and retained interfaces

The compact recursive **core**, before processing its reserved axes, acts as
`C` on its active selected bits and identity on every reserved and spectator
coordinate. This is an all-input operator identity; no reservoir content is
assumed zero. Under this existing contract and the accepted arbitrary-coordinate
router, two complementary axis passes remove the individual reserved-axis
term `d^(1-c)` from the complete balanced FFT cost.

Routing the constant number of exceptional top-bit rounds into supplied
temporary layouts also removes their separate `O(Vd)` bill. This changes a
construction, not the recurrence of a fixed program. It removes the requirement
`q<c`, where `q=1-lambda_prime`, and the balanced-prefix cost from this FFT
implementation. It does **not** remove Gaussian arithmetic, scalar work,
dimension, guard, prime packing, or `K=o(ell)` requirements. No larger numerical
kappa or unconditional multiplication theorem is claimed.

The source-pinned primary layout text defines `G=4 ceil(log2 p)+6`, `H=dG`,
`qF=ceil(2H/K)`, `qB=ceil(H/K)`, and
`q0=ceil(log2 W) ceil(log_m(2d))`. It explicitly separates:

1. individual transforms on `Q0=q0+qF+qB` selected reservoir axes;
2. the recursive core on the remaining active middle block;
3. the identity action on complete reservoir coordinates at core return.

We use item 2 with external complete reservoirs and omit item 1 in that call.
This is justified by the core proof, not by pretending the existing complete
layer black box has a new interface. Padding, recursive row splits, inverse
phase wrappers, exact restoration, scalar correction, and deletion of complete
zero rows are retained unchanged.

## Two physical layouts

There are `D=d-1` Fourier axes of lengths `2^(ell-1)` or `2^ell`.
Partition their names into disjoint sets A and B of sizes `floor(D/2)` and
`ceil(D/2)`. Partition the common low `ell-1` slots into the same balanced
groups as the existing transform. Every group j has a supplied chunk width
`K <= Kj < 2K`. Extra long-axis top bits remain a separate prefix.

For the A pass, in **every group**, order complete chunks as:

```
B row chunks | B front chunks | remaining B front spectators | all A chunks
             | B back chunks
```

Use the first q0 opposite-set chunks as the row index, the next qF as two
complete H-bit front fields, and the final qB as one complete H-bit back
field. Other bits are spectators. qF and qB use that group's actual Kj.
For the B pass use the same construction with A and B exchanged. The record
suffix and every named coordinate are preserved. These are permutations of
existing bits, with no padding of axis lengths or new independent volume.

For sufficiently large p, both sets provide enough chunks simultaneously
in every group. One convenient sufficient condition is

```
K >= 64G,       q0+2 <= d/8,       d >= 4.
```

Indeed `Q0 <= q0+3dG/K+2 <= 11d/64 < d/4`, whereas the smaller set has at
least d/4 axes. Fixed positive epsilon,c give these conditions eventually:
`d=Theta(p^epsilon)`, `K=floor(d^c)`, and `G,q0=O(log p)`.
There is no comparison between c and q in this capacity argument.

The surrounding groups, top-bit prefix, unused opposite-set chunks, and
polynomial suffix are spectators. The active chunks are contiguous. Front
and back fields are disjoint from the row index. Each padded row still
contains the complete within-row rectangle. The original role split and
arbitrary dirty-content restoration proof therefore apply literally.

## Chronology and exact operator

First complete **all** Fourier rounds of A, using B as reservoirs. Then
change the global physical layout once and complete all rounds of B, using
A as reservoirs. It is not necessary to alternate layouts at every round.
The tensor Fourier transform factors as

```
(F_A tensor I_B)(I_A tensor F_B) = F_A tensor F_B.
```

The A-pass output is arbitrary data from the B pass's perspective, including
superpositions in its reservoir indices. The full all-input identity action
on reservoirs, not a zero-input or address-only check, permits this use.
In each pass, process its extra long-axis top bits in one completed fast
layer using the temporary layout below, and then process its common named
levels in decreasing order. At level h, the twiddle uses
only the current branch and lower named slots of axes in that pass:

```
E = -sum_(i in pass) [2r/2^(h+1)] b_i sum_(v<h) 2^v x_(i,v)  (mod 2r).
```

No other axis occurs in that exponent. The layout retains all slot names.
The frequency significance of slot (i,h) is still `a_i-1-h`. Thus the final
operator is the same tensor transform in the declared final layout and
bit-reversed frequency order. The opposite procedure reverses both passes,
their rounds, and all layout permutations; it consumes the same pointwise
frequency order and has the original normalization `F^+ F^- = I/M`.

## Routed top-bit layers without new coordinates

Let n be the total number of existing binary address slots, with n=Theta(p),
and let f<=d be the number of long-axis top bits in the current pass. For
f=0 skip this step. Choose only **unselected existing slots** to supply the
following layout:

```
q0*K row bits | 2H front bits | f chunks of K bits | H back bits | remainder
```

Place one of the f selected top bits at offset zero of each active chunk;
fill its other K-1 slots with distinct unselected bits. The sufficient
capacity condition is

```
n >= q0*K + 3H + f*K.
```

The row region, front fields, active fillers and back field are disjoint.
Every other slot is a spectator. Because `epsilon(1+c)<1`,
`dK=o(p)`, while `dG=o(p)` and `q0*K=o(p)`. Hence this condition holds
eventually, uniformly for every f<=d. It enlarges no Fourier axis and adds no
coordinate; the original temporary complete-zero-row padding is retained.
Named low input bits may be fillers or temporary fields: the
completed core is identity on them, for all coefficient arrays.

Route once to this supplied map, run the original core with f active chunks
and external reservoirs, convert the completed C tensor to the normalized
H tensor, and perform the top twiddle using the original names. Route to the
common-pass layout afterward. For small f the retained stopped core has
its ordinary individual leaf cost, already below the same global layer
bound. Only a constant number of such top layers occurs in the full FFT.
This replaces the old d individual top kernels by one fast layer per pass.

## Cost of the core and global routing

Set `chi=tau+(1-beta)max(sigma-tau,0)` and
`leaf=sigma+beta(1-sigma)`. The source core recurrence, including dirty-field
repair and row traffic, is

```
F(e) <= (s/W) F(e/m) + O(G^tau e^tau+1),
F(e) = O(e) when e < d^beta.
```

Global d,K,G,H and external reservoir fields stay fixed throughout a call.
Base-m decomposition handles an arbitrary active count. Each pass has
Theta(d) active axes. Since its reservoir axes are not individually
processed, the cost is

```
O(V (log p)^3 [d^chi + d^leaf + 1]).
```

As before, choose `max(tau,sigma,chi)<lambda<lambda_prime<1` and
`leaf<lambda_prime`. The complete active-pass layer costs
`O(V d^lambda_prime)`. There is no `d^(1-c)` term. There are at most two
common layers per named level, which changes only a constant.

Each common-pass or top-bit layout is a single supplied coordinate permutation
on O(p) named binary slots. The accepted arbitrary-source router implements
it in `O(V p^tau polylog(p)+poly(p))`, without assuming free random access or
an offset oracle. There are at most five global routes: up to two into top
layouts, two into common layouts, and one to the required output layout.
Inverse transforms use a constant number of reverse routes. The polynomial
suffix absorbs polynomial setup.
There is **no routing factor ell**. The existing strict coordinate-movement
margin absorbs its polylogarithms. Construction of the maps uses polynomial
setup and O(p)-bit current descriptors, not an arbitrary free descriptor.
Twiddle exponents in a virtual layout are computed from the original named
slots. The deterministic layout rule can be evaluated with polynomial work
per complete record or controlling fiber; the same superpolynomial polynomial
suffix absorbs this work. No random-access coordinate lookup is assumed free.
The finite operator code is a mathematical control, not the claimed tape
implementation or a measurement of its asymptotic running time.

Top layers cost `O(Vd^lambda_prime)` and are absorbed by the common layers.
The completed FFT therefore has the following two cost types (up to constants)

```
O(V [p^tau polylog(p) + ell d^lambda_prime]).
```

The balance of named slots still requires `epsilon(1+c)<1`, so that
`K=o(ell)`. This requirement cannot be removed merely by removing the
reserved-axis preprocessing bill.

## Precision and completed boundaries

Each normalized active butterfly tensor is a contraction; twiddles and
layout permutations are exact signed coefficient permutations. Run active
layers at precision p+2, embedding the p-grid input exactly. There are at
most 2ell normalized layers across both passes. Their accumulated error is
strictly below `sqrt(2)*(ell/2)*2^-p`. One final Q_p truncation adds less
than `sqrt(2)*2^-p`. For ell>=2 this is no more than the retained
`sqrt(2)*ell*2^-p` error allowance. The output stays in the disk.

For these runs G and the reservoir capacity tests use the working precision
p+2. All displayed growth estimates and eventual conditions are unchanged
by this fixed shift. In particular `G <= 4 ceil(log2 p)+10` for p>=2.

The linear semantic guard applies to each core: completed child boundaries
are unchanged, there are at most d selected axes, and external temporary
fields return exactly. Replacing p by p+2 changes neither the O(p) word
width nor any strict power inequality. A normalized layer completes before
the next one starts; unbounded internal intermediates are not passed as
disk inputs. All finite small-parameter cases may use the original fallback.

## What this removes, and what it does not

The two occurrences of `c-q>0` in the original assembly are the same
reserved-axis obligation. They can be replaced for this construction by
the external-capacity condition above and its eventual cutoff. The explicit
top-bit/prefix margin is also no longer needed. All other analytic and tape
conditions remain. In particular Gaussian/scalar constraints still cap the
balanced exponent below
`a/(1+a)`. This result makes one geometric dependency independent of the
desired compact saving; it does not increase the presently binding exponent.
The parameter controls reproduce #472's old arithmetic, then change only c
and check the remaining 44 strict expressions. They are a separation witness
between the two reservation rules, **not** a fresh complete finite invoice
or a replacement for #472's unchanged release certificate.

The capacity verifier supplies a compressed explicit eventual cutoff for any
fixed rational epsilon,c and any integer `B>=ceil(log2 W)`. For
`L=ceil(log2 p)`, d=floor(p^epsilon), and K=floor(d^c), use the conservative
bounds `K>=2^(epsilon*c*L-4)`, `d/8>=2^(epsilon*L-5)`,
`64G<=512L`, and `q0+2<=B(L+2)+2`. It selects L0 by rational inequalities
so the two exponent lower bounds, rounded down, are at least 4 and their
squares dominate the corresponding linear bounds for **every** L>=L0.
The integer induction `2^t>=t^2` for t>=4 proves both capacity inequalities
without expanding 2^L. A positive `1-epsilon(1+c)` and its separately checked
cutoff provide room for the balanced chunks. The examples B=14 and B=4000
are parameterized capacity controls, not claims that a new complete finite
compiler's row stock has been reconstructed.

More explicitly, if `n>=A*p` for fixed A>0, top capacity is implied eventually
by
`B(L+2)*p^(epsilon*c) + 3*p^epsilon*(4L+10) + p^(epsilon*(1+c)) <= A*p`.
All three normalized summands tend to zero because their power gaps are
positive. The verifier supplies a separate compressed sufficient cutoff,
including A, for this inequality. This address-volume hypothesis is essential;
an isolated one-bit rectangle does not provide the promised reservoirs.

If one *also* replaced the separate Gaussian/scalar bounds, the new FFT's
parameter cone would allow epsilon approaching one and c approaching zero
independently of q. That observation identifies remaining work; it is not a
claim that the Gaussian/scalar algorithms or a supplier saving approaching
one have been constructed.

Finite controls test actual polynomial Fourier operators against the closed
formula, named-slot routing with real pass changes, opposite normalization,
complete external-field inventories, and bad schedules. They do not measure
the asymptotic fixed-tape cost or formally prove the all-size compiler. That
transfer is the written argument above, conditional on the pinned interfaces.

Prepared by chafreaky with OpenAI Codex assistance. Retained layout and phase
contracts: Douglas Colkitt and the integer-mult-bounds contributors. Balanced
layout, semantic guard, and arbitrary router: the RaD project/hipotures,
Zhihao Chen, icekylinx and the authors credited in the pinned source reports.
No literature priority is claimed. Apache-2.0.
