# Joint three- and four-call owners: conditional κ = 0.001654192296855146

This improves the pinned [PR #656](https://github.com/CrocSwap/integer-mult-bounds/pull/656)
owner map from **0.001654108529511355** to **0.001654192296855146**, a
0.0050642% gain. The circuit, controller, bit supplier, and every inherited
verification and construction program are unchanged. This is an owner-only
delta against PR656, staged by the verifier in a temporary directory.

| Quantity | PR656 | This witness |
| --- | ---: | ---: |
| Conditional κ | 0.001654108529511355 | 0.001654192296855146 |
| Conservative κ | 0.001654108526615491 | 0.001654192293959223 |
| Helpers per call / calls | 492 / 72 | unchanged |
| Live / physical families | 7,168 / 7,670 | unchanged |
| Global paid rank / deficit | 520,704 / 2,560 | unchanged |

The exact exponent is `827096148427573/500000000000000000`.
The complex saving is `828466591481403378691/500000000000000000000000`;
the cited PR589 bit saving is `1733427039589844234749/1000000000000000000000000`.
The complex side binds.

## Contribution

Jay Mosley's [PR653](https://github.com/CrocSwap/integer-mult-bounds/pull/653)
releases two complete calls together. We extend that integer nomination model
to three and four calls: a family bucket records its free capacity and the
subset of selected calls allowed to use it. Variables assign at most one helper
of each selected call to a family. Exact width inventories and integer stop-loss
inequalities are imposed, then every nominated literal owner is checked again.

Starting at PR656, 180 three-call groups yielded eight strict improvements;
120 four-call groups yielded four more. The final idle remainders are
`{1:1, 3:1, 28:1, 32:2, 48:2398}`. Their distribution strictly majorizes PR656's
distribution at fixed total rank, improving every native homogeneous moment
with exponent in `(0,1)`. [PROOF.md](PROOF.md) gives the argument.
This bounded search does not establish global or neighborhood optimality.

The paid profile is:

```json
{"1":183025,"2":29808,"3":31249,"4":11088,"5":4032,"8":576,
 "28":1,"32":2,"48":2398}
```

We also supply an exact **relaxed packing ceiling** for this fixed local
profile and controller. Concentrating all 115,200 idle ranks into 2,400
dimension-48 remainders minimizes their moment even when the actual assignment
constraints are relaxed. Independent exact arithmetic bounds the corresponding
κ above by approximately **0.001654249113130438**. Feasibility of this ideal
packing is not claimed. This limits owner-only headroom; it does not bound
other circuits, controllers, local profiles, or integer multiplication in general.

## Reproduce

Python 3.11+ with assertions enabled; verification uses only the standard library.
Prepare the immutable inputs outside the checkout:

```sh
git fetch https://github.com/CrocSwap/integer-mult-bounds.git 0805e78f5fecc700804d4766d7e3e1d7d7e6a2ba
mkdir -p /tmp/layered-pr656
git archive FETCH_HEAD research/gauge44-layered-b | tar -x -C /tmp/layered-pr656
git fetch https://github.com/CrocSwap/integer-mult-bounds.git a6895a69f8ad98ab45777b03e9e6f48888c39f6f
mkdir -p /tmp/layered-pr635
git archive FETCH_HEAD research/complex-571-cold14-st2 | tar -x -C /tmp/layered-pr635

nice -n 15 python3 -B research/layered-joint-owners/verify.py \
  --main . --parent /tmp/layered-pr656/research/gauge44-layered-b \
  --pr635 /tmp/layered-pr635 --out /tmp/layered-joint-replay
```

The output directory must be new and outside input checkouts. Retained main
dependencies are pinned by hashes; the submission is based on main commit
`17ce0c79b7b51c2634b439ea5a2b754f09909693`. `SOURCES.json` pins the predecessor
commits and parent manifest. All parent source files and notices remain in the
staged copy. Only `data/PLAN.json`, `data/OWNERS.json.gz`, and `data/SPEC.json`
change there; the added staging receipt is bookkeeping.

Default verification rebuilds the scalar word and all layered ends, executes
the 30 pivot-swap and 59 layer-end controls, emits both native ledgers,
checks wrappers and phases, and independently audits all 716 scalar columns.
It strictly replays PR656, then independently re-derives the owner windows and
actual 73-column charts using that fresh baseline evidence. The owner audits
include nine mutations. Finally it strictly replays the new controller,
finite invoice, exact moments and outer assembly, including 15 controller,
69 admission and 12 bit-supplier controls, and independently prices the profile.
No optimizer or discovery mode runs during verification.

For incremental replay, `--local /path/to/rebuilt/local` accepts an existing
layered native directory including phases. The output explicitly records that
the local construction was not rebuilt in that invocation. Historical PR645
evidence retained by PR656 is never used as current local/owner evidence by
the new driver. Generated gzip artifacts are compared by inherited semantic
identities; immutable submitted inputs retain byte pins.

Optional nomination uses NumPy/SciPy (discovery: 2.5.4/1.18.1):

```sh
GAUGE44_PARENT=/tmp/layered-pr656/research/gauge44-layered-b \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
nice -n 15 python3 -B research/layered-joint-owners/search/group_owner_search.py \
  --owners research/layered-joint-owners/data/PR656-OWNERS.json.gz \
  --size 3 --groups 180 --seconds 2 --out /tmp/layered-triples
GAUGE44_PARENT=/tmp/layered-pr656/research/gauge44-layered-b \
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
nice -n 15 python3 -B research/layered-joint-owners/search/group_owner_search.py \
  --owners /tmp/layered-triples/OWNERS.json.gz \
  --size 4 --groups 120 --seconds 3 --out /tmp/layered-quads
```

HiGHS is limited to one thread. Timing and solver choices can change nominations;
the frozen owners and receipts, rather than repeatable optimizer decisions, are
the submitted witness. Both discovery receipts, the intermediate triple owner map, and bounded search
transcripts are retained under `data/`. A further bounded five-call pass
(30 groups, six seconds per group) accepted no moves; its transcript is retained
without a claim of neighborhood optimality. The final receipt compares to the triple endpoint;
the independent audits compare directly to PR656.

## Recorded validation

`VALIDATION.json` records a complete fresh Linux/Python 3.12.3 replay of the
default driver, including local construction and phases. Selected receipts and
all replay logs are retained under `evidence/`. The earlier `make verify` run
on the identical unchanged main base passed all 18 groups (including
`gen4-bank-verify`) and 84 isolated test modules; its receipt and compressed
log are retained with an explicit prior-run scope. The standalone addition is
validated by its new full replay, not by that earlier repository check.

## Scope and attribution

This remains conditional on the retained all-size compiler,
common-label/mutable-source realization, whole-call hosting, precision/tape,
exact-recovery, analytic-transfer, and bit H1–H5 interfaces. It is a finite
conditional witness, not an unconditional theorem or complete Lean proof.
The PR589 bit circuit is cited unchanged; its exact profile and exceptional
residue surcharge are freshly priced, but its circuit is not rebuilt here.

Prepared by **Jeremy Diviney**, with substantial **OpenAI Codex** assistance.
The multi-call search extends **Jay Mosley / jaymosley07's PR653** model; its
solver-free auditors and staging pattern are adapted with attribution. The
layered word and seed owners are **jeremykothe2's PR655/656**, prepared with
Claude Code. They build on **icekylinx's PR645 Gauge44**, with GPT-6 Astra and
Codex assistance, and the PR601/604/617/627/635/637 end-construction lineage,
including DreamingOfClouds, Jeremy Diviney and CarrierBypass. Earlier packing
work includes **vectorsss / Chi Zhao's PR638**. **DreamingOfClouds's PR589**
bit supplier retains its eumemic lineage and Claude attribution. All earlier
contributors, source-specific notices and Apache-2.0 licensing in the pinned
packages remain in force; see [NOTICE.md](NOTICE.md).
