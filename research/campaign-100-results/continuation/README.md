# Continuation after PR364

This continuation was executed on 2026-10-11 and is separate from the historical campaign.
Source: PR364 commit `f8c6a47abfec24b87cb1eb0a138dd73dfce2abe4`.
Result: [PR366](https://github.com/CrocSwap/integer-mult-bounds/pull/366), certificate head
`d3d84202e528d6e147a8ea62463ae5c0125997cf`.

| Experiment | Outcome | Evidence |
|---|---|---|
| Commuting ADD movement, radius 64 and then unrestricted range | 84,214 placements at 19,914 boundary gates; zero improvements | [full search](reorder-all.json), [radius 64](reorder64.json) |
| Free-form annealing, seed 1, T0=2, 432 seconds | 50,422,591 proposals; 322 changed frames; improved candidate | [selection](freeform364.json), [log](freeform364.log) |
| Exact beneficial-component reduction | 99 changes in 30 components; kappa 0.000804928788870063 | [selection](freeform364-reduced.json) |
| Cold annealing, seed 7, T0=0.1, 144 seconds | 14,135,553 proposals; zero selected moves | [result](freeform364-cold.json), [log](freeform364-cold.log) |
| CP-SAT, 180 seconds, 2 workers | FEASIBLE, not OPTIMAL. Whole candidate had worse search cost; beneficial components retained separately | [raw result](cpsat364.json.gz), [log](cpsat364.log), [normalized frame IDs](cpsat364-normalized.json.gz), [reduction](cpsat364-reduced.json.gz) |
| Combine compatible beneficial components | 123 frame changes, 35 components; kappa = 160987957846297/200000000000000000 | [combined selection](combined364.json), [candidate replay](candidate-combined.log) |
| Full standalone final package replay | PASS_SOURCE_BOUND_COUPLED_RETIMING; 0 source-span violations and restored registers; native five-stage checks and exact pricing pass | [receipt](PR366-RESULT.json), [full replay log](PR366-replay.log) |

The final kappa is 0.000804939789231485, up 0.007506520200 percent from PR364.
The original signed scalar sequence, COPY windows, endpoints, register stock and rank mass are preserved.
This is a conditional finite-word improvement under the inherited compiler, chart, restored-row,
selector/routing, prime-supply, precision/recovery and analytic interfaces. It is not a global optimum
or an unconditional multiplication theorem. Search estimates are not certificate inputs.
The replay log and receipt are execution evidence, not a substitute for replaying PR366's pinned package.
