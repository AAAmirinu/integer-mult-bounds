# The PR6066 stochastic prefix needs at least 76 retained bits

For the exact integer-grid forward map in [PR6066](https://github.com/CrocSwap/integer-mult-bounds/pull/6066), with its random tape unchanged, exact dirty restoration needs auxiliary information with at least **76 bits of worst-case capacity**. The existing 84-bit parity log can therefore save at most eight bits under the same boundary. No matching compression algorithm or new kappa is claimed.

The authenticated historical 9,589-event prefix has 60 halvings before any doubling. Its first 8,411 events are surjective and exactly 2^60-to-one on arbitrary integer data. Eight disjoint later 16-role blocks each have a verified four-preimage collision for one all-zero coin tape. Their product and the surjective prefix give a 2^76-point fiber of the full rounded forward map. [PROOF.md](PROOF.md) gives the quantifiers, finite-width guard and limits; [COLLISIONS.json](COLLISIONS.json) provides the small exact witnesses.

## Significance for researchers

This resolves a substantial part of PR6066's question about reducing its 84 parity bits. The 32 later doublings do not imply a 52-bit log is sufficient: chronology and source-bound collisions force at least 76 bits at the forward boundary. A smaller log would require proving and implementing a compression within the remaining eight-bit gap, or changing the forward/restoration contract.

## Reproduce

```sh
python3.12 -B scripts/research_package.py --package research/stochastic-restoration-memory
python3.12 -B scripts/check_research_commit.py --package research/stochastic-restoration-memory
```

The standard-library verifier authenticates the historical word and retained PR6066 statement, checks all 32 small collision preimages with exact integer arithmetic, exhausts each nominated block fiber, verifies disjoint literal source domains, and checks 86 complete lifted source executions plus signed-half and invalid-counting controls. The written composition proof supplies the 2^76 quantifier; this many inputs are not enumerated. Normal and optimized registered checks compare RESULT.json.

## Open next questions

Are all fibers of each tail block bounded by four, for every output and coin tape? Start with its eight exact inverse branches; a proof could close the remaining eight-bit information gap. Finite probes are not an all-tape proof.

Can a smaller retained log be computed and erased under the actual physical caller at a favorable total cost? First distinguish retained information from working scratch, charge compression and random-tape movement, and keep every arbitrary dirty input. The native MOVE and full error/cost contracts remain blockers.

## Scope and credit

This uses the historical PR5599 prefix used by PR6066, not the different selected PR6030 word. The 76-bit floor is worst-case for exact pathwise restoration with arbitrary integer inputs and unchanged tape. It does not assert an average-length lower bound, a matching 76-bit implementation, a complete physical resource optimum, or a result for every small fixed width. A conservative 4,571-bit signed/guard width suffices for the entire collision family; executed representative fixtures need only ten magnitude bits. No native/selected cold replay or new kappa is claimed.

Prepared by [zxv](https://github.com/zxv) with substantial OpenAI Codex assistance. Credit [Nick Petalas](https://github.com/petalas)'s [PR6026](https://github.com/CrocSwap/integer-mult-bounds/pull/6026), [Ali Romman](https://github.com/aliromman)'s [PR5599](https://github.com/CrocSwap/integer-mult-bounds/pull/5599), and the retained source lineage. The pending PR6066 statement is retained verbatim with exact head/hash. Apache-2.0. No independent human review or proof-kernel acceptance is claimed.
