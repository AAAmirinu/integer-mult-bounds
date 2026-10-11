κ = 1.019752143318808e-3

# Checker-clean R779: our #424 layers on #426's word, gate-frame retimings and a target-172 prefix

A conditional finite construction with **κ = 127469017914851/1.25·10¹⁷ ≈ 1.019752143318808 × 10⁻³**. It is the best gx/gxcore-clean result we know of on the R781/R779 E8 line:
- **+9.85·10⁻⁷ over ai-nanachi's #426** (1.018766833e-3, checker-clean, the best clean claim when this was prepared);
- +1.06·10⁻⁷ over rohanarun's #429 (1.019646576e-3, price-only draft, built on #422's word, which keeps #404's 124/125 recovery and #411's quarter target-144 prefix; neither PR claims gx/gxcore acceptance);
- +1.24·10⁻⁶ over our #424.

For context, jacklightChen's #425 (κ ≈ 1.048005508e-3) uses a different Hamming-packet complex network under its own lemma in place of gx's source-immutability and target-read rules, so it is not comparable under Sussman's checkers.

The complex side binds, with b = 255198274817418511443/2.5·10²³ ≈ 1.020793099e-3. The bit side is #404's, unchanged: c ≈ 1.021539e-3 > b. Our #417 bit supplier (c ≈ 1.044e-3) would leave more headroom, but it is not needed here.

The word passes Jacob Sussman's `gx.check1` (E0–E7, exact scalar replay and gauged-dirt rule) and `gxcore` (sixths mirror), plus our flipped-sign and source-span controls.

## Construction (`code/compose426.py`)

1. **Input: #426's R779 gauged word** (ai-nanachi; pinned blob, used as data; #426's scripts are not run).
   - #426 inlines helpers 556 = −2(354+461) and 577 = −2(402+478) and rebuilds the #404/#412/#410/#409 gauge layer: 202 gauges.
   - Control: our emitter and price, at #426's 8 replicas and patterns, reproduce #426's complex coefficient and profile exactly.
   - Re-implementing the two substitutions directly on #398's signed R781 word (our #424 base) is frame-infeasible, so we start from #426's word.
2. **Our #424 layers, mapped to R779** (helper r → r − #{556, 577 below r}):
   - #414's group, #416's three promotions and our 947 re-pivot, #420's 672, and #421's 435/367: 52 literal shears, 213 gauges, operator identity on all 1,019 columns;
   - the 14 enlargements (13 of #423's and our 838);
   - fused sinks 301/387;
   - #402's 177/220 re-synthesis, relocated with restore source y221 (y180 would fail gx E4 in #426's signed layer);
   - our target-124 helper prefix.
3. **Fourteen fixed-scalar gate-frame retimings: 12 single gates and 2 five-gate blocks.**
   - The idea is eumemic's (#427/#428). The search and selection on our word are ours (`code/retime.py`, exact).
   - Thirteen bases coincide with #428's eleven and #427's two. The fourteenth (B1157 → rank 7) is new.
   - Scalar words and the raw operator are unchanged, and each retiming alone raises b.
4. **Target-172 prefix (ours, new).**
   - y172 is 125's partner in #426's signed layer. Its pre-cut writes are replaced by −h562/2 at frame 336, h358/2 at 904 (358's next frame), −h367/2 at 904 and −h280/2 at 724.
   - Protected columns are unchanged, and the histogram moves by {2:+1, 3:−2, 4:+1}.
5. **Price at 64 replicas.**
   - Inventory {9:36224, 8:9408, 7:1536, 5:1152, 4:1536}: 5,845 width-73 banks and live stock 114,045.
   - The 128 fused occurrences own slot 0 of distinct rank-1-padded banks.
   - Sweep 8 → 1.019662e-3, 32 → 1.019731e-3, 96 → 1.019745e-3, 128 = 64.

## Negative results on this word (exploration; see PROOF §25)

- **Promotions:** 1-, 2- and 3-donor promotions (5,659 candidates) found no gain.
- **Enlargements:** single, two-dimension, pair-joint and triple-joint enlargements (3,554 candidates) all break a final frame under closure.
- **Further inlining:** equal-helper aliases 672/447 and 674/471 are frame-infeasible.
- **Sinks:** the free sinks are still only 301/324/387, and 324 fails gxcore E5.
- **Prefixes:** an all-target prefix re-search finds only 124/172.
- **Retimings:** none are left after the fourteen.
- **Replicas:** 64 replicas (= 128) is the best T.

## Verify

    bash research/e8-r779-retimed-closure/verify.sh --quick /tmp/e8r-q    # about a minute
    bash research/e8-r779-retimed-closure/verify.sh /tmp/e8r-full         # adds the retiming-search regeneration

This needs Python 3.11+ and the standard library only. The script:
- checks the manifest and the git-blob pins;
- runs our #424 pipeline (`compose423.py`) as a control;
- runs `code/compose426.py` (sections A–F);
- runs `gx.check1`, `gxcore` and our controls on the #424 word and ours.

## Admitted conditions

- **Re-opened here:**
  - the phases of the 11 promoted gauges, the 14 enlarged entrance tokens, and the 39 raised and 22 retimed gate frames;
  - the 124/172 and 177/220 target edges with their changed ungauged dirt (the emitter recomputes the scalar response; the native invoice is not re-run);
  - the 128 fused slots' owner placement.
- **Inherited and not re-run:**
  - #426's Gaussian phases, routes and invoice for its R779 layer;
  - #401/#404 normalisation and entrance-chart phases;
  - the finite invoice;
  - the bit component, via #404's pinned `RESULT.json`.
- We emit with #390's dirty-preconditioned bracket.

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **ai-nanachi:** #426 (R779 helper substitutions, chronological gauge layer, the input word).
- **eumemic:** #427/#428 (gate-frame retiming idea and blocks), #423 (enlargements), #421, #420, #416, #414, #411 (target-prefix idea), #410 and #408.
- **rohanarun:** #429 (comparison), #422, #418, #415, #409 (sequential gauges), #406, #405, #403, #400, #396, #395 and #387/#392 (bootstrap).
- **Dugongue:** #404 (shared-donor gauges and bit supplier), #401, #398 and #390.
- **applecrusher (#376):** the R781 substitutions and the frame edit.
- **jacklightChen (#377):** the nine-stage component.
- **#352:** the local invocation and emitter.
- **Jacob Sussman:** E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375, #381) and **utcorvusvolat-dotcom** (#370): the bit-side lineage.
- **DreamingOfClouds (PR #315):** the engines.
- **Ours:** #378, #394/#399, #402, #407, #412, #419, #424, and here the R779 composition, the retiming search with the new B1157 retiming, the target-172 prefix and the negative screens.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
