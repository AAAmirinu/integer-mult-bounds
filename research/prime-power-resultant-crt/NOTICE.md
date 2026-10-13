# Attribution and assistance

Ali Romman (`aliromman`) supplied the uniform prime-power cyclic inverse
proof and two arithmetic checkers in #621, reviewed at
`520774462b19b29af41554b74def31f9d01e997e`. Its integral tail-product
kernel, conjugate-reciprocal Sylvester matrix, residue identity, and
historical exact values are the objects independently checked here.
No code from either predecessor checker is imported or copied.

The kernel definition is from the OpenAI exact-DFT preprint at
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`, section `local.tex`,
`loc:newton` and `loc:fourier-factorization`. The inherited source pin
and Apache-2.0 scope are preserved in `SOURCE.json`. The underlying
q-Pochhammer/Newton factorization is classical; #621 credits Alexey
Kuznetsov, *Using q-calculus to study LDLT factorization of a certain
Vandermonde matrix*, arXiv:1507.02959v2.

Concurrent #628 by Ali Romman supplies rounded and dirty inverse programs
and kernel certificates through radix 16. It is adjacent work, not a
dependency of this checker. The finite CRT method and the radix-25/27
extension provide distinct evidence.

Scott Woolsey Biggart (`swbiggart`) contributed this package with substantial
OpenAI Codex assistance in task selection, mathematical reasoning, code,
verification and documentation. No delegated reviewers or human review
are claimed. The contribution is under the repository's Apache-2.0
license. It changes no selected result or upstream source.
