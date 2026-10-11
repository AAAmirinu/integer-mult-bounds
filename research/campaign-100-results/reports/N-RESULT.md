# N-centre-lemma — the open lemma behind idea 26 (ℓ = h(h−3)), decided computationally at p = 5, 6, 7

**Verdict: lemma holds at small p (no counterexample).** Every decoder found at p = 5, 6, 7 has centre mass
Σ_j dim span(supp f_j) ≥ h(h−2) (= 80, 120, 168); the point stars attain it and nothing beats them under
simulated annealing (≈ 4·10⁸ proposals over 17 Daytona runs + local runs), library CP-SAT over ≈ 3–12 k
structured centre candidates, or exact enumeration inside the star span. A general proof is **not** obtained:
the only rigorous lower bounds I can state are ≈ h(h−4) (clique counting) and "h(h−2) inside the star span";
the gap h(h−4) … h(h−2) is exactly what a proof must close, and I explain why the clique method cannot. No κ
change results (idea 26 stays blocked); the "I − J/s²" port-size family (idea 20) is priced out as well.

Files: `/tmp/radical/N/nlib.py` (instance, F₂ delivery check, exact Q-rank mod 2⁶¹−1), `sa.c` (annealer),
`mkinst.py`, `libsat.py` (CP-SAT over a candidate library), `cstar.py`, `cliques.py`, `rho.py`, `idea20.py`,
`showdesign.py`, Daytona launchers `dt_sa.py`, `dt_sa2.py`, `dt_check.py`, logs `sa_*.log`, `libsat_p5.log`,
`libfix_p6_0.log`, designs `dt_out_*.txt`.

## 1. What the lemma is, pinned to the code

* Ports S = triples of [h] with one coordinate from each of three pairs (2i, 2i+1), v = 8·C(p,3)
  (`paired_cube_bit_word.py:15-16,187`). Labels χ_S ∈ Q^h; Gram H0 = (I − J/9)/2 gives B_{T,S} = (|T∩S|−1)/2
  (`notes/paired-cube-construction.tex:1-15`). B = G Fᵀ with F_{S,i} = [i ∈ S] (the h stars, columns f_i =
  "sum of the ports touching coordinate i") and G_{T,i} = (3[i∈T] − 1)/6: (B x)_T = ½Σ_{i∈T} S_i − ⅙Σ_i S_i
  (`paired-cube-construction.tex:74-79`).
* The verifier only checks the **mod-2** decoder (`check_paired_cube_bit.py:176-212`): for every target T,
  (XOR of the centres T reads) ⊕ (side roots + partner-pair deliveries) = {T}, where the side part must be exactly
  Σ_{|S∩T|=1} x_S — those are the ports whose label lies in the cap ker(3χ_T − 1), the only sources a target may
  read directly (`:247`, `base_word.py:92`). Centre frames must equal the star span and are G-nondegenerate
  (`:241-249, :375`); ℓ = Σ_centres dim(frame) (`:249`), one copy transform of rank dim(frame) per centre and
  stage (`base_word.py:75`, `copied-centers-lemma.tex:37-60`: the copy is transformed D_U → D_0 at rank r and
  read at D_0, so a target can read any centre, and the only per-centre price is r = dim U).
* Hence the exact combinatorial content ("support span" = Q-span of the labels of the ports in the centre's
  support; the integer coefficients of the producer are irrelevant since J-arith showed the word is an F₂ object):

  **Lemma (decoder cost).** Let C ⊆ F₂^v be the span of centre functionals f_j = 1_{P_j} (P_j ⊆ ports). The
  decoder is realisable iff for every target T there is c ∈ C with c_T = 1 and c_S = 0 for all S ∈ N_T :=
  {S ≠ T : |S∩T| ∈ {0,2}} (orthogonal ports are free: side roots). Claim: Σ_j rank_Q{χ_S : S ∈ P_j} ≥ h(h−2).

  This is the memo's "for every factorisation B = G Fᵀ, any number of centres, not necessarily in the row space
  of B" made exact over F₂, and it is *more* permissive than the memo's version (the side channels are allowed
  to change; if the minimum is h(h−2) here it is h(h−2) a fortiori with "local channels unchanged").
  Sanity: the stars pass with cost h(h−2) (ranks all h−2; F₂-dim C = h) and the v singletons pass with cost v
  (`nlib.py` self-test: p=4 48/32, p=5 80/80, p=6 120/160, p=7 168/280) — so the lemma is **false at p = 4**
  (singletons, 32 < 48), a tie at p = 5 (v = h(h−2) = 80), and the real question starts at p = 6.

## 2. Searches run (all with exact Q-rank and exact F₂ delivery check)

| p | h | v | h(h−2) | best cost found | by | proposals / time |
|---|---|---|---|---|---|---|
| 5 | 10 | 80 | 80 | **80** (stars; also 80 from random starts = singleton-equivalent mixtures) | SA ×7 runs (3·10⁷ each), CP-SAT library (2,848 cands, 500 s) | ≈ 2·10⁸ |
| 6 | 12 | 160 | 120 | **120** (stars) ; random starts reach only 160–162 (singleton level) | SA ×8 runs (0.8–2·10⁷ each, stopped at the 3 h budget), CP-SAT library (5,906 cands, ≈ 45 min, best 161 from scratch) | ≈ 8·10⁷ |
| 7 | 14 | 280 | 168 | **168** (stars) ; random starts still infeasible at rank ≈ 225 when stopped | SA ×7 runs (0.8–4·10⁶ when stopped), CP-SAT library (11 k cands, no solution logged in 45 min) | ≈ 2·10⁷ |

Details.
* **SA (`sa.c`)**: state = list of port subsets; cost = Σ rank + 2·(#undelivered targets); moves = toggle 1–3
  ports, XOR two generators, move a port, add/remove a generator, XOR a structured mask (K_{ab} = ports ⊇ {a,b},
  stars, cubes, faces, pair-avoiders, sub-stars). Hot runs from the star seed (T₀ = 1.2) climb to cost 480–530 and
  cool back only to ≥ 120/168; cold runs (T₀ = 0.35) drift to 190–250 and never find < h(h−2). Random-start
  runs converge to singleton-equivalent designs (every generator an independent set: cost = v). **No feasible
  design below h(h−2) was ever proposed.**
* **Library CP-SAT (`libsat.py`)**: candidates = singletons, stars, K_{ab}, cubes, faces, pair/2-pair avoiders,
  two-pole sets Y_{cd} = {S : |S∩{c,d}| = 1} (rank h−1, the densest hyperplane sets), star XORs, all "ports inside
  a coordinate set X" and "ports inside X through c" for |X| ≥ h−4; reads g_{T,j} with XOR constraints per
  (T, S ∈ {T}∪N_T), objective Σ rank·y. p = 5: optimum 80 found at 15 s, no better in 500 s (bound stays 0 — the
  XOR model has no LP strength, so CP-SAT gives no lower bound). p = 6/7 on Daytona (3,000 s, 2 workers):
  nothing below the singleton level from scratch; forcing 11 of the 12 stars and forbidding the 12th
  (`libsat_fix.py`, 150 s) found no replacement cheaper than +111 (the solver is weak here; inconclusive).
* **Inside the star span C\* = span{star_c}** (`cstar.py`, exact): the support of Σ_{c∈A} star_c is
  {S : |S∩A| odd}; its rank over all 2^h − 1 choices of A is ≥ h−2, with equality exactly for the h stars and the
  p pair-avoiders A = [h]∖{c,c̄} (p=5: 15 elements of rank 8, 195 of rank 9, 813 of rank 10; p=6: 18/288/3789;
  p=7: 21/399/15963). Since dim C\* = h, **any generating set of C\* costs ≥ h(h−2)** (min-cost basis of a linear
  matroid = greedy). So a counterexample must have span ≠ C\*; J-arith's split census and this are the same fact.

## 3. What a proof has to do (and what the search suggests)

* **Necessary clique conditions.** For a clique K of the non-orthogonality graph Γ (S ~ T iff |S∩T| ∈ {0,2}),
  every T ∈ K needs a vector of C that is e_T on K, so the generators restricted to K span F₂^K: at least |K|
  generators meet K. Cliques: K_{ab} = {a,b,z} (size h−4, one per cross coordinate pair, 2p(p−1) of them) and the
  "4-set" cliques (all four triples on a 4-set of coordinates from distinct pairs, unions over disjoint 4-sets:
  size 4⌊h/4⌋; `cliques.py`: max clique 8/12/12 at p = 5/6/7). Counting incidences over the K_{ab} family gives
  cost ≥ 2p(p−1)(h−4)/ρ\*, ρ\* = max over port sets of (#coordinate pairs covered)/rank. If ρ\* were p−1
  (true for stars, pair-avoiders, the full set) this would be h(h−4). It is slightly larger: the two-pole sets
  Y_{cd} have (2p²−2p−2)/(2p−1) and random hyperplane sets reach 4.75/5.5/6.3 at p = 5/6/7 (`rho.py`), so the
  certified-by-sampling bound is 50/87/133 versus h(h−2) = 80/120/168. Moreover the clique conditions alone are
  satisfiable near h(h−4): a large set of 3-GDDs of type 2^p (h−4 pairwise block-disjoint GDDs partitioning all
  ports, each a generator of rank ≤ h and meeting every K_{ab} in exactly one port) meets them at cost ≤ h(h−4)
  but fails delivery because of the |S∩T| = 0 ports on disjoint pair-triples. **So the missing h·2 must come
  from the |S∩T| = 0 (disjoint-triple / antipode) conditions, not from the |S∩T| = 2 cliques.**
* **Restriction identity (the induction that would finish it).** Restricting a feasible design to the ports
  avoiding pair π gives a feasible design of the (p−1)-instance, so p·cost_{p−1} ≤ Σ_π Σ_j r(P_j ∩ A_π) =
  (p−2)·cost − Σ_j [Σ_π d_π(P_j) − 2 r(P_j)], d_π(P) = r(P) − r(P ∩ A_π). Stars satisfy Σ_π d_π = 2r with
  equality (d = 2 for the p−1 other pairs, h−2 for their own), singletons and cubes satisfy it strictly, and
  cost_p ≥ p/(p−2)·cost_{p−1} with base cost_5 = 80 gives exactly 4p(p−1) = h(h−2) for all p ≥ 5. The only
  violators of Σ_π d_π ≥ 2r are "coordinate-dense" generators with n(P) < 2 r(P) covered coordinates (full set,
  pair-avoiders, two-pole sets: deficit 2p, 2p−2, 2p−4). A proof therefore needs: (i) cost_5 = 80 exactly (p = 5
  is a tie with singletons, so this is a finite but non-trivial statement), and (ii) that dense generators cannot
  pay for themselves in a feasible design, i.e. the design-level inequality Σ_j Σ_π d_π(P_j) ≥ 2·cost. Both are
  what the computations support and neither is proved.
* Reductions that are rigorous and shrink the search: a generator with r(P) = |P| may be replaced by its
  singletons (same cost, larger span), and a matroid-separable generator by its components; so WLOG every
  generator is a singleton or a connected dependent set. An exact model over all such sets is out of reach: the
  port matroid at p = 5 already has 73,160 rank-3 and 1,043,250 rank-4 flats (3,000 / 127,410 of them "rich",
  `flats.c`), so a flat-enumeration ILP is infeasible and the XOR CP-SAT gives no bounds.

## 4. Idea 20 — port size s ≠ 3 (Gram I − J/s²), same lemma, same tool (`idea20.py`)

Orthogonality is |S∩T| = 1 for every s. Symmetric k-star designs (centres = all k-stars for k in a set K):

| s | p | h | v | cheapest delivering K | ℓ | ℓ/v | 4v − 5ℓ |
|---|---|---|---|---|---|---|---|
| 2 | 5 | 10 | 40 | {1} | 80 | 2.00 | < 0 |
| 3 | 6 | 12 | 160 | {1} (stars) | 120 | 0.75 | +40 |
| 4 | 5 | 10 | 80 | {2,3} | 560 | 7.00 | < 0 |
| 4 | 6 | 12 | 240 | {2,3} | 1440 | 6.00 | < 0 |
| 5 | 6 | 12 | 192 | {3} | 960 | 5.00 | < 0 |
| 5 | 7 | 14 | 672 | {1,3} | 2408 | 3.58 | < 0 |

For s = 3 the ratio is ℓ/v = 3/(p−2) (0.375 at p = 10, deficit 4v − 5ℓ = 2,040 > 0); for every other s the
cheapest symmetric centre family costs several times v, i.e. a negative deficit at every p tried, and the ratio's
leading term s(s−1)/(2(p−s+1)) only reaches 0.8 for s = 5 at p ≥ 17 (where v = 32·C(p,5) is astronomically
large). Singletons (ℓ = v) are always available and always negative. **s = 3 is the only port size for which the
five-stage deficit is positive; idea 20 is dead as a centre-mass lever.**

## 5. κ implication

None: no decoder with ℓ < h(h−2) exists at p = 5, 6, 7, and the mechanisms that would produce one (designs
outside the star span) were never found cheaper. For reference (J-arith / B's `whatif.py`): ℓ = h(h−3) = 340 at
p = 10 would be +3.8·10⁻⁵ uncapped, +2.43·10⁻⁶ under the complex cap; each unit of ℓ ≈ +1.9·10⁻⁶ uncapped.

## 6. Verdict

**Lemma holds at small p (p = 5, 6, 7: minimum = h(h−2) in every search; exact inside the star span; false only at
p = 4 where singletons win), undecided in general.** What remains for a proof: the finite statement cost₅ = 80
over all designs (not just the library), and the design-level inequality Σ_j Σ_π d_π(P_j) ≥ 2·cost (equivalently:
dense generators with fewer covered coordinates than twice their rank cannot be net-useful); with those two the
restriction induction gives h(h−2) for all p ≥ 5. Clique counting alone provably cannot do it (GDD large sets
reach h(h−4) on cliques). Recommendation for the ranked list: demote idea 26 from "open (15 %)" to "very likely
true lemma, ≤ 5 %"; the decoder-side deficit lever 4v − 5ℓ is closed unless someone finds a non-star span at p ≥ 6
below 120, which three independent search methods did not.
