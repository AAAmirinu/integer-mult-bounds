# Six more cold ends on the layered gauge word

**Conditional kappa = 0.001654269575689572** (`413567393922393/250000000000000000`). This improves independently replayed PR656 (`0805e78f5fecc700804d4766d7e3e1d7d7e6a2ba`, kappa0.001654108529511355).

The witness retains PR655/656's six pivot swaps, eight entering-end extensions and54 cold ends, adds six cold dimension-eight ends, and constructs a whole-owner assignment whose only idle children are **2,409 rank48 children**. The complex side binds. PR589's bit supplier, its derived deficit and exceptional-residue surcharge remain unchanged.

| Quantity | PR656 word | This word |
|---|---:|---:|
| Helpers |492|492|
| Cold ends |54|60|
| Local rank mass |5632|5626|
| Residual width mass |3776|3770|
| Width inventory |4:52,5:48,7:42,8:116,9:234|4:52,5:48,7:42,8:122,9:228|

The new raw helpers are519,580,581,582,590,591. Their profile change is `{1:+6,2:+12,3:-12}`. The global profile is `{1:183456,2:30672,3:30384,4:11088,5:4032,8:576,48:2409}`, with rank mass520704 and deficit2560. The exact complex lower endpoint is `1657010718107129084353/10^24`; the bit endpoint is `1733427039589844234749/10^24`.

## Reproduce

Python3.11+ and the standard library suffice. No network, optimizer or third-party Python package is needed:

```bash
bash research/complex-layered-cold60/verify.sh /tmp/layered-cold60-fresh
```

Use a new output directory outside the package. Set `LAYERED_COLD60_PYTHON` to select Python. Assertions must remain enabled; allow several minutes.

The driver freshly replays the PR558 ancestor and checks every pinned ancestral input consumed by global admission. It reconstructs gauge44, derives its cold recipe again, rebuilds the six-pivot layered word and its30 pivot/59 layer controls, then applies the frozen60-end recipe. The final word passes all716 arbitrary-dirt columns in both orientations, native phase identities, residual wrappers,59 inherited end mutations and30 focused mutations for the six new ends. Global verification includes69 admission mutations,12 bit-supplier mutations, two exact moment engines and47 strict outer constraints.

An independent scalar/frame/cone checker and a separate native-width/literal-owner/rational-moment checker must agree. The 10KB integer pattern-flow/slot certificate reconstructs all35,424 owner roles byte-for-byte and rejects7 corruptions. The optimizer is neither trusted nor run by verification. `PROOF.md` explains the construction and fixed-word packing optimum; `PROVENANCE.md` identifies sources.

Historical provider identifiers and recipe metadata are retained for compatibility. The recipe's60-element cold-end list, constructed word and independently recomputed frames/profile are authoritative. Historical upstream records live under `provenance/`, separate from this witness's receipts.

## Scope and weakest steps

This is a finite exact conditional witness, not an unconditional multiplication theorem, practical speedup, or kappa=1. All-size compilation, common-label/mutable-source realization, complete-invocation hosting, precision/tape accounting and analytic transfer remain inherited obligations. PR589's punctured bit-unit and interleaved-interface assumptions remain. The command exactly reprices its pinned bit record; a separate complete bit-circuit replay is retained in the companion validation package.

Full-48 packing attains the exact moment optimum for this fixed word,72-call dispatch and inherited idle capacities. It is not a bound on other words, schedules or algorithms.
