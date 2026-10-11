# Release verification

The complete unchanged-source root verifier passed on macOS and Linux with Python 3.14.8, actual Boost multiprecision and native C++ compilers. Both started with new output directories and rebuilt the complete pinned #496 package, including #484 and #493, before verifying the changed word and composition. No cached-parent option exists in the published verifier.

All 24 root stages passed on each platform. The complete deterministic RESULT.json files are byte-identical (SHA-256 `4a951fc558757d045f8296b4014e4be71553ac7514a4d996d4bf0232ebefec5f`). The source manifest is `0280d00a97632273b94af7e9956e38755bc6d76194de424e5fe73c91c72bb0db`. All 297 upstream files match pinned Git bytes, and all 306 manifest entries match the publication index.

The evidence includes 2,945 all-column transition identities, compensation and centre-chain checks, 122 normalized helper identities, 806 basis and eight dense whole-program inputs in both orientations, 14 Lemma G controls, 18 controller controls, five serial-pool controls, and 47 strict outer inequalities. Whole-program inputs are not an exhaustive basis of the complete register space. The pre-operation integer bounds peak at 14 numerator bits for the instance checks and 29 for the whole-program checks.

Platform receipts retain timings, input/output hashes and original toolchain paths. RESULT.json contains the exact rational margins and cutoffs. The conditional all-size obligations are stated in the package proof; successful finite replay does not establish them. GitHub CI status is separate from this recorded local evidence.
