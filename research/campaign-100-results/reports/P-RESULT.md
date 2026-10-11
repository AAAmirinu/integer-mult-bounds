# P-compose: composing the campaign's base-word gains with the p10b stage stack — RESULT

Stopped on the coordinator's order (2026-10-10 ~20:25 EDT): PR #346 (LJH-217, κ 7.9258e-4) made the complex side
binding with the bit root 1.07% above the cap, so every bit-side package is now worth zero. No PR was opened, no
commit was made (a clean worktree `/private/tmp/imbwork/wcomp` on branch `p10b-composed-clean` = origin/main +
cherry-pick of joint-dual-repin `a45747d` exists, with nothing added). All 30 Daytona sandboxes of this task were
deleted (registry `/tmp/r338/dt/registry.json`, every entry `deleted: true`). Work state is under `/tmp/r338`.

## Pricing tool (exact, reproduces the packages)

`/tmp/r338/tools/pricelib.py` prices any word/pickle with the p10b package formula of `code/price.py` (300 replicas,
idle 115200 at ranks 4/19/38/42, stock = 230400 + 3·residual, PR327 supplier b = 779597612622781/10^18, 47 outer
constraints with `--full`). It reproduces #337's native κ `155529226266457/2e17` from `/tmp/r337/final.pkl`, #337's
`base_kappa` 7.70652338831057e-4 from its parity word, and #341/#342's base κ. `stackprice.py` prices a discovery
package (#320's transcript-stage package with a predecessor's bit word installed, `make_disc.py`) after each stage.

## 1. Campaign base-word levers on the oriented (#337) source — all dead

Parity-word κ on #337's source (base 7.70652339e-4), each variant regenerated with #337's two-pass
`regenerate_structural.py` flow and a fresh carrier matching (`tools/regen_install.py`, `tools/patch_producer.py`):

| variant | κ (parity word) | vs #337 base |
|---|---|---|
| A: design-list reorder (C's top1_transposition, [G,1,2,0] first) | 7.70866357e-4 | +0.0278% |
| B: reorder + PLAIN = 12 | 7.70826663e-4 | +0.0226% (PLAIN 12 loses 0.005%) |
| D: reorder + κ-exact min-cost carrier matching | 7.70893986e-4 | +0.0314% |
| C: reorder + PLAIN 12 + min-cost | 7.70854290e-4 | +0.0262% |
| E/F: C's top2 / top1 orders + min-cost | 7.70893986e-4 | identical plateau |
| G: min-cost matching alone (no reorder) | 7.70656873e-4 | +0.0006% |
| H: min-cost matching on #341's source | 7.70748574e-4 | −0.0033% vs #341 (its 40 hand carrier switches are better) |

So on the oriented source the reorder is worth +0.028% (not +0.063%), PLAIN 12 loses, and the min-cost matching is
≈ 0 (its +0.0036% on D was an interaction with the reorder). Worse, **the G-first reorder destroys the kernel stage**:
with the same pools (26,935 lines, 7,615 subspaces, identical first-frame dims) chafreaky's closure packing finds only
957 entries / φ −1562 on D's word against 1241 entries / φ −2268 on #337's word — and the packer is not at fault: on
#337's own post-target word it reproduces #337's frozen kernel exactly (φ −2267.864, 1241 entries, rank 1245, every
seed identical; rigid landscape). Stack prices: #337 word parity 7.70652e-4 → post-kernel 7.75575e-4; D word parity
7.70894e-4 → post-kernel 7.74780e-4 (−0.10%). The predecessor for D was fully re-pinned (`/tmp/r338/predD`, repin
PASS, κ pin 154178797260407/2e17, regenerate_structural byte-exact) but is useless downstream.

## 2. The real lever: plane creation order scored THROUGH the kernel (Daytona, 30 sandboxes)

Job (`/tmp/r338/dt/bundle/job.sh`): on #342's source (the leader at the time, κ 7.77733997e-4, base 7.70747e-4), for
each candidate design-list order: patch `local_design_p10.json`, two-pass regeneration with fresh Hopcroft–Karp
matching, #320's `descent_search.py` + `target_search.py`, `dump_at`/census/lines(5)/planes(15), sink prescreen
(`tools/prescreen_sinks.py`, excluded from packing), closure packing NOISE 5 (K's `run_pack.py`, 150 s), kernel
freeze, price after descent/target/kernel. 62 candidates queued (original, C's transposition, each plane moved to
front, each plane moved to end, 36 random orders, 2 min-cost variants); 37 scored before the stop
(`/tmp/radical/P/order-search/*.json`). Reference: #342's own stages post-kernel κ = 7.756703286e-4.

| candidate | post-kernel κ | vs #342 | parity κ | kernel φ | entries |
|---|---|---|---|---|---|
| **m09_front** ([A,2,0] created first) | **7.760759188e-4** | **+0.0523%** | 7.704776e-4 | −2727.6 | 1366 |
| **e06_end** ([G,0,1,0] created last) | **7.760510565e-4** | **+0.0491%** | 7.707060e-4 | −2553.4 | 1241 |
| **e07_end** ([G,0,1,1] created last) | 7.760510565e-4 | +0.0491% | 7.707060e-4 | −2553.4 | 1241 |
| m08_front ([A,2,1] first) | 7.758533e-4 | +0.0236% | 7.702583e-4 | −2727.6 | 1366 |
| m07/m06_front ([G,0,1,*] first) | 7.75741e-4 / 7.75735e-4 | +0.009% | 7.70818e-4 | −2267.7 | 1240 |
| c00_orig (HK re-solve, #342's order) | 7.756277e-4 | −0.0055% (= value of #342's hand carrier switches) | 7.707060e-4 | −2267.7 | 1240 |
| j00_orig (min-cost matching) | 7.756440e-4 | −0.0034% | 7.707220e-4 | −2267.7 | 1240 |
| every G-first order (C's plateau) | 7.7480…7.7504e-4 | −0.08…−0.11% | 7.7092e-4 | −1559…−1718 | 956–979 |
| other random orders | 7.7396…7.7576e-4 | −0.22…+0.011% | | | |

The kernel φ depends almost only on which plane is created first/last (the A-2-0-first family all share φ −2727.6 and
1366 entries; the G-0-1-*-last family φ −2553.4), the parity price on the rest of the order; the two are nearly
separable, so untested combinations (e.g. [A,2,0] first AND [G,0,1,0] last) are the obvious next candidates.

## 3. Full build on e06_end (K) — state at the stop

`/tmp/r338/predK` = #342's predecessor with the e06_end order, fresh HK arcs, re-pinned (repin PASS, 39 pins, κ pin
770705955529293/1e18, bit root 48206275105043/6.25e16), README/NOTICE/STRUCTURAL-PROVENANCE updated, MANIFEST refreshed.
`/tmp/r338/discK` = discovery package with descent (480 gates, φ −637.17), target (120 groups), kernel (1241 entries,
rank 1245, φ −2553.429, sharing {1:55, 2:80, 3:118, 4:85, 5:217, 6:186}), sinks prescreen 16 roles.
`/tmp/r338/pkgK` = #342's package with vendor/predecessor = predK and the three frozen stages; `materialize_record.py`
(record-mode materialize) produced the fresh restore (240), sink (16 removed, R 8084), reorder (124 moves) selections
in `pkgK/stages/` and `/tmp/r338/mK/post_reorder.pkl` (raw sha eb6f8f2d…, 328480 ADDs, 47612 paid calls, 378226
records).

Exact prices with the PR327 supplier (bit binds everywhere): parity 7.70705956e-4 → descent 7.71636813e-4 → target
7.72304129e-4 → kernel 7.76051057e-4 → **post-reorder κ = 7.7807554265037e-4** (bit root 7.78681416e-4, stock
653385, residual 140995), i.e. **+0.0439% over #342's final (7.77733997e-4) and +0.0165% over #344's (7.77947425e-4)
before the final retiming**. Not done: descent2 (exact CP-SAT / free-form, expected ≈ +1.6e-8), #344's cache
stage, SOURCE/MANIFEST/docs, verify.py, PR. The m09_front build (L) was killed during its stage prep.

## Verdict

The campaign's parity-level base-word gains (reorder, PLAIN, matching) do not survive the stage stack on the
oriented sources — the design-list order must be scored through the kernel, where it is worth up to +0.05%
(m09_front/e06_end on #342's source), with a post-reorder word at 7.78076e-4 that would have led the bit-side board.
Moot after #346 made the complex side binding; left here for the record. Nothing was pushed or opened.

Files: `/tmp/r338/tools/*` (pricelib, patch_producer, regen_install, make_disc, run_stages.sh, prescreen_sinks,
stackprice, materialize_record, build.sh), `/tmp/r338/dt/*` (bundle, cands, launch/poll/fixjob, results),
`/tmp/r338/{predD,predK,discK,pkgK,mK}`, logs `/tmp/r338/*.log`.
