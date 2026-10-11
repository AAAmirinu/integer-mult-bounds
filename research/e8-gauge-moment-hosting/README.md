# Moment-directed hosting of the E8 gauge/kernel word

The same complex local word as [PR #484](https://github.com/CrocSwap/integer-mult-bounds/pull/484), with a different whole-residual packing, supports conditional

**κ = 0.001325117552367841**, using the freshly replayed R489 bit supplier from [PR #493](https://github.com/CrocSwap/integer-mult-bounds/pull/493).

The complex saving is **b = 0.001326875818805153**, compared with #484's 0.001326789535340266. The complex supplier binds. Both suppliers retain their declared all-size and mutable-basis interfaces; this is not an unconditional multiplication theorem.

The packing moves every entering helper onto a data family. Its 66 remaining banks contain only width-nine helpers. Live stock stays 7,746, physical stock stays 8,324, and the largest paid complex child decreases from rank nine to rank eight. The local scalar word, phase recipes, residual wrappers, host ownership rule, and global schedule are unchanged. See [PROOF.md](PROOF.md).

Run the complete fresh composition:

```sh
python -m pip install numpy sympy
BOOST_INCLUDE=/path/to/boost/include \
  python -B research/e8-gauge-moment-hosting/verify.py /absolute/new/output
```

Use Python **3.13 or 3.14**, a C++17 compiler, and actual Boost multiprecision headers. The unchanged #484 package compares compressed byte hashes generated with the normalized gzip OS header of Python 3.13+. Its supplied final receipt fails on Python 3.12 despite passing the operator and numerical checks; this wrapper does not replace that receipt or alter the vendored package. Python 3.15 changes the default compression level and is outside the supported receipt format. These version changes are documented in the [Python gzip reference](https://docs.python.org/3/library/gzip.html#gzip.compress).

The verifier rebuilds #484 in `--all` mode, including the anchor, three variants, exact Gaussian operator checks, and necessity controls. It then runs #493's full bit verifier, emits the new hosting from a frozen selection, runs #484's unchanged independent hosting audit, independently recounts the packing and rejects five selection mutations, and runs both rational moment engines, the finite invoices, and all 47 strict outer inequalities. `RESULT.json` is deterministic; its bit-template fingerprint excludes only the inherited geometry generation timer. `RECEIPT.json` retains the original bit-template and geometry hashes, timings, and parent receipt hashes.

The six complete inherited packages are pinned in [SOURCE.json](SOURCE.json), including Git blob identities. The source packages are unchanged. No optimizer runs during verification. Optional discovery, requiring SciPy:

```sh
python -B research/e8-gauge-moment-hosting/code/discover.py \
  /absolute/verified-parent484/gauge80-kernel42 /absolute/new/search
```

The frozen feasible packing is the witness. No claim of global optimality depends on the floating-point search or its solver status.
