# Fixed E8 center-basis obstructions

This is a finite obstruction proof for the **frozen R779 local E8 word**.
It does not prove optimality among new motifs, new center completions,
nonmonotone live words, collective helper operators, or changed endpoints.
It changes no supplier and claims no new multiplication exponent.
The existing supplier's source attribution is retained in
`research/e8-clean-reuse-extension/NOTICE.md`.
Prepared with substantial OpenAI Codex assistance; new code is Apache-2.0.

## Data and conventions

Read the pinned `kernel-base.json.gz` from the E8 clean-reuse extension.
It has h=9, v=120, R=779 and eight retained totals. Its 120 distinct binary
port vectors q_t in F_2^9 have odd weight, hence q_t·q_t=1. Port indices
in the certificate below are zero based.

Set the clean source registers to independent indeterminates x_s and set
the other registers to zero. Replay phase A over Q, preserving the exact
order and rational coefficients of every addition. The eight retained
clean totals define an 8-by-120 matrix B:

    total_k = sum_s B[k,s] x_s.

Apply the pinned scatter table to these totals to obtain a 120-by-120
center matrix C=AB. Every entry of B is integral in this frozen word; the
computed common denominator is 1. These are **characteristic-zero scalar
matrices**. Their binary port labels are separate frame data.

The helper/source/target basis and the center row-space are frozen for
the second result below. No claim about arbitrary dirty states is needed
to prove these clean source-support obstructions.

## 1. The monotone side restriction

Assume every live role has an increasing subspace frame path, every
scalar gate has one common frame on all its incident roles, source X_s
starts at the line <q_s>, and target Y_t ends at q_t^perp. Consider a
causal dependency path from x_s to Y_t that uses only such live gates
and increasing transitions. At a scalar gate its source and target
share the frame; subsequent frame changes only enlarge it. Induction
along the path therefore gives <q_s> contained in q_t^perp.

Consequently its scalar side coefficient is zero whenever q_s·q_t=1.
This conclusion is preserved under cancellation of paths: if no path
exists, summing their coefficients still gives zero. It does not apply
to a copied center whose frame decreases from the full space to zero,
nor to a new program that changes the stated monotonicity or endpoints.

If the total clean data map is I and S denotes this restricted side
map, the complementary center map satisfies

    C[t,s] = delta[t,s] whenever q_t·q_s = 1.

The producer also checks this pattern directly in the frozen C using
exact rational arithmetic, including every C[t,t]=1.

## 2. At least eight scalar center channels

The following eight ports are pairwise nonorthogonal over F_2:

| Port index | Binary port, expressed as an integer |
|---:|---:|
|0|7|
|13|25|
|22|97|
|27|385|
|92|505|
|105|487|
|114|415|
|119|127|

Their pairings, including self-pairings, are all 1. By the preceding
restriction the corresponding principal minor of any complementary C
is exactly I_8. Thus rank_Q C >= 8. A center realization through j
scalar totals factors C through Q^j and has rank at most j, so j >= 8.
For the frozen C, the displayed factorization C=AB with eight rows
also gives rank_Q C <= 8; its rank is exactly 8.

The graph here is the binary **nonorthogonality** graph. No assertion
that the port vectors form a rational orthonormal family is used. The
rank conclusion concerns scalar channels, not physical Fourier ranks.
It does not say every alternate rank-eight completion equals the
frozen C or has its row-space.

## 3. Every nonzero frozen center form has full binary source span

For each nonzero a in F_2^9 define the binary hyperplane

    U_a = {q : a·q = 0},
    E_a = {s : a·q_s = 1}.

The certificate supplies eight distinct columns J_a contained in E_a
such that the integer 8-by-8 minor B[:,J_a] has nonzero determinant
modulo the prime 101. It contains all 511 values a=1,...,511, not a
sample. Each record gives `normal`, `outside_ports`, `minor_columns`,
and `nonzero_minor_mod101`. The producer verifies the outside condition
and computes the determinant of the selected square minor afresh.

An integer determinant nonzero modulo 101 is nonzero over Q. Since B
has eight rows, this proves rank_Q B[:,E_a]=8 exactly. No CRT, probability
estimate, finite-field extrapolation, or numerical tolerance is needed.

Now let b=lambda^T B be a nonzero rational center form. If the binary
span of the port vectors in its nonzero scalar support were proper,
that span would be contained in some U_a with a != 0. Then b_s=0 for
every s in E_a and lambda^T B[:,E_a]=0. Its rank is eight, so lambda=0,
a contradiction. Hence

    span_F2 {q_s : b_s != 0} = F_2^9

for every nonzero b in the frozen center row-space. The same proof
holds over any characteristic-zero coefficient extension, including
Q(i), because the witnessed integer minor remains invertible there.

## 4. Consequence for rebasing the frozen centers

A monotonically gathered clean form supported on sources q_s needs a
frame containing all their source lines. Result 3 forces that frame
to be the full nine-dimensional space for every nonzero form in the
frozen center row-space. An invertible basis change of its eight
centers selects eight nonzero forms in the same row-space; none can
be gathered at frame rank below nine.

In the current copied-center primitive, each is copied at that frame,
then carried by a paid exact child from that frame to frame zero, and
only then scattered into Y at frame zero. Its Fourier rank is therefore
nine. Rebasing these eight forms leaves the local copied rank mass
at least 8*9=72. The frozen word attains that value. With 9 stages and
8 replicas, this is 576 rank-nine children and global rank mass 5184.

This obstruction excludes lowering the copy cost **solely by changing
the basis of the frozen center row-space**. It does not exclude an
alternate center completion, nonmonotone live transitions, a changed Y
chronology, different source/target endpoints, or a genuinely joint
bank construction with a fully audited data/helper endpoint.

## Pins and reproduction

The immutable derivation snapshot is retained in `vendor/`. `SOURCE-PINS.json`
binds it and the supplier inputs by SHA256. The portable executable changes
only default paths and output handling. From a repository checkout:

```sh
python -B research/e8-structural-frontiers/verify.py /fresh/output
```

All 511 explicit minors are freshly recomputed. Expected mathematical records
are compared only after calculation; host-specific absolute paths are omitted
from that comparison. This proves the finite statements above, retaining the
supplier's separate all-size compiler, fixed-tape, routing and analytic gaps.
