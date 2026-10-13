# Attribution and assistance

Prepared for Jason Willems (@at1as) with substantial OpenAI Codex assistance
in selecting the scope, deriving the fixed-radix bounds and modular lifting argument, writing the
programs and documentation, and executing verification. A separate Codex
agent reviewed the lifting proof, and another reviewed its checker. No independent
human mathematical review is claimed. “Independent verifier” refers to
its separate arithmetic implementation, not independent human authorship.

Ali Romman (@aliromman), PR #621 at
`520774462b19b29af41554b74def31f9d01e997e`, supplied the prime-power cyclic
conditioning theorem, the conjugate-reciprocal strategy and the all-length
Fourier inverse bound. His original package's attribution and AI disclosure
remain in research/prime-power-cyclic-inverse/NOTICE.md. This contribution
adds literal composite-radix certificates, a seed-certificate modular lifting
argument, an integer-only checker and finite modular diagnostics;
it neither replaces that uniform theorem nor claims its methodology as new.

The kernel definition comes from the OpenAI exact-DFT preprint at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, section local.tex,
anchors loc:newton and loc:fourier-factorization. Classical q-Pochhammer
and Newton Fourier factorization is credited there and to Alexey Kuznetsov,
“Using q-calculus to study LDLT factorization of a certain Vandermonde
matrix,” https://arxiv.org/abs/1507.02959v2. No external source code is copied
or executed. The predecessor's SOURCE.json retains the detailed source pins.

Chafik Boukhalfa's concurrent PR #628 concerns rounded prime-power inversion,
restoration and stride routing. It was inspected for overlap but is neither
a dependency nor a rounded-program claim of this package.

Scott Woolsey Biggart (@swbiggart), concurrent PR #668 at
`b861542035d612ff844d0a9d1deaa0713329811a`, supplies a split-prime CRT audit
of prime-power resultants through radix 27. Its scope was checked for overlap;
no code or result from that audit is used here.

SymPy 1.14.0 supplies the optional nomination engine. Verification requires
only Python's standard library. All new files use the repository's
Apache-2.0 license. No all-composite-radix or literature-priority claim.
