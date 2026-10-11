κ = 1.002661106042177e-3

# Bank padding fused into clean-sink helper climbs, on #398's signed target-prefix R781 E8 complex program

A conditional finite construction with **κ = 1002661106042177/10¹⁸ ≈ 1.002661106042177 × 10⁻³**.
That is +1.66446412313·10⁻⁷ (+0.0166 %) over Dugongue's #398 (125311832453733/1.25·10¹⁷ ≈ 1.002494659629864e-3).

The complex side binds. Its coarse saving rises from #398's b = 31359395740192012461/3.125·10²² ≈ 1.003500664e-3 to **b = 1003667444352030197427/10²⁴ ≈ 1.003667444e-3** (+1.66781·10⁻⁷).
The bit side is our #382 word, unchanged, with c ≈ 1.006907e-3 > b. #398's bit c gives the same κ.

## What this composes

- **#398 (Dugongue)** applies 25 signed disjoint target-prefix pairs to #376's R781 word (781 helpers, T = 8 replicas, one rank-1 padding per whole bank).
- **Our #394** fuses a bank's rank-1 padding C₇₂ into the final climb of a free zero-row sink helper in that bank (rank 2 + rank 1 → rank 3). See `PROOF.md`.

**Fusion does not apply under #398's own bracket.** #398 keeps #352's frozen old response K followed by the full cleanup of the non-y word at FULL. `clean.py` checks that every one of the 781 helpers is the target or source of some non-y gate. Each helper is therefore touched by the cleanup after its final climb, which a fused padding forbids.

**It applies once the bracket is #390's.** We compile #398's word with #390's dirty-preconditioned bracket instead: target precancellation y −= B·A⁻¹·h, helper prewhitening, and FULL repair of N_r·x for non-sink helpers only. #390 introduced this bracket. Our re-implementation reproduces #390's `prewhite.json` on #390's own word.

On #398's word the new bracket costs nothing:
- the emitted paid local histogram equals the word's histogram;
- #398's own b and κ are reproduced exactly from our emission.

The free-sink search over all 773 lifting helpers of #398's word finds exactly **301, 324 and 387** (final lift rank 2, frames 731/744/759, cuts 1974/2005/2040). For 301:

    h276 += h1019/2;  h301 −= h276/2;  h276 −= h1019/2

Under #398's bank rule, bank and slot are divmod(rep·781 + r, 8). The 24 fused occurrences per stage fall in 24 distinct banks, and every slot route fixes coordinate 72. Paddings per stage drop from 781 to 757:

    profile delta vs #398 = {1: −216, 2: −216, 3: +216}   (live 14,709, deficit 2,496, max child 48 unchanged)

## Verify

    bash research/e8-clean-r781/verify.sh --quick /tmp/e8c3-q     # ~1 min
    bash research/e8-clean-r781/verify.sh /tmp/e8c3-full          # adds the free-sink regeneration (~3 min)

This needs Python 3.11+ and the standard library only. No C++ or Boost is needed. The script:

1. Checks `MANIFEST.sha256` and the git-blob pins of all inputs: #398's `signed25.json.gz` and `VALIDATION.json`; #390's prefix18, sink-audit and prewhite; #378's word; Sussman's gx; and #382's bit word.
2. Bracket regression: on #390's own word, our compiler reproduces `prewhite.json` gate for gate.
3. Words:
   - `gx.check1` (E0–E7, exact scalar) and the gxcore mirror pass on #398's word and on ours.
   - #398's x → (x, y) operator equals #378's.
   - The all-helpers-touched check confirms that #398's own bracket excludes fusion.
   - Ours keeps the paid histogram, x/y operator rows and retained totals of #398's word, and the three sink rows are exactly zero.
   - Full mode only: the free-sink search regenerates exactly our gates.
4. Local program: #398's word and ours are replayed in both orientations on all 1,021 live columns. Five mutation controls are rejected.
5. Banks: distinct fused banks, and coordinate 72 is fixed.
6. Price, with #398 as the control. #398's 24-digit coarse root (both PR #315 engines, 10⁻¹⁶ fallback) and its κ are reproduced exactly from our emission. The κ uses the #392/#398 six-level bootstrap with PR #315's outer assembly (47 strict constraints, next grid point rejected). Ours is priced the same way.
7. Runs `cxcheck` (gx, flipped-sign control, source-span rule) on #398's word and on ours.

## Admitted conditions

- **Re-opened, with the argument in PROOF.md:**
  - #398's literal K/cleanup bracket is replaced by #390's bracket. This is checked here on all columns in both orientations, but #398's Clifford/phase and finite-invoice audits were run for its own bracket;
  - #377's padding as a separate sweep, for the 24 fused banks per stage.
- **Inherited and not re-run:**
  - #398's R781 reconstruction (#376's helper substitutions), its Clifford edge and phase audits, global template and finite invoice (row coefficient 15,445 < 20,161). We add 9 scalar helper gates per invocation; the bracket uses 1,551/7,776 pre-helper/post-repair gates;
  - #392's bootstrap argument;
  - #377's and #352's interfaces;
  - #382's bit claims.

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **Dugongue:** #398 (the signed target-prefix construction on R781 and its bank/invoice composition) and #390 (the target-prefix mechanism and the dirty-preconditioned bracket used here).
- **applecrusher (#376):** the R781 helper substitutions and frame repairs.
- **rohanarun:** #392/#387 (six-level bootstrap pricing) and #395 (signed prefixes).
- **jacklightChen (#377):** the nine-stage compressed component, banks and padding.
- **#352:** the local invocation, Clifford compiler and original emitter.
- **Jacob Sussman:** the E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375, #381) and **utcorvusvolat-dotcom** (#370): the bit-side lineage.
- **DreamingOfClouds (PR #315):** the engines and outer assembly.
- **Ours:** #378 (far retiming, the base of R781), #382 (bit word), #394 (padding fusion and free-sink search), and here the bracket transfer to #398's word and the checks.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
