# Validation record

Base 553d26d796fde9871ff2661a49ac7732e945410f. Registered interpreter:
`/Users/aliromman/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`,
Python 3.12.14 on macOS arm64.

Completed before the final benchmark:

- The unchanged complete selected source passes and matches both saved artifacts.
  Its first cold measurement was 391.93981024995446 s. This single measurement is
  orientation evidence; it is not substituted for the alternating benchmark.
- The uncached quadratic prototype passes the full selected replay in 180.42 s.
  This is not the final implementation or final speedup figure.
- The bounded-cache implementation passes the complete source and all new controls.
  RESULT.json records 39041 state requests,19988992 amplitude entries,21073 cache
  hits and 17968 misses. The cache holds at most 8192 entries.
- The adapter checks compare 1522 literal states and 22700 amplitudes. Changed keys,
  invalid numeric aliases, mutable outputs, capacity and eviction controls pass.
- Three actual source-proof omissions reject. The width-mismatch assertion rejects
  under optimized Python. All 13 assertions in the declared input closure are
  retained as explicit failures in the derived compiler.
- `scripts/research_package.py --package research/selected-quadratic-replay --check-only`
  passes metadata and pins. This is not scientific acceptance.

The serial six-process benchmark passes with identical stdout SHA256
`1975d01770a017b3f0b3a98a54c7c79b887d90ba0a2e1a77c37db05c385fa42b` in every run.
Medians:269.0034654160263 s literal and 98.37080179096665 s new; ratio 2.7345864882513213.
BENCHMARK.json retains every run, source input and implementation digest.

The complete actual-state audit passes: 17,651 distinct inputs and 9,037,312
amplitude entries per original literal interpreter. Both interpreters agree
with every new state numerator, zero and denominator. The trace SHA256 is
`73ac04db73d83151efb474925d48298664cc7490d31bdec7a70dcf79b448f481`.

The canonical-main refresh at de5ec2e7a6074068452f45b1a191b5c72832df4a
read priority 8. At 16:25 UTC, the overlap cache covered all 312 open PRs and
5,110 Discussion records. The only matching active claim was this investigation.
The local scan covered 7,840 main notes at the frozen base. Later main notes
require a separate search before submission.

Pending: committed export, sealed read-only optimized registered commands,
actual source-corruption controls and published artifact checks.
Hosted CI, independent human review and proof-kernel acceptance are separate.
