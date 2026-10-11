κ = 9.98634656132003e-4

# #377's nine-stage complex E8 component with our re-timed E8 unit (#378), paired with our B₃ bit word (#382)

A conditional finite construction with **κ = 998634656132003/10¹⁸ ≈ 9.98634656132003 × 10⁻⁴**.
That is +3.91502·10⁻⁷ (+0.0392 %) over our #382 (998243154231047/10¹⁸), which pairs the same bit word with #377's component as shipped.

The complex side binds. Its coarse saving rises from #377's b = 999240641319551/10¹⁸ to **b = 999632926176283/10¹⁸ ≈ 9.99632926e-4** (+3.92285·10⁻⁷).
The bit side is our #382 word, unchanged, with c ≈ 1.006907e-3.

| side | supplier | layout | coarse saving |
| --- | --- | --- | ---: |
| complex | jacklightChen's #377 nine-stage E8 component, with **our #378 re-timed unit `gcert1-e8-r783-far`** in place of Sussman's `gcert1-e8-r783` | m = 73, W = 14,727, deficit 2,496, max child 48, halving degree 2 (all as #377) | b = 999632926176283/10¹⁸ |
| bit | our #382 word (#370's E8 bit word + retime + shared-donor kernel) | B₃ unsplit: m = 56, max child 34, halving degree 2 | c = 251726760077483/(2.5·10¹⁷) |

## Why the unit can be swapped

#377 states that its component uses "the same pinned E8 local word". That word is Sussman's certificate, sha256 `4b92f00f…`, which is byte-identical to the original in this package. #377's paid profile is built from it (its `complex_candidate.py` and `global_nine.py`, read as data) as follows:

- **Local children.** 9 stages × 8 replicas = 72 invocations, each paying the certificate's child histogram pooled over all blocks (x, y, s, c).
- **Idle data advances.** 2v·T children at each of the ranks 16, 8, 32, 8, 48, 8, 48, 32, 16.
- **Bank padding.** 9·R paid rank-1 paddings.

Here m = 73 and W = 8vT + 9R = 14,727. Only the first term depends on the certificate beyond (h, v, R, cst, ports, start/final frames). #378's certificate keeps all of those, and the full rational operator on all 1,023 registers and the retained totals are identical. So the data routes, phases, banks, padding, bridges, exchange and cover corrections of #377 are unchanged, and only the pooled local histogram moves:

| child rank | 1 | 2 | 3 | 4 | 6 |
| --- | ---: | ---: | ---: | ---: | ---: |
| per invocation | +2 | +2 | +6 | −21 | +10 |
| profile (× 72) | +144 | +144 | +432 | −1,512 | +720 |

The rank mass, W, the deficit 2,496 and the largest child, 48, do not change. The new profile is

    1:157743, 2:43632, 3:37728, 4:8568, 5:15480, 6:24552, 7:3096, 8:7488, 9:576, 16:3840, 32:3840, 48:3840.

**Further moves.** We re-ran our whole move family with the χ ledger at #377's m = 73 and #377's pooled price. The family is far piece relocation, single, block and sub-block retiming, and in-group piece relocation. Started from Sussman's original, it converges to exactly #378's certificate, byte for byte. Started from #378's certificate, it finds no improving move. Pooling the blocks makes the ledger m-independent to first order (a·Σ r ln(m/r) at fixed mass), which explains why the B₃ optimum carries over.

## Verify

    bash research/e8-far-nine-complex/verify.sh --quick /tmp/e8n-q     # ~20 s
    bash research/e8-far-nine-complex/verify.sh /tmp/e8n-full          # adds the m = 73 regeneration (~40 s)

Only Python 3.11+ and the standard library are needed. The steps are:

0. `MANIFEST.sha256`: every file listed, none unlisted.
1. Inputs pinned by git blob id:
   - Sussman's certificate, `gx.py` and `gxcore.py`;
   - #378's certificate;
   - #377's `GLOBAL-REVIEW.json`;
   - #382's bit word.

   Sussman's certificate also has its sha256 checked against #377's pin.
2. On both certificates:
   - Sussman's `gx.check1` (E0–E7, exact scalar replay E5) and the `gxcore` mirror histogram;
   - a flipped-sign control, which must be rejected;
   - the source-span rule.

   Then the full rational operator identity and the unchanged family data.
3. `code/nine.py`:
   - rebuilds #377's profile from Sussman's certificate and checks it equals `GLOBAL-REVIEW.json` field for field. Both rational engines (with the 10⁻¹⁶ fallback, next grid point excluded) re-certify #377's b exactly;
   - builds the profile with #378's certificate and prices b the same way;
   - re-derives the bit c from #382's word in B₃ unsplit;
   - runs PR #315's `outer.assembly` (47 strict constraints, adjacent κ rejected). The κ with #377's b equals #382's as a regression.
4. Full mode only: `code/far9.py` (our search with #377's ledger) from Sussman's original must regenerate the shipped certificate byte for byte (decompressed).

## Admitted conditions and open obligations

**Inherited from #377 (its claims, not re-proved here).** These include:
- the m = 73 compressed window lift and the arbitrary-bank dirty composition;
- the four-pair scalar chain, the idle advances and the paid padding;
- the exact Clifford data and cover phases (X_q, X_δ(g)), the injective owner routes, and the finite invoice;
- the two-level halving argument (73² > 2·48²) with its row coefficient 15,445 < 20,161;
- m = 73, which is beyond #375's m ≤ 72 cover bound;
- everything #377 retains from #352: the local E8 invocation theorem, the general Clifford/compiler interfaces, the tape primitives, precision and row allowances, and the analytic recurrence interfaces.

None of #377's scripts were run. Only its receipt's `profile`, `m`, `live` and `deficit` are read, and its scripts were read as data.

**#377's certificate-specific finite checks are not re-run on the new unit.** These are:
- the #352 emitter/splice and the scalar-word and lifetime replay (1,242,936 local events, 1,023 dirty columns);
- the local Clifford frame checks (946 frames, 3,120 transitions, 240 adapters);
- the finite invoice's local terms.

The new unit has the same ports, start/final frames, retained totals and operator. Its gates and frames differ: there are 775/1,226 gates (against 773/1,220, +0.4 %) and 948 frames (two new). The new transitions are nested, as `gx.check1` E1 checks, so they fall under #377's general Clifford compiler interface. The finite invoice's exponents (router < 2³⁰⁰⁰⁰ against 7,984 bits used) leave far more slack than a 0.4 % change in the scalar-macro count consumes. Still, these are obligations of this package and are stated as such.

**#378's own conditions** carry over: there is no Lean proof of the new certificate, which is checked by Sussman's `gx.check1`/`gxcore` and by the full operator identity.

**The bit side is #382's claim**, including its halving-degree-two admission. Here we re-derive c from the word only. #382's stage replays, legality and B₃ formal-columns checks are in `research/e8-kernel-bit-b3/`.

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **jacklightChen (Zhihao Chen), #377:** the nine-stage compressed complex component, which is the whole complex construction used here. It covers the window, banks, padding, phases, invoice and the profile rule this package reproduces.
- **Jacob Sussman:** the E8 unit `gcert1-e8-r783`, `gx`/`gxcore` and the stage geometry (wht-power-saving-lean, Apache-2.0).
- **aliromman (#365):** the first coupled re-timing of this unit. #378's moves generalise it.
- **DaysSky (#363, #373, #375):** B_K, the seven-stage bit construction, and the halving-degree-two guard used on the bit side.
- **utcorvusvolat-dotcom (#370):** the E8 bit word under our #382 stages.
- PR #315's moment engines and outer assembly (DreamingOfClouds).
- **Ours:** the far-piece-relocation certificate (#378), the bit word stages (#382), and this substitution.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`). See `NOTICE.md` and `PROOF.md`.
