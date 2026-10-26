# Validation record

Environment: macOS, CPython 3.12.14, standard library only. Scientific
replays run serially in the isolated contribution worktree.

The frozen scientific input base is canonical main
`5e0052ca0aa3036a3afa8b0438927377c8d97d53`, priority revision 7.
The follow-up branch starts from refreshed canonical main
`6cf7a683f447b9f1e2333791907fd92be5009a63`. That main contains PR5599 at
`09dd0965711ca7eeb169057a420abab1c9052137`, merged by a maintainer during
this work. The selected frontier and shared executable inputs are unchanged.

## Current complete replay

The direct isolated normal replay passed with artifact generation:

```sh
python3 -I -B research/p104-helper-subspace-splits/verify.py --write
```

The marker is `PASS_P104_HELPER_SUBSPACE_KAPPA_00310440546`.
The claimed saving is 0.00310440546, tested at 0.003104405465. The exact raw
crossing is (0.00310440547057, 0.00310440547058). The reserve is 10^-12.
Power and logarithm power remain 1024. The compiler threshold is
`N = 2^80511200000000000`.

The verifier authenticates 18 live inputs before source imports. It replays
the PR5580, PR5565 and PR5601 words and checks both source deltas. The unchanged
PR5605 and PR5612 constructors build the shared and delayed relays. Their
13 combined source edits are disjoint from PR5601's 21 edits. The delayed
paid delta is exactly H4+H7-H5-H6, with every target retained.

It then checks five fixed PR5602 boundary relations, nine independent cuts
and both PR5606 preparation identities on the new word. Every intermediate
arbitrary-input interface passes. Only the witness event indices change.
The H2 target is debited and both replaced H1 queries are removed. Nine
owned roles, eleven lifetimes and peak occupancy two are charged.

The final checks cover 565,504 transpose coefficients, 2,916 exact native
maps, 1,070 helper normalizers, 208 main adapters and the complete physical
caller. Two exact moment engines, all compiler conditions, 54 strict outer
conditions and four functional conditions pass. Eleven local/controller
mutation controls reject, as do the wrong-phase, old-cutoff and old-BIT controls.

The scalar allowance is 220154 and the route allowance is 5175000 per local
call; their sum is below 10000000. The paid rank mass is 5986. The complete
nonrecursive bound is 184647552, below 1000000000.

A separate exact receipt comparison uses PR5613 at
`32f23af8790cc3c435bb1f495d861332b4f000e3`. Its bill differs by 72 extra rank-five
paid calls and 72 extra rank-five targets. Thus its signed moment equals
this one. That comparison does not independently accept PR5613's construction.
The tighter reserve uses headroom in that common invoice; it does not claim
another physical mechanism.

The final finite split screen tested 46 boundary groups and found no further
candidate. The screen is restricted to the declared after-MOVE basis-pair class.

Registered normal and optimized replays both passed at scientific commit
`3e038c5da1b56e9c9e3ad76c0592e91914f7eb6d`. The metadata/source-pin check and
36-file committed-byte check passed. The official export and its integrity
check also passed. These commands reproduce those checks:

```sh
python3 -B scripts/research_package.py --package research/p104-helper-subspace-splits --check-only
python3 -B scripts/research_package.py --package research/p104-helper-subspace-splits
python3 -B scripts/check_research_commit.py --package research/p104-helper-subspace-splits
python3 -B scripts/export_research_package.py export --package research/p104-helper-subspace-splits --ref 3e038c5da1b56e9c9e3ad76c0592e91914f7eb6d --output /tmp/helper-splits.tar
python3 -B scripts/export_research_package.py check /tmp/helper-splits.tar
```

The exported package passed a fresh isolated optimized replay with no Git
directory, an empty PATH, file mode 0444 and directory mode 0555. The run
used an absolute CPython 3.12.14 executable with `-I -O -B`. All 37 files,
including the export manifest, kept their hashes and modes. A one-byte change
to the retained PR5612 constructor then failed at its SHA256 check before
import. The test restored the exact source bytes and mode and checked all
files again. The harness returned
`PASS_READ_ONLY_GIT_FREE_REPLAY_AND_SOURCE_FAULT`.

Only this validation record changes after the frozen scientific replay.
The final publication check compares all other 35 package/input files with
that commit. No pre-existing unmerged branch objects or writable source files
were needed for the sealed replay. These are author-side checks, not
independent scientific acceptance.

## Source history and limits

The source copies are pinned to retained paths at ancestor commits
`29fe88ba218b5d2192d8e31f07a01d1141afdacd` (PR5580),
`bf64e66656843a64e798b8374cd9f53add3f6f46` (PR5565),
`55914a0de83df255bd7e7071d79ad04b81ca1070` (PR5601),
`0bccb2ff858db877119217f7d98409ee6a24ccce` (PR5602),
`4ae31ae93e86d6ab7ddd75e42fee86cf21cdb8c8` (PR5605 and PR5606), and
`a692fd471ee7c47fa30ae755b80e51ef7e022689` (PR5612).
Each SHA256 and Git blob equals its recorded published source. Registered
replay needs no cached unmerged-branch objects. Full-history preflight is
not run because this checkout is shallow.

Independent human review and hosted CI are pending. No complete rounded
multiplier or enormous uniform word was materialized. The five selected
framework assumptions and the helper-endpoint contract remain. No global
optimum is claimed.
