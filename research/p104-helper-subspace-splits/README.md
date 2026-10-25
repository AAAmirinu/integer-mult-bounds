# Conditional kappa 0.00310432 from composed helper splits

This construction gives complete conditional **kappa 0.00310432**.
It improves the consumed [PR5601](https://github.com/CrocSwap/integer-mult-bounds/pull/5601)
claim by **0.00001837** and the released
[PR5608](https://github.com/CrocSwap/integer-mult-bounds/pull/5608) claim by
**0.00000248**. The gain over selected 0.003027288235 is **0.000077031765**
(about **2.5446%**). The selected record is unchanged.

At a common-frame cut, a pure helper input functional and a pure helper
output direction can have unit pairing. Explicit scalar bases then let one
independent target finish early and a fresh independent input use the rest
of the program. Both complete boundary supports must be proved. A pure
intermediate row alone does not earn a second target.

The construction combines the released PR5605 shared relay with PR5601,
then applies five fixed PR5602 boundary relations and nine independent helper
splits. Finally it applies PR5606's two preparation identities in the new
basis. The preparation removes two paid rank-one queries and debits the
rank-two helper target. Its extra owned work is charged.

Read the [proof](PROOF.md), [five fixed relations](BOUNDARIES.json),
[nine exact cuts](SPLITS.json), [preparation sites](PREPARATION.json),
[complete word](WORD.json.gz), [receipt](RESULT.json),
[source pins](SOURCES.json), and [validation record](VALIDATION.md).

| Quantity | Result |
| --- | ---: |
| Local public inputs / independent helpers | 743 / 535 |
| Owned roles / lifetimes / peak | 9 / 11 / 2 |
| Local events | 25,428 |
| Complete paid calls | 66,546 |
| Complete productive fields | 12,958 |
| Complete rank-mass surplus | 760 |
| Tested saving | 0.0031043205 |
| Complete conditional kappa | 0.00310432 |
| Raw crossing | (0.00310432143397, 0.00310432143398) |
| Exact native maps | 2,916 |

Every helper normalizer, main adapter, scalar basis operation, route,
COPY/CLEAR path, thin query and whole idle is charged. The independent field
count enters the completion-tail bound. Tail decay is 39/40 and the compiler
logarithm power is 1024. The ordinary BIT saving stays at 0.0034. Two exact
moment engines, every compiler condition, 54 strict outer conditions and
four functional conditions are checked. The finite compiler threshold is
`N = 2^707182000000000`; that word is not materialized.

A negative derivative bound gives the raw ceiling for this fixed invoice
on [0,0.0034]. The final discovery screen finds no further tested basis pair
in 46 boundary groups. Neither result proves a global optimum.

## Reproduce

Use Python 3.12 and the standard library, from the repository root:

```sh
python3 -B scripts/research_package.py --package research/p104-helper-subspace-splits --check-only
python3 -B scripts/research_package.py --package research/p104-helper-subspace-splits
```

The registered hook runs normally and with `-O`. Success markers are
`PASS_P104_HELPER_SUBSPACE_KAPPA_00310432` and
`PASS_REGISTERED_RESEARCH_PACKAGE`. Direct replay needs no Git or network:

```sh
python3 -I -B research/p104-helper-subspace-splits/verify.py
python3 -I -O -B research/p104-helper-subspace-splits/verify.py
```

Normal replay is read-only. `--write` explicitly regenerates the word and
receipt. Seventeen live inputs are authenticated before any source import.
The checks reject a wrong boundary event, contaminated prefix or suffix,
missing basis work, unearned target credit, a missing paid call, a wrong
native phase, a missing central translation, an inadequate cutoff and
insufficient BIT stock. The complete nine-role owned inventory and all eleven lifetimes are checked.

## Sources and coordination

The branch starts from canonical main
`5e0052ca0aa3036a3afa8b0438927377c8d97d53`, priority revision 7.
The [canonical claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/5125#discussioncomment-19183208)
records the changed question, released components and composition checks.
The last full overlap snapshot covered 340 open PRs and 4,874 Discussion
records, with complete remote pagination and incomplete sparse local coverage.
These counts describe coverage; they are not a novelty proof.

The main input is PR5601 at
`8f7e870b22885a367b347dc12791da98fd53f83d`. It contains Pierre-Loic Doulcet's
PR5565 cascade and the PR5580/PR5569/PR5561 lineage. The fixed boundary
constructor and witnesses are from PR5602 at
`6c224aa720203c4f4615e6538d8038a275387db8`. Their bytes are retained unchanged.
Only the five published relations with helpers 652, 341, 596, 668 and 684
are used. The sixth relation uses a contact removed by PR5565 and is omitted.
The relay constructor is from PR5605 at
`4a57d245ac3918ccc9947a867ece24573605e243`. Its eight source edits are disjoint
from PR5601's 21 source edits against their common PR5580 input. The preparation
identities are from PR5606 at `cd7d89345c6c5d2114625e5ce912a52ecd5e1d27`;
they are checked on the new split word before the retired helper is renamed
into the owned range. PR5608 supplied a useful earlier relay/split composition.
No new boundary, relay, preparation or frame search is introduced.

The verifier also replays the retained PR5580 and PR5565 words and checks
both source deltas. Each retained input is pinned to an ancestor of this
branch. Registered replay needs no cached unmerged-branch objects.

The earlier fifteen-split component on PR5580 remains frozen at
`31a4de233bbdd65c04c63dc3398ecf0eed8e1375`. The
[parallel claim](https://github.com/CrocSwap/integer-mult-bounds/discussions/5125#discussioncomment-19154639)
released PR5602 before this final composition check. The shared rank-one
mechanism and every reused boundary relation are credited. No exclusive
method discovery is claimed. The old components' reported gains are not
added: this word, its full native interface and its complete bill are checked.

## Credit and limits

- **Ali Romman**, with OpenAI Codex assistance: independent helper splits;
  the separate PR5602 boundary relations and PR5601 three-contact change;
  PR5580 contact step and PR5544/5545 complete P104 caller and replay.
- **flyingviper**: PR5605 shared relay and PR5608 earlier composition.
  **Scratch-net**: PR5606 prepared-helper identities and target debit.
- **Pierre-Loic Doulcet / hexapode**: PR5565 commuting-contact cascade.
- **Joel Pulikkan / GamingPuzzled**: PR5569 priced handoff and PR5472 successor
  construction. **DreamingOfClouds**: PR5561 free endpoints and PR5568 tools.
  **thu-nmrc**: PR5551 contact improvements.
- **Gareth Davidson / bitplane**, **David Arias** and **Cinna Davis**: PR2305
  composition, PR2152 coalesced word, PR2219 private reuse and controller
  lineage. **Jacob Alan Sussman**: productive mixed-target recursion.
  **zxv** and **Cao Yifan**: retained interval, compiler and native/pricing
  lineage. Earlier geometry, BIT and analytic credit remains in source notices.

The elementary basis identity is not claimed as a new general theorem.
This package supplies an explicit independent-target construction and a
complete conditional price. The same AI-assisted author constructed and
checked it; no subagents or independent human review. Apache-2.0. See [NOTICE](NOTICE).

The five selected framework assumptions remain: native implementation at
all widths, owned erasure, uniform compiler closure, precision and tape cost,
and analytic recovery. The helper-endpoint contract also remains. The full
rounded multiplier and huge uniform word are not materialized. Independent
scientific acceptance and global optimality are not claimed.

## Open next questions

An independent reviewer can check the fixed boundary relations and the first
split, then replay the complete package. More general bases, cut orders or
new frame paths remain open. Every additional target needs a clean independent
input/output contract and a complete caller bill. [TASK.json](TASK.json)
records the remaining obligations.

The finite continuation screen is available with:

```sh
python3 -I -B research/p104-helper-subspace-splits/search.py
```

It tests exact elimination-basis pairs after MOVE events within equal-boundary
helper groups. Its failure to find another candidate is not an optimum proof.
The complete-kappa verifier does not depend on that search failure.
