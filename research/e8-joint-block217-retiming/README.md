# Joint gate-frame block retiming

κ = 0.001018364819189613.

The complete finite conditional verifier exited 0 at `1018364819189613/1000000000000000000`. Its exact increase over frozen PR423 is `5937864973/200000000000000000 > 0`; larger κ is better.

Two joint frame blocks change ten gate labels in PR423's complete construction. Each block changes four A gates and one B gate, while preserving every scalar instruction, its order, all 1,021 raw and pre-snapshot columns, and the retained snapshots. The construction keeps 217 gauges, 391 entrance dimensions, and 701 literal entrance gates. Both reflected ledgers, dirty restoration, coefficient words, phases, paid banks, and the complete compiler invoice are freshly verified.

Run `python -B research/e8-joint-block217-retiming/verify.py /absolute/new/output`. Python 3.11+ and a C++17 compiler are required. Optional `--replay-bit` freshly replays the unchanged source-bound bit supplier.

All-size window, correlated dirty-bank, compiler, precision, and analytic interfaces remain assumptions. This is a finite conditional construction; no unconditional multiplication theorem is claimed. New work used substantial OpenAI Codex assistance. Prior sources, licenses, notices, and AI disclosures are preserved.

The predecessor is frozen [PR423](https://github.com/CrocSwap/integer-mult-bounds/pull/423), head `997613cb3064b4096b996409a671e558251d55f8`. This result is published separately.
