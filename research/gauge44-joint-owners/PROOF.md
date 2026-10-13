# Joint whole-family owners: exact legality and strict moment improvement

This package changes the complex whole-family owner assignment of the Gauge44 construction. The local Gauge44 word, native provider, ports, centers, residual widths, 72-call dispatch, asynchronous controller order, and physical stock remain those of PR645. The final owner map is a strict moment improvement over both PR645 and PR649, whose stronger repacking appeared during this work. The bit supplier and the final outer bound are admitted separately by `verify.py`.

The final map is `data/OWNERS.json.gz`, with compressed-input SHA-256 `171bb95fb21461563b846a69ff3f5dc0a0ff9d81f282f467a09aae4b63cdee00`. It was obtained by 22 strict joint owner reallocations from the actual PR649 seed, in one bounded pass over 120 nominated call pairs, with a two-second solver cap per model. The optimization program supplies a nomination; the proof below uses only the frozen integer assignment and independently reconstructed geometry.

## Pinned comparison maps

| Comparison | Source commit | Owner input SHA-256 |
|---|---|---|
| PR645 | `638a5171dd1aca89ff50d07dcbe288b567769804` | `90ff7657a23dcfb67532b49c0800c5fc259b27c89005081e24bf184869e1bd57` |
| PR649 | `1b931ee055d738753778e1051300140c16ae219d` | `2e044174dea692e558772def65c54d31867542b5f1061206f562fc2ee3cdb535` |

PR649's actual map is retained as `data/PR649-OWNERS.json.gz`. Its published package deliberately preserves PR645's old evidence and result files for provenance. Those files are not used to infer the PR649 comparison profile: `independent_owners.py` reads and checks its actual owner assignment.

## Literal controller and physical-family legality

The independent checker imports no optimizer, emitter, or upstream checking program. It reads the actual canonical provider and derives all 492 residual widths from the native entrance and final frames. The inventory is `{4:52, 5:48, 7:34, 8:114, 9:244}`. It also reads the local paid profile literally.

The checker reconstructs complete-call positions from PR645's serialized `execution_schedule`. Every bridge is included as an actual family touch. For each owner replica and pending child, the legal window is the strict interval after that family's previous touch and before its pending idle sweep. Every derived eligible-call list must agree exactly with the pinned plan. Each of the eight replica controllers preserves all nine stages, and every local invocation is indivisible. The two zero-rank pending children are explicitly excluded only after reading their actual phase ranks; all 18 positive children remain charged.

For every one of the 35,424 helper occurrences, the checker verifies:

- The helper, stage, replica, time, residual width, port, copy, and physical-family formula.
- One whole helper per physical family in a complete invocation, with no active data family used for hosting.
- The literal window inequality, rather than only a nominal deadline.
- Capacity, disjoint coordinate footprints across calls, and compact prefix consumption within each pending child.
- The exact residual and spectator chart: all 73 columns are reconstructed from the pinned pending axes, with the active coordinates and nine-coordinate invocation embedding checked explicitly.

The chart is a permutation of an independently checked orthonormal binary basis. The exact DATA-PHASES input hash is `c5916ff312678f12aba403847643fbbc29f643acec60bdf836fa56cd3e8251fa`, matching the provider's bound artifact. The baseline chart stream hash is reproduced before the new map is audited. The final map has 7,550 distinct charts and chart-stream SHA-256 `f3adabafdd6af8f448a5e8dbedc4caac0f4a58a70a72a3a7c27fa2c42d1b7cf6`.

All 7,168 live data families and the physical stock of 7,670 remain unchanged. That stock includes eight center slots, 492 reserved helper slots, and two coefficient slots. Every idle remainder is included in the derived paid profile. No new role or free completion is inferred from the packing score.

## Exact improvement for every exponent between zero and one

For one comparison map, let `a_r` be its idle-remainder multiplicities and let `b_r` be those of the new map. Pad both distributions with zero remainders to the same 16,128 pending-child coordinates. Their first moments agree. The complete paid rank mass remains 520,704, so the deficit is still

`73 · 7168 − 520704 = 2560`.

For each integer threshold `k`, define the exact stoploss difference

`D_k = Σ_r (b_r − a_r) max(r − k, 0)`.

The integer audit establishes the following independently for both comparisons:

| Comparison | `D_0` | Thresholds with `D_k > 0` | Maximum `D_k` | `D_k = 0` again for |
|---|---:|---|---:|---|
| PR645 | 0 | Every integer from 1 through 47 | 1,061 | `k ≥ 48` |
| PR649 | 0 | Every integer from 1 through 31 | 54 | `k ≥ 32` |

For any function `f` on the nonnegative integers with `f(0)=0`, and any integer `x` from zero through 48, the exact discrete identity is

`f(x) = x f(1) + Σ_{k=1}^{47} [f(k+1) − 2f(k) + f(k−1)] max(x−k, 0)`.

Take `f(x)=x^p`, where `0<p<1`. Every bracketed second difference is strictly negative. Multiplying by `b_r−a_r` and summing cancels the linear term because the first moments agree. For each comparison, every `D_k` is nonnegative and at least one is strictly positive, so the remaining sum is strictly negative. Consequently

`Σ_r b_r r^p < Σ_r a_r r^p`

for every such exponent, separately against PR645 and PR649. The local paid profile and live/ambient denominators are unchanged, so the same strict inequality holds for the complete complex supplier moment. This argument needs no floating-point root or optimizer assertion.

The final complete profile is

`{1:181029, 2:29091, 3:32312, 4:11521, 5:4032, 7:27, 8:577, 16:4, 20:1, 32:9, 48:2357}`.

It has 260,960 paid children, compared with 261,239 for PR645 and 260,986 for PR649. The new assignment differs in 3,237 records from PR645 and 1,530 from PR649, including offset compactions. The exact profile deltas and every integer stoploss value are retained in `evidence/INDEPENDENT-OWNERS.json`.

## Verification and scope

From this package directory, the portable independent check is:

```sh
python3 independent_owners.py --main /path/to/pinned-main --parent /path/to/pinned-pr645/research/gauge44-global --owners data/OWNERS.json.gz --compare PR649=data/PR649-OWNERS.json.gz --out evidence/INDEPENDENT-OWNERS.json --mutation-controls
```

Only Python's standard library is needed. Assertions must remain enabled; the program explicitly rejects optimized execution. Six mutation controls reject a wrong residual width, capacity overflow, family alias, duplicate helper, overlapping footprints across calls, and borrowing outside a literal idle window. The retained receipt contains no machine-specific path.

This proof establishes whole-family allocation legality and strict complex-moment improvement. `verify.py` separately replays the local scalar and Clifford providers, global native controller, coefficient invoice, bit admission, and outer assembly. The inherited all-size compiler, common-label and mutable-source realization, normalized wrappers, precision/tape, exact recovery, analytic-transfer, and bit interface assumptions remain conditional. This is not an unconditional multiplication theorem or a Lean certification of the complete construction, and it does not establish the requested κ ≥ 2^-8 target.

## Attribution

PR645's Gauge44 factory and 44 cold rank-four endpoints are icekylinx's construction. PR649, by jeremykothe2, supplies the dissolved seed map and already composes the same reviewed PR589 bit supplier. Its gap-merge lineage credits vectorsss / Chi Zhao's PR638 `relocate_two` method. The PR635 lineage and all upstream contributors, licenses, notices, and conditional interfaces are retained. The new contribution is the jointly reallocated owner map, its exact comparisons, and the independent legality and concavity proof. Prepared with substantial OpenAI Codex assistance.
