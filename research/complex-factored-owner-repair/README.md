# Owner repair on the two-factored-end K492 supplier

This package certifies conditional **κ = 0.001635877117861902**, exactly
`817938558930951/500000000000000000`, improving PR627 by
`0.000000127279804738`. The conservative rate is `0.001635877114991649`.

The two supplier words, scalar construction, recipes, dispatch of 64 JP8
and 8 CK calls, and all verifier code are unchanged from
[PR627](https://github.com/CrocSwap/integer-mult-bounds/pull/627), pinned at
`f95308a9afa5adc071fe75c8cd7feec172503d4f`. A coordinated reassignment of
18,250 owner placements changes the idle remainder profile to
`{1:44, 2:1, 3:2, 12:1, 16:3, 32:2, 48:2220}`.
There remain 35,424 hosted roles, 7,168 live families, 7,670 physical
families, rank mass 520,704 and deficit 2,560. The exact invoice prices
the combined profile; no separately estimated improvements are added.

## Verification

Python 3.11 or newer and a C++ compiler with Boost headers are required.
All six inherited source packages are vendored with their original pins:

```sh
bash research/complex-factored-owner-repair/verify.sh /tmp/factored-owner-fresh
```

The output directory must not already exist. The wrapper first checks
that WITNESS and EXPECTED reconstruct SPEC, then rebuilds all source and
provider chains and runs native arbitrary-input replay, reflected ledgers,
wrappers, phases, physical owner checks, finite invoice, both exact moment
engines and strict outer inequalities. It also checks 23 owner mutations,
114 assembly mutations, inherited supplier and generated-identity controls.
Finally a separate checker derives every width and paid child count from
actual native programs, checks every literal owner placement, and prices
the complete profile with a separate exact interval implementation.
Native program hashes must match the independently replayed PR627 words.
The sibling validation package retains complete fresh platform evidence.

The strict experimental admission explicitly reused our freshly checked
PR627 baseline and native receipts while rebuilding every construction
chain. The final portable replays are fresh and do not use that shortcut.

## Search and deterministic map reconstruction

A bounded 300-second three-bin dynamic-programming search used seed 627495
and a floating `sum(r*log(r))` nomination objective. It completed 19 strict
consolidations and 68,991 neutral moves. Floating scores do not certify
an exponent; the independent physical and exact global audits do.
The submitted placements are recorded explicitly in `data/OWNER-MOVES.json`:

```sh
python3 -B research/complex-factored-owner-repair/tools/replay_owner_map.py   --base-data /path/to/pinned-pr627/research/complex-571-cold14-k492b/data   --out /tmp/rebuilt-factored-owners
```

This deterministic exporter checks the pinned PR627 inputs, replays all
placement changes, regenerates compacted offsets, checks capacity and
family exclusions, and reproduces the submitted owner payload. It is not
an alternative to official admission. Supplier reconstruction and credits
remain in FACTORED-END.md, comparison/PR627-FACTORED-END.md and NOTICE.md.
The search is not an optimality proof and does not exclude larger schedules
or other supplier constructions.

## Conditional scope

All-size compiler, common-label and mutable-source realization, whole-call
hosting, precision/tape/exact recovery, and analytic transfer remain
assumptions. The cited PR543 bit supplier is repriced rather than rebuilt;
its surcharge and H1-H5 remain. This is not an unconditional multiplication
theorem, complete Lean proof, or practical speed measurement.

The unchanged factored suppliers are credited to Jeremy Diviney and all
predecessors retained in NOTICE.md. The owner-only repair and its validation
were prepared with OpenAI Codex for chafreaky.
