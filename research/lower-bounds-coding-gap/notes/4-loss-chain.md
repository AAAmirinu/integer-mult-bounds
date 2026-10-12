# 4. Where κ goes: an exact loss chain, and a piece-count remark

Status: §4.1 is an **identity plus a first-order expansion** (exact computation on published profiles). §4.3
Theorems 1 and 4 are **proved** (short convexity arguments, not independently reviewed), and the numerical bounds
are interval-certified. The hypotheses H1–H6 are **assumptions** about the framework, not theorems.

## 4.1 The chain

A supplier saving a is the root of the hub's moment equation Σ_r (r n_r/(mW))(m/r)^a = 1. Here the 10⁻¹⁶ bad-class
term is omitted; it changes the roots by less than 10⁻⁸ relative. Write δ = D/(mW) with D = mW − Σ r n_r, and
L_ent = ln m − E[ln r], where the expectation is rank-weighted over paid children. Then

  a ≈ δ / L_ent = (1/m) · (D/W) · (1/L_ent),      κ ≈ a/(1 + a).

The exact root is 1.0007 to 1.0027 times the first-order value on every profile below. So κ is a product of:

1. **thin-label dilution** 1/m: each data role saves one of m label dimensions;
2. **net gain per live role** D/W: the data share of the stock, after the centre copies;
3. **climb entropy** 1/L_ent: how small the paid pieces are;
4. **outer assembly** 1/(1 + a): under 0.16 %.

`scripts/loss_chain.py REPO_ROOT` reproduces every published saving from its profile to < 10⁻⁸ relative. It reads the
current two rows from main:

| profile | 1/m | D/W | L_ent = ln m − E ln r | δ/L_ent | root a | a/(1+a) |
|---|---|---|---|---|---|---|
| gen4 bit (#276 + #279, merged) | 1/120 | 0.2058 | 2.370 = 4.787 − 2.418 | 7.236e-4 | 7.2410e-4 | **7.2357e-4** (= gen4 κ) |
| complex #501 (R560, open) | 1/73 | 0.3250 | 3.316 = 4.290 − 0.974 | 1.342e-3 | 1.34533e-3 | 1.34352e-3 |
| bit #493 (R489) | 1/78 | 0.3400 | 2.789 = 4.357 − 1.568 | 1.563e-3 | 1.56544e-3 | — |
| **complex, selected on main (#596)** | 1/73 | 0.3571 | 3.035 = 4.290 − 1.256 | 1.612e-3 | 1.615326e-3 | **1.612721e-3** (= main κ) |
| bit #589 (p111, R439, 9 stages) | 1/64 | 0.3615 | 3.267 = 4.159 − 0.892 | 1.729e-3 | 1.733427e-3 | — |

From merged gen4 to today's selected complex supplier, the root grew ×2.23: 1/m ×1.64 (E8 labels and compressed
windows), D/W ×1.74 (hosting removes helper and bank streams from W; puncturing improves the copy ratio), and
1/L_ent ×0.78 (smaller pieces). On the whole-hosted words, D/W = 1 − (2K + 1)·cst/(2K·v) exactly.

## 4.2 Relation to #595

#595 (DreamingOfClouds, `research/format-limits`) contains the first-order bound in its own form, X ≤ D_s/Cost_s
(§A.2). It also decomposes the log-gap between its ceiling and the real words (§A.5: helpers 87–93 %, fragmentation
19–25 %, hosting −7 to −18 %), prices helpers and descents per call (§C.7, §E) and gives a moment-cost census by
class (§E.2). Those results answer "how much is left, and what does each helper cost?". The chain here answers a
different question, "what is κ made of?", as an identity on published profiles. Its new content is only the
four-factor identity and the historical comparison in §4.1.

## 4.3 Remark: many paid pieces per role cap a, for any label family

The hub's ceilings are route-specific: #183 (κ < a/(1+a)), #458 (whole-hosted format, κ < 2/127), #203 (fixed data
calls, < 8.9·10⁻³), #201 (paired-cube design, < 2.56·10⁻³), Swapnil Jain's a ≤ 1 − log_m 2 (P1/P2,
`docs/CLOSED_IDEAS.md` in Swapnil-jain/integer-mult-kappa), and #595's certified format ceiling κ ≤ 5.1595·10⁻³
(outward displays corrected in #602). #595 is much tighter than anything below *inside its scope* (B_K schedules,
star copies, the realised units). The statements below are weaker, but they need no schedule, copy or unit
hypothesis. They also bear on the open question "does anything rule out κ → 1?" (tara-sooo, fork issue 10).

**Framework assumptions (what "the framework" means here).**

- **H1** (moment recursion). a is the root above. F is increasing, and F(0) = 1 − δ.
- **H2** (outer assembly). κ < a/(1 + a) and κ < 1/4 (`docs/research/assembly-domain-audit.md`).
- **H3** (thin labels). Data terminal labels are lines (source U, sink U^⊥) and scratch runs from 0 to F. Label
  telescoping, as in the preprint's `lem:motif-residuals`, gives D ≤ #data roles ≤ W.
- **H4** (compressed hosted architecture). L = 2K + 1 invocations, W = 2Kv data roles per replica (plus any banks),
  m = 1 + L(h − 1), and D ≤ 2Kv − L·cst.
- **H5** (profile decomposition). The paid profile is L copies of the local word plus idle and bank children, each of
  rank ≤ m.
- **H6** (local window). Local children have rank ≤ h, and each source and target climbs h − 1 inside its window, so
  the local mass per invocation is ≥ 2v(h − 1) + cst. H6 holds on every certified word we checked, but **it is not
  proved for all words**.

**Theorem 1 (piece count) [P].** Take any profile with n ≥ W paid children, all of rank ≤ r̄. Then a is at most the
root for the two-point profile with the same (n, Σr, r̄). With r̄ = m:

  a ≤ D(m − 1) / ((m(n − W) + D)·ln m).

*Proof.* r ↦ r^{1−a} is concave, so the chord through r = 1 and r = r̄ is an LP-dual certificate that the two-point
profile minimises F at fixed (n, S, r̄); F is increasing in a. For the closed form, g(r) = r ln(m/r) is concave with
g(1) = ln m and g(m) = 0, so Λ ≥ ln m·(nm − S)/((m − 1)mW). Then apply a ≤ δ/Λ, which follows from
x^a ≥ 1 + a ln x. ∎

**Theorem 4 (thin-label decay) [P].** Under H3, if n ≥ (1 + ν)W, then a ≤ (m − 1)/((mν + 1) ln m) < 1/(ν ln m).
So any family with ν bounded below and m → ∞ has a → 0. (This is Theorem 1 with D ≤ W, since the bound increases
in D.)

At m = 73: ν = 1 gives a < 0.227, ν = 2 gives 0.114, and the observed ν ≈ 35 gives 6.6·10⁻³. The last value is
above #595's ceiling, as expected for a hypothesis-light bound.

**Copy-free window decay under H1–H6 [certified numbers].** With zero copy cost, local mass ≥ 2(h − 1) per line,
local pieces ≤ h and idle pieces ≤ m, the best stage count gives a ≤ 0.415 (h = 2), 0.115 (h = 4), 0.0460 (h = 8),
0.0400 (h = 9), 0.0208 (h = 16) and 0.00485 (h = 64). Here (h − 1)·a decreases from 0.415 to about 0.30. So **under
H6 no label family reaches κ → 1**: large windows lose like 1/h, and at tiny windows H2's κ < 1/4 binds first.
`scripts/piece_count.py` prints these values with interval certificates and checks the chord certificates.

**What is not claimed.** None of this is a ceiling below #595's inside #595's scope, and none of it bounds designs
that violate H3 or H6 (for example, merging active-window climbs into multi-window idle children). The lower bound
on n/W (ν) is itself unproved beyond a transfer-count lemma: #centres + #side-transfer terms ≥ v.
