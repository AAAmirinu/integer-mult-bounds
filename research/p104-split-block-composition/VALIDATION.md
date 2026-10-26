# Validation record

Scientific commit: `a8d9d47f07acb187dfc88262bd8990c89fcc298c`.
Source-retention commit: `700a41e17e7eb7267b72596febfeac71255951dd`.
Environment: macOS arm64, CPython 3.12. Standard library only. No subagents.

The registered command passed all four commands in 507.38 seconds:

```sh
python3.12 -B scripts/research_package.py --package research/p104-split-block-composition
```

The primary and native-interval scripts each ran normally and with `-O`.
Both primary runs produced `PASS_P104_SPLIT_BLOCK_KAPPA_00311236528`.
Both chart runs produced
`PASS_ALL_67_NATIVE_CHARTS_1206_RANKS_AND_RANK3_REJECTION`.
The complete output matched every retained JSON field and the emitted word.
No scientific file changed after these checks.

`check_research_commit.py` passed all 28 scientific package files at the
scientific commit. The official exporter and export checker each passed the
same 28-file inventory. The manifest adds one file in the extracted export.

A separate optimized replay used `-I -O -W error -B`, an empty PATH, no Git,
files with mode 0444 and directories with mode 0555. The primary script passed
in 230.47 seconds; the chart supplement passed in 0.47 seconds. All 29 file
hashes and modes stayed unchanged. Temporary source extraction and bytecode
cache paths were outside the sealed export. The command sequence was:

```sh
python3.12 -I -O -W error -B research/p104-split-block-composition/verify.py
python3.12 -I -O -W error -B research/p104-split-block-composition/native_interval.py
```

Nine actual source-corruption controls passed in a disposable package copy
under optimized Python. For each direct source and the retained tar export,
flip the middle byte with XOR 1, enter `sources.sources()`, require ValueError,
then restore the bytes. `SOURCE-CONTROLS.json` records every file and rejection.
Each failure occurred at source authentication before scientific source import.
The published source files were not changed.

The initial weaker PR5718-only composition also passed its full primary replay
at conditional kappa .00311036741. It is superseded here by the stronger public
seventeen-split source. It is not counted as another result.

The submission checkpoint fetched canonical main at
`de5ec2e7a6074068452f45b1a191b5c72832df4a`. Revision 8, the current priorities,
family record and changed scalar-to-moment card were read. The complete public
overlap cache covers 312 open PR records at 16:17UTC and 5109 Discussion records
at 16:19UTC. Sparse local coverage is 93 of 7842 note paths; unpublished work is
outside this search. The disjoint block integration was handed to the active
23-split investigation with the exact public scientific commit.

The final publication commit adds only this record and SOURCE-CONTROLS.json.
Its metadata, raw committed bytes and export inventory are checked separately.
The shallow checkout prevents the optional full-history ancestry preflight;
it was not run. Frozen exports in this branch's own history remove the runtime
dependency on the unmerged seventeen-split source branch. Original Git pins,
source bytes and attribution remain explicit.

Hosted CI and independent scientific acceptance are separate and pending at
publication. No full Lean proof, huge uniform word or rounded multiplier is
materialized. The same five framework assumptions remain. No frontier change,
merge or closure is performed.
