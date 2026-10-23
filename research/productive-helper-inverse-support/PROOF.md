# Proof of the scoped cold-basis obstruction

## 1. Reverse-support necessity

Work with arbitrary independent vector-valued registers over the rationals.
Every scalar instruction is an invertible ADD or nonzero SCALE. At a scalar
contact, all participating registers use one common canonical binary chart.
Along a paid transport assume chart inclusion `A subset B` in the forward
direction. Retained transport changes representation, not the logical scalar
register value. There are no native operators inside the replaced local block.

Let `R` be its invertible scalar matrix, with input charts `A_i` and output
charts `B_j`. Then

```
R[j,i] != 0       implies A_i subset B_j,
R^-1[i,j] != 0    implies A_i subset B_j.
```

For the first implication, a nonzero coefficient has at least one chronological
dependency path from input `i` to output `j`. Charts increase along that path.
For the second, reverse every instruction and transport. The inverse scalar
circuit has decreasing charts. A nonzero inverse coefficient has a reverse
dependency path from output `j` to input `i`, giving the same containment.
Cancellations can remove coefficients; they cannot produce a nonzero coefficient
without a path. This proves necessity, not sufficiency.

## 2. Source-derived block factorization

Use the source and interval in README.md. All 24 local inputs are independent;
the fifteen cold helpers have zero charts but arbitrary data. Let `B=P T`, where
`T` acts on outputs 417/419 and `P` exchanges outputs 416/417. Exact row replay
gives `(B M x)_416 = x_13 + x_416`. Thus the available ascending preparation
`E:416+=13` makes `S=B M E^-1` fix its carrier row. After ordering carrier 416
first, write

```
S = [[1,0],[c,D]],
S^-1 = [[1,0],[-D^-1 c,D^-1]],
alpha = D^-1 c.
```

The checker verifies inverses and the factorization exactly. The only nonzero
entries of `alpha` are `+1/2` on 418,419,420,421,424,425 and `-1/2` on 430,431.
All are in the cold set `C={417,...,431}`. Matrix notation in the implementation
retains an identity carrier row and column; `D` here denotes its outside block.

Consider **any** invertible rational `Q` supported on `C`, extended by identity
on the other outside registers. Grant its implementation without imposing any
extra restriction. With protected value `u` fixed, apply all prefix compensation
`z -> z + beta u`, where `beta=Q alpha`. To reach `c u + D x` from `Q x+beta u`,
the remaining outside matrix is uniquely `R=D Q^-1`. It leaves carrier 416
untouched. Every row with nonzero `beta_i` has received `u` at a common chart
containing direction 73; subsequent ascending transports retain 73 there.

The exact, source-reconstructed identity is

```
alpha_C = -D^-1[C,78] + (1/2) D^-1[C,431].                 (1)
```

This is a projected identity on `C`, not an asserted identity on foreign main
coordinates. In particular it does not justify ruling out changes to main
carriers, interleaved compensation, or a larger scalar region.

## 3. Suffix caps without native or helper constraints

After the local output basis `B`, emit the same source suffix conjugated by `B`
and append `B^-1`. The paired source native maps are equal on helpers 417/419,
so this is the nominated logical continuation. The checker verifies their exact
map columns and all positive/inverse occurrences. The backward program uses
the corresponding inverse-transpose basis.

Build the chronological graph of scalar contacts and final main endpoints.
Every paid edge imposes inclusion from its earlier to later node. Owned contacts
have their source chart; all other scalar contacts have variable charts.
For the feasibility relaxation, delete **every native relation**, omit all
adapter pins, and leave **every helper final chart free**. Each remaining graph
component is a directed acyclic graph with identity inclusions. Propagating the
intersection of descendant fixed charts backwards therefore gives the greatest
allowed chart at each node. These are necessary constraints for any actual
native choices and helper boundaries, since removing constraints cannot reduce
the feasible set.

The exact caps at local outputs 78 and 431 are respectively
`span(25,45,462)` and `span(45,76)`. Neither contains 73. A separately validated
paid-only path of length 8 from 78 and length 9 from 431 ends at main 125's fixed
chart, which excludes 73. No native choice, helper return chart, or adapter
interpretation occurs on those paths. The checker derives the same caps in both
orientations and for both declared suffix variants. Coalescing is only by exact
commuting ADD merges; every crossed instruction is checked.

## 4. Contradiction for every cold basis

Since `Q` is invertible and `alpha` is nonzero, choose a cold row `i` with
`beta_i != 0`. Its input to `R` contains 73. Section 1 and the output caps in
section 3 require

```
(Q D^-1)[i,78] = (Q D^-1)[i,431] = 0.
```

Row `i` of `Q` is supported on `C`, so multiplying (1) by that row gives

```
beta_i = -(Q D^-1)[i,78] + (1/2)(Q D^-1)[i,431] = 0,
```

a contradiction. This includes concentration into one slot and compensation
distributed among any number of cold slots. It does not depend on pivot order,
temporary matrix fill-in, or the scalar instruction count used to realize `R`.
The obstruction in the forward program alone rules out a complete dual supplier in this scope;
checking both suffix orientations provides additional source validation.

## 5. Entire scalar-encoder extension

The same argument also applies to the larger source interval `[6347,10315)`.
This begins immediately after phase A's last native operation and ends at the
centers marker. Every intervening instruction is an invertible scalar ADD or
SCALE on persistent registers. Treat all 632 entries at this cut as independent,
including every dirty register. Reconstructing their actual current charts
gives 457 zero-chart outside registers, including cold main registers.

The desired row is again exactly `entry13+entry416`. With this larger `M`, form
the same `S=B M E^-1`, `D`, and `alpha`. Exact sparse inverse replay gives the
same compensation coefficients as section 2 except that entry 424 vanishes.
The two-column identity (1) holds on **all 457** cold coordinates, and alpha
has no support outside this set. The checker derives this from the full source,
not by extrapolating the 24-role calculation or assuming untouched spectators.

Rebuild the declared conjugated suffix from cut 10315. With all native edges,
helper final pins, and adapter pins removed, its caps at 78 and 431 still exclude
73. Applying section 4 rules out every invertible basis on the 457 cold inputs
and every distribution of the complete upfront compensation, followed by an
ascending outside scalar circuit and that suffix. This closes enlargement to
the whole scalar encoder under the same scheduling premise.

## 6. Limits

The theorem fixes the nominated source-consuming block, prefix placement of
all compensation, and one of the two explicitly generated suffix contact
graphs. It does not fix local exit charts beyond necessary suffix caps. It
assumes subspace inclusion on paid edges; equal-dimensional rotations and
downward transports must be charged and are outside this proof. Different
scalar suffixes, main interfaces, native-bearing replacement blocks, larger
encoder regions crossing native operations, or a different interleaving require
a fresh calculation.
No global lower bound on productive-helper algorithms or kappa is inferred.
