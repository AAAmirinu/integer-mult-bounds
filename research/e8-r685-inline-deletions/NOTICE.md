# Notices
- PR #504 (our draft; `research/e8-r687-read-then-climb`, head 35057a6), used unchanged and pinned in `SOURCE.json`: the R687 hierarchy
  (`data/hierarchy-r687.json`), read-then-climb phases (`code/hier_word_rtc.py`; restated here in `code/r685_word.py`), the kernel step
  (`code/kernel_exact.py`), pivot data and bounds (`code/pivot_data.py`, `code/exactgen.py`), B-rule-aware mixing (`code/mix_target.py`), the
  relaxed all-column checker, the mix check, the copy-anatomy check and the eleven-stage hosting, audit and assembly code. Its own credits are in
  its NOTICE.
- PR #370 producer, compile2/fullword, checkers and pricing (Dylan Crow, utcorvusvolat-dotcom), Apache-2.0: used unchanged from
  `e8-r740-replica32/parent436`. Only one statement of compile2 (the chain loop) is replaced at run time, by the pinned register chains
  (`code/r685_word.py` applies the patch to the unchanged source and asserts each anchor occurs exactly once).
- PR #443 elimination reuse and retiming (eumemic), and its kernel/replica/replay code (chafreaky), Apache-2.0: used unchanged from `e8-r740-replica32`.
- PR #442 idle-axis whole-residual hosting (DaysSky) and its complex supplier: cited and verified unchanged from `idle-axis-hosting`.
- The D4(c) inline and the optimal register chains (`data/inline-kids.json`, `code/chain_model.py`, an exact path-cover ILP over the read events of a
  fixed hierarchy) come from the project's poset and section scouts (DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code); the sections
  scout's exact per-block search over inline and re-pairing moves is the proof that the inline is the only move in that family.
- The sweep that finds redundant copies (`code/copy_sweep.py`: exact symbolic replay, legal-frame windows, deletion with alternative sources) and the pivot
  annealer restated on the pivot data (`code/select_pivots.py`, after the annealer of `research/e8-r715-kernel-cap`): DreamingOfClouds with Claude Opus 5.5
  (Anthropic), via Claude Code.
- The exact pivot certificate (`code/exactgen.py`, via #504) and the matroid formulation of pivot selection: the project's matroid scout.
