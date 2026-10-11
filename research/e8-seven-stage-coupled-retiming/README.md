# Seven-stage E8 with the coupled complex retiming

Combining PR365's four coupled frame changes with PR373's seven-stage construction raises the conditional integer-multiplication saving to

**κ = 233014627343551 / 250000000000000000 = 0.000932058509374204.**

This is approximately **0.01551% above PR373** at commit `3ff87b5dc0b22a57958547ee347d5da25b7f9401`. The bit word, its seven-stage layout, replica count, banks, and finite bill are unchanged. The improvement comes from applying PR365's already checked complex circuit to the seven-stage complex supplier. This package claims that composition, not a new E8 word or new retiming discovery.

| Quantity | PR373 baseline | Composition |
|---|---:|---:|
| Complex coarse saving b, denominator 10^18 | 932783231884153 | 932928054566567 |
| Bit coarse saving c, denominator 10^18 | 968197503705007 | unchanged |
| Final κ, denominator 10^18 | 931913956512090 | 932058509374204 |
| Complex recursive calls in seven stages | 29978 | 29971 |
| Complex rank mass | 94473 | unchanged |
| Complex width / live normalization | 63 / 1503 | unchanged |
| Complex deficit / maximum child | 216 / 31 | unchanged |
| Complex scalar primitive steps, forward / backward | 68158 / 72856 | unchanged |

The complex side still binds. The exact difference in κ is `72276431057 / 500000000000000000`.

## Replay

Requires Python 3.11 or later, NumPy, SymPy, mpmath, a C++17 compiler, Boost headers, Bash, and `sha256sum`:

```sh
python -m pip install -r research/e8-seven-stage-coupled-retiming/requirements.txt
python -B research/e8-seven-stage-coupled-retiming/verify.py /path/to/fresh/output
```

The output must be outside the package and not already exist. On macOS with Homebrew Boost, add `--boost-include /opt/homebrew/include`. Temporary files stay beneath the supplied output. Allow several minutes and at least 200 MB of available output space.

The verifier first runs the entire pinned PR373 replay, including its producer reconstruction, native all-column checks, negative controls, geometry, banks, finite bills, five-stage regressions and original complex supplier. It then runs PR365's reconstruction and complete rational scalar-map comparison, binds its source certificate to PR373's original certificate, and checks the retimed circuit through PR373's complex B3 label, scalar, splice and precision checkers with frozen new pins. Neither vendor tree is edited.

Both exact rational moment engines prove the new complex saving and reject the adjacent 10^-18 grid point. The unchanged bit certificate is repriced with that supplier; all 47 strict outer constraints hold and the next κ grid point is rejected. The resulting finite bit bill must equal the baseline receipt. `RESULT.json` is written only after all checks pass. Expected results are comparison targets, not substitutes for replay.

The full original Bash replay receives a small transport adapter for paths containing spaces and for the chosen Python interpreter. It retains every original scientific check. A standard-header compatibility file supports macOS Clang. `SOURCES.json` pins both source PRs and that header; `MANIFEST.json` binds every shipped file. All source notices remain in the vendor trees.

## Why the cost decreases

PR365 independently checks the one-invocation histogram delta

```
rank:   1   2   3   4   5   6
count: +2  -6  +4  +1  -6  +4
```

It is a positive weighted sum of second differences of `x^p`, with weights `(1,4,1,2,4)` and `0^p=0`. For `0<p<1`, strict concavity makes the change strictly negative. The delta preserves rank mass and removes one child per invocation. In B3, the idle layout is unchanged, so the total histogram delta is exactly seven times this delta. The fallback term also falls, because it is proportional to the number of children. This proves the direction of improvement independently of a floating-point root. The actual bounds use rational enclosures.

## Proof scope

This remains a conditional finite-certificate improvement under the interfaces of PR373, PR365 and their ancestors. It is not an unconditional integer-multiplication theorem or a global optimum. No new Lean build is performed. The original Sussman data regenerate byte for byte during the baseline replay; that assertion applies to the original circuit, not the modified one.

In particular, the seven-stage B3 bridge has executable geometry/scalar checks but no new Lean proof here. PR370's admission of nine retained totals at bit dimension eight, its E8 route/geometry interfaces, the complex frame-transfer and helper-cleanup interfaces, and the recursion, tape compiler, balanced assembly and finite-bill proof interfaces remain inherited. Seven-stage formulas are replayed from PR373; their proof text is not newly derived by this composition. Exact scalar agreement does not by itself establish those interfaces.

## Credit

Jacob Sussman supplied the E8 complex unit and proof/checker framework. Dylan Crow (utcorvusvolat-dotcom), with Claude assistance, supplied PR370's E8 bit word. DaysSky, with Claude assistance, supplied PR363's B_K extension and PR373's seven-stage composition. Rohan's PR365, prepared with OpenAI Codex assistance, supplied the four complex retimings. PR315 and its cited predecessors supplied the exact pricing and balanced assembly engines. See the preserved notices for complete upstream credit. This composition and its source-bound verifier were prepared with substantial OpenAI Codex assistance and are offered under Apache-2.0.
