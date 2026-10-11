# Seven-stage E8 bit supplier with the nine-stage complex component

The checked composition gives the conditional integer-multiplication saving

**κ = 483630501585197 / 500000000000000000 = 0.000967261003170394.**

This is **1.32149% above PR378**'s published `0.00095464544449649` at commit `c248962c3cf641d4f6226d63d86843f2c096a7d0`. PR378 is a comparison point, not a construction dependency.

PR377 supplies a stronger complex component but evaluates its final bound with the frozen PR361 bit supplier. This package pairs that component with the already checked seven-stage E8 bit supplier from PR373/375. The bit word and both constructions are unchanged. The new contribution is the source-bound compatibility check, exact combined assembly and full replay of both suppliers.

| Quantity | Value |
|---|---:|
| Seven-stage bit coarse saving c | 968197503705007 / 10^18 |
| Nine-stage complex coarse saving b | 999240641319551 / 10^18 |
| Final κ | 967261003170394 / 10^18 |
| Binding side | bit |
| Bit dimension / replicas / normalized live stock | 56 / 7 / 11095 |
| Complex dimension / replicas / live stock | 73 / 8 / 14727 |
| Complex physical streams / halving degree | 15520 / 2 |
| Complex physical row coefficient | 15445 < 20161 |

This is an actual combined conditional certificate, not the hypothetical higher bit saving used in PR377's title projection. The resulting κ remains below `2^-10`.

## Replay

Requires Python 3.11 or later, NumPy, SymPy, mpmath, Bash, `sha256sum`, a C++17 compiler and Boost headers:

```sh
python -m pip install -r research/e8-seven-bit-nine-complex/requirements.txt
python -B research/e8-seven-bit-nine-complex/verify.py /path/to/fresh/output
```

Use a fresh directory outside the package. Temporary files stay under that directory. On macOS with Homebrew Boost, add `--boost-include /opt/homebrew/include`. Allow several minutes and at least 200 MB of output space.

The verifier runs all of PR375's original checks, including producer reconstruction, all 1,585 seven-stage formal columns, negative controls, five-stage regressions, geometry, banks and finite bills. It also reproduces the prior complex-bound result. Every scientific check in the original Bash replay is retained; a transport adapter handles spaces in paths and the selected Python interpreter.

It then runs all eight stages of PR377's original component verifier: frozen-source integrity; local dirty admission; finite routes, banks and profile; 946 exact Clifford frames and 3,120 transitions; endpoint and cover phase corrections; the global template and complete invoice; independent template audit and two rational moment engines; and PR377's fixed-bit regression. Neither vendor tree is edited.

Both source packages use byte-identical `outer.py`. The newly reconstructed nine-stage invoice fits the same retained envelope: G = 2^30000, E = 2^100000, C0 = 2^210000 and row coefficient 20161. The actual complex coefficient is 15445, router bit length 7984, literal-charge bit length 35284 and required-C0 bit length 200012. Its completed-child induction gap is 49B. The verifier checks these constraints before composing the suppliers.

With eta = 10^-12 and beta = 10^-9, the bit coarse saving lies strictly below the complex leaf cap. Three inherited bootstrap steps start at `384599/10^10`. The exact outer assembly admits all 47 strict constraints and rejects the adjacent 10^-18 κ grid point. Both moment engines and adjacent-tick exclusions run for both suppliers. The final bit finite bill must equal the baseline bill. Full rational constraints are emitted in `assembly.json`; `RESULT.json` appears only after every check passes.

## Scope

The theorem remains conditional on the pinned supplier interfaces. This composition does not prove a new bit circuit, a new complex circuit, a new tape compiler or a new Lean multiplication theorem. It does not claim global optimality.

The nine-stage component retains the local E8 theorem, Clifford/rank-zero compiler, compressed-window and arbitrary correlated-bank composition, complete-stream tape primitives, common-grid precision, row and analytic recurrence interfaces. Exact phase, owner, bank and finite-invoice checks do not by themselves discharge those all-size theorem obligations. Its source proof is preserved in `source377/work/complex-nine-native/PROOF.txt`.

The bit side retains PR373/375's B3, nine retained totals at local dimension eight, E8 bank/geometry, recursion and seven-stage finite-bill interfaces. No new Lean proof of B3 or astronomical cover enumeration is supplied. Different bit and complex dimensions are already permitted by the inherited two-supplier assembly; compatibility here means the explicit checked shared envelope and 47 inequalities under those interfaces.

## Credit

Zhihao Chen, with substantial OpenAI Codex assistance, supplied PR377's nine-stage complex construction and checks. Jacob Sussman supplied the E8 complex unit, checkers and proof framework. Dylan Crow / utcorvusvolat-dotcom, with Claude assistance, supplied PR370's E8 bit word. DaysSky, with Claude assistance, supplied the B_K extension and PR373/375 constructions. The pricing and balanced-assembly authors are credited in the preserved source notices.

This composition and verifier were prepared by Rohan with substantial OpenAI Codex assistance. New work is Apache-2.0; all upstream notices and licenses are preserved. `SOURCES.json` pins the exact commits, and `MANIFEST.json` covers every shipped file.
