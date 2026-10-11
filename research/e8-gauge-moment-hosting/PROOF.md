# Packing change and proof boundary

## 1. Fixed construction

Keep #484's `gauge80-kernel42` word and its nine-stage geometry: m = 73, h = 9, v = 120, R = 560, eight replicas, 7,680 data families. The helper widths per invocation are 438 of width nine, 104 of width eight, 14 of width seven, and four of width five. No scalar gate, entrance frame, target level, center path, phase recipe, wrapper, or schedule changes.

A pattern places whole residuals into one pending idle child. Each stage appears at most once in a pattern. The sum of widths does not exceed the pending rank. Each idle child has 120 physical copies per replica. Patterns collectively use no more than the available helpers of each stage and width. The inherited window check proves that children sharing one physical family have disjoint eligible stages. Thus the unchanged one-owner rule applies to every hosted entering helper and its borrowed spectator coordinates.

`data/SELECTION.json` is an integer witness for these conditions. The unchanged #484 emitter constructs all owners and routes; its independent audit checks the resulting template. `code/check_selection.py` separately reads the selection, checks all supplies and capacities, and derives the paid profile without importing the emitter, bank tiler, or optimizer.

## 2. Exact accounting

All 122 entering helpers are hosted in every invocation. There are 66 unhosted width-nine helpers across the nine stages, each repeated in eight replicas. They fill 66 pure banks, eight disjoint nine-axis residuals per 73-axis bank and one paid rank-one pad. No wrapper acts on a bank. Banks per stage are `[4, 0, 0, 0, 0, 0, 0, 0, 62]`.

The resulting 39,792 hosted residual instances, 7,746 live families, 8,324 physical families, and rank deficit 2,496 are read back from the emitted template. The profile is:

| Rank | Children |
|---:|---:|
| 1 | 148282 |
| 2 | 66816 |
| 3 | 7408 |
| 4 | 19728 |
| 5 | 24368 |
| 6 | 1744 |
| 7 | 1800 |
| 8 | 4376 |

Relative to #484, the only profile changes are +66 rank-one children, −528 rank-five children, +528 rank-six children, and −66 rank-nine children. Their total rank change is zero. The stock, local word, and fallback charge count remain unchanged because the total number of children also stays unchanged.

## 3. Why the full moment improves

Write p = 1 − b with 0 < p < 1. The change in the unnormalized main moment is

`66 [1 + 8·6^p − 8·5^p − 9^p]`.

For f(x) = x^p, the derivative f′ is strictly decreasing and strictly convex on positive x. Its average on [1,9] is strictly larger than f′(5), by strict convexity and the interval's midpoint. Its average on [5,6] is strictly smaller than f′(5), by strict decrease. Hence

`f(9) − f(1) > 8 [f(6) − f(5)]`,

so the displayed moment change is strictly negative. This is an improvement for every b in (0,1), not merely for the floating-point search point. The fallback mass uses the unchanged child count and live stock, so the complete charged moment also improves.

The supplied exact assembler independently encloses the new root with two rational engines. It certifies b = 1326875818805153 / 10^18 and rejects the next grid point. It recomputes the inherited finite invoice with the actual stock and combines this with the fresh #493 bit saving 391360506745414227149 / 250000000000000000000000. Six bootstrap levels and 47 strict inequalities give κ = 1325117552367841 / 10^18. The next κ grid point and invalid outer parameters are rejected.

## 4. Scope and validation

The default verifier executes both source packages from scratch. #484's complete `--all` replay validates the fixed local word and its Lemmas A and G, including all 512 basis columns for each recorded operator identity, sampled and structured complete-program columns in both orientations, dense dirty inputs, and mutation controls. The new global packing receives a separate unchanged hosting audit, plus an independent count check. Banked-entering-helper controls are inapplicable to the new packing because all entering helpers are hosted; they are still exercised by the fresh original #484 replay.

#493's full replay verifies the actual source-carrier word using the unchanged official C++ cohort checkers with real Boost arithmetic, the declared mutable-source interface checker, hosted realization, invoices, and regression controls. The complex assembler consumes the bit saving, charged composition coefficient, and row allowance from that fresh result, rather than a copied headline value.

The conditional all-size compiler, correlated dirty-array, mutable-basis, whole-owner normalization, and analytic interfaces are inherited unchanged. Finite exact replay does not discharge those interfaces. No Lean theorem or unconditional bound is claimed.
