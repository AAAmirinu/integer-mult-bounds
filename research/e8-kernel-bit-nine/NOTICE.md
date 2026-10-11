# Notice

Apache-2.0 (`LICENSE`). Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance.

- `data/input/bitE8-r865.json.gz`: utcorvusvolat-dotcom's (Dylan Crow) PR #370 E8 bit word, byte-identical (git blob 8bec1751; = PR #381 `data/bit`).
- `data/pr376/frame-selection.json`, `data/pr376/reuse-selection.json`: applecrusher's PR #376 witnesses (`research/e8-bit-helper-reuse`, head d2ca983), byte-identical (git blobs 647b3436, a6954dc6), Apache-2.0 (`data/pr376/LICENSE-pr376`). Prepared there with OpenAI Codex assistance.
- `code/apply376.py`: our own re-implementation of applying those witnesses, written from #376's PROOF.md data semantics. It does not import or run #376 code.
- `code/checkers/`: PR #266's official cohort checkers, our B_K columns port (`columns_k.cpp`) and nlohmann/json (MIT), as in our PR #382.
- `code/engines/`: PR #315's moment engines and outer assembly (DreamingOfClouds), unchanged.
- `code/bootstrap.py`: our reimplementation of rohanarun's PR #392 refined pricing tail, from our PR #407.
- `data/complex-b.json`: complex coarse savings cited from PR #407 (ours), #410 (eumemic) and #409 (rohanarun).
- `code/layout_bk.py`, `code/guard.py`: our reimplementations of DaysSky's B_K rule (#363) and #375's halving-degree guard.
