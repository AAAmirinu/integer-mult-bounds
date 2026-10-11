# 100 radical, untested ideas for CrocSwap/integer-mult-bounds (2026-10-10)

Scope rule: nothing below is a stage lever (descent, squares, kernels, restorations, sinks, reorder, transport,
fixed prime), a module anneal, or a local-design anneal — all of those are in the repo. I scanned every
`research/*/README.md` on origin/main for the keywords; none of the items below appears there. Tags:
[hardcode] brute force / lookup tables, [months] would take months of compute even on hundreds of sandboxes,
[impractical] no human team would attempt it by hand, [math] needs a new proof before any run,
[ML] a search method the repo has never used, [enabler] makes other items possible.
Mechanism anchors: κ ≈ bit root c (moment-certificate root of the five-stage paid histogram at width m = 5h with
deficit 4v − 5h(h−2)), fed through a depth-3 outer chain from 384599·10⁻¹⁰, η = 10⁻¹², β = 10⁻⁹; the word is a
sequence of frame climbs and ADD gates over nested rational frames of Q^h; the generator is the paired-cube
program (pair module, all-but-one module, cube-local recipe trees, carrier matching).

## A. Hardcoding and brute force at a scale nobody has tried

1. [hardcode][months] **Free-form word.** The verifier only replays the word under PR200's word classes; it never
   needs the paired-cube generator. Treat the ~250,000-gate word itself as the variable: emit it as a literal table and
   optimise gate by gate (frame, operand order, coefficient) with the exact κ as objective and no generator constraint.
2. [hardcode][months] **Exhaustive cube-local design.** Enumerate every recipe tree for one cube class (the design is
   cube-local, so there are finitely many up to symmetry), price each physically, and ship the best as a lookup table.
3. [hardcode] **Frame-lattice table.** Precompute, once, every legal frame of every gate (closure under meet/join with
   its neighbours' chains) into a multi-GB table so that any later search samples legal moves in O(1) instead of
   re-running linear algebra; then run item 1 against it.
4. [hardcode][months] **Whole-word ILP.** One binary per (gate, candidate frame) over the table of item 3, nesting as
   precedence constraints, exact first-order objective; millions of binaries, Gurobi/HiGHS for weeks. The repo's ILPs
   only ever covered one stage at a time.
5. [hardcode] **SAT-enumerate the pair module.** The 273-addition pair module is a tiny bilinear program; ask a SAT
   solver for *all* programs with ≤ 260, 250, 240 additions computing the same map, and price each physically.
6. [hardcode] **Universal bank tiling table.** Pre-solve the (r⁴, 24ᵃ, 4ᵇ) tiling for every histogram in a large box
   once, so divisibility (restorations ≡ 0 mod 3, 60·width ≡ 0 mod m) never again drops pairs or restorations.
7. [hardcode] **Exact constant search in the outer polytope.** The 47 constraints and seven margins define a polytope
   in (η, β, grid, fallback, chain start); solve exactly for the best legal point instead of inheriting the constants.
8. [hardcode][months] **True root instead of certified root.** The moment certificate is only a bound on the root of
   the histogram price; compute the exact rational optimum (exact LP/SDP over all moment orders) and measure the slack.
9. [hardcode][months] **Largest-ever complex supplier.** Run the centre-sharing complex recipe at the largest size that
   fits 500 GiB and ship the explicit multi-million-gate complex word as a literal; raise the cap so the bit side is
   never capped again.
10. [hardcode][months] **Joint enumeration of orientation × design × matching.** #325 changed cube orientation by hand;
    enumerate all orientations jointly with the design and the carrier matching (the three interact through reuse pairs).
11. [hardcode] **Lagrangian DP per register.** Each register's chain is a path in a small poset; the only coupling is
    nesting across gates. Dynamic programming per register with Lagrange multipliers on the coupling, iterated to
    convergence — exact per-register optimality that greedy descent never reaches.
12. [hardcode][months] **GPU exhaustive entrance census.** Kernel entrances today come from lines, planes and their
    intersections; enumerate every rank 3–8 subspace spanned by helper read vectors on GPU (combinatorial explosion,
    weeks of GPU), then pack.
13. [hardcode] **10⁶ restart packings.** The closure packing used 16 seeds and 400 restarts; run a million restarts
    with a restart distribution fitted to the winners (item 71).
14. [hardcode] **Symmetry-reduced word.** Compute the automorphism group of the paired-cube word (S_p × cube symmetries
    × Z₂ pairing), optimise one orbit representative with exact methods, replicate by symmetry.
15. [hardcode][impractical] **Hard-coded optimal small instance, then lift.** Solve p = 4 (h = 8, v = 32) *exactly* by
    exhaustive search over all legal words (fits in days on 100 sandboxes), read off the structure of the optimum, and
    use it as the design template for p = 10/12.

## B. Changing the global shape (never varied)

16. **Map κ(p).** Only p = 12 and p = 10 words exist; build p = 8, 9, 11, 14, 16. κ is not monotone in p a priori
    (deficit 4v − 5h(h−2) scales differently from v) and nobody has drawn the curve.
17. **Mixed cube sizes** in one word (p = 10 and p = 12 blocks sharing centres), to tune v/h independently.
18. [math] **k-stage layouts for k ≠ 5.** The five-stage layout (PR234) fixes width 5h, 60 replicas and the idle ranks;
    derive the general k-stage completion and price k = 3…8 on the same word.
19. [math] **Non-uniform stage widths** (m₁…m₅ not all equal to h) with a matching completion proof.
20. [math] **Other Gram forms.** G = I − J/9 is inherited; find the admissible family (I − J/k, rank-two
    perturbations, block forms) and price the word under each.
21. [math] **Other idle-rank sets** than (2h−2, h−1, 2h+2, 4) — they are layout constants, not theorems.
22. [math] **Frames over number fields** (Q(i), Q(√2), Q(ζ₈)) or finite fields: more nondegenerate subspaces exist
    between the same cover vectors, so more kernel entrances and cheaper climbs may be legal.
23. [math] **Non-nested chains.** Allow a register's frames to form a lattice path that is not a chain, priced by a
    new certificate (climb + descent pairs); the "nested" rule is the single most binding constraint of every stage.
24. **Asymmetric words** with v_sources ≠ v_targets (the cube pairing forces equality today).
25. **Different centre design:** rank h−3 centres, 2h centres, or no copied centres at all (the 24 copies at rank 22
    are a fixed cost of 24·22 in every word).
26. [math] **Smaller ℓ = h(h−2)** completion geometry — the deficit term 5ℓ is paid by every word; a completion that
    needs only h(h−3) would be worth more than every stage lever combined.
27. **Two-level word:** gates that are themselves small verified words (recursive finite composition), mirroring how
    the outer assembly chains three levels.
28. [math] **Deeper outer chain.** The assembly iterates three times from 384599·10⁻¹⁰; re-derive the per-level
    margins to see whether four or five levels are legal.
29. **Make the complex side bind on purpose.** Push the bit root above the complex cap and optimise the complex
    supplier instead; the capped path of `math_check.py` has never been exercised by any package.
30. [math] **Lazy banks** without the mod-3 / mod-5 divisibility rules (a tiling theorem with padding priced exactly).

## C. New generator architectures (not the paired cube)

31. [impractical] **Superoptimised word:** program-synthesis search (as in superoptimisers) for the whole word from the
    specification alone, no cubes, no modules.
32. **Toom-Cook word:** evaluate/interpolate at k points instead of pairing cubes.
33. **Karatsuba-tree pairing:** recursive binary pairing of cube halves instead of flat pairs.
34. **Expander matchings:** choose the carrier matching that maximises the spectral gap of the reuse graph (more
    compensated reuse pairs) rather than any maximum matching.
35. **Cayley-graph indexing:** index sources by a group so every module is group-invariant and the local design is
    one representation-theoretic object.
36. **Character frames:** frames spanned by characters of Z₂^h are coordinate-aligned; every nondegeneracy check
    becomes Boolean and the frame lattice is enumerable.
37. **Tensor-rank modules:** treat the pair module as a bilinear map and use border-rank / Strassen-type
    decompositions; fewer additions means fewer climbs.
38. **Signed-digit coefficients** {−1, 0, 1} with carry-free accumulation, removing the 960 coefficient-3 events.
39. **Wallace/Dadda accumulation** of dirty responses (tree reduction instead of chains).
40. **Random legal words + repair:** sample words from a Markov chain over gates, repair with descent, price
    thousands — a distribution, not a single design.
41. **Transposed word** (swap sources and targets; the transposition principle gives the same map with a different
    histogram).
42. **MDS-code cover vectors** (Reed–Solomon parity checks) so that every h-subset spans — guaranteed nondegeneracy.
43. **LLL-reduced covers** to maximise the number of small-rank intersections available as entrances.
44. **Steiner-system pairing** S(2,3,v): every pair covered exactly once, no duplicate carriers.
45. **Triple (hypergraph) module** replacing pair + all-but-one modules.

## D. Certificate and analytic layer (where the big constants live)

46. [math] **Exact large-deviation root** (Cramér) instead of the moment bound.
47. [math] **SDP relaxation of the histogram price** as a second certificate type.
48. **Exact 10⁻¹⁸ grid accounting:** recover every rounding loss in the 47 constraints (small, but free).
49. [math] **Different concave price** than r·ln(m/r): prove a completion that prices rank r by a cheaper function.
50. [math] **True entrance-stock price** for initial entrances (today they are priced like climbs).
51. [math] **Fewer replicas** than 60 via a divisibility theorem on the bank tiling.
52. [math] **No fallback class** for either supplier (remove the 10⁻¹⁶ fallback cost entirely).
53. [math][months] **Lean the whole bound**, then let an automated prover search for the weakest sufficient
    hypotheses — the inherited "fixed finite-alphabet multitape" hypothesis is where the 384599·10⁻¹⁰ constant lives.
54. [math] **Smaller η, β** by re-deriving where 10⁻¹² and 10⁻⁹ come from.
55. **Optimise exact κ, not J.** Every search in the repo optimises the first-order proxy; the exact κ gradient over
    the histogram is computable and the two disagree at second order.
56. [math] **Mod-3 parity fusion:** the parity transform removes even additions in characteristic 2; a characteristic-3
    analogue could remove a second class.
57. [math] **Information-theoretic register price** (entropy of the response matrix rows) as a new certificate.
58. [math] **Alternative independence control** replacing the "omission control" so words with differently structured
    dirty responses become admissible.
59. [math] **Nested temporaries** (several COPY/ERASE lifetimes open at once).
60. [math] **Gate frames below operand spans** with a corrected integer replay (relax `span_violations`).

## E. Search methods the repo has never used

61. [ML] **GNN surrogate of physical κ** (76 s/eval → milliseconds) trained on the 100-chain data, then millions of
    design steps against the surrogate with periodic exact checks.
62. [ML][months] **AlphaDev-style reinforcement learning** over gate retimings with κ as reward.
63. [ML] **Evolutionary search with crossover** over local designs and modules.
64. [ML] **LLM program synthesis** of modules (they are tiny programs) with the verifier as the critic.
65. [ML] **MCTS** over frame-assignment sequences.
66. **Large-neighbourhood search:** CP-SAT on windows of ~1,000 gates with the exact objective, sliding over the word.
67. **Tabu search** on the kernel packing (never tried; only greedy/restarts).
68. [impractical] **QUBO on a quantum annealer** for the packing.
69. [ML] **Bayesian optimisation** of generator hyper-parameters (rank thresholds, gauge thresholds, tiering).
70. [ML] **Differentiable frames:** relax frames to the Grassmannian, gradient-descend, round to rational frames.
71. [ML] **Learned restart distributions** for packings (feeds item 13).
72. [ML] **Cross-size transfer:** learn an embedding of p = 12 designs and transfer to p = 10/8/14.
73. [ML] **Quality-diversity (MAP-Elites)** over histogram shapes instead of a single best.
74. **Cross-entropy method** for the carrier matching.
75. [months] **10,000-sandbox population search** with shared elites.

## F. Algebraic replacements of the suppliers

76. **NTT complex supplier** over Mersenne/Fermat primes instead of the centre-sharing complex word.
77. **Gaussian / Eisenstein integer bit words** (coefficients in Z[i], Z[ω]).
78. **p-adic / Hensel coefficient structure** (carries handled by lifting).
79. **Group-algebra word** over F₂[G] for non-abelian G.
80. **Quaternion packing** of four real products.
81. **Cyclotomic frames** (ideals of Z[ζₙ]).
82. **Montgomery/Barrett reduction** inside the word.
83. **Winograd minimal-multiplication filters** as the pair module.
84. **Rader/Bluestein structure** for prime cube sizes (p = 11, 13).
85. **Good–Thomas indexing** of sources (v as a product of coprime sizes).
86. **Clifford-algebra frames** (the repo retains "general Clifford" proofs but never built frames in one).
87. **Mixed-radix cubes.**
88. **Known-optimal small bilinear algorithms** (e.g. 3×3 in 23 multiplications) as modules.

## G. Enablers (make the impossible runs possible)

89. [enabler] **verify.py in C++/Rust** (100× faster replay) so months become days.
90. [enabler] **GPU/FPGA exact replay** of the F₂ and integer columns.
91. [enabler] **Incremental κ evaluator** — O(Δ) re-pricing per gate move instead of 76 s per evaluation.
92. [enabler] **Word compiler:** high-level description → verified package, so a thousand variants per day are possible.
93. [enabler] **Public dataset of every word and κ** for the ML items.
94. [enabler] **Pin-free development mode** for packages (today every experiment fights the pins).
95. [enabler] **Composable stage library** across packages (one stage stack, any base word).
96. [enabler][months] **Community compute pool** (persistent sandboxes with shared elites).

## H. The analytic theorem itself

97. [math][months] **Re-derive the inherited analytic theorem** with a stronger machine model (k tapes, larger
    alphabet); the chain start 384599·10⁻¹⁰ is the single biggest constant in κ.
98. [math] **Three suppliers** (bit, complex, and a ternary/NTT side) in the outer assembly instead of two.
99. [math][months] **Prove the limit κ(p → ∞)** of the paired-cube family analytically, so the bound is the limit
    rather than any finite word.
100. [math][impractical] **Replace the finite word by an infinite family certified by a parametric Lean proof** — a
     construction indexed by p whose κ(p) is proved for all p, ending the race of ever-larger literal packages.
