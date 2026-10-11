κ = 1.136403735815528e-3

# Shared-donor kernels on the R740 E8 bit word

This conditional construction combines frozen PR #436's R740 bit word with a newly selected shared-donor response kernel and PR #433's unchanged split-centre complex supplier. The exact result is

`κ = 142050466976941 / 125000000000000000 = 0.001136403735815528`.

The bit supplier binds at `c = 1137696618503020372244 / 10^24`. The complex supplier remains `b = 1183986549206329 / 10^18`. This improves PR #438's `κ = 0.001133508328719775` by approximately 0.25544%.

After kernel construction, 57 A-only primitive gate frame changes improve the complete paid profile while preserving the scalar ADD sequence. The bit construction has 740 helpers. Its 112 kernel entries use 100 donor slots and add 136 total entrance dimensions. In each compressed nine-stage window, 5,920 residual slots tile 723 width-64 banks exactly, with no padding. Live stock is 14,187 and the rank deficit is 2,496. No previous published PR is changed.

## Reproduce

Python 3.11 or later and its standard library suffice. Run from any directory, choosing a fresh output directory:

```sh
python3 -B research/r740-shared-donor-kernel/verify.py /tmp/r740-shared-donor-kernel-check --replay-phases
```

Omit `--replay-phases` to reuse only the unchanged, source-bound complex phase evidence. The full command reconstructs the PR #436 word from its pinned producer parameters, elimination reuse and retiming; applies the frozen kernel and retiming selections; replays both scalar orientations and arbitrary dirty columns; checks both reflected frame ledgers and exact bank coordinates; rebuilds complete paid profiles and finite invoices; verifies two rational moment engines and all 47 strict outer inequalities. The full complex replay reconstructs every selected Gaussian phase pair as well.

The phase input is bound to a frozen canonical payload whose original compressed hash matches PR #433's receipt. Comparing decoded bytes removes the Python 3.12/3.14 gzip metadata difference without changing the mathematical input. `MANIFEST.json` and `SOURCES.json` bind package files and provenance. `EXPECTED.json` binds the final exact result and template hashes.

## Construction and scope

PR #436 is reproduced exactly before the new kernel is applied. The new kernel and retiming selections are finite witnesses, not claims of optimal search. Explicit residual isometries follow the obligation made concrete by PR #439, and their route factors are charged in the invoice. Ordered primitive expansion and retiming also follow the contemporaneous idea in PR #434. The kernel mechanism comes from Chafik Boukhalfa's PR #417; the compressed mixed-width admission follows PR #438 and PR #386. The complex program is reconstructed and checked from the pinned PR #433/PR #425 inputs.

The precise finite claim is in [PROOF.md](PROOF.md). All-size compressed-window and correlated dirty-bank semantics, recursive compiler, restored-work/tape/common-grid precision, and analytic transfer interfaces remain inherited assumptions. No unconditional multiplication theorem or new Lean proof is claimed.

Prepared by eumemic with OpenAI Codex assistance. Earlier Anthropic Claude and OpenAI assistance is preserved in [NOTICE.md](NOTICE.md), [SOURCES.json](SOURCES.json), and the original notices. Historical documents under `proofs/` describe their original constructions; they do not state this package's result.
