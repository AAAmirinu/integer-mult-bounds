κ = 1.018509848057013e-3

# Checker-clean entrance enlargements, closure gauges and a target-125 prefix on the R781 E8 complex program

A conditional finite construction with **κ = 1018509848057013/10¹⁸ ≈ 1.018509848057013 × 10⁻³**.
- That is **+1.747·10⁻⁷ over eumemic's #423** (254583782466187/2.5·10¹⁷ ≈ 1.018335130e-3), the best open claim when this was prepared.
- It is +3.42·10⁻⁸ over rohanarun's #422 (1.018475695e-3, price-only draft), +6.20·10⁻⁷ over eumemic's #421 and +5.47·10⁻⁷ over our #419.

The complex side binds, with b = 254887067002137341481/2.5·10²³ ≈ 1.019548268e-3. The bit side is #404's, unchanged: c ≈ 1.021539e-3 > b.

The word passes Jacob Sussman's `gx.check1` (E0–E7, exact scalar replay and gauged-dirt rule) and `gxcore` (sixths mirror), plus our flipped-sign and source-span controls. #420, #421, #422 and #423 do not claim gx/gxcore E4/E5 acceptance. They keep #404's 124/125 recovery (gx E4) and #411's quarter target-144 prefix (gxcore E5), as #414–#416 did.

## What changes over our #419 (`code/compose423.py`)

1. **#420's closure gauge 672 → [48] and #421's rank-two gauges 435 → [304,111] and 367 → [259,246] (eumemic), with relations unchanged.**
   - They are re-implemented as literal unit shears with frame closure.
   - All 215 gauged response columns are zero.
   - The raw operator equals #412's word times the 52-shear prefix on all 1,021 columns.
2. **Fourteen one-dimension entrance enlargements.**
   - Thirteen are #423's (eumemic): 661, 695, 834, 835, 846, 851, 852, 858, 861, 863, 941, and the joint 914/960 → [48,12].
   - #423's 785 is not a gauge on our word; this is recorded.
   - The fourteenth is ours: 838 [204] → [304,204], found by an exact screen of all 819 one-dimension enlargements of our gauges inside their first gate frames.
   - No scalar instruction changes; the operator is identical on all 1,021 columns.
   - 29 gate frames are raised by closure, and reverting any one fails gx E1.
3. **Target-125 prefix re-synthesis (ours).**
   - y125's pre-cut writes (358/2 @485, 367/2 @904, −251/2 @724) are replaced by helper 563/2 @336, 367/2 @904 and −251/2 @724.
   - The 367 delivery runs at slot 975 while 367 is still between frames 485 and 904; it moves 367 to 904 early, and 367's next touch is at 904 anyway.
   - Only halves of integral helper rows are used, with no y source.
   - The protected x/y/gauged columns are unchanged.
   - 125's chain goes (3,3,1,1) → (2,4,1,1), worth +1.02·10⁻⁸.
4. **Price at 64 replicas.**
   - Inventory per stage: {9:36224, 8:9536, 7:1536, 5:1152, 4:1536}, giving 5,859 width-73 banks and live stock 114,171.
   - The 128 fused occurrences own slot 0 of distinct rank-1-padded banks.
   - Replica sweep: 16 → 1.018468e-3, 32 → 1.018488e-3, 128 = 64.
5. **Kept from #419:** everything (it runs as a control): #414's group, #416's promotions with the 947 re-pivot, fused sinks 301/387, 177/220 re-synthesis and the target-124 helper prefix.

## Target 144: no sixths-legal prefix in the searched space (PROOF §19)

**Search space.** We searched prefixes built from helper and x sources, delivered at the frame of the source's current or next touch, so no source's climb partition changes. Any number of deliveries was allowed, with up to four frame groups, and shift/restore among same-frame sources.

**Method.** Each chain gets an exact rational solve plus an integer-lattice test: each group's x/gauged total must lie in (1/6)ℤ, checked by Hermite normal form.

**Result for 144.** Only (3,4,1) via 311 → 935 and (4,3,1) via 551 → 935 are solvable, and both fail the lattice test. Every source at frame 935 has x₆ = x₁₂/2, while the target total has x₆ = x₁₂ = −½, so the early group must carry x₆ = −¼.

- y sources are excluded by E4, because 144 already reads y into 208.
- Across all 120 targets, 125 is the only new feasible form, and 144 is the only one blocked solely by sixths.
- Exploration scripts are not in the package.

## Other negative results

- **Further promotions.** A screen of all 933 one- and two-donor relations with denominators ≤ 2, at every existing entrance space inside the pivot's first frame, found no promotion that adds at 64 replicas.
- **Enlargement pairs.** Pairs among the legal single enlargements found nothing either.
- **#418/#422 (rohanarun):** these compose the same eumemic selections (#414, #416, #420, #421, #423) on #415's word, so there is nothing orthogonal to add.

## Verify

    bash research/e8-enlarged-closure/verify.sh --quick /tmp/e8e-q    # a few minutes
    bash research/e8-enlarged-closure/verify.sh /tmp/e8e-full         # adds the regenerations of the #399/#402/#407 controls

This needs Python 3.11+ and the standard library only. The script:
- checks the manifest and the git-blob pins of every input from #390, #398, #401, #404, #408, #409, #410, #414, #416, #420, #421 and #423;
- runs our #399, #402, #407, #412 and #419 pipelines as controls;
- runs `code/compose423.py` (sections A, A2, B, C, D);
- runs `gx.check1`, `gxcore` and our controls on #412's word, #419's word and ours.

## Admitted conditions

- **Re-opened by this package:** the Gaussian phases of the 3 new gauges, the 14 enlarged entrance tokens and the 39 raised frames; the target-125 edges with their changed ungauged dirt (the emitter recomputes the scalar response; the native invoice is not re-run); the 128 fused slots' owner placement at 64 replicas.
- **Re-opened by #419 and earlier packages:** the phases of the #414/#416 promotions, the 947 pivot and its raised frames; the target-124 edges; the phases of the re-pivoted tokens; the fused final climbs; the 177/220 target edges and their scalar invoice.
- **Inherited and not re-run:**
  - two-sided residual normalisation and entrance-chart Gaussian phases (#401/#404, #409/#410);
  - bank routes and owner injections;
  - the finite invoice;
  - the bit component, via #404's pinned `RESULT.json`.
- **Not re-checked here:** #407's sink-isolation premise on this word.
- We emit with #390's dirty-preconditioned bracket.

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **eumemic:** #423 (entrance enlargements, 13 used unchanged), #421 (rank-two gauges 435/367), #420 (closure gauge 672), #416 (frame closure and promotions), #414 (grouped promotion), #411 (target-prefix idea), #410 (enlargements) and #408.
- **rohanarun:** #422 and #418 (comparison claims), #415, #409 (sequential gauges), #406, #405, #403, #400, #396, #395 and #387/#392 (bootstrap).
- **Dugongue:** #404 (shared-donor gauges), #401, #398 and #390.
- **applecrusher (#376):** the R781 substitutions and the frame edit.
- **jacklightChen (#377):** the nine-stage component.
- **#352:** the local invocation and emitter.
- **Jacob Sussman:** E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375, #381) and **utcorvusvolat-dotcom** (#370): the bit-side lineage.
- **DreamingOfClouds (PR #315):** the engines.
- **Ours:** #378, #394/#399, #402, #407, #412, #419, and here the 838 enlargement, the target-125 prefix, the 144 lattice analysis and the composition.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
