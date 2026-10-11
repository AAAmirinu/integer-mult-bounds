# Exact outer-assembly slack refinement

Conditional **kappa = 0.000998634657132636** (`249658664283159/250000000000000000`), versus #384's 0.000998634656132003. The absolute gain is **0.000000000000999633**, about **0.0000001002001076024877%**. This is a tiny witness-parameter improvement, with unchanged circuits and unchanged coarse savings.

## Reproduce

Python 3.11+ and its standard library are sufficient:

```sh
python -B research/e8-outer-slack-refinement/verify.py /fresh/output/directory
```

The output directory must not exist. The verifier first runs the complete pinned #384 verifier, including exact operator equality, both moment engines, all baseline inequalities, and full regeneration of its retimed certificate. Its only shell adaptations select the active Python and preserve paths with spaces. It then computes the new witness using the unchanged, pinned `outer.assembly`, checks all 47 strict rational slacks, rejects four invalid witnesses, and proves the next 10^-18 grid point exceeds the entire retained three-round family's supremum. Original source integrity is checked before and after.

## What changes

The existing construction has bit coarse saving `251726760077483/250000000000000000` and complex coarse saving `999632926176283/10^18`. The latter limits the allowed bootstrap saving. Instead of #384's beta=10^-9, eta=10^-12 and coarse-grid backoff, use beta=eta=10^-18 and choose `s=(1-beta)*b-10^-24`. All inequalities remain strictly positive. Keep the same three bootstrap rounds and the same finite envelope. `EXPECTED-WITNESS.json` records the full exact chain and every slack; it is compared against a fresh calculation, never used as the calculation's input.

The only improvement is in the final witness. This does not improve the local word, recursive moment, stock, finite invoice, bit or complex coarse saving. The stronger numerical witness retains #384's conditional scope.

## Proof scope

All supplier assumptions and unresolved obligations of #384 remain, including #382's kernel entrance-completion/bit-geometry/finite-bill obligations and #377's compressed-window, arbitrary-dirty-bank, exact Clifford/compiler, common-grid, row and analytic interfaces. This package runs exactly the checks #384 supplies. It does not newly discharge its certificate-specific splice/Clifford/invoice obligations, and does not claim an unconditional multiplication exponent or new Lean proof.

The grid-optimality statement is only for the retained three-round assembly family and fixed coarse inputs; it is not a global bound on other bootstrap depths, circuits or assembly constructions. See `PROOF.md`.

The source384 directory is unchanged from commit fd81a16a1e4e82acfb4d45752cba17450644fde6. Its original licenses, notices, checkers, search, proof and manifest are preserved. The three joint-dual metadata files outside this package reuse #318's source-pin repair without any mathematical change.
