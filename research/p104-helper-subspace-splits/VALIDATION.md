# Validation record

Environment: macOS, CPython 3.12.14, standard library only. Scientific
replays ran serially on the isolated `codex/kappa-structural-20261025` branch.
The scientific base is canonical main
`5e0052ca0aa3036a3afa8b0438927377c8d97d53`.
The verified scientific commit is
`baf2921bede71664d201e055e5ba34fe5f979674`.

The follow-up branch `codex/kappa-composed-00310432` starts from refreshed
canonical main `6cf7a683f447b9f1e2333791907fd92be5009a63` and incorporates that
scientific commit. Main contains the earlier PR5599 result at
`09dd0965711ca7eeb169057a420abab1c9052137`, merged by a maintainer during this
work. The scientific files and shared runtime inputs retain their exact bytes.
Only this validation record and the README change after the scientific replay.
Priority revision 7 and the selected frontier are unchanged.

## Current complete replay

The direct isolated normal replay passed with artifact generation:

```sh
python3 -I -B research/p104-helper-subspace-splits/verify.py --write
```

It reconstructs the PR5605 relay and checks that its eight source edits are
disjoint from PR5601's 21 edits. It then checks five fixed PR5602 boundary
relations, nine independent prefix/suffix cuts and both PR5606 preparation
identities on the new word. Every intermediate arbitrary-input interface
passes. The rank-two target is debited and both replaced paid queries are
removed. Nine owned roles, eleven lifetimes and peak occupancy two are charged.

The final checks cover 565,504 transpose coefficients, 2,916 exact native
maps, 1,070 helper normalizers, 208 main adapters and the complete physical
caller. Two exact moment engines, every compiler condition, 54 strict outer
conditions and four functional conditions pass. Eleven local/controller
mutation controls reject, as do the retained wrong-phase, old-cutoff and
old-BIT controls. The exact raw crossing is
(0.00310432143397, 0.00310432143398).

The native growth bound uses local paid rank mass 5986. The scalar allowance
is 219990 and the route allowance is 5175000 per local call; their sum is
below 10000000. The complete nonrecursive bound is 184647552, below 1000000000.
The compiler threshold is `N = 2^707182000000000`.

The verifier authenticates 17 live inputs before source imports. It replays
the PR5580, PR5565 and PR5601 words and checks both source deltas. The retained
PR5602 and PR5605 constructors are unchanged. The PR5606 constructor is retained
as provenance; its exact identities are adapted to this word, checked again,
and followed by an explicit public/owned role permutation. No source function
is monkey-patched.

The final discovery run tested 46 boundary groups and found no further
candidate in its finite basis-pair class. This is not a global optimum.

The registered normal and optimized replays both passed:

```sh
python3 -B scripts/research_package.py --package research/p104-helper-subspace-splits --check-only
python3 -B scripts/research_package.py --package research/p104-helper-subspace-splits
python3 -B scripts/check_research_commit.py --package research/p104-helper-subspace-splits
```

The metadata and source-pin check passed. The committed-byte check passed
for all 35 package and declared-input files at the scientific commit.
The exporter and its integrity check also passed:

```sh
python3 -B scripts/export_research_package.py export --package research/p104-helper-subspace-splits --ref baf2921bede71664d201e055e5ba34fe5f979674 --output /tmp/helper-splits.tar
python3 -B scripts/export_research_package.py check /tmp/helper-splits.tar
```

The exported package passed a fresh isolated optimized replay with no Git
directory, an empty PATH, file mode 0444 and directory mode 0555. The run
used an absolute Python executable with `-I -O -B`. All 36 files, including
the export manifest, kept their hashes and modes. A one-byte change to the
retained PR5605 constructor then failed at its SHA256 check before import.
The test restored the exact source bytes and mode and checked all files again.
The harness returned `PASS_READ_ONLY_GIT_FREE_REPLAY_AND_SOURCE_FAULT`.
No pre-existing branch objects or writable source files were needed for this
replay. These are author-side checks, not independent scientific acceptance.

## Source history and limits

The source copies are pinned to retained paths at ancestor commits
`29fe88ba218b5d2192d8e31f07a01d1141afdacd` (PR5580),
`bf64e66656843a64e798b8374cd9f53add3f6f46` (PR5565),
`55914a0de83df255bd7e7071d79ad04b81ca1070` (PR5601),
`0bccb2ff858db877119217f7d98409ee6a24ccce` (PR5602), and
`4ae31ae93e86d6ab7ddd75e42fee86cf21cdb8c8` (PR5605 and PR5606).
Each SHA256 and Git blob equals its recorded published source. Registered
replay needs no cached unmerged-branch objects. Full-history preflight is
not run because this checkout is shallow.

Independent human review and hosted CI are pending. No complete rounded
multiplier or enormous uniform word was materialized. The five selected
framework assumptions and the helper-endpoint contract remain.
