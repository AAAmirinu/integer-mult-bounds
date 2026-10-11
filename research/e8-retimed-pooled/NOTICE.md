# Attribution

Prepared by chafreaky with OpenAI Codex, under Apache-2.0.

The complete PR #496 package by eumemic is vendored unchanged at `vendor/pr496`, pinned to 00cf70efd6a8637531deafef698157ca83e249ee. Its original licenses, notices, source pins and complete #484/#493 dependencies are preserved. Whole-owner pooling, the frozen colored allocation, controller audits, prefix argument and finite accounting are reused from that package.

The frame schedule is taken from PR #495 at 355d9f7ff293e291676ff4a32eed434419692576, `research/e8-combined/data/complex/FULL-WORD.json.gz`, by aliromman. Only the matching main-word frame fields are transferred; its separate kernel prefix is discarded. The gauge/kernel builder and selection are reused unchanged from PR #484 by DreamingOfClouds, prepared with Claude Opus 5.5. The bit supplier is PR #493 by eumemic. Earlier source attributions remain in the vendored notices.

`code/lg_mutants_retimed.py` is an attributed derivative of #484's mutation checker. It changes only M8's choice of a valid outside-centre control instance and adds explicit assertions that G3 rejects it and all 14 controls reject. No positive checker is weakened. The new contributions are the exact retiming-transfer gate, the composition with gauges and pooled whole owners, and the fresh root verification and certificate.
