κ = 1.013357935292321e-3

# Exact target re-synthesis on #401's response-subspace R781 E8 complex program

A conditional finite construction with **κ = 1013357935292321/10¹⁸ ≈ 1.013357935292321 × 10⁻³**.
That is +4.704783·10⁻⁸ (+0.0046 %) over Dugongue's #401 (101331088745971/10¹⁷ ≈ 1.013310887459710e-3).

The complex side binds. Its coarse saving rises from #401's b = 507169363968149971159/5·10²³ ≈ 1.014338728e-3 to **b = 1014385871264415626437/10²⁴ ≈ 1.014385871e-3** (+4.714·10⁻⁸).
The bit side is #401's, unchanged: c = 255384852701747/2.5·10¹⁷ ≈ 1.021539e-3 > b.

## What changes

The base is #401's word: #398's R781 signed-prefix word plus #401's 26 entrance response subspaces (119 gauged pivots, 240 unit entrance shears). `code/entrance.py` re-implements #401's construction and reproduces its frozen candidate hash (`3b78069c…`).

We **re-synthesise the B-phase feeds of two targets, y₁₇₇ and y₂₂₀.** Each target's feed list is replaced by a different exact rational combination of register values that are already present, read at frames where their registers already sit. These "tokens" can come from helpers, sources or another target's restored prefix. The frames of the new combination form a shorter or more unbalanced nested chain:

    y177, y220: climbs (3, 5) -> (6, 2)        local histogram {2:+2, 3:-2, 5:-2, 6:+2}

Both re-syntheses read y₁₈₀ at frame 892 at its existing restored cut, with a #398-style setup y_i −= y₁₈₀ at the start of B. The other deliveries are helper values at frames 892, 179 and 222. Every original feed gate becomes #398's source-touching empty marker, so no helper walk changes.

**Exactness.** The full raw rational operator is **identical** to #401's on every register and all 1,021 input columns, including every helper-dirt column. So #401's response block K, its 119 zero gauged columns and the retained totals are unchanged. `gx.check1` (E0–E7, including E7's gauged-dirt rule), the gxcore mirror and the source-span rule all pass.

**Discovery.** `code/search.py` runs an exact search over all 120 targets:
- It enumerates nested frame chains of length 1–3 that would beat the current climb partition under φ = Σ r ln r. The moment is concave, so merged or more unbalanced climbs are cheaper.
- It finds split positions with an exact breakpoint scan over token windows.
- It solves over ℚ, keeping the x-part, the y→y identity and all gauged dirt columns fixed.

Results:
- 27 targets could improve.
- 25 of them are #398 donors that an existing restore reads. Improving them would need their own destination as donor, which is circular.
- On #401's word, 151 and 157 need gauged-dirt tokens.
- That leaves exactly 177 and 220. `--regen` regenerates them.

**Padding fusion does not compose here.** On #401's word the only same-frame zero-row sinks are again 301/324/387. Each needs exactly a quarter of a #401-gauged register (1018/1019/1020), and the solution is unique. That leaves 1/4 of gauged dirt in the sink, which gxcore's sixths rule (E5) rejects. Fusion would otherwise add about +1.7·10⁻⁷. The full verifier records this as a negative check.

## Bracket

We emit and replay with #390's dirty-preconditioned bracket, as in our #399. On #401's unmodified word our emission reproduces #401's 24-digit complex root and κ exactly, which is the control. It passes the replay in both orientations on all 1,021 live columns.

Because the re-synthesised word has the same full raw operator as #401's, #401's own bracket also applies to it unchanged. That bracket is the complete old response K, the main word, the complete cleanup and the two-sided R₀⁻¹/L⁻¹ adapters. The scalar schedule of the two target walks changes, so Gaussian phases of the new target edges are admitted (see PROOF.md).

## Verify

    bash research/e8-response-resynth/verify.sh --quick /tmp/e8r-q     # ~1.5 min
    bash research/e8-response-resynth/verify.sh /tmp/e8r-full          # adds every regeneration (~4 min)

This needs Python 3.11+ and the standard library only. The script:
- checks the manifest and the git-blob pins, including #401's `selection.json`, `BANK-PATTERNS.json` and `RESULT.json`;
- re-runs our #399 pipeline as a control (#390 bracket regression, #398 b/κ, #399 κ);
- re-implements #401's word and checks its raw operator against #398's · diag(I, I, S);
- runs the sink negative check;
- applies the re-synthesis and checks it: operator identity, gx/gxcore, walks, histogram and mutation controls;
- replays the local program in both orientations on all columns;
- re-implements #401's bank patterns (748 banks per stage, 482 rank-1 + 1 rank-10 paddings);
- prices it: #401's b and κ as the control, then ours with both PR #315 engines, the 10⁻¹⁶ fallback and six bootstrap levels with 47 strict constraints.

## Admitted conditions

- **Inherited from #401 and not re-run:**
  - its two-sided normalisation, entrance-chart Gaussian phases, bank routes and owner injections, and finite invoice;
  - its bit component, used through its pinned `RESULT.json` bit coarse bound, as #401 itself does through receipts.
- **Inherited from #398 and earlier:** #398's R781 reconstruction (#376), #392's bootstrap, and #377's and #352's interfaces.
- **Re-opened:** Clifford/Gaussian-phase audits of the new target edges (0→892, 892→179, 892→222) and the changed scalar invoice. The changes are 10 helper→target deliveries, 2 target restores and 2 setups per invocation. No helper walk, bank or residual changes.

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **Dugongue:** #401 (response subspaces, two-sided normalisation, mixed-residual banks, used here as the base), #398 (signed target prefixes on R781, and the empty-marker and setup/restore form we reuse) and #390 (target prefixes, the dirty-preconditioned bracket, heterogeneous banks).
- **rohanarun:** #400 (R781 heterogeneous banks with padding fusion, re-implemented and composed in our exploration), #396 (the entrance response-kernel route #401 extends), #395, and #387/#392 (six-level bootstrap pricing).
- **applecrusher (#376):** the R781 helper substitutions.
- **jacklightChen (#377):** the nine-stage compressed component, banks and padding.
- **#352:** the local invocation, Clifford compiler and emitter.
- **Jacob Sussman:** the E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375, #381) and **utcorvusvolat-dotcom** (#370): the bit-side lineage carried by #401.
- **DreamingOfClouds (PR #315):** the engines and outer assembly.
- **Ours:** #378 (far retiming), #394/#399 (sinks, padding fusion, bracket transfer), and here the value-level target re-synthesis search, the re-implementation of #401's word and the checks.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
