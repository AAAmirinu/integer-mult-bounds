# Finite, stable tensor tests for the full dyadic Clifford group

**A uniform algebraic interface theorem and an exact verifier; no new kappa.**
For fixed scalar register programs on n binary axes, with unitary dyadic
Clifford operators and every dirty input/return retained, equality at widths
**1 through 8n+4 is equivalent to equality at every positive width**. This
covers Gaussian and Hadamard gates as well as phase-monomial maps. The cutoff
does not depend on program length or expanded support.

The [proof](PROOF.md) also gives a stable test. Let M be the squared coefficient
norm after equal exact native operators are combined. Some tested width has
normalized squared Hilbert-Schmidt residual at least **(14/15)M**. An explicit
rational polynomial recovers M from the finite norm sequence. Base-space pair
traces suffice. A conditional norm procedure finds a nonzero tensor entry
without allocating a tensor matrix.

For the source's nine binary axes, the sufficient tensor-width cutoff is **76**.
This is an algebraic bound, not a full supplier replay or a minimal cutoff.
The complete kappa calculation and selected frontier are unchanged.

## A concrete small-width trap

The [Reynolds example](examples/reynolds.json) adds the average of the 96
one-axis native group operators to a dirty target. It preserves the source.
Its complete endpoint is the identity at widths **1 through 7**, but fails at
width **8**, with a literal entry **5/24**. The
[certificate](examples/reynolds.certificate.json) gives the roles and coordinates.
This example uses the full group, not a numerical sample.

## Use

Python 3.12 and the standard library suffice. From the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/clifford-tensor-gram
```

Both registered modes print `PASS_CLIFFORD_TENSOR_GRAM_NO_NEW_KAPPA`.
Direct commands also work in a Git-free export:

```sh
python3.12 -I -W error -B research/clifford-tensor-gram/verify.py
python3.12 -I -O -W error -B research/clifford-tensor-gram/verify.py
python3.12 -I -B research/clifford-tensor-gram/certify.py \
  research/clifford-tensor-gram/examples/native-relation.json
python3.12 -I -B research/clifford-tensor-gram/check_witness.py \
  research/clifford-tensor-gram/examples/reynolds.json \
  research/clifford-tensor-gram/examples/reynolds.certificate.json
python3.12 -I -B research/clifford-tensor-gram/audit_mutations.py
```

The producer prints JSON. Read `equivalent_at_all_positive_widths`; a successful
process means the decision completed, and a counterexample is a valid result.
The independent witness checker prints `PASS_LITERAL_TENSOR_WITNESS 5/24`.
It uses a separate signed-word interpreter and literal matrix entries, with
no producer import, trace calculation or interpolation argument. Only the
frozen scalar arithmetic is shared.
It checks the literal nonzero entry, not the claimed norms or the universal
cutoff theorem.

## Input contract

The [native relation example](examples/native-relation.json) gives the format.
`axes` is n; `roles` counts arbitrary independent inputs and returns.
`operators` contains exact 2^n-by-2^n matrices, with integer entries or
Gaussian-rational strings such as `1/2-1/2i`. Floats are rejected. The frontend
checks dyadic entries, unitarity and normalization of all Pauli generators.
`program` and `reference` are complete instruction lists. An empty reference
is identity on every role.

| Instruction | Required fields | Action |
| --- | --- | --- |
| `add` | `src`, `dst` | Add a scalar multiple of a role |
| `query` | `src`, `dst`, `symbol` | Add an operator image of a role |
| `apply` | `dst`, `symbol` | Apply an operator to a role |
| `scale` | `dst`, `coefficient` | Scale a role |
| `swap` | `src`, `dst` | Exchange roles |

`add` and `query` accept an optional `coefficient`, default one. `query` and
`apply` accept Boolean `inverse`, default false. Self queries read the previous
value. Global phase stays inside the tensor power; scalar coefficients stay
outside. The source convention has H^2=iI. Replacing that operator with scalar
scaling by i passes width one and fails width two, as the
[phase example](examples/phase-trap.json) shows. Scalar coefficients need not
be dyadic.

## Evidence and limits

[RESULT.json](RESULT.json) records 96 group elements, 689 exact trace-filter
values, 2,124 source columns, 48 entangling trace cases, 60 explicit tensor
norms, 72 complete endpoint comparisons, 24 full tensor program comparisons,
16 random literal witnesses, two zero-axis boundary cases and 20 controls.
The source columns include both
orientations of an actual nine-axis Gaussian gate. Controls reject nonunitary
inputs, non-dyadic phases, Toffoli, malformed instructions, wrong tensor phases,
missing helper returns and false witnesses. Source hashes are checked before
the replay imports the frozen files.

[MUTATIONS.json](MUTATIONS.json) records four private-copy defects rejected in
both Python modes: a missing trace factor, an ignored inverse, an omitted
dirty return and a missing Gram normalization. The audit prints
`PASS_CLIFFORD_GRAM_MUTATIONS`. The local runs used CPython 3.12.13 on macOS
with no third-party packages.

The written proof supplies the universal quantifiers. Finite tests corroborate
it. This is author-checked with substantial AI assistance, not independent
human or proof-kernel acceptance. Compilation can expand exponentially many
terms; the base dimension is also 2^n. No polynomial-time claim in instruction
length or practical full-supplier speedup follows. No complete provider,
selected cold replay, native admission, Lean or Docker run is claimed.
Physical storage, tapes, stock, precision and outer recovery remain separate.
Programs that change with f, non-Clifford gates, continuous phases, nonunitary
scalings, rounded leaves and restricted clean-input contracts are excluded.

## Sources and credit

Base: canonical main `7c472563474e60185e6ca101a17622133d047e56`, priority 7.
[SOURCES.json](SOURCES.json) binds exact sources. No predecessor is modified.
Rohan Arun supplies the retained native compiler, following Jeremy Kothe and
the native lineage. Tekalign's retention and Cinna Davis's borrowing work keep
their credit. The complete [notice](vendor/NATIVE-LINEAGE-NOTICE) accompanies
the byte-identical kernel.

zxv's [PR #5235](https://github.com/CrocSwap/integer-mult-bounds/pull/5235)
supplies the independent-symbol interface and frozen Gaussian arithmetic.
Krzysztof Wojt's [PR #5262](https://github.com/CrocSwap/integer-mult-bounds/pull/5262)
supplies the inverse-aware interface and native-relation handoff. lm1909's
[projection-recursion check](https://github.com/CrocSwap/integer-mult-bounds/blob/7c472563474e60185e6ca101a17622133d047e56/research/projection-recursion-check/README.md)
already uses positive-width group separation, following Jacob Alan Sussman's
engine model. Cinna Davis, ToikY, Sagar Thakrar, roger-sato and the retained
free-word/tensor audits keep their earlier results and attribution.

Chris R's [PR #4928](https://github.com/CrocSwap/integer-mult-bounds/pull/4928)
and [PR #4978](https://github.com/CrocSwap/integer-mult-bounds/pull/4978)
already use finite Clifford alphabets and tensor Gram separation. Their
[general separation proof](https://github.com/CrocSwap/integer-mult-bounds/blob/7c472563474e60185e6ca101a17622133d047e56/research/two-full-retained-helper-ceiling/science/PROOF.md)
and [passive-query clarification](https://github.com/CrocSwap/integer-mult-bounds/blob/7c472563474e60185e6ca101a17622133d047e56/research/passive-saved-query-ceiling/evidence/frozen/pr4948-saved-query-macro-gate/UNIFORM-ALPHABET-ADDENDUM.md)
retain that credit. This package adds an explicit linear cutoff and constant
stability bound for fixed scalar coefficients in the full dyadic class.

Concurrent [PR #5369](https://github.com/CrocSwap/integer-mult-bounds/pull/5369)
proves a four-width criterion for affine-quadratic monomial maps.
Its scope excludes Hadamard gates. The
[coordination claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/5236#discussioncomment-19153620)
records this package's larger class, Gram test and stability claim. Public
PR/Discussion bodies and relevant main notes were checked. Historical diffs
and unpublished work remain outside coverage.

Classical ingredients are credited in [PROOF.md](PROOF.md). No new general
Burnside-Brauer theorem, general circuit identity algorithm or global priority
is claimed. The contribution is the explicit native trace filter, stable
cutoff, program frontend, compressed witness and source-bound validation.

## Open next questions

1. Replace dense matrices with phase-exact Clifford tableaux and a proved
   trace/entry routine. Start with the complete one-axis and entangling fixtures.
   Exact global-phase binding is the remaining blocker.
2. Find the sharp cutoff. Start with one-axis Gram kernels. The width-eight
   example is a lower bound; this package does not prove twelve is necessary.
3. Bind a complete current provider and measure support growth. Retain every
   input/return and native phase. Physical admission and a full bill remain open.

Ali Romman, with substantial OpenAI Codex assistance. Apache-2.0.
