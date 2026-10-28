# Response to the Claude Code review of ff365dba

The review examined `ff365dba6911ce615bec76e8d1f149faf1fe16ca` and confirmed the scoped theorem and numerical enclosures. This response preserves that theorem, its fixed raw-p7 scope and all parameter values. Claude Code and the follow-up Codex reviewers are AI reviewers, not independent human or formal verification.

| Finding | Resolution | Evidence and limit |
| --- | --- | --- |
| 1. Stone statement and uniformity need precise citation | PROOF.md §3 now names Corollary 1 (7), Theorem (5) and footnote 2; gives the normalization/rescaling and characteristic-function/support equivalence. | Fixed-x (12) is explicitly not the source of uniform concentration. The review reports checking the primary paper; the follow-up internal proof review corroborated the uniform form from Stone's later text but did not retrieve the original afresh. Stronger nonlattice rate hypotheses fail for finite support; this does not exclude quantitative rates by other methods. |
| 2. Terminal-rank flags overstate coverage | Removed the redundant self-factorization assertion; renamed flags as fixture sensitivity. The source identity is the complete histogram comparison. | `test_controls.py` actually empties or truncates the source leaf branch in a temporary tree, re-pins the mutant bytes, and requires semantic rejection by both source-law entry points, normally and under `-O`. A checksum failure cannot count as this semantic rejection. |
| 3. Remainder bounds lack discriminating controls | Added `test_enclosures.py`, an exact-rational independent enclosure oracle. | It checks every successful log/exp argument captured from current `parameters()` and `controls()`. Logarithms use a different series; exponentials use a positive-series geometric tail rather than the primary Lagrange bound. Zero logarithm/exponential tails and the invalid majorant 1 are rejected at explicit fixtures even though the old rounded receipt did not distinguish them. |
| 4. Standalone independent source checker lacks byte binding | `independent_source.py` authenticates every declared live input before any predecessor import. | Comment-only mutations to both predecessor verifier and original flow are rejected by both standalone entry points in normal and optimized modes. No Git is needed. |
| 5. Executable source domain ends at G≤3 | Retained and explicitly scoped; no unnecessary search expansion. | The source proof is for every G, while the local primary/independent fixtures remain eight/ten checks through G=3. Claude reported further G=4–5 corroboration; this package does not present that as a newly executed local check. |
| 6. Leaf observable lacks an explicit formula | PROOF.md §1 now defines the normalized potential-weighted sum over `X−BX`, and its equivalent sum with weights `F[G][ρ] P_r (rρ)^t`. | The final rank uses the full paid inventory and both denominators are positive. The limit is unchanged. |

## What the new controls do not prove

The remainder oracle certifies containment on the captured finite argument domain. Both implementations still share Python's exact rational arithmetic and the exponential series; the logarithm series and exponential remainder arguments differ. This is not formal verification or a proof of the routines for arbitrary future inputs. Its domain digest and loaded verifier SHA identify the checked inputs and code.

The +1 histogram mutations are regressions for the fixed narrow root bracket, not general tests of interval arithmetic. The derivative-bound endpoint ordering is justified by the written monotonicity argument and code review; a changed printed derivative is also caught by the expected receipt. The new enclosure tests do not claim to independently prove that derivative formula.

The source mutation controls exercise the complete histogram equality checks. A flag saying that a fixture has an exit above N/121 only describes its ability to distinguish truncation; it does not independently authenticate or validate a source implementation.

The registered runner still declares Python 3.12. README commands now explicitly select `python3.12` to avoid a default `python3` selecting 3.13 and failing that version gate. No dependency or runner policy is changed.

## Reproduce the response

```sh
python3.12 -B scripts/research_package.py --package research/direct-flow-leaf-saturation
python3.12 -O -B research/direct-flow-leaf-saturation/test_controls.py
python3.12 -O -B research/direct-flow-leaf-saturation/test_enclosures.py
```

[VALIDATION.md](VALIDATION.md) records the actual runs, source hashes and portable replay. The full-flow ceiling, finite-depth rates, stable shares, and supplier admission remain open. The selected #6030 record is unchanged.
