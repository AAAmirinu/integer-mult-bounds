# Attribution, license and assistance

This contribution is offered under Apache-2.0. The original rational arithmetic
engine in `reference/base_two_moment.py` is retained **byte for byte** from
CrocSwap/integer-mult-bounds at commit
`66849e1475c930fd7732b1a0067ffee7e1e95f60`, from
`research/five-stage-gen4-banks/base_two_moment.py`. Its Git blob is
`14a90fa0e788217856f070382c9e61bd7c603c61`. The same blob is present at
`research/complex-allcold/engines/base_two_moment.py`. Its original docstring,
imports, constants and checks are preserved. The repository is maintained by
Douglas Colkitt; this contribution does not reassign authorship of that engine.

The arithmetic fixtures credit Chafik Boukhalfa's #626 owner repair, Jeremy
Kothe's #622/#623 K-triangle/provider work, eumemic's #543 bit supplier, Rohan
Arun's #559 native-complex recurrence correction, and the cumulative contributor
lineage retained in the repository's selected review. Their supplier counts,
physical constructions, original interval engine, surcharge rule and accepted
witness are not new contributions of this package. This package neither
independently reconstructs those suppliers nor takes credit for their bounds.

The new contribution applies homogeneous integer Horner evaluation to the
existing 80-term logarithm, with a scoped equivalence derivation, tests,
mutation controls and measured timings. Horner evaluation and clearing common
denominators are standard algebraic techniques; no invention or literature
priority claim is made for them.

Prepared at Tuomo Kiiskinen's request with substantial OpenAI ChatGPT assistance
in the derivation, code, testing, benchmarking, packaging and prose. The
assistant performed the reported local runs. No independent human review,
separate-agent review, remote CI pass, or Lean verification is claimed.

The subsequent submission pass used OpenAI Codex to inspect the supplied ZIP,
review the code and algebra, verify pinned inputs against a complete checkout,
replay the unchanged implementation and controls on macOS, and prepare the PR.
The original implementation, proof and Linux evidence remain unchanged; fresh
submission receipts are identified separately in SUBMISSION.json.

The final overlap check also read PR585 and PR605 descriptions. Their scoped
Lean logarithm/moment certificate proofs are prior complementary work; this
package neither imports them nor claims to replace their formal guarantees.
