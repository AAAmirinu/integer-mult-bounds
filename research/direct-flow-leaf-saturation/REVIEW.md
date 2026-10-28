# Review history and source independence

The sections below through “Initial integration review” record the initial `ff365dba6911ce615bec76e8d1f149faf1fe16ca` snapshot; their hashes and logs are historical after the later review response. Two separate OpenAI Codex agents examined pinned source inputs before seeing the lead's proof. These are internal AI checks, not independent human review, proof-kernel verification, or maintainer acceptance.

## Independent mathematical derivation

The first verifier derived the bounded-offset exponential deficit law and expectation limit from the source independently, then compared the written proof. It identified the need for a global interval concentration bound to justify the mean, and verified the extra outgoing rank is unconditioned. Its 70-digit mpmath diagnostic found `λ≈0.00749912850517142053` and limiting leaf mean `136.518703301364906…`, agreeing with the later rational intervals. Those floating-point values are diagnostic, not the certified evidence.

The independent argument and lead proof both use Stone's interval local-limit theorem. Thus this is an independently derived argument with a **shared classical theorem**, not two unrelated foundations or an independent proof of that theorem. Neither review retrieved the original 1965 theorem's full text; the exact standard interval formulation used is stated in PROOF.md. Original journal contents and published bibliographies corroborate the citation.

The comparison reviewed PROOF.md SHA256 `6c3bdfeeb87bf007d6d37fd2eb131ddf9cbff548d837ecb880f72c0bd229c7d4`. It found no gap in the source law, uniform bounded-offset argument, boundary-atom treatment, or expectation tail bound. It caught a bibliographic error: the draft's Duke journal reference was wrong. The final proof uses *Annals of Mathematical Statistics* 36(2), 546–551 (1965), DOI `10.1214/aoms/1177700165`. This correction and spelling out integer J do not change the argument.

## Independent source check

The second verifier reconstructed the leaf histogram by enumerating ordered paid-rank words, then compared it with **both** #4467's diagnostic flow and the original #4436 `Flow` class. Ten exact fixtures straddle lockstep boundaries: N=121,604,605,606,3024,3025,3026,15124,15125,15126. Their leaf support sizes are 9,9,26,26,30,55,55,65,98,98. All agree; every fixture distinguishes incorrectly truncating the outgoing rank.

The independently written check is preserved as [independent_source.py](independent_source.py), with its output in [logs/independent.log](logs/independent.log). The lead changed only its path selection for portability and replaced assertions with explicit errors so its controls survive `-O`; both forms of the integrated script were rerun. The independent check and primary fixture share the same source inventories and ordered-word characterization, but compare against separately implemented predecessor flows. This checks source interpretation, not the asymptotic theorem.

Source identities checked against retained #4467 head `5f5c1f98c62b9ce4f3db6c0ca47a850a0be577dc`:

| Input | SHA256 |
| --- | --- |
| `research/direct-flow-leaf-walk/verify.py` | `2030d79d7f136b39b4e2a3f5b033af4bba18ab87579ec352267dc1697e02157d` |
| `research/direct-flow-leaf-walk/diagnostics/overlap_flow.py` | `7a1945cadb6bf8f8d88eae32f321ad75c10d5280805e111de6bb02d3d7628117` |
| `research/direct-flow-leaf-walk/README.md` | `bf79c953cd02ad62ffd44c58ae4f5b78f2b3439574176140ba6eceb1b77430cc` |

Original `research/direct-mixed-flow/flow.py` matches #4436 head `56003680aee2871773de408e5f01cc5dd46b144c` (SHA256 `460f0b0262d7b6880973f46240b3fff1e9f04601fa1d658dda18688b1e26575a`). Its retained p7 receipt has SHA256 `9b814be97e3b45fcc28eafa8a65694897a7387f71a14d44796c6aadf303d7fab`; `strictification.paid` and `.targets` equal P,W. All replay inputs are pinned at the publication base, so these historical source-head references are provenance, not required foreign commits.

## Skeptical proof and checker review

The second reviewer then inspected the frozen proof and verifier (verifier SHA256 `a290589881aa04480ac1b50245a1c0faf3e1acebebea9d99ddc227280c519cfe`; see validation source hashes for final integrated bytes). It checked the rational logarithm and exponential remainders, endpoint isolation, nonlattice premise, tail bounds, and claim limits. Normal and `-I -O` verifier outputs agreed. Altered source bytes, a corrupted expected receipt, and +1 paid/target multiplicity mutations were rejected.

No blocking issue was found. The reviewer recommended strengthening monotonicity from the tiny root enclosure to the predecessor's full `[0.99,1]` bisection interval. The final checker implements that stronger bound, exceeding 211661, and includes both +1 histogram controls. The lead reran all affected evidence after this change; the original review hashes do not pretend to identify the final bytes.

## Initial integration review

The skeptical reviewer read the integrated stronger derivative bound, both +1 histogram controls, portable two-source fixture and package claims. No blocker remained. Final reviewed proof SHA256 `b6edd825bc5a3a48fc2860533040faa111c7f239f8724bb3b50cc8a3bdfdc6e7`; verifier SHA256 `9a6ed8de94eab4a643685eba3697d34503bae9dd4c6097b6b8a6f230c29dd3b8`. The reviewer checked that the last proof change was only PR-reference spelling. The confirmed canonical claim link was added to README. Registered evidence and publication checks are reported separately.

## Overlap and limits

Orientation coverage was complete for 375 open PRs, 5,222 closed/merged PRs, 5,771 Discussion records and 8,348 local notes at base `721c03822c421b7f7fcbb2598993b947c4d88419` (2026-10-28 11:09–11:11 UTC). Broader body searches also found #4477's disposition, the later finite-share diagnostic, and the author's explicit request for a saturation proof; these still left the proof open. The final refresh is recorded in VALIDATION.md. No body search establishes novelty or covers every code diff.

Remaining obligations are an effective finite-depth rate and the other full-flow components/exact induction ratio. Finite tests do not prove the asymptotic result; the asymptotic result does not certify finite-depth extrapolations, a supplier, or the multiplication theorem.

## Claude review and follow-up

A user-provided Claude Code AI review independently examined `ff365dba6911ce615bec76e8d1f149faf1fe16ca`. It confirmed the scoped theorem and certified parameter values, reported inspection of Stone's primary text, and identified citation precision and checker-coverage gaps. It is not human or formal verification. The earlier internal reviews' primary-text limitation above remains an accurate description of their work; the later review supplies the equation/footnote mapping now in PROOF.md.

[CLAUDE-RESPONSE.md](CLAUDE-RESPONSE.md) maps all six findings to the changes and their remaining limits. The theorem and every numerical parameter interval are unchanged. The standalone source checker now authenticates inputs, coverage labels distinguish fixture sensitivity from actual source comparisons, and exact independent log/exp bounds discriminate the reported remainder faults. An additional internal reviewer checked the integrated fixes; current checks and source hashes are in the follow-up section of VALIDATION.md.

### Final review of the response

A separate internal reviewer checked the integrated changes without running a competing replay. It verified the alternative logarithm series, the degree 82 exponential geometric tail, full interval containment, meaningful remainder fixtures, re-pinned source mutations and pre-import hashes. No blocking defect was found. Current reviewed verifier SHA256 `3a88ad1da0691afefead7d71c00ab4a51d547c770a40dc2e232c39dc02d8366d`; oracle SHA256 `b92a75601ef676ab0b412395eb2ccaa52c8e802f89fe1fb2f3820cafa173aea4`; proof SHA256 `09dc0d6fd22b5e502b812543ddf78395ab7deacc894cd52430709475acfb2978`. The final oracle metadata addition was checked against the earlier reviewed bytes. These are internal AI reviews with the shared arithmetic/series dependencies disclosed in CLAUDE-RESPONSE.md, not formal verification.
