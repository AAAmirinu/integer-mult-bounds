# Proof: twisted outputs are at most paid odd shears minus one

## Setting

One central port. The caller word of `research/p104-productive-controller/caller.py` acts on `n = 32` banks
(16 pairs). A bank holds an element of `R = K[Q, Q⁻¹] ⊗ K[D_0, …, D_33]`, `K = ℚ`; the banks start as the rows of
the constant right boundary matrix (invertible), and the constant left boundary matrix is applied at the end. The
alphabet is replayed literally:

| event | action on the rows | kind |
|---|---|---|
| `ADD y x c` | `y += c·x`, `c ∈ K` | free |
| `SWAP`, `SIGNED_SWAP` | exchange two rows, one sign | free |
| `Q_POWER r ±2` | `r *= Q^{±2}` | free (even central powers are translations) |
| `IDLE pair S` | both rows of the pair `*= ∏_{s∈S} D_s` | free in this count (its rank-`8|S|` price is a lift, cancelled by the target rank) |
| `LOCAL s pair back` | `y += Q^{-1}·x` (or `x += −Q·y` backward), then both rows `*= D_s` | **paid odd shear** (one full call) |
| `QUERY_SHEAR s pair back` | `y += Q^{-1}·x` (or `x += −Q·y`) | **paid odd shear** (one rank-one request per port) |

Write every row as `a + Q·b` with `a, b ∈ R_even = K[Q^{±2}] ⊗ K[D]`; `a` is the **even part**. Let `E` be the
`n × n` matrix over `R_even` whose rows are the even parts, and `rank E` its rank over the fraction field of
`R_even`.

## Lemma

1. Every free event is an invertible row operation of `(E | odd parts)` with coefficients in `R_even` (constants,
   `Q^{±2}`, monomials in `D`); it preserves `rank E`.
2. A paid shear `y += Q^{±1}·x` changes exactly one row of `E`: `E_y += Q^{±1}·(odd part of x)`, which lies in
   `R_even`. So `rank E` changes by at most one.
3. Before the first paid shear every odd part is zero (the right boundary is constant), so the first paid shear
   does not change `E` at all.
4. A row that ends as an odd monomial `Q^{±1}·D^S·e_i` (every declared diagonal output) has zero even part.

**Theorem.** With `s` paid shears and `n_odd` outputs that are odd (zero even part),

    n_odd ≤ n − rank E_final ≤ n − (n − (s − 1)) = s − 1 .

Proof: `rank E` starts at `n` (invertible right boundary), stays `n` through free events and the first paid
shear, drops by at most one at each of the other `s − 1` paid shears, so `rank E_final ≥ n − (s − 1)`; the
`n_odd` zero rows give `rank E_final ≤ n − n_odd`. ∎

The verifier evaluates the same argument after the ring homomorphism `D_s → 1`, `Q² → θ` (`θ = 7/3`, `11/5`):
items 1–4 hold verbatim in the image, so the per-event rank trace is a complete check on the given word.

## Consequence for the complete invoice

Let a caller use `n_thick` full calls and `n_thin` thin shears, all on one pair each, and let every one of its
`n_out` outputs be an odd monomial with stage set `S_i` (target rank `1 + d·|S_i|`, `d = 8`). Every stage that
appears in an output was paid once as a lift of that content (`d` per bank per full call or per idle stage), so

    income per port = Σ_i (1 + d|S_i|) − d·(lifts) − n_thin = n_out − n_thin ≤ (n_thick + n_thin − 1) − n_thin = n_thick − 1 .

The three retained p16 controllers have `n_out = 32`, `n_thin = 15`, `n_thick = 18`: income `17 = 18 − 1`, the
bound with equality (checked from the literal words in `RESULT.json`).

With `v` ports and a local word that loses `c` units of rank mass per full call outside the main lifts (the owned
centre: `c = 56` on the PR5907 word, `64` on #4610), the complete rank-mass surplus is

    M = v·(income) − n_thick·c ≤ n_thick·(v − c) − v ,

equal to `18·48 − 104 = 760` on PR5907. Each additional thick call can add at most `v − c` units of surplus, and
no change of the caller graph inside this alphabet (path or not, any prefix/suffix idle law, any pairing of thin
shears) can add more. The remaining complex-side levers are therefore the centre `c`, the fragmentation of the
local word (which enters the moment, not the mass; see `research/fragmentation-ceiling`), and the moment cost of
the target ranks that grows with `n_thick` (which is why `p = 16` is optimal for the retained local profile,
PR5554).

## Relation to the binary theorem

`research/productive-controller-basis-search/GLOBAL-PROOF.md` (Cinna Davis), Theorem B, proves the count
`queries ≥ 2p + 1` for `2p` independent monomial outputs over `F₂[Q]/(Q² − 1)` with constant binary boundaries
and without idle work, by the rank of `n` rank-one nilpotents summing to the identity. The lemma above is the same
count in the retained complex alphabet: `K = ℚ`, `Q` a Laurent variable with `Q² ≠ 1`, free idle markers, outputs
counted one by one (so partially twisted words are covered), and it is read off the even-part rank rather than
the derivative at `Q = 1`. The pruning remark of that package's `PROOF.md` ("a query changes the even part from
`E` to `E + NO`, so its rank can fall by at most one") is the step (2) of the lemma; here it is made the whole
argument, with the first-shear refinement (3) that gives the `− 1`.

## Scope

The alphabet is the literal one of the retained callers; a paid job that touches several banks or several ports at
once (a cross-port or multi-bank primitive) is outside it and is the only way to escape the bound (see
`TASK.json`, open questions). The bound is on rank mass; it says nothing new about the moment at `t < 1`, where
PR5554's convexity argument and the fragmentation ceiling apply.
