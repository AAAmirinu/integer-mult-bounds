κ = 9.98243154231047e-4

# A staged E8 bit word in the seven-stage bridged word B₃, paired with #377's nine-stage E8 complex component

A conditional finite construction with **κ = 998243154231047/10¹⁸ ≈ 9.98243154231047 × 10⁻⁴**. It is complex-bound, at the cap of jacklightChen's #377 complex component.

The bit side is utcorvusvolat-dotcom's #370 E8 bit word with two of our transcript stages: retiming and a shared-donor response kernel. It runs in DaysSky's B₃ (#363/#373). The idle climbs are unsplit, at halving degree two (#375's guard).

| side | supplier | layout | coarse saving |
| --- | --- | --- | ---: |
| bit | **#370's word + our retime (44 gates) + kernel (171 entries, entrance rank 320)** | B₃ unsplit: m = 56, max child 34, halving degree 2, deficit 216 | c = 251726760077483/(2.5·10¹⁷) ≈ 1.006907e-3 |
| complex | #377 nine-stage E8 component (its claim; re-certified from its profile) | m = 73, W = 14,727, deficit 2,496, halving degree 2 | b = 999240641319551/10¹⁸ ≈ 9.99241e-4 |

The bit side exceeds b, so the complex side binds. All 47 constraints of `outer.assembly` hold, and the adjacent 10⁻¹⁸ κ is rejected.

**Without the bit-side halving-degree-two admission** (B₃ split at 27, degree 1, as #373) the same word gives
**κ = 245546943425791/(2.5·10¹⁷) ≈ 9.82187773703164e-4**, bit-bound. That result needs no new admission.

| bit word with #377's b | B₃ split (degree 1) | B₃ unsplit (degree 2) |
| --- | ---: | ---: |
| #370 / #373 | c 9.68198e-4 → κ 9.67261e-4 | c 9.91226e-4 → κ 9.90245e-4 |
| **this word** | c 9.83153e-4 → **κ 9.82188e-4** | c 1.006907e-3 → **κ 9.98243e-4** (complex-bound) |

## The bit word

The stages are those of our #329/#359 stack, ported to the E8 frames, which are root-spanned subspaces of Q⁸ under the positive definite form ⟨x,y⟩ = x·y/2. Each stage is applied from a frozen selection bound to its exact input word, and the full exact replay runs after each one (`code/stages.py`).

1. **Retiming** (#287/#291/#299 descent lineage). 44 gates of #370's word move to new frames inside their feasible intervals. A gate's interval runs from the join of its source spans and its participants' previous frames to the meet of their next frames.
2. **Shared-donor response kernel** (#272/#299/#319/#320/#329 lineage).
   - **Response.** resp(h) is the set of targets whose frame-0 completion reads read helper h. An entry is a pivot p, an entrance E (inside the first frame of p and of every donor), and donors D with resp(p) = ⊕ resp(D) over F₂.
   - **Pivot.** p starts at E and loses its completion reads.
   - **Donors.** Each donor climbs to E at the start of A and adds its pivots there. After C it adds them again at FULL (over F₂ this subtracts them).
   - **Selection.** 171 entries with entrance ranks 1/2/4 and total rank 320 (= 0 mod 40), using 97 donor slots. Pivots are never donors, and a donor serves one entrance.
3. **Residuals.** The residual census is {8: 694, 7: 120, 6: 2, 4: 49}. It tiles exactly into width-56 banks with 7 replicas (825 banks), and into width-40 banks with 1 replica.

## Verify

    bash research/e8-kernel-bit-b3/verify.sh --quick /tmp/e8b-q
    bash research/e8-kernel-bit-b3/verify.sh /tmp/e8b-full

The checks need Python 3.11+ (standard library), a C++17 compiler and Boost headers.

0. `MANIFEST.sha256`.
1. Pinned inputs by git blob id: #370's word (= #373's `data/bit`) and #377's `GLOBAL-REVIEW.json`. In full mode, our engine also reproduces #370's c, κ(b₂) and κ(b₃).
2. The two stages from the frozen selections, each followed by our exact replay:
   - legality: nested root-spanned frames, common gate frames, completion reads at frame 0, y at frame 0 at the scatter, the 9 retained totals at FULL, and the final frames;
   - F₂ on all 1,105 columns, dirty helpers included;
   - the integer source-span rule.

   The rebuilt word must equal the shipped one. Five mutation controls are rejected.
3. Labels and frames, then the official checkers:
   - the 120 E8 root lines, and exact Gram determinants > 0 on all 945 frames (prime 2 only);
   - our own export to PR249 records, and PR #266's official cohort legality at h = 8 with NCOPY = 9;
   - the unmodified copy count NCOPY = 8 is rejected;
   - **our port of #266's five-stage columns checker to B_K** (`columns_k.cpp`). At K = 2 it reproduces the #266 receipt field for field, except the original's h = 20 literal `fresh_center_copies`. At K = 3 it checks all **1,585 physical columns over F₂ through 7 invocations, 12 twin bridges and the terminal exchange**, and the 12 omitted-bridge controls are rejected.

   The columns check simulates invocations and bridges. It does not depend on how the idle climbs are split, so it covers the split and unsplit layouts alike.
4. The layout and the guard:
   - our B_K layout reimplementation (#363's rule): B₂ gives (2h+2 | 2h−2, h−1, 4), and B₃ gives #373's [34] | [14, 7, 20] | [28, 7, 6];
   - the exact bank tilings;
   - **the halving-degree guard at the bit parameters** (`code/guard.py`, #375's form). Unsplit: m = 56, max child 34, least t = 2 (56² = 3,136 > 2·34² = 2,312), stock 1,551 bits, row coefficient 2·1551 + 9909 + 252 = **13,263 < 20,161**, induction gap 43·B, m ≤ 72. Split: t = 1, row 11,712, gap 57·B.
5. #377's b is re-certified by our two rational engines from its own profile (m 73, W 14,727, deficit 2,496). Then the bit c (split and unsplit) and #315's outer assembly.

## Admitted conditions and open obligations

- **Bit-side halving degree two** (unsplit B₃ idle climbs, max child 34 of 56). It is admitted under #375's generalised finite-bridge guard and #375's own precedent list:
  - #144's integration review: degree 4, row 4·2571 + 9909 + 252;
  - the copied-centres assembly: degrees 9 and 20, with D_j(e) = t_j⌈log₂ e⌉;
  - PR234 on the bit side: "the proper child ratio 5/6 requires halving degree four".

  Step 4 gives the exact guard numbers at the bit parameters. Without this admission the result is the split κ ≈ 9.82188e-4.
- **#377's b is #377's claim.** That includes its m = 73 setting, which is beyond #375's m ≤ 72 cover bound, its compressed window lift, its padding and its finite invoice. It is re-certified here only from its profile, with our engines. #377's own checks are not re-run.
- **No Lean proof** of B₃, or of this bit word or its stages.
- **#373's PR234-style port geometry on 7 blocks and its finite bill at m = 56** are not re-run on this word. The ports and their isometries are #370's, and only helpers change. The kernel entrances (σ > 0 for 171 helpers) need the entrance completion P_σ + (I − P_E) of our #329 lineage, which is not re-proved here for the E8 family.
- **Everything #370 admits:** 9 retained totals at h = 8, PR234's banks for a non-paired-cube family, and the inherited bit interfaces.
- This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **utcorvusvolat-dotcom (#370):** the E8 bit word, its format and the generalized bit checkers this package mirrors.
- **jacklightChen (#377):** the nine-stage E8 complex component.
- **DaysSky (#363, #373, #375):** B_K, the seven-stage bit construction and the halving-degree-two guard.
- **Jacob Sussman:** the E8 family, the bridged five-stage word and the stage geometry.
- **Our stage lineage:**
  - retiming: #287/#291/#299, via our #329/#359;
  - the shared-donor kernel: #272/#299/#319/#320, via our #329/#359;
  - PR #266's official checkers (ported);
  - PR #315's engines and outer assembly (DreamingOfClouds).

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`). See `NOTICE.md`.
