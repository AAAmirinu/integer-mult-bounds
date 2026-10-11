# Notice

Apache-2.0 (`LICENSE`). Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance.

- `data/input/bitE8-r865.json.gz`: utcorvusvolat-dotcom's (Dylan Crow) PR #370 E8 bit word, byte-identical (git blob 8bec1751)
  to #370's and #373's `data/bit` (Apache-2.0).
- `data/pr377/GLOBAL-REVIEW.json`: jacklightChen's (Zhihao Chen) PR #377 receipt `research/nine-stage-complex-e8-validation/GLOBAL-REVIEW.json`
  at `d0a620f`, byte-identical (git blob 332f011f), Apache-2.0. Only its `profile`, `m`, `live` and `deficit` fields are read. None of #377's scripts were run.
- `data/final/bitE8-kernel.json.gz`, `stages/*.json`: this package's stages and final word.
- `code/checkers/legality_h.cpp`, `columns_h.cpp`, `json.hpp`: PR #266's official cohort checkers, as vendored in our #312/#359
  packages. Only the copy count (NCOPY, default h) and the constants h, v and R are parameterised; `bits/stdc++.h` is a portability shim.
  `columns_k.cpp` is our port of `columns_h.cpp` to the bridged word B_K. Its schedule and bridge tables are generated from DaysSky's #363 rule.
  #373's `columns_k.cpp` was read as data for reference only.
- `code/engines/*`: PR #315's engines (DreamingOfClouds; eumemic; #144/#23 lineage), as vendored in our #329/#359 packages.
- `code/layout_bk.py`: our reimplementation of #363's B_K rule. `code/guard.py` evaluates #375's generalised guard form at the bit
  parameters; it is our own code, and #375 was read as data.
- `code/e8core.py`, `stages.py`, `export249.py`, `nondeg.py`, `controls.py`, `tile_m.py`, `kappa.py`: our own code. `tile_m.py`'s `tile()` and
  `economy_tile()` are verbatim from our #329 `bank_template.py`.
