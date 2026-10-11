# Blockwise evaluation-pair exposure

## Constructed improvement

The selected circuit changes which already-computed pair values are copied into PR507's own-tetrad helpers. It retains the public factory's 560 helpers and exact scalar endpoint, while changing the geometric frames at which the 112 own-helper values first become available. Reconstructing the response cancellations gives 99 pivots, compared with the previous 92, using 113 donors in eleven classes. This is a change to the actual circuit's admissible exposure geometry, not a relabeling of a donor search or a same-frame basis change.

For a tetrad ordered t0,t1,t2,t3, define the three pair covers:

    0: (t0,t1), (t2,t3)
    1: (t0,t2), (t1,t3)
    2: (t0,t3), (t1,t2).

The public partial-own constructor uses cover1 in both parity tetrads of all fourteen blocks. The selected circuit uses cover0 in both parities except in blocks {0,2,4,6} and {0,3,4,7}, where it uses cover1. The factory already computes both independent linear pair values for every selected pair. Each copied pair basis is invertible and lives at its existing rank-two frame. No extra pair computation is assumed free.

Let x be the four source values of a tetrad, T its actual copied pair-basis matrix, and M the required own-output matrix. The constructor computes T^(-1) exactly and emits an elementary factorization of M T^(-1) at the admissible tetrad frame. Thus (M T^(-1))(T x)=M x. The inverse cleanup is rebuilt from the actual circuit. All selected scalar denominators are powers of two, and every scale is a signed power of two, as required by the existing scalar compiler.

This clean calculation is only the first step. The actual helper response matrix C is recomputed. For each selected common entrance frame E, every pivot column is expressed as a rational combination of donor columns. The corresponding prefix corrections cancel that response; all frame containment chains are checked. Dirty-input compensation is rebuilt and checked on every basis column in both forward and inverse-transpose orientations. The selected word passes 800 columns in each orientation and 99 independent omitted-correction controls.

The local child profile is:

    rank:   1     2    3   4    5   6  7   8
    count: 2530  182  516  88  298  68  1  17

The whole-residual inventory is 18 width-seven, 161 width-eight and 381 width-nine helpers. Relative to the previous 92-pivot word, the local delta is -9 rank-one, +22 rank-two and -14 rank-three calls. The seven local rank units removed correspond to the seven extra entrance dimensions; the complete owner allocation pays the changed idle remainders. Consequently the final global gain is determined from the full invoice, not by adding seven free deficit units. The hosting lane has produced a literal 40,320-role assignment; the final independent provider and outer arithmetic replay remains the authority for the published exponent.

## Precise OpenAI source connection

The inspected proof is OpenAI, *Uniform marked-polygon estimates and sharp finite bridge moments* (2026), implemented in the HoneycombChords family. In namespace `OAI.CriticalHoneycomb.FiniteFunctional.StripAsymptotic`, `powerNewton_evaluation` states

    v(j)^n = sum_{k < m} powerNewton(v,n,k) * newtonBasis(v,k)(v(j)).

It factors evaluations through the first m Newton coefficients even for sparse powers of degree larger than m; the proof discards higher basis terms because they vanish at earlier nodes. `sparseTestMatrix_factor` uses this identity to factor its evaluation matrix as `sparseCofactorMatrix * newtonEvaluation`. The latter is triangular in nodal order and has positive determinant for strictly increasing nodes.

The transferred design principle is to choose an intermediate evaluation basis together with the order and geometry of its exposure, then reconstruct the exact downstream decoder. Our circuit uses only the elementary degree-one/pair-basis part of that pattern. The source theorem does not directly certify this circuit, nor does it establish the kappa gain. The new contribution is the nonuniform choice of admissible pair covers and its complete reconstructed response word. This attribution is source-inspired construction, not a claim that the whole Newton interpolation argument or its analytic positivity estimates were imported.

A useful restriction prevented a false gain: if all mixed registers have identical admissibility frames, an invertible basis change preserves the rank of every eligible response class. Such a change alone cannot increase cancellation nullity. Our selected covers change the actual first-frame subspaces, so they escape that restricted invariance statement.

## Bounded comparisons and exact evidence

Nine uniform parity-cover choices and 44 single-block or mixed-block choices were constructed, followed by 36 two-block combinations. Every recorded accepted candidate passed exact relation and frame reconstruction. A separate native 500-iteration architecture search used block-disjoint response templates; its synthesis was compared exactly against 80 independently constructed mixed words before use. Its best discovery-score candidate was reconstructed exactly but lost under complete inventory pricing. It is not included as a gain.

The safe single-block candidate had the same inventory as the old 92-pivot word and replaced ten rank-one calls by two rank-two and two rank-three calls. This strictly lowers the child moment for every exponent parameter between zero and one. The selected two-block 99-pivot circuit is stronger under the full physical invoice. The 101-pivot alternative was also tested; its larger pivot count did not by itself give a better supplier. All candidate screens, including losing ones, are retained.

Reproduction uses `build_pair35.py`, `pair-3-5-SPEC.json`, and the frozen `pair-3-5/SELECTION.json`. The builder regenerates the altered factory from the pinned public constructor, transfers only matching inherited scalar-event frames, reconstructs the actual kernel, checks the dyadic compiler contract, and binds the entire normalized word. It runs no optimizer. Only two previously established stale display floats and an asserted redundant register count are omitted from normalized hashing.

Public source: PR507 commit `8d4444cf8a16d500cbb94add6e4fa8bcfb9c7d5e`. Public constructor SHA-256: `8b9a7f1bb69626d76fec9e915134cec7199a70b53656723ce49ecc47f4644afd`. The inherited response/gauge compiler, pooled-owner framework and retiming originate in PR484, PR496 and PR495/501/502. The coordinated four-gauge simplification extends the PR473 inspiration and our preceding package; the asynchronous schedule also comes from our prior package. These are credited inherited mechanisms.

Normalized selected-word SHA-256: `bf26b8c3709039eb027430218f8b9bd3c369eb9c584e4ebfc2f9e350bab93f19`. Constructor replay and scalar audit receipts are retained separately. OpenAI source hashes are recorded in `EXPOSURE-SOURCES.json`; these are source inspections, not a fresh Lean kernel certification.

The mandatory local research-route controller was invoked with the written mathematical plan but rejected it because its schema requires a Lean `theorem` header. This task explicitly requested no formalization. The original plan and exact finite-search artifacts were retained; no dummy Lean theorem was substituted and no controller certificate is claimed.
