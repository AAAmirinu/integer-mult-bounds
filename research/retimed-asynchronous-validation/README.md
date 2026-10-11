# Fresh verification receipts

Two independent fresh runs of the frozen package passed all 20 stages on
macOS arm64 and Linux aarch64, using Python 3.14.8 and NumPy. Their complete
stable `RESULT.json` bytes are identical:

`94585e3cdc8605de54323755ce6014a101bdc6b9a1cf73adbac0458805df6619`.

Both runs used source manifest
`5803b204360b144ff8e111abae713e27cae320d89cce1b6ef72410c9752bcb35`.
`SOURCE-BYTE-AUDIT.json` records 109 manifest checks and 99 source files
compared directly against their pinned Git blobs. The proof and source
package were frozen before these runs.

The platform receipts retain every step's exit status, elapsed time and log
hash; toolchain records identify both environments. The included stage logs
and detailed admission/guard artifacts are from macOS. The Linux result and
receipt are retained separately. Only the stable complete result is claimed
byte-identical across platforms; timings and diagnostic logs may differ.

The result is conditional κ = 0.001369588870945540, with complex supplier
b = 0.001371467217183061206788. Fresh checks cover both physical orientations,
all helper instances, whole-program columns and dense inputs, 19 asynchronous
controller mutations, 14 local controls, the finite invoice, two rational
moment engines and all 47 strict outer inequalities.

The unchanged #493 bit operator is a source-pinned dependency; these runs
reprice its histogram but do not rebuild it. The inherited all-size and
analytic interfaces remain conditions, as specified in the package README
and proof. These receipts do not turn the conditional result into an
unconditional theorem.

Reproduce from the repository root with a new output directory:

```sh
python3.14 -m pip install numpy
python3.14 -B research/retimed-asynchronous-whole-owners/verify.py /absolute/new/output
```

The dedicated GitHub workflow runs the same full verifier on Python 3.13
and 3.14. Its remote status is separate from these completed local runs.
