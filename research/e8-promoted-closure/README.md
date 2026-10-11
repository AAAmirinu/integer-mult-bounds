κ = 1.017962405296845e-3

# Checker-clean grouped and frame-closure entrance promotions on the R781 E8 complex program

A conditional finite construction with **κ = 203592481059369/2·10¹⁷ ≈ 1.017962405296845 × 10⁻³**.
- That is **+1.644·10⁻⁷ over eumemic's #416** (1017798035290733/10¹⁸ ≈ 1.017798035e-3), the best open claim when this was prepared.
- It is +1.763·10⁻⁷ over rohanarun's #415, +3.015·10⁻⁷ over eumemic's #414 and +1.863·10⁻⁷ over our #412.

The complex side binds, with b = 254749927172825437387/2.5·10²³ ≈ 1.018999709e-3. The bit side is #404's (= #401's), unchanged: c ≈ 1.021539e-3 > b.

The word passes Jacob Sussman's `gx.check1` (E0–E7, exact scalar replay and gauged-dirt rule) and `gxcore` (sixths mirror), plus our flipped-sign and source-span controls.

## Correctness note: #414, #415 and #416 are not checker-clean

- All three keep #404's 124/125 output-basis recovery, which fails **gx E4** (a pivot is the target of a gate reading y; see #412).
- All three use #411's target-144 prefix, which delivers −¼·helper 255 first. That leaves y144's x-content in quarters, and `gxcore` rejects it (**E5 at register 144**; we reproduced this on our word). #411, #414, #415 and #416 state that they do not claim gx E5 acceptance.
- #416's raw 214-gauge entrance word (`closure214/discovery/replay/candidate.json`) already fails `gxcore` E5 at register 947, before any recovery or prefix. That is #404's pivot 555, which our #407 re-pivots to 748.

## What changes over our #412 (`code/compose416.py`)

1. **#414's grouped promotion (eumemic), re-implemented.** Helpers 766, 917, 627 and 948 become pivots together in the rank-1 entrance [48], with #414's nine-donor relations unchanged. They are prepended as literal unit shears.
2. **#416's frame-closure promotions (eumemic), re-implemented.** These are 892 → [51], 669 → [12] and 644 → [63], with #416's relations unchanged. Gate frames that no longer contain their operands' current frames are raised to the span and propagated (#416's rule, our code). This raises 5 frames on our word. Reverting any one fails gx E1.
3. **#416's 821 → [240], re-solved and re-pivoted.**
   - #416's relation uses donor 748, which is one of our pivots.
   - On our word the relation is unique on 821's other donors plus 555 and 947. It needs −½ on 947, which `gxcore` rejects (E5, register 947, recorded).
   - We pivot the same relation on 947 instead. The row 947 + 2·821 + 4·522 + 2·555 + 769 − 2·888 − 913 + 3·936 + 957 is integral, and gxcore passes.
4. **Target-124 prefix re-synthesis (our search; #411's prefix-window idea, itself adapted from our #402).**
   - Target 124's two B writes before its first positive-frame read are helper 358/2 at frame 485 and −helper 253/2 at frame 723.
   - They are replaced by helper 563/2 at frame 336 and −helper 253/2 at frame 723. The rewrite uses helper sources only, halves only, and no y source, so E4 and E5 are untouched.
   - The protected x, y and gauged columns of every row are unchanged. Only y124's and y171's ungauged dirt changes, and the emitter recomputes it.
   - 124's chain goes (3,4,1) → (2,5,1), worth +1.77·10⁻⁸.
5. **Kept from #412:** fused sinks 301/387, the 177/220 re-synthesis, #409's re-pivoted groups and #410's enlargements.

All 212 gauged response columns are zero. The full raw operator and retained totals equal #412's gauged word times the literal 48-shear prefix on all 1,021 columns.

**Banks.** With 32 replicas the inventory per stage is {9:18208, 8:5152, 7:288, 5:608, 4:736}. It fills 2,939 width-73 banks, with 1,459 rank-1 paddings. The 64 fused occurrences own slot 0 of distinct padded banks. Live stock is 57,171. Replica sweep: 16 replicas give 1.017919503e-3, and 64 give exactly the 32-replica value.

**What did not work** (exploration, not in the package):
- A sixths-legal form of #411's target-144 prefix. With 255 at frame 311 or 551 and 777/808 at frame 935, the coefficients are forced to quarters (the frame-935 helpers tie columns 12 and 26). Our bounded search (≤4 helper deliveries, ≤2 frames) found no sixths-legal alternative.
- An E4-legal 124/125 recovery. The 358/2 content is held at frame 904 only by y124, and any y→y link between 124 and 125 meets the existing 124→171 and 125→172 recoveries. No helper holds it at 904.
- Re-running #410's enlargement search on our selection finds no further enlargement. From scratch it re-finds exactly #410's eight.
- A screen of 319 single-pivot promotions at existing entrance spaces, each priced exactly, found none that adds on top.

## Verify

    bash research/e8-promoted-closure/verify.sh --quick /tmp/e8p-q    # a few minutes
    bash research/e8-promoted-closure/verify.sh /tmp/e8p-full         # adds the regenerations of the #399/#402/#407 controls

This needs Python 3.11+ and the standard library only. The script:
- checks the manifest and the git-blob pins of every input from #390, #398, #401, #404, #408, #409, #410, #414 and #416;
- runs our #399, #402, #407 and #412 pipelines as controls (#412 also reproduces #406/#408/#409/#410's hashes and their b and κ, and records their checker failures);
- runs `code/compose416.py` (its sections A–D);
- runs `gx.check1`, `gxcore` and our controls on #412's word and on ours.

## Admitted conditions

- **Re-opened by this package:**
  - the Gaussian phases of the 8 new entrance tokens (#414 group, #416 promotions, our 947 pivot) and of the 5 raised frames;
  - the target-124 edges, with its changed ungauged dirt (the scalar response is recomputed by our emitter; the native invoice is not re-run).

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

- **eumemic:** #416 (frame-closure promotions; 892, 669 and 644 used unchanged, and 821's relation re-solved and re-pivoted), #414 (grouped promotion [48], used unchanged), #411 (target-prefix re-synthesis idea), #410 (entrance enlargement, used here re-implemented) and #408 (205 shared-donor gauges and 64-replica banks, a control here).
- **rohanarun:** #415 (enlarged entrances with target prefixes, a comparison claim), #409 (ordered sequential entrance gauges, used here re-implemented and re-pivoted), #406 (re-synthesis relocation), #405, #403, #400, #396, #395 and #387/#392 (bootstrap).
- **Dugongue:** #404 (shared-donor gauges), #401, #398 and #390.
- **applecrusher (#376):** the R781 substitutions and the frame edit.
- **jacklightChen (#377):** the nine-stage component.
- **#352:** the local invocation and emitter.
- **Jacob Sussman:** E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375, #381) and **utcorvusvolat-dotcom** (#370): the bit-side lineage.
- **DreamingOfClouds (PR #315):** the engines.
- **Ours:** #378, #394/#399, #402, #407 (re-pivoting), #412, and here the 947 re-pivot, the helper-sourced 124 prefix and the composition.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
