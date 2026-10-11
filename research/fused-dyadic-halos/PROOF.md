# Fused compression halos with a binary main box

This changes the layout around the retained bulk Gaussian **compression**
map. It keeps the same global analytic map, local principal inverses,
normalization and error allowance. It does not change the local Gaussian
arithmetic, prove a joint-axis solver, or produce a new kappa.

Dependencies are the pinned phase-cell and microbox locality reports and
the arbitrary-source binary coordinate router. The fixed-tape argument
below is conditional on those interfaces. Finite tests verify data order,
head travel, requests, repair and a local contraction fixture. They do not
execute the Gaussian principal inverses or prove the all-size transfer.

## 1. Change the core stride, not the halo precision

Let D=d-1<=p. Retain the dyadic target axis lengths t_i, prime source
lengths s_i with rho_i=t_i/s_i between 1 and 2, and the source phase-cell
parameters. Take the same A=4096p^3 halo, but use the larger dyadic side

```
L=2^ceil(log_2(p^12)),    C=L-2A.
```

Eventually every t_i>=p^24, is divisible by L, and exceeds every fixed
polynomial needed by the original source cutoff. These follow from the
retained log(t_i)=Theta(p^(1-epsilon)), for fixed 0<epsilon<1. The new
choice L is polynomial, so source setup and factor catalogues are still
n^o(1). We may enlarge the eventual cutoff; no practical-size claim is
made. In particular C>L/2, L>=64DA, and Q_i=t_i/L>=2.

Partition the target axis into cores

```
T_(i,k)=[kC,min((k+1)C,t_i)),  0<=k<N_i=ceil(t_i/C).
```

The corresponding source cores are
J_(i,k)=[floor(kC/rho_i),floor(min((k+1)C,t_i)/rho_i)).
They partition [0,s_i) exactly. Supply the periodic target window

```
W_(i,k)=[kC-A,kC-A+L),
```

which has **exactly L slots**, including for the last partial core. Let
I_(i,k) consist of the lifted source indices whose nearest target indices
q_j belong to W_(i,k). The core is at source distance at least A/2-3
from its artificial endpoints, by the same rounding bound as the source
microbox report. The last partial core only has more right-hand padding.
Moreover |I_(i,k)|<=L/rho_i+O(1)<=L, since the retained prime interval gives
1-1/rho_i>1/(8d), and L/(8d) eventually exceeds the endpoint constants.

Apply the **same global H** principal inverse, local C selection,
D normalization and final scale from the source report. Do not recompute
weights at new origins or merge cells across the original physical period
cut. The stronger t_i>=p^24 ensures the original complement-gap hypothesis
for these length-L windows. The inherited locality, perturbation and
contraction arguments therefore apply with C in place of the old core
length. Keep only J_(i,k), and pad that output field back to L.

All local fields are now binary before and after each local map. There is
no permanent field of size L+2A, and no simultaneous rounding of D halo
fields up to 2L. The price is that N_i is generally not dyadic. Sections
2–4 isolate that issue in a sparse exceptional region.

## 2. One fused stream for the binary main box

The **main** coarse coordinates are 0<=k_i<Q_i=t_i/L. Their local field
is 0<=z_i<L. Thus their full rectangular shape is

```
[Q_0][L][Q_1][L] ... [Q_(D-1)][L],
```

all powers of two, with exactly T=product(t_i) records. At each main
position define f_i=k_i*C-A+z_i. Copy the original coefficient at f if
every 0<=f_i<t_i; otherwise emit zero. This is a clipped main stream.
The wrap-affected main tiles will be completely replaced later.

Emit this whole tensor stream directly from one original input tape.
Do not create D intermediate halo tensors. An odometer on the existing
binary fields changes fewer than 2T field records over the T outputs.
Maintain each f_i, a count of out-of-range axes, and the formal flattened
source address sum_i f_i*stride_i. Ordinary z increments change that
address by stride_i; a new core changes f_i by 1-2A; a complete axis reset
uses its known endpoint delta. Each carry update uses O(p)-bit additions
and comparisons, hence O(p) bit work. The full control state has O(p)
address bits plus polynomial-size headers, on a fixed number of tapes.
There is no D-term recomputation per payload.

When the active out-of-range count is nonzero, write a zero without
moving the input head. Otherwise move the input head to the maintained
address and copy its O(p)-bit coefficient. The travel bound below accounts
for the actual distance of these moves, including backward overlap
visits. This is not a RAM-address access assumption.

### Exact head-travel bound

Suppress the clipped zero entries in one axis's coordinate list and call
the remaining list f_i. It has m_i=t_i-A entries: only the first A slots
are outside the input, since L>=64DA and Q_i>=2. Its first entry is zero,
its last is t_i-2AQ_i+A-1, and

```
U_i=sum_j |f_i(j+1)-f_i(j)-1| =2A(Q_i-1),
g_i=(t_i-1)-f_i(last)=2AQ_i-A.
```

Let V=product(m_i)<=T, P_i=product_(j<i)m_j,
S_i=product_(j>i)t_j, and E_i=product_(j>i)m_j. The valid source head
visits the Cartesian product of these lists, in their inherited order.
At an i-axis transition its address displacement is

```
(f_i(next)-f_i(current))*S_i - Delta_i,
Delta_i=sum_(j>i) f_j(last)*product_(k>j)t_k.
```

Thus its exact total variation is
sum_i P_i sum_j |(f_i(j+1)-f_i(j))*S_i-Delta_i|.
Write G_i=S_i-1-Delta_i>=0. The triangle inequality gives

```
variation <= sum_i P_i [S_i U_i+(m_i-1)(G_i+1)].
```

Here U_i/m_i<=4A/L. Also
G_i/S_i=sum_(j>i) g_j/product_(k=i+1..j)t_k <=4A/L,
using g_j/t_j<=2A/L and t_j>=2. The suffix ratio S_i/E_i is below two:
product_j(1-A/t_j)>=1-sum_j A/t_j>=1-DA/(2L)>1/2.
Finally sum_i 1/E_i<2, since every m_i>=2. Therefore

```
variation <= V*(2+16DA/L) <= (9/4)T.
```

The initial valid address is zero. Returning the input head to zero costs
less than T additional record crossings. Thus total input-head travel is
**less than 4T**. Output writes, metadata and reading/copying coefficients
cost O(Tp) too. This bound is uniform in D. The finite checker compares
the exact displacement formula against explicitly executed tensor walks;
large-volume tests compute the formula only and are labeled accordingly.

## 3. Route the main box using complete named binary fields

The main stream already has the displayed interleaved complete binary
shape. Use one call to the retained arbitrary-source coordinate router
to gather all coarse fields before all local fields. This is a genuine
permutation of complete binary fields on exactly T records, not a mixed
radix transpose. It costs O(Tp*p^tau*polylog(p)) plus retained polynomial
setup. Each resulting inner box has D local fields of length L.

The operator pages still depend on their original axis and coarse origin
k_i*C. Sequential catalogue scans and page reuse have the same ordering
as the source bulk schedule; the catalogue now has ceil(t_i/C) entries,
still polynomial in t_i,p. Each local source window and core output fits
L, so every intermediate local field can retain the same dyadic length.

After the chosen local tensor algorithm, return the same named binary
fields by one inverse router call. Discard padded output slots in one
fused odometer scan. For each axis the kept source coordinates increase
contiguously through J_(i,0),...,J_(i,Q_i-1). Consequently the main output
is already in the original source lexicographic order on the prefix
rectangle of side floor(Q_i*C/rho_i). This operation uses a maintained
invalid-slot count and endpoint increments, not D comparisons per record.
**Do not sort the full main output.** The finite program executes the
inverse field permutation and fused deletion, then checks strict order.

This adapter supplies a binary box suitable for a future joint-axis
algorithm. If the retained per-axis solver is used, its d arithmetic and
local exposure costs still have to be paid. The adapter itself does not
remove them or assert a tensor FFT factorization of that solver.

## 4. Rare tails and wraps use an explicitly paid fallback

A tile is **bad** if some k_i>=Q_i (a tail tile) or some k_i=0 (a physical
wrap tile). Every nonbad main window lies entirely inside the original
target tensor. Main wrap tiles may be skipped or processed with the
clipped inputs: all their core outputs are replaced. Since local maps
never mix different coarse tuples, their provisional values cannot
contaminate a nonbad tile.

Write e_i=N_i/Q_i-1. Since C>=L/2,

```
0<=e_i<=4A/L+L/t_i.
```

If zeta=sum_i e_i<1/2, product_i(1+e_i)<=1/(1-zeta)<=1+2zeta. The total
tail-tile volume is at most 2T*zeta. Wrap planes contribute at most
2T*sum_i L/t_i. Thus the combined bad **input tile** volume M obeys

```
M <= T*[8DA/L+4 sum_i L/t_i].
```

With D<=p, L>=p^12, L<2p^12 and t_i>=p^24, the bracket is at most
32768/p^8+8/p^11, which is below p^-5 for every integer p>100.
Also zeta<1/2 and L>=64DA hold. These elementary inequalities may be
checked after multiplication by positive powers of p; no floating point
or unproved numeric cutoff is used. The finite census checks exact
rational powers of N_i/Q_i against this bound at selected large p.
Those are parameter controls, not executions of tensors of that volume.

Generate one request for every needed periodic input slot of every bad
tile: (original flattened input address, tile ID, local address). Tags
have O(p) bits because log T=O(p). Enumerating these regular windows and
computing addresses costs at most O(p^3) per requested record even with
schoolbook control arithmetic. Sort requests by source address with a
fixed-tape mergesort, scan the original input **once** to join values, and
sort the responses by tile/local address. The sorts cost O(Mp log M)
=O(Mp^2); the joined full-input scan costs O(Tp). Duplicated requests are
kept and receive the same original value. There is no random access to
the original input and no separate full scan for each bad tile.

Apply the existing local Gaussian algorithm to the complete bad L^D boxes,
processing the sparse collection one axis at a time in coarse-tuple order.
All its real periodic inputs are now present. The source phase-cell cost
is O(M*p^(1+delta)*(d+w^2+d*w^2/L)), and its short-field moves are within
the same bound after a fixed exponent backoff. For d<=p, w<=p with the
retained w^2=O(p/u)<=O(p), and 0<delta<1, this is O(Mp^3). Tags and even
straightforward per-axis local reordering are covered by that allowance.
Polynomial page setup remains n^o(1). For a fixed axis, keep its current
page while traversing the surviving B suffix; reset the catalogue only at
the next A prefix, as in the source's [A][k_i][B] schedule. Sparse gaps in
k_i are scanned, not jumped over for free. Across all possible A prefixes,
even full catalogue scans cost at most
O(T*D*page_size/L^D), with page_size=poly(p). This is O(Tp) eventually
because D grows and L^D exceeds every fixed polynomial in p. Thus sparse
page access does not silently require a separate catalogue scan per tile.

Output only each bad tile's source core. Its source cores partition the
exceptional rows without overlap. Sort those O(M) output records by
their original source address and merge with the ordered main stream:
exception rows override equal main addresses and fill the missing tail
addresses. This is a two-stream merge on fixed tapes. Total fallback
work, apart from the constant number of full scans, is O(Mp^3)=O(Tp).
The sparse repair never sorts all T main records.

## 5. Analytic interface and complete scope

For every good main tile and every repaired bad tile, the resulting core
map is precisely the original normalized principal-window construction
on the same global H, with the new window origin and the same halo A.
All windows satisfy the original complement-gap and physical-period-cut
rules. The principal-map row norms remain contractions. The tensor-core
locality and rounding argument therefore still gives the retained loose
D*p^2*2^-p error allowance. Both real and imaginary components use the
same data movement. Scalar normalization gamma is unchanged.

The complete **adapter** uses O(Tp) additional streaming/sparse-fallback
work and two main-router calls, hence

```
O(Tp*[1+p^tau polylog(p)]) + n^o(1).
```

Its main-box local numerical work is deliberately separate. Using the
old solver still costs O(T*p^(1+delta)*(d+w^2+d*w^2/L)); using #481's
conditional batching changes only its boundary factors. Neither choice
removes per-axis Gaussian work. This package proves no new complete
outer cost, optimized assembly, kappa, or unconditional multiplication
theorem. Expansion from the prime input is also outside this change.

The finite operator fixture is a three-point periodic contraction composed
with nearest-index selection, on unequal target/source shapes. It tests
the exact window, sparse-repair and source-core interfaces; it is **not a
Gaussian inverse**. Full basis checks and signed probes compare the
pipeline with a separately evaluated tensor formula. Mutants omit wrap
repair, omit tails, prefer bad main values, or use the wrong core stride.
The all-size movement argument and inherited analytic transfer remain the
main review obligations, rather than consequences of those finite tests.
