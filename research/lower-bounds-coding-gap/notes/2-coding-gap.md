# 2. The rank saving is a finite network-coding gap

Status labels as in note 1. This note answers one question: is #109's saving the same mechanism as the known Li–Li
counterexamples, or something else? Answer: the same mechanism. A labelled motif with rank saving s < Wm is itself a
finite coding-versus-routing gap, and the size of the gap is fixed by η = 1 − s/(Wm).

## 2.1 The known counterexamples [K]

| Source | Construction |
|---|---|
| [dysfunctor/network-coding-counterexample](https://github.com/dysfunctor/network-coding-counterexample) @ `2ad45b0`, `writeup/` | 33 vertices, 91 edges, total capacity 149, 30 unit messages, each at hop distance 5. Built from #109's XOR swap: no source–sink path is layer-monotone, so routing pays 5 hops to climb 3 layers, while the code pays once per row and column with parity bits. Coding rate 1, routing ≤ 149/150. Lean proof in the repository. |
| Zhang–B. Li–Z. Li, arXiv 2610.09367 | a short completion-time code turned into a reversible circuit, amplified to (log n)^c |
| Braverman–He, arXiv 2610.10108 | a linear code over F₉ on a 182-vertex PG(2,9) incidence subgraph, flow ≤ 147/157, amplified to (log n)^ε |

**Independent check [exact computation].** `scripts/mcf33.py` reads dysfunctor's edge table, produced by their
own `verify-network-coding-33.py --print-edges` (nothing from that repository is vendored here). It solves the
edge-formulation concurrent-flow LP with HiGHS and with GLOP, then certifies **λ\* = 149/150 exactly** with a
rational dual (unit edge lengths) and a rational primal (path decomposition, rescaled).

## 2.2 Identity: the motif's rank saving is its coding gap [P; numbers exact]

**Instance.** Take the labelled exchange network of `03-motifs.tex` (bit or complex).

- Every role is demanded: X_a → Y_a, Y_a → X_a, and each scratch role returns to itself, so restored scratch is a
  carrier, as in dysfunctor's write-up.
- Subdivide each wire edge into as many unit edges as its frame cost. That is rank_Q(M_head − M_tail) for the bit
  network and |Δ dim| of the binary label for the complex network.
- Contract interior edges of cost 0, and add one pendant unit edge at each terminal.

**Coding rate is 1.** The scalar network routes one symbol per unit edge. The bit network works over F₂. The complex
network works over F₅ (i = 2, ½ = 3), because its scalars lie in Z[i, ½]. #109's Lemma scalar-motifs makes the
permutation exact for arbitrary scratch contents.

**Flow is below 1.** The edge costs are distances in a metric:

- the rank distance rank(M − M′) for the bit network;
- the subspace distance dim A + dim B − 2 dim(A ∩ B) for the complex network.

Every source–sink path costs at least the endpoint distance, and that distance is **m for every role**: #109's
Prop. bit-motif-interface gives M_sink(ρw) − M_source(w) = I_m, and d(U_a, U_a^⊥) = d(0, F) = m. The network has
s + 2W unit edges, where s is the paper's rank sum. LP duality with unit lengths gives

  λ_flow ≤ (s + 2W) / (Wm + 2W) < 1   ⇔   s < Wm,

and **s < Wm is exactly the paper's rank-saving statement** (η > 0).

`scripts/rank_metric_gap.py` rebuilds the paper's ledgers and reproduces its η exactly:

| network | η = 1 − s/(Wm) | flow bound | coding |
|---|---|---|---|
| bit | 339/22587335000000 | 1 − 1.50·10⁻¹¹ | 1 |
| complex | 73/19906842167500 | 1 − 3.67·10⁻¹² | 1 |

**Mechanism.** dysfunctor's layer index is a one-dimensional potential. Here the frame (a subspace or matrix) plays
that role. The route X_a → Y_a goes from U_a (dimension 1) to U_a^⊥ (dimension m − 1). Since U_a ⊄ U_a^⊥, no
monotone path exists, so routing pays m instead of m − 2: +2 per pair, the analogue of dysfunctor's "5 hops for 3
layers". The code pays only monotone climbs plus the 2L centre descents, which play the role of the shared parity
bits.

**Consequence.** The motif recurrence satisfies m^σ ≥ s/W = m(1 − η). So a positive saving from a motif is
equivalent to η > 0, which is equivalent to a finite coding/flow gap of at least 1/(1 − η) on the rank-weighted
motif network. The numerical C/H layers supply only the edge weights (kernel counts), the scalar XOR network supplies
the coding, and address permutations are wiring. We found no second gap mechanism in #109.

## 2.3 Community words [C]

The hub's words have the same per-invocation ledger: s = Rh + 2v(h − 1) + cst against a naive (R + 2v)h, for a
saving of 2v − cst. `rank_metric_gap.py` prints the implied gap ratios (≈ 1.008 for gcert1-p11, ≈ 1.024 for the
R560 E8 word). These are **not checked**. A single forward word (y += x) is not a role permutation and has no gap on
its own. The ratios assume that the compressed-window composite exchanges roles at endpoint distance m per role, as
the paper's three-stage composite does, and we did not verify that against the nine-window code.

## 2.4 Not done

- No LP on a faithful labelled #109 motif. The smallest paper-style motif with η > 0 needs h ≈ 21–22, so N = v³ is
  about 2·10⁹. The bound in §2.2 is an exact analytic dual and needs no LP.
- The exact λ\* of the motif instance was not computed, only the upper bound.
