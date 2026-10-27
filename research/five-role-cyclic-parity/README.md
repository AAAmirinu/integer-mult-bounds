# The five-role cyclic parity stencil needs exactly nine XORs

This contribution was produced by Nick Petalas. Apache-2.0.

Claim type: finite certificate with a written reduction to arbitrary binary
vector inputs. The complete invertible map

```
y_i = x_i + x_(i+1 mod 5) + x_(i+2 mod 5),   0 <= i < 5,
```

has exact minimum cost nine when each directed register addition costs one.
All five initial registers are arbitrary. No workspace or free basis operation
is allowed. [PROOF.md](PROOF.md) displays a nine-instruction word and explains
the exhaustive lower bound. The complete radius-four neighborhoods of the
identity and target each contain 22,531 matrices and are disjoint, excluding
every word of length at most eight.

This answers one concrete larger-domain synthesis question beyond the four-role
limit in [Ali Romman's PR #5793](https://github.com/CrocSwap/integer-mult-bounds/pull/5793),
head `9ddb022cc1d879a5d3173f8f1f526a2ff504e7b3`. That predecessor is motivation,
not a scientific input or executable dependency. The new endpoint and finite
exclusion are the contribution here. Finite-group shortest paths and
meet-in-the-middle exclusion are classical; literature priority is unclaimed.

## Reproduce

From the worktree root, with the CPython 3.12 standard library:

```sh
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -B research/five-role-cyclic-parity/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -I -W error -O -B research/five-role-cyclic-parity/verify.py
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/research_package.py --package research/five-role-cyclic-parity
/Users/nick/git/integer-mult-bounds/.venv/bin/python3.12 -B scripts/check_research_commit.py --package research/five-role-cyclic-parity --check-source-history
```

Local validation used CPython 3.12.15 on macOS 27.0.1 arm64.
Another CPython 3.12 interpreter may replace that absolute path. Both registered
commands have a 120-second bound. The direct verifier needs neither Git nor
network and writes no files. It emits `PASS_FIVE_ROLE_CYCLIC_PARITY` in a generated
JSON receipt containing the SHA256 hashes of all six package files. No receipt
is handwritten. Historical catalogue and selected-record pins in
[SOURCES.json](SOURCES.json) provide provenance; they are not live math inputs.

The verifier re-enumerates all three radius-four balls, including the known
eight-gate positive control, then checks all 32 literal input bit patterns,
the reversed word, nine deleted-gate controls and nine malformed-input controls.
The counts measure labeled matrices, with no quotient by wire permutations.
The lower bound quantifies over every finite word shorter than nine, not merely
one search grammar or a selected list of Gaussian eliminations.

## Scope and limits

The original `complex-rank-shape-decoder` card is explicitly changed to this
scalar linear-synthesis side result in [TASK.json](TASK.json). Current selected
metadata orientation passed on canonical main
`de5ec2e7a6074068452f45b1a191b5c72832df4a`, priority revision 8. The selected
conditional kappa is unchanged. This package does not bind the stencil to an
actual source-native caller or meet the card's complete-supplier gate.

Other endpoints, additional dirty or clean roles, free basis changes, nonlinear
instructions, odd characteristic and unequal gate prices are outside scope.
Native phases, route and ownership legality, restoration costs, rounding,
physical tapes, full recursive invoices and supplier admission remain open.
No selected cold replay, Lean or Docker run is needed or claimed. Independent
human and formal proof-kernel review are unclaimed.

Power of Ten inspection is confined to the new verifier. All loops are bounded
by five roles, twenty gates, four search layers, 32 inputs or nine witness gates.
Each search ball contains at most `1+20+20^2+20^3+20^4=168421` generated-word
endpoints, before deduplication. The actual retained ball has 22,531 matrices.
Functions fit within 60 lines, use no recursion, subprocesses or dynamic code,
and keep all mutable search state local. Boundary checks reject malformed
literal inputs. Mathematical checks remain active under optimization. Rule 3
has a managed-runtime deviation: Python allocates bounded integers, tuples
and sets during the finite command. The fixed domains above bound retained
storage; this is not a steady service. Warning-strict ordinary and optimized
execution and in-memory syntax compilation provide diagnostics.

## Open next questions

Can one actual native caller use this stencil as a cheaper complete adapter?
First identify its exact five-role source and target boundary, then charge
aliases, native phases, conversions, ownership and every restoration operation.
No compatible caller or complete paid invoice is supplied. A nine-XOR scalar
minimum alone does not imply a recursive gain. No follow-up is reserved.

## Related work and credit

Ali Romman #5793 supplies the custom-alphabet finite-group synthesis interface
and its explicit four-role boundary. Its cited zero-frame feedback censuses
retain their separate source contracts and attribution. No predecessor code is
copied or replayed. PR #5898 concerns four arbitrary data inputs and a zero
helper with a bank-exchange endpoint; this contribution has five arbitrary
inputs and a nonpermutation full-rank endpoint. The two scalar minima are for
different contracts.

The [advance CLAIM](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19216913)
preceded the substantive search. Live PR bodies, recent account submissions,
main README formulas, merged PRs, current Discussions and local reservations
were checked. Cached overlap coverage has freshness and sparse-checkout limits;
these searches cannot establish absence of unpublished overlap.
