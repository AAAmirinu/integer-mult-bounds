# Exact envelope refinement of the reviewed gen4 checkpoint

The same conditional gen4 physical construction admits the rational witness

```
kappa = 361785796939503063587 / 500000000000000000000000
      = 0.000723571593879006127174.
```

This improves the reviewed PR279 value `0.000723571590007464` by exactly
`1935771063587/500000000000000000000000`, about `3.87e-12` in kappa
(`0.00000053506%`). The gain is small. It refines arithmetic envelopes and
finite composition, with the scalar word, frames, banks, physical stock,
prime threshold and complex supplier unchanged. It is not a practical
runtime claim or a claim to exceed stronger concurrent submissions.

The contribution keeps the public reviewed selection unchanged. It is a
new candidate for review, based on main at
`12a4934d15006e8c10f9b2264f13f8f341be802b`. For comparison, PR369 at
`4f5466fbde2ff11d4ce75b359568e4ed3bc3a3cf` claims approximately
`0.0008049429571461736`; that different construction was not reproduced here.

## What changes mathematically

The retained fallback proof already derives `346314` recursive children,
then rounds up to `460800`. The proof also bounds the bad-class fraction
using primes greater than `2^80`, then rounds up to `10^-16`. This package
retains the unrounded fallback, sharpens the explicit invertibility
conditioning, and accounts for mutually exclusive good and bad branches.
Every bad class still pays the complete fallback. The resulting two power
moments justify the same inductive majorant; the synthetic mixture is not
claimed to bound an arbitrary recurrence componentwise.

The final witness uses seven fixed ordinary-leaf levels, positive outer
backoff `eta=10^-24`, and `beta=10^-9`. All 47 strict outer constraints and
seven margins pass. Both independent rational interval engines accept the
coarse saving and reject the adjacent coarse grid point. The adjacent
headline point fails the binding outer inequality. The recipe coefficient,
all `502915820400` bank selector calls, and the external complex row reserve
remain charged. Implementation constants remain quantified finite constants,
as in the inherited proof; no numerical bound on all machine constants is
claimed.

Read [PROOF.md](PROOF.md) for the argument, assumptions and finite cutoff
quantifiers, and [NOTICE.md](NOTICE.md) for attribution and AI assistance.

## Reproduce

Python 3.11 or newer and the inherited pinned dependency are required:

```sh
python -m pip install -r research/five-stage-gen4-banks/requirements.txt
python -B -m unittest discover -s tests -p test_gen4_envelope_refinement.py -v
python -B research/gen4-envelope-refinement/verify.py --output /new/output/directory
```

The default verifier freshly executes every mandatory stage of the
unchanged gen4 package, compares its full certificate and finite bill with
the pinned baseline, then regenerates the refined arithmetic. The output
directory must be new and outside both source packages. Assertions must
remain enabled. The launcher selects UTF-8 for the inherited verifier and
its children, including on Windows. The equivalent Make target is
`make gen4-envelope-verify`.

For a quick arithmetic-only check that explicitly reuses pinned historical
physical evidence:

```sh
python -B research/gen4-envelope-refinement/verify.py \
  --arithmetic-only --output /new/arithmetic/directory
```

This mode checks all original package file hashes, both exact moment
engines, finite composition, constraints and adverse cases. Its execution
receipt says `physical_replay_fresh: false`. It does not claim a fresh
physical replay.

`EXPECTED.json` contains the complete deterministic certificate, all 55
trials, rejected trials, source hashes and interval endpoints. `SUMMARY.json`
is a separately labelled bounded index with the full certificate's SHA-256;
large integer parameters are strings. Both are regenerated and compared by
the verifier. Search decimals only propose endpoints; every accepted sign
is checked using rational interval arithmetic.

## Eleven improvement cycles

The first strict improvement triggers ten further bounded searches. A cycle
is a tested hypothesis, not a claim that every trial succeeds. All trial
parameters and their exact outcomes remain in the full certificate.

| Cycle | Question | Outcome |
| --- | --- | --- |
| 1 | Reduce positive outer backoff at three fixed leaf levels | Strict improvement |
| 2 | Search finite depths 4, 5, 6 and 8 | Strict improvement; ties retained |
| 3 | Search smaller positive backoffs | Strict improvement |
| 4 | Does the complex-leaf allocation beta bind? | No gain; two infeasible trials rejected |
| 5 | Refine coarse and headline grids to `10^-24` | Strict improvement |
| 6 | Use the proved unrounded full fallback count | Strict improvement |
| 7 | Use the existing prime threshold for bad-class probability | Strict improvement |
| 8 | Compose the two source-backed envelope refinements | Strict improvement |
| 9 | Sharpen conditioning on matrix invertibility | Strict improvement |
| 10 | Account for disjoint good and bad branches | Strict improvement |
| 11 | Jointly search finite depth and positive backoff | Strict improvement; seven levels selected |

Cycles 6 and 7 are separate branches from cycle 5; cycle 8 composes their
actual formula changes. Independently reported gains are never added.
Finite-depth ties and strict boundary exclusions are preserved. No
infinite-depth or zero-backoff endpoint is accepted.

Evidence Forge retains the questions, hypotheses, plans, results,
counterevidence and advisory decisions in its authoritative SQLite ledger.
Search records were retained retrospectively, not preregistered. Its
independent dossier assessments establish only exact captured JSON values
and file identities. The mathematical reasoning, external Python execution
and physical replay are separately scoped evidence; they are not Forge
semantic-adapter acceptance, evaluated lookup guidance, a full Lean theorem
proof or independent human peer review.

All retained all-size compiler, common-chart, restored-row, routing,
selector, prime-supply, precision/recovery, complex symbolic and analytic
transfer assumptions still apply.
