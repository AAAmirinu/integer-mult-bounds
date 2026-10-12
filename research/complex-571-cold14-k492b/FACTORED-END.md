# One factored extra cold end on PR623

## Exact change and inherited interfaces

The pinned base is PR623 `e39a615ca601ce5d62abeb24f3fcdb8644ca1005`. The jp8 word keeps 492 helpers, all entrances, all old ends, every cut, all target levels and all scalar B gates. The ck supplier and the dispatch jp8 ×64 / ck ×8 are unchanged. The new helper is raw register **590**, helper index **366**, initially cold. Its terminal frame is the reduced binary basis **[266,138,72,40,24,6,1]**, dimension 7. The supplier gains its 23rd cold low-frame end.

The new A prefix consists of the ten exact rank-zero additions in `data/FACTORED-END.json`. It includes a dual-row basis correction needed to transfer the candidate from PR617's factory basis to PR622's K-triangle basis. The ten operations intentionally retain that derivation, including two canceling pairs; their frame is empty, so this redundancy adds no paid rank. All operands are cold helpers. These gates run after the entry adapters and paid residual wrappers, exactly as in the inherited cold-end construction.

After input-HPE A gate 1800, insert `q87 += (1/2) S419` at frame **[408,73,49,6]**. Both operands already have that frame, and q87 is untouched by the remaining A, cut and B program. Thus the insertion is free in the paid profile and changes no live forward computation. The inherited constructor independently checks these conditions. The final A position differs because the cold premix and preceding insertions are included; the metadata records actual positions for the mutation controls.

After every inherited early cleanup gate, append:

1. `q80 += q84` at `[408,73,49,6]`;
2. `q80 += q87` at the same frame;
3. `S590 += (1/2) q80` at `[266,138,72,40,24,6,1]`.

The first two additions form the necessary linear combination before its accumulator climbs. The naive separate reads at dimension 7 were more expensive; this factorization is the new useful step.

## Scalar identity and cleanup

The generator computes the exact rational forward matrix after A, cut, B and the entire early tail. It checks that every ended helper has its identity row and that its column is zero in all other non-target rows. The new helper's target dirt is also checked by the independent native auditor, including post-wrapper compensation rules.

It then performs exact Gauss-Jordan elimination on the remaining non-target, non-ended registers only. Every pivot must be a signed dyadic unit; all scales are therefore allowed dyadic units. No FULL remainder gate touches an ended helper or a target. This is an exact refactorization of cleanup, not an assumed inverse: the unchanged native auditor replays every arbitrary input column in both orientations, checks all frame chains, the row/column cone conditions, endpoint identity and paid profile.

`tools/build_factored_end.py` checks that its complete output exactly equals the unchanged `build_cold_end.py` applied to the new declarative recipe. The existing constructor also checks the rank-zero prefix, dead-port absorption, preservation of inherited HPE ends and actual width inventory. The existing raw-word controls, reflected program checks, residual wrappers and exact phase checks remain admission requirements. Their implementation is unchanged.

## Cost and global ownership

Per jp8 call, the paid profile changes by **{1:+1,2:+1,5:−1}**, with rank mass −2, exactly matching the helper's width reduction 9→7. The factored accumulator merges the required lower-frame arithmetic before its climb; the intermediate rank-3 terms cancel in the before/after profile comparison. The new residual wrapper is the inherited exact `(E=0,U=dimension 7)` interface, checked with phase by the unchanged wrapper machinery.

Across 64 jp8 calls this frees 128 units of owner capacity. The submitted owner map is a feasible simultaneous repacking: 15,454 placements differ from PR623, and exactly 64 width fields change, all on helper index 366 at jp8 calls. The independent physical auditor checks every helper, time window, family, capacity, interval and residual frame. Live 7,168, physical 7,670, 35,424 hosted roles, rank mass 520,704 and deficit 2,560 remain unchanged. Both exact moment engines, strict outer inequalities and the conservative calculation determine the κ printed in SPEC/EXPECTED.

No gains from the supplier and packing searches are added numerically: the whole combined profile is invoiced and certified afresh. The cited PR543 bit supplier is repriced, not rebuilt. All-size compiler, common-label/mutable-source realization, whole-call hosting, precision/tape/exact recovery, analytic transfer and bit H1–H5 assumptions remain.

## Deterministic construction and map reproduction

First independently replay pinned PR623 using its documented sources. Then:

```sh
python3 -B research/complex-571-cold14-k492b/tools/build_factored_end.py \
  --base-word /path/to/pr623-replay/jp8-step6-cold_end/FULL-WORD.json.gz \
  --base-hpe /path/to/pr623-replay/jp8-step5-hyperplane_end/FULL-WORD.json.gz \
  --base-recipe /path/to/pr623/research/complex-571-cold14-k492b/data/recipes/k492-jp8-cold_end.json.gz \
  --out /tmp/factored-end-rebuilt
python3 -B research/complex-571-cold14-k492b/tools/replay_owner_map.py \
  --base-data /path/to/pr623/research/complex-571-cold14-k492b/data \
  --out /tmp/factored-owner-map
```

Compare the rebuilt recipe and owner payload with the package. The map exporter uses the submitted PLAN's provider bindings; it does not replace the independent supplier checks. Both exporters reject optimized Python before creating output. The official verifier uses only the declarative recipe and owner map, not these generators or the search heuristics.

## Full fresh verification

Use the inherited immutable source pins (all unchanged): PR568 `71c99ac935a33bb7b59a1b4a7af8725a939b0b90`, PR571 `b7bdc5a8de18fcf418cfb9c7d83a2b1097a5e4a3`, PR569 `897213a855b7fb8a1b8b0e552a2f5c42e6c1b326`, PR575 `eac6f7e378ab622dac50a2fd4b7ef6eab014de44`, PR583 `89be768f0157f5a3d8e4db69cf1748768605eac9`, and direct-delivery manifest `c1997405c5c0ccd9bdb0a30b0eb9a5a2dc7dc7ce7b59c6a83a2152b80f6410d1`.

```sh
python3 -B research/complex-571-cold14-k492b/verify.py --jobs 2 \
  --work /tmp/factored-end-fresh \
  --source multicold=/path/to/pr568/research/complex-multicold \
  --source structural_gain=/path/to/pr571/research/structural-gain \
  --source larger_gain=/path/to/pr569/research/larger-gain \
  --source joint_prefix=/path/to/pr575/research/complex-joint-prefix \
  --source frame_coalescing=/path/to/pr583/research/kernel-frame-coalescing \
  --source direct_delivery=/path/to/direct-delivery504-global
```

## Discovery and limits

Earlier exact row/column capacity screens found no extra end within the restricted fixed-circuit frames tested. Allowing free dead-port absorptions yielded 156 algebraic leads; naive tails were all locally more expensive. Factoring their cleanup yielded 24 locally beneficial variants, on four helper identities. One independently audited variant was transferred to the current K492 construction, with its dual row corrected in the new factory basis. Its unchanged constructor, native and phase admission preceded owner search.

A width-adjusted PR623 map, our earlier small packing improvement, greedy consolidation and five million one-/two-role swap trials (seed 0, temperature 1) produced this submitted map. A 300-second restricted pattern solve did not improve it. These are search procedures, not proofs of optimality. Exploratory two-helper and larger schedules are not included in this claim. Construction credit remains with all predecessors in NOTICE; the factored extra end, generator, repacking and contributor validation were prepared by Jeremy Diviney with OpenAI Codex assistance.
