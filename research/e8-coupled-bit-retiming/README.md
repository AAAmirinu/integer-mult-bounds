# Coupled E8 bit frames and an exact record update

Conditional candidate, October 11, 2026; maintainer review pending.

The fully replayed seven-stage bit / nine-stage complex composition gives

```
kappa = 998634658090834606116833 / 1000000000000000000000000000
      = 0.000998634658090834606116833
```

It exceeds PR #387's `998634657132636 / 10^18` by
`958198606116833 / 1000000000000000000000000000`, approximately
`9.58198606116833e-13` (relative `9.59509e-8 %`). This is a small exponent
improvement, not a measured runtime improvement. The headline gain applies
applecrusher's PR #376 exact assembly refinement to the freshly replayed
PR #384 retimed unit in PR #377's complex supplier; it is **not attributed to
the new bit frames**. This package also freshly supplies the certificate-specific
physical, Clifford and finite checks left open in PR #384, using the derivation
pattern of Rohan Arun's PR #385.
It also adopts PR #387's smaller beta=10^-18 while retaining eight bootstrap
steps, eta=10^-24 and the 10^-27 grid; all new strict cutoffs and zero/unit
parameter controls are checked.

The new contribution on the bit side is deterministic coalescence of connected
one-, two- and three-gate groups, applied after PR #376's 43-helper reuse.
Seventy accepted moves change 98 distinct scalar gate frames. Scalar gate
order, sources, destinations, copied totals, endpoint frames and helper count
remain fixed. An exact interval argument proves the cost decrease including
fallback charges; independent physical checkers establish legality.

The chosen layout is PR #381's unsplit `B_3`, with seven stages, dimension 56,
seven literal replicas, 822 helpers, 10,794 stock and halving degree two.
The candidate's exact bit coarse saving is `63613071872999 / 62500000000000000`.
Both the unchanged reused word and the improved word exceed the complex cap.
Their final refined kappas are therefore equal. The separate bit improvement,
baseline comparison and finite coefficient are in [the expected record](data/EXPECTED.json).

## Reproduce

Requires Python 3.13 or 3.14, Bash, a C++17 compiler, Boost headers and the pinned
Python dependencies. There is no network lookup in the verifier.

```sh
python3 -m pip install -r research/e8-coupled-bit-retiming/requirements.txt
make e8-coupled-verify
```

Or choose an absent output directory outside this package:

```sh
python3 -B research/e8-coupled-bit-retiming/verify.py /tmp/e8-coupled-fresh
```

The command verifies both manifests, runs the **entire** pinned PR #375
supplier suite and its historical regressions, regenerates the reused and
retimed words, exports records, compiles native checkers, checks all 1,062 local
and 1,542 global dirty columns, rejects corrupted words/records/bridges,
checks all 120 port geometries and routes, checks literal banks, runs all eight
original PR #377 stages, fully replays PR #384's changed unit and its new
Clifford frames and finite invoice, compares the common finite envelope, computes both
moment engines, recomputes the finite invoice, and checks the refined assembly
and adjacent rejected tick. It finishes only if the result equals the frozen
expected record. Stored PASS receipts cannot replace those steps.

Windows may specify `--shell /path/to/sh.exe --boost-include /path/to/boost`;
the compiler and its runtime libraries must be on PATH. The small transport
adapters resolve the interpreter, LF writes and native filename encoding.
All scientific supplier files are byte-identical to their pinned commits.

`make e8-coupled-record-check` checks the repository's
[candidate record](../../certificates/candidates/e8-coupled-bit-retiming.json)
against this package and its exact numbers. The repository's reviewed selected
result has a separate review status.

## Exploration and limits

[The campaign](campaign/REPORT.md) records 25 bounded trials, five promising
families, coupled group searches and the final reuse/layout adaptation. Float
entropy scores guide discovery only. The accepted result uses rational
arithmetic and two independent moment engines.

This is a finite **conditional** witness. It retains the upstream all-size
compiler, charts, recursive supplier, compressed Clifford windows, correlated
banking, Gaussian precision/recovery, routing, restored-row and analytic
transfer obligations. It does not prove the complete multiplication theorem
in Lean. See [PROOF.md](PROOF.md) and [NOTICE.md](NOTICE.md).

Prepared by ai-nanachi with substantial OpenAI Codex assistance; Apache-2.0.
