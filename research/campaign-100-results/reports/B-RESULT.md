# B-certificate-whatif — what each proof-level change of the certificate/layout is worth on #325's word

Ideas 8, 18, 20, 21, 26, 28, 29, 46, 47, 48, 51, 54 of RADICAL-IDEAS.md, priced as pure arithmetic on #325's
five-stage paid histogram (no new words). Scripts and logs: `/tmp/radical/B-certificate-whatif/`
(`pe_dump.py` = physical_eval.py + histogram dump; `whatif.py`, `modelc.py`, `modelc2.py`, `caps.py` and their
`.log`s; `whatif_results.json`).

## 0. Reproduction (required first)

`/tmp/p10job/physical_eval.py PKG none OUT` on a copy of #325's package (`/private/tmp/imbwork/w325/research/five-stage-p10b-banks`)
reproduces **κ = 384842019691667/(5·10^17) = 7.69684039383334e-4 exactly** (76 s, R = 8100, literal stock 658800,
entrances {16: 1200}, 0 dropped pairs). No tiering/orientation discrepancy: the matching re-solve in regenerate
gives the pinned word. Pricing path (math_check.py / physical_eval.py bottom block):

- one-stage paid histogram (incl. the h = 20 centre copies at rank h−2 = 18), rank mass 179,640:
  `{1:21400, 2:9149, 3:6065, 4:1359, 5:1092, 6:1006, 7:640, 8:164, 9:293, 10:248, 11:80, 12:1006, 13:2, 14:344, 16:960, 17:2536, 18:980}`
- five-stage paid = 5×core + idle 2v = 1920 each at ranks (38, 19, 42, 4) + 1200 entrance completions at rank 5·16 = 80;
  mass 1,191,960; W = 4v + R = 11,940, m = 100, deficit = mW − mass = 2040 = 4v − 5h(h−2).
- banks remove the 1200 rank-80 completions → banked histogram (calls 244,300, mass 1,095,960); literal stock
  W_lit = 60·4v + 5·banks_per_stage = 658,800; normalized ÷5: Hn = 12×banked, Wn = 131,760, deficit 24,480.
- `moment.certify(Hn, 100, 131760, bad=True)` (with the 10^-16 fallback, 32·m²·calls rank-one children) →
  root bisected to 1e-24 then floored to the 1e-18 grid: c = 7.70276909563042e-4; adjacent grid point rejected.
- s = min(c, floor((1−β)b − 1e-18)) with b = 7.72714351296671e-4 (β = 1e-9) → bit binds, s = c.
- chain a_{j+1} = (1−s)s + s·a_j, 3 steps from 384599e-10; q = a_3(1−2η), η = 1e-12; minimum = (1−η)q/(1+q);
  κ = largest 1e-18 grid point strictly below minimum.

Independent check: my 60-digit mpmath root agrees with `certify()` to all 24 printed digits on the baseline and
on two integer variants (ℓ = h(h−3): 8.08013348918820898901e-4; merged idle: 7.91076021477659610169e-4).

Useful sensitivities (baseline histogram): **Δκ ≈ +3.8e-7 per unit of five-stage deficit** (one paid rank unit
removed per invocation at fixed stock), i.e. ~600× the per-unit-J proxy (6.3e-10).

## 1. The table

κ_base = 7.69684039383334e-4. "capped" = what math_check.py would certify with the current complex supplier
(b = 7.72714351296671e-4, cap κ = 7.721177237e-4); "uncapped" = the bit-side value if the complex side did not bind.

| # | change | κ | Δκ vs base | which proof must change |
|---|---|---|---|---|
| (a) 8/46/47 | true root of the moment equation (60 dps) instead of certify()'s | root 7.7027690956304264998764e-4 vs certify 7.70276909563042649987e-4; c (grid) differs by 6.5e-19; κ +1.0e-18 | +1.0e-18 | none — certificate has no slack. The "moment" is the Akra–Bazzi characteristic equation Σ (rH_r/mW)(m/r)^a + fallback = 1 (three-stage-cover-bit.tex §"strict moment"); its root is the exact growth exponent of a linear recursion with a fixed histogram, so no LP/SDP/Cramér refinement can beat it. |
| (a') 52 | drop the 10^-16 bad-class fallback envelope on the bit | 7.69684042337737e-4 | +2.95e-12 | PROOF §4 fallback envelope |
| (b) 48 | no 1e-18 floors anywhere (root, s, κ) | 7.69684039383335e-4 | +1.05e-18 | none |
| (b) 48 | adjacent grid point c+1e-18 (moment = 1 + 8.45e-19 > 1: rejected) | would be +1e-18 | +1e-18 | illegal |
| (c) 54 | η = β = 0 | 7.69684039385642e-4 | +2.31e-15 | outer.py (delta_positive/beta_positive forbid 0; limit value) |
| (c) 54 | η, β halved | 7.69684039384488e-4 | +1.15e-15 | outer.py |
| (c) 54 | β halved alone | unchanged | 0 | β only enters the cap (bit binds) |
| (d) 28 | chain depth 2 / 4 / 5+ | 7.696836061790e-4 / 7.696840397170e-4 / 7.696840397173e-4 | −4.33e-10 / +3.34e-13 / +3.34e-13 | INTEGRATED_PROOF §5 "three finite levels"; math_check `for _ in range(3)`; none of the 47 constraints references depth (outer.py takes only a_bit, b, κ, η, β). Fixed point of the chain is s itself; loss after 3 levels is s³(s−a0) = 3.3e-13. |
| (e) 51 | replicas T = 30 / 20 / 12 / 5 / 1 | unchanged | 0 | none for κ: the root is scale-invariant (H and W both ∝ T). For #325's word every T tiles exactly (families: 1200×width 4, 6900×width 20, both divide m = 100). T only enters the finite bill (selector calls K ∝ T). |
| (e) 18 | k stages, user formula deficit 4v − kℓ, 5-stage idle kept, k = 3 / 4 / 6 / 7 / 8 | uncapped 2.111e-3 / 1.223e-3 / 4.991e-4 / 3.215e-4 / 1.972e-4 (k ≤ 4 capped to 7.7212e-4) | +1.34e-3 / +4.53e-4 / −2.71e-4 / −4.48e-4 / −5.73e-4 | k-stage completion theorem. Caveat: this W is not a register count (k = 3 implies 9987 < 4v+R−G/h = 10980). |
| (e) 18 | consistent model C: 2P banks, k stages (pair 1 gets k−2(P−1) stages, others 2), W = 2Pv + R − G/h, deficit 2Pv − kℓ, idle mass forced = 2v[(P−1)kh + k − P] (reproduces 3-stage virtual 2v−3ℓ and 5-stage 4v−5ℓ exactly) | k=3,P=1: 7.0502e-4; **k=4,P=2: uncapped 1.19e-3…1.26e-3** (capped 7.7212e-4); k=7,P=3: 7.0908e-4 (split idle) … 7.7238e-4 (merged); k=9,P=4: 6.360e-4 … 7.409e-4; k=6,P=3: uncapped 9.1e-4…1.05e-3 (capped); k=8,P=4: 7.383e-4 … uncapped 9.32e-4 | k=4: **+4.2e-4…+4.9e-4 uncapped**, +2.43e-6 capped; k=7: −6.1e-5 … +2.7e-6; k=9: −1.3e-4 … −2.9e-5 | k-stage completion (PR234 layout: pair A's three XOR stages implement a swap; pair B swaps with two stages + 6v bridges). A 4-stage (2+2) completion would be the biggest lever in this file, but it must replace the 3-XOR swap of pair A. More stages per pair count lose: each extra stage multiplies the dominant rank-1 climbs. |
| (f) 26 | ℓ = h(h−3) (copies at rank 17; deficit 2140) | uncapped 8.07360990e-4; capped 7.7212e-4 | **+3.77e-5** uncapped; +2.43e-6 capped | copied-centres lemma (proof/copied-centers-lemma.tex) / completion geometry |
| (f) 26 | ℓ = h(h−4) (deficit 2240) | uncapped 8.45035e-4 | +7.54e-5 | same |
| (f) 21 | idle (2h−2, h−1, 2h+2, 4) → merged (3h−3, 2h+2, 4), same mass | uncapped 7.90451e-4 | +2.08e-5 | PR234 idle boundary projectors (global_lowering.idle_projectors: which=0 and which=1 both act on banks 2,3; merging them is one boundary instead of two) |
| (f) 21 | idle fully merged per bank pair (3h+1, 2h+2) | uncapped 7.99230e-4 | +2.96e-5 | same, plus the rank-4 fixups folded in |
| (f) 21 | idle (2h, h, 2h, 3) same mass | 7.70589e-4 | +9.0e-7 | same |
| (f) 21 | idle (2h−1, h, 2h+2, 2) / (2h−2, h−1, 2h+3, 3) | 7.7218e-4 / 7.71080e-4 | +2.5e-6 / +1.4e-6 | same |
| (f) 21 | rank-4 fixups removed at fixed stock (deficit +8v = 9720) — fantasy | 3.675e-3 | +2.9e-3 | would need the data registers to end 4 ranks lower; shows deficit sensitivity only |
| (g) 20 | Gram form G = I − J/9 | κ unchanged by construction | 0 | pricing (moment.py/outer.py) never sees G. G enters only (i) the word's definition: bit labels χ_S with H0 = G/2, H0(χ_S,χ_T) = (|S∩T|−1)/2 (producer/paired_cube_bit_word.py:16,148), so J/9 is tied to |S| = |T| = 3 cube labels; (ii) legality: gram_nondegenerate_frame (producer:163), geometry527.py:96 (P^T G = G P for new source frames), base_word.py nondeg; (iii) prime_check.py:40 cleared Gram determinants (prime range), bank_check.py residual rows (h−9)a − Σa (chart size → finite bill). A different G changes which words are legal, not how a histogram is priced; it cannot be evaluated by arithmetic. |
| (h) 29 | complex cap with #325's bit root under b = 7.7271e-4 (#315) / 7.7372e-4 (#327 #304-recipe) / 7.7960e-4 (#327 centre-sharing) / 7.80e-4 / 7.90e-4 / 8.00e-4 | 7.69684039e-4 in every case (bit binds) | 0 | — |
| (h) 29 | κ ceiling imposed by each cap (bit root → ∞) | 7.72117724e-4 / 7.73120399e-4 / 7.78990313e-4 / 7.79392073e-4 / 7.89376391e-4 / 7.99360510e-4 | +2.43e-6 / +3.44e-6 / +9.31e-6 / +9.71e-6 / +1.97e-5 / +2.97e-5 | complex supplier (math_check.complex_supplier) and outer leaf_saving_above_bit |
| (h) 29 | bit-root headroom before each cap binds | +0.316% / +0.447% / +1.210% / +1.262% / +2.561% / +3.859% above c = 7.70276910e-4 | — | — |
| (h) 29 | hypothetical bit root +0.7% (7.75669e-4, after a full stage stack) under the three caps | #315: 7.72117724e-4 (capped, loses 2.95e-6); #327 #304: 7.73120399e-4 (capped, loses 1.95e-6); #327 centre-sharing: 7.75067652e-4 (bit binds, full gain) | +2.43e-6 / +3.44e-6 / +5.38e-6 | #327 centre-sharing unlocks the whole +0.7% and everything up to +1.21% |
| (h) 29 | bit root +0.5% / +1.0% under #327 centre-sharing | 7.73529483e-4 / 7.77374896e-4 (bit binds) | +3.85e-6 / +7.69e-6 | — |
| (h) 29 | complex b needed for the cap to bind at #325's current root | b < 7.70276910333e-4 (i.e. a *worse* complex than any on the table) | — | — |

## 2. Verdict — ranking by Δκ per expected derivation effort

1. **Complex cap first (idea 29, no derivation needed once #327 lands).** Every bit-side lever worth more than
   +0.316% in root (+2.43e-6 in κ) is wasted under #315's complex; #327's centre-sharing b raises the ceiling to
   7.78990e-4 (+9.3e-6) and the headroom to +1.21% in bit root. All the large rows below are capped at
   7.72118e-4 today and at 7.78990e-4 with #327. Nothing in (a)–(d) matters next to this.
2. **ℓ = h(h−3) (idea 26): +3.77e-5 uncapped, +2.43e-6/+9.3e-6 capped.** One lemma (the copied-centre rank /
   deficit term), pure geometry, no new word. Highest Δκ per effort among the [math] items; worth ~100 units of
   deficit, i.e. more than any stage lever on this word. Even ℓ = h(h−3) alone overshoots the #327 cap, so it
   should be paired with a complex improvement.
3. **Merged idle boundaries (idea 21): +2.1e-5 (merge the two banks-2,3 boundaries) to +3.0e-5 (one climb per
   pair).** Same rank mass, same deficit, only the concavity of r·ln(m/r). Needs the PR234 idle projector pairs
   for which=0/1 to be replaced by one boundary (global_lowering.idle_projectors); plausibly a small change to
   the layout proof. Mass-preserving re-splits that keep four boundaries are worth ≤ +2.5e-6.
4. **4-stage layout (idea 18) with 2 bank pairs: +4.2e-4…+4.9e-4 uncapped (κ ≈ 1.2e-3).** By far the largest
   number, but it requires replacing pair A's three-XOR swap by a two-stage-plus-bridge swap with no extra
   scratch pair, which is exactly what PR234's structure appears to forbid; k = 6/7/8/9 under the consistent
   model are negative or ≤ +2.7e-6. Treat as "derive or refute the 2+2 completion"; if it exists it dwarfs
   everything, and would only pay through a much better complex supplier (cap).
5. **Everything in the certificate/outer layer is dead:** certificate slack +1e-18 (the moment root is exact,
   ideas 8/46/47), grid rounding +1e-18 (48), η/β +2.3e-15 (54), chain depth +3.3e-13 (28), fallback envelope
   +3e-12 (52), replica count exactly 0 (51; only the finite bill changes). Gram form (20) does not enter
   pricing at all; it is part of the word's definition and legality.
