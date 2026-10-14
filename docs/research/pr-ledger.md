# PR review and integration ledger

The immutable starting snapshot contains **446 PRs**. Explicit later family rounds extend the current inventory to **722**; unrelated arrivals remain outside the round.

[Machine-readable ledger](pr-ledger.json) · [Starting snapshot](../../research/pr-reconciliation-20261012/starting-snapshot.json)

The ledger separates historical review from integration. A prior snapshot or a mention in a note does not certify a contribution. “Partially reviewed” includes scoped review and triage with their original limitations; “changed since review” means the present head lacks matching recorded coverage. Archived incorporation preserves a historical implementation and attribution without making it the selected result.

| Disposition | Count |
|---|---:|
| incorporated | 576 |
| partially reviewed | 27 |
| superseded | 1 |
| unreviewed | 118 |

The earlier reconciliation closing snapshot had 438 starting PRs still open and 441 total open. These are historical counts, not a live queue measurement. Later dispositions are recorded below.

[Earlier family review](community-family533-review.md) · [Earlier dispositions](../../research/community-family533-audit/DISPOSITIONS.json)

The earlier construction family #533–#537 and formal connections #513/#528 are covered there, including the #503/#510 bit dependency. #463 has only its vendored pipeline subset reviewed.

[Family through #588](community-family588-review.md) · [Exact-head dispositions](../../research/community-family588-audit/DISPOSITIONS.json)

This frozen round covers #543/#545/#555 and related construction, research and tooling packages through #588. Each disposition distinguishes completed checks, publication and remaining obligations. The separate formalization PRs and later arrivals are not approved by this round.

[100-PR historical reconciliation](community-reconciliation100-review.md): exact-head coverage and individual carry-forward tasks; it is not 100 completed mathematical audits.
[Five early contributions](community-historical-five-review.md): #2/#4/#8/#9/#12 retained with complete historical sources and focused replays.
[Remaining 92 contributions](community-reconciliation92-review.md): source retention, scoped review and closure receipts; #122 awaits its missing parent circuit/profile.
[Previous 100 contributions, #153–#303](community-reconciliation-next100-review.md): individual scope and explicit remaining obligations.
[Third 100 contributions, #304–#421](community-reconciliation-third100-review.md): constructions, research and verification with source-bound execution.

## Remaining priorities

1. Resolve the explicit remaining questions on partially reviewed or changed heads; consult the latest family disposition before repeating a replay.
2. Continue with a frozen chunk of live, non-draft, unreviewed PRs. Compare current heads with published reviews and exclude submissions awaiting a concrete revision.
3. Keep source retention, scoped execution, publication and actual GitHub closure separate. Preserve research, verification and parallel contribution credit even when a result is superseded.
4. Build formal connections to the actual finite constructions; abstract theorem builds alone do not instantiate the selected multiplication algorithm.

## Starting PR inventory

Each evidence link leads to the original scoped assessment. The JSON records exact heads, unresolved questions, integration locations and closure receipts.

| PR | Contributor | Disposition | Evidence or remaining question |
|---|---|---|---|
| [#1](https://github.com/CrocSwap/integer-mult-bounds/pull/1) | Paureel | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#2](https://github.com/CrocSwap/integer-mult-bounds/pull/2) | Bortlesboat | incorporated | [record 1](../../research/community-historical-five-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#3](https://github.com/CrocSwap/integer-mult-bounds/pull/3) | eumemic | incorporated | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) · [record 2](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#4](https://github.com/CrocSwap/integer-mult-bounds/pull/4) | dleen | incorporated | [record 1](../../research/community-historical-five-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#5](https://github.com/CrocSwap/integer-mult-bounds/pull/5) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#6](https://github.com/CrocSwap/integer-mult-bounds/pull/6) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#7](https://github.com/CrocSwap/integer-mult-bounds/pull/7) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#8](https://github.com/CrocSwap/integer-mult-bounds/pull/8) | rohanarun | incorporated | [record 1](../../research/community-historical-five-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#9](https://github.com/CrocSwap/integer-mult-bounds/pull/9) | rohanarun | incorporated | [record 1](../../research/community-historical-five-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#12](https://github.com/CrocSwap/integer-mult-bounds/pull/12) | rohanarun | incorporated | [record 1](../../research/community-historical-five-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#13](https://github.com/CrocSwap/integer-mult-bounds/pull/13) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#14](https://github.com/CrocSwap/integer-mult-bounds/pull/14) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#15](https://github.com/CrocSwap/integer-mult-bounds/pull/15) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#16](https://github.com/CrocSwap/integer-mult-bounds/pull/16) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#17](https://github.com/CrocSwap/integer-mult-bounds/pull/17) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#19](https://github.com/CrocSwap/integer-mult-bounds/pull/19) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#20](https://github.com/CrocSwap/integer-mult-bounds/pull/20) | hipotures | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#21](https://github.com/CrocSwap/integer-mult-bounds/pull/21) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#22](https://github.com/CrocSwap/integer-mult-bounds/pull/22) | DominikScholz | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#23](https://github.com/CrocSwap/integer-mult-bounds/pull/23) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#25](https://github.com/CrocSwap/integer-mult-bounds/pull/25) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#27](https://github.com/CrocSwap/integer-mult-bounds/pull/27) | DominikScholz | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#28](https://github.com/CrocSwap/integer-mult-bounds/pull/28) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#29](https://github.com/CrocSwap/integer-mult-bounds/pull/29) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#31](https://github.com/CrocSwap/integer-mult-bounds/pull/31) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#33](https://github.com/CrocSwap/integer-mult-bounds/pull/33) | DominikScholz | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#34](https://github.com/CrocSwap/integer-mult-bounds/pull/34) | jamesyc | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#35](https://github.com/CrocSwap/integer-mult-bounds/pull/35) | DominikScholz | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#38](https://github.com/CrocSwap/integer-mult-bounds/pull/38) | DominikScholz | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#40](https://github.com/CrocSwap/integer-mult-bounds/pull/40) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#41](https://github.com/CrocSwap/integer-mult-bounds/pull/41) | hipotures | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#42](https://github.com/CrocSwap/integer-mult-bounds/pull/42) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#44](https://github.com/CrocSwap/integer-mult-bounds/pull/44) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#47](https://github.com/CrocSwap/integer-mult-bounds/pull/47) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#63](https://github.com/CrocSwap/integer-mult-bounds/pull/63) | DominikScholz | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#65](https://github.com/CrocSwap/integer-mult-bounds/pull/65) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#66](https://github.com/CrocSwap/integer-mult-bounds/pull/66) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#67](https://github.com/CrocSwap/integer-mult-bounds/pull/67) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#68](https://github.com/CrocSwap/integer-mult-bounds/pull/68) | DominikScholz | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#69](https://github.com/CrocSwap/integer-mult-bounds/pull/69) | eumemic | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#70](https://github.com/CrocSwap/integer-mult-bounds/pull/70) | alejandrozu | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#71](https://github.com/CrocSwap/integer-mult-bounds/pull/71) | chafreaky | incorporated | [record 1](../../docs/research/community-round3-validation.json) · [record 2](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 3](../../research/overnight-pr-review-20261009/dispositions.json) · [record 4](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#74](https://github.com/CrocSwap/integer-mult-bounds/pull/74) | tomdif | partially reviewed | [record 1](../../docs/research/community-round3-validation.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#75](https://github.com/CrocSwap/integer-mult-bounds/pull/75) | alejandrozu | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#76](https://github.com/CrocSwap/integer-mult-bounds/pull/76) | DominikScholz | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#77](https://github.com/CrocSwap/integer-mult-bounds/pull/77) | huxint | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#78](https://github.com/CrocSwap/integer-mult-bounds/pull/78) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#79](https://github.com/CrocSwap/integer-mult-bounds/pull/79) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#80](https://github.com/CrocSwap/integer-mult-bounds/pull/80) | rohanarun | incorporated | [record 1](../../docs/research/community-round3-validation.json) · [record 2](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 3](../../research/overnight-pr-review-20261009/dispositions.json) · [record 4](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#81](https://github.com/CrocSwap/integer-mult-bounds/pull/81) | DominikScholz | incorporated | [record 1](../../docs/research/community-round4-validation.json) · [record 2](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 3](../../research/overnight-pr-review-20261009/dispositions.json) · [record 4](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#82](https://github.com/CrocSwap/integer-mult-bounds/pull/82) | rohanarun | incorporated | [record 1](../../docs/research/community-round4-validation.json) · [record 2](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 3](../../research/overnight-pr-review-20261009/dispositions.json) · [record 4](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#83](https://github.com/CrocSwap/integer-mult-bounds/pull/83) | JosephDemarest | incorporated | [record 1](../../docs/research/community-round4-validation.json) · [record 2](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 3](../../research/overnight-pr-review-20261009/dispositions.json) · [record 4](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#84](https://github.com/CrocSwap/integer-mult-bounds/pull/84) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#85](https://github.com/CrocSwap/integer-mult-bounds/pull/85) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#86](https://github.com/CrocSwap/integer-mult-bounds/pull/86) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#87](https://github.com/CrocSwap/integer-mult-bounds/pull/87) | gupt1156 | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#88](https://github.com/CrocSwap/integer-mult-bounds/pull/88) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#89](https://github.com/CrocSwap/integer-mult-bounds/pull/89) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#90](https://github.com/CrocSwap/integer-mult-bounds/pull/90) | anxkhn | superseded | [record 1](../../docs/research/community-round5-validation.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#91](https://github.com/CrocSwap/integer-mult-bounds/pull/91) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#92](https://github.com/CrocSwap/integer-mult-bounds/pull/92) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#93](https://github.com/CrocSwap/integer-mult-bounds/pull/93) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#94](https://github.com/CrocSwap/integer-mult-bounds/pull/94) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#95](https://github.com/CrocSwap/integer-mult-bounds/pull/95) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#97](https://github.com/CrocSwap/integer-mult-bounds/pull/97) | jacklightChen | incorporated | [record 1](../../docs/research/community-round5-validation.json) · [record 2](../../docs/research/community-round6-validation.json) · [record 3](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 4](../../research/overnight-pr-review-20261009/dispositions.json) · [record 5](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#98](https://github.com/CrocSwap/integer-mult-bounds/pull/98) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#99](https://github.com/CrocSwap/integer-mult-bounds/pull/99) | djsmanchanda | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#100](https://github.com/CrocSwap/integer-mult-bounds/pull/100) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#102](https://github.com/CrocSwap/integer-mult-bounds/pull/102) | SovereignSteak | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#103](https://github.com/CrocSwap/integer-mult-bounds/pull/103) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#106](https://github.com/CrocSwap/integer-mult-bounds/pull/106) | Th0rgal | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#107](https://github.com/CrocSwap/integer-mult-bounds/pull/107) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#108](https://github.com/CrocSwap/integer-mult-bounds/pull/108) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#109](https://github.com/CrocSwap/integer-mult-bounds/pull/109) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#110](https://github.com/CrocSwap/integer-mult-bounds/pull/110) | ikeboy | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#111](https://github.com/CrocSwap/integer-mult-bounds/pull/111) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#113](https://github.com/CrocSwap/integer-mult-bounds/pull/113) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#114](https://github.com/CrocSwap/integer-mult-bounds/pull/114) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#116](https://github.com/CrocSwap/integer-mult-bounds/pull/116) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#117](https://github.com/CrocSwap/integer-mult-bounds/pull/117) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#118](https://github.com/CrocSwap/integer-mult-bounds/pull/118) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#121](https://github.com/CrocSwap/integer-mult-bounds/pull/121) | Th0rgal | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#122](https://github.com/CrocSwap/integer-mult-bounds/pull/122) | SovereignSteak | partially reviewed | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#123](https://github.com/CrocSwap/integer-mult-bounds/pull/123) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#124](https://github.com/CrocSwap/integer-mult-bounds/pull/124) | jamesyc | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#125](https://github.com/CrocSwap/integer-mult-bounds/pull/125) | GamingPuzzled | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#126](https://github.com/CrocSwap/integer-mult-bounds/pull/126) | DanieleCorso | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#127](https://github.com/CrocSwap/integer-mult-bounds/pull/127) | GamingPuzzled | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#128](https://github.com/CrocSwap/integer-mult-bounds/pull/128) | an664 | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#129](https://github.com/CrocSwap/integer-mult-bounds/pull/129) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#131](https://github.com/CrocSwap/integer-mult-bounds/pull/131) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#133](https://github.com/CrocSwap/integer-mult-bounds/pull/133) | Th0rgal | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#135](https://github.com/CrocSwap/integer-mult-bounds/pull/135) | DanieleCorso | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) |
| [#137](https://github.com/CrocSwap/integer-mult-bounds/pull/137) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#138](https://github.com/CrocSwap/integer-mult-bounds/pull/138) | geckods | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#141](https://github.com/CrocSwap/integer-mult-bounds/pull/141) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#142](https://github.com/CrocSwap/integer-mult-bounds/pull/142) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#143](https://github.com/CrocSwap/integer-mult-bounds/pull/143) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#145](https://github.com/CrocSwap/integer-mult-bounds/pull/145) | Th0rgal | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#146](https://github.com/CrocSwap/integer-mult-bounds/pull/146) | Th0rgal | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/overnight-pr-review-20261009/dispositions.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) · [record 4](../../research/pr-reconciliation-20261012/content-comparison.json) |
| [#148](https://github.com/CrocSwap/integer-mult-bounds/pull/148) | gupt1156 | partially reviewed | [record 1](../../research/overnight-pr-review-20261009/dispositions.json) · [record 2](../../research/pr-reconciliation-20261012/content-comparison.json) |
| [#153](https://github.com/CrocSwap/integer-mult-bounds/pull/153) | geckods | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#154](https://github.com/CrocSwap/integer-mult-bounds/pull/154) | eumemic | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round8-audit/validation.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#158](https://github.com/CrocSwap/integer-mult-bounds/pull/158) | geckods | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#160](https://github.com/CrocSwap/integer-mult-bounds/pull/160) | GamingPuzzled | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#162](https://github.com/CrocSwap/integer-mult-bounds/pull/162) | DaysSky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#163](https://github.com/CrocSwap/integer-mult-bounds/pull/163) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#164](https://github.com/CrocSwap/integer-mult-bounds/pull/164) | eumemic | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#165](https://github.com/CrocSwap/integer-mult-bounds/pull/165) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#166](https://github.com/CrocSwap/integer-mult-bounds/pull/166) | jamesyc | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#167](https://github.com/CrocSwap/integer-mult-bounds/pull/167) | GamingPuzzled | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#168](https://github.com/CrocSwap/integer-mult-bounds/pull/168) | eumemic | incorporated | [record 1](../../research/community-round8-audit/validation.json) · [record 2](../../research/pr-reconciliation-20261012/incorporation-checks.json) |
| [#169](https://github.com/CrocSwap/integer-mult-bounds/pull/169) | GamingPuzzled | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#170](https://github.com/CrocSwap/integer-mult-bounds/pull/170) | huxint | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#171](https://github.com/CrocSwap/integer-mult-bounds/pull/171) | jon314159 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#172](https://github.com/CrocSwap/integer-mult-bounds/pull/172) | mikey1201 | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#173](https://github.com/CrocSwap/integer-mult-bounds/pull/173) | GamingPuzzled | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#174](https://github.com/CrocSwap/integer-mult-bounds/pull/174) | TeS44 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#175](https://github.com/CrocSwap/integer-mult-bounds/pull/175) | chafreaky | incorporated | [record 1](../../research/community-round8-audit/validation.json) · [record 2](../../research/pr-reconciliation-20261012/incorporation-checks.json) |
| [#177](https://github.com/CrocSwap/integer-mult-bounds/pull/177) | gabriele-nespoli | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#178](https://github.com/CrocSwap/integer-mult-bounds/pull/178) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#179](https://github.com/CrocSwap/integer-mult-bounds/pull/179) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#180](https://github.com/CrocSwap/integer-mult-bounds/pull/180) | M6LI | partially reviewed | [record 1](../../research/community-round9-audit/review-ledger.json) |
| [#181](https://github.com/CrocSwap/integer-mult-bounds/pull/181) | chafreaky | incorporated | [record 1](../../research/community-round8-audit/validation.json) · [record 2](../../research/pr-reconciliation-20261012/incorporation-checks.json) |
| [#182](https://github.com/CrocSwap/integer-mult-bounds/pull/182) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round8-audit/validation.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) · [record 4](../../research/pr-reconciliation-20261012/content-comparison.json) |
| [#183](https://github.com/CrocSwap/integer-mult-bounds/pull/183) | romainhedouin | incorporated | [record 1](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) · [record 2](../../research/pr-reconciliation-20261012/content-comparison.json) |
| [#185](https://github.com/CrocSwap/integer-mult-bounds/pull/185) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round8-audit/validation.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) · [record 4](../../research/pr-reconciliation-20261012/content-comparison.json) |
| [#187](https://github.com/CrocSwap/integer-mult-bounds/pull/187) | rohanarun | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#188](https://github.com/CrocSwap/integer-mult-bounds/pull/188) | huxint | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#189](https://github.com/CrocSwap/integer-mult-bounds/pull/189) | chafreaky | incorporated | [record 1](../../research/community-reconciliation92-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) · [record 3](../../research/pr-reconciliation100-20261013/DISPOSITIONS.json) |
| [#191](https://github.com/CrocSwap/integer-mult-bounds/pull/191) | ikeboy | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#192](https://github.com/CrocSwap/integer-mult-bounds/pull/192) | DaysSky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#193](https://github.com/CrocSwap/integer-mult-bounds/pull/193) | ikeboy | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#194](https://github.com/CrocSwap/integer-mult-bounds/pull/194) | ikeboy | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#195](https://github.com/CrocSwap/integer-mult-bounds/pull/195) | huxint | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#196](https://github.com/CrocSwap/integer-mult-bounds/pull/196) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#197](https://github.com/CrocSwap/integer-mult-bounds/pull/197) | evmckinney9 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#199](https://github.com/CrocSwap/integer-mult-bounds/pull/199) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#200](https://github.com/CrocSwap/integer-mult-bounds/pull/200) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#201](https://github.com/CrocSwap/integer-mult-bounds/pull/201) | DaysSky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#202](https://github.com/CrocSwap/integer-mult-bounds/pull/202) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#203](https://github.com/CrocSwap/integer-mult-bounds/pull/203) | huxint | partially reviewed | [record 1](../../research/community-round9-audit/review-ledger.json) |
| [#204](https://github.com/CrocSwap/integer-mult-bounds/pull/204) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#205](https://github.com/CrocSwap/integer-mult-bounds/pull/205) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#207](https://github.com/CrocSwap/integer-mult-bounds/pull/207) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#208](https://github.com/CrocSwap/integer-mult-bounds/pull/208) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#210](https://github.com/CrocSwap/integer-mult-bounds/pull/210) | eumemic | incorporated | [record 1](../../docs/research/community-pr210-integration.json) · [record 2](../../research/community-batch970-audit/COMPANION-REVIEWS.json) · [record 3](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 4](../../research/community-round9-audit/review-ledger.json) · [record 5](../../research/pr-reconciliation-20261012/content-comparison.json) |
| [#211](https://github.com/CrocSwap/integer-mult-bounds/pull/211) | rohanarun | partially reviewed | [record 1](../../research/community-round9-audit/review-ledger.json) |
| [#212](https://github.com/CrocSwap/integer-mult-bounds/pull/212) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#214](https://github.com/CrocSwap/integer-mult-bounds/pull/214) | antoine-olivier | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#215](https://github.com/CrocSwap/integer-mult-bounds/pull/215) | GamingPuzzled | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#216](https://github.com/CrocSwap/integer-mult-bounds/pull/216) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#217](https://github.com/CrocSwap/integer-mult-bounds/pull/217) | hcg890 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#221](https://github.com/CrocSwap/integer-mult-bounds/pull/221) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#223](https://github.com/CrocSwap/integer-mult-bounds/pull/223) | ikeboy | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#224](https://github.com/CrocSwap/integer-mult-bounds/pull/224) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#225](https://github.com/CrocSwap/integer-mult-bounds/pull/225) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#226](https://github.com/CrocSwap/integer-mult-bounds/pull/226) | pCwOrM | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#227](https://github.com/CrocSwap/integer-mult-bounds/pull/227) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#228](https://github.com/CrocSwap/integer-mult-bounds/pull/228) | tehruhn | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#229](https://github.com/CrocSwap/integer-mult-bounds/pull/229) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#233](https://github.com/CrocSwap/integer-mult-bounds/pull/233) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#234](https://github.com/CrocSwap/integer-mult-bounds/pull/234) | hcg890 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#235](https://github.com/CrocSwap/integer-mult-bounds/pull/235) | gabriele-nespoli | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#236](https://github.com/CrocSwap/integer-mult-bounds/pull/236) | jamesyc | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#237](https://github.com/CrocSwap/integer-mult-bounds/pull/237) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#240](https://github.com/CrocSwap/integer-mult-bounds/pull/240) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 2](../../research/community-round9-audit/review-ledger.json) |
| [#241](https://github.com/CrocSwap/integer-mult-bounds/pull/241) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#242](https://github.com/CrocSwap/integer-mult-bounds/pull/242) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#243](https://github.com/CrocSwap/integer-mult-bounds/pull/243) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#244](https://github.com/CrocSwap/integer-mult-bounds/pull/244) | eumemic | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#245](https://github.com/CrocSwap/integer-mult-bounds/pull/245) | sandersdavid90-droid | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#248](https://github.com/CrocSwap/integer-mult-bounds/pull/248) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#249](https://github.com/CrocSwap/integer-mult-bounds/pull/249) | eumemic | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#250](https://github.com/CrocSwap/integer-mult-bounds/pull/250) | SovereignSteak | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#251](https://github.com/CrocSwap/integer-mult-bounds/pull/251) | eumemic | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#252](https://github.com/CrocSwap/integer-mult-bounds/pull/252) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#254](https://github.com/CrocSwap/integer-mult-bounds/pull/254) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#255](https://github.com/CrocSwap/integer-mult-bounds/pull/255) | hvaliconAI | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#256](https://github.com/CrocSwap/integer-mult-bounds/pull/256) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#258](https://github.com/CrocSwap/integer-mult-bounds/pull/258) | amanforindia | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#259](https://github.com/CrocSwap/integer-mult-bounds/pull/259) | Dugongue | partially reviewed | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#260](https://github.com/CrocSwap/integer-mult-bounds/pull/260) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#261](https://github.com/CrocSwap/integer-mult-bounds/pull/261) | sennemmi | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#262](https://github.com/CrocSwap/integer-mult-bounds/pull/262) | maxime-fleury | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#263](https://github.com/CrocSwap/integer-mult-bounds/pull/263) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#264](https://github.com/CrocSwap/integer-mult-bounds/pull/264) | dataisfire | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#265](https://github.com/CrocSwap/integer-mult-bounds/pull/265) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#266](https://github.com/CrocSwap/integer-mult-bounds/pull/266) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#267](https://github.com/CrocSwap/integer-mult-bounds/pull/267) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#268](https://github.com/CrocSwap/integer-mult-bounds/pull/268) | eumemic | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#269](https://github.com/CrocSwap/integer-mult-bounds/pull/269) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#270](https://github.com/CrocSwap/integer-mult-bounds/pull/270) | utcorvusvolat-dotcom | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#271](https://github.com/CrocSwap/integer-mult-bounds/pull/271) | evmckinney9 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#272](https://github.com/CrocSwap/integer-mult-bounds/pull/272) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#273](https://github.com/CrocSwap/integer-mult-bounds/pull/273) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#274](https://github.com/CrocSwap/integer-mult-bounds/pull/274) | shea256 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#275](https://github.com/CrocSwap/integer-mult-bounds/pull/275) | lydakis | partially reviewed | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#277](https://github.com/CrocSwap/integer-mult-bounds/pull/277) | hcg890 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#278](https://github.com/CrocSwap/integer-mult-bounds/pull/278) | hcg890 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#279](https://github.com/CrocSwap/integer-mult-bounds/pull/279) | rohanarun | incorporated | [record 1](../../docs/research/community-pr279-integration.json) · [record 2](../../research/community-batch970-audit/COMPANION-REVIEWS.json) · [record 3](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) · [record 4](../../research/pr-reconciliation-20261012/content-comparison.json) |
| [#280](https://github.com/CrocSwap/integer-mult-bounds/pull/280) | utcorvusvolat-dotcom | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#281](https://github.com/CrocSwap/integer-mult-bounds/pull/281) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#282](https://github.com/CrocSwap/integer-mult-bounds/pull/282) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#283](https://github.com/CrocSwap/integer-mult-bounds/pull/283) | Dugongue | partially reviewed | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#284](https://github.com/CrocSwap/integer-mult-bounds/pull/284) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#285](https://github.com/CrocSwap/integer-mult-bounds/pull/285) | DreamingOfClouds | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#286](https://github.com/CrocSwap/integer-mult-bounds/pull/286) | GamingPuzzled | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#287](https://github.com/CrocSwap/integer-mult-bounds/pull/287) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#288](https://github.com/CrocSwap/integer-mult-bounds/pull/288) | eumemic | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#289](https://github.com/CrocSwap/integer-mult-bounds/pull/289) | gupt1156 | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#290](https://github.com/CrocSwap/integer-mult-bounds/pull/290) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#291](https://github.com/CrocSwap/integer-mult-bounds/pull/291) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#292](https://github.com/CrocSwap/integer-mult-bounds/pull/292) | sannidhi-hemanth | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#293](https://github.com/CrocSwap/integer-mult-bounds/pull/293) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#294](https://github.com/CrocSwap/integer-mult-bounds/pull/294) | maximussthegreat | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#295](https://github.com/CrocSwap/integer-mult-bounds/pull/295) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#296](https://github.com/CrocSwap/integer-mult-bounds/pull/296) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#297](https://github.com/CrocSwap/integer-mult-bounds/pull/297) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#298](https://github.com/CrocSwap/integer-mult-bounds/pull/298) | M6LI | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#299](https://github.com/CrocSwap/integer-mult-bounds/pull/299) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#300](https://github.com/CrocSwap/integer-mult-bounds/pull/300) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#301](https://github.com/CrocSwap/integer-mult-bounds/pull/301) | maximussthegreat | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#302](https://github.com/CrocSwap/integer-mult-bounds/pull/302) | maximussthegreat | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#303](https://github.com/CrocSwap/integer-mult-bounds/pull/303) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-next100-audit/DISPOSITIONS.json) |
| [#304](https://github.com/CrocSwap/integer-mult-bounds/pull/304) | DreamingOfClouds | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#305](https://github.com/CrocSwap/integer-mult-bounds/pull/305) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#306](https://github.com/CrocSwap/integer-mult-bounds/pull/306) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#307](https://github.com/CrocSwap/integer-mult-bounds/pull/307) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#308](https://github.com/CrocSwap/integer-mult-bounds/pull/308) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#309](https://github.com/CrocSwap/integer-mult-bounds/pull/309) | Dugongue | partially reviewed | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#310](https://github.com/CrocSwap/integer-mult-bounds/pull/310) | utcorvusvolat-dotcom | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#311](https://github.com/CrocSwap/integer-mult-bounds/pull/311) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#312](https://github.com/CrocSwap/integer-mult-bounds/pull/312) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#313](https://github.com/CrocSwap/integer-mult-bounds/pull/313) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#314](https://github.com/CrocSwap/integer-mult-bounds/pull/314) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#315](https://github.com/CrocSwap/integer-mult-bounds/pull/315) | DreamingOfClouds | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#316](https://github.com/CrocSwap/integer-mult-bounds/pull/316) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#317](https://github.com/CrocSwap/integer-mult-bounds/pull/317) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#318](https://github.com/CrocSwap/integer-mult-bounds/pull/318) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#319](https://github.com/CrocSwap/integer-mult-bounds/pull/319) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#320](https://github.com/CrocSwap/integer-mult-bounds/pull/320) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#321](https://github.com/CrocSwap/integer-mult-bounds/pull/321) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#322](https://github.com/CrocSwap/integer-mult-bounds/pull/322) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#323](https://github.com/CrocSwap/integer-mult-bounds/pull/323) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#324](https://github.com/CrocSwap/integer-mult-bounds/pull/324) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#325](https://github.com/CrocSwap/integer-mult-bounds/pull/325) | DreamingOfClouds | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#327](https://github.com/CrocSwap/integer-mult-bounds/pull/327) | DreamingOfClouds | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#328](https://github.com/CrocSwap/integer-mult-bounds/pull/328) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#329](https://github.com/CrocSwap/integer-mult-bounds/pull/329) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#330](https://github.com/CrocSwap/integer-mult-bounds/pull/330) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#331](https://github.com/CrocSwap/integer-mult-bounds/pull/331) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#332](https://github.com/CrocSwap/integer-mult-bounds/pull/332) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#333](https://github.com/CrocSwap/integer-mult-bounds/pull/333) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#334](https://github.com/CrocSwap/integer-mult-bounds/pull/334) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#335](https://github.com/CrocSwap/integer-mult-bounds/pull/335) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#336](https://github.com/CrocSwap/integer-mult-bounds/pull/336) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#337](https://github.com/CrocSwap/integer-mult-bounds/pull/337) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#338](https://github.com/CrocSwap/integer-mult-bounds/pull/338) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#339](https://github.com/CrocSwap/integer-mult-bounds/pull/339) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#340](https://github.com/CrocSwap/integer-mult-bounds/pull/340) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#341](https://github.com/CrocSwap/integer-mult-bounds/pull/341) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#342](https://github.com/CrocSwap/integer-mult-bounds/pull/342) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#343](https://github.com/CrocSwap/integer-mult-bounds/pull/343) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#344](https://github.com/CrocSwap/integer-mult-bounds/pull/344) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#345](https://github.com/CrocSwap/integer-mult-bounds/pull/345) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#346](https://github.com/CrocSwap/integer-mult-bounds/pull/346) | LJH-217 | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#347](https://github.com/CrocSwap/integer-mult-bounds/pull/347) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#348](https://github.com/CrocSwap/integer-mult-bounds/pull/348) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#349](https://github.com/CrocSwap/integer-mult-bounds/pull/349) | erebos-labs | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#350](https://github.com/CrocSwap/integer-mult-bounds/pull/350) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#351](https://github.com/CrocSwap/integer-mult-bounds/pull/351) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#352](https://github.com/CrocSwap/integer-mult-bounds/pull/352) | DaysSky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#353](https://github.com/CrocSwap/integer-mult-bounds/pull/353) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#354](https://github.com/CrocSwap/integer-mult-bounds/pull/354) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#355](https://github.com/CrocSwap/integer-mult-bounds/pull/355) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#356](https://github.com/CrocSwap/integer-mult-bounds/pull/356) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#357](https://github.com/CrocSwap/integer-mult-bounds/pull/357) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#358](https://github.com/CrocSwap/integer-mult-bounds/pull/358) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#359](https://github.com/CrocSwap/integer-mult-bounds/pull/359) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#360](https://github.com/CrocSwap/integer-mult-bounds/pull/360) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#361](https://github.com/CrocSwap/integer-mult-bounds/pull/361) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#362](https://github.com/CrocSwap/integer-mult-bounds/pull/362) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#363](https://github.com/CrocSwap/integer-mult-bounds/pull/363) | DaysSky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#364](https://github.com/CrocSwap/integer-mult-bounds/pull/364) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#365](https://github.com/CrocSwap/integer-mult-bounds/pull/365) | aliromman | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#366](https://github.com/CrocSwap/integer-mult-bounds/pull/366) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#367](https://github.com/CrocSwap/integer-mult-bounds/pull/367) | amanforindia | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#368](https://github.com/CrocSwap/integer-mult-bounds/pull/368) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#369](https://github.com/CrocSwap/integer-mult-bounds/pull/369) | applecrusher | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#370](https://github.com/CrocSwap/integer-mult-bounds/pull/370) | utcorvusvolat-dotcom | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#371](https://github.com/CrocSwap/integer-mult-bounds/pull/371) | artuskg | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#372](https://github.com/CrocSwap/integer-mult-bounds/pull/372) | DesmondForward | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#373](https://github.com/CrocSwap/integer-mult-bounds/pull/373) | DaysSky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#374](https://github.com/CrocSwap/integer-mult-bounds/pull/374) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#375](https://github.com/CrocSwap/integer-mult-bounds/pull/375) | DaysSky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#376](https://github.com/CrocSwap/integer-mult-bounds/pull/376) | applecrusher | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#377](https://github.com/CrocSwap/integer-mult-bounds/pull/377) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#378](https://github.com/CrocSwap/integer-mult-bounds/pull/378) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#379](https://github.com/CrocSwap/integer-mult-bounds/pull/379) | eumemic | partially reviewed | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#380](https://github.com/CrocSwap/integer-mult-bounds/pull/380) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#381](https://github.com/CrocSwap/integer-mult-bounds/pull/381) | DaysSky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#382](https://github.com/CrocSwap/integer-mult-bounds/pull/382) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#383](https://github.com/CrocSwap/integer-mult-bounds/pull/383) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#384](https://github.com/CrocSwap/integer-mult-bounds/pull/384) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#385](https://github.com/CrocSwap/integer-mult-bounds/pull/385) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#386](https://github.com/CrocSwap/integer-mult-bounds/pull/386) | jacklightChen | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#387](https://github.com/CrocSwap/integer-mult-bounds/pull/387) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#388](https://github.com/CrocSwap/integer-mult-bounds/pull/388) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#389](https://github.com/CrocSwap/integer-mult-bounds/pull/389) | ai-nanachi | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#390](https://github.com/CrocSwap/integer-mult-bounds/pull/390) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#391](https://github.com/CrocSwap/integer-mult-bounds/pull/391) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#392](https://github.com/CrocSwap/integer-mult-bounds/pull/392) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#394](https://github.com/CrocSwap/integer-mult-bounds/pull/394) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#395](https://github.com/CrocSwap/integer-mult-bounds/pull/395) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#396](https://github.com/CrocSwap/integer-mult-bounds/pull/396) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#397](https://github.com/CrocSwap/integer-mult-bounds/pull/397) | artuskg | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#398](https://github.com/CrocSwap/integer-mult-bounds/pull/398) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#399](https://github.com/CrocSwap/integer-mult-bounds/pull/399) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#400](https://github.com/CrocSwap/integer-mult-bounds/pull/400) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#401](https://github.com/CrocSwap/integer-mult-bounds/pull/401) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#402](https://github.com/CrocSwap/integer-mult-bounds/pull/402) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#403](https://github.com/CrocSwap/integer-mult-bounds/pull/403) | rohanarun | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#404](https://github.com/CrocSwap/integer-mult-bounds/pull/404) | Dugongue | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#405](https://github.com/CrocSwap/integer-mult-bounds/pull/405) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#406](https://github.com/CrocSwap/integer-mult-bounds/pull/406) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#407](https://github.com/CrocSwap/integer-mult-bounds/pull/407) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#408](https://github.com/CrocSwap/integer-mult-bounds/pull/408) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#409](https://github.com/CrocSwap/integer-mult-bounds/pull/409) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#410](https://github.com/CrocSwap/integer-mult-bounds/pull/410) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#411](https://github.com/CrocSwap/integer-mult-bounds/pull/411) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#412](https://github.com/CrocSwap/integer-mult-bounds/pull/412) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#413](https://github.com/CrocSwap/integer-mult-bounds/pull/413) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#414](https://github.com/CrocSwap/integer-mult-bounds/pull/414) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#415](https://github.com/CrocSwap/integer-mult-bounds/pull/415) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#416](https://github.com/CrocSwap/integer-mult-bounds/pull/416) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#417](https://github.com/CrocSwap/integer-mult-bounds/pull/417) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#418](https://github.com/CrocSwap/integer-mult-bounds/pull/418) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#419](https://github.com/CrocSwap/integer-mult-bounds/pull/419) | chafreaky | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#420](https://github.com/CrocSwap/integer-mult-bounds/pull/420) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#421](https://github.com/CrocSwap/integer-mult-bounds/pull/421) | eumemic | incorporated | [record 1](../../research/community-reconciliation-third100-audit/DISPOSITIONS.json) |
| [#422](https://github.com/CrocSwap/integer-mult-bounds/pull/422) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#423](https://github.com/CrocSwap/integer-mult-bounds/pull/423) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#424](https://github.com/CrocSwap/integer-mult-bounds/pull/424) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#425](https://github.com/CrocSwap/integer-mult-bounds/pull/425) | jacklightChen | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#426](https://github.com/CrocSwap/integer-mult-bounds/pull/426) | ai-nanachi | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#427](https://github.com/CrocSwap/integer-mult-bounds/pull/427) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#428](https://github.com/CrocSwap/integer-mult-bounds/pull/428) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#429](https://github.com/CrocSwap/integer-mult-bounds/pull/429) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#430](https://github.com/CrocSwap/integer-mult-bounds/pull/430) | artuskg | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#431](https://github.com/CrocSwap/integer-mult-bounds/pull/431) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#432](https://github.com/CrocSwap/integer-mult-bounds/pull/432) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#433](https://github.com/CrocSwap/integer-mult-bounds/pull/433) | icekylinx | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#434](https://github.com/CrocSwap/integer-mult-bounds/pull/434) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#435](https://github.com/CrocSwap/integer-mult-bounds/pull/435) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#436](https://github.com/CrocSwap/integer-mult-bounds/pull/436) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#437](https://github.com/CrocSwap/integer-mult-bounds/pull/437) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#438](https://github.com/CrocSwap/integer-mult-bounds/pull/438) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#439](https://github.com/CrocSwap/integer-mult-bounds/pull/439) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#440](https://github.com/CrocSwap/integer-mult-bounds/pull/440) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#441](https://github.com/CrocSwap/integer-mult-bounds/pull/441) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#442](https://github.com/CrocSwap/integer-mult-bounds/pull/442) | DaysSky | incorporated | [record 1](../../docs/research/community-formal-20261012-integration.json) · [record 2](../../docs/research/community-formal-20261012-review.md) |
| [#443](https://github.com/CrocSwap/integer-mult-bounds/pull/443) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#444](https://github.com/CrocSwap/integer-mult-bounds/pull/444) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#445](https://github.com/CrocSwap/integer-mult-bounds/pull/445) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#446](https://github.com/CrocSwap/integer-mult-bounds/pull/446) | DreamingOfClouds | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#447](https://github.com/CrocSwap/integer-mult-bounds/pull/447) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#448](https://github.com/CrocSwap/integer-mult-bounds/pull/448) | higherbeing | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#450](https://github.com/CrocSwap/integer-mult-bounds/pull/450) | DreamingOfClouds | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#451](https://github.com/CrocSwap/integer-mult-bounds/pull/451) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#452](https://github.com/CrocSwap/integer-mult-bounds/pull/452) | amanforindia | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#453](https://github.com/CrocSwap/integer-mult-bounds/pull/453) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#454](https://github.com/CrocSwap/integer-mult-bounds/pull/454) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#455](https://github.com/CrocSwap/integer-mult-bounds/pull/455) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#456](https://github.com/CrocSwap/integer-mult-bounds/pull/456) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#457](https://github.com/CrocSwap/integer-mult-bounds/pull/457) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#458](https://github.com/CrocSwap/integer-mult-bounds/pull/458) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#459](https://github.com/CrocSwap/integer-mult-bounds/pull/459) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#460](https://github.com/CrocSwap/integer-mult-bounds/pull/460) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#461](https://github.com/CrocSwap/integer-mult-bounds/pull/461) | Srikrishnabalaji | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#462](https://github.com/CrocSwap/integer-mult-bounds/pull/462) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#463](https://github.com/CrocSwap/integer-mult-bounds/pull/463) | DreamingOfClouds | partially reviewed | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#464](https://github.com/CrocSwap/integer-mult-bounds/pull/464) | ahrazzle | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#465](https://github.com/CrocSwap/integer-mult-bounds/pull/465) | Srikrishnabalaji | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#466](https://github.com/CrocSwap/integer-mult-bounds/pull/466) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#467](https://github.com/CrocSwap/integer-mult-bounds/pull/467) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#469](https://github.com/CrocSwap/integer-mult-bounds/pull/469) | ahrazzle | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#470](https://github.com/CrocSwap/integer-mult-bounds/pull/470) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#471](https://github.com/CrocSwap/integer-mult-bounds/pull/471) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#472](https://github.com/CrocSwap/integer-mult-bounds/pull/472) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#473](https://github.com/CrocSwap/integer-mult-bounds/pull/473) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#474](https://github.com/CrocSwap/integer-mult-bounds/pull/474) | artuskg | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#475](https://github.com/CrocSwap/integer-mult-bounds/pull/475) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#476](https://github.com/CrocSwap/integer-mult-bounds/pull/476) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#478](https://github.com/CrocSwap/integer-mult-bounds/pull/478) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#479](https://github.com/CrocSwap/integer-mult-bounds/pull/479) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#480](https://github.com/CrocSwap/integer-mult-bounds/pull/480) | higherbeing | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#481](https://github.com/CrocSwap/integer-mult-bounds/pull/481) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#482](https://github.com/CrocSwap/integer-mult-bounds/pull/482) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#483](https://github.com/CrocSwap/integer-mult-bounds/pull/483) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#484](https://github.com/CrocSwap/integer-mult-bounds/pull/484) | DreamingOfClouds | incorporated | [record 1](../../docs/research/community-formal-20261012-integration.json) · [record 2](../../docs/research/community-formal-20261012-review.md) |
| [#485](https://github.com/CrocSwap/integer-mult-bounds/pull/485) | DreamingOfClouds | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#486](https://github.com/CrocSwap/integer-mult-bounds/pull/486) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#487](https://github.com/CrocSwap/integer-mult-bounds/pull/487) | jamesyc | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#488](https://github.com/CrocSwap/integer-mult-bounds/pull/488) | jamesyc | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#489](https://github.com/CrocSwap/integer-mult-bounds/pull/489) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#490](https://github.com/CrocSwap/integer-mult-bounds/pull/490) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#491](https://github.com/CrocSwap/integer-mult-bounds/pull/491) | M6LI | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#492](https://github.com/CrocSwap/integer-mult-bounds/pull/492) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#494](https://github.com/CrocSwap/integer-mult-bounds/pull/494) | higherbeing | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#495](https://github.com/CrocSwap/integer-mult-bounds/pull/495) | aliromman | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#496](https://github.com/CrocSwap/integer-mult-bounds/pull/496) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#497](https://github.com/CrocSwap/integer-mult-bounds/pull/497) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#498](https://github.com/CrocSwap/integer-mult-bounds/pull/498) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#499](https://github.com/CrocSwap/integer-mult-bounds/pull/499) | rosswaycaster | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#500](https://github.com/CrocSwap/integer-mult-bounds/pull/500) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#501](https://github.com/CrocSwap/integer-mult-bounds/pull/501) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#502](https://github.com/CrocSwap/integer-mult-bounds/pull/502) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#503](https://github.com/CrocSwap/integer-mult-bounds/pull/503) | DreamingOfClouds | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#504](https://github.com/CrocSwap/integer-mult-bounds/pull/504) | DreamingOfClouds | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#505](https://github.com/CrocSwap/integer-mult-bounds/pull/505) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#506](https://github.com/CrocSwap/integer-mult-bounds/pull/506) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#507](https://github.com/CrocSwap/integer-mult-bounds/pull/507) | eumemic | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#508](https://github.com/CrocSwap/integer-mult-bounds/pull/508) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#509](https://github.com/CrocSwap/integer-mult-bounds/pull/509) | DreamingOfClouds | incorporated | [record 1](../../docs/research/community-formal-20261012-integration.json) · [record 2](../../docs/research/community-formal-20261012-review.md) |
| [#510](https://github.com/CrocSwap/integer-mult-bounds/pull/510) | DreamingOfClouds | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#511](https://github.com/CrocSwap/integer-mult-bounds/pull/511) | jamesyc | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#512](https://github.com/CrocSwap/integer-mult-bounds/pull/512) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#513](https://github.com/CrocSwap/integer-mult-bounds/pull/513) | jamesyc | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#515](https://github.com/CrocSwap/integer-mult-bounds/pull/515) | DreamingOfClouds | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#516](https://github.com/CrocSwap/integer-mult-bounds/pull/516) | DreamingOfClouds | incorporated | [record 1](../../docs/research/community-formal-20261012-integration.json) · [record 2](../../docs/research/community-formal-20261012-review.md) |
| [#517](https://github.com/CrocSwap/integer-mult-bounds/pull/517) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#518](https://github.com/CrocSwap/integer-mult-bounds/pull/518) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#519](https://github.com/CrocSwap/integer-mult-bounds/pull/519) | jamesyc | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#520](https://github.com/CrocSwap/integer-mult-bounds/pull/520) | higherbeing | incorporated | [record 1](../../docs/research/community-formal-20261012-integration.json) · [record 2](../../docs/research/community-formal-20261012-review.md) |
| [#521](https://github.com/CrocSwap/integer-mult-bounds/pull/521) | applecrusher | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#522](https://github.com/CrocSwap/integer-mult-bounds/pull/522) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#525](https://github.com/CrocSwap/integer-mult-bounds/pull/525) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#526](https://github.com/CrocSwap/integer-mult-bounds/pull/526) | jamesyc | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#527](https://github.com/CrocSwap/integer-mult-bounds/pull/527) | rohanarun | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#528](https://github.com/CrocSwap/integer-mult-bounds/pull/528) | jamesyc | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#529](https://github.com/CrocSwap/integer-mult-bounds/pull/529) | chafreaky | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#530](https://github.com/CrocSwap/integer-mult-bounds/pull/530) | jamesyc | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#532](https://github.com/CrocSwap/integer-mult-bounds/pull/532) | Dugongue | unreviewed | No exact-head review established; inspect contribution and dependencies. |
| [#533](https://github.com/CrocSwap/integer-mult-bounds/pull/533) | chafreaky | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#534](https://github.com/CrocSwap/integer-mult-bounds/pull/534) | rohanarun | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#535](https://github.com/CrocSwap/integer-mult-bounds/pull/535) | icekylinx | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#536](https://github.com/CrocSwap/integer-mult-bounds/pull/536) | rohanarun | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#537](https://github.com/CrocSwap/integer-mult-bounds/pull/537) | Dugongue | incorporated | [record 1](../../research/community-family533-audit/DISPOSITIONS.json) |
| [#538](https://github.com/CrocSwap/integer-mult-bounds/pull/538) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#539](https://github.com/CrocSwap/integer-mult-bounds/pull/539) | rohanarun | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#541](https://github.com/CrocSwap/integer-mult-bounds/pull/541) | Dugongue | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#542](https://github.com/CrocSwap/integer-mult-bounds/pull/542) | rohanarun | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#543](https://github.com/CrocSwap/integer-mult-bounds/pull/543) | eumemic | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#544](https://github.com/CrocSwap/integer-mult-bounds/pull/544) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#545](https://github.com/CrocSwap/integer-mult-bounds/pull/545) | DreamingOfClouds | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#546](https://github.com/CrocSwap/integer-mult-bounds/pull/546) | rohanarun | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#547](https://github.com/CrocSwap/integer-mult-bounds/pull/547) | rohanarun | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#548](https://github.com/CrocSwap/integer-mult-bounds/pull/548) | Dugongue | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#549](https://github.com/CrocSwap/integer-mult-bounds/pull/549) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#550](https://github.com/CrocSwap/integer-mult-bounds/pull/550) | eumemic | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#551](https://github.com/CrocSwap/integer-mult-bounds/pull/551) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#552](https://github.com/CrocSwap/integer-mult-bounds/pull/552) | Dugongue | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#554](https://github.com/CrocSwap/integer-mult-bounds/pull/554) | rohanarun | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#555](https://github.com/CrocSwap/integer-mult-bounds/pull/555) | eumemic | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#556](https://github.com/CrocSwap/integer-mult-bounds/pull/556) | Dugongue | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#557](https://github.com/CrocSwap/integer-mult-bounds/pull/557) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#558](https://github.com/CrocSwap/integer-mult-bounds/pull/558) | eumemic | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#559](https://github.com/CrocSwap/integer-mult-bounds/pull/559) | rohanarun | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#560](https://github.com/CrocSwap/integer-mult-bounds/pull/560) | Dugongue | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#561](https://github.com/CrocSwap/integer-mult-bounds/pull/561) | eumemic | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#562](https://github.com/CrocSwap/integer-mult-bounds/pull/562) | eumemic | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#563](https://github.com/CrocSwap/integer-mult-bounds/pull/563) | Dugongue | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#564](https://github.com/CrocSwap/integer-mult-bounds/pull/564) | eumemic | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#567](https://github.com/CrocSwap/integer-mult-bounds/pull/567) | jon314159 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#568](https://github.com/CrocSwap/integer-mult-bounds/pull/568) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#569](https://github.com/CrocSwap/integer-mult-bounds/pull/569) | DominikScholz | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#571](https://github.com/CrocSwap/integer-mult-bounds/pull/571) | DominikScholz | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#572](https://github.com/CrocSwap/integer-mult-bounds/pull/572) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#574](https://github.com/CrocSwap/integer-mult-bounds/pull/574) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#575](https://github.com/CrocSwap/integer-mult-bounds/pull/575) | jon314159 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#576](https://github.com/CrocSwap/integer-mult-bounds/pull/576) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#577](https://github.com/CrocSwap/integer-mult-bounds/pull/577) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#578](https://github.com/CrocSwap/integer-mult-bounds/pull/578) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#579](https://github.com/CrocSwap/integer-mult-bounds/pull/579) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#580](https://github.com/CrocSwap/integer-mult-bounds/pull/580) | artuskg | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#582](https://github.com/CrocSwap/integer-mult-bounds/pull/582) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#583](https://github.com/CrocSwap/integer-mult-bounds/pull/583) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#584](https://github.com/CrocSwap/integer-mult-bounds/pull/584) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#586](https://github.com/CrocSwap/integer-mult-bounds/pull/586) | chafreaky | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#587](https://github.com/CrocSwap/integer-mult-bounds/pull/587) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#588](https://github.com/CrocSwap/integer-mult-bounds/pull/588) | jeremykothe2 | incorporated | [record 1](../../research/community-family588-audit/DISPOSITIONS.json) |
| [#589](https://github.com/CrocSwap/integer-mult-bounds/pull/589) | DreamingOfClouds | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#591](https://github.com/CrocSwap/integer-mult-bounds/pull/591) | jeremykothe2 | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#592](https://github.com/CrocSwap/integer-mult-bounds/pull/592) | jeremykothe2 | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#593](https://github.com/CrocSwap/integer-mult-bounds/pull/593) | jeremykothe2 | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#594](https://github.com/CrocSwap/integer-mult-bounds/pull/594) | eumemic | partially reviewed | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#595](https://github.com/CrocSwap/integer-mult-bounds/pull/595) | DreamingOfClouds | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#596](https://github.com/CrocSwap/integer-mult-bounds/pull/596) | jeremykothe2 | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#598](https://github.com/CrocSwap/integer-mult-bounds/pull/598) | DominikScholz | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#599](https://github.com/CrocSwap/integer-mult-bounds/pull/599) | DreamingOfClouds | incorporated | [record 1](../../research/community-hyperplane599-audit/DISPOSITIONS.json) |
| [#600](https://github.com/CrocSwap/integer-mult-bounds/pull/600) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#601](https://github.com/CrocSwap/integer-mult-bounds/pull/601) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#602](https://github.com/CrocSwap/integer-mult-bounds/pull/602) | artuskg | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#603](https://github.com/CrocSwap/integer-mult-bounds/pull/603) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#604](https://github.com/CrocSwap/integer-mult-bounds/pull/604) | DreamingOfClouds | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#605](https://github.com/CrocSwap/integer-mult-bounds/pull/605) | jamesyc | partially reviewed | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#606](https://github.com/CrocSwap/integer-mult-bounds/pull/606) | DominikScholz | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#607](https://github.com/CrocSwap/integer-mult-bounds/pull/607) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#608](https://github.com/CrocSwap/integer-mult-bounds/pull/608) | higherbeing | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#609](https://github.com/CrocSwap/integer-mult-bounds/pull/609) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#610](https://github.com/CrocSwap/integer-mult-bounds/pull/610) | DreamingOfClouds | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#611](https://github.com/CrocSwap/integer-mult-bounds/pull/611) | eumemic | partially reviewed | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#612](https://github.com/CrocSwap/integer-mult-bounds/pull/612) | jamesyc | partially reviewed | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#613](https://github.com/CrocSwap/integer-mult-bounds/pull/613) | eumemic | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#614](https://github.com/CrocSwap/integer-mult-bounds/pull/614) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#615](https://github.com/CrocSwap/integer-mult-bounds/pull/615) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#616](https://github.com/CrocSwap/integer-mult-bounds/pull/616) | chafreaky | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#617](https://github.com/CrocSwap/integer-mult-bounds/pull/617) | jeremykothe2 | incorporated | [record 1](../../research/community-cold617-audit/DISPOSITIONS.json) |
| [#618](https://github.com/CrocSwap/integer-mult-bounds/pull/618) | jeremydiviney | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#619](https://github.com/CrocSwap/integer-mult-bounds/pull/619) | chafreaky | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#620](https://github.com/CrocSwap/integer-mult-bounds/pull/620) | GamingPuzzled | partially reviewed | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#621](https://github.com/CrocSwap/integer-mult-bounds/pull/621) | aliromman | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#622](https://github.com/CrocSwap/integer-mult-bounds/pull/622) | jeremykothe2 | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#623](https://github.com/CrocSwap/integer-mult-bounds/pull/623) | jeremykothe2 | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#624](https://github.com/CrocSwap/integer-mult-bounds/pull/624) | jeremydiviney | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#625](https://github.com/CrocSwap/integer-mult-bounds/pull/625) | jeremykothe2 | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#626](https://github.com/CrocSwap/integer-mult-bounds/pull/626) | chafreaky | incorporated | [record 1](../../research/community-k492-audit/DISPOSITIONS.json) |
| [#662](https://github.com/CrocSwap/integer-mult-bounds/pull/662) | cbethin | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#675](https://github.com/CrocSwap/integer-mult-bounds/pull/675) | tekuuu | incorporated | [record 1](../../research/community-frontier741-audit/DISPOSITIONS.json) |
| [#681](https://github.com/CrocSwap/integer-mult-bounds/pull/681) | alluri-ritual | incorporated | [record 1](../../research/community-frontier741-audit/DISPOSITIONS.json) |
| [#688](https://github.com/CrocSwap/integer-mult-bounds/pull/688) | aliromman | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#691](https://github.com/CrocSwap/integer-mult-bounds/pull/691) | mtpsl | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#694](https://github.com/CrocSwap/integer-mult-bounds/pull/694) | g-guthrie | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#695](https://github.com/CrocSwap/integer-mult-bounds/pull/695) | jsnider3 | incorporated | [record 1](../../research/community-frontier741-audit/DISPOSITIONS.json) |
| [#696](https://github.com/CrocSwap/integer-mult-bounds/pull/696) | thakrarsagar | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#704](https://github.com/CrocSwap/integer-mult-bounds/pull/704) | roife | incorporated | [record 1](../../research/community-frontier741-audit/DISPOSITIONS.json) |
| [#707](https://github.com/CrocSwap/integer-mult-bounds/pull/707) | cbethin | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#708](https://github.com/CrocSwap/integer-mult-bounds/pull/708) | thakrarsagar | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#709](https://github.com/CrocSwap/integer-mult-bounds/pull/709) | mtpsl | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#713](https://github.com/CrocSwap/integer-mult-bounds/pull/713) | swbiggart | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#721](https://github.com/CrocSwap/integer-mult-bounds/pull/721) | cxnmai | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#727](https://github.com/CrocSwap/integer-mult-bounds/pull/727) | TMM2009 | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#740](https://github.com/CrocSwap/integer-mult-bounds/pull/740) | azide0x37 | incorporated | [record 1](../../research/community-frontier741-audit/DISPOSITIONS.json) |
| [#741](https://github.com/CrocSwap/integer-mult-bounds/pull/741) | chafreaky | incorporated | [record 1](../../research/community-frontier741-audit/DISPOSITIONS.json) |
| [#772](https://github.com/CrocSwap/integer-mult-bounds/pull/772) | ellipsi2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#777](https://github.com/CrocSwap/integer-mult-bounds/pull/777) | tekuuu | incorporated | [record 1](../../research/community-frontier741-audit/DISPOSITIONS.json) · [record 2](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#795](https://github.com/CrocSwap/integer-mult-bounds/pull/795) | chafreaky | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#799](https://github.com/CrocSwap/integer-mult-bounds/pull/799) | jeremykothe2 | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#806](https://github.com/CrocSwap/integer-mult-bounds/pull/806) | Rohansguliani | incorporated | [record 1](../../research/community-frontier799-audit/DISPOSITIONS.json) |
| [#812](https://github.com/CrocSwap/integer-mult-bounds/pull/812) | ljste | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#813](https://github.com/CrocSwap/integer-mult-bounds/pull/813) | bitplane | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#816](https://github.com/CrocSwap/integer-mult-bounds/pull/816) | dd-hemant | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#818](https://github.com/CrocSwap/integer-mult-bounds/pull/818) | MrPink604 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#819](https://github.com/CrocSwap/integer-mult-bounds/pull/819) | MrPink604 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#828](https://github.com/CrocSwap/integer-mult-bounds/pull/828) | mihir-s-05 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#834](https://github.com/CrocSwap/integer-mult-bounds/pull/834) | chinmayarvind23 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#837](https://github.com/CrocSwap/integer-mult-bounds/pull/837) | bitplane | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#838](https://github.com/CrocSwap/integer-mult-bounds/pull/838) | ljste | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#839](https://github.com/CrocSwap/integer-mult-bounds/pull/839) | faw01 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#841](https://github.com/CrocSwap/integer-mult-bounds/pull/841) | mihir-s-05 | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#845](https://github.com/CrocSwap/integer-mult-bounds/pull/845) | mihir-s-05 | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#847](https://github.com/CrocSwap/integer-mult-bounds/pull/847) | chinmayarvind23 | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#848](https://github.com/CrocSwap/integer-mult-bounds/pull/848) | navinor | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#849](https://github.com/CrocSwap/integer-mult-bounds/pull/849) | bitplane | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#850](https://github.com/CrocSwap/integer-mult-bounds/pull/850) | cbethin | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#851](https://github.com/CrocSwap/integer-mult-bounds/pull/851) | AdemVessell | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#853](https://github.com/CrocSwap/integer-mult-bounds/pull/853) | navinor | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#856](https://github.com/CrocSwap/integer-mult-bounds/pull/856) | chinmayarvind23 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#857](https://github.com/CrocSwap/integer-mult-bounds/pull/857) | zeusinsight | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#862](https://github.com/CrocSwap/integer-mult-bounds/pull/862) | chafreaky | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#864](https://github.com/CrocSwap/integer-mult-bounds/pull/864) | navinor | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#865](https://github.com/CrocSwap/integer-mult-bounds/pull/865) | nightangelflowerwin-ops | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#866](https://github.com/CrocSwap/integer-mult-bounds/pull/866) | bitplane | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#867](https://github.com/CrocSwap/integer-mult-bounds/pull/867) | navinor | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#869](https://github.com/CrocSwap/integer-mult-bounds/pull/869) | jeremykothe2 | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#870](https://github.com/CrocSwap/integer-mult-bounds/pull/870) | jeremykothe2 | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#873](https://github.com/CrocSwap/integer-mult-bounds/pull/873) | navinor | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#874](https://github.com/CrocSwap/integer-mult-bounds/pull/874) | AmnonTamsut | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#875](https://github.com/CrocSwap/integer-mult-bounds/pull/875) | mightyOil | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#877](https://github.com/CrocSwap/integer-mult-bounds/pull/877) | bitplane | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#879](https://github.com/CrocSwap/integer-mult-bounds/pull/879) | mightyOil | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#880](https://github.com/CrocSwap/integer-mult-bounds/pull/880) | Deftsalt-debug | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#881](https://github.com/CrocSwap/integer-mult-bounds/pull/881) | SethBurkart123 | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#882](https://github.com/CrocSwap/integer-mult-bounds/pull/882) | mightyOil | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#883](https://github.com/CrocSwap/integer-mult-bounds/pull/883) | mightyOil | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#884](https://github.com/CrocSwap/integer-mult-bounds/pull/884) | martinxxx9 | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#886](https://github.com/CrocSwap/integer-mult-bounds/pull/886) | SethBurkart123 | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#887](https://github.com/CrocSwap/integer-mult-bounds/pull/887) | bitplane | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#890](https://github.com/CrocSwap/integer-mult-bounds/pull/890) | chafreaky | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#891](https://github.com/CrocSwap/integer-mult-bounds/pull/891) | navinor | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#893](https://github.com/CrocSwap/integer-mult-bounds/pull/893) | WeberChen8128 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#894](https://github.com/CrocSwap/integer-mult-bounds/pull/894) | navinor | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#896](https://github.com/CrocSwap/integer-mult-bounds/pull/896) | bitplane | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#900](https://github.com/CrocSwap/integer-mult-bounds/pull/900) | ToikY | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#901](https://github.com/CrocSwap/integer-mult-bounds/pull/901) | ToikY | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#903](https://github.com/CrocSwap/integer-mult-bounds/pull/903) | just-mn | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#904](https://github.com/CrocSwap/integer-mult-bounds/pull/904) | bitplane | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#905](https://github.com/CrocSwap/integer-mult-bounds/pull/905) | chafreaky | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#906](https://github.com/CrocSwap/integer-mult-bounds/pull/906) | CubeJerry | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#908](https://github.com/CrocSwap/integer-mult-bounds/pull/908) | RossRichardson | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#909](https://github.com/CrocSwap/integer-mult-bounds/pull/909) | ToikY | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#910](https://github.com/CrocSwap/integer-mult-bounds/pull/910) | navinor | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#911](https://github.com/CrocSwap/integer-mult-bounds/pull/911) | ToikY | incorporated | [record 1](../../research/community-frontier890-audit/DISPOSITIONS.json) |
| [#914](https://github.com/CrocSwap/integer-mult-bounds/pull/914) | RossRichardson | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#915](https://github.com/CrocSwap/integer-mult-bounds/pull/915) | bitplane | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#916](https://github.com/CrocSwap/integer-mult-bounds/pull/916) | nightangelflowerwin-ops | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#917](https://github.com/CrocSwap/integer-mult-bounds/pull/917) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#919](https://github.com/CrocSwap/integer-mult-bounds/pull/919) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#920](https://github.com/CrocSwap/integer-mult-bounds/pull/920) | ArnavSwiggy | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#921](https://github.com/CrocSwap/integer-mult-bounds/pull/921) | navinor | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#923](https://github.com/CrocSwap/integer-mult-bounds/pull/923) | RossRichardson | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#925](https://github.com/CrocSwap/integer-mult-bounds/pull/925) | RossRichardson | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#926](https://github.com/CrocSwap/integer-mult-bounds/pull/926) | bitplane | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#929](https://github.com/CrocSwap/integer-mult-bounds/pull/929) | chafreaky | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#930](https://github.com/CrocSwap/integer-mult-bounds/pull/930) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#932](https://github.com/CrocSwap/integer-mult-bounds/pull/932) | RossRichardson | incorporated | [record 1](../../research/community-batch932-audit/DISPOSITIONS.json) |
| [#934](https://github.com/CrocSwap/integer-mult-bounds/pull/934) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#936](https://github.com/CrocSwap/integer-mult-bounds/pull/936) | RossRichardson | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#937](https://github.com/CrocSwap/integer-mult-bounds/pull/937) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#939](https://github.com/CrocSwap/integer-mult-bounds/pull/939) | RossRichardson | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#941](https://github.com/CrocSwap/integer-mult-bounds/pull/941) | bitplane | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#942](https://github.com/CrocSwap/integer-mult-bounds/pull/942) | jon314159 | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#943](https://github.com/CrocSwap/integer-mult-bounds/pull/943) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#944](https://github.com/CrocSwap/integer-mult-bounds/pull/944) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#945](https://github.com/CrocSwap/integer-mult-bounds/pull/945) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#946](https://github.com/CrocSwap/integer-mult-bounds/pull/946) | navinor | partially reviewed | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) · [record 2](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#947](https://github.com/CrocSwap/integer-mult-bounds/pull/947) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#949](https://github.com/CrocSwap/integer-mult-bounds/pull/949) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#950](https://github.com/CrocSwap/integer-mult-bounds/pull/950) | RossRichardson | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#951](https://github.com/CrocSwap/integer-mult-bounds/pull/951) | chafreaky | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#952](https://github.com/CrocSwap/integer-mult-bounds/pull/952) | bitplane | incorporated | [record 1](../../research/community-batch952-audit/DISPOSITIONS.json) |
| [#953](https://github.com/CrocSwap/integer-mult-bounds/pull/953) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#954](https://github.com/CrocSwap/integer-mult-bounds/pull/954) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#957](https://github.com/CrocSwap/integer-mult-bounds/pull/957) | navinor | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#958](https://github.com/CrocSwap/integer-mult-bounds/pull/958) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#959](https://github.com/CrocSwap/integer-mult-bounds/pull/959) | yssite | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#960](https://github.com/CrocSwap/integer-mult-bounds/pull/960) | davidNbreslauer | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#961](https://github.com/CrocSwap/integer-mult-bounds/pull/961) | woklerx | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#963](https://github.com/CrocSwap/integer-mult-bounds/pull/963) | ToikY | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#964](https://github.com/CrocSwap/integer-mult-bounds/pull/964) | bitplane | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#965](https://github.com/CrocSwap/integer-mult-bounds/pull/965) | RossRichardson | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#966](https://github.com/CrocSwap/integer-mult-bounds/pull/966) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#967](https://github.com/CrocSwap/integer-mult-bounds/pull/967) | theon199 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#968](https://github.com/CrocSwap/integer-mult-bounds/pull/968) | themilkman216 | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#969](https://github.com/CrocSwap/integer-mult-bounds/pull/969) | ToikY | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#970](https://github.com/CrocSwap/integer-mult-bounds/pull/970) | woklerx | incorporated | [record 1](../../research/community-batch970-audit/DISPOSITIONS.json) |
| [#971](https://github.com/CrocSwap/integer-mult-bounds/pull/971) | ToikY | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#972](https://github.com/CrocSwap/integer-mult-bounds/pull/972) | ToikY | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#973](https://github.com/CrocSwap/integer-mult-bounds/pull/973) | 1337isnot1337 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#976](https://github.com/CrocSwap/integer-mult-bounds/pull/976) | martinxxx9 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#979](https://github.com/CrocSwap/integer-mult-bounds/pull/979) | DLamdata | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#980](https://github.com/CrocSwap/integer-mult-bounds/pull/980) | bitplane | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#986](https://github.com/CrocSwap/integer-mult-bounds/pull/986) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#987](https://github.com/CrocSwap/integer-mult-bounds/pull/987) | rohanarun | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#988](https://github.com/CrocSwap/integer-mult-bounds/pull/988) | ToikY | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#989](https://github.com/CrocSwap/integer-mult-bounds/pull/989) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#991](https://github.com/CrocSwap/integer-mult-bounds/pull/991) | tekuuu | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#992](https://github.com/CrocSwap/integer-mult-bounds/pull/992) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#994](https://github.com/CrocSwap/integer-mult-bounds/pull/994) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#995](https://github.com/CrocSwap/integer-mult-bounds/pull/995) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#998](https://github.com/CrocSwap/integer-mult-bounds/pull/998) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1000](https://github.com/CrocSwap/integer-mult-bounds/pull/1000) | ToikY | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1001](https://github.com/CrocSwap/integer-mult-bounds/pull/1001) | ToikY | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1002](https://github.com/CrocSwap/integer-mult-bounds/pull/1002) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1003](https://github.com/CrocSwap/integer-mult-bounds/pull/1003) | ToikY | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1004](https://github.com/CrocSwap/integer-mult-bounds/pull/1004) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1005](https://github.com/CrocSwap/integer-mult-bounds/pull/1005) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1006](https://github.com/CrocSwap/integer-mult-bounds/pull/1006) | bitplane | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1008](https://github.com/CrocSwap/integer-mult-bounds/pull/1008) | woklerx | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1009](https://github.com/CrocSwap/integer-mult-bounds/pull/1009) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1010](https://github.com/CrocSwap/integer-mult-bounds/pull/1010) | cbethin | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1016](https://github.com/CrocSwap/integer-mult-bounds/pull/1016) | ToikY | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1017](https://github.com/CrocSwap/integer-mult-bounds/pull/1017) | woklerx | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1018](https://github.com/CrocSwap/integer-mult-bounds/pull/1018) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1019](https://github.com/CrocSwap/integer-mult-bounds/pull/1019) | 1337isnot1337 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1020](https://github.com/CrocSwap/integer-mult-bounds/pull/1020) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1022](https://github.com/CrocSwap/integer-mult-bounds/pull/1022) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1023](https://github.com/CrocSwap/integer-mult-bounds/pull/1023) | thakrarsagar | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1027](https://github.com/CrocSwap/integer-mult-bounds/pull/1027) | bbMisk | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1028](https://github.com/CrocSwap/integer-mult-bounds/pull/1028) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1029](https://github.com/CrocSwap/integer-mult-bounds/pull/1029) | aliromman | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1030](https://github.com/CrocSwap/integer-mult-bounds/pull/1030) | AlexS-scale | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1031](https://github.com/CrocSwap/integer-mult-bounds/pull/1031) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1034](https://github.com/CrocSwap/integer-mult-bounds/pull/1034) | aliromman | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1035](https://github.com/CrocSwap/integer-mult-bounds/pull/1035) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1040](https://github.com/CrocSwap/integer-mult-bounds/pull/1040) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1041](https://github.com/CrocSwap/integer-mult-bounds/pull/1041) | thakrarsagar | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1042](https://github.com/CrocSwap/integer-mult-bounds/pull/1042) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1045](https://github.com/CrocSwap/integer-mult-bounds/pull/1045) | thakrarsagar | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1046](https://github.com/CrocSwap/integer-mult-bounds/pull/1046) | martinxxx9 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1047](https://github.com/CrocSwap/integer-mult-bounds/pull/1047) | woklerx | incorporated | [record 1](../../research/community-batch1047-audit/DISPOSITIONS.json) |
| [#1048](https://github.com/CrocSwap/integer-mult-bounds/pull/1048) | flemhhh | partially reviewed | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1049](https://github.com/CrocSwap/integer-mult-bounds/pull/1049) | thakrarsagar | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1050](https://github.com/CrocSwap/integer-mult-bounds/pull/1050) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1051](https://github.com/CrocSwap/integer-mult-bounds/pull/1051) | thakrarsagar | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1052](https://github.com/CrocSwap/integer-mult-bounds/pull/1052) | steph4n-gh | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1053](https://github.com/CrocSwap/integer-mult-bounds/pull/1053) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1055](https://github.com/CrocSwap/integer-mult-bounds/pull/1055) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1056](https://github.com/CrocSwap/integer-mult-bounds/pull/1056) | rohanarun | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1059](https://github.com/CrocSwap/integer-mult-bounds/pull/1059) | thakrarsagar | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1061](https://github.com/CrocSwap/integer-mult-bounds/pull/1061) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1062](https://github.com/CrocSwap/integer-mult-bounds/pull/1062) | thakrarsagar | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1063](https://github.com/CrocSwap/integer-mult-bounds/pull/1063) | rohanarun | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1065](https://github.com/CrocSwap/integer-mult-bounds/pull/1065) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1068](https://github.com/CrocSwap/integer-mult-bounds/pull/1068) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1069](https://github.com/CrocSwap/integer-mult-bounds/pull/1069) | thakrarsagar | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1072](https://github.com/CrocSwap/integer-mult-bounds/pull/1072) | davidNbreslauer | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1074](https://github.com/CrocSwap/integer-mult-bounds/pull/1074) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1077](https://github.com/CrocSwap/integer-mult-bounds/pull/1077) | woklerx | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1082](https://github.com/CrocSwap/integer-mult-bounds/pull/1082) | rohanarun | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1087](https://github.com/CrocSwap/integer-mult-bounds/pull/1087) | jeremykothe2 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1088](https://github.com/CrocSwap/integer-mult-bounds/pull/1088) | martinxxx9 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1089](https://github.com/CrocSwap/integer-mult-bounds/pull/1089) | martinxxx9 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1090](https://github.com/CrocSwap/integer-mult-bounds/pull/1090) | 1337isnot1337 | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1091](https://github.com/CrocSwap/integer-mult-bounds/pull/1091) | JosieElliston | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1092](https://github.com/CrocSwap/integer-mult-bounds/pull/1092) | ToikY | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1094](https://github.com/CrocSwap/integer-mult-bounds/pull/1094) | rohanarun | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1096](https://github.com/CrocSwap/integer-mult-bounds/pull/1096) | woklerx | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1097](https://github.com/CrocSwap/integer-mult-bounds/pull/1097) | bitplane | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1098](https://github.com/CrocSwap/integer-mult-bounds/pull/1098) | adamgall | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
| [#1099](https://github.com/CrocSwap/integer-mult-bounds/pull/1099) | woklerx | incorporated | [record 1](../../research/community-batch1099-audit/DISPOSITIONS.json) |
