# Gauge44: conditional κ = 0.001649483702558979

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

## Construction

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

## Proof and evidence

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

## Incremental reproduction

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
