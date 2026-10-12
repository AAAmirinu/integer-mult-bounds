# 3. Lorentzian label families: I_{11,1} and I_{13,1} have fitting rank n, not n − 1

Status: **proof** (paper argument, not independently reviewed, not formalised). Its finite steps are an
**exhaustive SAT check with DRUP proofs checked by drat-trim**, plus **exact rank computations over Q** (sympy). The
numerical searches mentioned in §4 are diagnostics, not evidence.

## 3.1 Setting

The E8 lines have a Lorentzian model: in Z^{9,1}, the 84 triples e_A + e_{10} (|A| = 3) and the 36 pairs e_i − e_j.
Their binary labels are the 3-set for a triple and the complement of {i, j} for a pair. This is the ordering of
Sussman's `tools/e8/e8.py` ([wht-power-saving-lean](https://github.com/jacobalansussman/wht-power-saving-lean) @
`9c94857`). The same recipe gives a family for every odd n ("I_{n,1} triples + pairs", v = C(n,3) + C(n,2)).
`scripts/lorentz/fam.py` builds it.

S **knows** T when S ≠ T and |label_S ∩ label_T| is even; no label knows itself (all weights are odd). For this
family "S does not know T" coincides with Lorentz product 0 (checked for n = 9, 11 by `explore.py`).

**Fitting matrix** (read from the gcert/1 checker, Sussman's `tools/gx/gx.py`, and the scatter rule of E8 totals):
a matrix B over the coefficient field with B_SS = 1, B_ST = 0 whenever S does not know T, and B_ST free otherwise.
The number of totals is at least rank B, so the least possible count is the Haemers-type minrank of the knowing graph
Γ_n. Equivalently B = R Gᵀ with r_U·g_U = 1 and r_U·g_V = 0 for every V in the non-knowing set Z(U); in particular
span{g_V : V ∈ Z(U)} lies in a hyperplane. A pairwise non-knowing set gives minrank ≥ n − 1, and the Lorentz Gram
matrix (rank n) gives ≤ n.

For n = 9 the minrank is 8 = n − 1 (E8's saving). The question is whether I_{11,1} or I_{13,1} also reach n − 1.
That would have been a cheaper unit than the Gram rank suggests.

## 3.2 Result

**Theorem.** For n = 11 and n = 13, minrank(Γ_n) = n over every field of characteristic ≠ 2. In characteristic 2,
Lemma B below already fails.

## 3.3 Proof

Suppose the rank is d = n − 1. Fix a centre a, let X be the other n − 1 points, and write P_xy = g_{xy},
T_xy = g_{axy} and Q_x = g_{ax}.

**Structure (exact).** The maximum non-knowing cliques of Γ_11 are the 10,395 sets
Cl(a, M) = {pairs e ∈ M} ∪ {a ∪ e : e ∈ M}, for a point a and a perfect matching M of the other 10 points.
(`explore.py 11` finds exactly 10,395 cliques of the maximum size 10, which is 11 × 945, the number of pairs (a, M).)
nauty reports |Aut Γ_11| = 11! and |Aut Γ_13| = 13! (`todre.py` writes the dreadnaut input).

**(F) Clique rule.** Each Cl(a, M) has d elements, so its g's form a basis and its r's form the dual basis. Hence
g_U ∈ span{g_T : T ∈ C, U knows T}. It follows that L_xy := span(P_xy, T_xy) is 2-dimensional, that L_e ∩ L_f = 0
for disjoint e and f, and that the six L_e with e inside a 4-set F lie in one 4-dimensional space W_F.

**Lemma A (σ-basis).** Adjacent L's meet. Otherwise W_{xyzw} would not depend on w, and six points would put
L_xy ⊕ L_zw ⊕ L_ut inside a 4-space. Adjacent L's are distinct and opposite ones are skew, so in P³ a K₄ line
configuration is a tetrahedron or a dual tetrahedron. The dual type propagates through 4-sets that share 3 points and
then forces all L_e of a 6-set into a 4-space, a contradiction. So there is a basis {s_x} with L_xy = span(s_x, s_y).

**Lemma B.** Z(T_axy) contains {P_uw, T_auw : u, w ∉ xy} ∪ {P_xy}, so the hyperplane of T_axy is
span(s_z : z ∉ xy) ⊕ ⟨P_xy⟩, and likewise for P_xy. Q_x is non-knowing to T_axy, and Q_z (z ∉ xy) is non-knowing
to P_xy. Writing Q_x = Σ q^x_z s_z, these give (q^x_u : q^x_w) = the T_uw-ratio for u, w ≠ x, and
(q^x_x : q^x_y) = the P_xy-ratio.

- **SAT step (`patsat_drat.py`).** Encode, for |X| = N, each P_e and T_e as "= s_u", "= s_w" or "generic", together
  with the zero-pattern relations above and Q_x ≠ 0, P_e ≠ T_e. For N = 6, 8, 10 and 12:
  - the base formula is satisfiable, with an all-generic model (calibration);
  - adding "some P_e or T_e is a basis point" makes it **unsatisfiable**. Glucose 4 emits a DRUP proof, and
    drat-trim reports `s VERIFIED`. The CNF and proof files are in `proofs/`, and `verify.sh` regenerates and
    re-checks them.
- In the all-generic pattern a cocycle argument, after rescaling the s, gives T_xy = s_x + s_y and
  P_xy = s_x + π s_y with a constant π = ±1. π = 1 makes P = T, which is impossible; in characteristic 2 this is
  where the argument stops. So **P_xy = s_x − s_y, T_xy = s_x + s_y, and Q_v = Σ_{u≠v} s_u − s_v.**

**Contradiction (`final_span.py`, exact over Q).** Take U a triple {x, y, z} not containing a, and Y = X − U. Then
Z(U) contains P_uw (u, w ∈ Y), P_e (e ⊂ U), T_auw (u ∈ U, w ∈ Y) and Q_v (v ∈ Y). The script checks every
membership. Modulo differences their span is ⟨s + t, 3s + (|Y| − 2)t⟩, with determinant |Y| − 5 = n − 9.

- n = 9: rank 7, a hyperplane, consistent with E8.
- n = 11: rank 10; n = 13: rank 12. In both cases this is the full space, which forces r_U = 0 and contradicts
  r_U·g_U = 1. ∎

The rank computation is over Q. For a field of characteristic p ≠ 2 the same conclusion needs n − 9 ≢ 0 (mod p),
which holds for n = 11 and 13; this step is argued from the determinant formula, not recomputed per field.

**Cross-check (`model.py`).** With the σ-model imposed, the clique rule (sampled over 60 centre-a matchings) forces
every other g. For n = 9 it outputs a valid rank-8 E8 fitting matrix with 0 violations. For n = 11 it reports 130
violating vertices: the 120 triples avoiding a and the 10 pairs {a, x}.

## 3.4 Why numerical searches cannot settle this

Local search for a rank-(n−1) B on I_{11,1} stalls at a plateau (objective ≈ 57–120), while warm starts from the
Lorentz solution converge (≈ 10⁻²⁶). The E8 control succeeds only because its basin is large (2 of 4 gauge-fixed
starts). So random-start searches are uninformative here, and the exact chain above replaces them. These diagnostic
scripts are not shipped.

## 3.5 Position against prior work

- The hub's E8 uniqueness and window results (#446, DreamingOfClouds), #595's pairing-uniqueness at the E8 pattern
  (C.6, SAT without proof logs) and erayyap's Haviv-bound argument concern E8 and F_q labels. They do not cover the
  Lorentzian family.
- hipotures' lattice screen ([rad](https://github.com/hipotures/rad/tree/main/research/integer-multiplication-bounds))
  ranks root lattices by deficit; Sussman's notes close fat labels. Neither covers I_{n,1} for n > 9.
- #598 (Leech / Turyn) and #606 (Niemeier), both DominikScholz, give scoped fitting bounds for other lattice
  families. This note is complementary: it is a complete minrank answer for one more family, with a proof.
- **Scope.** The result is about the minrank of these two knowing graphs. It does not bound κ for any word, and it
  does not exclude other Lorentzian label sets. The general claim for odd n ≥ 7, n ≠ 9, is **conjecture**: the SAT
  step was run only for |X| ≤ 12.
