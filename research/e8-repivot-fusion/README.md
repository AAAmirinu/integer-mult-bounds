κ = 1.016526770666368e-3

# Gauge re-pivoting, padding fusion and target re-synthesis on #404's shared-donor R781 E8 complex program

A conditional finite construction with **κ = 7941615395831/7812500000000000 = 1016526770666368/10¹⁸ ≈ 1.016526770666368 × 10⁻³**.
That is +1.044502·10⁻⁷ over Dugongue's #404 (1016422320428301/10¹⁸) and +5.71·10⁻⁸ over rohanarun's #406 (1.016469657190768e-3).

The complex side binds. Its coarse saving rises from #404's b = 254364121477661453089/2.5·10²³ ≈ 1.017456486e-3 to **b = 508780574407464422817/5·10²³ ≈ 1.017561149e-3**.
The bit side is #404's (= #401's), unchanged: c = 255384852701747/2.5·10¹⁷ ≈ 1.021539e-3 > b.

## What changes

**1. #404's word, re-implemented.** `code/entrance404.py` rebuilds #404's 194 shared-donor entrance gauges on #398's signed781 word, its 124/125 output-basis recovery and #376's frame edit. It reproduces both of #404's frozen hashes (`65b0f9dd…`, `d18ccdc5…`). Our emission of that word under #390's bracket reproduces #404's 24-digit b and κ exactly; this is the control.

Sussman's checkers reject #404's word as published:
- gxcore E5 (sixths) at register 947: pivot 555's relation has five half-coefficient donors, and their half-unit gauged dirt later meets a /2 gate;
- gx E4 at target 125: the 124/125 recovery makes 125 both a y-pivot (of its inherited 125 → 172 restore) and a target of a y-reading gate.

**2. Re-pivoting (new).** A response-gauge plan is a set of relations e_p + Σ c_{p,d} e_d on target-response columns. Any other choice of pivot columns spanning the same relations zeroes the same response space, so the raw operator is still M₃₉₈ · diag(I, I, S′) with every pivot column zero. The choice of pivot is what decides denominators and which register carries which gauged dirt. We swap four pivots (`data/repivot-e8.json`, `code/repivot.py`):

| plan | pivot out → in | why |
|---|---|---|
| 28 | 555 → 748 | all coefficients become integers, so the gxcore E5 failure at 947 disappears |
| 0 | 1019 → 958 | 1019 becomes a donor with coefficients −2, −2 |
| 5 | 1020 → 1001 | 1020 becomes a donor with coefficients −2, −2 |
| 27 | 585 → 636 | sink 387's inverse column no longer meets a gauged coordinate |

The 124/125 recovery is left out, because it fails E4. That costs #404's {1:+1, 3:−1, 4:−1, 6:+1}. The price is otherwise invariant under re-pivoting: the base is −5.69·10⁻⁸ below #404, all of it from the omitted recovery.

**3. Padding fusion (our #394/#399), now composable.** On the base, the only same-frame zero-row sinks are again 301, 324 and 387. Each needs exactly −1/4 of one helper (1019, 1018 and 1020 respectively), and no solution exists without that helper.
- On #401's and #404's gauges, 1019 and 1020 are pivots, so a quarter of their unit dirt breaks the sixths rule.
- After re-pivoting they are donors with even coefficients, so a quarter of their dirt stays in sixths. Sinks 301 and 387 are fused, with #394's sixths rewrite and with no climb change.
- 324 stays unfused. Its 1018 is the only donor of pivot 941 (relation e₉₄₁ + e₁₀₁₈), which leaves nothing to re-pivot.
  - Ungauging 941 needs a 739th bank, which is a net loss.
  - An advanced-donor uncompute of 324 exists, but it prices at −3.1·10⁻⁷.
- We also check the premise of #404's research note on sink isolation. For both fused sinks, a_G = 0 (row of the helper matrix A) and b_G = 0 (b = A⁻¹e_s) on all 194 gauged coordinates, with b_s = 1/2. Under #404's gauges, b_G was {1019: −4} for 301 and {585: −1, 1020: −4} for 387.

**4. Target re-synthesis (our #402).** Targets 177 and 220 climb (6, 2) instead of (3, 5). The full raw operator is identical.

**Banks.** We use #404's patterns: 738 banks per stage and 394 rank-1 paddings. The 16 fused occurrences (two sinks × 8 replicas) own slot 0 of 16 distinct rank-1-padded banks, with the padding on coordinate 72, so paddings per stage go from 394 to 378.

Profile delta vs #404: {1:−216, 3:+72, 4:+72, 5:−144, 6:+72}, with live 14,322, m = 73 and deficit 2,496.

## Verify

    bash research/e8-repivot-fusion/verify.sh --quick /tmp/e8p-q    # ~2 min
    bash research/e8-repivot-fusion/verify.sh /tmp/e8p-full         # adds every regeneration (~5 min)

This needs Python 3.11+ and the standard library only. The script:
- checks the manifest and the git-blob pins, including #404's `selection194.json`, `bank-patterns.json` and `RESULT.json`;
- runs our #399 and #402 pipelines as controls;
- runs `code/fusion404.py`, which covers sections A to G of its docstring;
- runs Sussman's `gx.check1` and `gxcore` plus the flipped-sign and source-span controls on our word.

## Admitted conditions

- **Inherited from #404/#401 and not re-run:**
  - two-sided residual normalisation and entrance-chart Gaussian phases, applied to the same 37 entrance spaces and the same pivot dimensions;
  - bank routes and owner injections, except the 16 fused occurrences' slot ownership;
  - the finite invoice;
  - the bit component, via #404's pinned `RESULT.json`.
- **Re-opened:**
  - the phases of four re-pivoted entrance tokens (a pivot and a donor of the same plan exchange roles; the entrance spaces are unchanged);
  - the 16 fused slots' owner placement;
  - the fused final climbs;
  - the 177/220 target edges and their scalar invoice.
- We emit with #390's dirty-preconditioned bracket. #404's own wrapper bracket is not claimed for the fused sinks, but its sink-isolation premise holds (see 3).

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **Dugongue:** #404 (shared-donor gauges, the base here, re-implemented from its data), #401 (response subspaces, two-sided normalisation, mixed banks), #398 (signed prefixes) and #390 (the dirty-preconditioned bracket).
- **rohanarun:** #406 and #405 (re-synthesis compositions), #400, #396, #395 and #387/#392 (bootstrap).
- **applecrusher (#376):** the R781 helper substitutions and the 203 → 942 frame edit.
- **jacklightChen (#377):** the nine-stage component.
- **#352:** the local invocation and emitter.
- **Jacob Sussman:** E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375, #381) and **utcorvusvolat-dotcom** (#370): the bit-side lineage.
- **DreamingOfClouds (PR #315):** the engines.
- **Ours:** #378, #394/#399 (sinks, padding fusion), #402 (target re-synthesis), and here gauge re-pivoting and the checks.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
