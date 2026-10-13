# Exact logarithm intervals with integer Horner evaluation

**Status: verification-engineering contribution; no new kappa.**

This add-only package evaluates the retained 80-term rational logarithm with
integer Horner arithmetic, preserving its exact lower and upper fractions.
The selected three charged moment pairs run 2.28 times faster in the fresh
macOS submission replay and 2.41 times faster in the original Linux handoff.
The isolated logarithm microbatch runs 10.62 and 12.58 times faster respectively.
These are arithmetic timings, not full frontier-replay timings.

Base: `66849e1475c930fd7732b1a0067ffee7e1e95f60`.
OS-random assignment seed: **89**, verification engineering.
The selected conditional witness remains
`51110230636731/31250000000000000 = 0.001635527380375392`.
No existing source, supplier, certificate, manifest or `upstream/` file changes.

## Reproduce

From the repository or extracted bundle root, with Python 3.10 or later:

```sh
python3 -B research/exact-log-horner/verify.py --benchmark
```

Expected result: `PASS_EXACT_LOG_HORNER`, with 5,872 exact logarithm comparisons,
six charged moment endpoints and eight detected implementation mutations.
Timings vary by environment and are not used to determine success.
Only the Python standard library is required; no network, numerical package,
solver, compiler, or upstream build is needed for this scoped check.

Optional exact-result receipt and optimized-mode check:

```sh
python3 -I -O -B research/exact-log-horner/verify.py   --output /tmp/exact-log-horner-new-receipt.json
python3 -B research/exact-log-horner/test_package.py
```

The output file must not already exist and must be outside this package.
The second command prints `PASS_PACKAGE_CONTROLS` and eight rejected cases.
It checks source/inventory failures in paths containing spaces, both normally
and under optimized Python. Neither command disables failure checks under `-O`.

## Mechanism and exactness

Let `z=(x-1)/(x+1)=a/b`, `D=lcm(1,3,...,159)` and
`N=sum((D/(2j+1))*a^(2j)*b^(158-2j), j=0,...,79)`.
The existing lower endpoint is exactly `2*a*N/(D*b^159)` and its unchanged
upper-tail addition is exactly `2*a^161/(161*b^159*(b^2-a^2))`.
The 79 integer Horner updates evaluate N without constructing and summing
80 rational powers. There is no lower precision, shortened series,
input-dependent cache, modified tail, or altered admission decision.

`PROOF.md` gives the all-rational algebraic identity and loop invariant.
This written proof is not a Lean proof. Finite comparisons corroborate the
implementation; they are not the justification for universal equality.

The harness loads two private copies of the byte-identical original engine
and substitutes only `log_unit` in one copy. Range reduction, log(2), outward
rounding at 10^-30, twelve-term exponentials, histogram weights and surcharge
pricing remain the original code. This is not an independent reimplementation
of those inherited enclosures. The standalone new function explicitly accepts
exact Fraction inputs and integer endpoints, rejecting non-exact input types.

## Measured results

Environment: CPython 3.13.5, Linux x86_64, as recorded in
`evidence/benchmark.json`. Seven repetitions per workload, alternating engine
order, with exact output comparison after every timed pair. Medians:

| Workload | Original | Integer Horner | Speedup |
|---|---:|---:|---:|
| Logarithm microbatch (20 × 9 exact arguments) | 83.970 ms | 6.675 ms | 12.58× |
| PR626 native-complex accepted/adjacent pair | 23.585 ms | 8.901 ms | 2.65× |
| All three charged accepted/adjacent pairs | 67.830 ms | 28.110 ms | 2.41× |

The microbatch uses the nine distinct arguments produced by the reference's
strict binary range reduction on the selected profiles, including log(2).
It repeats that set 20 times; it is not a timing for one logarithm. The two
moment workloads price their indicated full intervals including the unchanged
exponentials and final rounding. The combined workload includes native complex,
conservative complex with surcharge, and bit with surcharge.

Input preparation and module import/setup are excluded. No result cache is
used. The combined measured saving is about 40 milliseconds per six-endpoint
batch here; this does not establish a material reduction in a full replay that
also rebuilds physical suppliers and executes other verification stages.

## Verification coverage

The Codex submission replay independently reran the unchanged supplied code
on macOS arm64 / CPython 3.12.8, using the same seven alternating-order
repetitions. [evidence/codex-benchmark.json](evidence/codex-benchmark.json)
contains the raw samples and executed-input hashes:

| Workload | Original | Integer Horner | Speedup |
|---|---:|---:|---:|
| Logarithm microbatch (20 × 9 exact arguments) | 51.424 ms | 4.840 ms | 10.62× |
| PR626 native-complex accepted/adjacent pair | 14.881 ms | 6.133 ms | 2.43× |
| All three charged accepted/adjacent pairs | 43.783 ms | 19.167 ms | 2.28× |

Both the normal and isolated optimized submission runs reproduce the original
exact comparison fingerprint below. The eight package corruption checks also
pass. Original Linux evidence remains unchanged; the fresh receipts have
`codex-` names. [SUBMISSION.json](SUBMISSION.json) records the source ZIP and
the complete-checkout verification of all seven pinned repository paths and
the extracted arithmetic fields. No supplier construction was rerun.

- **5,872 logarithm comparisons:** 1,261 distinct unit rationals with denominator
  at most 64; 30 seeded/adversarial rationals up to 256-bit denominators; all
  4,560 child ratios m/t for 2<=m<=96; and 21 power-of-two boundary cases.
- **Six charged moment endpoints:** acceptance at the inherited lower point
  and rejection one 10^-24 step above, for native PR626, conservative PR626,
  and PR543 bit profiles. Both lower and upper rational outputs match exactly.
  Five additional pricing controls run in each engine, covering surcharge
  distinctions and an added charged child.
- **Failure detection:** eight numerical implementation mutants; 24 inherited
  domain rejection checks; three non-exact-input rejections; and eight
  source/inventory corruption cases across normal and optimized Python.

The normal and isolated optimized full runs have the identical exact comparison
fingerprint `c926bc76b11c982a477174b4c09ea0be2b4c549ae4dcd8215d7ac19deb91202a`.
Two exact integer endpoint checks are also included. Raw evidence binds the
executed reference, replacement, fixture and harness hashes. The manifest binds
all packaged files; it deliberately excludes itself and Python bytecode caches.

A development probe weakness is recorded in `CLAIM.json`: the first tail-power
mutation escaped arguments whose reduced numerator was always one. Adding
x=9/5, hence z=2/7, detects it. Every reported final mutation passes the corrected
suite. Runtime/syntax failures of mutants do not count as numerical detection.

## Source binding, coordination and integration boundary

`SOURCE.json` records source paths, Git blob identities, acquisition scope and
inherited dependencies. The original 1,742-byte reference is authenticated to
Git blob `14a90fa0e788217856f070382c9e61bd7c603c61` and SHA-256
`aee70c242a2f1d225528fabe2002e1564d1dc884797c07d28a831c7878ee9098`.
The path-local `.gitattributes` preserves the reference's inherited final blank
line without suppressing whitespace checks on authored files. The two profile
fixtures contain explicitly extracted fields, not full original certificate copies. Their counts and physical realizability are inherited
inputs, not proved by this checker.

`CLAIM.json` records three candidate tasks, the selected scope, the local claim,
prior work and the bounded final overlap check. The main head was refreshed and
still matched the base. No pinned sprint issue was found. Relevant prior work
includes the complementary PR585/605 Lean certificate proofs. This package makes
no exhaustive novelty or priority claim.

The original ChatGPT environment could not clone GitHub and produced a ZIP
and clean patch handoff from connector-fetched pinned sources. For this
submission, Codex imported the package into a separate full Git worktree at
the same exact base, checked the original source Git blobs and fixture fields
against the repository, and reran its verification and benchmarks. The
implementation, fixtures, proof, reference and original evidence remain
byte-identical to the supplied ZIP. Updated publication prose, fresh receipts
and the resulting package manifest are the submission changes.

The package deliberately **does not activate the optimization in the selected
pipeline**. That avoids silently invalidating source pins and historical
receipts. Maintainer adoption should separately identify callers, replace the
specific engine copy, update exactly its dependent pins, and run the affected
full replay and repository checks. Those integration checks are not completed
by this standalone tool.

Not executed here: `make verify`, `make frontier626-verify`, full supplier
reconstruction, the second moment engine, all 47 assembly inequalities, Lean,
or remote CI. The all-size/compiler, common-label/mutable-source, whole-call
hosting, precision/tape/exact-recovery and analytic-transfer obligations remain
unchanged. No new conditional exponent or unconditional theorem is claimed.

## Attribution

See `NOTICE.md` and `LICENSE`. The original engine and selected supplier lineage
retain credit. The new implementation, proof, tests and packaging were prepared
at Tuomo Kiiskinen's request with substantial OpenAI ChatGPT assistance. The
subsequent source review, replay and PR preparation used OpenAI Codex. No
independent human or separate-agent review is claimed.
