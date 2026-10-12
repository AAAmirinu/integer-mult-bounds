# Lower bounds, coding gaps and two scoped limits (no κ claim)

Research notes. **No κ claim, no word, no certificate change.** The main topic is how #109 relates to known lower
bounds and to network coding (notes 1–2). Two smaller results follow: a minrank obstruction for Lorentzian label
families (note 3), and a decomposition of κ on published profiles with a piece-count remark (note 4).

Every statement is conditional on #109's Theorem 1, or on the hub's conditional interfaces where it touches a
supplier. Nothing here is a Lean formalisation, and no finite check below is a proof of the multiplication theorem.

```sh
python3 -m pip install -r research/lower-bounds-coding-gap/requirements.txt
DYSFUNCTOR=/path/to/network-coding-counterexample DRAT_TRIM=/path/to/drat-trim \
  bash research/lower-bounds-coding-gap/verify.sh /fresh/output/dir
```

Both environment variables are optional; without them, those two checks print SKIP or only write the proofs. The
full run takes about 20 seconds (Python 3.14.4 on WSL Ubuntu, fresh venv from `requirements.txt`).

## Results

Status: **proved** = a written argument, checked only by its authors, not independently reviewed or formalised;
**exact** = rational, exhaustive, or interval-certified computation by the named script; **audit** = a careful
reading, not a formal check; **conjecture** = not established.

| # | Result | Status | Where |
|---|---|---|---|
| 1.1 | #109 contradicts no unconditional lower bound for multiplication. Each bound fails on a stated hypothesis: on-line (Cook–Aanderaa, Paterson–Fischer–Meyer, Clifford–Jalsenius), bounded coefficients (Morgenstern, Bürgisser–Lotz), well-conditioning (Ailon), or Li–Li (AFKL). | audit | [note 1](notes/1-lower-bounds.md) |
| 1.2 | **Lemma B′**: #109's machine can be made **oblivious at the same κ** (fixed-width scalars, compute-both branches, oblivious Schönhage–Strassen inside the p^κ margin). Hence **#109 ⇒ bounded-degree Boolean circuits for multiplication of size O(n(log n)^{1−κ})**. | proved, given a procedure-by-procedure audit ([table](notes/1a-oblivious-audit-table.md)) | note 1 |
| 1.3 | **#109 ⇒ on-line multitape multiplication is slower than off-line by Ω((log n)^κ)** (via Paterson–Fischer–Meyer). So no relaxed variant of #109's transforms can have (log n)^{o(1)} overhead. | proved, given #109 | note 1 |
| 1.4 | "#109 ⇒ Li–Li false" holds via AFKL, but **it is moot**: Li–Li was refuted on 2026-10-07 by Zhang–Li–Li, by Braverman–He, and by dysfunctor's network built from #109's XOR swap. No error signal either way. | known | note 1 |
| 2 | **The rank saving is a coding gap.** On #109's labelled exchange network (edges weighted by rank or subspace distance), coding rate 1 and λ_flow ≤ (s + 2W)/(Wm + 2W). This is < 1 exactly when s < Wm, i.e. η > 0. It reproduces the paper's η exactly (bit 339/22587335000000, complex 73/19906842167500). It is the same mechanism as dysfunctor's instance, whose flow we re-certify as exactly 149/150. | proved (analytic LP dual); exact (`rank_metric_gap.py`, `mcf33.py`) | [note 2](notes/2-coding-gap.md) |
| 2.3 | Implied finite gaps of the community words (≈ 1.008–1.024) | conjecture (role-exchange composite not checked) | note 2 |
| 3 | **I_{11,1} and I_{13,1} (triples + pairs) have fitting minrank n, not n − 1**, over every field of characteristic ≠ 2. E8 = I_{9,1} is the case n − 9 = 0. | proved; SAT step exhaustive with **drat-trim-verified DRUP proofs** (`proofs/`); exact ranks over Q | [note 3](notes/3-lorentzian-minrank.md) |
| 3′ | The same for every odd n ≥ 7, n ≠ 9 | conjecture (SAT run only for \|X\| ≤ 12) | note 3 |
| 4.1 | **Loss chain**: a ≈ (1/m)(D/W)/L_ent with L_ent = ln m − E ln r, and κ ≈ a/(1+a). It reproduces gen4, #493, #501, #589 and the selected #596 supplier to < 10⁻⁸ relative; the selected row gives main's κ = 1.612721e-3. | exact (`loss_chain.py`) | [note 4](notes/4-loss-chain.md) |
| 4.3 | **Piece-count remark**: with n ≥ (1+ν)W paid pieces and thin labels, a < 1/(ν ln m). Under H1–H6, copy-free windows give a ≤ ~0.31/(h−1), so **no label family reaches κ → 1**. This is complementary to, and weaker than, #595's κ ≤ 5.1595·10⁻³ inside #595's scope. | proved (Theorems 1, 4); exact interval-certified numbers; H6 is an assumption | note 4 |

## What is new, and what is not

- **New, as far as we can find** (preprint, hub PRs and comments through #618, openai/math, AFKL, HvdH 2021/2025,
  the HN and blog discussion): Lemma B′ and the circuit corollary (1.2), the on-line/off-line separation (1.3), the
  identity in 2, the Lorentzian minrank result (3), and the loss-chain identity (4.1).
- **Not new, cited:**
  - Li–Li's refutation (Zhang–Li–Li arXiv 2610.09367; Braverman–He arXiv 2610.10108;
    [dysfunctor](https://github.com/dysfunctor/network-coding-counterexample)). Our 33-vertex computation is an
    independent re-check of dysfunctor's value.
  - The AFKL reduction itself.
  - Route-specific ceilings: #183, #458, #203, #201, Swapnil Jain's P1/P2, and #595/#602.
  - Helper prices, descents and the log-gap decomposition (#595 §A.5, §C.7, §E).
  - Lattice and label screens: #446; #595 C.6; #598 and #606 (DominikScholz); #620 (GamingPuzzled) with #630's E6 correction (vectorsss); hipotures; Sussman.
  - Conditioning: #621 and #628 (chafreaky), cited on the Ailon row of note 1.
- Our earlier "Hadamard-rank" observation (a saving needs different scalar and label characteristics) duplicates
  Swapnil Jain's closed-ideas list and Sussman's mod-2 argument, so it is **not** included.

## Scope

- No κ, b or c is claimed or changed. No production file outside this directory changes.
- Notes 1 and 2 concern #109's own construction and its consequences *if Theorem 1 holds*. They do not say whether
  it holds.
- Note 3 is a minrank statement about two graphs. It does not bound any supplier.
- Note 4's remark assumes H1–H6. H6 is checked on the certified words but not proved for all words, and the remark
  is not a universal ceiling.
- The SAT proofs are DRUP proofs from Glucose 4 (python-sat), checked with drat-trim
  (marijnheule/drat-trim @ 2e3b2dc, built with `gcc -std=gnu99 -O2`). The CNF files are regenerated and compared
  byte-for-byte with `proofs/`.

## Files

- `notes/1-lower-bounds.md`, `notes/1a-oblivious-audit-table.md`, `notes/2-coding-gap.md`,
  `notes/3-lorentzian-minrank.md`, `notes/4-loss-chain.md`
- `scripts/rank_metric_gap.py`, `scripts/mcf33.py` (note 2); `scripts/lorentz/` (note 3: `fam.py`, `explore.py`,
  `final_span.py`, `model.py`, `patsat_drat.py`, `cliq.py`, `todre.py`); `scripts/loss_chain.py`,
  `scripts/piece_count.py` (note 4)
- `proofs/patsat-{6,8,10,12}.{cnf,drat}`
- `verify.sh`, `requirements.txt` (the tested set: Python 3.14.4, Linux/WSL), `MANIFEST.sha256`, `NOTICE.md`,
  `LICENSE`

`cliq.py` (it lists the size-(n−1) cliques and writes `cliques<n>.pkl`) and `todre.py` (it writes dreadnaut input
for the automorphism-group orders 11! and 13!) are supporting tools. `verify.sh` does not run them, and the nauty
values are recorded, not replayed.

## Credits

Prepared by ShikeChen01 with substantial assistance from Claude Opus 5.5 (Anthropic), via Claude Code; Apache-2.0.
Upstream: OpenAI #109. Prior work used or cited: dysfunctor; Zhang, B. Li and Z. Li; Braverman and He; Afshani,
Freksen, Kamma and Larsen; Harvey and van der Hoeven; Jacob Sussman; Swapnil Jain; hipotures; DreamingOfClouds (#446,
#595, #589); artuskg (#602); DominikScholz (#598, #606); GamingPuzzled (#620); vectorsss (#630); chafreaky (#621, #628); jeremykothe2 (#596); eumemic (#493, #501). See `NOTICE.md`.
