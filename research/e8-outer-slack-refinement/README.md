# Six-level ordinary bootstrap and exact outer witness

Conditional **kappa = 0.000998634658090835** (`199726931618167/200000000000000000`). This is above #384's 0.000998634656132003 and the previous three-level version of this PR, 0.000998634657132636. It is a small finite-bootstrap/witness improvement. The local circuits, paid profiles and bit coarse saving are unchanged. Retaining 24 certified decimal places in the complex coarse saving adds exactly 10^-18 to the preceding six-level witness. This last step removes a rounding loss; it is not a new circuit improvement.

## Reproduce

Python 3.11+ and its standard library are sufficient:

```sh
python -B research/e8-outer-slack-refinement/verify.py /fresh/output/directory
```

The output directory must not exist. The verifier first runs the complete pinned #384 verifier, including both moment engines, exact operator equality, baseline assembly and full regeneration of the retimed certificate. Its shell adapter only selects the active Python and preserves paths with spaces. It then certifies the complex coarse root between consecutive 10^-24 grid points with both independent rational moment engines, retaining the full 10^-16 bad-branch allowance, and reconstructs six fixed bootstrap levels, checks their closed forms and positive finite-cutoff gaps, verifies all 47 strict rational assembly constraints, and rejects six invalid witnesses/cutoffs. The next 10^-18 grid point exceeds `b/(1+b)`, the ceiling of the unchanged outer formula at this fixed complex saving. Original source integrity is checked before and after.

## The improvement

The bit input remains `c = 251726760077483/250000000000000000`. The same paid complex profile certifies `b = 999632926176283805553/10^24`, with the exact moment root strictly between b and b+10^-24. The old truncated input was `999632926176283/10^18`. Keep beta=eta=10^-18 and `s=(1-beta)*b-10^-24`. Starting with completed ordinary saving `a0=384599/10^10`, construct exactly six acyclic levels:

`a[j+1]=(1-s)*s+s*a[j] = s-s^(j+1)*(s-a0)`.

Each ordinary call in level j uses only the completed preceding level. Coarse recursive children still shrink their input width. Six is fixed independently of input size; no infinite-depth algorithm or growing stack is used. Every stage has positive atom, borrowing, remainder and stock gaps. Its lower-order tolls can therefore be absorbed above a finite cutoff, with the previously completed algorithm used below it.

This extends the fixed-depth argument from our reviewed #185 work, pinned under `bootstrap-sources/`. The earlier review covered three levels; the six-level extension and its conditional composition argument are supplied in `PROOF.md` here. For each stage the code checks the exact cutoff inequalities at representative constant bit bounds. The proof gives the formula for any fixed dominating stage constant; these examples do not claim to measure the inherited algorithm's actual constants.

The six-level witness reaches the largest 10^-18 grid point below `b/(1+b)`. In the retained outer formula, `a<b` and positive eta force the compact margin below this ceiling. Thus another bootstrap depth or slack choice in that same formula and at the same b cannot reach the next grid point. The verifier also proves `(b+10^-24)/(1+b+10^-24) < kappa+10^-18`, so additional coarse-root precision cannot reach the next final grid point either. This says nothing about a different paid profile or outer assembly. Five levels at the selected slacks are explicitly checked to fall short of the chosen grid point.

`THREE-ROUND-WITNESS.json` preserves and independently replays the prior chain at its original coarse input. `SIX-ROUND-18-DIGIT-COARSE-WITNESS.json` preserves the preceding six-level result. The new chain uses the stronger certified coarse input. `EXPECTED-COARSE-PRECISION.json` records both engines' signed interval residuals. `PARAMETERS.json` freezes the selected finite depth and slacks. `EXPECTED-WITNESS.json` is compared to fresh calculations, never used as their substitute.

## Conditional scope

All #384 supplier assumptions and unresolved obligations remain, including #382's kernel entrance-completion, bit-geometry and finite-bill obligations and #377's compressed-window, arbitrary-dirty-bank, Clifford/compiler, common-grid, row and analytic interfaces. The ordinary bootstrap additionally states the same inherited completed-leaf contract explicitly: arbitrary widths, complete spectators, restored internally borrowed rows and a fixed finite tape set. Each new fixed level must satisfy that conditional interface. There is no new proof of those base interfaces, measured machine constant, practical speedup, Lean build or unconditional multiplication exponent.

This package runs exactly the circuit checks #384 supplies; it does not discharge that PR's unrerun certificate-specific splice/Clifford/invoice obligations. The reviewed bootstrap sources explain why internal borrowing at completed endpoints does not require a new external row multiplier. The retained external 252 allocation is slack, not a claim about the six-level algorithm's internal workspace.

`source384/` is unchanged from fd81a16a1e4e82acfb4d45752cba17450644fde6. Its licenses, notices and manifest remain intact. Bootstrap proof sources are byte-bound to main commit 12a4934d15006e8c10f9b2264f13f8f341be802b. The three joint-dual metadata files outside this package reuse #318's source-pin repair without a mathematical change.
