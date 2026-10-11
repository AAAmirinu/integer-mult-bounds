# Coupled frame retiming after PR364

Conditional kappa **160987957846297 / 200000000000000000**, or
**0.000804939789231485**, improves frozen PR364's
0.000804879370798932 by **0.007506520200%**.

The construction changes 123 ADD frames in 35 coupled components of the final
Design T/min-cost-carrier word. All signed scalar instructions, their order,
registers, COPY windows and entrance/exit frames are preserved. The local paid
call count falls by 17; rank mass and helper stock are unchanged.

This is a conditional finite-word improvement. The compiler, common-chart,
restored-row, selector/routing, prime-supply, precision/recovery and analytic
transfer interfaces remain inherited. It is not an unconditional integer
multiplication theorem, a global optimum, or a new Lean certificate.

## Reproduce

```sh
python -m pip install -r research/w3-design-t-mc-coupled-retiming/requirements.txt
python -B research/w3-design-t-mc-coupled-retiming/verify.py /fresh/output
```

The output must be new and outside the package. Use `--cxx` and
`--boost-include` if the compiler or Boost headers are not in their default
locations. Assertions must remain enabled. Paths containing spaces are
supported. Completed intermediate snapshots are archived losslessly inside
the output directory to reduce disk use.

The verifier checks every package hash and the unchanged upstream manifest;
reconstructs PR364's Design T, twins, kernel, retiming and reorders; verifies
the exact source and output record hashes; reconstructs the new retiming;
compares the signed scalar instruction sequences byte for byte; replays all
formal F2 columns, source spans, nested frame paths and arbitrary dirty helper
restoration; checks new frame ranks and nondegeneracy, exact bank tiling,
independent native legality and all five-stage columns; repeats the PR346
historical control and unchanged E8 complex supplier checks; and certifies
the new bit saving and all 47 outer inequalities with two rational moment
engines, rejecting the adjacent kappa tick.

`source/` is an unchanged standalone snapshot of PR364 at
`f8c6a47abfec24b87cb1eb0a138dd73dfce2abe4`.
Its original manifests, licenses, attribution and disclosures are preserved.
`selection.json` is the new source-bound witness. `EXPECTED.json` pins the
final word, paid histogram and exact kappa. The receipts distinguish the
independently completed baseline replay from the changed-word validation.

## Discovery and limits

The prior campaign's free-form annealer was applied to PR364's actual final
word, with seed 1, initial temperature 2 and 432 seconds of annealing. It
tested 50,422,591 proposals and returned 322 changed frames. We then separated
changes into components connected by consecutive register uses, computed
each component's exact rational moment delta at the baseline bit exponent,
and retained only the 30 strictly beneficial components. This reduction
improved the result over retaining the whole annealed assignment. A separate
180-second CP-SAT solve over a finite frame universe returned a feasible,
nonoptimal assignment that was worse as a whole. The same exact component
reduction extracted 20 beneficial components. Five of those, comprising 24
gates, have no changed-gate adjacency to the annealer's retained components.
We compose those five with the first 30, then re-emit and reprice the entire
word. No global frame optimality is inferred from this bounded solve.

The retained changes lower 71 category-12 gate frames from dimension 13 to 12,
and 52 from 15 to 14. There are 53 newly registered frames. These are coupled
changes: legality is checked on the simultaneous assignment, not inferred
from a sequence of individually beneficial gate moves.

A separate low-temperature run found no gain. An expanded commuting-ADD
screen tested 84,214 placements around 19,914 boundary gates and found no gain;
removing its incidence-distance cutoff produced the same census. Those
negative results apply only to the tested move classes.

The bit side still binds. Sussman's E8 complex saving remains exactly
876248285600677 / 10^18. No supplier improvements or published kappa gains
are added arithmetically.

The repository-level PR also includes the unchanged three-file pin repair
from PR318 at `a45747d2559141a594916475f52642e4fab86e02`, whose pinned inputs
were checked against current main. This repairs the inherited joint-dual CI
failure without altering its mathematics.
