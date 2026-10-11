# Nine-stage E8 low-read composition

Conditional kappa = **0.000996761861969671** (`996761861969671/10^18`), **0.11097150583734022% above PR #381** at its pinned head. The bit side binds: `c = 997756388440101/10^18`; the complex side remains PR #377's `b = 999240641319551/10^18`.

This transplants the lower-read local schedule published in [PR #379](https://github.com/CrocSwap/integer-mult-bounds/pull/379) into [PR #381](https://github.com/CrocSwap/integer-mult-bounds/pull/381)'s nine-stage unsplit bit layout, retaining its unchanged nine-stage complex component. The new contribution is the composition, exact re-pricing, full replay harness, and the explicit strict-concavity identity below. The local schedule and nine-stage construction belong to their cited authors.

## Reproduce

Python 3.11+, a C++17 compiler, Boost headers, and `requirements.txt` dependencies are required. From the repository root:

```sh
python -m pip install -r research/e8-nine-stage-low-read/requirements.txt
python -B research/e8-nine-stage-low-read/verify.py /fresh/output/directory
```

The output directory must not exist. On macOS pass `--boost-include /opt/homebrew/include`. The included standard-header shim is used only on macOS. The workflow replays on Python 3.11 and 3.14.

The harness first reruns the complete pinned #381 verifier, including its K=2 and p10 regressions and the complete unchanged #377 complex verifier. A shell adapter only selects the current Python and supports paths with spaces. It then safely extracts the pinned #379 candidate certificate, checks its manifest, regenerates both words, verifies the commuting scalar-operator identity, and reruns independent local admission and mutation controls. The candidate receives fresh native legality, all 1,825 physical columns through nine stages, 18 omitted-bridge controls, six record mutations, exact frame nondegeneracy, unsplit geometry, width-72 bank tiling, two exact moment engines, all 47 outer inequalities, adjacent-grid rejection, and a fresh finite bill. Expected values never replace these calculations.

## Why the local profile improves

Only phase B changes. Its elementary additions have the same multiset; all destinations lie in Y and all sources lie outside Y. These transvections commute, so their abstract all-positive integer operator agrees. Every other word field is unchanged. This does not independently discharge the inherited signed-integer lifting interface.

The one-invocation paid-rank histogram change is

```
rank:     1    2   3    4   7
change: +20  -12  +6  -28 +14
```

For `f(r)=r^p`, this is exactly

```
20*(f(1)-2*f(2)+f(3)) + 28*(f(2)-2*f(3)+f(4))
+42*(f(3)-2*f(4)+f(5)) +28*(f(4)-2*f(5)+f(6))
+14*(f(5)-2*f(6)+f(7)).
```

Every bracket is strictly negative for `0<p<1`. Thus the recursive moment strictly decreases throughout that interval. Nine stages times nine replicas multiply the profile difference by 81. The verifier checks this identity against freshly reconstructed profiles. The paid call count 362,772, rank mass 1,179,792, stock 16,425, width 72, and deficit 2,808 are unchanged, so the inherited fallback cancels. Largest child 50 and halving degree two are unchanged.

## Scope

This is a conditional certificate improvement under the pinned suppliers' interfaces. It retains #381's nine-stage bit bridge, signed lifting, finite-bill and degree-two induction interpretation, and #377's exact Clifford/compiler, compressed-window, arbitrary-dirty-bank, tape, common-grid, row, and all-size analytic interfaces. The F2 all-column check is not by itself an integer-circuit proof. No new Lean proof or unconditional integer-multiplication exponent is claimed. Original proofs, notices, manifests, producers, and checkers are retained unchanged under `source381/` and the pinned candidate archive; `SOURCES.json` binds both heads.

The three joint-dual source-pin files outside this package reuse PR #318's repair solely to keep the repository's existing checks bound to their intended source. They do not alter this result.
