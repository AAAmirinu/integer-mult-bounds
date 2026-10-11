# E-module-sat: exact (CP-SAT) search for smaller pair / all-but-one modules (ideas 5, 37, 88)

Working dir: /tmp/radical/E-module-sat (scripts, modules, evals/*.json = physical_eval outputs).
Baseline reproduced first: #325 package, DESIGN none -> kappa = 7.69684e-4 (stock 658800, R 8100), 78 s.

## 1. Counts and lower bounds

| module | inputs | roots | additions |
|---|---|---|---|
| pm_p10.json (#325, annealed) | 36 | 37 (36 K_7 + centre K_9) | 273 |
| restricted_pairs(9) (generic PR117) | 36 | 36 | 273 |
| qmod_p10.json (#325, annealed) | 8 | 8 | 24 |
| all_but_one(8) (balanced tree) | 8 | 8 | 18 |
| nested_prefix(8) | 8 | 8 | 23 |
| prefix/suffix (3n-6) | 8 | 8 | 18 |
| all_but_one(10) / nested_prefix(10) / prefix-suffix(10) | 10 | 10 | 24 / 31 / 24 |

Trivial bounds: an unshared root of support size s needs s-1 additions (all-but-one: 8 x 6 = 48; pair: 36 x 20 = 720 + 35),
so all modules rely heavily on sharing; every root is a distinct node, so additions >= #roots (8 / 37).

**All-but-one exact minimum (CP-SAT, subset formulation + valid cuts, abo_sat2.py):** 3n-6 for every n tested:
n=4: 6, n=5: 9, n=6: 12, n=7: 15 (proved in 16 s), n=8: **18 proved optimal** (Daytona, 4 workers, 210 s).
So the balanced tree all_but_one(8) and the prefix/suffix module are both addition-optimal; qmod_p10 (24) is 6 above the minimum.
n=9 and n=10 (p=12) runs were still open at hand-off (7000 s limit; conjecture 21 and 24 = prefix/suffix; the LP bound
without the cuts is useless, the cuts "nodes avoiding input i >= n-2", the pair version, and the big-child covering cut are
what make n=7,8 provable).

**Pair module (n=9, 36 roots K_7 + K_9):** no exact answer (2^36 supports; a CP-SAT over explicit supports is infeasible and a
node/parent-selection model with K~250 nodes x 36 bits has ~3M clauses with no useful relaxation). What I have:
- Lower bound 99 additions from a counting LP (pair_lp in RESULT; each root tree with 21 leaves has >= ceil(21/(s-1))-1 nodes of
  >= s edges; a node spanning u vertices lies in at most C(9-u,2) roots) - weak.
- **New upper bound 244 additions** (pair_ag23.py, pm_ag23.json, contract-checked, 37 roots incl. the centre): AG(2,3) /
  Steiner-triple construction: K_7(V\{i,j}) = K_6(V\T) + star(v, V\T) with T the line through {i,j}, v = T\{i,j};
  K_6(V\T) = K_3(T') + K_3(T'') + sum_{v in T} Opp(v,T); Opp and the stars are all-but-one-of-4 gadgets per vertex
  (6 additions each); K_3(L) = pair-star + edge.  Only 12 K_6 nodes are needed because the 12 lines of AG(2,3) cover every pair.
  So 99 <= min <= 244, and 273 (PR117 / pm_p10) is not addition-minimal.

## 2. What kappa actually prices (why addition count is the wrong objective)

compile_word: R = donors + roots - arcs, ledger mass = h R + loss (verified: proxy R = physical R + 960 on every module).
An addition x = y + b gets a carrier arc when some other node t uses y (or b) with initial[t] contained in initial[x] and t later in
the order.  For the pair module the exact per-instance arc count equals the maximum matching donors -> operand uses with
**vertex-cover nesting** V(t) ⊇ V(x) (V = vertices spanned by the edge support, i.e. the covered coordinate pairs), equal covers
only to a later node index (vproxy.py / pair_proxy_anneal2.score(mod, False): pm_p10 181 = 3620/20, pm_ag23 52 = 1040/20,
pm_proxy78 172 = 3440/20, all exact).  For the qmod lane support nesting is exact (qmod_p10: 16 arcs = its provenance "arcs 16").

So the one-instance cost is **uncarried = additions - arcs** (plus the roots), not additions.  Structural facts for the pair module:
every root K_7(W) = C + D must have a child with full cover W (if both children missed a vertex the edge between the two missed
vertices would be in neither), and a 7-cover non-root node can only be carried by the K_9 chain, so uncarried >= ~36 roots + ~36
seven-cover children - O(K_9 chain) ~ 70.  pm_p10 has 92 (75 seven-cover nodes, 72 uncarried; only 16 of its 194 smaller nodes are
uncarried), i.e. it is already within ~20 of this structural floor.  qmod_p10 has uncarried = 8 = #roots, which is the floor
(no node of an all-but-one module can be carried from outside), so **qmod_p10 is optimal for the one-instance R objective**.

Order matters too: renumbering pm_p10's nodes with anneal_shape_lib.prune() alone costs 9 arcs/instance (92 -> 101) because the
compiler breaks equal-frame ties by node index.  Any module edit must keep a good topological order (stable_prune.py).

## 3. Physical prices (physical_eval.py, DESIGN none, 76-124 s each)

| module | adds | carried/inst | kappa | stock | R | delta vs baseline |
|---|---|---|---|---|---|---|
| baseline pm_p10 + qmod_p10 | 273 / 24 | 181 / 16 | **7.69684e-4** | 658800 | 8100 | 0 |
| pm_proxy92_272 (pm_p10 with one addition removed, same arcs) | 272 | 180 | 7.68741e-4 | 659490 | 8102 | -9.4e-7 |
| pm_generic restricted_pairs(9) (36 roots) | 273 | ~100 | 6.62635e-4 | 774000 | 10020 | -1.07e-4 |
| pm_ag23 (AG(2,3), 244 additions) | 244 | 52 | 6.63675e-4 | 780720 | 10100 | -1.06e-4 |
| pm_ag23_skew (262) | 262 | 70 | 6.60973e-4 | 780720 | 10100 | -1.09e-4 |
| pm_proxy78 (loose-proxy anneal, 295 adds) | 295 | 172 | 7.26693e-4 | 697275 | 8723 | -4.3e-5 |
| qmod balanced all_but_one(8) (addition-optimal) | 18 | 0 | 7.24624e-4 | 712800 | 9000 | -4.5e-5 |
| qmod prefix/suffix (addition-optimal) | 18 | 0 | 7.22866e-4 | 712800 | 9000 | -4.7e-5 |
| qmod nested_prefix(8) | 23 | 10 | 7.43488e-4 | 685800 | 8550 | -2.6e-5 |

Variation at FIXED addition count: 273 additions span 6.63e-4 .. 7.70e-4 (1.07e-4, i.e. ~170000 J-units); 18 additions span
7.229e-4 .. 7.246e-4 (same R, shape-only difference 1.8e-6).  The addition-minimal modules are all much worse than the annealed
ones; kappa is monotone in R (about 5e-8 kappa per register) and R is set by the carrier matching, not by the addition count.
The 244-addition module is the worst pair module measured.  Removing an addition at equal arcs (272) changed kappa by -9e-7.

## 4. Proxy anneal on the right objective

pa3.py: simulated annealing of the pair module on the exact proxy (uncarried, then additions) with the order-stable mutation,
~1000 candidates/s.  From pm_p10 it finds only neutral moves (92 uncarried with 272/271 additions); hotter schedules drift to
140-250 uncarried and never return (6 Daytona seeds + 4 local, 0.3-1.5M steps).  pm_p10 is a strict local optimum of the
one-instance objective under the mutate() neighbourhood - consistent with it having been physically annealed with the same moves.
A fully-carried all-but-one CP-SAT (abo_carry_sat.py, objective 1000*uncarried + nodes, with a no-dangling-node constraint) gives
n=5: 13 nodes/5 uncarried (optimal), n=6: 15/6, n=7: 21/7 (feasible, i.e. ~3n nodes for a fully-carried module vs 3n-6 for the addition minimum), n=8/10 unfinished at hand-off (sandboxes deleted); qmod_p10 (24 nodes, 8 uncarried) is at the
floor for n=8, so at most the node count could drop there, which section 3 shows is worth ~1e-6 at most.

## Verdict

Dead as stated (minimising additions): the exact minima are known (all-but-one 3n-6, proved to n=8; pair module 99 <= min <= 244
with a new explicit 244 construction), but every addition-minimal module is far worse physically (-4.5e-5 for the qmod, -1.06e-4 for
the pair module), because kappa prices R = additions + roots - carrier arcs, and the sharing that minimises additions destroys the
nested-cover reuse that the carrier matching needs.  The reusable outputs are the exact, millisecond per-instance proxy for the pair
module (vertex-cover nesting + index order; pair_proxy_anneal2.py), the structural floor (~70 uncarried vs pm_p10's 92, so at most
~22 x 20 = 440 registers ~ +2e-5 kappa remain in the pair module), the finding that node order alone is worth 9 arcs/instance,
and the fact that qmod_p10 is already optimal for its one-instance R.  Needs X: a search on the exact proxy with a richer move set
(whole-root re-decomposition keeping the 7-cover child structure) if anyone wants the remaining ~20 uncarried.

Files: pm_ag23.json (244), pm_ag23_skew.json (262), pm_generic.json, pm_proxy78.json, pm_proxy92_272.json, qmod_*_n8/n10.json,
abo_min_n{4..7}.json, abo_sat.py / abo_sat2.py (exact minimum), abo_carry_sat.py (carry objective), vproxy.py, arc_attrib.py
(per-instance arc attribution on the full compile), compile_stats.py (20 s R proxy), pa3.py + stable_prune.py (proxy anneal),
order_anneal.py, pair_ag23.py, dt_*.py (Daytona launch/poll; sandboxes deleted at hand-off).

Note: the package copy /tmp/radical/E-module-sat/pkg was removed to free /tmp; re-create it with
  cp -r /private/tmp/imbwork/w325/research/five-stage-p10b-banks /tmp/radical/E-module-sat/pkg
before rerunning compile_stats.py, arc_attrib.py or runq.sh.
