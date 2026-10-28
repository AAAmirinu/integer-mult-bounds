# Validation and reproducibility

The initial evidence below is pinned to `ff365dba6911ce615bec76e8d1f149faf1fe16ca`. Its receipt schema and source hashes are historical after the Claude-review response. Follow-up evidence is recorded at the end; numerical parameter intervals are unchanged.

Base and last upstream refresh: `721c03822c421b7f7fcbb2598993b947c4d88419`, 2026-10-28. Priority revision 8. The branch adds only `research/direct-flow-leaf-saturation/`; frozen predecessors and the selected record are unchanged.

## Initial local evidence actually run

Environment: 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]; Linux-6.18.55-x86_64-with-glibc2.41. Standard library only. The retained environment was activated in the isolated contribution worktree. No dependencies were installed.

The exact commands, elapsed seconds, return codes, and final scientific-file hashes are in [logs/validation.json](logs/validation.json). All commands below exited 0:

| Check | Exit | Seconds | Output |
| --- | --- | --- | --- |
| metadata | 0 | 0.207 | [log](logs/metadata.log) |
| primary | 0 | 15.394 | [log](logs/primary.log) |
| optimized | 0 | 16.419 | [log](logs/optimized.log) |
| independent | 0 | 0.098 | [log](logs/independent.log) |
| independent-optimized | 0 | 0.169 | [log](logs/independent-optimized.log) |
| mutations | 0 | 30.049 | [log](logs/mutations.log) |
| mutations-optimized | 0 | 30.11 | [log](logs/mutations-optimized.log) |
| registered | 0 | 43.277 | [log](logs/registered.log) |

Primary and optimized outputs match RESULT.json exactly. The two independent source runs cover ten exact fixtures and reject outgoing-rank truncation. Mutation controls reject altered input bytes in normal/optimized modes, a corrupted receipt under optimized Python, and +1 paid/target multiplicity changes. The registered replay runs all three commands serially and passes; metadata validation is separate from the mathematical proof.

The final proof's reference spelling and canonical Discussion link were normalized after these runs; these prose-only edits change no numerical input or mathematical statement. The scientific hash inventory records the final proof bytes and states that adjustment. The full source root monotonicity bound, corrected citation, independent source integration and mutation controls were already present for these runs.

## Freshness and overlap

Canonical upstream was fetched before selection and again before packaging; both fetched SHAs equal the base above, so no rebase or scientific-source migration was needed. Final cached body refresh: open PRs 2026-10-28T11:20:57Z (376 records), Discussions 2026-10-28T11:22:05Z (5,771 records), complete pagination with no warnings. The earlier closed/merged snapshot at 11:11:49Z has 5,222 records. All 8,348 tracked local note paths were searched; the new package adds two notes. No additional saturation proof was found. A separate live read confirmed the user's [canonical claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19240402). Searches cover bodies and local top-level notes, not every diff or historical source.

## Verification scope

The finite verifier certifies source bindings, rational numerical hypotheses, and semantic controls. The asymptotic argument is the written PROOF.md using the explicitly stated classical interval local-limit theorem. Internal AI reviewers found no unresolved mathematical blocker; REVIEW.md records corrections, final integration and shared dependencies.

No selected-construction replay, `make verify`, historical heavy suite, Lean, or Docker run is applicable to this isolated package. Explicit finite-depth bounds, stable whole-flow shares, the exact refined-induction ceiling, supplier admission, and all five selected framework assumptions remain unrun/unresolved here. Hosted CI is separate; consult the contribution PR for its actual status.

## Initial committed bytes and portable replay

At scientific commit `9465f263a673d2d86e7262523cbeb0e796f486cf`, the following commands passed on all 26 package/input files:

```sh
python3 -B scripts/check_research_commit.py --package research/direct-flow-leaf-saturation --check-source-history
python3 -B scripts/export_research_package.py export --package research/direct-flow-leaf-saturation --ref 9465f263a673d2d86e7262523cbeb0e796f486cf --output /tmp/leaf-saturation.tar
python3 -B scripts/export_research_package.py check /tmp/leaf-saturation.tar
```

The actual temporary archive path was outside the repository; `/tmp/leaf-saturation.tar` above is the portable equivalent. Both exporter commands reported `PASS_RESEARCH_EXPORT`. Committed-byte comparison reported `PASS_RESEARCH_COMMIT_BYTES`, with source-history commit `721c03822c421b7f7fcbb2598993b947c4d88419`.

After extraction into a fresh directory, with PATH pointing to an empty directory and no Git available, all three direct package commands passed: main verifier 14.383 s, independent source checker 0.094 s, mutation controls 28.189 s. [logs/portable-results.json](logs/portable-results.json) records the actual commands, exits and logs. Their source bytes are exactly the scientific commit above; subsequent packaging adds these logs and this record without changing the proof or checker.

These checks establish committed-source availability, transport integrity and portable replay. They do not prove the analytic theorem. Final publication-byte preflight is repeated after recording this evidence; the PR pins the final contribution SHA.

## Claude-review response: current local validation

The response addresses all six findings on `ff365dba6911ce615bec76e8d1f149faf1fe16ca`; [CLAUDE-RESPONSE.md](CLAUDE-RESPONSE.md) maps scope and evidence. All `RESULT.json.parameters` values compare exactly equal to that snapshot. The receipt's source-check labels changed to report histogram equality and fixture sensitivity accurately. The finite source domains remain G≤3.

The following Python 3.12 runs all exited 0. Commands, environment and final scientific-source hashes are in [logs/claude-validation.json](logs/claude-validation.json):

| Check | Seconds | Output |
| --- | --- | --- |
| metadata | 0.282 | [log](logs/claude-metadata.log) |
| registered | 75.068 | [log](logs/claude-registered.log) |
| optimized | 14.372 | [log](logs/claude-optimized.log) |
| independent-optimized | 0.155 | [log](logs/claude-independent-optimized.log) |
| mutations-optimized | 30.389 | [log](logs/claude-mutations-optimized.log) |

The registered replay now runs four commands, including the independent rational enclosure test. Normal and optimized oracle checks additionally passed in 28.674 s and 27.920 s with identical receipts; [timings](logs/claude-enclosures-timing.json), [normal receipt](logs/claude-enclosures-normal.json), [optimized receipt](logs/claude-enclosures-optimized.json). They cover 16 integer logarithm arguments and 127 distinct rational exponential arguments, and reject all three reported remainder faults. Their receipts identify the loaded verifier SHA and exact argument-domain digest. This independently certifies finite-domain enclosure containment, not all-input correctness or the asymptotic theorem.

Both standalone source checkers now reject altered source bytes. Re-pinned empty and terminal-truncated source branches are rejected by the actual histogram comparisons, in normal and optimized modes. This separates source semantics from checksum failures and from fixture sensitivity. Fixed-root-bracket and corrupted-receipt controls remain separately labelled.

The final internal review found no blocking issue in the updated proof, source binding, mutation tests or oracle mathematics. Primary numerical functions were compared by AST against the reviewed snapshot and are unchanged; only `finite_law` changed in verify.py. The oracle's last change adds the loaded source SHA to its receipt and was separately reviewed. README's final “adds eight”→“checks eight” wording avoids implying eighteen distinct source ranks; this prose-only change affects no evidence.

The previously opened draft #6118's hosted run at `ff365dba` had a failed planning job and skipped replay. Its [actual job log](https://github.com/CrocSwap/integer-mult-bounds/actions/runs/40681403297/job/122792722146) reports two failures in `test_research_current_status`: the old selected-family CI text and an exact bold-value match. The shared files involved are unchanged from base. This is separate from the passing package replay; no unrelated suite or shared documentation repair was added here. Check the PR for the latest head's CI status.

The current committed-byte/export/Git-free follow-up is recorded after execution below.
