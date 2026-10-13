# Gauge44 without K-triangles, with earlier jp8 layers and PR589's bit supplier: conditional κ = 0.001656193765416678

Under the retained all-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape, exact-recovery, analytic-transfer and bit H1–H5 interfaces (as in #645), and the PR589 bit supplier,

$$
T(n)=O\!\left(n(\log n)^{1-\kappa}\right),\qquad
\kappa=\frac{1656193765416678}{10^{18}}=0.001656193765416678.
$$

> **Review status: pending re-sign (NotriReviewer).** NotriReviewer found the no-triangle word, the NP layer chain and strict SOUND. Its re-sign of this tree, in particular the drivers in `construction/notri/` and `construction/layers_np/`, is pending. Do not ship before it.

**The construction is icekylinx's [#645](https://github.com/CrocSwap/integer-mult-bounds/pull/645) (`research/gauge44-global`).** This package changes four things:
1. **No-triangle word (PartialK).** #645's gauge44 chain is run with **none** of the four (p,−1) K-triangles, so there are R = 504 helpers. In the six K-blocks {0,1,2,11,12,13}, the completion priority is extended by the 6-row list `construction/notri/PRIO6.json`. Every block then pairs at rank 4, giving **56** rank-four cold ends instead of 44. `construction/notri/reproduce_notri.py` rebuilds this word from a #645 `reproduce.py --until word` output. It uses PartialK's generalisations of #645's and PR635's constructors (`cgx.py`, `port_stage_x.py`, `cold44x.py`; each differs from its original only in the documented parameters). It pins:
   - the pairing ranks [4]*14, inside `cold44x.py` and again in the driver;
   - the word (`3e99ba77…`);
   - the canonical word, the local programs and the Clifford recipes.
   `--control-g44` instead rebuilds #645's own gauge44 word (`78c7aada…`) with the same scripts.
2. **Layers on the no-triangle word (G44Stack).** `construction/layers_np/reproduce_np.py` applies to the no-triangle regroup word (`864ff4a1…`):
   - research/gauge44-layered's six pivot swaps, mapped to the 504-helper numbering (`PIVOT-SWAP-NP.json`, swap word `beb3579f…`);
   - the greedy HPE (46, `HPE-RECIPE-NP.json`);
   - the exact cold44 (same 56 ends);
   - the entering ends s4 (566/567/578/579 at U24) and x30 (608/610/543/555 at U30), plus BlockCombine's b6 and q4 dim-8 cold ends (`COLD-LAYERS-RECIPE-NP.json.gz`). p123 is negative on this base and dropped; j3 is dead.
   The layered word is pinned (`a9de804f…`): profile `{1:2534, 2:346, 3:458, 4:178, 5:56, 8:8}`, width 3800. The signed research/gauge44-layered files `construction/layers/build_pivot_swap.py` and `construction/layers/layer_end_controls.py` are used unchanged, and the latter must reject exactly 59 controls. The global code is research/gauge44-layered's (spot-width rule): SPEC `width_spot_helpers` [270,282,294,306] and `pivot_swap` → `construction/layers_np/PIVOT-SWAP-NP.json`, giving spot widths [9,9,8,8].
3. **Owner map (G44Pack, G44Pack2).** G44Pack2's `jo.py` (an implementation of jaymosley07's [#653](https://github.com/CrocSwap/integer-mult-bounds/pull/653) joint two-call nomination) gave joNPs, at this word's packing ceiling {48:2364}: `jo.py ../G44Pack/maps/NPb LLx/joNP --pairs 600 --passes 8 --seconds 3`. NPb came from G44Pack: `relabel.py maps/N6a <np local>/CANONICAL-WORD.json.gz NPs`, then `rewidth.py NPs <np local> gaugeNP/code NPr`, then `loop.py NPr NPL 5` (alternating `dissolve.py` and Mine636's `gapmerge.py`, which generalises vectorsss/Chi Zhao's [#638](https://github.com/CrocSwap/integer-mult-bounds/pull/638) `relocate_two.py`), with NPb = `NPL/03dz`. N6a came from relabelling G44Pack2's joN5c map onto the no-triangle word, followed by `rewidth.py` and `loop.py N6r N6L 6`. Only PLAN and OWNERS change. These are search inputs only; no verifier reads them.
4. **Expected values.** `data/SPEC.json` is re-derived by #645's discovery → `code/freeze_spec.py` → strict chain.

- **κ = 0.001656193765416678** (conservative 0.001656193762539939). That is +0.4068% over #645, +0.1354% over research/gauge44-layered and +0.0204% over the plain no-triangle word (N6a, 0.001655856595560428). The complex side certifies 0.001658941293644404576195 and PR589's bit supplier gives 0.001733427039589844234749, so **the complex side binds**. Under PR543 the bit side would cap κ at 0.001651096360425895 (`PROOF-NOTE-BIT.md`).
- **Evidence.** G44Pack2's strict replay with `verify_global.py` passes (`PASS_GAUGE44_STRICT_GLOBAL_REPLAY`, κ 0.001656193765416678). It ran this code and data against G44Stack's NP locals. `RESULT.json` is that replay's `REPLAY.json`, converted to LF. The locals rebuilt by `reproduce_np.py` match the strict locals byte for byte in every file except CLIFFORD-REVIEW and SCALAR-FRAME-AUDIT. Those two differ only in their `seconds` field, and the comparison normalises only that field. For this package, `data/SPEC.json` and a fresh `verify_global.py` replay on locals rebuilt by the two drivers are the binding record.
- **Independent price.** `independent/GAUGE44-INDEPENDENT-PRICE.json` is regenerated on this package's `data/PLAN.json` with the ported `independent/price_profile.py`: `PASS_FROZEN_PROFILE_TWO_EXACT_ENGINE_AND_OUTER47_CROSSCHECK`, κ equal to the strict replay.
- **Independent local audit.** `evidence/layers/LOCAL-AUDIT-LAYERED.json` is #645's `independent/audit_local.py`, run with `--main` on the layered word (content `a9de804f…`): `PASS_INDEPENDENT_EXACT_FORWARD_AND_DUAL_ENDPOINT_FRAMES_ENTRANCES_CONES`, 216 entering helpers, 120 low ends, 66 cold ends, 728 checked columns. Rerunning it reproduces the receipt except `elapsed_seconds` and, across zlib versions, `compressed_sha256`.
- **Historical #645 files (PR543-based, 492 helpers).** These are #645's files, retained unchanged and **not** updated for this package: `LOCAL-VALIDATION.json`, `CONSTRUCTION.md`, `hosting/`, `evidence/` (except `evidence/layers/`), the rest of `independent/`, `construction/reproduce.py` and its inputs, and `code/prepare_global.py`. They describe #645's word, owner map, PR543 supplier and κ 0.001649483702558979. `code/prepare_global.py` is #645's one-shot owner-map preparer, hard-wired to #645's parent plan and R = 492. No verifier imports it. This package's PLAN/OWNERS are frozen search output, and the strict replay checks them. `construction/reproduce.py` is still used for its `--until word` shadow and hamming inputs; its 492-word output is then superseded by `construction/notri/`. `construction/layers/reproduce_layers.py` is research/gauge44-layered's driver for the 492-helper layered word, shipped unchanged as signed; it is not used here.
- **Review.** NotriReviewer (re-sign pending for the drivers). Files by committed LF SHA-256:
  - `construction/notri/reproduce_notri.py` 90148c2a0422b4f92164298a283de73d413ab3d4cb7151a0e6b643a37ea025a8 (no-triangle driver)
  - `construction/notri/cgx.py` 3da039d4184097c14802f9dbf972520d5b807671196f5e47a2247bc9f29bb418 (PartialK's generalised construct_gauge_xcentre.py)
  - `construction/notri/port_stage_x.py` 38310744d054e393ea35e996047cddeb2d212141aaaaa4b07f7a4663b11db8e7 (PartialK's generalised build_port_stage.py)
  - `construction/notri/cold44x.py` f0bc3500efb2c839a0f8cb03dbb9ea0a54f1dfc71ef81e5373b3d638ac5b8296 (PartialK's generalised build_gauge_cold44.py plus the PAIRING_RANKS pin)
  - `construction/notri/PRIO6.json` de0412511b0dd1af13e9717bc791126ac0e91c569b5391fd6c70268083045d15 (completion priority)
  - `construction/layers_np/reproduce_np.py` 1a304144a250d00d14154692ba522365b036777cf2b6fac466095e8ba733c16c (NP layer driver)
  - `construction/layers_np/PIVOT-SWAP-NP.json` d49b8d316da1cbdaf995dd0e8314d3c67cc9cd4d5902e9d85ccb907be645bef5 (layer input)
  - `construction/layers_np/HPE-RECIPE-NP.json` 43900139f618bdc06b8319098fb8dccaf4fc315b43ef7c067ca2cd778cdba2c1 (layer input)
  - `construction/layers_np/COLD-LAYERS-RECIPE-NP.json.gz` 3164cfb71baaeba4ac43427bc14075a225fc3a32ecd9341e58aa52c03a4ee2c0 (layer input)
  - `construction/layers/build_pivot_swap.py` 8e8bced88be2e592ded40929499bac385ca92fcc1fa59183c22229dbf34093b8 (signed, unchanged)
  - `construction/layers/layer_end_controls.py` 7829187bfc8f909948d5250e0ec00f02c89f5fe98306a3ed88daee36cb3c92ef (signed, unchanged)
  - `construction/layers/reproduce_layers.py` 435699f6f79c6c7fb8d6cc5a8382576d6ac88747583a975ff671e45440b93c4e (signed, unchanged, unused here)
  The global code is research/gauge44-layered's, unchanged (LayerReviewer): assemble 4c270a99, assembly_controls e4c0f782, audit_allcold a87d7f48, bind 1d39bcc7, witness 779c5172. The bit-supplier code is unchanged (Bit589Reviewer): verify_global 16bd5e54, bit_supplier_controls e6d33fb6, price_profile d2f548ad.
- **Line endings.** These files had CRLF in the admitted trees and are committed as LF only (`crlf.replace(b'\r\n', b'\n') == lf`, no lone `\r`):
  - `data/SPEC.json`: CRLF 37c730471ab77c26…, committed (LF) c49d1ae1fabcd483…
  - `RESULT.json`: CRLF 47cd24d4ee678aef…, committed (LF) eb13739e8ad1fdba…


Clean-clone verification, from the repository root (Python 3.11+, assertions on; prepare the pinned #635 supplier as in the #645 section below):

```sh
python -B research/gauge44-notri-layered/verify_manifest.py
python -B research/gauge44-notri-layered/construction/reproduce.py \
  --main . --pr635 /tmp/gauge44-pr635 --out /tmp/notri-base --until word
python -B research/gauge44-notri-layered/construction/notri/reproduce_notri.py \
  --main . --pr635 /tmp/gauge44-pr635 --word-dir /tmp/notri-base --out /tmp/notri-word --word-only
python -B research/gauge44-notri-layered/construction/layers_np/reproduce_np.py \
  --main . --pr635 /tmp/gauge44-pr635 --notri-dir /tmp/notri-word --hamming /tmp/notri-base/hamming --out /tmp/notri-np
python -B research/gauge44-notri-layered/independent/audit_local.py \
  --word /tmp/notri-np/layers/FULL-WORD.json.gz --main . --output /tmp/notri-np-audit.json
python -B research/gauge44-notri-layered/verify_global.py \
  --main . --local /tmp/notri-np/local --work /tmp/notri-np-global
# kappa 0.001656193765416678
```

Optional control: `reproduce_notri.py ... --control-g44 --out /tmp/notri-ctl` rebuilds #645's gauge44 word `78c7aada…`.

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
