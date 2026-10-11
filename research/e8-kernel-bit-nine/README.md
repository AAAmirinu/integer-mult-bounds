c = 1.044063934627389e-3 (bit side, B₄)

# A stronger E8 bit supplier in the nine-stage bridged word B₄: #376's R822 word with a randomised shared-donor kernel

This package is a bit-side supplier. In DaysSky's nine-stage layout (#381: B₄, unsplit idle climbs, halving degree two), its E8 bit word has coarse saving

**c = 1044063934627389/10¹⁸ ≈ 1.044063934627389 × 10⁻³**.

That is **+2.205 %** over the bit side used by #390, #401, #404, #407, #409 and #410: c = 255384852701747/(2.5·10¹⁷) ≈ 1.021539 × 10⁻³. Our engine reproduces that value exactly, as a control.

The frontier is complex-bound, so **κ is unchanged** with every cited complex supplier. This package raises the bit cap from 1.0215e-3 to 1.0441e-3. A complex side can now gain up to about 2.5 % before the bit side binds.

| bit word in B₄ (m = 72, unsplit, degree 2) | c | split at m/2 (degree 1) |
| --- | ---: | ---: |
| #370's word (= #381's bit) | 249162322049641/(2.5·10¹⁷) ≈ 9.966493e-4 | 9.570229e-4 |
| #376's R822 word (= #390 … #410's bit) | 255384852701747/(2.5·10¹⁷) ≈ 1.021539e-3 | 9.799513e-4 |
| **this word** | **1044063934627389/10¹⁸ ≈ 1.044064e-3** | **1000662258257099/10¹⁸ ≈ 1.000662e-3** |

| complex supplier (cited b) | b | κ (refined pricing tail) | binding |
| --- | ---: | ---: | --- |
| our #407 (`research/e8-repivot-fusion`, in this branch) | 1.017561149e-3 | 7941615395831/7812500000000000 ≈ 1.016526770666368e-3 | complex |
| eumemic #410 | 1.018598633e-3 | 508781072593909/5·10¹⁷ ≈ 1.017562145187818e-3 | complex |
| rohanarun #409 | 1.018286353e-3 | 508625250464133/5·10¹⁷ ≈ 1.017250500928266e-3 | complex |

The κ values equal those PRs' own claims. With #390's bit, the same code gives the same κ: a complex-bound κ does not depend on c.

## The word

1. **Input: #376's R822 word.** applecrusher's #376 (`research/e8-bit-helper-reuse`) applies to #370's word:
   - 128 frame edits;
   - 43 helper-lifetime reuses, which take R from 865 to 822.

   We rebuild it with our own code (`code/apply376.py`) from #370's word and #376's two pinned witnesses. Its canonical sha256 is #376's `9974db55…`. None of #376's code is run.
2. **Retiming.** Our descent (#287/#291/#299 lineage, via our #382) is scored at m = 72. On #370's word it moves 44 gates. On #376's word it finds **no move**, before or after the kernel: #376's 128 frame edits subsume it. No retiming stage is shipped.
3. **Shared-donor response kernel** (#272/#299/#319/#320/#329 lineage, our #382 stage), re-derived on the R822 word with the B₄ ledger.
   - resp(h) is the set of targets whose frame-0 completion reads read helper h.
   - An entry is a pivot p, an entrance E and donors D, with resp(p) = ⊕ resp(D) over F₂. E lies inside the first frame of p and of every donor.
   - p starts at E and loses its completion reads.
   - Each donor climbs to E at the start of A and adds its pivots there. After C it adds them again at FULL.
   - Pivots are never donors, and a donor serves one entrance.
   - **Selection:**
     - 182 entries with entrance ranks 1 and 4, and total rank 416 (≡ 0 mod 8);
     - 121 donor slots;
     - residual census {8: 640, 7: 104, 4: 78}.
   - **Packing.** The deterministic greedy packing of our #382 gives c = 1.030841e-3 here. Randomised packing does better:
     - entrance order key gain·(1 + NOISE·u), NOISE 10–20, best of many seeds: 1.03502e-3;
     - iterated local search, which drops a random 5–35 % of the entrance groups and re-packs with noise: **1.044064e-3**.

     The tools are in `discovery/` and are not run by the verifier.

## Verify

    BOOST_INCLUDE=/opt/homebrew/include bash research/e8-kernel-bit-nine/verify.sh /tmp/e8b9-full
    bash research/e8-kernel-bit-nine/verify.sh --quick /tmp/e8b9-quick

The checks need Python 3.11+ (standard library), a C++17 compiler and Boost headers. Steps:

0. `MANIFEST.sha256`.
1. Pinned inputs by git blob id: #370's word, and #376's `frame-selection.json` and `reuse-selection.json`. Our reconstruction of #376's word must hit #376's output sha256.
2. The kernel stage from its frozen selection, bound to the exact R822 word by content sha. Then the full exact replay:
   - legality: nested root-spanned frames, common gate frames, completion reads at frame 0, y at frame 0 at the scatter, the 9 retained totals at FULL, final frames;
   - **F₂ on all 1,062 local columns**, dirty helpers included;
   - the integer source-span rule.

   The rebuilt word must equal the shipped one. Five mutation controls are rejected.
3. Labels and the official checkers:
   - the 120 E8 root lines, and exact Gram determinants > 0 on all 943 nonzero frames (prime 2 only);
   - our export to PR249 records, and PR #266's official cohort legality at h = 8 with NCOPY = 9, whose paid histogram equals our replay. The unmodified NCOPY = 8 is rejected;
   - **our port of #266's columns checker to B_K, at K = 4:**
     - all **1,782 physical columns over F₂** through 9 invocations, 18 twin bridges and the terminal exchange;
     - all 18 omitted-bridge controls rejected;
     - prefix payload 61 bits < 104.

     In full mode, the K = 2 port must also reproduce the #266 five-stage receipt field for field.
4. The layout, banks and guard:
   - our B_K layout reimplementation gives #381's B₄ idle climbs [50] | [14, 7, 36] | [28, 7, 22] | [42, 7, 8];
   - **banks:** an exact width-72 tiling with T = 9 replicas (770 banks, #381's replica count), without padding;
   - **the halving-degree guard** (#375's form, at the bit parameters): m = 72, max child 50, t = 2 (72² > 2·50²), row coefficient 15,295 < 20,161, induction gap 43·B, m ≤ 72.
5. The pricing:
   - the bit c, unsplit and split, by both PR #315 engines with the 10⁻¹⁶ fallback, and the next grid point excluded. #381's and #390's bit savings are reproduced exactly as controls;
   - κ with each cited complex b, by our reimplementation of #392's refined pricing tail (`code/bootstrap.py`, from our #407): 47 strict constraints, with the next grid point and invalid parameters rejected.

## Admitted conditions and open obligations

- **Bit-side halving degree two** (unsplit B₄, max child 50 of 72), as #381 and #390 admit. Without it, the split value is c ≈ 1.000662e-3.
- **Kernel entrances.** σ > 0 for 182 pivots needs the entrance completion P_σ + (I − P_E) of our #329/#382 lineage. That completion is not re-proved for the E8 family.
- **#376's word.** We rebuild it and check it with our own replay and the official/ported checkers. #376's seven-stage receipts are not re-run.
- **#381's B₄ obligations are not re-run on this word:**
  - its PR234 route geometry on 9 blocks (`geometry_k.py`);
  - its finite bill at m = 72 (`finite_k.py`).

  The ports and isometries are #370's, and only helpers change.
- **Everything #370 admits:** 9 retained totals at h = 8, PR234's banks for a non-paired-cube family, and the inherited bit interfaces.
- **No Lean proof** of B₄, of this word or of its stages.
- **The complex values are cited**, not re-run here. #407's is re-run by `research/e8-repivot-fusion/verify.sh` in this branch.
- This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **applecrusher (#376):** the 128 frame edits and 43 helper reuses that give the R822 word. Its witnesses are vendored byte-identical, Apache-2.0, `data/pr376/LICENSE-pr376`.
- **DaysSky (#381, #363, #373, #375):** the nine-stage B₄ bit layout, B_K and the halving-degree-two guard.
- **Dugongue (#390):** first composed #376 with #381's layout.
- **utcorvusvolat-dotcom (#370):** the E8 bit word, its format and the generalised bit checkers.
- **Jacob Sussman:** the E8 family and the bridged word.
- **eumemic (#410), rohanarun (#409, #392):** the cited complex savings, and the refined pricing tail.
- **Our lineage:**
  - the shared-donor kernel, #272/#299/#319/#320/#329 via our #382;
  - PR #266's checkers (ported);
  - PR #315's engines and outer assembly (DreamingOfClouds).

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`). See `NOTICE.md`.
