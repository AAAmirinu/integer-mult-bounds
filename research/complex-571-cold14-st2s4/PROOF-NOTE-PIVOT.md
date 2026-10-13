# Cost-neutral pivot swaps and four new entering ends (jp8)

Prepared with Claude Code assistance.  Apache-2.0.

## What changes

On the jp8 provider, one new chain step runs between `frame_regroup` and `hyperplane_end`:

```
port_stage x4 -> frame_regroup -> pivot_swap (NEW) -> hyperplane_end -> cold_end
```

`pivot_swap` (recipe `data/recipes/k492-jp8-pivot_swap.json`, code `code/build_pivot_swap.py`) moves the pivot role in
four existing entrance-kernel families:

| old pivot p | new pivot x | entrance E | family gates (part, index) |
|---|---|---|---|
| 488 | 560 | [24] | 5 (4 helper donors 628/630/676/678, plus x) |
| 489 | 561 | [24] | 3 (target donors 123, 187, plus x) |
| 500 | 572 | [24] | 5 (helper donors 640 x2, 688 x2, plus x) |
| 501 | 573 | [24] | 3 (target donors 211, 147, plus x) |

The `cold_end` recipe then ends the four new pivots 560, 561, 572 and 573 at
U24 = [256,128,64,32,24,4,2,1] (dim 8). They form one entering cluster, built with the same ColdSupply
"entering low-frame end" mechanism as the inherited E1 pair 597/599. Everything else in the recipe is #629's h4a
construction: v3 blocks, h4a hyperplane units and the E1 pair. The ck provider is unchanged.

## Family and swap rule

A kernel family on the input word is an entering helper p (`start_extra[p] = E`) together with the gates
`d += c_d * p @E` that read p before any other touch of p.  These are PR568 multicut donor gates; in B, d may also be a
target (a gauge-type donor).

Notation:
- col_g(r) is the response, at the target rows, of a unit of dirt placed in r just before gate g.
- col(r) is r's response from the start of the program **with the family gates deleted**. So col(p) is p's response
  through its own original reads only. p's complete response in the input word, family gates included, is 0.

The family gates cancel it:

    col(p) + sum_d c_d * col_{g_d}(d) = 0                                      (1)

After the swap, the old pivot p is an ordinary cold (non-entering) helper. Its nonzero dirty column is handled like
every other cold helper's: by the frame-zero compensation. The native audit's `compensation_additions` is unchanged at
8868, the same as #629.

The new pivot x must satisfy all of the following:
- x is a helper donor of the family;
- x is not entering;
- x has exactly one family gate g_x, and g_x is x's first touch;
- x has no other touch up to the family's last gate.

The swap is:

    g_x :  x += c_x p        ->  p += (1/c_x) x       (same position, frame E)
    g_d :  d += c_d p        ->  d += (c_d/c_x) x     (d != x; same position, frame E)
    start_extra:  p -> x  (same E);   cleanup := inherited inverse rule (FULL frames, target writes skipped)

All four swaps have c_x = ±1, so every new coefficient is dyadic. The builder asserts this.

## Exactness (zero dirty response of the new pivot)

In the new program, x holds only its initial dirt at every rewritten gate, because x is untouched before g_x and up to
the last family gate. p is read by no gate before g_x: its old family reads now read x, and its first original touch
comes after all family gates. So p holds only its initial dirt up to g_x, and from g_x on the program is unchanged.

Consider the dirt of x in the new program:
- it reaches the targets directly with col(x). Since x is untouched before g_x, this equals col_{g_x}(x).
- through g_d it reaches d with coefficient c_d/c_x. From then on d's suffix response is col_{g_d}(d). This suffix
  is identical in both programs: before g_x neither p nor x carries any of d's data, so the single changed gate at g_x
  acts identically on it.
- through g_x it reaches p with coefficient 1/c_x, and from there it propagates with col_{g_x}(p) = col(p).

The total is

    col(x) + col(p)/c_x + sum_{d != x} (c_d/c_x) col_{g_d}(d)
      = ( c_x col_{g_x}(x) + col(p) + sum_{d != x} c_d col_{g_d}(d) ) / c_x = 0    by (1).

The clean computation is unchanged: helpers hold 0 on clean inputs, so every family gate is a no-op on clean data.
The builder does not rely on this argument. It replays the complete forward program in exact rationals and asserts
that every new pivot's response is {} (`'new pivot dirty response not zero'`). The verifier step then runs the
package's native all-column audit (`hpe_audit_and_transport.py`, exact forward and inverse replay of every input
column plus native frame chains) on the swapped word.

## Cost neutrality

Every rewritten gate keeps its position and frame E, so the frame chains of p and x simply exchange roles:
- before: p starts at E, and x climbs [] -> E at g_x;
- after: x starts at E, and p climbs [] -> E at g_x, its first touch.

No other register's chain changes.
- `gk_word.profile(out) == gk_word.profile(in)` is asserted, and the width multiset is unchanged: one width-8 and one
  width-9 helper exchange labels.
- The verifier asserts `report(out) == report(in)`.

The step therefore adds no paid rank. Its only effect is to make x an entering helper whose end-of-B frame has dim 5,
low enough to end below FULL.

## The four new entering ends (cold_end)

Each new pivot x is an entering helper (E = [24]) with end-of-B frame of dim 5. The ColdSupply census (#604 necessary
condition with premix freedom) finds a feasible end at U24 for each of them, and the four are jointly feasible:
pairing rank 4 in the E = [24] premix group, which has 24 free helpers.

Exact dyadic premix, with r_i·c_j = δ_ij checked exactly:

| h | c | r | external partner (end-of-B dim) |
|---|---|---|---|
| 560 | e560 + 2e628 − 2e630 + e676 − e678 | e560 | 74 (7) |
| 561 | −e561 | −e561 | 383 (7) |
| 572 | −e572 | −e572 | 98 (7) |
| 573 | −e573 | −e573 | 399 (7) |

The sign choice for 561 and 573 (−1 rather than +1) is deliberate. With c = r = +e_h the premix would hold no gate
on these helpers, and the unchanged `cold_end_controls.py` (line 99, `next(...)` over the premix) needs one premix gate
per entering end to mutate. With −1 each gets a single `scale h, −1 @[24]` premix gate. The two signs give equivalent
vectors: r·c = 1, the profile is unchanged, and the scale is rank 0 at the entrance frame.

The construction is ColdThird's `construct4` with one extra `extra` cluster, the same code path as E1. The recipe is
consumed by the unchanged `code/build_cold_end.py`. Per jp8 call, against #629 (and identically against st2 = #629 + #627's two factored ends, on which this package stacks;
the recipe `data/recipes/k492-jp8-cold_end.json.gz` is st2's stack constructor (H4aFinish stack.py with s2.json) re-run on
the swapped words, exactness asserted, reviewed `apply` reproducing the word):
- profile delta {1:+8, 2:−4, 3:+4, 4:−4};
- widths 8→7 ×4: x goes 9→8 at the swap, the old pivot 8→9, and x then 8→7 at its end.

## Verifier and control changes (exhaustive)

1. **New code file `code/build_pivot_swap.py`.** Among the existing code files, only the spot-width rule changes (item 5).
2. **`verify.py`:** a new step function `pivot_swap`, allowlisted in `STEPS`. No other function changes. The step:
   - pins the recipe sha;
   - runs the constructor, which rejects 5 mutants per swap (20 here; pinned as `negative_controls`);
   - runs the native all-column audit;
   - then compares independently. Only the recipe's gates change, and each gate changes exactly from `before` to
     `after` at the same frame. The entrances move exactly p → x. The cleanup equals the inverse rule. The report is
     identical.
3. **SPEC pins, re-discovered for jp8:** the new step, plus `hyperplane_end` and `cold_end` input, recipe and output
   shas, and `word_content_sha256`. `cold_end.negative_controls` rises because the unchanged
   `code/cold_end_controls.py` runs its 6 entering-end mutants for every entering end, and there are now 6 entering ends
   (560, 561, 572, 573, 597, 599) instead of 2: 46 + 24 = 70. The HPE step is unchanged (34 helpers, 21 controls).
4. **Owner map / PLAN:** `data/OWNERS.json.gz` and `data/PLAN.json` are re-solved for the new jp8 widths (four 8→7) by
   the O2 exact-window MIP (dispatch jp8 ×71, ck ×1; warm-started from complex-571-cold14-st2's admitted map; 900 s,
   time limit, relative gap 7.17e-8). The physical auditor checks them as before.
5. **Spot widths (`code/witness.py` `spot_widths`, used in `bind_providers_portable.py`, `audit_allcold.py`,
   `assemble.py`; `assembly_controls.py` `cold_helper_width_swap`).** The global scripts used to assert that the four
   spot helpers have width 8. A pivot swap turns a swapped-out pivot p into an ordinary cold helper, so its width
   becomes 9 (here 264 and 276). The expected spot widths are now derived from the provider's pinned `pivot_swap`
   recipe: 9 at a swapped-out pivot, 8 everywhere else. The recipe sha is checked by `verify.py` before any global
   stage runs. The `cold_helper_width_swap` control now swaps with a width different from the spot's own, so it never
   becomes the identity. For words without `pivot_swap`, the rule and the control are unchanged.

## Negative controls added

Constructor (`PIVOT-SWAP.json`, per swap; each must raise at the pinned substring):

| mutant | pinned reason |
|---|---|
| another family gate's rescaled coefficient has the wrong sign | `new pivot dirty response not zero` |
| wrong pivot coefficient: the new g_x coefficient 1/c_x doubled | `new pivot dirty response not zero` |
| non-family gate (recipe `before` differs from the word gate) | `recipe gate is not the word gate` |
| new pivot replaced by another family donor (a target, or an already entering helper) | `new pivot must be a helper` / `new pivot already entering` |
| wrong entrance frame for the moved entrance | `pivot is not an entering helper at the entrance` |

New-end controls come from the unchanged `cold_end_controls.py`, run for each of 560/561/572/573, each with its
pinned audit reason:
- premix gate dropped;
- premix gate at frame [];
- premix gate moved into the precondition;
- lower-frame gate dropped (the dropped new-end gate);
- end dropped (profile pin);
- end at another hyperplane (the wrong-frame end).

## Search provenance (not used by the verifier)

- `swap2.py` / `batch.py` (scratch/PivotSwap) enumerate every family alternative on the 492 words: 48 in jp8, 38 in
  ck. Every alternative is cost-neutral.
- No alternative creates an HPE candidate. Every helper that could become a pivot keeps ≥ 3 cleanup gates, and HPE
  needs exactly 1.
- The entering-end census finds dim-8 ends only for the 8 short-lived donors 560/561/572/573 (E = [24]) and
  536/537/548/549 (E = [30], the E1 hyperplane).
- The E = [30] ends need the E1 premix to be re-picked; that is follow-up work, not in this package.
