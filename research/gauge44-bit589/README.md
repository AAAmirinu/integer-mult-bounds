# Gauge44 with PR589's bit supplier and a dissolved owner map: conditional κ = 0.001652528731617094

**The construction is icekylinx's [#645](https://github.com/CrocSwap/integer-mult-bounds/pull/645) (`research/gauge44-global`).** This package keeps #645's construction, supplier word and complex-side global code, and changes three things:
1. **Bit supplier (G44Stack's port).** The cited bit supplier is PR589's ([#589](https://github.com/CrocSwap/integer-mult-bounds/pull/589), merged; `research/e8-bit-p111-tuned/tune/EXPECTED.json` on main, shipped as `inputs/PR589-EXPECTED.json` and pinned in `code/assemble.py` by git blob `e293ddc5…`). It replaces #543's. `code/assemble.py` derives the bit rank-mass deficit from the word's parameters, T(2Kv − L·cst) at nine stages (the PR545/PR555 identity), where #645 hard-coded 9984. The new `code/bit_supplier_controls.py` holds 12 negative controls, which `verify_global.py` runs and requires. See `PROOF-NOTE-BIT.md`.
2. **Owner map (G44Pack).** The map started as #645's map, repacked by Mine636's gap-merge search (`gapmerge.py`, which generalises vectorsss/Chi Zhao's [#638](https://github.com/CrocSwap/integer-mult-bounds/pull/638) `relocate_two.py`) through G44Pack's `ceiling_pack.py`. That was run cp1 (round gm3), then cp2, resumed from it for 12 rounds. G44Pack's **dissolve move** then finished it: `dissolve.py --plan cp2/rounds/gm3/PLAN.json --owners cp2/rounds/gm3/OWNERS.json.gz --out dz1 --seconds 600 --nodes 50000`, which is deterministic. The move empties a non-empty bin by distributing its roles into defect bins, one role per (bin, time), within windows and capacity, and accepts if the concave idle cost drops. Only PLAN's `profile` and `assignment_sha256` change. These are search inputs only; no verifier reads them.
3. **Expected values.** `data/SPEC.json` is re-derived by #645's discovery → `code/freeze_spec.py` → strict chain.

- **κ = 0.001652528731617094** (conservative 0.001652528728737236). That is +0.1846% over #645 and +0.0868% over research/gauge44-repack (0.001651096360425895). The complex side certifies 0.00165526410310589140991 and PR589's bit supplier gives 0.001733427039589844234749, so **the complex side binds**. Under PR543 this map would be bit-bound at 0.001651096360425895, so the gain over gauge44-repack rests on the PR589 citation (`PROOF-NOTE-BIT.md`, "Effect on the outer chain").
- **Evidence.** G44Pack's strict replay with `verify_global.py` passes (`PASS_GAUGE44_STRICT_GLOBAL_REPLAY`, κ 0.001652528731617094). It ran this code and data with `--local` set to G44Stack's freshly rebuilt gauge44 local. For this package, `data/SPEC.json` and a fresh `verify_global.py` replay are the binding record.
- **Historical #645 evidence (PR543-based).** The following are #645's files, retained unchanged and **not** updated for this package: `RESULT.json`, `LOCAL-VALIDATION.json`, `CONSTRUCTION.md`, `hosting/`, `evidence/`, and the rest of `independent/` (`audit_local.py`, `review_guards.py` and their receipts). They describe #645's owner map, PR543 supplier and κ 0.001649483702558979. No verifier reads them. `SOURCES.json` and `NOTICE.md` say the same.
- **Independent price (ported).** `independent/price_profile.py` is G44Stack's port to PR589 (blob pin and an independently re-derived deficit). `independent/GAUGE44-INDEPENDENT-PRICE.json` is regenerated on this package's `data/PLAN.json`: `PASS_FROZEN_PROFILE_TWO_EXACT_ENGINE_AND_OUTER47_CROSSCHECK`, with κ equal to the strict replay. Rerunning `python -B independent/price_profile.py --main <main> --output <new>.json` reproduces it byte for byte.
- **Review.** Bit589Reviewer: **SOUND-WITH-FIXES** (packaging and documentation only; no mathematical or verifier hole). It signs the three changed code files, by their committed LF SHA-256:
  - `code/assemble.py` 1d4449ae65d92b21ca62ca50917ff0b74908542ada5d4687b54744dc9b9abc39 (changed from #645)
  - `code/bit_supplier_controls.py` e6d33fb61a570c3f50669412acc467a3fd06ef0b806da6a75bc296c6ba2142a5 (new)
  - `verify_global.py` 16bd5e54598592e92e210f99065348c5df261b8350fdc688072ce053d15b088a (changed from #645)

  The ported `independent/price_profile.py` (LF sha256 d2f548ad6b99f64a…, not run by `verify_global.py`) is submitted to Bit589Reviewer for the same sign-off. The other 20 `.py` files are byte-identical to #645's. The reviewer re-traced all 12 controls on the gauge44 word and recomputed the outer chain under both suppliers. Its packaging fixes are applied here: the PR589 citation in SOURCES/NOTICE, and the historical labels above.
- **Line endings.** These files had CRLF in the admitted trees and are committed as LF only (`crlf.replace(b'\r\n', b'\n') == lf`, no lone `\r`):
  - `code/assemble.py`: CRLF ee717045f6e436fd…, committed (LF) 1d4449ae65d92b21…
  - `verify_global.py`: CRLF 58cd1b9a2276dde0…, committed (LF) 16bd5e54598592e9…
  - `data/SPEC.json`: CRLF 6ecf8a66f6aff0f8…, committed (LF) 7f124fcb19d315b1…
  No verifier pins their bytes except `MANIFEST.json`, which is regenerated here. The bit input is pinned by its git blob and is unchanged.

Clean-clone verification, from the repository root (Python 3.11+, assertions on; prepare the pinned #635 supplier as in the #645 section below):

```sh
python -B research/gauge44-bit589/verify_manifest.py
python -B research/gauge44-bit589/construction/reproduce.py \
  --main . --pr635 /tmp/gauge44-pr635 --out /tmp/gauge44-bit589-local --until phases
python -B research/gauge44-bit589/verify_global.py \
  --main . --local /tmp/gauge44-bit589-local/local --work /tmp/gauge44-bit589-global
# kappa 0.001652528731617094
```

## Predecessor: #645's README (unchanged below; paths read `research/gauge44-global`)

### Gauge44: conditional κ = 0.001649483702558979

New contributions by **icekylinx**, with **OpenAI GPT-6 Astra** assistance.
Local review and packaging used OpenAI Codex. Original notices and Apache-2.0 licenses are retained.

Under the retained all-size compiler, common-label/mutable-source realization,
whole-call hosting, precision/tape, exact-recovery, analytic-transfer and bit
H1–H5 interfaces,

$$
T(n)=O\!\left(n(\log n)^{1-\kappa}\right),\qquad
\kappa=\frac{1649483702558979}{10^{18}}=0.001649483702558979.
$$

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
