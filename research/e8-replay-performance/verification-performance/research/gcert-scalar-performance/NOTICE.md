# Attribution and changes

`reference/gx.py` is Jacob Sussman's unchanged gcert/1 checker from
`jacobalansussman/wht-power-saving-lean`, commit
`9c94857bbaee886f8649edee0bc2d3c738f9555e`. Its original Apache-2.0 license and
notice are preserved in `reference/LICENSE` and `reference/NOTICE`.

`gx_fast.py` is a modified copy: only `scal` is changed, to use a shared
denominator per sparse register instead of a Fraction object per entry.
The optimization, differential tests, CLI and benchmarks were prepared with
OpenAI Codex assistance on 2026-10-11. The new code is Apache-2.0.

The E8 circuit fixture is Sussman's; the retimed fixture is from CrocSwap
PR365. The p10 centre-sharing fixture is from CrocSwap PR327, prepared by
DreamingOfClouds with substantial Anthropic Claude assistance, building on
the preceding module/flow/lift work credited in that package. Source paths,
commits and hashes are recorded in `SOURCE.json`.

No upstream author's review or endorsement of this optimization is implied.
