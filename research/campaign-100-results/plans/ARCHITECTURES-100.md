# 100 new word architectures for CrocSwap/integer-mult-bounds (2026-10-11)

These are constructions of the *finite word itself* — new decoders, new port geometries, new centre designs, new
module algebra — not optimisations of the paired cube. None appears in the repo's research directories (checked against
every README on origin/main) and none was built in the first campaign. What the verifier admits (from /tmp/radical/N and
/tmp/radical/M): ports S with labels χ_S ∈ Q^h, targets T with cover vectors, a decoder identity checked mod 2 in which a
target reads directly only ports with |S∩T| = 1, centres = port sets readable after one COPY of rank dim span(χ over the
set), modules = positive addition DAGs, five-stage price = moment root of the paid histogram at width 5h with deficit
D = 4v − 5ℓ (ℓ = Σ centre dimensions, v = sources, h = coordinates). The paired cube has v = 8·C(p,3), h = 2p, ℓ = h(h−2).
What every architecture is judged on: (a) is D > 0 and larger per port than the paired cube's 4 − 15/(p−2); (b) does the
decoder need fewer/cheaper climbs per target; (c) does it admit annealable modules. Each entry: the idea → what changes.

## A. Different port geometries (what a "port" is)

1. **Pairs instead of triples.** Ports = pairs of coordinate pairs (two coordinates), v = 4·C(p,2); targets need centres
   of rank h−1 or sparser covers; deficit per port changes from 4 − 15/(p−2) to a new series.
2. **Quadruple ports** (four coordinate pairs, v = 16·C(p,4)): more sources per h, centres span less of each port.
3. **Mixed-arity ports** (triples and pairs in one word) sharing centres.
4. **Simplex ports:** ports = k-subsets of a single coordinate set [h] (no pair structure), decoder by inclusion–exclusion.
5. **Projective-plane ports:** ports = lines of PG(2,q), two ports meet in exactly one point — the |S∩T| = 1 cap rule
   holds for every pair automatically.
6. **Affine-plane ports** AG(2,q): parallel classes give natural "partner" structure for free partner reads.
7. **Steiner triple ports** S(2,3,n): every pair of coordinates in exactly one port.
8. **Kirkman (resolvable) triple ports:** parallel classes become the five stages' idle families.
9. **Hypercube-vertex ports:** ports = vertices of Q_k, coordinates = edges; neighbours differ in one coordinate.
10. **Cyclic difference-set ports:** ports = translates of a planar difference set in Z_n; cyclic symmetry = one module
    for all targets.
11. **Grassmannian ports:** ports = 2-subspaces of F_2^k, labels = Plücker coordinates; centres = pencils.
12. **Hadamard ports:** ports = rows of a Hadamard matrix (±1 labels, pairwise orthogonal); Gram form becomes diagonal.
13. **Latin-square ports:** ports = cells, coordinates = row/column/symbol — three "pairs" per port with transversals as
    partner families.
14. **Tensor-product ports:** ports = (a,b) with a ∈ cube_1, b ∈ cube_2 (two small cubes), decoder = product decoder.
15. **Toroidal ports:** cube coordinates taken mod p (wrap-around) so every port has the same neighbourhood.
16. **Hexagonal / triangular-lattice ports** (coordinates on A_2 lattice instead of Z^3).
17. **Octahedral ports** (dual of the cube: ports = faces).
18. **Permutation ports:** ports = permutations of [k], coordinates = transpositions (Cayley graph of S_k).
19. **Binary-tree ports:** ports = leaves of a depth-d tree, coordinates = internal nodes; ancestor chains are frames.
20. **Random-hypergraph ports** with the pair-intersection property enforced by rejection sampling (tests whether
    regularity matters at all).

## B. Different decoders (how a target is reconstructed)

21. **Inclusion–exclusion decoder:** target = alternating sum over sub-ports, no centres at all (ℓ = 0, deficit 4v).
22. **Parity-check decoder:** targets are syndromes of a linear code over F_2 whose parity-check rows are the ports.
23. **Two-level decoder:** target = Σ over super-centres, each super-centre = Σ over small centres (ℓ counted once).
24. **Shared-centre decoder** with 2h centres of rank h/2 (lower total ℓ if the star structure allows).
25. **Rotating centres:** h centres but each copied at a different stage, so copies are spread across the five stages.
26. **Partner-chain decoder:** each target reads its partner, which reads its partner, … (a cycle of length k) so the
    partner contribution is amortised.
27. **Differential decoder:** targets encoded as differences of neighbours (T − T'), so the identity has half the terms.
28. **Walsh decoder:** targets = Walsh–Hadamard coefficients of the port vector; all reads are ±1 at full frame.
29. **Majority-logic decoder** (Reed–Muller style): target recovered by majority of several short sums — more reads,
    each at a smaller frame.
30. **Convolutional decoder:** targets indexed by time, each reading a sliding window of ports (frames climb once per
    window shift).
31. **Lifting decoder:** compute targets mod 2 by the usual identity and lift to Z by a separate carry word.
32. **Dual-cover decoder:** two cover vectors per target (a target reaches the h−1 cap via two different chains, pick the
    cheaper per instance).
33. **Partner-free decoder:** drop the partner read, replace by one extra centre of rank h−3 per pair.
34. **Centre-free decoder with gauge registers** (the "gauge" mechanism of PR144 used as the only global object).
35. **Recursive decoder:** a target of the big word is itself the output of a small verified word (two-level word).

## C. Different centre designs (the ℓ term)

36. **Half-stars:** centres = half of a star (rank ≈ h/2), twice as many — ℓ = h(h−2) only if the lemma is tight; test
    whether a split with total < h(h−2) exists for non-cube port sets.
37. **Line centres:** centres = all ports on a coordinate line (rank small), many of them.
38. **Random sparse centres** chosen by greedy rank minimisation for the given port set.
39. **Centres over F_2 only** (frames spanned by 0/1 vectors) for port sets where the cube's parity obstruction is absent.
40. **Centres as code cosets:** centre = coset of a small code in the port space, rank = code dimension.
41. **One giant centre** (rank h−1) read by every target plus per-target corrections.
42. **No copies:** centres live in the targets' caps so no COPY/ERASE is needed (requires a port set whose caps contain
    the centre span).
43. **Stage-local centres:** a different centre set per stage (five sets, each cheaper).
44. **Centres priced as entrances** (initial-frame objects) instead of copied helpers.
45. **Centre lattice:** centres form a chain C_1 ⊂ C_2 ⊂ … so copies telescope.

## D. Different algebra (the ring the word computes over)

46. **Z[i] word:** coefficients Gaussian integers; one complex multiply = one word (replaces the separate complex
    supplier).
47. **Z[ω] (Eisenstein) word** — 6 units, cheaper sign structure.
48. **Z[√2] word** — units of infinite order, coefficient reduction.
49. **Quaternion word:** four real products packed per word.
50. **F_4 / F_8 words** (characteristic 2 extension fields) — the mod-2 decoder becomes field arithmetic.
51. **Z/3 word with ternary parity transform.**
52. **Balanced-ternary coefficients {−1,0,1}** throughout (no coefficient-3 events by construction).
53. **p-adic word:** coefficients reduced by Hensel lifting at each stage.
54. **Montgomery-form word:** inputs pre-multiplied so every reduction is a shift.
55. **Group-algebra word over F_2[Z_2^k]:** convolution structure gives free "partner" reads.
56. **Cyclotomic word Z[ζ_n]:** the centres are ideals; n chosen so the Gram form is a trace form.
57. **Clifford-algebra word Cl(h):** frames = subalgebras; nondegeneracy automatic.
58. **Polynomial-ring word F_2[x]/(x^n+1)** (NTT-style): the word computes a cyclic convolution directly.
59. **Mersenne-prime NTT word** (mod 2^61−1): exact integer arithmetic in one register width.
60. **Fermat-prime NTT word** (mod 2^16+1).

## E. Different module algebra (what the modules compute)

61. **Karatsuba modules:** pair module computes (a+b)(c+d) − ac − bd style sums with shared sub-sums.
62. **Toom-3 modules:** evaluation at 5 points instead of 2.
63. **Winograd minimal filters** as modules.
64. **Strassen-type bilinear modules** (rank-7 2×2 products) for the pair step.
65. **Modules with negative coefficients** (positive DAGs are a convention — test whether signed modules are admissible).
66. **Modules shared across two cubes** (one module instance serving a pair of cubes).
67. **Hierarchical modules:** a module of modules (all-but-one of all-but-one).
68. **Prefix-sum modules** (Blelloch scan) — every root is a prefix, maximal nesting.
69. **Gray-code-ordered modules** so consecutive roots differ by one input (carrier arcs by construction).
70. **Fibonacci-tree modules** (unbalanced trees with many nested covers).

## F. Different global layouts (stage structure, still five stages)

71. **Two interleaved words** (odd/even targets) sharing idle families.
72. **Staggered stages:** stage k of word A runs with stage k+1 of word B so idle mass is shared.
73. **Mirror word:** the word followed by its own transpose (the reflected ledger is free) computing x·y and y·x
    jointly for a symmetric product.
74. **Pipelined centres:** centres copied in stage 1 and reused across replicas.
75. **Register-recycling word:** dirty helpers reused by two targets at disjoint frames (one register, two chains).
76. **Split-source word:** each source split into two half-sources with half-rank frames.
77. **Asymmetric source/target counts** (v_s ≠ v_t) with a rectangular decoder.
78. **Three-operand gates** (if the verifier's gate class admits them: a += b + c at one frame).
79. **Fused multiply-add gates** (coefficient ×2^k) to halve climbs.
80. **Lazy restoration word:** helpers never restored, priced as entrances at exit (idea 44 of the old list as a design).

## G. Hybrid / composite words

81. **Paired cube × projective plane** (cube for the pair step, plane for the all-but-one step).
82. **Cube with Steiner-triple faces** (faces replaced by STS(7) blocks).
83. **Two cube sizes in one word** (p=8 cubes for pairs, p=12 for triples).
84. **Cube + Hadamard centres** (Hadamard rows as centre spans).
85. **Cube over Z[i]** (architecture 46 with cube ports).
86. **Cube with Karatsuba pair modules** (61 with cube ports).
87. **Cube with inclusion–exclusion decoder** (21 with cube ports) — zero centres.
88. **Cube with half-star centres** (36 with cube ports).
89. **Cube, partner-free** (33 with cube ports).
90. **Cube with recursive targets** (35 with cube ports).

## H. Generated / searched architectures

91. **Evolved port hypergraph:** evolve the port set itself (not the design) under the deficit-per-port objective.
92. **SAT-generated decoder:** given a port set, SAT-solve for a decoder with minimal centre rank.
93. **LLM-proposed decoders:** propose decoder identities, verify mod 2, price (idea 64 as architecture search).
94. **Random linear decoders** over F_2 with the cap rule, 10,000 samples, keep the ones with D > 0.
95. **Dual of the paired cube** (swap roles of coordinates and ports).
96. **Minimum-ℓ port set:** search port sets of size v in Q^h minimising the centre lemma's bound h(h−2) — i.e. find
    port geometries where stars are NOT the minimum.
97. **Maximum-deficit port set:** maximise 4v − 5ℓ per coordinate over all hypergraphs with the intersection property.
98. **Port sets from strongly regular graphs** (adjacency = |S∩T| = 1).
99. **Port sets from finite geometries over F_3** (ternary cubes).
100. **Port sets from association schemes** (Johnson, Hamming): decoders from the scheme's eigenspaces.
