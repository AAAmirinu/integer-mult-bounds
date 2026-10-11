# A pattern-only source-span obstruction for rank-eight E8 centers

This supplement is independent of the frozen center gather matrix. It extends one part of `CENTER-PROOF.md`, while retaining a narrower conclusion than the frozen-basis rank-nine result. It is a finite statement about the 120 pinned ports and the monotone-side zero pattern; it is not an impossibility theorem for joint, nonmonotone or higher-rank center constructions.

Let `q_0,...,q_119` be the distinct odd ports in `kernel-base.json.gz`, with SHA256 `785a6160912b8bf8535ccd438c7d13c0730f874d6a5d07ef530e50279e7cf7d8`. Work over a characteristic-zero scalar field K, including Q or Q(i). Let C be **any** 120-by-120 matrix satisfying

\[
\operatorname{rank}_K C=8,\qquad C_{tt}=1,\qquad
C_{ts}=0\quad(t\ne s,\ q_t\cdot q_s=1\text{ in }\mathbb F_2).
\]

The hypotheses do not require C to be symmetric, positive semidefinite, or the currently emitted Gram matrix. The zero pattern follows from the monotone-side constraint already proved in `CENTER-PROOF.md`. If that causal constraint is changed, this supplement does not apply.

**Claim.** Every nonzero form in the row space of C has source support whose binary port span has dimension at least seven. Consequently, any eight-channel full-rank factorization `C=A B` requires each of its eight nonzero B rows to be copied at a frame of rank at least seven. Its total copied rank is at least 56. This statement does not assert that 56 is achievable.

## Finite certificate

For each nonzero binary normal a, put `E_a={t:a dot q_t=1}`. The independent program `universal_rank8_span.py` uses only the ports to build the graph with edges `q_t dot q_s=1`, and finds an eight-clique inside E_a for 391 normals. Each returned clique S satisfies `C[S,S]=I_8` for **every** C in the hypothesis. Therefore

\[
\operatorname{rank} C[:,E_a]=8
\]

for these 391 normals. `UNIVERSAL-RANK8-SPAN.json` records all 391 explicit clique witnesses, not numerical matrix ranks.

The other 120 normals are exactly the vectors of Hamming weight two or six. The program exhausts its finite clique search before putting a normal in this set. Calling these normals uncertified would be sufficient for the proof; the exhaustive search additionally establishes that none of them has an eight-clique. This does **not** show that their outside restriction has rank below eight.

The 120 exceptional normals contain no three-dimensional binary subspace. This has a short algebraic proof. They lie in the even-weight subspace, on which

\[
Q(a)=\frac{\operatorname{wt}(a)}2\pmod2,
\qquad Q(a+b)=Q(a)+Q(b)+a\cdot b.
\]

The exceptional normals are exactly the nonzero vectors with Q=1. If independent a,b,c and all seven nonzero sums had Q=1, then `Q(a+b)=Q(a+c)=Q(b+c)=1` would imply `a dot b=a dot c=b dot c=1`. But then `Q(a+b+c)=0`, a contradiction. As a redundant exact check, the program tests all 393,120 possible independent third generators extending the 3,360 all-exceptional generating pairs; no all-exceptional three-space occurs. There are 1,120 distinct all-exceptional two-planes.

## From the certificate to support span

Suppose a nonzero row-space form f has support ports spanning a subspace U of dimension at most six. Its annihilator U-perp has dimension at least three, so the previous paragraph supplies a certified nonzero normal a in U-perp. Since f is supported in U, f vanishes on E_a.

Write `f=lambda^T C`. The columns C[:,E_a] already span the full eight-dimensional column space of C. Thus a scalar functional lambda annihilating these columns annihilates every column of C, and f=0. This contradiction proves the claim.

For an eight-channel factorization, A has full column rank eight, so B and C have the same row space. Every B row is nonzero and has binary source-span at least seven. A copied frame must contain that source-span. Hence the sum of eight copied frame ranks is at least 56.

**Scope of the remaining escape.** A seven-dimensional support would have a two-dimensional annihilator whose three nonzero normals all have weight two or six, so only the 1,120 listed exceptional two-planes can occur. This is a necessary combinatorial restriction, not a construction. More than eight feature rows can have cancellations outside the row space of C, and a center completion of rank greater than eight can have localized rows. Those possibilities are not excluded here. Neither is a protocol that absorbs the Fourier bridge into a joint endpoint without these private copied centers.

## What the bound means for the target budget

Under the **additional** hypothesis that all non-center R779 calls, W=14691, m=73 and fallback stay fixed, replace the eight current rank-nine copies by eight rank-seven copies in each of the 72 invocations. This optimistic cost model has deficit 3648, and its exact moment interval at the required coarse saving b=1/499 has lower endpoint

\[
\frac{26993519853286249543575145263152640471610927815337004160704625045967}
{26959946667150639794667015087019630673637144422540572481103610249216}>1.
\]

Thus even this optimistic model misses kappa=.002. With the other invoice entries fixed, lowering the eight copied centers' ranks within a rank-eight completion is insufficient. Changes to the side word, helper endpoint, number/type of center channels, or bridge protocol remain possible. Passing any alternative cost budget would still construct no circuit or all-size theorem.

## Reproduction

From the repository checkout, with assertions enabled:

```sh
python -B research/e8-structural-frontiers/verify.py /fresh/output
```

The unmodified producer is retained in `vendor/universal_rank8_span.py`.
The verifier passes explicit source, budget, engine and output paths, enforces
all source pins and compares the fresh mathematical record after calculation.
The producer refuses output under immutable input repositories and suppresses
bytecode writes. Its mathematical JSON has no host paths.

Budget-source SHA256: `0e3a9ceb4ab14a126a8e9e0d056322f9d2234ccda4f7472a8ad2849bd7a54131`. Moment-engine SHA256: `81cbc864e106418fc7854322746f72180cb8110ff39f74450a3b8d55a82c1482`.

The existing frozen appendix/checker pair is unchanged. The elementary graph pattern is related to the E8 root-line orthogonality graph studied by [Schmidt, 2024](https://www.numdam.org/articles/10.5802/alco.335/); the source-span conclusion here is proved by the displayed finite certificates and quadratic argument, rather than claimed from that paper.
