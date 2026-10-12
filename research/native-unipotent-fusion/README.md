# Native unipotent shared-query fusion

This standalone research packet replaces one specified pair of reflected
ADDRESS queries by one unipotent ADDRESS query on native BIT arrays. The
exact local implementation uses one recursive child instead of two. Both
implementations use four XOR scans after their shared chart is cancelled.

Run from any directory with Python 3.8 or later:

```sh
python3 /path/to/native-unipotent-fusion/check.py
```

The checker uses only Python's standard library and files in this folder.
It checks the exact rational matrices, literal ordered programs and
inverses, the specified comparison, all 344 dirty BIT basis columns on
orbits in the true rings Z/5, Z/25, Z/7 and Z/49, 86 extra VALUE spectator
columns, ADDRESS spectators, fixed points and recovery negative controls.
It verifies the recorded results and SHA-256 manifest without rewriting
any file. `--write-results` regenerates results for development and does
not verify the manifest.

`PROGRAM.json` contains every literal program used. `PROOF.md` establishes
the identities for arbitrary arrays and every permitted chunk width;
finite orbit tests illustrate rather than replace that proof.
`SOURCE-PINS.json` records public contract attribution and prior exact
verification provenance. Those prior checks are not runtime dependencies.

This is an independently verified local primitive, with a paid private
row and the original child/ordered-affine contracts as premises. It does
not provide a complete three-DATA cyclic interchange supplier, a complex
interchange supplier, an all-size row scheduler or a new exponent kappa.
See the full scope and invoice in the proof.
