# Recorded validation

These are historical host execution results from 2026-10-11, prepared with
OpenAI Codex assistance. They are separate from Evidence Forge's captured
JSON assessments and do not establish the retained all-size assumptions.
The deterministic arithmetic certificate is `EXPECTED.json`; wall times
below are observations, not performance comparisons.

## Complete affected pipeline

On Windows, Python 3.12.10 with SymPy 1.14.0 executed:

```sh
python -B research/gen4-envelope-refinement/verify.py --output /new/output/directory
```

The actual output directory was a fresh private host directory. The process
exited successfully. Its execution receipt recorded `status: PASS`,
`mode: fresh-physical-replay`, and `physical_replay_fresh: true`.
The complete run took approximately 603.14 seconds, including approximately
593.97 seconds for the unchanged inherited verifier.

All nine mandatory inherited stages passed: virtual word, raw ledger, bit
physical/global/geometry, scalar columns and restoration, prime exclusions,
banks, complex supplier, mathematics, and finite bill. The replay recorded
`inputs_unchanged: true` and all nine omitted-stage rejection controls.
The wrapper compared the complete fresh inherited certificate and finite
bill with the pinned historical JSON before accepting refined arithmetic.

The source inventory contained 112 files. The source manifest SHA-256 was
`99e202d9ffe5baf89e02796edbfc7095b2b227622eccf7b61afa01fd61aeb385`.
The final refined certificate SHA-256 was
`4e2baeaa66ed90260a41cd887cf2e4c3b97853d82484872abac6c1f7ee41b8bb`.
The retained private execution receipt SHA-256 was
`4b8866ea1f83db9505bcb2aa813f4d79d12a0c98af63487957529c4558226092`;
its inherited verification receipt SHA-256 was
`26198ba4c83518fac0cf362d2c90178e14d83d05ef3576c95f01d1455e8baa94`.
These hashes identify retained observations; a reader should reproduce the
run rather than treat a receipt hash as independent execution attestation.

## Arithmetic portability and focused tests

The wrapper's explicitly labelled `--arithmetic-only` mode passed on both
Windows/Python 3.12.10 and Ubuntu 24.04 under WSL/Python 3.12.3. Both runs
produced exactly the certificate hash above, with
`physical_replay_fresh: false`. Canonical UTF-8/LF serialization avoids
platform-dependent certificate hashes.

```sh
python -B -m unittest discover -s tests -p test_gen4_envelope_refinement.py -v
python -B -m unittest discover -s tests -p test_selected_result.py -v
python -B scripts/verify_selected_result.py
```

All 15 new tests passed on both Windows and Ubuntu/WSL. All four existing
selected-result tests and the selected-result check passed on Windows.
The new checks include exhaustive small-field invertibility counts,
disjoint-branch endpoint/interior cases and a failing cheap fallback,
finite composition identities, strict grid endpoints, changed-source and
missing-stage rejection, both rational engines and canonical bytes.

The full arithmetic report retains 55 trials across eleven cycles, 47
strict outer inequalities, seven margins, two exact moment engines, and
nine adverse controls. Both engines exclude the next coarse grid point;
the next headline grid point fails its binding inequality.

## Retained failure and limitations

An earlier direct invocation of the unchanged inherited verifier failed
after six stages because Windows' legacy `cp1252` decoder could not read a
captured UTF-8 Lean source. The failure was not a passing full replay.
Its retained failure receipt SHA-256 is
`107317bd8ff8f0ea86ce61c4a924c88c303e73b28eb03d3d77b656ef6aca648e`.
The new launcher sets `PYTHONUTF8=1` for the inherited verifier and its
children. The successful full run above restarted every stage; it did not
resume or relabel the failed attempt. The original package stayed unchanged.

The aggregate `make verify` command could not start locally because GNU
Make was unavailable. This record therefore claims completion of the
affected Python pipeline and focused tests, not the repository's entire
historical, C++ or Lean verification suites. Dedicated Linux CI replays
the affected pipeline on Python 3.11 and 3.13; CI completion is not implied
by this local record. Existing broader CI remains separate.

Evidence Forge's public investigation index is `EVIDENCE-FORGE.json`.
Its authoritative ledger retains the failed attempt and non-improving
cycle alongside the successful observations. Those observations remain
distinct from independent dossier assessments and mathematical acceptance.
