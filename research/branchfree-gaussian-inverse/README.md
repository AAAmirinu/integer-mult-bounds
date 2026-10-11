# Branch-free Gaussian interior inverse

The retained phase-cell solver uses a difference of two convolution pairs.
This package replaces its online interior operation with two triangular
convolutions and three diagonal factors inside the existing similarity.
The identity is classical q-calculus; the contribution here is an explicit
perturbation transfer to the independently rounded, truncated source,
rounded arithmetic, and composition with the unchanged Schur system.

The global H and exact Schur setup remain unchanged. The conditional proof
preserves the scalar precision, disk and normalization interface. It also
bounds both weighted triangular factors by 3p, identifying a useful target
for future tensor computation. A checked counterexample rejects materializing the unweighted tensor kernel
on the scalar precision grid before reweighting. This is a failure of that
implementation, not a general FFT or weighted-operator lower bound.

A fast weighted tensor evaluator, routing,
padding and boundary composition are still missing; no new kappa or change
to the Gaussian dimension exponent is claimed.

Run from the repository root with Python 3.11 or later, standard library only:

```sh
python3 -B research/branchfree-gaussian-inverse/verify.py /tmp/branchfree-check
```

The output must not already exist. The verifier checks package and source
hashes before and after execution, then compares complete exact results
against the frozen expectation. It exercises signed integer packing,
independent rational matrix inverses, large similarity guards, complete
Gaussian/Schur operations, five-stage tensor identities and weighted decay.
The all-size argument is in [PROOF.md](PROOF.md); these bounded finite tests
are not formal verification of the complete multiplication algorithm.

Sources are pinned to PR #486's head; the actual Gaussian/Schur code and
boundary proof are inherited from the RaD/hipotures phase-cell work and
PR #481. Classical attribution and the exact specialization appear in the
proof. No inherited source is modified.
