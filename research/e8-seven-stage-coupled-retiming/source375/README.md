κ = 9.5424356568133e-4

# Seven-stage E8 bit and complex suppliers, with the complex idle climbs at halving degree two

This package gives a conditional finite construction with **κ = 95424356568133/10¹⁷ ≈ 9.5424356568133·10⁻⁴**:

- +2.40 % over PR #373 (9.3191395651209e-4), which it extends;
- +9.00 % over PR #370 (8.75481145306751e-4).

Everything is PR #373's, with one change on the complex side. PR #363 split the complex supplier's two longest idle
climbs below m/2, 38 → 31 + 7 and 32 → 31 + 1, to meet the half-shrink guard of the inherited finite bridge
(2 · max child < m). Here they are **left whole**. The largest complex child is then 38 of m = 63, so one recursion level
no longer halves the size, but two do: 63² = 3969 > 2 · 38² = 2888, which is **halving degree two**.

| side | supplier | layout | coarse saving |
| --- | --- | --- | ---: |
| bit | PR #370's E8 bit word `bitE8-r865`, unchanged (PR #373) | B₃, split (max child 27 of 56, degree 1) | c = 968197503705007/10¹⁸ ≈ 9.68197503705007·10⁻⁴ |
| complex | Sussman's E8 unit `gcert1-e8-r783`, unchanged | B₃, **unsplit** (max child 38 of 63, degree 2) | b = 119394377245827/(125·10¹⁵) ≈ **9.55155017966616·10⁻⁴** |

The bit side is 1.4 % above the complex side, so **the complex side binds**. κ is the complex-bound assembly of PR
#315's `outer.assembly`: all 47 constraints hold, the complex leaf cap itself is rejected, and the adjacent 10⁻¹⁸ grid
point is rejected. The bit word, its seven-stage checks and the circuit of the complex unit are unchanged from PR #373.
That includes the Lean binding of Sussman's `wht_main_block_B2Ge8x`.

## Halving degree two

The half-shrink guard is used once in the inherited complex finite bridge
(`code/complex/inputs/complex/retained/FINITE_BRIDGE.txt`, section 4): "The complex child maximum below m/2 gives
halving degree 1, while log2 W < 5208 < 10000". The external row coefficient is then bounded by
A = 10000 + 9909 + 252 = 20161. With halving degree t the recursion depth is t·⌈log₂ n⌉, and the row term becomes
t·log₂ W. The guard (`code/complex/portable_complex.py`) now:

- computes the least t with mᵗ > 2·(max child)ᵗ;
- charges t times the actual physical stock logarithm, 2 · 1903 + 9909 + 252 = 13,967 < 20,161, so A and the outer
  assembly are unchanged;
- keeps the cover bound m ≤ 72 and the completed-child induction gap, now 49·B > 0.

At t = 1 it is the original guard. The B₂ run (PR #352's pins) and the split B₃ run (PR #363's pins) are
regressions in `verify.sh`.

This is the generalization the repository already uses elsewhere:

- **PR #144's integration review** (`research/pr-review-20261009/check_paired_cube_arithmetic.py`): a complex child of
  60 at m = 72, halving degree 4, and the row coefficient 4·2571 + 9909 + 252.
- **The copied-centers assembly** (`copied-centers-assembly.tex`, with `research/copied-fixed-reversed/balanced_assembly.py`):
  halving degrees 9 and 20, a row reserve D_j(e) = t_j⌈log₂ e⌉, and coefficient Σ t_j·w_j.
- **PR234 on the bit side** (`research/five-stage-source527-banks/UPSTREAM-PR234-PROOF.md`): "The proper child ratio 5/6
  requires halving degree four. The one-level weighted recurrence is retained; its histogram is not multiplied by four."

The moment equation is the one-level histogram either way. Only the finite row constant depends on t.

**Why not further.** Unsplit complex B₄ prices at 9.5673·10⁻⁴, but m = 81 exceeds the cover bound m ≤ 72. Unsplit B₅
needs halving degree three and prices lower (9.3708·10⁻⁴). The bit side keeps PR #373's split layout because it does
not bind. Unsplit, at halving degree two, it would give 9.9123·10⁻⁴.

## The layout

PR #370's bit word uses the five-stage bridged word: two bank pairs per class, five invocations, three layers of twin
bridges, then the terminal exchange. In B_K (PR #363, `code/complex/code/bridged.py`) pair p borrows its first forward
invocation from pair p − 1 in the same way:

    stage 0, 1, 2      pair 1: forward, backward, forward
    stage 2p-1, 2p     pair p: backward, forward                      (p = 2..K)
    after stage 2p-3   X(p-1) += Xp,  Yp -= Y(p-1)
    after stage 2p-2   Yp += Y(p-1),  X(p-1) -= Xp
    at the end         Y(p-1) -= Yp,  Xp += X(p-1)                    (p = K..2)

So K pairs are exchanged by 2K + 1 invocations on H ⊕ 2K·H, with m = (2K+1)h, W = 2Kv + R and D = 2Kv − (2K+1)·L for copy
loss L per invocation. With L = 72, both E8 units have D = 120 in five stages and D = 216 in seven. One invocation of
the bit word is unchanged. Only the word around it changes:

- **Idle climbs of the bit word in B₃** (h = 8): pair 1 [34], pair 2 [14, 7, 20], pair 3 [28, 7, 6]. The two climbs
  above m/2 are split at explicit intermediate frames, 34 → 27 + 7 and 28 → 27 + 1. The largest paid child is then
  27, and 2 · 27 < 56 satisfies the half-shrink guard.
- **Banks.** Every helper starts at frame 0, so all 865 residuals have width 8. Width-56 banks hold 7 of them, and 7 ∤ 865,
  so the bank tiling uses **T = 7 literal replicas**: 865 exact width-56 banks. The moment arithmetic is invariant
  under this normalization.

## What is checked (`bash research/e8-seven-stage-halving-two/verify.sh <fresh dir>`, about 4 min)

Every step of PR #373's verification runs: PR #370's steps and their B₃ versions, each with its K = 2 regression.
Steps 8 and 9 add the halving-degree-two complex supplier and keep PR #373's values as regressions.

0. **Manifest and provenance.** 142 files have the git blob ids of PR #370 at `b7fe9cd`, 4 those of PR #363 at
   `9df55da`, and 7 those of PR #373 at `3ff87b5` (`SOURCE-pr370.json`, `SOURCE-pr363.json`, `SOURCE-pr373.json`).
   The edited files are `portable_complex.py` (the halving degree), `certify_b3.py`, `verify.sh`, `provenance.py`,
   README and NOTICE. The new file is `pins-e8-b3h.json`.
1. **The word** (PR #370) is regenerated from its producer parameters, and the PR249 records are exported.
2. **One invocation** (PR #370): the independent all-column checker and its 6 word-level controls.
3. **Legality and formal columns.** Legality of one invocation uses PR #266's checker (NCOPY = 9).
   `columns_k.cpp -DKPAIRS=3` is PR #370's all-column F₂ check of the whole bridged word, extended to seven stages:
   - all 1,585 physical columns, dirty helpers included, through 7 invocations, 12 twin bridges and the terminal
     exchange;
   - all 12 omitted-bridge controls rejected;
   - PR #370's 6 record-level controls rejected.

   At K = 2 the receipt equals `columns_h`'s. On the PR #325 p10b word it equals PR #346's unmodified checker.
4. **Exact nondegeneracy** under the E8 Gram, and prime witnesses, on every frame (PR #370; the only prime is 2).
5. **PR234's route and idle geometry**, on all 120 ports, with W(E8) reflection words as port isometries.
   `geometry_k.py 3` uses 7 blocks:
   - routes involutive, 6 stage boundaries chained;
   - every idle climb a commuting nested pair whose gap rank equals `bridged.py`'s;
   - the two splits at dyadic intermediate frames Q = b − D, where D is a sum of orthogonal E8 root projectors, so
     the prime set stays {2};
   - the 7-window entrance completion exact, and a duplicated window rejected.

   At K = 2 it gives PR #370's idle ranks (14, 14, 7, 7, 18, 18, 4, 4).
6. **Banks.** `tile_k.py`: an exact zero-padding width-56 tiling with 7 replicas. At K = 2 it is byte-identical to
   `tile_g.py`.
7. **Copied centres.** 9 retained totals at the full frame. This is PR #370's admission, and it is charged as NCOPY = 9
   per invocation everywhere.
8. **Complex supplier** (`certify_b3.py`):
   - the B₂ regression reproduces PR #352's pins and b (halving degree 1);
   - the split B₃ regression reproduces PR #363's pins and b₃ = 932783231884153/10¹⁸ (halving degree 1);
   - **unsplit B₃**, against `pins-e8-b3h.json`, runs PR #352's portable checks at m = 63: max child 38, halving degree
     2, rows 2·1903 + 9909 + 252 = 13,967 < 20,161, induction gap 49·B, m ≤ 72;
   - Sussman's Lean data regenerated byte for byte, and his replay accepts;
   - b₃ = 119394377245827/(125·10¹⁵), with two engines and the 10⁻¹⁶ fallback, and the adjacent grid point rejected.
9. **Bit coarse saving and outer assembly.** `certify_bit_k.py 3 8 7` takes the one-level histogram
   7 × (one invocation) + 240 × (B₃ idle blocks), with W = 7 · 1,585, m = 56 and deficit 7 · 216. It uses PR #315's
   two engines with the 10⁻¹⁶ fallback, and rejects the adjacent grid point. The outer assembly gives 47 positive
   constraints and κ.

   At K = 2, T = 1 the receipt fields equal PR #370's (κ = 8.75481145306751e-4). With the split b₃ it gives PR #373's
   κ = 93191395651209/10¹⁷. With the halving-degree-two b₃ it gives κ = 95424356568133/10¹⁷.
10. **Finite bill at m = 56** (`finite_k.py`). The original formulas with the stage counts of B₃:
    - 7 invocations' additions plus 12v bridge additions;
    - route families 2·7·(2v + R) + 6v;
    - 7·NCOPY·T copy/erase episodes;
    - the selector bill 2·7·T·(…).

    The coefficient is 57,685,376,070,645 (46 bits) < 2⁸⁰, with q-power bound q³¹³⁷. All 120 port routes are exact
    elementary programs with denominators {1, 2, 4}. At K = 2 the bill is byte-identical to PR #370's, and the p = 10
    regression reproduces the original coefficient.

## Open obligations

- **No Lean proof of the bridged word B₃**, on either side. Sussman's `bridge2_certificate` covers B₂. Here B₃ rests on:
  - the all-column F₂ check of the whole seven-stage bit word (step 3);
  - PR234's exact rational geometry on 7 blocks (step 5);
  - PR #363's coordinate-frame check and exchange identity for the complex side.
- **Everything PR #370 admits**, unchanged:
  - the 9 retained totals at h = 8, a layout pin of the paired-cube words;
  - PR234's bank construction for a non-paired-cube family, checked on the exact matrices and not re-proved;
  - the inherited bit-supplier interfaces.
- **Everything PR #363 / #352 / #346 / #315 admit on the complex side:**
  - the complex symbolic correctness;
  - the precision/recovery and row interfaces, including the additive row constants;
  - the analytic transfer.
- **Halving degree two on the complex side.** The inherited finite bridge text states half-shrink (degree 1). Here
  its row term is charged at degree 2 as in the repository's degree-4 and degree-9/20 precedents (above), with the
  precision/recovery interface inherited at that depth. The outer assembly's constants are unchanged.
- The finite bill takes PR #370's formulas with the counts of seven stages (above). Its proof text is PR #370's and the
  source527/p10 lineage's, not re-derived here.
- This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **Dylan Crow (utcorvusvolat-dotcom), PR #370:** the E8 bit word, its producer, its independent checker, and the
  generalized bit-side checkers this package extends.
- **Jacob Sussman:** the E8 family and the E8 complex unit; the bridged five-stage word and its geometry, which B₃
  generalizes.
- **PR #363 / PR #373 (DaysSky):** B_K, the seven-stage complex unit and the seven-stage bit construction.
- The halving-degree generalization follows PR #144's integration review, the copied-centers assembly and PR234 (hcg890
  / Henry Grant).
- **PR #352 / #346 / #315 / #266 / source527 / PR234 lineage:** see `NOTICE.md` and `NOTICE-PR352.md`.

Prepared by DaysSky, assisted with Claude.
