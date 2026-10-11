κ = 1.138798055343319e-3

# Block retiming on the R740 shared-donor E8 word

This conditional construction combines frozen PR #436's R740 bit word with a newly selected shared-donor response kernel and PR #433's unchanged split-centre complex supplier. The exact result is

`κ = 1138798055343319 / 1000000000000000000 = 0.001138798055343319`.

The bit supplier binds at `c = 1140096394900736521536 / 10^24`. The complex supplier remains `b = 1183986549206329 / 10^18`. This improves PR #440's R740 shared-donor package's `κ = 0.001136403735815528` by approximately 0.21069%.

After kernel construction and the preceding 57 A-only primitive frame changes, this successor applies 112 net B-frame changes following 53 pair moves and single-gate descent, then 42 further B-frame changes selected by 14 window moves. Every stage preserves the complete ordered scalar ADD sequence and uses only the existing frame family. The bit construction has 740 helpers. Its 112 kernel entries use 100 donor slots and add 136 total entrance dimensions. In each compressed nine-stage window, 5,920 residual slots tile 723 width-64 banks exactly, with no padding. Live stock is 14,187 and the rank deficit is 2,496. No previous published PR is changed.

## Reproduce

Python 3.11 or later and its standard library suffice. Run from any directory, choosing a fresh output directory:

```sh
python3 -B research/r740-block-retimed-kernel/verify.py /tmp/r740-block-retimed-kernel-check --replay-phases
```

Omit `--replay-phases` to reuse only the unchanged, source-bound complex phase evidence. The full command reconstructs the PR #436 word from its pinned producer parameters, elimination reuse and retiming; applies the frozen kernel and retiming selections; replays both scalar orientations and arbitrary dirty columns; checks both reflected frame ledgers and exact bank coordinates; rebuilds complete paid profiles and finite invoices; verifies two rational moment engines and all 47 strict outer inequalities. The full complex replay reconstructs every selected Gaussian phase pair as well.

The phase input is bound to a frozen canonical payload whose original compressed hash matches PR #433's receipt. Comparing decoded bytes removes the Python 3.12/3.14 gzip metadata difference without changing the mathematical input. `MANIFEST.json` and `SOURCES.json` bind package files and provenance. `EXPECTED.json` binds the final exact result and template hashes.

## Construction and scope

PR #436 is reproduced exactly before the new kernel is applied. The kernel and all three retiming selections are finite witnesses, not claims of optimal search. Every stage is reconstructed from its input hash; the final word has SHA256 `00d8aa8608e40b53fd8752399de06cb730cc55caaadc528f88379cb31b8460a6`. The previous 57-gate package is published as PR #440 at commit `bd03373b6d4d4e380d0b6ea7d55cd2ac8f163544`; its claim and selected word remain frozen, and its release manifest is pinned in SOURCES.json. Explicit residual isometries follow the obligation made concrete by PR #439, and their route factors are charged in the invoice. Ordered primitive expansion and retiming also follow the contemporaneous idea in PR #434. The kernel mechanism comes from Chafik Boukhalfa's PR #417; the compressed mixed-width admission follows PR #438 and PR #386. The complex program is reconstructed and checked from the pinned PR #433/PR #425 inputs.

The precise finite claim is in [PROOF.md](PROOF.md). All-size compressed-window and correlated dirty-bank semantics, recursive compiler, restored-work/tape/common-grid precision, and analytic transfer interfaces remain inherited assumptions. No unconditional multiplication theorem or new Lean proof is claimed.

Prepared by eumemic with OpenAI Codex assistance. Earlier Anthropic Claude and OpenAI assistance is preserved in [NOTICE.md](NOTICE.md), [SOURCES.json](SOURCES.json), and the original notices. Historical documents under `proofs/` describe their original constructions; they do not state this package's result.
