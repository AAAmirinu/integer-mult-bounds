# The fixed #4467 leaf deficit saturates, uniformly across lockstep levels

This package proves the saturation predicted by Ryanson Jonathan / pinterbanget's [#4467](https://github.com/CrocSwap/integer-mult-bounds/pull/4467). For its fixed raw-p7 paid-rank law, the conditional deficit `B_G−S_G` converges to `Exp(λ)`, **including convergence of the mean**, uniformly for `B_G=G log5+δ`, `0≤δ<log5`.

The [proof](PROOF.md) uses the classical nonlattice interval local-limit theorem and supplies the tail argument needed for the expectation. The [exact rational certificate](RESULT.json) encloses

- `λ ∈ [0.00749912850515, 0.00749912850519]`;
- limiting mean deficit in `[133.34882837,133.34882838]`;
- limiting actual leaf log-depth in `[136.51870330,136.51870331]`.

The source has **G conditioned paid ranks plus one unconditioned terminal rank**. Ten independent exact fixtures compare the complete leaf histograms of both the original #4436 flow and #4467's diagnostic. Both standalone entry points authenticate all declared inputs before executing them. Separate mutation tests re-pin empty or terminal-truncated source branches and confirm that the actual histogram comparisons reject them; fixture-sensitivity flags are not counted as extra source checks. The main certificate checks eight fixtures and a lattice countermodel showing why discrete support alone does not justify an exponential limit.

This resolves the qualitative saturation part of #4467's open question. It supplies **no explicit finite-depth error rate**, stable-share theorem, full-flow log-gap limit, numerical refined-induction ceiling, new κ, or supplier admission. The raw-p7 profile is historical; the selected #6030 record and its five assumptions are unchanged. In particular, the predecessor's estimated `.0025–.0026` ceiling and enormous finite-rank thresholds remain unproved here.

## Sources and coordination

Scientific base: `721c03822c421b7f7fcbb2598993b947c4d88419`; priority revision 8. #4467's frozen source head is `5f5c1f98c62b9ce4f3db6c0ca47a850a0be577dc`. Its [completed investigation](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19111052) and [request for a saturation proof](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19111508) are predecessor coordination references. The current canonical claim is [#1166 comment 19240402](https://github.com/CrocSwap/integer-mult-bounds/discussions/1166#discussioncomment-19240402). [SOURCES.json](SOURCES.json) pins every live predecessor input to the base; no unmerged source history is needed.

The original direct flow is zxv's #4436 (`56003680aee2871773de408e5f01cc5dd46b144c`); the refined induction is Cinna Davis / 1337isnot1337's #4405; the lockstep construction is Jacob Alan Sussman's Theorem 1G. #4467, following #4465, already conjectured saturation and measured it numerically. The added value here is the proof, bounded-offset uniformity, certified hypotheses, and explicit separation of the leaf result from the whole-flow extrapolations.

## Reproduce

Python 3.12, standard library only, assertions not needed. From the repository root:

```sh
python3.12 -B scripts/research_package.py --package research/direct-flow-leaf-saturation --check-only
python3.12 -B scripts/research_package.py --package research/direct-flow-leaf-saturation
python3.12 -O -B research/direct-flow-leaf-saturation/verify.py --expect research/direct-flow-leaf-saturation/RESULT.json
```

The registered runner requires Python 3.12; using a default `python3` that selects 3.13 fails its declared version gate. Direct commands also work from a package export without Git:

```sh
python3.12 -B research/direct-flow-leaf-saturation/verify.py --expect research/direct-flow-leaf-saturation/RESULT.json
python3.12 -B research/direct-flow-leaf-saturation/independent_source.py
python3.12 -B research/direct-flow-leaf-saturation/test_controls.py
python3.12 -B research/direct-flow-leaf-saturation/test_enclosures.py
```

The main certificate uses `Fraction` intervals throughout: a 48-term `2 atanh(z)` series with a geometric tail bounds logarithms after power-of-two reduction; an 80-term exponential Taylor series uses `e^x≤3^5` on `[0,5]` to bound the remainder. Strict endpoint signs and a derivative lower bound isolate the invoice root. Strict monotonicity of the tilted mean (its derivative is a positive variance) isolates the tilt. Output decimals are rounded outward. The certificate does not execute the predecessor's floating-point root finder or fit its data. `test_enclosures.py` independently encloses every executed logarithm/exponential argument using a different logarithm series and a geometric-tail exponential bound. It detects zero tails and an invalid exponential majorant even when the rounded parameter receipt stays unchanged. These are finite-domain controls, not an all-input proof of the routines; both engines share exact rational arithmetic and the exponential series.

[VALIDATION.md](VALIDATION.md) records actual commands, environments and logs, including the response to the user-provided Claude Code review of `ff365dba6911ce615bec76e8d1f149faf1fe16ca`. [REVIEW.md](REVIEW.md) records the independent derivation, source check, skeptical review and shared dependencies. The proof's local-limit theorem remains an external mathematical input, rather than an assertion tested by finite examples.

## Open next questions

1. **Give a certified finite-G error bound.** This would make finite-rank extrapolations assessable. Start with a quantitative interval local-limit estimate for this fixed law and combine it with the exponential tail bound in PROOF.md §4. The present qualitative theorem supplies no effective onset or error constants.
2. **Analyze the other direct-flow components and the exact induction ratio.** This is necessary to establish a total log-gap or numerical ceiling. Start from the original source and boundary sums at the same level offset. Their limiting shares and the exact ratio remain unresolved here.

Structured questions are in [TASK.json](TASK.json). No wider construction search is justified by this package alone.

Prepared for DLamdata with substantial OpenAI Codex (GPT-6 Astra) assistance, including two separate AI agents for independent mathematical/source checks and skeptical review. Claude Code (Opus 5.5) reviewed the initial published snapshot; its findings and the response are recorded in CLAUDE-RESPONSE.md. This is not independent human review, formal verification, or maintainer acceptance. Predecessor credit and Apache-2.0 licensing are retained.
