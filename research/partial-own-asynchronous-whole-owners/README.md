# Partial-own factory with asynchronous whole owners

This combines #507's partial-own factory and 84 kernel pivots with #473's
nonuniform order of 72 complete invocations and a new literal owner allocation.
The conditional result is **κ = 0.001388049083313897**, with complex supplier
**b = 0.001389978441615608493590**. The unchanged #493 bit supplier is nonbinding.

Shrinking the 42 changed helpers inside the old assignment does not suffice:
it leaves too many small remainders and loses the scheduling gain. This package
reallocates all 40,320 whole helpers against the changed width inventory. The
actual emitted controller checks every physical owner, event window, chart and
remainder. No residual is split across physical families.

```sh
python3.14 -m pip install numpy sympy
python3.14 -B research/partial-own-asynchronous-whole-owners/verify.py \
  /absolute/new/output --boost-include /path/to/boost/headers
```

Python 3.14, NumPy, SymPy, a C++17 compiler, Bash and genuine Boost headers are
required. The offline verifier reconstructs both pinned suppliers, the changed
factory, scalar/frame/physical checks and the new asynchronous composition.
It accepts no cached supplier output and runs no optimizer. The freshly rebuilt
bit profile, invoice and emitted-program hash bind the exact assembly.

The vendored #507 constructor has one documented portability edit: two
historical discovery-only floating display fields use their published values.
On Linux those fields differed in the last bits, while every other generated
word field agreed with macOS. The original source is retained; the frozen
source-word and candidate-word hash assertions are unchanged. See
`references/UPSTREAM-PORTABILITY.json`. The original upstream Linux verifier
failed at that hash check; an unchanged upstream full pass is not claimed.

`PROOF.md` describes composition and placement. `SOURCE.json` records copied
Git bytes, and the complete `MANIFEST.json` binds the derivative. `discovery/`
contains the nomination procedure and solver records; floating optimization
is not part of certificate acceptance or an optimality proof.

The inherited all-size compiler, mutable-basis/common-label transport, #484
Lemma A realization with borrowed spectators, restored-row, precision/tape and
analytic-transfer conditions remain. This is a conditional exponent witness,
not an unconditional multiplication theorem, a Lean proof or a measured speedup.
The disputed #448/#494 cross-family split interface is not used.

Prepared by chafreaky with OpenAI Codex. Credits and retained notices are in
`NOTICE.md` and the vendor directories.
