# Verification of the PR627 owner repair

Conditional κ is `817938558930951/500000000000000000`
(`0.001635877117861902`), improving pinned PR627 by
`0.000000127279804738`. The two supplier words, all recipes, verifier code
and 64 JP8 / 8 CK dispatch remain unchanged.

The submitted idle profile is `{1:44,2:1,3:2,12:1,16:3,32:2,48:2220}`.
Every one of the 35,424 roles is checked against actual native widths,
call chronology, physical family, time window, disjoint capacity and
compacted offsets. Rank mass remains 520704. The supplemental checker
uses a separate exact rational log/exp engine for strict moment checks;
its native program hashes are pinned to our independent PR627 replay.

Fresh macOS arm64/Python3.14.8 replay:367.1773s. Fresh Linux
aarch64/Python3.14.8 replay:430.7771s. Both independent map/interval
certificates are byte-identical.

`collect_verify.py` checks each fresh platform's package and six source
pins, all64 successful stages, all51 receipt artifact hashes and every
raw stage-log hash. `macos/` and `linux/` retain the complete checked
receipts, artifacts and logs. No baseline or native receipts are reused
in these final replays. Their timings are operational metadata, not a
controlled speed comparison.

The declaration checker reconstructs SPEC from WITNESS and EXPECTED.
`audit_supplements.py` verifies two positive cases and eight malformed
inputs under `-I -O -B`. `PACKAGING-CORRECTION.json` records the initially
rejected upstream dotted-key representation and its value-preserving
normalization; verifier and mathematical thresholds were not weakened.

`selected-search/` preserves the bounded search and its earlier strict
admission. That earlier run explicitly reused the freshly verified PR627
baseline and native receipts while rebuilding supplier chains. It is
contextual evidence; the final platform replays supply fresh admission.
Floating nomination scores and successful aggregate packing do not prove
an exponent, a global optimum or even physical feasibility. The literal
map, native replay and strict exact admission are the proof boundary.

`SOURCE-REVIEW.json` checks executable/recipe identity and the deterministic
map exporter. Historical `data/search/` files in the core preserve upstream
search provenance; the present search is recorded here and in the core
README. All supplier and predecessor credit remains in NOTICE.md.

The inherited compiler, common-label/mutable-source realization,
whole-call hosting, precision/tape/exact recovery, analytic-transfer and
bit H1-H5 assumptions remain. There is no new supplier construction,
optimality, unconditional theorem, complete Lean proof or practical
speedup claim. Prepared with OpenAI Codex for chafreaky.

```sh
bash research/complex-factored-owner-repair/verify.sh /tmp/factored-replay
python3 -I -O -B research/complex-factored-owner-repair-validation/audit_supplements.py --work /tmp/factored-replay
```
