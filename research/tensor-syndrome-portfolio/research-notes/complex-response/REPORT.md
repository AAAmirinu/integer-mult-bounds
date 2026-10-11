# Complex-control lane: sufficient rewrite and bounded paid-moment screen

## Outcome

No new complex paid-moment improvement was found. Current complex lower bound is 0.001305231506267591, above the tn12 bit lower bound 0.001298290062988365072981. A complex-only improvement would therefore not raise tn12 kappa. SCREEN.json records exact rational/GF(2) finite screens on the SHA-bound kernel79 word; screen.py reproduces them in about one second. This is not an exhaustive search of circuits or the full DAG.

## Sufficient temporal observability cancellation

Consider a linear straight-line program over a field, with designated target projection P. Let two additive instructions, at i<j, add a*x_s to x_u and b*x_s to x_v. Assume neither instruction writes x_s and no intervening instruction writes x_s. Let R_i and R_j be the maps from a perturbation immediately after each instruction to the final target vector, evaluated in the original program. If

    a R_i e_u + b R_j e_v = 0,

then deleting BOTH instructions leaves the entire target map unchanged on every input, including arbitrary dirty helper inputs.

Proof: the source x_s is identical at the two positions and is unchanged by deleting the first instruction, because nothing in the interval writes x_s. The difference introduced by deleting the first instruction is -a*x_s*e_u. Its propagation through the second instruction coincides with propagation when that instruction is deleted: the second instruction reads x_s and the difference in that coordinate is zero. The second deletion contributes -b*x_s*e_v. By linearity, the total target difference is -(a R_i e_u+b R_j e_v)*x_s=0. This proves exact equality, not merely vanishing first derivative. It also explains why arbitrary response dependencies without the source-stability condition are insufficient.

In the local supplier, replacing the helper/source cleanup by the literal inverse of the changed non-target program restores those registers exactly. Dirty target compensation must be reconstructed and checked if other transformations change it. The theorem itself does not license dropping cleanup, the phase wrappers, full-rank footprints, or physical owner checks.

## Exact screen

- 79 entrance pivots and 229 entrance correction gates.
- No pivot has a strictly larger common entrance subspace contained in its own first substantive frame AND every correction donor's first substantive frame. This rules out only the fixed-donor lift tested, not another kernel basis.
- No individually target-unobservable A instruction.
- Fourteen pairs satisfy the exact sufficient temporal cancellation test. Each pair has unchanged paid child-rank profile. Deleting every pair also leaves the frame-profile tally unchanged; simultaneous scalar compatibility of all pairs was not needed or certified because the paid-moment gate already rejects the candidate.
- Baseline and every tested pair profile: {1:1981,2:932,3:20,4:224,5:392,8:24}.
- Thus up to 28 scalar-instruction cancellations are worth exploring only for implementation constants. No kappa gain is claimed, and they are not inserted into the new release.

## New PR transfer assessment

PR479, exact streamed chirp phases: maintains quadratic values and first differences along a mixed-radix traversal, fewer than 2T adjacent-axis visits, O(p) persistent control, unchanged exact phase argument. Removes a dimension factor in chirp generation. It explicitly claims no kappa increase because the unchanged Gaussian margin is already no larger than the old scalar margin. Useful for a future executable scalar layer, not grounds to improve our paid supplier moment.

PR481, batched Gaussian boundary: groups right-hand sides and uses exact Strassen blocks in triangular solves, Woodbury correction and sparse couplings. The conservative boundary margin becomes (3+29r)/32-delta. It explicitly claims no new kappa; other Gaussian/normalization/field-exposure terms still bind. It can reduce a later scalar/analytic invoice only after that interface is explicitly wired; cannot be added numerically to the supplier gain.

PR482: independent non-hosting R715 target-factor/bank construction at 0.001168862033074029. Useful explicit same-owner routes and browser/release validation practices; its numerical result is below the current hosted supplier. A non-hosting route does not justify combining its bank savings with already consumed hosted residuals.

Sources inspected: the frozen public/479.txt,481.txt,482.txt and our kernel79 producer, normalization, phase and ownership code. Existing library structural inspection included LinearAlgebra/SchurBlockElimination.lean (explicit elimination/reconstruction equivalence), External/IntegerMultBounds20261008/Matrix/LateQuotient.lean (late decoding from an explicitly assumed circuit identity), and InversionResponseReconstruction20260907.lean (signed response reconstruction). None supplies a free physical rank reduction. These were source reads, not new kernel audits, and do not constitute searching the entire tree.

## Reuse recommendation

Keep the completed complex supplier unchanged while the bit side binds. Use the finite sufficient temporal rewrite as a future candidate generator only when it removes a frame touch and improves the actual paid profile. Re-run all-column, phase, owner and moment checks on any accepted changed construction.
