# Architectural κ ceilings and a price frontier for productive-helper descendants

The productive-helper architecture that moved κ from .0023 to about .003
contains both exhausted controller derivatives and open native/state changes.
We prove a reusable distinction between them: an exact local-debt threshold for
all lengths, splits and FULL/QUERY masks of the rank-eight prefix/suffix path,
plus source-bound ceilings for the selected neutral bill and the newer P104 bills.

| Local contract | Supremum of raw saving over the entire path family |
|---|---|
| Selected [#5413](https://github.com/CrocSwap/integer-mult-bounds/pull/5413) | (.00302728824993, .00302728824995) |
| P104 [#5544](https://github.com/CrocSwap/integer-mult-bounds/pull/5544) | (.00304057807630, .00304057807631) |
| P104 [#5545](https://github.com/CrocSwap/integer-mult-bounds/pull/5545) | (.00304117181649, .00304117181650) |
| P104 [#5551](https://github.com/CrocSwap/integer-mult-bounds/pull/5551) | (.00304153116714, .00304153116715) |
| Neutral bill with eight H8 completion calls free | (.00807671283977, .00807671283979), an unrealized optimistic cap |

The universal exchange/convexity reduction builds on
[Ali Romman](https://github.com/aliromman)'s
[#5405](https://github.com/CrocSwap/integer-mult-bounds/pull/5405) and
[Chris R](https://github.com/Clear1nsight)'s independent
[#5409](https://github.com/CrocSwap/integer-mult-bounds/pull/5409).
Our per-FULL price frontier eliminates the infinite controller search for
changed providers: with local debt L(t), a favorable raw moment exists exactly when
L(t)<v*lambda_8(t). Three rational signs certify the optimal discount over all
FULL counts. For example, reaching C=.0034 from the latest P104 bill requires
more than **4.91394927369 net moment units saved per FULL**, before compiler
and outer losses. Even freeing the neutral bill's eight H8 calls cannot reach .01.

We also prove that the stated moment closure—disjoint combinations, positive
scaling, declared tensor products, exact typed cancellation and charged
splitting/completion—cannot amplify a failed bill. Compatible autonomous
provider menus cannot beat their best member. These statements do not cover a
new cross-boundary consumer, changed idle law or arbitrary native refactorization.

## Significance for researchers

Agents can stop searching longer versions of an exhausted controller and screen
new local mechanisms against a quantitative architectural target. The newer P104
claims genuinely change local economics; old fixed-profile ceilings do not exclude
them. A ceiling for **all** productive-helper native mechanisms would additionally
need a universal lower bound on local debt, which is not proved here. The claim
map also separates the higher coded p19 proposal
[#5440](https://github.com/CrocSwap/integer-mult-bounds/pull/5440) from admitted
results: its exact source still records missing chain-to-native-event compilation.

## Evidence and scope

See [the proof](PROOF.md), [claim map](CLAIMS.md), [exact receipt](RESULT.json),
[source origins](ORIGINS.json) and [validation](VALIDATION.md). An independent
standard-library rational engine reconstructs every coefficient of four complete
source invoices, proves six all-length/all-larger-saving gates and thirteen
all-length discount gates, and checks 912 small-mask comparisons. Disposable
source, invoice, profile and receipt mutations are rejected in normal and
optimized Python. The package includes a command to price a new autonomous bill.

Validation uses Python 3.12, registered serial replays and a Git-free source export.
No selected construction, frontier, allocation or queue disposition changes.
The caps are raw moment theorems under the stated controller/local contracts;
native words and the five framework assumptions are inherited. No whole selected
replay, proof-kernel theorem or independent human acceptance is claimed.

## Open next questions

- Prove a lower bound covering arbitrary legal native factorizations, or give a
  complete changed provider that crosses the local-debt threshold.
- Lower and price the coded consumer's actual native event chain, preserving
  recodings, phases, ownership and all later calls.
- Change an explicit query, idle, state or geometry invariant and derive its
  own full optimistic invoice before extending a search.
- Independently validate the written ratio-frontier proof, especially the
  small-count junction and its universal sign gate.

We retain the productive/compiler lineage of
[Cinna Davis](https://github.com/1337isnot1337),
[Cao Yifan](https://github.com/intqwq),
[Dillon Amburgey](https://github.com/dillona),
[Jacob Alan Sussman](https://github.com/jacobalansussman),
[Ali Romman](https://github.com/aliromman),
[Chris R](https://github.com/Clear1nsight),
[Gareth Davidson](https://github.com/bitplane),
[David Arias](https://github.com/DavidAriasC),
[thu-nmrc](https://github.com/thu-nmrc),
[zxv](https://github.com/zxv) and all notices in the unchanged source extracts.
Prepared with substantial OpenAI Codex assistance; Apache-2.0.
