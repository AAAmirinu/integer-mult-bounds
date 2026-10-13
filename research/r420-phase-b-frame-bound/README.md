# R420 phase B: a sharp bound for fixed-order frame reassignment

**Scoped negative result; no new κ.** In eumemic's PR543 R420 bit word,
simultaneously reassigning the frames of any of the 837 phase-B gates cannot
lower the paid recursive moment if the scalar gates, their operand lists and
order, and the surrounding D/A/scatter/C and boundary frames stay fixed.
The bound allows arbitrary rational subspaces of the eight-dimensional label
space, including frames outside the shipped catalogue. It is not limited to
single-gate moves or a local search neighborhood.

The existing schedule attains a relaxed lower bound: after independently
relaxing each register's frame path to dimension intervals, its original rank
increments majorize every allowed alternative. Both implementations enumerate
918 distinct per-register partitions across all 660 registers, with no gap.
This is weak optimality of the paid moment, not uniqueness of the schedule.

## Reproduce

From the repository root, with Python 3.11 or newer:

```sh
python3 -B research/r420-phase-b-frame-bound/verify.py
```

Expected final lines:

```text
PASS_CONTROLS 12
PASS_FIXED_ORDER_B_FRAME_BOUND gates=837 registers=660 partitions=918 gaps=0
```

Only the standard library is required. The command checks immutable input
hashes, runs PR543's existing exact label/frame/all-column/interface checker,
recomputes the certificate, exercises the controls below, and compares every
register's intervals and complete partition set against a second implementation.
An optional `--output /absolute/new/report.json` writes the full fresh report
and baseline/auditor output. Existing files are not overwritten. Neither
verification nor discovery uses a solver, floating-point arithmetic or network.

[CERTIFICATE.json](CERTIFICATE.json) is a small exact summary, including the
hash of every register's full reconstructed evidence. The independent
[audit.py](audit.py) imports no repository module: it enumerates ordered
compositions and feasible event cuts, while [check.py](check.py) propagates
sets of `(current rank, sorted increment partition)` states. The linear-algebra
implementations use separate elimination routines. Both were written with
Codex assistance in this contribution; this is computational cross-checking,
not a claim of independent human review or Lean verification.

## Statement and proof

Let `E_r` be register r's frame after fixed phase A and `F_r` its fixed exit
frame. The retained COPY/scatter boundary does not change these frames. In this
word every C gate is at the full frame on source/helper registers, and targets
do not occur in C. Thus `F_r` is the full frame for each source/helper and its
specified hyperplane for each target. The checker verifies this C restriction.
The variable bill includes the climb into C or the final frame, even for a
register untouched by B. All earlier climbs and all nine retained COPYs are
fixed.

For a gate with operand register set S, a legal frame contains every operand's
previous frame and is contained in its next frame. Compute two necessary
constraints without restricting frames to the catalogue:

1. Forward, initialize `L_r = E_r`. At each B gate set
   `L_gate = span(L_r : r in S)` and assign it to all registers in S.
2. Backward, initialize `U_r = F_r`. At each reversed B gate set
   `U_gate = intersection(U_r : r in S)` and assign it to all registers in S.

Induction in the respective direction shows that every legal reassignment
satisfies `L_gate ⊆ G_gate ⊆ U_gate`. Intersections are computed as rational
subspaces by orthogonal complements, not by intersecting lists of root labels.
The resulting interval census is:

| Gate dimension interval | Gates |
|---|---:|
| [2,3] | 120 |
| [3,4] | 10 |
| [4,4] | 457 |
| [4,5] | 10 |
| [6,6] | 120 |
| [7,7] | 120 |

For each register independently, retain only its entry/exit dimensions,
nondecreasing dimensions at its visits, and these intervals. Drop actual
subspace compatibility and agreement between registers sharing a gate. This
enlarges the feasible set, so an attained lower bound in this relaxation is
also a lower bound for all legal frame assignments.

Normalize a frame path to its gate visits and fixed exit. Extra intermediate
climbs cannot help: for `0 < p < 1`, `a^p + b^p >= (a+b)^p`. Merging them
preserves the nested endpoints and weakly reduces the bill. Enumerate all
nondecreasing integer-rank paths through the visit intervals, and sort their
positive increments. Their sum is always `dim(F_r) - dim(E_r)`.

The entire partition certificate reduces to six types:

| Registers | Baseline partition | Complete relaxed partition set |
|---:|---|---|
| 89 helpers | () | () |
| 240 helpers | (1,1) | (1,1) |
| 91 helpers | (2) | (2) |
| 18 sources | (2,2,1,1) | (2,2,1,1), (2,1,1,1,1), (1,1,1,1,1,1) |
| 102 sources | (2,2,1,1) | (2,2,1,1), (2,1,1,1,1) |
| 120 targets | (5,2) | (5,2), (4,3) |

The baseline majorizes every alternative: after zero-padding, every prefix sum
of the descending baseline is at least the corresponding alternative prefix
sum, and the totals agree. Concavity of `x^p` gives no larger baseline cost.
Here the comparison also follows directly: splitting 2 into two 1s costs more,
and `5^p + 2^p <= 4^p + 3^p` by decreasing secant slopes of `x^p`.
Therefore the attained lower bound for B plus its exit climbs is

```text
Phi_B(p) = 720 + 451 * 2^p + 120 * 5^p,     0 < p < 1.
```

Its rank mass is 2222. Adding the fixed exterior and COPY profile
`{1:600, 2:989, 4:60, 8:9}` reproduces the complete published local profile
`{1:1320, 2:1440, 4:60, 5:120, 8:9}`, rank mass 5112. A common positive
normalizing factor and fixed hosting/fallback terms preserve this comparison.
In the inherited bit pricing convention `p = 1-c`, this also minimizes the
equivalent excess charge `sum H_k * (64^c * k^(1-c) - k)` for `0<c<1`.

## Controls and completed coverage

The driver checks exact subspace intersection without common listed generators,
rejects same-rank unequal-space containment, and checks the majorization
direction and equal-mass condition. The rank-state algorithm is compared with
literal rank-path enumeration on all 1,000 three-visit interval domains over
ranks 0 through 3.

A substantive control promotes B[8], the target-8 single-source read, from its
rank-2 frame to its legal rank-3 upper intersection. This adds a previously
uncatalogued frame. The complete frame walk remains legal, but the checker
finds gaps at source register 13 and target register 128, with baseline
partitions `(2,1,1,1,1)` and `(4,3)` respectively. Removing the mandatory
rank-2 constraint from target 8 instead exposes the spuriously favorable
partition `(7)`. Thus the checker can detect both a suboptimal legal schedule
and the effect of omitting required source access.

Other controls reject an illegal rank-0 read, a non-full cleanup gate, corrupted
partition-count and rank-mass certificates, an omitted gate census entry, and a bad input
pin. These are finite checks of the stated obligation. The generic induction,
normalization and concavity argument above supply the link to all legal
reassignments and all `0<p<1`; no finite sampling of exponents is used.

The stopping rule is complete enumeration of the relaxed paths for every
register of this one frozen word. This is not a failed heuristic search.
Assignment seed **8** selects the third of the three locally recorded candidate
tasks via `8 mod 3`, rotates the register traversal, and selects the concrete
B[8] control. [CLAIM.json](CLAIM.json) records the alternatives and overlap check.
There was no pinned sprint coordination issue, so the claim was recorded locally.

## Pins, scope and credit

Base: **66849e1475c930fd7732b1a0067ffee7e1e95f60**.
[SOURCES.json](SOURCES.json) pins the input word and baseline checker from
[PR543](https://github.com/CrocSwap/integer-mult-bounds/pull/543), head
`2065fe4f72a914d907f1046603f5a36f17018535`. The selected record at this base is
PR626 with PR543, κ = `51110230636731/31250000000000000`; its construction and
maintainer review were consulted. This contribution changes neither that record
nor any supplier input.

This result excludes gate reordering, moving individual summands across other
gates, factoring, pruning, resynthesis, changes to A/scatter/C, new helper or
COPY boundaries, alternative bit words, and changed hosting/assembly. It does
not rule out improving R420 through those mechanisms or improving the R439
punctured supplier. No stronger bound on integer multiplication follows. The
inherited compiler, common-label/mutable-basis realization, whole-call hosting,
precision/tape and analytic-transfer obligations remain conditional.

Credit to **eumemic** for PR543's R420 word, interleaved interface and exact
checker, and the PR493 lineage; **Dylan Crow** for PR370's word format and
framework; **DreamingOfClouds** for PR510 and PR589; **Dugongue** for PR541/548;
and **Rohan Arun / rohanarun** for PR542. PR589 already tunes both A and B,
including least-span frames, and explicitly does not claim optimality. Its
source at `a5afc8c6169ea61ba7c51dfd3cade02cc7b13b46` is related prior work, not
an execution dependency here. This contribution adds a simultaneous all-frame
bound for the specific R420 B schedule, rather than rerunning its greedy search.
The selected PR626 review and cumulative supplier authors retain their credit.

Prepared for **yuj1r0** with substantial **OpenAI Codex** assistance, including
separate Codex workers for computational cross-checking and scope review.
New files use the repository's Apache-2.0 license. Predecessor files and notices
are read unchanged. This is a finite-instance mathematical bound with an exact
replay, not a formal proof of the complete multiplication theorem.
