# Validation of batched Gaussian boundary controls

Fresh complete wrappers passed on macOS Python 3.11.15 and 3.14.8 and Linux
Python 3.12.3. Entire CHECKS.json and RESULT.json bytes agree. The package
EXPECTED.json contains the complete checked artifact. All 12 source pins
match parent Git bytes; the package manifest remained unchanged throughout
these final runs. No cached mathematical result was reused.

The first Linux launch used an incorrect home directory and exited 127
before finding its script. The second launch reached integrity checking,
which rejected eight AppleDouble `._` metadata sidecars from the macOS tar
archive. No expected file was missing or changed. A separate clean archive
with COPYFILE_DISABLE=1 and --no-xattrs preserved every source byte and the
original manifest. The final fresh unit completed with exit 0. The original
failed source snapshot and both failure logs were preserved. Neither failed
launch executed the mathematical checks.

Only the final clean run supplies the Linux success receipt. Its service was
research-resume-20261011-batched-boundary-final3, with RuntimeMaxSec=900,
CPUQuota=200%, MemoryMax=8G; terminal state inactive/dead, ExecMainStatus=0.
No active research compute remains after validation.

The algebraic controls are finite. The all-size bit/tape/analytic transfer
is the conditional written argument in PROOF.md. Complete Schur comparisons
use exact dense local inverse references with the newly rounded boundary
and coupling program. Real Gaussian coefficients act on complex payloads
by applying the same batched program separately to real and imaginary parts;
this incurs constant work and error factors covered by the proof's slack.
GitHub CI is separate and was not claimed passed at draft submission.
