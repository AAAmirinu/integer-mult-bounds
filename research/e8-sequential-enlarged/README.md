κ = 1.017776060460931e-3

# Checker-clean sequential gauges and enlarged entrances on the R781 E8 complex program

A conditional finite construction with **κ = 1017776060460931/10¹⁸ ≈ 1.017776060460931 × 10⁻³**.
- That is **+2.139·10⁻⁷ over eumemic's #410** (508781072593909/5·10¹⁷ ≈ 1.017562145e-3).
- It is +5.256·10⁻⁷ over rohanarun's #409 (1.017250501e-3) and +7.534·10⁻⁷ over eumemic's #408.

The complex side binds, with b = 254703245981514431773/2.5·10²³ ≈ 1.018812984e-3. The bit side is #404's (= #401's), unchanged: c ≈ 1.021539e-3 > b.

## Correctness note: #406, #408, #409 and #410 fail Sussman's checkers

We re-implemented all four words from their published data and reproduced their frozen hashes and their exact b and κ. Sussman's `gx.check1` **and** `gxcore` reject each of them:
- **E4, a pivot is the target of a gate reading y.** This comes from #404's 124/125 output-basis recovery, which all four inherit.
- With the recovery removed, `gxcore` still rejects two of them:
  - **#409: E5 at register 275** (and at 204 with its group [51] alone). Its own sequential groups [51] and [195] use half-coefficient pivots 1010 and 910. Their half-unit gauged dirt meets a later /2 gate, which leaves sixths.
  - **#410: E5 at register 947.** This is #404's pivot 555, which our #407 already re-pivots.

The word here passes `gx.check1` (E0–E7, exact scalar replay and gauged-dirt rule) and `gxcore` (sixths mirror). It also passes our flipped-sign and source-span controls.

## What changes

1. **Our #407 base.** #404's 194 shared-donor gauges with our four exact re-pivotings (555→748, 1019→958, 1020→1001, 585→636), #376's frame edit, and no 124/125 recovery.
2. **#410's eight entrance enlargements (eumemic), re-implemented.** A frozen pivot keeps its relation but moves to a one-pivot group on a strictly larger entrance space. Our `enlarge()` regenerates #410's `enlarged205.json` exactly from #408's selection and #410's change list. Pivot 1020 is re-pivoted in our base, so its enlargement is carried by the same relation pivoted at 1001 (the same roles, so the same admissibility).
3. **#409's four ordered sequential groups (rohanarun), re-implemented, two of them re-pivoted.** These are ten promoted pivots in the rank-1 entrances [51], [195], [204] and [240], prepended as 55 unit shears, with every source read before any entrance write to it.

   | group | pivot out → in | effect |
   |---|---|---|
   | [51] | 1010 → 739 | the gauged dirt stays in sixths (gxcore E5 at 204 removed) |
   | [195] | 910 → 531 | all three relations become integral (gxcore E5 at 275 removed) |

   Exact rank checks confirm that each group keeps its relation span.
4. **Padding fusion (our #394/#399/#407).** Sinks 301 and 387 each need −¼ of 1019 / 1020, which are even-coefficient donors after re-pivoting. Their final climbs absorb their banks' rank-1 padding.
5. **Target re-synthesis (our #402).** Targets 177 and 220 use our #402 designs, relocated onto the changed word as #406 does. The full raw operator is identical.

The full raw operator, with retained totals, equals #398's operator times the literal 555-gate entrance prefix on all 1,021 columns. All 204 gauged response columns are zero.

**Banks.** With 32 replicas the inventory per stage is {9:18464, 8:4896, 7:288, 5:608, 4:736}. It fills 2,943 width-73 banks (our greedy patterns, which reproduce #404's and #409's published patterns on their inventories), with 1,495 rank-1 paddings. The 64 fused occurrences own slot 0 of 64 distinct padded banks. Live stock is 57,207 and the deficit is 9,984.

Replica sweep: 16 replicas give 1.017733e-3, and 64 give exactly the 32-replica value, so #408's 64-replica banks add nothing here. #408's 205-pivot selection re-optimises the same rank-1 entrances ([51], [195], [204]) that #409 promotes into. It is therefore not orthogonal, and we keep #409's groups.

## Verify

    bash research/e8-sequential-enlarged/verify.sh --quick /tmp/e8s-q    # a few minutes
    bash research/e8-sequential-enlarged/verify.sh /tmp/e8s-full         # adds the regenerations of the #399/#402/#407 controls

This needs Python 3.11+ and the standard library only. The script:
- checks the manifest and the git-blob pins of every input from #390, #398, #401, #404, #408, #409 and #410;
- runs our #399, #402 and #407 pipelines as controls;
- runs `code/compose410.py`, which covers sections A to E of its docstring:
  - reproduces the #406, #408, #409 and #410 hashes;
  - reproduces #408's, #409's and #410's b and κ from our emission;
  - records the checker failures;
  - builds, checks and prices ours;
- runs `gx.check1`, `gxcore` and our flipped-sign and source-span controls on our word.

## Admitted conditions

- **Inherited and not re-run:**
  - two-sided residual normalisation and entrance-chart Gaussian phases, from #401/#404 and #409/#410 for their entrance spaces;
  - bank routes and owner injections;
  - the finite invoice;
  - the bit component, via #404's pinned `RESULT.json`.
- **Re-opened:**
  - the phases of the re-pivoted entrance tokens (four from #407, two new);
  - the 64 fused slots' owner placement;
  - the fused final climbs;
  - the 177/220 target edges and their scalar invoice.
- **Not re-checked here:** #407's sink-isolation premise (a_G = b_G = 0) on this word.
- We emit with #390's dirty-preconditioned bracket.

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **eumemic:** #410 (entrance enlargement, used here re-implemented) and #408 (205 shared-donor gauges and 64-replica banks, a control here).
- **rohanarun:** #409 (ordered sequential entrance gauges, used here re-implemented and re-pivoted), #406 (re-synthesis relocation), #405, #403, #400, #396, #395 and #387/#392 (bootstrap).
- **Dugongue:** #404 (shared-donor gauges), #401, #398 and #390.
- **applecrusher (#376):** the R781 substitutions and the frame edit.
- **jacklightChen (#377):** the nine-stage component.
- **#352:** the local invocation and emitter.
- **Jacob Sussman:** E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375, #381) and **utcorvusvolat-dotcom** (#370): the bit-side lineage.
- **DreamingOfClouds (PR #315):** the engines.
- **Ours:** #378, #394/#399, #402, #407 (re-pivoting), and here the checker fixes and the composition.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
