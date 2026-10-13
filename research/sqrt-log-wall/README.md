# The square-root wall: every current assembly has κ < 1/2

**No new κ is claimed.** This note proves a ceiling that holds for the manuscript and for every assembly in the
repository: an algorithm built on the shared framework runs in time at least of order n·√(log n), so
κ ≤ 1/2. Within each assembly's own accounting the bound is strict, κ < (1 − δ)/2 < 1/2.

The selected record, κ = 0.001635527380375392 (`certificates/selected-result.json`), sits about 306× below the
wall. The largest κ among the tex assemblies is the paired-cube note's 4.609169·10⁻⁴, about 1085× below it.

`wall_check.py` checks each step against the source text and the selected certificate:

```sh
python3 -B research/sqrt-log-wall/wall_check.py
```

It uses the standard library only and ends with `PASS_SQUARE_ROOT_WALL_REDUCTION`.

## The reduction every assembly keeps

All ten tex assemblies keep the manuscript's reduction (`upstream/build/sections/08-assembly.tex`):

- the manuscript itself;
- `notes/{batched, copied-centers, endpoint-gauge, paired-cube, partial-gauge, partial-swap, stopped-product,
  structured-bulk, three-stage-cover}-assembly.tex`.

So do all 122 research outer engines that define margins (`research/**/outer.py`), including the one behind the
selected record. The reduction has four parts.

1. **The box.** The product becomes a d-dimensional cyclic transform on T points, with `Tp = Θ(n)` stored bits
   (eq. `sizes`). The axis lengths satisfy `t_i ∈ {r/2, r}`, `∏ t_i = T`, `r = 2^ℓ`, so
   `d·ℓ ≥ log₂ T = log₂ n − O(log log n)`.
2. **One pass per butterfly level.** Each axis has ℓ radix-2 levels. The framework runs them as at most ℓ
   *simultaneous rounds*, one level on all d axes per round, at `O(V d^{λ'})` per round (Proposition
   `simultaneous-layer`). It also runs packed products on records of length r.
3. **One pass per axis.** The Gaussian resampling is a tensor product of d line maps, applied axis by axis ("axis i
   has at most T/t_i processed lines"). Chirp numerators are "sums of d terms".
4. **A fixed accounting `T(n) = O(n p^{1−κ})`.** Every assembly carries two rows that follow from the two kinds of
   pass, and requires κ below each margin:
   - the **dimension** row, margin ε (manuscript: "Packed polynomial products & log(rp) & 1 − ε");
   - the **scalar-work** row, margin 1 − ε − δ (manuscript: "Chirps, twists and scalar products & dp^δ & ε + δ";
     three notes use the smaller 1 − δ − 2ε).

## Theorem (square-root wall)

Any algorithm that performs the framework's ℓ level rounds and d axis passes over the full box runs in time
Ω(n·√(log n)). Hence κ ≤ 1/2. Every assembly in the repository satisfies the strict bound κ < (1 − δ)/2 < 1/2.

### Proof

1. **Level passes.** A round reads and writes every stored bit, so it costs at least V = Tp, however well the motif
   networks accelerate the butterflies. ℓ rounds cost at least ℓV. The manuscript charges each round
   `V d^{λ'} ≥ V`.
2. **Axis passes.** Each of the d Gaussian line passes also processes every coefficient, so together they cost at
   least dV.
3. **Combining.** The time is at least
   (d + ℓ)·V ≥ 2√(dℓ)·V ≥ 2√(log₂ T)·V = Ω(n√(log n)),
   because V = Θ(n) and log T = Θ(log n). Comparing with T(n) = O(n (log n)^{1−κ}) gives 1 − κ ≥ 1/2.
4. **Strictness in each assembly.** The rows require κ < ε and κ < 1 − ε − δ. The maximum of
   min(ε, 1 − ε − δ) over ε is (1 − δ)/2, attained at ε = (1 − δ)/2. Every assembly has δ > 0, so
   κ < (1 − δ)/2 < 1/2. ∎

The pass bound alone allows κ = 1/2 exactly: Ω(n√log n) is consistent with O(n (log n)^{1/2}). Strictness comes from
the rows.

## The network side meets the same wall

The butterfly row has margin ε(1 − λ′) = εq with q = 1 − λ′ (manuscript row "Simultaneous butterfly rounds";
research engines `compact_phase_layer = eps*q`). Every assembly requires τ < λ < λ′ < 1, so q < a = 1 − τ. Then

κ < min(εa, 1 − ε) ≤ a/(1 + a),

attained at ε = 1/(1 + a). The manuscript takes 0 < τ < 1 as a hypothesis on its motif ratio `s/W < m^τ` (§3,
Proposition `power-interchange`), so a < 1 and κ < 1/2 again.

A perfect interchange (τ → 0) and perfect layers would only bring κ up to this wall, never past it.

## What it does and does not say

**It holds against** any improvement to:
- the networks, frames or recurrences (rank-1, weighted or pressure-identity);
- the Gaussian, chirp or packing constants;
- any assembly parameter (ε, c, β, λ, λ′, δ, C₁).

**Escaping it** needs a change to the skeleton itself, for example:
- several butterfly levels per pass;
- axis passes fused into fewer than d sweeps;
- a reduction other than the d-axis box.

The ten tex assemblies and the 122 research outer engines on main do none of these.

**Where the assemblies stand.**
- **Research engines.** These include the selected record, κ = 1.6355·10⁻³, ε = 0.998364, δ = 1.25·10⁻²⁵. Here the
  binding rows are εq and 1 − ε − δ ≈ q, so κ < q/(1 + q) with q ≈ a. That is κ ≈ a, the bit-network saving.
  Their constraint `complex_below_one_over32` also gives a < b < 1/32.
- **The manuscript's literal assembly.** It has the tighter cap 1/20: it needs εC₁ < 1 with C₁ = 20, and κ < ε.
  Its binding margin is g₂ = εc(1 − τ), with ε(2 − τ) < 1 − τ and τ(1 + c/β) < λ < 1. So ε < a/(1 + a) and
  c < βa/(1 − a), which gives κ = O(a³).
- **The three balanced-prefix notes** (batched, endpoint-gauge, partial-swap) have rows 1 − 2ε and εa_b, so
  κ < a_b/(2 + a_b) < 1/3.

Inside the wall, the real limit is the bit-network saving a. No all-network upper bound on a is known.

## Scope

- This is a structural statement about the framework's schedule and accounting. It is not a lower bound for
  integer multiplication in general.
- The pass bound assumes each level round and each axis pass reads every stored bit of the box. This is how the
  manuscript and all current assemblies are written.
- No Lean proof is claimed.

See `NOTICE.md` for credits.
