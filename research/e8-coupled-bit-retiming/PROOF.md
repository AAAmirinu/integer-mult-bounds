# Construction, finite checks and conditional scope

This supplement is a finite conditional argument, not an all-size theorem audit.
Exact upstream inputs and licenses are bound in `SOURCE-PINS.json`; all package
bytes are bound in `MANIFEST.json`. Scientific source files are never patched.

## The bit word

Start with Dylan Crow's E8 word (PR #370, h=8, v=120). Replay PR #376's 128
scalar frame changes and 43 helper reuse decisions, including its six witness
mutation controls. This gives R=822. On this word, move connected scalar-gate
groups to their common lowest or highest legal frame. Every outside preceding
frame is contained in the candidate, and the candidate is contained in every
outside following frame. Shared-role occurrences must be consecutive. Fixed
data operations and scatter pins cannot move. The search preserves the scalar
sequence and endpoints. `generate.py` deterministically reproduces the final
word, and `audit_cost.py` compares all non-frame fields exactly.

The local positive-rank child histogram changes by

```
rank          1    2    3    4    5    7
count delta +70  -28  -28  -42  +28  +14
```

Rank mass is unchanged; the number of children increases by 14. Consequently
we do not claim a cost improvement for every exponent between zero and one.
For e=1-p in [1/10000,1/500], set
`A=sum(delta[r]*r*log(r))` and `B=sum(abs(delta[r])*r*log(r)^2)`.
Since the second derivative of `r*exp(-e*log(r))` is at most `r*log(r)^2`,

```
delta cost <= -e*A + e^2*B/2
           <= -(1/10000)*(A-B/1000).
```

The unchanged rational logarithm engine bounds A below and B above. Its strict
decrease exceeds the extra `10^-16 * 32 * 56^2 * 14` fallback charge. The
chosen bit root and the fair unchanged-word root lie in this exponent interval.
All unchanged copy and idle charges cancel. Floating scores certify nothing.

Independent F2 word replay, native legality, full dirty basis columns, exact
Gram/projector checks and omitted-operation mutation tests verify physical
legality separately from this cost comparison. Native `columns_h` and
`columns_k2` receipts must match after removing their elapsed-time field; the
seven-stage checker also replays all 1,542 columns and rejects all 12 omitted
bridge controls. The frozen PR #375 suite replays its p=10 and earlier E8
regressions before these new checks.

## Unsplit B3 and common finite envelope

Use PR #381's generalized unsplit route, moment and finite-bill checkers at
K=3, h=8, T=7. The idle climbs are whole projector gaps, verified on all 120
ports; helper entrances are all zero. The largest child has rank 34 in m=56.
The least halving degree is two: `56^2=3136 > 2*34^2=2312`.
Its row reserve is `2*(56^2+1)=6274 < 20161`. This uses the previously supplied
degree-two recursion interface, not the split half-shrink interface.

The native column receipts supply the actual addition count and forward/inverse
cancellation-free row bounds. Every one of the 120 rational port route
programs is factored and replayed, with dyadic denominators valid over odd
prime fields; omitted factors are rejected. The regenerated finite invoice
has coefficient `56346946940397 < 2^80`, power bound `q^3137`, stock 10794,
and deficit 1512. Both independent moment engines include the fallback charge
and reject the adjacent `10^-18` coarse-saving tick.

The complex baseline is the **complete** pinned PR #377 package. Its original
verifier runs all eight stages, including 1,023 dirty columns, Clifford-frame
recipes and the finite invoice. Its complex coarse saving is
`999240641319551/10^18`; m=73, live=14727, physical=15520, deficit=2496,
halving degree two and restored-row coefficient 15445<20161. The fresh bit
envelope fits these dimension, stock, deficit and row ceilings. Following the
source-bound composition in PR #380, both suppliers retain G=2^30000,
E=2^100000, C0=2^210000, the common 20161 row coefficient and the same balanced
outer assembly engine. The verifier compares those exact fields and the
engine bytes. These interfaces remain mathematical hypotheses as in the
supplier notes, even after finite receipts pass.

The actual selected complex unit is Chafik Boukhalfa's PR #384 far-retimed
certificate, with coarse saving `999632926176283/10^18`. Following the exact
derivation procedure in Rohan Arun's PR #385, `complex_replay.py` creates a
separate work tree, updates the certificate and its reviewed census/bill pins,
changes the local child census from 3974 to 3973 and changes the expected
coarse-price assertion. A before/after digest records every such change.
No checker algorithm or control is removed. The new unit passes Sussman's
reference and mirror checks, flipped-sign rejection, source-span checks and
the complete rational operator comparison on all 1023 registers. Fresh dirty
scalar words, lifetimes, exact Clifford recipes, data/cover phases, global
template, finite invoice and independent two-engine template audit then pass.
The global profile delta is `{1:144,2:144,3:432,4:-1512,6:720}`; paid calls
decrease by 72, and the rank mass, dimensions and finite-envelope ceilings
remain unchanged. This supplies the finite certificate-specific checks which
PR #384 explicitly left open; it does not discharge PR #377's general
compressed-window or analytic hypotheses.

## Exact assembly refinement

Apply PR #376's eta=10^-24, eight bootstrap steps and 10^-27 grid, with
PR #387's smaller positive beta=10^-18, to the new complex saving b.
The retained outer interface permits every strict 0<beta<1; this changes its
witness backoff, not the supplier or finite-envelope hypotheses. Select the bit saving strictly below
`(1-beta)*b` and within two grid ticks of it, and recertify it with both moment
engines on the actual histogram. For each bootstrap step, compute all four
positive gaps and a fresh eventual cutoff at the **new finite coefficient**:

```
L >= 36/delta^2
L*delta >= 2*(4+ceil(log2(coefficient))).
```

The 47 exact outer slacks and seven margins are positive. The next 10^-27
assembly tick fails; admission at the complex leaf cap fails as well. This
produces the rational kappa in `data/EXPECTED.json`, larger than PR #387's
3-bootstrap / eta=10^-18 / 10^-18-grid witness. Zero eta, zero beta and unit
beta are additional rejected controls. The larger kappa comes from
this assembly refinement. The unchanged PR #376 bit word reaches the same
complex cap under the same new layout and parameters; the verifier explicitly
checks that its final kappa equals the new bit word's, and separately records
the latter's strictly better bit coarse saving.

## What finite replay leaves open

The upstream general all-size affine/compiler and chart interfaces, recursive
rank-cost realization, compressed correlated banks/Clifford windows, fixed
tapes, precision and recovery, uniform routing, restored-row and analytic
transfer remain assumed. There is no new general theorem or Lean proof.
`q^3137` is the bit invoice's power bound, not the global asymptotic exponent.
The headline comparison is a dated comparison with a pinned public witness;
it does not assert global novelty or maintainer acceptance.
