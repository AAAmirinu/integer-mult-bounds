# Lean 4.21 reproduction

**Full port validation is pending.** These are the intended normal build
commands. A successful receipt from the complete fresh run is still required.

Start from a clean checkout of the port commit being reviewed. Record
`git rev-parse HEAD`. Install Git, Python 3.13 and elan using upstream's normal
setup. Each project selects its compiler through `lean-toolchain`; no external
resource settings, special compiler flags or environment overrides are used.

From the repository root:

```sh
python3 -m pip install -r research/lean-external-review/requirements.txt
cd research/lean-multi-host-source
lake exe cache get Mathlib.Data.Matrix.Mul \
  Mathlib.Algebra.BigOperators.Fin Mathlib.Tactic.FieldSimp \
  Mathlib.Tactic.Ring Mathlib.Tactic.NormNum
cd ../..
make formal-pr442-verify
```

The Make target defaults to `LAKE=lake`. A local installation can select its
Lake executable with `make formal-pr442-verify LAKE=/path/to/lake`; this is
executable selection only, not a compiler flag or environment override.

These are the commands used by the added `pr442` entry in upstream's existing
formal CI matrix. That job retains its 45-minute limit. The package must first
qualify against the more conservative approximately 30-minute projection,
including a slower four-core runner and a safety margin; this has not yet
been established by a full fresh build.

The cache request selects the five imported Mathlib modules and their full
dependency closure; it does not download unrelated Mathlib modules. These are
cache selections, not compiler flags. The ordinary build remains `lake build`.
The official Mathlib cache contains only pinned external dependency artifacts.
It must not supply local contribution artifacts. If the cache is unavailable,
ordinary Lake can compile the dependencies from source; the additional time
must be reported separately and included in any cache-free CI projection.
The current managed environment blocks the official cache endpoint, so local
validation may reuse fingerprinted external dependencies built from source.
That does not establish cold-cache CI runtime.

For a complete local receipt set in a new directory outside the checkout:

```sh
python3 research/lean-external-review/reproduce.py \
  --receipt-dir /tmp/pr442-review-receipts
```

This requires `research/lean-multi-host-source/.lake/build` to be absent or
empty. Use a new clean checkout if local project artifacts already exist.
Pinned external artifacts in `.lake/packages` may be reused and are
fingerprinted. `--lake` optionally selects the Lake executable; it does not
change compilation or resource settings. No resume mode is offered.

The reproduction runs inventory validation, all literal source checks, the
flat-data parser mutation checks, a fresh Lake build and the five separate
axiom inventories. The Task B inventory has 931 declarations and Task A has
21. The nine historical third-party source snapshots are excluded from
compilation and axiom auditing, while their unchanged bytes remain hashed.
The differential test is delegated separately and is not reported here.

The current canonical completed-build location is
`validation/lean421-fresh.json`. Until that file exists with a matching PASS,
the strict package verifier fails. During preparation only,
`verify_package.py --allow-pending-port` checks the pending inventory and
reports `PENDING_PORT`, never PASS. A reviewer may validate a new local run
using `verify_package.py --build-receipt /tmp/pr442-review-receipts/lean421-fresh.json`.

Historical `replay.py` scripts and Lean 4.33 receipts explain earlier work;
they are not the supported current reproduction route.
