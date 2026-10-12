# Exact E6 correction to the PR620 ADE screen

**Research correction; no new κ or supplier claim.** The archived
[`ade_screen.py`](../e8-decoder-floors-and-cold14-notes/ade_screen.py) labels
an orthogonal-pair complement in E8 as E6. It actually constructs D6.
This standalone companion preserves the archived submission and provides
the corrected exceptional-root census with exact arithmetic and no dependencies.

## Reproduce

Python 3.9 or newer and its standard library suffice, from any working directory:

```sh
python3 -B research/exact-ade-census/test_census.py
python3 -B research/exact-ade-census/census.py --check research/exact-ade-census/RESULTS.json
python3 -B -I -O research/exact-ade-census/census.py --check research/exact-ade-census/RESULTS.json
```

The paths above assume the repository root; use absolute paths elsewhere.
Without `--check`, the census prints deterministic JSON. The tests reject an
incomplete root set, a repeated root line and a zero root, and distinguish
rational rank from characteristic-two rank. Production validation uses explicit
exceptions and remains active under optimized Python.

## The error and its geometric certificate

Normalize roots to squared norm two. Let

```
a = (1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2, 1/2).
```

The archived function first restricts E8 roots to `a.perp`, then selects a
second root `b` **orthogonal** to `a` and restricts again. Its deterministic
choice is `b = e1 - e2`. These two roots span A1 + A1, whose complement here
has 30 root lines. Its computed simple-root Gram matrix has determinant 4
and a trivalent Dynkin tree with arm lengths 1, 1, 3: type D6.

For E6 use `b = e1 + e2` instead, with `a.b = 1`. Now `a` and `-b` have
Gram matrix `[[2,-1],[-1,2]]`, so they span A2. Their common orthogonal
root set has 36 lines. Its simple-root Gram matrix has determinant 3 and
arm lengths 1, 2, 2: type E6. Both explicit Gram matrices and the doubled
simple-root coordinates are retained in [RESULTS.json](RESULTS.json).

The verifier builds the 120 E8 lines as the 56 lines `e_i ± e_j` and the
64 sign classes of half-integral roots with an even number of minus signs.
All coordinates are doubled integers. It checks root norms, integral
pairings and reflection closure for **every ordered pair** in each of the
four root sets (20,565 pairs in total). Lexicographic positive roots that
cannot be decomposed into two positive roots supply the simple roots;
exact elimination checks that they form a basis. The resulting Dynkin
trees identify the types independently of the root-set labels.

For classical background, SageMath's
[type-E root-system documentation](https://doc.sagemath.org/html/en/reference/combinat/sage/combinat/root_system/type_E.html)
records the Bourbaki-based E6/E7/E8 construction. The finite checks here
are implemented independently and do not require SageMath.

## Corrected screen and its limits

For the norm-two Gram matrix `G`, let `c = rank_F2(J + G)` and retain
PR620's **full-rank-totals proxy** `x = c*h/v`:

| Unit | Root lines v | Rational dimension h | Binary rank c | Proxy x |
|---|---:|---:|---:|---:|
| D6 (archived “E6”) | 30 | 6 | 5 | 1 |
| E6 (corrected) | 36 | 6 | 7 | 7/6 |
| E7 | 63 | 7 | 7 | 7/9 |
| E8 | 120 | 8 | 9 | 3/5 |

Under this proxy the per-port deficit is `D_s = (s-1) - s*x`.
Corrected E6 gives `D_s = -1 - s/6 < 0` at every positive stage count,
while the archived D6 row gives `D_s = -1`. Thus this correction preserves
the lack of positive deficit for that E6 screen, with the right geometry.
The binary rank is the rank of **this particular matrix**, not a minimum
over all fitting matrices. Charging every total the full ambient rank is
a cost premise, not a universal lower bound on all decoder circuits.
Nothing here excludes E6 constructions using other decoders, lower-rank
reader supports, different labels, helper schedules or cost models.

No SAT infeasibility claim from PR620 is certified by this package. The
production E8 suppliers, selected exponent and historic review receipts
are untouched; no full multiplication theorem is proved.

## Provenance and attribution

The issue was found while reviewing
[PR620](https://github.com/CrocSwap/integer-mult-bounds/pull/620) at the
repository snapshot `17ce0c79b7b51c2634b439ea5a2b754f09909693`.
The preserved script's SHA256 is
`3c5da517f02752e67ef315792f656bf6fbd5e9026090d755761d0bf39efd2d82`.
Its as-run E6 selection can be recognized directly at `E6()`; the companion
does not rewrite it or replace the source bytes covered by the review archive.

The original ADE screen and research direction are credited to Joel Pulikkan
/ GamingPuzzled, with the Claude Opus 5.5 assistance disclosed in that package.
The proxy accounting follows DreamingOfClouds' PR595 format analysis and its
PR446 premises, with their original notices retained. This correction,
independent exact census and regression checks were prepared for Chi Zhao
with substantial OpenAI Codex assistance. Apache-2.0, following the repository.
