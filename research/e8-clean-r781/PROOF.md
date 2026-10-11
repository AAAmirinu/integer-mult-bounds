# Why the fused program computes #398's operator, and what is re-opened

Notation: x (120 sources), h (783 helpers), y (120 targets). The main word is the gcert/1 word (A, scatter, B), here Dugongue's #398 R781 word with our nine new helper → helper gates (no #390 sinks; R781 has 781 helpers, 1,021 live columns).

**0. The base word and the bracket change.** The main word is Dugongue's #398 R781 word (#376's R781 helper substitutions on our #378 far word, plus 25 signed disjoint target-prefix pairs), byte-pinned, with our nine new helper → helper gates. #398 compiles it with #352's frozen old response K, main and the full cleanup of the non-y word at FULL. Every one of its 781 helpers is the target or source of a non-y gate (`clean.py` checks this), so under that bracket every helper is touched after its final climb and no padding can be fused. We compile the same word with #390's dirty-preconditioned bracket (§1) instead. Both brackets realize the same invocation (x, h, y) → (x, h, y + x) on arbitrary dirty inputs, which `validate` checks on all 1,021 live columns in both orientations. Both use only scalar operations at common frames, so the paid local events coincide with the word's histogram. Our emission of #398's word reproduces #398's b and κ exactly. The changed scalar schedule, and the Gaussian phases of its endpoint adapters, are an admitted re-opened item (see below); no new climb or edge is introduced.

**1. The bracket (#390, re-implemented and regression-checked).** The main acts on scalar values as x' = x, h' = N·x + A·h, y' = y + M·x + B·h. Here A is the product of the literal helper → helper shears. The bracket has three parts:
- **Before the main**, at the common old frame: y −= (B·A⁻¹)·h, then h ← A⁻¹·h, where A⁻¹ is the reversed, negated helper → helper subword.
- **The main** now yields (x, N·x + h, y + M·x).
- **After the final climbs**, at FULL: for every non-sink helper, h_r −= N_r·x.

`emit.prewhite` computes these lists. On #390's own word it reproduces #390's `prewhite.json` exactly, in the same order. On ours, `emit.validate` replays all 1,021 live columns exactly in both orientations. The backward orientation is the same chronological sequence with each t += a·s replaced by s −= a·t. The replay confirms (x, h, y) → (x, h, y + x) forward and (x, h, y) → (x − y, h, y) backward, private work zero, and every main scalar at a common exact frame label.

**2. Our gates keep everything but the sink rows.** Each new gate is helper → helper at a frame where all three registers already sit, so no climb is added and the paid histogram is unchanged. Each is inserted after the sink's last influence on any y or retained total. The adjoint of the main from all y outputs, including the scatter, is identically zero on the sink from that point on. The x and y rows of the full rational operator and the retained totals are therefore unchanged, as `clean.py` checks against #378. `gx.check1` (E0–E7, exact scalar E5) and the gxcore mirror (sixths units) accept the word. The sinks' clean rows N_r are exactly zero.

**3. A zero-row sink needs no cleanup.** With N_r = 0, the bracket leaves h_r equal to its input value up to its frame walk. The emitted program has no event on the sink after its final climb except its rank-0 new → old adapter, which acts on the local factor. `validate` enforces this, and a control that adds a FULL repair on a fused sink is rejected.

**4. Fusing the padding.** The sink's final climb from frame f to FULL is compiled as M₁·C_[d]·M₂ (d = 2 for all three sinks, and these are existing audited edges 731→1, 744→1, 759→1). On the bank stream we apply instead (climb) ⊗ C₇₂ = (M₁⊗I)·(C_[d]⊗C₇₂)·(M₂⊗I). This is one C child of rank d + 1 on a coordinate set (d local coordinates plus window coordinate 72) between the same monomials, so the paid profile changes by rank 2 + rank 1 → rank 3.

Since no event touches the stream afterwards in this invocation, the fused invocation equals the unfused invocation followed by C₇₂ on that stream. The arbitrary-dirt property of #377 says each invocation acts on a helper stream as C_block ⊗ I_exterior, and its y output is independent of the helper value. So C₇₂ commutes with every other invocation on that bank stream, and with all data-family operations, which use disjoint families. Hence the result equals #377/#390's schedule, where the padding is a separate sweep before the X_δ(g) cover correction.

The routes of #398's whole banks (bank, slot = divmod(rep·781 + r, 8); the slot route swaps local coordinates 0–8 with block 9·slot … 9·slot+8) fix coordinate 72 (`clean.py` rebuilds them from #398's rule). The fused C on invocation coordinate 72 is therefore P_g·C₇₂·P_g⁻¹ at the bank class g = d·A⁻¹, exactly #377's padding. Each fused occurrence (3 helpers × 8 replicas per stage) lies in a distinct bank, so every such bank class receives C₇₂ exactly once.

**5. Price.** #398's profile formula: 72 × (validated paid local events) + 1,920 idle children at each of 16, 8, 32, 8, 48, 8, 48, 32, 16 + 9·(781 − 24) paddings. m = 73, live 14,709, deficit 2,496, max child 48, halving degree 2 (73² > 2·48²). From our emission of #398's word this reproduces #398's 24-digit b and κ exactly. Ours: b = 1003667444352030197427/10²⁴, κ = 1002661106042177/10¹⁸ (six bootstrap levels, 47 strict constraints, complex-bound; our #382 c and #398's bit c give the same κ).

## Re-opened arguments

- **#398's bracket** (#352's frozen K + cleanup) is replaced by #390's dirty-preconditioned bracket (§0, §1). It is checked here on every live column in both orientations, with common exact labels and private erasure. #398's Gaussian-phase, global-template and finite-invoice audits were run for its own scalar schedule and are not re-run for ours. The scalar work changes (precancellation instead of K, repair instead of cleanup), so the invoice must be re-counted. #390's invoice for the same bracket on R783 stayed below its row reserve.

- **#352's emitter/validator chronology** (old_response, cleanup after adF of every non-y gate) is not used. It is replaced by #390's bracket (§1), which #390 already introduced. Our extra rule is §3.
- **#377's padding as an end-of-schedule paid rank-1 cover sweep**, for 96 banks per stage. It is replaced by §4. That argument relies on the arbitrary-dirt invocation property (#377/#352, retained) and on the general compiler admitting a C child whose coordinate set mixes local coordinates with an exterior window coordinate. The latter is the same kind of child the compiler emits, up to a coordinate permutation, but #377's window-lift lemma is stated for transitions that cancel the exterior factor. For stage 8, where E₈ already contains coordinate 72, the canonical label T_U ⊗ C_{E_s} is not the right bookkeeping. The argument above is at the operator level and does not use labels.

## Re-proved by our checks

- the word's labels, nesting and exact scalar replay (`gx.check1`, gxcore);
- x/y operator rows and retained totals;
- sink zero rows;
- #398's word: gx/gxcore, its x → (x, y) operator equal to #378's, and the all-helpers-touched property of #352's bracket;
- #390's bracket (regression on #390's word), and the bracket on #398's word and on ours, in both orientations on all 1,021 columns, with lifetimes and common labels;
- the fused-sink rule;
- bank distinctness and coordinate-72 fixing;
- the profile from events, b, c and κ.

## Not re-run (inherited obligations)

- #398's R781 reconstruction (#376), its Clifford edge and Gaussian-phase audits, global template and finite invoice (row coefficient 15,445 < 20,161), for its own bracket. #392's six-level bootstrap argument. Our word adds 9 scalar gates per invocation; our bracket uses 1,658/1,551/7,776 precancellation/pre-helper/post-repair gates (1,658/1,542/7,800 for #398's word itself). No new local edge is used.
- #377/#352's retained interfaces: window lift, arbitrary-dirt banks, X_δ(g), injective routes, halving, rows, precision.
- #382's bit-side admissions.
