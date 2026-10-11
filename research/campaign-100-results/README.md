# 100 research ideas: results, failures and execution gaps

This publishes the available evidence from the October 10, 2026 research campaign and its October 11 continuation.
**The original list contains 100 ideas, not 100 completed tests.** The table below gives all 100 a status,
an outcome and evidence links. Several ideas share one experiment; counts below are idea classifications, not run counts.

The archive contains 16 original final reports, 1075 selected raw evidence files in lossless archives,
ten architecture-prototype result JSONs, decoder failure logs, and the later PR366 replay receipt.
Raw evidence includes per-run results, logs, model outputs and matching arrays; these are not independent test cases.

- [All 100 results as JSON](results.json) or [CSV](results.csv)
- [Original 100 ideas](plans/RADICAL-IDEAS.md)
- [Separate architecture-plan results and failures](prototype/README.md)
- [PR364 continuation, including unsuccessful searches](continuation/README.md)
- [Raw-file inventory with SHA-256 hashes](RAW-INVENTORY.json)
- [Original file provenance](PROVENANCE.json) and [attribution](NOTICE.md)

## How to read the evidence

Historical reports and raw outputs are archived, not re-executed in this publication. Their baseline is usually PR325,
sometimes PR337/342; their kappa values and complex caps must not be compared as if they used one common source.
The PR364 continuation was independently replayed. Its complete executable certificate is in [PR366](https://github.com/CrocSwap/integer-mult-bounds/pull/366).

`partial_gain` means a reported gain in the tested variant or proxy, not necessarily a complete or current record.
`bounded_no_gain` and `bounded_infeasible` apply only to the tested scope. `analysis_only` is a memo or what-if,
`partial_experiment` falls short of the stated proposal, `implemented` is a demonstrated tool, `blocked` is an explicit
execution blocker, and `not_evidenced` means no located execution result. None of these labels asserts global optimality.

Important corrections preserved alongside the failures:

- Report B prices hypothetical four-stage and merged-idle gains; report M later rejects those implementations in the fixed layout.
- Report O discards apparent 90/91-uncarried-node improvements caused by dangling nodes; the corrected searches remain at 92.
- Report D records 20 discrepant historical module labels and replaces them with fresh histogram data. Its original dataset is retained with that warning.
- J agrees with most sampled kappa rankings, but report D records nine disagreements; it is not an exact ranking oracle.
- Report N finds no centre-lemma counterexample at the searched sizes; its general proof is unfinished.
- Report P records a promising partially assembled candidate and the stop before final replay/publication; it is not an admitted record.
- Words such as "dead" or "optimal" in historical reports are the original authors' assessments; the scoped index below governs the archive summary.

## Status counts

| Status | Ideas |
|---|---:|
| analysis_only | 14 |
| blocked | 1 |
| bounded_infeasible | 3 |
| bounded_no_gain | 20 |
| implemented | 1 |
| not_evidenced | 40 |
| partial_experiment | 11 |
| partial_gain | 10 |

## All 100 ideas

| # | Idea | Status | Observed result and limits | Evidence |
|---:|---|---|---|---|
| 1 | Free-form word | partial_gain | Bounded frame retiming improved the tested word. Full gate/operand/coefficient synthesis was not run. Later combined with CP-SAT in PR366. | [G-RESULT](reports/G-RESULT.md), [README](continuation/README.md) |
| 2 | Exhaustive cube-local design | bounded_no_gain | All 11,471 node-minimal 24-node designs were priced in the reported finite class; no replacement beat the baseline. This is not an optimum over all words. | [L-RESULT](reports/L-RESULT.md) |
| 3 | Frame-lattice table | partial_gain | Depth-2 meet/join candidates and zero-cost drift helped; this was not a table of every rational subspace. | [G-RESULT](reports/G-RESULT.md) |
| 4 | Whole-word ILP | partial_gain | Bounded gate-frame CP-SAT models ran; the proposed months-long whole-word solve did not. PR366 extracted beneficial components from a time-limited FEASIBLE solve, without an optimality claim. | [H-RESULT](reports/H-RESULT.md), [README](continuation/README.md) |
| 5 | SAT-enumerate the pair module | bounded_no_gain | Addition-minimal modules priced worse. Corrected SA/LNS found no module below 92 uncarried nodes; apparent 90/91-node results were invalid dangling-node artifacts. | [E-RESULT](reports/E-RESULT.md), [O-RESULT](reports/O-RESULT.md) |
| 6 | Universal bank tiling table | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 7 | Exact constant search in the outer polytope | analysis_only | Related constant and margin what-ifs were priced, but no exhaustive exact outer-polytope search is evidenced. | [B-RESULT](reports/B-RESULT.md) |
| 8 | True root instead of certified root | bounded_no_gain | Independent high-precision moment root agreed with certification; rounding slack was about one 1e-18 tick on the tested baseline. | [B-RESULT](reports/B-RESULT.md) |
| 9 | Largest-ever complex supplier | blocked | The original largest-size complex-supplier experiment was blocked by unavailable recipe provenance. Later complex certificates do not establish this particular experiment ran. | [TRACKING-historical](reports/TRACKING-historical.md) |
| 10 | Joint enumeration of orientation × design × matching | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 11 | Lagrangian DP per register | partial_experiment | Compound/free-form frame moves were tested; a full Lagrangian register-path DP was not implemented in the surviving evidence. | [G-RESULT](reports/G-RESULT.md) |
| 12 | GPU exhaustive entrance census | bounded_no_gain | CPU read-span census added 5,496 rank-2/3/4 candidates and changed packing value by zero on tested seeds. No broad GPU search over arbitrary rank-3 to rank-8 subspaces. | [F-RESULT](reports/F-RESULT.md) |
| 13 | 10⁶ restart packings | partial_gain | About 16,000 packings, not one million. Best proxy improvement about 4.9 phi; kappa unchanged because that historical complex supplier capped it. | [K-RESULT](reports/K-RESULT.md) |
| 14 | Symmetry-reduced word | bounded_no_gain | The tested word had trivial effective automorphism structure after identical-record ambiguity; no symmetry compression gain. | [F-RESULT](reports/F-RESULT.md) |
| 15 | Hard-coded optimal small instance, then lift | partial_gain | p=6 gate-frame model solved optimally within its candidate set; p=5 had no positive price and larger solves were bounded/time-limited. No exact optimum over every legal small word or general lift. | [H-RESULT](reports/H-RESULT.md) |
| 16 | Map κ(p) | bounded_no_gain | Generic p=8 through 14 and restricted annealed modules were evaluated. None beat the then-current p=10 word; module quality confounds any claim about the optimal size. | [A-RESULT](reports/A-RESULT.md) |
| 17 | Mixed cube sizes | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 18 | k-stage layouts for k ≠ 5 | bounded_infeasible | Four-stage arithmetic what-ifs looked attractive but the proposed fixed-layout implementation was refuted by later finite geometry checks. A new architecture remains a separate question. | [B-RESULT](reports/B-RESULT.md), [M-RESULT](reports/M-RESULT.md) |
| 19 | Non-uniform stage widths | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 20 | Other Gram forms | bounded_no_gain | Selected symmetric I-J/s^2 port/centre families with s != 3 had negative deficit at tested sizes. Not an exclusion of all Gram forms. | [B-RESULT](reports/B-RESULT.md), [M-RESULT](reports/M-RESULT.md), [N-RESULT](reports/N-RESULT.md) |
| 21 | Other idle-rank sets | bounded_infeasible | Merged-idle pricing gains were hypothetical; finite checks refuted the proposed merge in the inherited fixed bridge layout. | [B-RESULT](reports/B-RESULT.md), [M-RESULT](reports/M-RESULT.md) |
| 22 | Frames over number fields | bounded_no_gain | Tested finite-field/number-field intermediate-frame analyses yielded no additional usable nondegenerate frames; broader field constructions remain untested. | [F-RESULT](reports/F-RESULT.md) |
| 23 | Non-nested chains | analysis_only | Feasibility memo for non-nested chains; no admitted replacement word or stronger bound. | [M-RESULT](reports/M-RESULT.md) |
| 24 | Asymmetric words | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 25 | Different centre design | bounded_no_gain | Point-star copied spans have rank h-2 and tested splits cost more. Lower total centre mass needs a different decoder. | [J-RESULT](reports/J-RESULT.md), [N-RESULT](reports/N-RESULT.md) |
| 26 | Smaller ℓ = h(h−2) | bounded_no_gain | No smaller-centre counterexample found at p=5,6,7; exact statements apply only to specified subfamilies. The general lemma remains unproved. | [M-RESULT](reports/M-RESULT.md), [N-RESULT](reports/N-RESULT.md) |
| 27 | Two-level word | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 28 | Deeper outer chain | analysis_only | Deeper outer-chain arithmetic approaches a fixed point; reported possible gain roughly 3.3e-13, without a new assembled certificate. | [B-RESULT](reports/B-RESULT.md), [M-RESULT](reports/M-RESULT.md) |
| 29 | Make the complex side bind on purpose | analysis_only | Supplier-cap sensitivity was priced. Raising a bit root above a cap does not itself improve the capped kappa. | [B-RESULT](reports/B-RESULT.md) |
| 30 | Lazy banks | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 31 | Superoptimised word | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 32 | Toom-Cook word | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 33 | Karatsuba-tree pairing | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 34 | Expander matchings | bounded_no_gain | Spectral matching heuristics were uninformative in the tested graph; 202 physical evaluations across matching variants are reported. | [I-RESULT](reports/I-RESULT.md) |
| 35 | Cayley-graph indexing | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 36 | Character frames | bounded_no_gain | Character-aligned frames encountered the tested parity obstruction; no new frame construction. | [F-RESULT](reports/F-RESULT.md) |
| 37 | Tensor-rank modules | partial_experiment | Related module synthesis tested smaller addition programs and lost physically. No full border-rank/Strassen architecture was established. | [E-RESULT](reports/E-RESULT.md), [O-RESULT](reports/O-RESULT.md) |
| 38 | Signed-digit coefficients | bounded_no_gain | The removable coefficient-3 operations occur at rank zero; the proposed rewrite gives no paid-climb improvement. | [J-RESULT](reports/J-RESULT.md) |
| 39 | Wallace/Dadda accumulation | bounded_no_gain | Arithmetic reassociation under the tested lifetime/frame rules preserves the priced climb census; no Wallace/Dadda replacement certificate. | [J-RESULT](reports/J-RESULT.md) |
| 40 | Random legal words + repair | partial_experiment | Random matching variants were tested; a sampler over general legal words with repair was not run. | [I-RESULT](reports/I-RESULT.md) |
| 41 | Transposed word | bounded_no_gain | Transposition gave the same priced histogram for the tested word. | [F-RESULT](reports/F-RESULT.md) |
| 42 | MDS-code cover vectors | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 43 | LLL-reduced covers | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 44 | Steiner-system pairing | bounded_no_gain | No-duplicate carrier restrictions lost roughly 6 to 10 percent; this screens a restricted analogue, not every Steiner-system construction. | [I-RESULT](reports/I-RESULT.md) |
| 45 | Triple (hypergraph) module | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 46 | Exact large-deviation root | analysis_only | For the fixed recurrence, the moment root is its characteristic exponent; no separate improved large-deviation certificate was built. | [B-RESULT](reports/B-RESULT.md), [M-RESULT](reports/M-RESULT.md) |
| 47 | SDP relaxation of the histogram price | analysis_only | Certificate analysis found no fixed-histogram slack; no new SDP solver experiment or admitted SDP certificate. | [B-RESULT](reports/B-RESULT.md), [M-RESULT](reports/M-RESULT.md) |
| 48 | Exact 10⁻¹⁸ grid accounting | bounded_no_gain | Exact grid what-ifs recover about 1e-18; the adjacent baseline root tick fails the strict inequality. | [B-RESULT](reports/B-RESULT.md) |
| 49 | Different concave price | analysis_only | No proved completion with a cheaper rank price was supplied. | [M-RESULT](reports/M-RESULT.md) |
| 50 | True entrance-stock price | analysis_only | Memo found no admitted improvement from repricing entrance stock. | [M-RESULT](reports/M-RESULT.md) |
| 51 | Fewer replicas | bounded_no_gain | Replica what-ifs leave the moment root invariant when the bank arithmetic is legal; finite resource counts still change. | [B-RESULT](reports/B-RESULT.md) |
| 52 | No fallback class | analysis_only | Dropping the fallback costs would give about 3e-12 in arithmetic; removal was not proved or assembled. | [B-RESULT](reports/B-RESULT.md), [M-RESULT](reports/M-RESULT.md) |
| 53 | Lean the whole bound | analysis_only | Feasibility memo only; the whole bound was not formalized in Lean. | [M-RESULT](reports/M-RESULT.md) |
| 54 | Smaller η, β | analysis_only | Margin what-ifs give tiny changes (about 2.3e-15 at the zero-margin limit); zero margins are not admissible. | [B-RESULT](reports/B-RESULT.md) |
| 55 | Optimise exact κ, not J | partial_gain | J and exact kappa disagree on 9 of 287,669 sampled comparisons. Exact comparison code was developed; PR366 used rational component selection. | [D-RESULT](reports/D-RESULT.md), [README](continuation/README.md) |
| 56 | Mod-3 parity fusion | bounded_infeasible | The tested mod-3 decoder identity fails; removable additions are rank-zero and would not improve the paid histogram anyway. | [J-RESULT](reports/J-RESULT.md) |
| 57 | Information-theoretic register price | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 58 | Alternative independence control | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 59 | Nested temporaries | analysis_only | Nested temporary lifetimes are already allowed within the stated limits; no improved constructed word. | [M-RESULT](reports/M-RESULT.md) |
| 60 | Gate frames below operand spans | analysis_only | Frames below required source spans need a new mathematical lemma; no valid relaxation or witness. | [M-RESULT](reports/M-RESULT.md) |
| 61 | GNN surrogate of physical κ | partial_experiment | Ridge, boosted regression and MLP surrogates were evaluated, not a GNN. Coarse rankings help, fine rankings and module features fail; 20 historical module labels disagreed on replay. | [D-RESULT](reports/D-RESULT.md) |
| 62 | AlphaDev-style reinforcement learning | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 63 | Evolutionary search with crossover | partial_gain | 1,695 evaluations across population methods found plane-order gains on the old baseline; crossover added no benefit beyond that plateau, and gains did not simply compose through later stages. | [C-RESULT](reports/C-RESULT.md), [P-RESULT](reports/P-RESULT.md) |
| 64 | LLM program synthesis | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 65 | MCTS | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 66 | Large-neighbourhood search | partial_experiment | CP-SAT LNS was run on module roots/supports, not the proposed sliding windows of about 1,000 word gates. No corrected module gain. | [O-RESULT](reports/O-RESULT.md) |
| 67 | Tabu search | bounded_no_gain | Tested packing tabu moves did not improve their starting seeds. | [K-RESULT](reports/K-RESULT.md) |
| 68 | QUBO on a quantum annealer | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 69 | Bayesian optimisation | partial_gain | Bayesian knob search found a small PLAIN=12 gain on the old source; it lost on the later oriented source. | [C-RESULT](reports/C-RESULT.md), [P-RESULT](reports/P-RESULT.md) |
| 70 | Differentiable frames | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 71 | Learned restart distributions | bounded_no_gain | Learned restart distributions matched the plain-restart plateau; no superior verified kappa. | [K-RESULT](reports/K-RESULT.md) |
| 72 | Cross-size transfer | partial_experiment | Coordinate restrictions transferred modules across sizes; the proposed learned embedding was not trained. | [A-RESULT](reports/A-RESULT.md) |
| 73 | Quality-diversity (MAP-Elites) | partial_gain | MAP-Elites reached the plane-order gain but did not improve the shared plateau; no distinct methodology advantage established. | [C-RESULT](reports/C-RESULT.md) |
| 74 | Cross-entropy method | partial_gain | Matching/search variants include a reproducible min-cost matching gain of about 0.0082 percent on the old baseline; not evidence that the exact proposed cross-entropy method succeeded. | [C-RESULT](reports/C-RESULT.md), [I-RESULT](reports/I-RESULT.md) |
| 75 | 10,000-sandbox population search | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 76 | NTT complex supplier | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 77 | Gaussian / Eisenstein integer bit words | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 78 | p-adic / Hensel coefficient structure | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 79 | Group-algebra word | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 80 | Quaternion packing | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 81 | Cyclotomic frames | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 82 | Montgomery/Barrett reduction | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 83 | Winograd minimal-multiplication filters | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 84 | Rader/Bluestein structure | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 85 | Good–Thomas indexing | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 86 | Clifford-algebra frames | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 87 | Mixed-radix cubes | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 88 | Known-optimal small bilinear algorithms | partial_experiment | Related small-module synthesis was priced, but the named optimal bilinear algorithms were not installed as a full word. | [E-RESULT](reports/E-RESULT.md) |
| 89 | verify.py in C++/Rust | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 90 | GPU/FPGA exact replay | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 91 | Incremental κ evaluator | implemented | Incremental histogram pricing and exact comparison implemented; the expensive missing link is a fast design-to-histogram map. | [D-RESULT](reports/D-RESULT.md) |
| 92 | Word compiler | partial_experiment | Generic word-compiler prototype produced ten surviving result JSONs. Two fail pricing; new architectures lack a full admitted source-bound certificate. | [README](prototype/README.md) |
| 93 | Public dataset of every word and κ | partial_experiment | A local dataset existed and is now archived with its label-noise caveat. This is not a dataset of every fully verified word. | [D-RESULT](reports/D-RESULT.md), [RAW-INVENTORY](RAW-INVENTORY.json) |
| 94 | Pin-free development mode | partial_experiment | Record-mode/unpinned discovery runs are documented. No standalone general pin-free development product was validated. | [F-RESULT](reports/F-RESULT.md), [P-RESULT](reports/P-RESULT.md) |
| 95 | Composable stage library | partial_experiment | Stage-composition tooling ran and exposed non-additive gains; a candidate build was stopped before final packaging and verification. | [P-RESULT](reports/P-RESULT.md) |
| 96 | Community compute pool | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 97 | Re-derive the inherited analytic theorem | analysis_only | Machine-model feasibility memo only; no re-derived stronger analytic theorem. | [M-RESULT](reports/M-RESULT.md) |
| 98 | Three suppliers | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 99 | Prove the limit κ(p → ∞) | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |
| 100 | Replace the finite word by an infinite family certified by a parametric Lean proof | not_evidenced | No execution result located in the archived campaign evidence; do not count this proposal as a completed test. | No located result |

## Reuse and verification

Run `python3 research/campaign-100-results/validate_archive.py` from the repository root.
It checks unique idea IDs 1–100, status totals, evidence paths, provenance hashes, every archived raw member,
and the complete file manifest. It does not prove the archived mathematical claims.

The raw archives preserve selected surviving result files byte-for-byte. Large generated words, full dependency trees,
remote sandbox disks and every intermediate file referenced by historical reports are not included.
A report pointing to an absent old path is not a claim that the path is reproducible from this archive alone.
No new remote compute, mathematical theorem, or complete architecture certificate is claimed by this publication.
