# Review findings and evidence limits

## Current review status

The current scientific files are those at `553198839618962e07519b51cb3bbe808ca6f1dc`, with their hashes and replay receipts indexed in [VALIDATION.md](VALIDATION.md#current-evidence-index). Subsequent changes record evidence, attribution and reading guidance. The scoped theorem and every numerical parameter interval are unchanged from the initial published snapshot `ff365dba6911ce615bec76e8d1f149faf1fe16ca`.

Claude Code (Opus 5.5) reviewed that initial snapshot, confirmed the scoped theorem and numerical enclosures, and reported checking Stone's primary text. The six findings and their resolutions below are the canonical review record. Follow-up OpenAI Codex (GPT-6 Astra) review found no unresolved blocker in the integrated response. These are AI reviews, not independent human review, proof-kernel verification or maintainer acceptance.

A separate internal reviewer checked the integrated changes without running a competing replay. It verified the alternative logarithm series, the degree 82 exponential geometric tail, full interval containment, meaningful remainder fixtures, re-pinned source mutations and pre-import hashes. No blocking defect was found. Current reviewed verifier SHA256 `3a88ad1da0691afefead7d71c00ab4a51d547c770a40dc2e232c39dc02d8366d`; oracle SHA256 `b92a75601ef676ab0b412395eb2ccaa52c8e802f89fe1fb2f3820cafa173aea4`; proof SHA256 `09dc0d6fd22b5e502b812543ddf78395ab7deacc894cd52430709475acfb2978`. The final oracle metadata addition was checked against the earlier reviewed bytes. These are internal AI reviews with the shared arithmetic/series dependencies disclosed below, not formal verification.

## Claude review findings

| Finding | Resolution | Evidence and limit |
| --- | --- | --- |
| 1. Stone statement and uniformity need precise citation | PROOF.md §3 now names Corollary 1 (7), Theorem (5) and footnote 2; gives the normalization/rescaling and characteristic-function/support equivalence. | Fixed-x (12) is explicitly not the source of uniform concentration. The review reports checking the primary paper; the follow-up internal proof review corroborated the uniform form from Stone's later text but did not retrieve the original afresh. Stronger nonlattice rate hypotheses fail for finite support; this does not exclude quantitative rates by other methods. |
| 2. Terminal-rank flags overstate coverage | Removed the redundant self-factorization assertion; renamed flags as fixture sensitivity. The source identity is the complete histogram comparison. | `test_controls.py` actually empties or truncates the source leaf branch in a temporary tree, re-pins the mutant bytes, and requires semantic rejection by both source-law entry points, normally and under `-O`. A checksum failure cannot count as this semantic rejection. |
| 3. Remainder bounds lack discriminating controls | Added `test_enclosures.py`, an exact-rational independent enclosure oracle. | It checks every successful log/exp argument captured from current `parameters()` and `controls()`. Logarithms use a different series; exponentials use a positive-series geometric tail rather than the primary Lagrange bound. Zero logarithm/exponential tails and the invalid majorant 1 are rejected at explicit fixtures even though the old rounded receipt did not distinguish them. |
| 4. Standalone independent source checker lacks byte binding | `independent_source.py` authenticates every declared live input before any predecessor import. | Comment-only mutations to both predecessor verifier and original flow are rejected by both standalone entry points in normal and optimized modes. No Git is needed. |
| 5. Executable source domain ends at G≤3 | Retained and explicitly scoped; no unnecessary search expansion. | The source proof is for every G, while the local primary/independent fixtures remain eight/ten checks through G=3. Claude reported further G=4–5 corroboration; this package does not present that as a newly executed local check. |
| 6. Leaf observable lacks an explicit formula | PROOF.md §1 now defines the normalized potential-weighted sum over `X−BX`, and its equivalent sum with weights `F[G][ρ] P_r (rρ)^t`. | The final rank uses the full paid inventory and both denominators are positive. The limit is unchanged. |

## Shared dependencies and remaining limits

The remainder oracle certifies containment on the captured finite argument domain. Both implementations still share Python's exact rational arithmetic and the exponential series; the logarithm series and exponential remainder arguments differ. This is not formal verification or a proof of the routines for arbitrary future inputs. Its domain digest and loaded verifier SHA identify the checked inputs and code.

The +1 histogram mutations are regressions for the fixed narrow root bracket, not general tests of interval arithmetic. The derivative-bound endpoint ordering is justified by the written monotonicity argument and code review; a changed printed derivative is also caught by the expected receipt. The new enclosure tests do not claim to independently prove that derivative formula.

The source mutation controls exercise the complete histogram equality checks. A flag saying that a fixture has an exit above N/121 only describes its ability to distinguish truncation; it does not independently authenticate or validate a source implementation.

The registered runner still declares Python 3.12. README commands now explicitly select `python3.12` to avoid a default `python3` selecting 3.13 and failing that version gate. No dependency or runner policy is changed.

The independent mathematical derivation and lead proof both use Stone's interval local-limit theorem. Initial internal reviewers did not retrieve the original 1965 full text; Claude's later primary-text review supplied the precise equation/footnote mapping. The follow-up internal reviewer corroborated the uniform form using Stone's later text but did not retrieve the original paper afresh. These are distinct review steps, not multiple independent checks of that primary citation.

The independent and primary finite source checks share the pinned inventories and ordered-word characterization; they compare against two separately implemented predecessor flows. Eight primary and ten independent fixtures include overlapping ranks and extend only through G=3. They are corroborating examples, not an exhaustive all-G check or evidence for the asymptotic theorem.

For commands and current receipts, use [VALIDATION.md](VALIDATION.md#current-evidence-index). Finite-depth rates, stable whole-flow shares, the exact refined-induction ceiling and supplier admission remain open. The selected #6030 record is unchanged.

## Historical review record

The following sections record the initial `ff365dba6911ce615bec76e8d1f149faf1fe16ca` contribution and intermediate reviewed bytes. Their hashes and receipts are historical; use the current evidence index above for present code. Two separate OpenAI Codex agents examined pinned source inputs before seeing the lead's proof.

### Independent mathematical derivation

The first verifier derived the bounded-offset exponential deficit law and expectation limit from the source independently, then compared the written proof. It identified the need for a global interval concentration bound to justify the mean, and verified the extra outgoing rank is unconditioned. Its 70-digit mpmath diagnostic found `λ≈0.00749912850517142053` and limiting leaf mean `136.518703301364906…`, agreeing with the later rational intervals. Those floating-point values are diagnostic, not the certified evidence.

The independent argument and lead proof both use Stone's interval local-limit theorem. Thus this is an independently derived argument with a **shared classical theorem**, not two unrelated foundations or an independent proof of that theorem. Neither review retrieved the original 1965 theorem's full text; the exact standard interval formulation used is stated in PROOF.md. Original journal contents and published bibliographies corroborate the citation.

The comparison reviewed PROOF.md SHA256 `6c3bdfeeb87bf007d6d37fd2eb131ddf9cbff548d837ecb880f72c0bd229c7d4`. It found no gap in the source law, uniform bounded-offset argument, boundary-atom treatment, or expectation tail bound. It caught a bibliographic error: the draft's Duke journal reference was wrong. The final proof uses *Annals of Mathematical Statistics* 36(2), 546–551 (1965), DOI `10.1214/aoms/1177700165`. This correction and spelling out integer J do not change the argument.

### Independent source check

The second verifier reconstructed the leaf histogram by enumerating ordered paid-rank words, then compared it with **both** #4467's diagnostic flow and the original #4436 `Flow` class. Ten exact fixtures straddle lockstep boundaries: N=121,604,605,606,3024,3025,3026,15124,15125,15126. Their leaf support sizes are 9,9,26,26,30,55,55,65,98,98. All agree; every fixture distinguishes incorrectly truncating the outgoing rank.

The independently written check is preserved as [independent_source.py](independent_source.py), with its output in [logs/independent.log](logs/independent.log). The lead changed only its path selection for portability and replaced assertions with explicit errors so its controls survive `-O`; both forms of the integrated script were rerun. The independent check and primary fixture share the same source inventories and ordered-word characterization, but compare against separately implemented predecessor flows. This checks source interpretation, not the asymptotic theorem.

Source identities checked against retained #4467 head `5f5c1f98c62b9ce4f3db6c0ca47a850a0be577dc`:

| Input | SHA256 |
| --- | --- |
| `research/direct-flow-leaf-walk/verify.py` | `2030d79d7f136b39b4e2a3f5b033af4bba18ab87579ec352267dc1697e02157d` |
| `research/direct-flow-leaf-walk/diagnostics/overlap_flow.py` | `7a1945cadb6bf8f8d88eae32f321ad75c10d5280805e111de6bb02d3d7628117` |
| `research/direct-flow-leaf-walk/README.md` | `bf79c953cd02ad62ffd44c58ae4f5b78f2b3439574176140ba6eceb1b77430cc` |

Original `research/direct-mixed-flow/flow.py` matches #4436 head `56003680aee2871773de408e5f01cc5dd46b144c` (SHA256 `460f0b0262d7b6880973f46240b3fff1e9f04601fa1d658dda18688b1e26575a`). Its retained p7 receipt has SHA256 `9b814be97e3b45fcc28eafa8a65694897a7387f71a14d44796c6aadf303d7fab`; `strictification.paid` and `.targets` equal P,W. All replay inputs are pinned at the publication base, so these historical source-head references are provenance, not required foreign commits.

### Skeptical proof and checker review

The second reviewer then inspected the frozen proof and verifier (verifier SHA256 `a290589881aa04480ac1b50245a1c0faf3e1acebebea9d99ddc227280c519cfe`; see validation source hashes for final integrated bytes). It checked the rational logarithm and exponential remainders, endpoint isolation, nonlattice premise, tail bounds, and claim limits. Normal and `-I -O` verifier outputs agreed. Altered source bytes, a corrupted expected receipt, and +1 paid/target multiplicity mutations were rejected.

No blocking issue was found. The reviewer recommended strengthening monotonicity from the tiny root enclosure to the predecessor's full `[0.99,1]` bisection interval. The final checker implements that stronger bound, exceeding 211661, and includes both +1 histogram controls. The lead reran all affected evidence after this change; the original review hashes do not pretend to identify the final bytes.

### Initial integration review

The skeptical reviewer read the integrated stronger derivative bound, both +1 histogram controls, portable two-source fixture and package claims. No blocker remained. Final reviewed proof SHA256 `b6edd825bc5a3a48fc2860533040faa111c7f239f8724bb3b50cc8a3bdfdc6e7`; verifier SHA256 `9a6ed8de94eab4a643685eba3697d34503bae9dd4c6097b6b8a6f230c29dd3b8`. The reviewer checked that the last proof change was only PR-reference spelling. The confirmed canonical claim link was added to README. Registered evidence and publication checks are reported separately.

### Overlap and limits

Orientation coverage was complete for 375 open PRs, 5,222 closed/merged PRs, 5,771 Discussion records and 8,348 local notes at base `721c03822c421b7f7fcbb2598993b947c4d88419` (2026-10-28 11:09–11:11 UTC). Broader body searches also found #4477's disposition, the later finite-share diagnostic, and the author's explicit request for a saturation proof; these still left the proof open. The final refresh is recorded in VALIDATION.md. No body search establishes novelty or covers every code diff.

Remaining obligations are an effective finite-depth rate and the other full-flow components/exact induction ratio. Finite tests do not prove the asymptotic result; the asymptotic result does not certify finite-depth extrapolations, a supplier, or the multiplication theorem.
