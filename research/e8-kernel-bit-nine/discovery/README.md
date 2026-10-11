# Discovery (not run by verify.sh)

Search tools that nominated the frozen kernel selection. Their floating scores only nominate; `verify.sh` rebuilds and checks the result from `stages/kernel-selection.json` alone.

- `ils.py IN NOISE SEED NSEED ITERS`: shared-donor kernel packing, scored by the linearised B₄ ledger χ(r) = r((72/r)^a − 1).
  - Phase 1 runs NSEED randomised greedy packings. The entrance order key is gain·(1 + NOISE·u).
  - Phase 2 is iterated local search: drop 5–35% of the entrance groups at random, re-pack greedily with noise, and accept if χ improves.
  - Env `START` seeds the search from a selection, and `FRACS` sets the drop fractions.
- `kernel.py`, `census.py`: the entrance candidates and per-entrance plans (our #320/#329 kernel). `NOISE`, `PNOISE` and `SEED` randomise the greedy.
- `retime.py`, `rt9.py`: our retiming descent scored at m = 72. It finds no move on #376's word, before or after the kernel.
- `trimT.py`: an exact-DP trim of a selection to a residual census that tiles width-72 banks with T ∈ {1, 3, 9} replicas.
- `mksel.py PKG SEL`: writes `stages/kernel-selection.json` and `data/final/` from a selection.

Run: 38 chains (NOISE 10/15, 30 seeded packings, then ILS) on two 20-core hosts. The best was chain s102, with χ = 0.749126, 182 entries, total entrance rank 416 and c = 1.044063934627e-3. A restart round from it found no improvement.
