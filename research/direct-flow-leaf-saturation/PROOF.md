# A nonlattice saturation theorem for the fixed #4467 leaf law

This is a scoped mathematical proof using the classical nonlattice interval local-limit theorem stated below. The Python certificate verifies its source-specific numerical hypotheses and finite source-law controls; it is not a proof-kernel verification of this argument. No finite-depth error rate is claimed.

## 1. Source law and statement

Use the fixed raw-p7 inventories in Ryanson Jonathan / pinterbanget's #4467 (`research/direct-flow-leaf-walk/verify.py`):

```
P = {1:37305, 2:10695, 3:3360, 4:1530, 5:300,
     8:1464, 16:448, 32:448, 48:448}
W = {5:420, 6:270, 7:840, 8:1395, 9:3195,
     25:448, 41:448, 57:448, 121:224}
m = 121
```

Let `Z(s) = Σ_r P_r r^s`, `μ(s) = Z'(s)/Z(s)`, and let `t` be the unique root of `Σ_k W_k k^t = Z(t)` in the certified interval `[0.99731351095114, 0.99731351095116]`. Put `a = log 5`. Let `α` be the unique solution of `μ(α)=a` and set `λ=t−α`.

The certificate also bounds the invoice derivative strictly above 211661 on the predecessor’s entire bisection interval `[0.99,1]`, so the isolated root is its unique root there. The certificate proves `μ(t)>a`, `α∈[0.98981438244597, 0.98981438244599]`, and thus `λ∈[0.00749912850515, 0.00749912850519]`. All intervals here are outward bounds, not floating-point root guesses. Uniqueness of α follows from `μ'(s)=Var_s(log r)>0`, its limits 0 and log48 at the two infinities, and `0<a<log48`.

Under `p_t(r)=P_r r^t/Z(t)`, take independent `X_i=log R_i` and write `S_G=Σ_{i=1}^G X_i`. For any `δ∈[0,a]` let `B_G=Ga+δ`, and condition on `S_G≤B_G`. Define `Y_G=B_G−S_G` on that event.

**Theorem.** Uniformly for `δ∈[0,a]`, as `G→∞`,

1. `P_t(Y_G≥x | S_G≤B_G) → exp(−λx)` for each fixed `x≥0`;
2. `E_t[Y_G | S_G≤B_G] → 1/λ`.

The condition has positive probability because `P_1>0`.

**Actual leaf consequence.** For every integer rank `N≥121`, set `G=floor(log_5(N/121))` and `δ=log(N/121)−G log5∈[0,a)`. The potential-weighted mean leaf log-depth in the pinned flow satisfies

`D_leaf(N) → log121 − μ(t) + 1/λ ∈ [136.51870330,136.51870331]`

as `N→∞`, including sequences approaching either end of a lockstep level. There is no restriction to the level starts `N=121·5^G`.

## 2. Why this is the source's measure

The pinned `diagnostics/overlap_flow.py` constructs `F[d][ρ]` by multiplying `d` paid ranks and retaining a new product precisely when `121·ρ≤N`. All paid ranks are positive integers, so their logarithms are nonnegative: the final product constraint implies every earlier constraint. Consequently `F[G][ρ]` is exactly the sum of `Π_i P_{r_i}` over ordered G-tuples with product ρ and `ρ≤N/121`.

In its `d==G` branch, the flow issues *every* final rank `r` with multiplicity `F[G][ρ] P_r` at exit rank `rρ`. This final rank is **not conditioned** by `121·rρ≤N`. Weighting by `(rρ)^t` factorizes into the conditioned G-step law above and an independent terminal `R` with law `p_t`.

Thus, exactly at every finite N,

`E[log(N/(Rρ))] = log121 − μ(t) + E[Y_G | S_G≤B_G]`.

This G-versus-G+1 distinction matters. The checker independently enumerates ordered words through G=3 and compares all leaf multiplicities with the whole-flow `X−BX`; an extra-terminal-truncation mutant fails. The source audit also checks the original #4436 flow. These are finite controls for the source derivation, not evidence for the asymptotic theorem.

## 3. The classical input and its hypotheses

We use the nonlattice interval local-limit theorem in the following standard form. If iid real `V_i` have mean zero, finite positive variance `σ²`, and a nonlattice law, then for each fixed `h>0`,

`sup_x | sqrt(G) P(Σ V_i∈[x,x+h)) − h/(σ sqrt(2π)) exp(−x²/(2Gσ²)) | → 0`.

Reference: C. Stone, “A local limit theorem for nonlattice multi-dimensional distribution functions,” *The Annals of Mathematical Statistics* 36(2) (1965), 546–551, [DOI 10.1214/aoms/1177700165](https://doi.org/10.1214/aoms/1177700165), one-dimensional specialization. This theorem is an external mathematical dependency; it is stated here rather than silently replacing a discrete distribution by a density. Its asymptotic form supplies no explicit error constant or onset G.

Apply it to the tilted law `q(r)=P_r r^α/Z(α)`, with `V=log r−a`. Its mean is zero by definition, and its variance is positive and finite because the support is finite and contains distinct points of positive mass. The support is nonlattice: it contains `0,log2,log3` before centering. If all belonged to a translate of `hZ`, their differences would imply `log2/log3` rational. An integer relation `u log2=v log3` with nonzero integers would imply `2^u=3^v`, contradicting unique factorization. Centering and tilting do not alter this property.

Two consequences are used:

- For fixed finite intervals in y, `sqrt(G) Q(B_G−S_G∈I) → |I|/(σ sqrt(2π))`, uniformly over bounded δ.
- There is a constant C such that for all `G≥1` and all real x, `sqrt(G) Q(S_G∈[x,x+1))≤C`.

The second follows from the theorem for h=1 for sufficiently large G, and enlarging C for finitely many smaller G. It is an existence bound, not a computable convergence rate. Either convention for half-open intervals works: the maximum atom is `o(G^(-1/2))`, by bounding it with an interval of arbitrary fixed h and then taking h down to zero. This also handles an atom at the exact truncation boundary.

## 4. Weighted local limits and integrable tails

Write `c=1/(σ sqrt(2π))`. For the nonnegative functions

`f_0(y)=exp(−λy)`, `f_1(y)=y exp(−λy)`, and `f_x(y)=1_{y≥x} exp(−λy)`,

we claim, uniformly in δ,

`sqrt(G) E_q[f(B_G−S_G) 1_{S_G≤B_G}] → c ∫_0^∞ f(y)dy`.

On a fixed compact interval this follows by upper and lower step-function approximations and the interval local limit. The functions are bounded and Riemann integrable there, including the single jump of `f_x`; the possible boundary atom is negligible by §3.

For an integer `J≥0` and the tail partition into intervals `[j,j+1)`, the concentration bound in §3 gives, uniformly over G and δ,

`sqrt(G) E_q[f_0(Y_G) 1_{Y_G≥J}] ≤ C Σ_{j≥J} exp(−λj)`,

and

`sqrt(G) E_q[f_1(Y_G) 1_{Y_G≥J}] ≤ C Σ_{j≥J} (j+1) exp(−λj)`.

Here Y_G denotes the unconditioned difference `B_G−S_G` inside the indicated nonnegative event. Both series tend to zero as `J→∞` because λ>0; `f_x≤f_0` has the same domination. This proves the weighted local limits and supplies the missing uniform-integrability argument for the mean. Weak convergence alone would not suffice.

## 5. Undoing the tilt

For an ordered G-tuple,

`p_t(tuple)/q(tuple) = (Z(α)/Z(t))^G exp(λ S_G)`.

On writing `S_G=B_G−y`, the common factor `(Z(α)/Z(t))^G exp(λ B_G)` cancels in every conditional ratio. Hence

`P_t(Y_G≥x | S_G≤B_G) = E_q[f_x(B_G−S_G) 1_{S_G≤B_G}] / E_q[f_0(B_G−S_G) 1_{S_G≤B_G}]`,

and the analogous numerator with `f_1` gives the conditional expectation. By §4, the three scaled integrals converge to `c exp(−λx)/λ`, `c/λ²`, and `c/λ`. The denominator limit is strictly positive, so their ratios converge uniformly over δ to `exp(−λx)` and `1/λ`. Section 2 then gives the claimed leaf-depth limit.

## 6. Scope, controls, and remaining decisions

This proves the saturation that #4467 explicitly labelled heuristic. It does **not** prove its suggested total log-gap `g∞≈122`, stable source/boundary/leaf shares, any numerical refined-induction ceiling, or the quoted astronomical ranks required to achieve a saving. Those require separate control of other flow components and a finite-depth estimate. The raw-p7 inventory is historical and is not the selected #6030 invoice.

Nonlattice support is essential for this limit law. For `X∈{0,log2}` with probabilities `(1/3,2/3)` and even G, conditioned at `B_G=G log2/2`, λ=1 but the limiting deficit is `log2` times a geometric variable with probabilities `2^(-j-1)`, j≥0. Its mean is `log2`, not 1. Indeed the successive binomial mass ratio below G/2 tends to 1/2 and is bounded by 1/2, which proves both the geometric limit and mean convergence by domination. The verifier includes this failure control. Zero or negative relative drift likewise lies outside the theorem's λ>0 hypothesis.

Credit: the flow is zxv's #4436, the refined induction is Cinna Davis / 1337isnot1337's #4405, the lockstep construction is Jacob Alan Sussman's Theorem 1G, and the source law, saturation conjecture and diagnostics are Ryanson Jonathan / pinterbanget's #4467 (following #4465). This proof and certificate were prepared for DLamdata with substantial OpenAI Codex assistance. Apache-2.0. Internal AI checks are not independent human review or formal verification.
