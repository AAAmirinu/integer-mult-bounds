# Faster complete PR358 replay

This package shares freshly computed producer prefixes, accelerates exact
predecessor arithmetic and scalar admission, and overlaps independent native
work with the same two active stage workers. It runs every original check.
No saved proof result replaces execution. The adapters are external and refuse
source/AST drift; the original 839 upstream blobs remain unchanged.

The construction is PR358 at
`e76d7a94e6ad819e2aa9dc99083ecfa3e7842e0b`, package
`research/w3-353354-471-signed18-native`. Its conditional finite certificate stays
at κ = `80367971186626189473809/100000000000000000000000000`, with final word
SHA256 `98007fb3a634ca671bcfea6bed8c1b33da190606ffbea748cd931399ecf65d2d`.
The inherited all-size interfaces remain assumptions. This is execution
infrastructure, with no new κ or unconditional multiplication theorem.

## What is measured

The historical same-schedule scalar A/B took **168.54 → 164.11 seconds** for
the full pipeline (**2.63% less**) and **25.04 → 16.11 seconds** for scalar
admission (**35.68% less**). Total process-tree CPU time fell **2.39%**. Both
variants already included the other optimizations in this package. Scalar-child
peak RSS increased from 693.3 to 800.1 MiB on macOS. These are one sequential
CPython3.13.12 pair with OS caches unflushed, not a median, memory improvement
or community discovery-throughput measurement. Compact historical evidence is
in `evidence/historical-scalar-ab.json`.

The separate fresh relocated-package comparison in `evidence/packaged-ab.json`
compares `original` with all optimizations (`scalar`). It is not a measurement
of scalar admission alone. The `original` baseline uses the same two-worker
proof driver; it is not the upstream serial wrapper. Percentages from different
experiments must not be multiplied. `evidence/packaged-tests.txt` records the
focused tests run against this package. No latest-frontier pipeline was timed.

## Reproduce

Python3.11+, POSIX `fork`/`wait4`, little-endian execution, a C++17 compiler and
Boost headers are required. Use a virtual environment and install the pinned
upstream `requirements.txt` (numpy, scipy, sympy). This is a POSIX prototype;
one BLAS/OMP thread and Python hash seed0 are fixed by the launcher.

```sh
P=research/e8-replay-performance
python -m pip install -r "$P/requirements.txt"
# Explicit network acquisition: 839 blobs / 36,086,336 bytes, all Git-blob checked.
python -B "$P/fetch.py"
# Offline alternative: python -B "$P/fetch.py" --from /path/to/exact/pr358/package
python -B "$P/check.py"
python -B "$P/replay.py" --variant original --output /tmp/e8-original-new --cxx c++ --boost-include /usr/include
python -B "$P/replay.py" --variant scalar --output /tmp/e8-fast-new --cxx c++ --boost-include /usr/include
python -B "$P/compare.py" /tmp/e8-original-new /tmp/e8-fast-new --output /tmp/e8-comparison-new.json
```

Run heavy variants sequentially on the same host. Outputs must be new and
outside the frozen source; inside this package use the ignored `build/`
directory. `fetch.py` alone uses the network. Replay, comparison and tests are
offline. Acquisition is excluded from the timed replay. The shared pinned
source is copied/downloaded into the ignored `e8-pipeline-profile/pr358-source/`.

Intermediate variants are `shared`, `predecessor`, `scheduled`, `admission` and
`combined`. To isolate scalar admission, compare `scalar-baseline` with `scalar`.
The copied folder names preserve the original, tested adapter dependency paths
within this one package; no sibling workspace experiments are needed.

## Execution changes

1. **Fresh prefix sharing.** Prepare/physical/parity run once. Six original
   producer/search consumers execute in isolated fork children. Deeper transform
   results are reused only after their actual selections are freshly regenerated.
   Complete byte-equal copied package inputs and parent fingerprints bind the
   admission-to-producer handoff. A private pipe transports a fresh child result;
   no external pickle is read. Child mutation and failure controls are tested.
2. **Predecessor proof.** Exact common-denominator sparse arithmetic replaces
   per-entry Fractions in gx.scal and bank-factor replay. Only gx.scal changes;
   all other gx code and gxcore remain unchanged. Bounded predicates key current
   row contents. Transcript caches store encoding bytes, never validation PASS.
3. **Scheduling.** After the reference proof, its worker verifies the immutable
   reserve and compiles five native checkers while the source proof continues.
   Bank and chart checks run together in disjoint directories after their inputs
   are ready. All original command arguments, logical stage order and final
   receipt bindings remain checked. No third stage worker is introduced.
4. **Generator.** Two fixed-prime modular inverses use extended Euclid via
   `pow(x,-1,P)` instead of Fermat exponentiation. The complete generator still
   runs and its output is compared exactly.
5. **Scalar admission.** Signed unit addition avoids giant integer multiplication;
   pure orthogonality predicates key complete current rows; integer triples use
   identical compact JSON bytes; identical compiled code is reused across fresh
   control namespaces. Every event and all fifteen replays still execute.

### Exact radix change

Fresh majorant computation gives residual bound B=23,954. The clean checker
selects the smallest byte width satisfying `2**bits > 2*B`:16 instead of24.
For q=`2**bits`, residual coefficients satisfy |d_i|≤B. If k is the largest
nonzero coefficient index, |d_k q^k|≥q^k while all lower terms together have
magnitude at most B(q^k−1)/(q−1)<q^k. Cancellation is impossible. Hence a zero
packed integer certifies every coefficient is zero, using unbounded exact
integers. B=0 is immediate.

This changes only proof encoding, not physical payload widths or the invoice.
Both clean signed directions use16 bits; **all eleven corruption controls keep
the original24 bits**, including the flipped-sign integer control. Receipt
`majorant.packing_bits` intentionally changes24→16, including its embedded copy
in ADMISSION.json. All other mathematical fields are compared exactly.

### Provenance and checks

`ORIGINAL-CODE.json` pins the35 copied original adapter/reference/input/notice
files. They remain byte-identical to the locally tested prototypes; the new
portable launcher, acquisition, comparison, package tests and documentation are
separate. `MANIFEST.json` pins implementation/documentation inputs, excluding
the separately pinned source cache, build outputs and publication evidence.
Fresh `PACKAGE-RUN.json` records that manifest, runtime, variant and process-tree
CPU/wall times. Preserve the prefix, predecessor, scalar and native performance
sidecars with all optimized receipts: original source hashes alone do not
describe an externally optimized execution.

The comparator checks49 binary/state/frame/selection/native artifacts, complete
producer outputs (gzip payloads decompressed), predecessor and source-admission
receipts, prices, certificates and refinement. Any run-specific receipt hash
excluded from equality is first validated against the actual fresh file. Stage
intervals confirm two overlapping jobs at most. Original corruption, stage
omission, geometry, prime and supplier controls remain part of the full replay.

The pstats aggregation fix in `profile_scalar.py` avoids losing costs when
distinct compiled code objects share filename/function/line keys. It sums
`Profiler.getstats()` entries before saving diagnostic statistics. Instrumented
times are not uninstrumented benchmark baselines.

Later frontier packages have different E8 bit/scalar/global-template interfaces.
They need new profiles, source pins and manifests before these timings or
adapters can be applied to them. This package is independent of PR367's exact
frame-algebra performance package and does not require that branch.

See `NOTICE.txt` and retained component notices for attribution.
