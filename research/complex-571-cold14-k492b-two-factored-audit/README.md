# Contributor validation for two factored extra cold ends

This directory records the current two-helper package, conditional κ = 408937459514291/250000000000000000 = 0.001635749838057164. The pinned predecessor is PR623 at e39a615ca601ce5d62abeb24f3fcdb8644ca1005. Construction and replay commands are in the sibling package's FACTORED-END.md. Jeremy Diviney prepared this contribution with OpenAI Codex assistance; all inherited attribution and assumptions remain.

RESULT, RECEIPT, STAGES and stage-logs record the final strict default-SPEC replay with no reused baseline or provider locals. VALIDATION independently binds all receipt artifacts and raw logs to the frozen package manifest. SOURCE-REVIEW checks the unchanged 23 inherited code files and verify.py, sources, shadow chains, ck supplier, preceding jp8 steps and dispatch. It also recursively compares WITNESS inputs and EXPECTED outputs with SPEC, including recipe pins. The legacy generic witness-spec tool lacks the predecessor's newer step types; GENERIC-TOOL-LIMITATION records that unchanged PR623 is rejected identically. No generic-verifier pass is claimed.

FOCUSED-NEW-HELPER-CONTROLS records a positive full native replay and fourteen deliberate corruptions, seven for each new helper. The unchanged native auditor rejects every corruption. Reproduce with:

```sh
python3 -B check_new_helpers.py \
  --package ../complex-571-cold14-k492b \
  --word /path/to/fresh/jp8-step6-cold_end/FULL-WORD.json.gz \
  --routing /path/to/pr568/research/complex-multicold/vendor/pr558/vendor/pr552/complex-local/inputs/phase-baseline/CANONICAL-WORD.json.gz \
  --out /tmp/two-helper-controls
```

EXPORTER-CHECKS records exact recipe, word and owner-map reproduction, and rejection of optimized Python before output. Across environments, compare decompressed JSON rather than compression streams. Both generators are nominations; all admission checks are independent and unchanged. The final fresh run also includes the inherited 38 cold-end controls, 23 owner controls, 114 assembly controls, native/reflected checks, wrapper and exact-phase checks, two exact moment engines and strict outer inequalities.

REPOSITORY-REGRESSION gives the exact checkout and raw log for the broad make verify suite, including gen4-bank-verify and the selected frontier617 check. That suite runs on the PR623 base; all shared infrastructure is byte-identical. The contributed standalone package receives its own full fresh verification. PREDECESSOR-* records our independent fresh PR623 reproduction. DISCOVERY-ASSEMBLY used already verified baseline/provider artifacts and is separately labeled; the final fresh replay supersedes it. search/ retains nomination maps, scripts and settings. These heuristic searches do not prove optimality.

A preliminary two-helper replay was stopped during source review: the input-only WITNESS still carried the predecessor's recipe SHA, while SPEC already pinned the correct new recipe. We corrected WITNESS, rebound EXPECTED, refroze the manifest, and restarted the complete replay in a new directory. No circuit, owner map or κ changed. The same stale auxiliary WITNESS pin exists in the historical single-helper commit. Its package-specific SPEC-based replay is valid for that single-helper circuit, but the historical SOURCE-REVIEW claim of full WITNESS correspondence was too broad; the current recursive comparison corrects that limitation. The single-helper evidence is retained separately for provenance and does not certify this final two-helper package.

The all-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape/exact recovery, analytic transfer and bit H1–H5 obligations remain assumptions. The PR543 bit supplier is cited and repriced, not rebuilt. These are exact finite contributor checks awaiting independent review, not an unconditional theorem or a full Lean proof.
