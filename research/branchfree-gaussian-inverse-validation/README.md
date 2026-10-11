# Fresh validation of the branch-free local inverse

The full source-bound verifier passed on macOS Python 3.11.15 and 3.14.8,
and Linux aarch64 Python 3.12.3 on Spark 2. Every run rebuilt all finite
checks; no computational receipt was reused. Complete CHECKS.json and
RESULT.json are byte-identical across all three runs. Each receipt binds
the same package manifest and upstream-source hashes. The Linux systemd
unit ended with exit 0, inactive state and MainPID 0.

Commands from the repository root:

```sh
python3.11 -B research/branchfree-gaussian-inverse/verify.py /tmp/branchfree-311
python3.14 -B research/branchfree-gaussian-inverse/verify.py /tmp/branchfree-314
python3.12 -B research/branchfree-gaussian-inverse/verify.py /tmp/branchfree-312
```

The macOS 3.11 executable came from the existing verification virtualenv;
the bare python3.11 alias was absent, detected before verifier execution.
Linux used /usr/bin/python3. Use a new output directory for every run.
The Linux job was bounded to 900 seconds, 200% CPU and 8 GiB RAM.

These are exact rational finite arithmetic and error checks. They execute
the new packed interior convolutions and the old rounded batched boundary
and sparse coupling maps. The complete-Schur reference is an independent
dense inverse of the unchanged source H. The conditional all-size proof,
not these samples, supplies the general error/tape transfer. No fast joint
weighted evaluator, complete multiplication theorem or new kappa is claimed.

The updated package also checks 4,096 entries of a dense three-axis operator:
a 14-bit unweighted kernel grid erases 28 entries above the 8-bit error
target, while a 30-bit grid passes. Four symbolic parameter rows support
the separate all-size precision counterexample; their tensors are not
executed. The full wrappers above were all rerun after adding this guard,
and their complete outputs again match byte for byte. The previous
receipts remain available at the initial PR commit.
