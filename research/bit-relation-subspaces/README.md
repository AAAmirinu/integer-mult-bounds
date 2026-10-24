# No further BIT helper relation subspace after #5421

**Negative result; no new κ and no new BIT saving.**

[PR #5421](https://github.com/CrocSwap/integer-mult-bounds/pull/5421) (Ali Romman) owns nine helper
relations on the reverse PR589 BIT word. Each relation zeroes one COPY job (rank 7) and one rank-1 move,
and costs one rank-8 helper target. Its README says that a further BIT gain needs a new relation space.
[PR #5428](https://github.com/CrocSwap/integer-mult-bounds/pull/5428) (target 6) proposes systematic
relation-space selection for the same purpose.

This package answers the question exactly for that word. Any number of additional relations, in any
combination, removes at most 7.5 units of paid rank mass per relation dimension. A dimension costs one
rank-8 target. Every relation subspace therefore loses at least `8^t - 7.5 = 0.4424` raw moment per
local call at `C = 0.00347207`. The bound holds for every `C < 0.031`.

## Model

The model is #5421's. Replay the source records in reverse over GF(2) with 661 entry symbols. A paid job
is a MOVE of rank `r > 0` or a COPY entrance (rank 7). A relation subspace `V` consists of entry forms
supported on full-entrance fields, with helper pivots. A job becomes free exactly when the binary row of
its moved value lies in `V`. The raw moment changes per local call by

```text
sum over removed jobs of r^t  -  8^t dim V,      t = 1 - C,
```

and the controller multiplies this by its eighteen full calls. The certificate ignores the frame and pivot
conditions, so it bounds legal subspaces as well.

## Certificate

Let `E'` be the multiset of job rows, with each row repeated `rank` times, and let `w(V)` be the paid mass
with rows in `V`. By the matroid union theorem, if `m` copies of `E'` split into `p` linearly independent
sets, then `m w(V) <= p dim V` for every subspace `V`. Edmonds' augmenting paths make the split exact.
A row in a tight subspace (`w = 8 dim`) is one for which an extra copy cannot be inserted.

| Check | Result |
|---|---|
| Source paid jobs / jobs with a legal row | 2,920 / 2,384 (1,773 distinct rows) |
| Source word, `E'` into 8 sets | splits, so `max_V (w - 8 dim) = 0` |
| Source word, tight subspaces | exactly nine, each COPY H7 + MOVE H1: the #5421 relations |
| Modulo those nine, `E'` into 8 sets | splits; no tight row, so `w(V) < 8 dim V` |
| Modulo those nine, `2E'` into 15 sets | splits, so `w(V) <= 7.5 dim V` for all `V` |
| Control: source `2E'` into 15 sets | fails, as required |
| Control: extra rank-1 job on a COPY row | breaks the 8-split, as required |

Since `r^t <= r` for `r >= 1`, the moment change is at most `(7.5 - 8^t) dim V < 0`.
[RESULT.json](RESULT.json) holds the rebuilt numbers.

## Reproduce

```sh
python3.12 -B scripts/research_package.py --package research/bit-relation-subspaces
python3.12 -I -B research/bit-relation-subspaces/verify.py
python3.12 -I -B research/bit-relation-subspaces/test_verify.py
```

The verifier uses only the standard library and finishes in about half a minute. It prints
`PASS_BIT_RELATION_SUBSPACES_NO_FURTHER_GAIN_AFTER_5421`. The controls print
`PASS_BIT_RELATION_SUBSPACES_CONTROLS`.

## Scope

The result fixes the PR589 operation order, helper inventory and job set. It does not cover a changed
chronology, a different BIT word or new helpers. Snapshot replacement in the style of PR #5377 applies
only to owned fields. On this word the only owned paid jobs are the nine COPY jobs, which #5421 already
removes. The nine relations come from the source word itself, so #5421 is not a live input.

## Open next questions

- Does a changed chronological order or a different BIT word admit a relation subspace of density
  above `8^t`? First run the same 8- and 15-part splits on its job rows. No frozen changed BIT word with an
  admitted invoice is available yet.
- Does the same certificate close relation subspaces on the selected complex word, which is the binding
  side? Complex relation searches so far tested single relations. A subspace of density above `9^t` there
  would raise κ directly. The partition must run over Q with rank-9 targets.

## Credit

DreamingOfClouds (PR #589) and eumemic (PR #555) supplied the source word and port construction.
Ali Romman's PR #5421 and PR #5383 supplied the owned-helper relation method that this package
generalises. zxv's PR #5428 named relation-space selection as a target. Prepared by Mark (Matarener)
with substantial Claude Code assistance. New work is Apache-2.0.
