# Notice

New utility, adapter, tests and documentation prepared by Aman with substantial
OpenAI Codex assistance, under Apache-2.0 (the repository LICENSE).

`reference/stagelib.py` is byte-for-byte source from Chafik Boukhalfa's PR364 at
`f8c6a47abfec24b87cb1eb0a138dd73dfce2abe4`. It credits substantial Anthropic Claude
assistance. Its original notice and Apache license are retained in `reference/`.
The differential oracle compiles the two unchanged function AST nodes, avoiding
an unnecessary numpy dependency for the unit suite.

`fixtures/pr364-frames.json.gz` is a lossless deduplicated collection of B/A frame
tables from a complete replay of that source. SOURCE.json pins the source files,
five original output snapshots, fixture checksum and expected exact price. Frame
identifiers are omitted from this algebra-only fixture; the full replay adapter
checks the original full frame and word bytes, including their identifiers.

The source construction and its dependencies retain the credits in
`reference/NOTICE-pr364.md`, including DreamingOfClouds, utcorvusvolat-dotcom,
LJH-217, eumemic, Rohan Arun, Jacob Sussman, DaysSky and the official-checker and
five-stage contributors. The optimization does not claim those constructions.
