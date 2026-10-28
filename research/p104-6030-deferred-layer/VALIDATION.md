# Validation record

Scientific base: `721c03822c421b7f7fcbb2598993b947c4d88419`. Runtime: CPython 3.12.14 on Linux; standard library only. No dependency installation was needed. Repository activation and inherited authentication/remotes were preserved.

## Scientific checks actually run

```sh
python -B scripts/research_package.py --package research/p104-6030-deferred-layer
```

Result: `PASS_REGISTERED_RESEARCH_PACKAGE`, outcome completed. This executes primary and independent checkers with `-I -B`, then `-I -O -B`, each with its own 120-second timeout. The combined local run completed in under one second. The actual output is retained in [evidence/registered.txt](evidence/registered.txt).

- Primary: 11 source inputs, seven selected-source bindings, exact moment/margin/atom arithmetic, 48 symbolic-threshold fixtures, 528 whole-row padding fixtures, 12 rejected controls.
- Independent: 4,152 exact stopped-recursion models, 255 deferred schedules, three rejected parameter mutations, and an eager-reservation failure family. Normal and optimized outputs agree.
- `git diff --check` passed before packaging. Lightweight startup `make selected-record-check` and selected baseline binding checks passed; these are source/metadata checks, not scientific replays.

An initial metadata invocation rejected the nonstandard outcome string; it was changed to the allowed `completed` value before the successful run. No scientific evidence depended on that metadata error.

## Publication checks

Committed-byte, source-history, export/integrity and read-only Git-free replay receipts are added below after execution. Export is a transport/dependency check, not mathematical certification. Final commit/status details also appear in the contribution PR.

## Checks deliberately not run

No `make verify`, selected `make frontier6030-verify`, all-historical suite, Lean, Docker, native/physical replay or external Claude review. The package changes no selected construction or shared verifier. Its inherited compiler, physical, precision and analytic contracts are explicit; rerunning unrelated historical suites would not prove those missing universal implications. Hosted CI is reported separately from local evidence.
