# Validation record

Environment: macOS, CPython 3.12.14, standard library only. All scientific
replays run serially in the isolated `codex/kappa-structural-20261025` worktree.
The scientific base is canonical main
`5e0052ca0aa3036a3afa8b0438927377c8d97d53`.

## Completed checks

The direct isolated normal replay passed with explicit artifact generation:

```sh
python3 -I -B research/p104-helper-subspace-splits/verify.py --write
```

It checked all 15 prefix and suffix witnesses, every intermediate complete
interface, 574,564 final transpose coefficients, 2,926 exact native maps,
1,084 helper normalizers, 208 main adapters and the complete physical caller.
Two exact moment engines, all compiler conditions, 54 strict outer conditions
and four functional conditions passed. All eight local/controller mutation
controls rejected. The retained wrong-phase, old-cutoff and old-BIT controls
also rejected. The raw crossing is in
(0.00309839352211, 0.00309839352212).

The first parameter trial failed the compiler complement-capacity condition
with logarithm power 1000. The final power 1024 passes that condition and the
complete compiler check. The old count and growth constants are not reused
for the changed helper inventory.

The optional final-word discovery screen returned 53 tested boundary groups
and no further candidate. The screen restricts the cut locations and tested
basis pairs; it is not an optimality certificate.

## Committed and exported replay

The final scientific files at commit
`31a4de233bbdd65c04c63dc3398ecf0eed8e1375` passed the registered normal and
optimized replays:

```sh
python3 -W error -B scripts/research_package.py --package research/p104-helper-subspace-splits --check-only
python3 -W error -B scripts/research_package.py --package research/p104-helper-subspace-splits
python3 -B scripts/check_research_commit.py --package research/p104-helper-subspace-splits --ref 31a4de233bbdd65c04c63dc3398ecf0eed8e1375
```

The package metadata, source pins and exact committed bytes passed.
The registered hook ended with `PASS_REGISTERED_RESEARCH_PACKAGE`.
Both scientific modes ended with `PASS_P104_HELPER_SUBSPACE_KAPPA_00309839`.
Later publication edits affect only documentation and TASK metadata.

The official exporter produced a 27-file payload plus its export manifest
from that commit. Its integrity check passed. In a fresh directory with no
Git repository, empty PATH, read-only files and read-only directories, the
isolated optimized verifier passed. Every file hash and mode stayed fixed.
A temporary one-byte source corruption was rejected at SHA256 authentication
before any imported source code ran. The original bytes and mode were then
restored and checked. The final harness marker was
`PASS_READ_ONLY_GIT_FREE_REPLAY_AND_SOURCE_FAULT` (28 files with the manifest).

```sh
python3 -B scripts/export_research_package.py export --package research/p104-helper-subspace-splits --ref 31a4de233bbdd65c04c63dc3398ecf0eed8e1375 --output /tmp/helper-splits.tar
python3 -B scripts/export_research_package.py check /tmp/helper-splits.tar
```

The copied source is pinned to its retained path at ancestor commit
`29fe88ba218b5d2192d8e31f07a01d1141afdacd`. Its SHA256 and Git blob equal the
recorded PR5580 source. The original PR5580 Git object was checked before
this retention change. The final registered replay does not require cached
unmerged-branch objects. The base and retained-source commits were both
confirmed as ancestors of the contribution. Full-history preflight was not
run because this checkout is shallow.

The final continuation screen also allows the source's owned erasures. It
still returns 53 tested boundary groups and no further candidate.

Independent human review and hosted CI are pending. No complete rounded
multiplier or enormous uniform word was materialized.
