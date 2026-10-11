# O-pair-module: structural search on the uncarried-node objective of the pair module

Working dir: /tmp/radical/O (proxy.py = exact per-instance proxy with breakdown; ols.py = SA with structural moves;
lns.py = CP-SAT large-neighbourhood search; exact_inst.py = per-instance check of the proxy in the real p=10 geometry;
evals/*.json = physical_eval outputs; dt/ = Daytona job lists / registries / downloaded bests; pkg = copy of #325).

## 1. Proxy re-derived and validated (task 1)

proxy.py re-implements E's rule independently: donor x=[y,b] is carried by a use (t,y) or (t,b), t != x, iff the vertex
cover V(t) contains V(x) (equal covers only if t comes later in the node order); uncarried = additions - maximum matching.
Physical R of a 37-root module = 5520 + 20 * (additions + 37 - arcs/instance) (5520 = everything outside the 20 pair
instances; one module node = 20 registers).

| module | adds | arcs/inst (proxy) | uncarried | R predicted | R physical | kappa physical |
|---|---|---|---|---|---|---|
| pm_p10 (#325 baseline, re-run) | 273 | 181 | 92 | 8100 | 8100 | **7.69684e-4** (reproduced) |
| pm_rand (pm_p10 + 40 random mutate_stable moves, new) | 289 | 162 | 127 | 8800 | 8800 | 7.24949e-4 (-4.47e-5) |
| pm_ag23 (E) | 244 | 52 | 192 | 10100 | 10100 | 6.63675e-4 (-1.06e-4) |
| pm_proxy78 (E) | 295 | 172 | 123 | 8720 | 8723 (3 dropped) | 7.26693e-4 |
| pm_proxy92_272 (E) | 272 | 180 | 92 | 8100 | 8102 (2 dropped) | 7.68741e-4 |
| LNS output fix_test_4 (277 adds), exact_inst.py | 277 | 183 | 94 | 8140 | 8140 (full compile R 9100 = phys + 960) | (not priced) |

exact_inst.py recomputes compile_word's own rule (initial frames in Q^20, order by frame rank then index, root uses) for
pair instance 0 and compares adjacency lists: for pm_p10 and for an LNS output the two adjacency lists are identical,
no module donor has an external or root carrier, and every one of the 20 instances gets exactly the proxy's arc count.
Slope: -4.47e-5 for +700 registers (pm_rand) and -1.06e-4 for +2000 (pm_ag23): 5.3-6.4e-8 kappa per register, i.e.
about 1.1-1.3e-6 kappa per uncarried module node (20 registers).  (pm_generic, 36 roots, is priced differently by the
producer: it adds the centre sums itself, R 10020 vs 9760 predicted; the 37-root formula is exact on every 37-root module.)

Caveat found on the way: a module node that is unreachable from the roots is still an addition in the compiled word; a
"carried dangling node" is free in the proxy only if dangling nodes are allowed (they are not: physical R of such a
module, start90.json, was 8140 = that of the module with the dangling nodes counted as uncarried).  All search code below
forbids dangling nodes.

## 2. Floor (task 2)

Exact CP-SAT over all DAGs is infeasible (2^36 supports), so the floor is split: nodes of cover >= 7 and nodes of cover <= 6.

**Cover >= 7 part: uncarried >= 71 (proof, per root family + the K_9 tree).**  Facts used: under each root the reachable
nodes form a tree (disjoint supports), so a node has one parent per tree; a node of cover W (|W| = 7) lies only in the
W-tree and/or the K_9 tree; a node of cover >= 8 lies only in the K_9 tree; a carrier of x via operand y is another user
t of y with V(t) >= V(x).
- A = K_9-tree nodes of cover >= 8: all uncarried (any carrier would be a second K_9-parent of their operand), they form
  a connected subtree containing the root, so exactly a+1 of their 2a uses point to non-A children, and only those uses
  can carry anything (a use pointing to an A child carries nothing).  Each such use carries one node.
- Per root W let C_W = W-cover nodes of the W-tree (>= 2: the root and the child that must have full cover W, since if
  both children missed a vertex the edge between the missed vertices would be in neither).  A C_W node can be carried
  only by a K_9-tree node of cover >= W (A, or B_W = K_9-tree nodes of cover exactly W outside the W-tree); the root
  r_W itself cannot be carried by a B_W node that is carried (that node would have to come after r_W and before a W-tree
  node).  Each non-A subtree of the K_9 tree (a+1 of them) is of cover <= one W and helps that single W by at most 1:
  either through its A-use (carrying one W-tree node) or through B-nodes (a B node that carries two C_W nodes is
  itself uncarried; a B node carried by a C_W node carries at most one; and if the subtree top is in the W-tree the
  whole subtree is shared and contains no B node).  Hence u_W >= 2 - (subtrees assigned to W), sum over W >= 72 - (a+1),
  and uncarried_{>=7} >= a + 72 - (a+1) = 71.
- pm_p10: a = 4 (three 9-cover + one 8-cover K_9 nodes), 75 seven-cover nodes (two roots have chains of 4 and 3
  W-cover nodes instead of 2), 72 of them uncarried, 2 of the 5 A-uses carry small nodes: 76 = 71 + 2 (wasted A-uses)
  + 3 (extra chain nodes).
**Cover <= 6 part:** no non-trivial lower bound; pm_p10 has 16 uncarried small nodes (each is the largest-cover user
of both of its operands).  So the floor is 71 and pm_p10 is 21 above it: 5 in the K_9/chain structure, 16 small nodes.

## 3. Search (task 3)

### 3a. Simulated annealing with structural moves (ols.py), 15 Daytona sandboxes x 12 min + local
Moves: node re-decomposition into existing halves (E's mutate), carrier-targeted re-decomposition (make an uncarried
node's operand the operand of a larger-cover node, or rewire a larger-cover node onto it), whole-subtree rebuild of a
root / 7-cover node from existing parts (greedy largest-first cover + random merge tree), and order moves (move a node
to any other valid topological position).  Exact proxy at ~1500 candidates/s.  15 sandboxes (t0 0.08-0.3, four move
mixes), 460k-710k steps each: best 92 everywhere (plateau walks at 92 with 271-283 additions; hotter schedules drift
to 95-119 and never return).  pm_p10 is a strict local optimum for this move set too.

### 3b. CP-SAT large-neighbourhood search (lns.py)
Round: choose k roots F (random, or targeted: the owners of a random uncarried node plus the owners of the other
users of its operands); nodes reachable from F are variable (those also reachable from other roots must keep their
support if a fixed node uses them, but may be re-decomposed or dropped), the rest fixed; candidate pool = all existing
supports + (differences of existing nodes inside the freed roots) + (closure by random unions / differences, up to
max_new = 300-1200) + single-edge removals.  Exact model: exists / decomposition Booleans, global integer positions
(topological order, equal-cover arcs need carrier after donor), carrier matching Booleans (each donor <= 1, each use
<= 1), no dangling nodes, roots forced; objective = uncarried.  Model value == exact proxy on every extracted module.
Per round: 400-700 variable supports, 700-1500 decompositions, 3k-7k arc Booleans; k <= 8 rounds mostly solve to
proven optimality in 1-60 s, k >= 10 hit the time limit (LP bound useless, 40-70).
25 Daytona sandboxes (k = 5..20, solve limit 20-180 s, max_new 300-1200, centre root probability 0-1, targeted
probability 0-1), 5000 s each, plus local runs: **no round improved on 92** (several hundred rounds, >100 of them
proven optimal within their neighbourhood).  An earlier batch reported 91/90 but those modules contained dangling
nodes (bug: pinned nodes were forced to exist without a user; fixed, batch discarded, physical price of the dangling
90-module = that of 94).

### 3c. Exact solves with every root free (local, 2 workers)
- all 37 roots free, pool = pm_p10's own 273 supports + 80 single-edge removals (353 variable supports, only 487
  decompositions: the support set admits almost no alternative splits): best 92 after 900 s, bound 53.
- all roots free, pool + 1580 generated supports (1853 variable supports, 2643 decompositions, 14940 arc Booleans):
  best 92 (a different DAG: 274 additions, 182 arcs) after 1800 s, bound useless.

### 3d. Totals and physical prices
3353 LNS rounds on 35 sandboxes (25 + 10 with carrier-difference candidates; 46 rounds proven optimal within their neighbourhood, the rest time-limited) + ~60 local rounds + 2 all-free solves + one 900 s round targeted at the K_9 tree and the two long chains (F = centre + 7 roots, 1375 variable supports, 25k arc Booleans: 92),
plus 15 x 12 min of SA: nothing below 92.  Best modules found are 92-uncarried variants of pm_p10 with fewer additions;
physical prices (DESIGN none, --pair):

| module | adds | arcs | uncarried | R | kappa | vs 7.69684e-4 |
|---|---|---|---|---|---|---|
| pm_p10 (baseline) | 273 | 181 | 92 | 8100 | 7.69684e-4 | 0 |
| pm92_271.json (LNS, 271 adds) | 271 | 179 | 92 | 8100 | 7.69625e-4 | -5.9e-8 (-0.008%) |
| pm92_272b.json (LNS sandbox lnsc05, 272 adds) | 272 | 180 | 92 | 8100 | 7.69544e-4 | -1.4e-7 (-0.018%) |
| start90.json (buggy LNS, 5 dangling nodes, 277 adds) | 277 | 183 real | 94 real | 8140 | 7.67066e-4 | -2.6e-6 |

At equal R the remaining variation is the climb-rank shape (~1e-7).  So the one-instance objective R is the right
first-order target (1.1-1.3e-6 per uncarried node), but no module with fewer than 92 uncarried nodes was found, and
pm_p10 remains the best module physically.  pm_best.json = pm_p10 (unchanged); the 92-variants are in
/tmp/radical/O/pm92_271.json and pm92_272b.json (both contract-checked, both priced, both slightly worse).

### 4. All-but-one module
E's floor claim re-checked: in an all-but-one module a root cannot be carried (a carrier would need support containing
the root's, and the only such node, the full sum, does not exist in the module; the merged nodes u = Pm + Qm of the
producer use the root itself, not its operands), so uncarried >= #roots = 8; qmod_p10 has 24 additions, 16 arcs,
8 uncarried = the floor.  Nothing to do (task 4 skipped as instructed).

## Verdict

Needs X / effectively dead for this lever.  The objective is confirmed (exact per-instance proxy, validated
against compile_word's frame rule and against four physical prices; 20 registers = 1.1-1.3e-6 kappa per uncarried
module node) and the floor is sharpened to 71 for the cover>=7 part (proof above; pm_p10 is at 76 there, 71 + 2 wasted
K_9-tree uses + 3 extra chain nodes) with 16 uncarried small nodes on top, i.e. at most ~21 x 20 = 420 registers
(~+2.3e-5) in principle.  But pm_p10 is a strict local optimum for everything tried: SA with re-decomposition,
carrier-targeted, subtree-rebuild and order moves (15 x 12 min, 0.5-0.7M steps each), ~3000 CP-SAT neighbourhood
solves over 5-20 roots with 400-1900 candidate supports (including neighbourhoods built around each uncarried node and
its potential carriers), and two all-roots-free exact models (92 after 900 s / 1800 s, bounds non-informative).  The
two physically priced alternatives at 92 are 0.6-1.4e-7 worse (shape).  What could still work: (i) an exact model
with a principled candidate pool (all subsets of K_7(W) that are unions of at most 3 existing nodes, or a column
generation over per-root trees with the K_9 tree enumerated separately: the floor proof shows the K_9 tree's a+1
subtrees are the only lever for the 7-cover part), or (ii) a constructive design that realises 71 + few small nodes
directly (K_9 tree whose a+1 non-A subtrees are each the d_W child of a root chain, every small node a non-top user
of one operand) and then physically annealing it; both are multi-hour efforts, and the prize is <= 2.3e-5 with the
first ~1e-6 requiring a strictly better DAG than the annealed one, which 3000 exact neighbourhood solves did not find.

Files: proxy.py (exact proxy + breakdown + R prediction), ols.py (SA), lns.py (CP-SAT LNS; args START OUT seed seconds
k solve_s max_new centre_prob workers target_prob), allfree.py (all-roots-free solve), exact_inst.py (real-geometry
check), mkrand.py, pm_rand.json, pm92_271.json, pm92_272b.json, pm_best.json (= pm_p10), evals/, dt/ (jobs, registries,
downloaded bests, launch logs), dt_launch.py / dt_poll.py / dt_rounds.py / dt_delete.py.  All sandboxes deleted at
hand-off.  Note the dangling-node pitfall for anyone reusing E's proxy in an optimiser: unreachable module nodes are
still additions in the compiled word.
