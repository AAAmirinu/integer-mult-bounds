# Gauge44 with PR589's bit supplier and an alternating dissolve/gap-merge owner map: conditional κ = 0.001652760598550299

**The construction is icekylinx's [#645](https://github.com/CrocSwap/integer-mult-bounds/pull/645) (`research/gauge44-global`).** This package keeps #645's construction, supplier word and complex-side global code, and changes three things:
1. **Bit supplier (G44Stack's port).** The cited bit supplier is PR589's ([#589](https://github.com/CrocSwap/integer-mult-bounds/pull/589), merged; `research/e8-bit-p111-tuned/tune/EXPECTED.json` on main, shipped as `inputs/PR589-EXPECTED.json`, pinned in `code/assemble.py` by git blob `e293ddc5…`). It replaces #543's. `code/assemble.py` derives the bit rank-mass deficit from the word's parameters, T(2Kv − L·cst) at nine stages (the PR545/PR555 identity), where #645 hard-coded 9984. The new `code/bit_supplier_controls.py` holds 12 negative controls, which `verify_global.py` runs and requires. See `PROOF-NOTE-BIT.md`. The code is the same as research/gauge44-bit589's, byte for byte.
2. **Owner map (G44Pack / G44Pack2).** The map started as #645's map, repacked by Mine636's gap-merge search (`gapmerge.py`, which generalises vectorsss/Chi Zhao's [#638](https://github.com/CrocSwap/integer-mult-bounds/pull/638) `relocate_two.py`) through G44Pack's `ceiling_pack.py`. G44Pack's **dissolve move** (`dissolve.py`) gave research/gauge44-bit589's dz1 map; that move empties a non-empty bin into defect bins, one role per (bin, time), within windows and capacity, if the concave idle cost drops. This map comes from G44Pack's `loop.py`, which alternates `dissolve.py` (900 s, 50000 nodes) and `gapmerge.py` (300 s): `python -B loop.py dz1 L1 8` (run by G44Pack from dz1; the loop stopped after round 04, and only completed rounds are used). The map is round 04's gap-merge output (`L1/04gm`). Only PLAN's `profile` and `assignment_sha256` change. These are search inputs only; no verifier reads them.
3. **Expected values.** `data/SPEC.json` is re-derived by #645's discovery → `code/freeze_spec.py` → strict chain.

- **κ = 0.001652760598550299** (conservative 0.001652760595670246). That is +0.1987% over #645, +0.1008% over research/gauge44-repack and +0.0140% over research/gauge44-bit589 (0.001652528731617094). The complex side certifies 0.001655496738330440231813 and PR589's bit supplier gives 0.001733427039589844234749, so **the complex side binds**. Under PR543 this map would be bit-bound at 0.001651096360425895, so the gain over gauge44-repack rests on the PR589 citation (`PROOF-NOTE-BIT.md`, "Effect on the outer chain").
- **Evidence.** G44Pack2's strict replay with `verify_global.py` passes (`PASS_GAUGE44_STRICT_GLOBAL_REPLAY`, κ 0.001652760598550299), running this code and data. `RESULT.json` is that strict replay's `REPLAY.json`, converted to LF and otherwise unchanged. For this package, `data/SPEC.json` and a fresh `verify_global.py` replay are the binding record.
- **Independent price (ported).** `independent/price_profile.py` is G44Stack's port to PR589 (blob pin and an independently re-derived deficit). `independent/GAUGE44-INDEPENDENT-PRICE.json` is regenerated on this package's `data/PLAN.json`: `PASS_FROZEN_PROFILE_TWO_EXACT_ENGINE_AND_OUTER47_CROSSCHECK`, with κ equal to the strict replay. Rerunning `python -B independent/price_profile.py --main <main> --output <new>.json` reproduces it byte for byte.
- **Historical #645 evidence (PR543-based).** The following are #645's files, retained unchanged and **not** updated for this package: `LOCAL-VALIDATION.json`, `CONSTRUCTION.md`, `hosting/`, `evidence/`, and the rest of `independent/` (`audit_local.py`, `review_guards.py` and their receipts). They describe #645's owner map, PR543 supplier and κ 0.001649483702558979. No verifier reads them. `SOURCES.json` and `NOTICE.md` say the same.
- **Review.** Bit589Reviewer gave its final verdict, **SOUND** (after SOUND-WITH-FIXES, whose fixes were packaging and documentation only), on research/gauge44-bit589. It signs these files by their committed LF SHA-256, and this package ships them byte for byte:
  - `code/assemble.py` 1d4449ae65d92b21ca62ca50917ff0b74908542ada5d4687b54744dc9b9abc39 (changed from #645)
  - `code/bit_supplier_controls.py` e6d33fb61a570c3f50669412acc467a3fd06ef0b806da6a75bc296c6ba2142a5 (new)
  - `verify_global.py` 16bd5e54598592e92e210f99065348c5df261b8350fdc688072ce053d15b088a (changed from #645)
  - `independent/price_profile.py` d2f548ad6b99f64a8ca5fbaf822a89560bb99359957ce3420b497f6a46fc0acf (ported; not run by `verify_global.py`)

  The other 20 `.py` files are byte-identical to #645's. The reviewer re-traced all 12 controls on the gauge44 word (same sites, deficit 10272) and recomputed the outer chain under both suppliers. This package changes only the owner map and its re-derived expected values.
- **Line endings.** These files had CRLF in the admitted trees and are committed as LF only (`crlf.replace(b'\r\n', b'\n') == lf`, no lone `\r`):
  - `code/assemble.py`: CRLF ee717045f6e436fd…, committed (LF) 1d4449ae65d92b21…
  - `verify_global.py`: CRLF 58cd1b9a2276dde0…, committed (LF) 16bd5e54598592e9…
  - `data/SPEC.json` (from pkg/data/SPEC.json): CRLF d760bf2aff651f3a…, committed (LF) b970b9e3f757d958…
  - `RESULT.json` (from strict/REPLAY.json): CRLF 1fdb0dcd5ebdb4ec…, committed (LF) 759d603135420c5b…
  No verifier pins their bytes except `MANIFEST.json`, which is regenerated here. The bit input is pinned by its git blob and is unchanged.

Clean-clone verification, from the repository root (Python 3.11+, assertions on; prepare the pinned #635 supplier as in the #645 section below):

```sh
python -B research/gauge44-bit589b/verify_manifest.py
python -B research/gauge44-bit589b/construction/reproduce.py \
  --main . --pr635 /tmp/gauge44-pr635 --out /tmp/gauge44-bit589b-local --until phases
python -B research/gauge44-bit589b/verify_global.py \
  --main . --local /tmp/gauge44-bit589b-local/local --work /tmp/gauge44-bit589b-global
# kappa 0.001652760598550299
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
