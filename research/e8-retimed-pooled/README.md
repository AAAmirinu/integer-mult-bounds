# Retimed gauge word with pooled whole-helper owners

The main-word frame schedule from [PR #495](https://github.com/CrocSwap/integer-mult-bounds/pull/495), applied to the gauge80-kernel42 selection from [PR #484](https://github.com/CrocSwap/integer-mult-bounds/pull/484), composes with [PR #496](https://github.com/CrocSwap/integer-mult-bounds/pull/496)'s whole-owner pooling. The conditional certificate is

**κ = 0.001343518018117309**, with complex saving **b = 0.001345325487149526878087** and the freshly rebuilt [PR #493](https://github.com/CrocSwap/integer-mult-bounds/pull/493) bit supplier. The complex side binds. This retains the inherited all-size compiler, mutable-basis, common-label, restored-row, precision/tape, analytic-transfer and Lemma A spectator-realization contracts; it is not an unconditional multiplication theorem.

The transfer changes 224 A-event frames and 504 B-event frames. Scalar operations, helper entrances, target levels and centre chains are preserved. All 40,320 whole helper roles fit on 7,680 existing data families; physical stock is 8,258 and the largest paid child has rank eight. No helper invocation is split across physical families. See [PROOF.md](PROOF.md).

Run in Python **3.13 or 3.14**, with NumPy, SymPy, a C++17 compiler and actual Boost multiprecision headers:

```sh
python -m pip install numpy sympy
python -B research/e8-retimed-pooled/verify.py /absolute/new/output \
  --boost-include /path/to/boost/include
```

Verification first runs the complete unchanged #496 package, including its #484 and #493 supplier rebuilds, real arbitrary-precision Boost probe, original pooling admission and controls. It then reconstructs the changed word, reruns scalar and selection controls, serializes both orientations and all used exact phase recipes, checks residual wrappers, independently replays common labels and all instance identities on 512 basis columns, and checks the complete program on 806 basis and eight dense inputs in both orientations. Every fixed-width arithmetic operation in the latter operator checks has a preceding Python-integer overflow bound. These whole-program inputs are not an exhaustive basis of the entire register space.

The retimed word changes the frame catalogue. The original M8 mutation constructor assumes that its first centre has a particular outside extension, which no longer exists. Our attributed copy chooses the first available centre descent with an outside one-dimensional extension, retaining the same G3 violation and physical check; all 14 controls must still reject. The unchanged parent checker remains vendored and is exercised on the unchanged parent word.

The final checks independently recount every owner, spectator, remainder and invoice; test the serial reuse model; reject 18 controller mutations; and run both exact moment engines and all 47 strict outer inequalities. `RESULT.json` is deterministic; `RECEIPT.json` records platform-specific timings and raw artifact hashes. Source hashes and upstream commits are in [SOURCE.json](SOURCE.json). No optimizer or network access is used during verification.
