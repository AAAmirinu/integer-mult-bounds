# Two-hour bounded exploration, 2026-10-11 JST

The task was to prepare by 14:30, test 25 ideas by 15:00, deepen five families
by 15:30, select one by 16:00 and submit by 16:30. The initial screen completed
at approximately 14:34; the family comparisons completed by approximately
14:45. Source checks, independent replay and adaptations to newly published
suppliers continued afterward. Public PR descriptions and the existing PR #368
campaign were checked for overlap. These are new bounded trials in this
campaign, not a claim that no one anywhere has tried the ideas.

`plan25.json` lists all 25 ideas. `screen25-results.json` records every trial,
including failed-to-improve trials; all trial words passed the exploratory
complete F2 identity and nested-frame checks. These scores are discovery
numbers, **not certified kappas**. Their common five-stage bit baseline was
approximately 0.000904072821; comparing that score with the final seven-stage
composition would be invalid.

| IDs | Trial family | Best exploratory bit score |
|---|---|---:|
| 1–5 | low-read rank/cost restrictions | 0.000871148694 |
| 6–14 | read covers, source choice, phase thresholds | 0.000904072821 |
| 15–17 | balanced trees, frame-aware trees, subtree reuse | 0.000851279141 |
| 18–21 | extremal frames and equal-frame components | 0.000905250752 |
| 22–24 | commuting gate orders and earlier cleanup | 0.000904493999 |
| 25 | copied-total basis change | 0.000904072821 |

Five promising families were deepened: extremal single frames, equal-frame
components, connected pairs, forward commuting and backward commuting.
`deep5-results.json` includes order variants and 12 pair-search seeds.
Connected pairs gave approximately 0.000907399199. Three-gate coalescence
in `coupled-triples.json` gave approximately 0.000907445316. A bounded
four-gate search did not improve that result (`coupled-groups-4.json`).
Independent complex-side frame and neutral-plateau experiments gave no useful
improvement; they were not promoted into the scientific package.

The selected family is deterministic connected frame coalescence. After PR
#376 appeared, its exact reused R=822 word was reconstructed and this search
was reapplied: 70 accepted moves, 98 changed gate frames
(`reused-retiming-changes.json`). PR #377's nine-stage complex supplier and
PR #381's unsplit degree-two bit layout then replaced superseded suppliers.
Both full supplier suites and the new physical word are replayed by `verify.py`.
The initial comparison was against PR #382, available at 15:20. The final
comparison is against PR #384's stronger far-retimed unit. Its previously
unreplayed physical, Clifford and finite stages are now replayed from the full
pinned #377 source, following #385's derivation procedure, before admission.
PR #387's smaller beta backoff was then incorporated into the eight-step
assembly; that three-round witness is the final comparison.

To reproduce a screen trial from the repository root:

```sh
python3 -B research/e8-coupled-bit-retiming/campaign/code/explore_e8.py retime_both --out /tmp/e8-screen-one
```

Other methods are the `method` values in `plan25.json`. The final candidate is
reproduced by the mandatory full verifier, not by the floating screen. Source
pins, exact costs, finite charges, baseline equality at the complex cap and
conditional proof obligations are recorded in the package proof and record.

The optional campaign scripts also require SciPy 1.18.1; the mandatory exact
verifier has no SciPy dependency.
