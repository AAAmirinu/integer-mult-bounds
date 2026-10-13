# Completed checks and limits

Exact base: `17ce0c79b7b51c2634b439ea5a2b754f09909693`.
The refreshed upstream head `66849e1475c930fd7732b1a0067ffee7e1e95f60`
changes only `CONTRIBUTING.md`; the selected result and all four scientific
input pins are unchanged. All authored scientific code was checked locally
on macOS 27.2 arm64. No remote Linux or GitHub CI pass is claimed here.

## Scientific package

- Python 3.9.6, 3.11.16 and 3.13.16 reproduce `RESULTS.json` exactly,
  including isolated optimized runs (`-B -I -O`). An explicitly generated
  fresh Python-3.11 receipt matches the committed bytes by `cmp`.
- Ten radices, 80 primitive embeddings, 193 split-prime runs and **2,918
  determinant/adjugate evaluations** are completed. Every CRT modulus
  exceeds twice the conservative coefficient bound. Radices 16, 25 and 27
  use 25, 60 and 71 auxiliary primes respectively.
- All eight predecessor determinant/norm examples match exactly, including
  Galois substitutions for nontrivial primitive powers. The original #621
  primary checker was also rerun in Python 3.11 and its complete output
  compared byte-for-byte to its pinned `EXPECTED.json`.
- Eight scientific negative controls pass. The six extra regression tests
  pass on all three Python versions, including optimized execution. They
  check 96 small matrices against the permutation determinant formula,
  literal adjugate minors (including a singular nonzero-adjugate case),
  and all **1,000** monomial/coefficient trace-duality identities across
  the radix domain, as well as CRT/interpolation/source-pin failures.
- The fresh optimized Python-3.11 scientific replay took 5.87 seconds
  locally. This is a reproduction observation, not a before/after benchmark
  or performance-improvement claim.

Certificate SHA256:

```
2ec2a8eec36bd7cd29f9fcd63eec8b9fb05f0cbbf8eb80d83807453734babcb1
```

No producer imports, rational cyclotomic-field engine, or SymPy are needed
by this package. The scoped CI workflow uses the repository's existing
pinned checkout/setup actions and runs the tests and complete byte-equal
receipt replay on Linux/Python 3.11 and 3.13. Remote execution is separate
from these local results.

## Repository checks

`python3 -B scripts/verify_selected_result.py` passes against the unchanged
base selection. The original #621 primary replay passes. The read-only
joint-dual source-pin check also passes at this base; an earlier import
attempt lacked the experiment directory on `sys.path`, and was corrected
before that source check ran.

The required `make gen4-bank-verify` passes completely in a separate clean
temporary checkout at the exact base. All nine mandatory fresh stages,
source integrity, scalar/prime controls and omission controls pass. It took
237.486 seconds. Its source-bound original report is retained in
`GEN4-RECEIPT.json`; this historical κ is not the selected frontier.

One full `make verify` was attempted in another temporary checkout. It
passed community, producers, partial-gauge, three-stage-cover, paired-cube,
recycled-bit, entrance-banks and gen4 checks. It then stopped in
`frontier626-verify` at the bit543 cohort C++ compilation because
`boost/multiprecision/cpp_int.hpp` is absent. The preceding bit-supplier
scalar/interface controls passed. The full suite did **not** pass, and
later targets were not run. No assertions, coverage, source pins or required
checks were disabled to get past that environmental failure. The suite was
not repeatedly relaunched. Numeric dependencies for these inherited checks
were isolated in `/private/tmp/integer-mult-seed83-venv`: NumPy 2.3.5,
SciPy 1.17.0, SymPy 1.14.0 and mpmath 1.3.0.

All regeneration took place in temporary checkouts; the contribution tree,
`upstream/`, old packages, selected record and repository generators are
unchanged. This evidence establishes the scoped finite identities and
reproducibility, not the uniform inverse or full multiplication theorem.

The scoped workflow was parsed with PyYAML 6.0.2 in the temporary verification
environment; its triggers, read-only permissions, two-version matrix and six
steps were checked. Git diff whitespace checks pass on the staged change.

Retained local log SHA256 values:

- Full make attempt: `8e331316515a19a318cf547ed273a4995809a64091edc8343d8c9fca13f37a14`.
- Historical gen4 replay: `9384605a4172f923c97fa0b567ebdcc0635cfd3fc6b54baa1d0ef6039b2f1100`.
- Bit543 failure log: `ad26f7b3b47dd788bfec6cf03c85d6020e1a1eec3f28263d13e71cdcc1d6b5f4`.
