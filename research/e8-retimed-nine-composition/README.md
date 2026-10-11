# Retimed nine-stage complex with the kernel bit supplier

Conditional **kappa = 0.000998390813251625** (`7987126506013/8000000000000000`), **0.014791889125625176% above PR #382**. The complex component binds: `b = 999388595603943/10^18`, while the unchanged #382 bit component supplies `c = 251726760077483/250000000000000000`.

The composition places Ali Romman's [PR #365](https://github.com/CrocSwap/integer-mult-bounds/pull/365) retimed complex unit in Zhihao Chen's [PR #377](https://github.com/CrocSwap/integer-mult-bounds/pull/377) nine-stage layout and pairs it with Chafik Boukhalfa's [PR #382](https://github.com/CrocSwap/integer-mult-bounds/pull/382) kernel bit word. This contributes the source-bound composition and fresh global replay; the local retiming, bit kernel, and nine-stage construction remain their authors' work.

## Reproduce

Python 3.11+, a C++17 compiler, Boost, and the dependencies in `requirements.txt` are needed:

```sh
python -m pip install -r research/e8-retimed-nine-composition/requirements.txt
python -B research/e8-retimed-nine-composition/verify.py /fresh/output/directory
```

The output must not exist. On macOS use `--boost-include /opt/homebrew/include`. GitHub CI runs Python 3.11 and 3.14. All generated files stay outside the package.

The verifier runs the full unchanged #382 baseline including its five-stage regression, both producer stages, integer source-span rule, local and global F2 columns, mutation controls, exact Gram checks, width-56 banks, degree-two guard, two exact moment engines, and outer assembly. It also runs all eight stages of the unchanged #377 complex verifier and the complete #365 reconstruction and rational scalar-map comparison.

It then derives a separate working copy of #377, changing only the certificate, certificate/census pins, the expected local child count (3974 to 3973), and expected rational price. `DERIVATION.json` records every old and new file hash. The original source packages stay byte-identical and are checked again at completion. Candidate input and count pins are frozen before execution; no validation is disabled.

Fresh candidate checks cover the complete local dirty scalar words and erased scratch, exact Clifford representatives for 948 frames and 3,122 directed transitions, data routes and Gaussian phases, nine-stage owner injections, 56,376 residual assignments, the complete emitted template, all 14,727 terminal cover corrections, global mutation controls, the finite invoice, two rational moment engines, all 47 outer inequalities, and adjacent-grid rejection.

## Change in the profile

The local retiming removes one paid call and preserves rank mass. Nine stages times eight replicas remove 72 calls. The global rank-count difference is `{1:+144, 2:-432, 3:+288, 4:+72, 5:-432, 6:+288}`. The freshly emitted profile has 310,383 calls, rank mass 1,072,575 and deficit 2,496, with `m=73`, live stock 14,727, physical stock 15,520, and maximum child 48. Halving degree two, row coefficient 15,445 below the retained 20,161, and the 49B induction gap remain unchanged.

## Conditional scope and open obligations

This retains every #382 bit admission and open obligation. In particular, its E8 kernel entrance completion remains inherited from its earlier lineage; its seven-block PR234-style port geometry and full finite bill at m=56 are not independently discharged here. We rerun its existing checks and its stated generalized degree-two guard. Its global F2 columns alone do not prove the complete integer circuit.

The complex side retains #377's compressed-window lift, arbitrary-dirty-bank composition, exact Clifford/compiler, all-cover symbolic route argument, tape/common-grid/row, and all-size analytic interfaces. Its dimension m=73 and degree-two induction interpretation remain explicit assumptions. This PR freshly checks the changed component's full finite template and invoice but does not supply a new Lean proof or an unconditional multiplication exponent.

`SOURCES.json` pins all three supplier commits. Licenses, notices, original manifests, proof documents, and checkers are retained. Outside this package, the three joint-dual source-pin metadata files reuse #318's repair without a mathematical change.
