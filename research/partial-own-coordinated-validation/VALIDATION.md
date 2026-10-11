# Fresh verification

Both complete Python 3.14 runs passed: macOS arm64 and Linux aarch64. Each ran
7 outer stages, 21 dependency stages and 13 new coordinated-local stages, all
with exit status zero. Both bit and complex suppliers were rebuilt. The complete
RESULT.json files and the underlying dependency EXACT-MATH.json files match
byte for byte across platforms.

RESULT SHA-256: b5700b468a40f9e142165999b4818a6de0af53183f801b8057c0a40fa78c9c59

Frozen package manifest SHA-256:
9544660a1a54915a45f0c48abb3c327ce3f01381a2a448ca09442c18cfcb992c

All 350 manifest files match the source frozen before either run. All 328 copied
source files also match their pinned Git commits. The portability edit inherited
from PR512 is documented inside the source package, with its upstream original.

The Linux initial launch supplied an absent /usr/include Boost path and stopped
before any supplier computation. Its failure is preserved. The corrected fresh
run used genuine Boost headers from the existing research toolchain, recorded
in LINUX-BUILD-TOOLCHAIN.json; its 257-bit C++ integer probe passed.

The actual asynchronous controller has 2,898 orthogonal charts and rejects
19 corruptions. Both exact moment engines, all 47 strict outer inequalities,
six bootstrap levels and four outer controls passed. Required prefix: 205 bits;
charged prefix: 512 bits; physical row coefficient: 16,467 < 20,161.

The separate packing dual was checked against the newly rebuilt local word,
not only the discovery output. Its standalone checker uses exact rationals and
rejects five certificate corruptions; see packing-ceiling/PROOF.md. Optimizer
output is not an acceptance premise.

PR514 subsequently reported a higher conditional result with 92 pivots. This
84-pivot package and its fixed-word ceiling do not claim to exceed or bound that
changed word. GitHub CI is separate; the local receipts do not imply CI passed.
