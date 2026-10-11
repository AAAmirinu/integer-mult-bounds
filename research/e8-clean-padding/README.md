κ = 1.000385913854264e-3

# Bank padding fused into clean-sink helper climbs, on #390's dirty-preconditioned E8 complex program

A conditional finite construction with **κ = 125048239231783/1.25·10¹⁷ ≈ 1.000385913854264 × 10⁻³**.
That is +1.65691·10⁻⁷ (+0.0166 %) over Dugongue's #390 (125027527861191/1.25·10¹⁷ ≈ 1.000220222889528e-3).

The complex side binds. Its coarse saving rises from #390's b = 40048866680681/4·10¹⁶ to **b = 40055507598519/4·10¹⁶ ≈ 1.001387690e-3** (+1.66023·10⁻⁷).
The bit side is our #382 word, unchanged, with c ≈ 1.006907e-3 > b. Because κ is complex-bound, #390's larger bit c would give the same κ.

## The mechanism

In #377's nine-stage component, every bank holds eight 9-dimensional helper residuals plus one **paid rank-1 padding child** on coordinate 72 (m = 73). #390 keeps 3,123 such paddings per stage.

Fusing a padding into the final climb of a helper of the same bank replaces two children (rank d and rank 1) by one child of rank d + 1. The fused child is exact: if the compiled climb is M₁·C_[d]·M₂ (two monomials around one C child), then the climb tensored with C on window coordinate 72 is (M₁⊗I)·(C_[d]⊗C₇₂)·(M₂⊗I). That is one rank-(d+1) C child between the same monomials, so no new phase or edge appears.

The fusion is legal only if **nothing touches the helper after that climb**. Otherwise a later addition would mix a C₇₂-transformed stream with an untransformed one, and no common exact label exists.

- **Under #352's bracket it is impossible.** Its cleanup runs after all final climbs and reverses every non-y gate, both x → helper and helper → helper. In #378's word every one of the 775 lifting helpers is the target of at least one x → helper gate, so every helper is touched after its final climb.

  Re-scheduling cannot help. The undo of an x → helper gate needs the helper and that x at one exact label. The x roles are at FULL from gate 768 (in A) on, and the undo must follow the helper's last read, which feeds y in B. Our scan of every helper confirms this: no helper can be cleaned at its pre-climb frame, even when the undo is allowed anywhere after the helper's last influence on y.
- **Under #390's bracket it works for zero-row sinks.** #390 precancels the targets (y −= B·A⁻¹·h) and prewhitens the helpers (h ← A⁻¹h) before the main. Afterwards a helper holds N_r·x + h_r, and the only cleanup is "subtract N_r·x at FULL". A helper with N_r = 0 (a sink) needs no cleanup, so its final climb is its last event and can carry the padding.

## The three new sinks

We searched every lifting helper of #390's word for a **free** sink. The search looks for an exact rational combination of other helpers that, at the same time, sit at the helper's exact frame (no donor advance), applied after the helper's last influence on any y or retained total, that zeroes its clean x-row. It finds exactly three: 301, 324 and 387. Each has final lift rank 2.

For 301, at cut 1254 and frame 731, the gates are

    h276 += h1021/2;  h301 −= h276/2;  h276 −= h1021/2

(324: cut 1284, frame 744, donors 311 and 1020; 387: cut 1318, frame 759, donors 316 and 1022.) The temporary donor shear keeps every entry in sixths, as gxcore's E5 requires, and uses coefficients ±1/2 only. The paid local histogram is unchanged.

Allowing paid donor advances gives 16 more candidates, the same count #390 reports. Every one lowers b, so none is used.

Per invocation, three rank-2 lifts become rank-3 fused children. Over 9 stages × 32 replicas, 96 fused occurrences per stage sit in 96 distinct ordinary banks of #390's own assignment, and each of those routes fixes coordinate 72. Paddings per stage drop from 3,123 to 3,027:

    profile delta = {1: −864, 2: −864, 3: +864}   (rank mass, live 58,899, deficit 9,984 and max child 48 unchanged)

## Verify

    bash research/e8-clean-padding/verify.sh --quick /tmp/e8c-q     # ~1 min
    bash research/e8-clean-padding/verify.sh /tmp/e8c-full          # adds the free-sink regeneration (~3 min)

This needs Python 3.11+ and the standard library only. The script:

1. Checks `MANIFEST.sha256` and the git-blob pins of every input: #390's `prefix18.json.gz`, `sink-audit.json` and `prewhite.json`; #378's word; Sussman's `gx.py`/`gxcore.py`; #382's bit word.
2. On #390's prefix18 word, runs Sussman's `gx.check1` and the gxcore mirror, rejects a flipped-sign control, checks the source-span rule, and confirms the full operator identity with #378.
3. Rebuilds #390's main word (prefix18 plus the 355/403 uncomputes) and ours. For both it runs `gx.check1` and the gxcore mirror, and for ours also `cxcheck` (flipped-sign control, source-span rule). It then checks:
   - the paid local histogram is unchanged;
   - the five sinks' clean rows are exactly zero;
   - the x and y rows of the full rational operator and the retained totals equal #378's;
   - full mode only: the free-sink search over all 773 lifting helpers of #390's word regenerates exactly our gates.
4. Runs our reimplementation of #390's bracket compiler. On #390's word it reproduces `prewhite.json` gate for gate (1,660 / 1,550 / 7,800). On ours it emits both orientations, and an independent replay checks:
   - all 1,023 live columns: x, h restored; y += x forward, x −= y backward;
   - private work erased, and every scalar at a common exact label;
   - no event on a fused sink after its padded climb.

   Five mutation controls are rejected.
5. Rebuilds #390's bank assignment and checks the distinct-bank and coordinate-72 conditions.
6. Builds the profile from the validated paid events. It re-derives #390's b from its own emitted program as a regression, and prices ours with both PR #315 engines (10⁻¹⁶ fallback, adjacent grid point excluded). It re-derives c from #382's word and runs PR #315's outer assembly: 47 strict constraints, adjacent κ rejected, and #390's κ reproduced exactly.

## Admitted conditions and open obligations

See `PROOF.md`. In short:
- **Re-opened, with the replacement argument in PROOF.md:**
  - #352's emitter chronology and validator;
  - #377's bank padding as a separate end-of-schedule cover sweep, for the 96 fused banks per stage;
  - the general compiler's admission of a child whose coordinate set spans local and exterior window coordinates.
- **Re-proved here:** the items in Verify steps 3–6.
- **Inherited and not re-run:**
  - #390's rank-8 endpoint adapters for its sinks 355/403, its Clifford edge audits and its finite invoice. Our word adds 9 scalar gates per invocation, and the bracket changes from 1,550/7,800 to 1,556/7,776 pre-helper/post-repair gates;
  - all of #377's and #352's retained interfaces (window lift, arbitrary-dirt banks, cover correction X_δ(g), halving degree 2, rows, precision);
  - #382's bit-side claims.

This is a conditional finite construction, not a formal verification of the multiplication theorem.

## Credits

- **Dugongue (#390):**
  - the 18 target-prefix rewrites;
  - the dirty-preconditioned bracket (target precancellation, helper prewhitening, FULL repair) that makes sinks cleanup-free;
  - sinks 355/403;
  - the heterogeneous T = 32 banks.

  This package changes only which ordinary banks pay a separate padding.
- **jacklightChen (#377):** the nine-stage compressed component, banks and padding.
- **#352:** the local invocation, Clifford compiler and original emitter.
- **Jacob Sussman:** the E8 unit, `gx`/`gxcore`.
- **DaysSky** (#363, #373, #375) and **utcorvusvolat-dotcom** (#370): the bit-side lineage.
- **PR #315** (DreamingOfClouds): the engines and outer assembly.
- **Ours:** #378 (far retiming), #382 (bit word), and here the padding fusion, the free-sink search and the checks.

Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance. Apache-2.0 (`LICENSE`).
