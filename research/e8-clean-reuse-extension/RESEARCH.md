# Extension research record

The requested target is conditional kappa > 0.002. The design deadline is
21:00 JST and PR completion deadline 22:00 JST on 2026-10-11. Effort is split
between integrating existing results and independent structural experiments.
The validated value in EXPECTED.json is below that target.

Integration work pins PR376's R781 supplier and frame repairs, PR390's
prefix identity and PR395's signed extension, then replays the changed full
physical supplier. In parallel, the new stream investigates helper elimination,
clean-reset reuse, shared prefix donors, altered frame directions, center
readouts and use of retired intermediate aggregates. A screen is not an
admitted supplier and is not counted as an achieved exponent.

The successful new mechanisms are the two complex two-donor substitutions
and 27 bit clean-reset reuses. Their fixed witnesses and mathematical controls
are reproduced by construct.py; the full admission follows in verify.py.

Bounded private screens at the frozen R779 baseline found:

| Screen | Outcome and limit |
|---|---|
| Shared signed prefix donors, coefficients +/-1 and +/-2 | 532 legal trials, 49 positive edges; 32 deterministic selections returned 25 distinct donors, with no extra gain over the signed selection. |
| Complex adaptive clean readouts with one or two donors | 13,482 pair screens yielded no additional helper removable under the unchanged frame guards. |
| Early clean-zero restoration | Six rank-eight sinks from 62,490 pair screens; no arbitrary-dirt, bank or phase admission, so no gain included. |
| Recycle totals from retired phase-A aggregates | 39 available donors of rank 34 represented none of the eight missing center increments; no candidate admitted. |
| Generalized B_K pair count | Numerical profiles for K=2 through 30, with whole-bank padding charged, did not improve the selected complex K=4. Changed profiles have no physical admission. |

These are bounded discovery observations, not global impossibility or priority
claims. The implementation submitted here contains the successful construction
and its complete verification. Further structural ideas remain research work.
Original author credit is preserved in NOTICE.md and SOURCE-PINS.json.
