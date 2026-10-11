# Combined E8 witness

This package checks the conditional bound

\[
\kappa=1307044366925301/10^{18}=0.001307044366925301.
\]

It is 80.637878% above the selected value on main at
`12a4934d15006e8c10f9b2264f13f8f341be802b`. This compares exponent
savings. It does not measure runtime. The complex supplier limits the bound.

The package combines an R705 bit word with a retimed R560 complex word.
It contains the fixed positive words, owner choices, finite schedule, and
the source code needed to check them. It regenerates records, geometry,
phases, templates, costs, and all 47 strict outer inequalities. It does
not contain searches or the nested historical source packages.

Use Python 3.11 or later. The replay was checked with Python 3.14 and
SymPy 1.14.0. Install the one external dependency, then run:

```sh
python3 -m pip install -r research/e8-combined/requirements.txt
python3 -B research/e8-combined/verify.py --output "$(mktemp -d)"
```

The command uses an empty output directory outside the source package. It checks the committed
`certificate.json` against a fresh construction. The output includes
the complete inequalities and component audit records. No network access,
C++ compiler, old checkout, or saved build directory is needed.

Read [PROOF.txt](PROOF.txt) for the dependency argument and assumptions.
The finite checks do not prove all-size compilation, complete-cover
execution, bad-class portability, or the analytic multiplication theorem.
The pending E8 mutable-target, idle-hosting, and Gaussian-adapter interfaces
extend the conditions stated on main. This package does not select a new
main result. Source attribution and AI assistance are in [NOTICE](NOTICE).
