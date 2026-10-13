# Gauge44 with earlier jp8 layers, PR589's bit supplier and a repacked owner map: conditional κ = 0.00165395497190225

Under the retained all-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape, exact-recovery, analytic-transfer and bit H1–H5 interfaces (as in #645), and the PR589 bit supplier,

$$
T(n)=O\!\left(n(\log n)^{1-\kappa}\right),\qquad
\kappa=\frac{165395497190225}{10^{17}}=0.00165395497190225.
$$

> **Review: SOUND.** LayerReviewer signed the layered code and inputs listed under "Review" below, after its fixes (the layer-end controls and the recipe meta). Bit589Reviewer signed the bit-supplier code (SOUND). Every listed hash equals the committed file.

**The construction is icekylinx's [#645](https://github.com/CrocSwap/integer-mult-bounds/pull/645) (`research/gauge44-global`).** This package is research/gauge44-bit589b's package (PR589 bit supplier; code reviewed SOUND by Bit589Reviewer) with three changes:
1. **Layered provider word (G44Stack).** Earlier community jp8 layers are re-applied to #645's gauge44 word by `construction/layers/reproduce_layers.py`, after `construction/reproduce.py --until word`:
   - six cost-neutral pivot-role swaps (PR641's `build_pivot_swap.py`; s4 and s6 swaps);
   - 8 entering ends: 560/561/572/573 at U24 (s4), and 597/599 (#629's E1 pair) plus 537/549 (s6) at U30;
   - 10 factored dim-8 cold ends (p123 and q4).
   #645's 44 rank-four cold ends, premix and tails are rebuilt exactly. The word is pinned (`0be48b1d…`), and 59 raw-word layer-end controls (LayerReviewer's adaptation of PR635's `cold_end_controls.py`) must all be rejected while it is built. Per call, the residual width goes 3794 → 3776 and the profile becomes `{1:2542, 2:414, 3:434, 4:154, 5:56, 8:8}`. The global code gains the spot-width rule for swapped-out pivots, pinned through SPEC key `pivot_swap`. See `PROOF-NOTE-LAYERS.md`.
2. **Owner map (G44Pack).** Mine636's `widen_repair.py` re-fitted gauge44-bit589b's L1g4 map to the new widths. G44Pack's `rewidth.py` then moved it onto the layered locals, and `loop.py` (alternating `dissolve.py` and Mine636's `gapmerge.py`, which generalises vectorsss/Chi Zhao's [#638](https://github.com/CrocSwap/integer-mult-bounds/pull/638) `relocate_two.py`) repacked it. This map comes from an LNS (`lns5.py`, Mine636's type-aggregated LNS with an exact HiGHS window solve) started from G44Pack's `LL/05gm`: `python -B lns5.py --plan LL/05gm/PLAN.json --owners LL/05gm/OWNERS.json.gz --out LN5 --seconds 1800 --workers 1 --k 120 --sub 120 --b 0.00165` (defaults --seed 1, --early 13, --e 1). LN5c is the snapshot after its fourth improvement. Its solve is time-limited, so a rerun may differ; the frozen map is the evidence. `LL/05gm` came from `loop.py wL2 LL 10`, where `wL2` = `rewidth.py wL locL/gauge44-local gauge44L/code wL2` and `wL` = Mine636's `widen_repair.py` on bit589b's L1g4 map (`L1/04gm`). Only PLAN and OWNERS change. These are search inputs only; no verifier reads them.
3. **Expected values.** `data/SPEC.json` is re-derived by #645's discovery → `code/freeze_spec.py` → strict chain. G44Pack admitted the new word with `NEWWORD=1 admit645.py`.

- **κ = 0.00165395497190225** (conservative 0.001653954969006336). That is +0.2711% over #645 and +0.0723% over research/gauge44-bit589b (0.001652760598550299). The complex side certifies 0.00165669507095177754089 and PR589's bit supplier gives 0.001733427039589844234749, so **the complex side binds**. Under PR543 the bit side would cap κ at 0.001651096360425895 (`PROOF-NOTE-BIT.md`).
- **Evidence.** G44Pack's strict replay with `verify_global.py` passes (`PASS_GAUGE44_STRICT_GLOBAL_REPLAY`, κ 0.00165395497190225), using this code and data and the layered locals. `RESULT.json` is that replay's `REPLAY.json`, converted to LF. For this package, `data/SPEC.json` and a fresh `verify_global.py` replay on locals rebuilt by `reproduce_layers.py` are the binding record.
- **Independent price.** `independent/GAUGE44-INDEPENDENT-PRICE.json` is regenerated on this package's `data/PLAN.json` with the ported `independent/price_profile.py`: `PASS_FROZEN_PROFILE_TWO_EXACT_ENGINE_AND_OUTER47_CROSSCHECK`, with κ equal to the strict replay.
- **Independent local audit of the layered word.** `evidence/layers/LOCAL-AUDIT-LAYERED.json` is #645's `independent/audit_local.py`, run with `--main` on the layered word (content `0be48b1d…`): `PASS_INDEPENDENT_EXACT_FORWARD_AND_DUAL_ENDPOINT_FRAMES_ENTRANCES_CONES`, 204 entering helpers, 96 low ends, 54 cold ends, 716 checked columns. It is an exact rational check of the whole word, complementing the layer-end controls (see `PROOF-NOTE-LAYERS.md`). The clean-clone command below reruns it; only `elapsed_seconds` varies.
- **Historical #645 evidence (PR543-based).** These are #645's files, retained unchanged and **not** updated for this package: `LOCAL-VALIDATION.json`, `CONSTRUCTION.md`, `hosting/`, `evidence/` (except `evidence/layers/`), and the rest of `independent/` (`audit_local.py`, `review_guards.py` and their receipts). They describe #645's word, owner map, PR543 supplier and κ 0.001649483702558979. No verifier reads them.
- **Review.** LayerReviewer's verdict is **SOUND**. It signs these files by their committed LF SHA-256:
  - `code/witness.py` 779c5172894b992131e85be1e592ed2a1aec8c287b872ff42007d36a7291e444 (changed from gauge44-bit589: spot_widths)
  - `code/bind_providers_portable.py` 1d39bcc7b63ac158e021454beaae897d123e174360573762aecade3cd43193f6 (changed: spot-width call site)
  - `code/audit_allcold.py` a87d7f4844ca963516637d249b14a0654f67f8047b6b265ae25b0cf30963e503 (changed: spot-width call site)
  - `code/assemble.py` 4c270a996b380ab712f72b81173ab24f1c73203a33578f261bfbaa7e67d75aec (changed: spot-width call site)
  - `code/assembly_controls.py` e4c0f7828af64fdaef1896e4448d0212bd3041805097140b8cfafd098f8a6162 (changed: cold_swap never the identity)
  - `construction/layers/reproduce_layers.py` 435699f6f79c6c7fb8d6cc5a8382576d6ac88747583a975ff671e45440b93c4e (new)
  - `construction/layers/layer_end_controls.py` 7829187bfc8f909948d5250e0ec00f02c89f5fe98306a3ed88daee36cb3c92ef (new: LayerReviewer's adaptation of PR635's cold_end_controls.py)
  - `construction/layers/build_pivot_swap.py` 8e8bced88be2e592ded40929499bac385ca92fcc1fa59183c22229dbf34093b8 (new here; PR641's constructor, the LF file PivotReviewer signed)
  - `construction/layers/PIVOT-SWAP-S6.json` c6254d8a6ed29211e490c74b4d1a43c7d66a9e733691cbe6c83c4f55d66f1d1f (layer input)
  - `construction/layers/HYPERPLANE-END-S6.json` 23c9d7ce46c3378448a12fd82b6affc0b8fce1d4f4c45c425b859d47f96be2cd (layer input)
  - `construction/layers/COLD-LAYERS-RECIPE.json.gz` 54a6b10f8933f22ecb8226bbeef1652bbc3ce6b31ad2e6637c3f6164f669da0f (layer input)

  Bit589Reviewer already signed `verify_global.py` 16bd5e54…, `code/bit_supplier_controls.py` e6d33fb6… and `independent/price_profile.py` d2f548ad…, and they are unchanged here. Every other `.py` file is byte-identical to #645's.
- **Line endings.** These files had CRLF in the admitted trees and are committed as LF only (`crlf.replace(b'\r\n', b'\n') == lf`, no lone `\r`):
  - `construction/layers/build_pivot_swap.py`: CRLF 318d1ffd96a77523…, committed (LF) 8e8bced88be2e592…
  - `data/SPEC.json`: CRLF 2f542205a3784858…, committed (LF) ee7925bd83cad9a4…
  - `RESULT.json`: CRLF b46f6cb681251112…, committed (LF) 9fdb57371f9f662b…
  The only byte pins on them are `MANIFEST.json`, which is regenerated here, and the pinned-word check, which hashes canonical JSON rather than file bytes.

Clean-clone verification, from the repository root (Python 3.11+, assertions on; prepare the pinned #635 supplier as in the #645 section below):

```sh
python -B research/gauge44-layered/verify_manifest.py
python -B research/gauge44-layered/construction/reproduce.py \
  --main . --pr635 /tmp/gauge44-pr635 --out /tmp/gauge44-layered-word --until word
python -B research/gauge44-layered/construction/layers/reproduce_layers.py \
  --main . --pr635 /tmp/gauge44-pr635 --word-dir /tmp/gauge44-layered-word --out /tmp/gauge44-layered-local
python -B research/gauge44-layered/independent/audit_local.py \
  --word /tmp/gauge44-layered-local/layers/FULL-WORD.json.gz --main . \
  --output /tmp/gauge44-layered-audit.json
# status PASS_INDEPENDENT_EXACT_FORWARD_AND_DUAL_ENDPOINT_FRAMES_ENTRANCES_CONES (= evidence/layers/LOCAL-AUDIT-LAYERED.json except elapsed_seconds)
python -B research/gauge44-layered/verify_global.py \
  --main . --local /tmp/gauge44-layered-local/local --work /tmp/gauge44-layered-global
# kappa 0.00165395497190225
```

## Predecessor: #645's README (unchanged below; paths read `research/gauge44-global`)

### Gauge44: conditional κ = 0.001649483702558979

New contributions by **icekylinx**, with **OpenAI GPT-6 Astra** assistance.
Local review and packaging used OpenAI Codex. Original notices and Apache-2.0 licenses are retained.

Under the retained all-size compiler, common-label/mutable-source realization,
whole-call hosting, precision/tape, exact-recovery, analytic-transfer and bit
H1–H5 interfaces,

$$
T(n)=O\!\left(n(\log n)^{1-\kappa_{645}}\right),\qquad
\kappa_{645}=\frac{1649483702558979}{10^{18}}=0.001649483702558979
$$

(This is #645's own κ. **This package's κ is the one at the top of this README.**)

The certified complex saving is `0.001652208994368411824947`. The unchanged
[#543](https://github.com/CrocSwap/integer-mult-bounds/pull/543) bit supplier gives
`0.001653826988146798944268`, so the complex side binds. The conservative complex
model separately certifies κ `0.001649483699681650`.

### Construction

This replaces the local supplier and all 72 owner assignments of pinned
[#635](https://github.com/CrocSwap/integer-mult-bounds/pull/635). Source/copy exchanges
at equal rank-one frames alter the factory's arbitrary-helper-input propagation.
An invertible completion of the retired rows and source-carried coordinate totals
then expose 44 rank-four cold endpoints. Exact input premixes, low-frame tails
and a recomputed full inverse realize them.

| Per-invocation quantity | Complete #635 JP8 | Gauge44 |
| --- | ---: | ---: |
| Source / target ports | 112 / 112 | 112 / 112 |
| Helpers | 492 | 492 |
| Rank-four cold endpoints | 22 | 44 |
| Helper residual width | 3,894 | 3,794 |
| Paid local rank mass | 5,750 | 5,650 |

The new paid local profile is `{1:2514, 2:404, 3:448, 4:160, 5:56, 8:8}`.
The explicit whole-family assignment covers 35,424 helper roles on 7,168 live
and 7,670 physical families. It retains the rank deficit 2,560 and charges every
idle remainder. Exact integer majorization certificates justify the owner
updates; the resulting map is a coordinate fixed point, with no claim of joint
optimality.

The assembled κ is 0.809306% above #635. `data/FRONTIER.json` records Pro's dated
comparison snapshot; it is not a live ranking of community results.

### Proof and evidence

- `CONSTRUCTION.md`: exact cold-space calculation, dyadic realization and attribution.
- `hosting/PROOF.md`: capacity, exchange and majorization arguments.
- `independent/CENTRE-GUARD-REVIEW.md`: ordered center-frame interface and source carriers.
- `data/SPEC.json`, `evidence/ASSEMBLY.json`: strict component moments and outer parameters.
- `evidence/audit/`: actual controller, physical charts and finite invoice.
- `construction/INPUTS.json`, `data/UPSTREAM-PINS.json`: inherited input hashes.
- `MANIFEST.json`, `SOURCES.json`, `LOCAL-VALIDATION.json`: submitted bytes, provenance and local checks.

Original Pro run receipts are retained as evidence; their raw logs remain in
the original archive outside the submission. Fresh replay writes new logs to
the selected output directory.

### Incremental reproduction

Use Python 3.11 or newer with assertions enabled. The required replay uses only
the standard library. The optional historical seed-discovery optimizer is not
part of admission.

Prepare the pinned #635 supplier in a separate directory (the main dependencies
are already present in this repository):

```sh
git fetch https://github.com/CrocSwap/integer-mult-bounds.git a6895a69f8ad98ab45777b03e9e6f48888c39f6f
mkdir -p /tmp/gauge44-pr635
git archive FETCH_HEAD research/complex-571-cold14-st2 | tar -x -C /tmp/gauge44-pr635
```

From the repository root, with fresh output directories:

```sh
python -B research/gauge44-global/verify_manifest.py
python -B research/gauge44-global/construction/reproduce.py \
  --main . --pr635 /tmp/gauge44-pr635 \
  --out /tmp/gauge44-local --until phases
python -B research/gauge44-global/verify_global.py \
  --main . --local /tmp/gauge44-local/local --work /tmp/gauge44-global
```

The dedicated workflow also runs the independent literal-word audit, exact owner
reproduction, preserved-assertion comparison and independent pricing on Python
3.11 and 3.14. `hosting/README.md` and `independent/README.md` give those commands.
No ancestral full replay, optimizer search or PDF generation is required.

The result remains a finite conditional witness. It does not establish an
unconditional multiplication theorem or a complete Lean formalization.
