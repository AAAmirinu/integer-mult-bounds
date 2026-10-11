# Notice

Apache-2.0 (`LICENSE`). Prepared by Chafik Boukhalfa (chafreaky) with substantial Anthropic Claude assistance.

- `complex/gcert1-e8-r783.json.gz`, `complex/gx/gx.py`, `complex/gx/gxcore.py`: Jacob Sussman,
  jacobalansussman/wht-power-saving-lean at `9c94857`, Apache-2.0. These are byte-identical (by git blob id) to our #378 copies and those vendored in
  #363/#365/#375. The certificate's sha256 equals the E8 certificate pinned by #377. The upstream LICENSE and NOTICE are kept as
  `complex/LICENSE-wht-power-saving-lean` and `complex/NOTICE-wht-power-saving-lean`.
- `data/gcert1-e8-r783-far.json.gz`: our #378 certificate (`research/e8-complex-far-retiming/data/`, c248962), byte-identical.
- `data/pr377/GLOBAL-REVIEW.json`: jacklightChen's (Zhihao Chen) PR #377 receipt
  `research/nine-stage-complex-e8-validation/GLOBAL-REVIEW.json` at `d0a620f`, byte-identical (git blob 332f011f), Apache-2.0.
  Only its `profile`, `m`, `live` and `deficit` fields are read. #377's `complex_candidate.py` and `global_nine.py` were read as data, to derive
  the profile rule that `code/nine.py` reimplements. None of #377's scripts were run.
- `data/bit/bitE8-kernel.json.gz`: our #382 bit word (`research/e8-kernel-bit-b3/data/final/`, 015f00b), byte-identical. It is derived
  from utcorvusvolat-dotcom's (Dylan Crow) #370 E8 bit word (Apache-2.0).
- `code/engines/moment.py`, `base_two_moment.py`, `outer.py`: PR #315's engines (DreamingOfClouds; eumemic; the #144/#23 lineage), as
  vendored in our #329/#359/#378/#382 packages.
- `code/layout_bk.py`: our reimplementation of DaysSky's B_K rule (#363).
- `code/e8core.py`, `cxcheck.py`, `cxop.py`, `cxretime.py`, `cxsplit.py`, `cxpiece.py`, `cxfar.py`, `cxfinal.py`, `cxkernel.py`: our own code,
  copied unchanged from #378. `code/nine.py` and `code/far9.py` are new here: #377's profile rule with the swapped unit, and our search with #377's ledger.
