# Architecture prototype results

The second [100-architecture plan](../plans/ARCHITECTURES-100.md) is a distinct proposal list. 
Only the surviving runs below and the decoder screens are evidenced here; it is not 100 completed architecture tests.

These are experimental compiler/pricing outputs. A positive prototype price is not a complete admitted certificate.
Failures retain the original null kappa and error; the accompanying numeric zero is not a certified exponent.

| Run | Family | h | Ports | Deficit | Reported kappa / failure |
|---|---|---:|---:|---:|---|
| [pc10](result_pc10.json) | paired_cube | 20 | 960 | 2040 | 384842019691667/500000000000000000 |
| [pc6](result_pc6.json) | paired_cube | 12 | 160 | 40 | 133611920469539/1000000000000000000 |
| [pc6_chi2](result_pc6_chi2.json) | paired_cube_variant | 12 | 160 | 40 | 133611920469539/1000000000000000000 |
| [pc6_nomix](result_pc6_nomix.json) | paired_cube_variant | 12 | 160 | 40 | 2038613116129/15625000000000000 |
| [pc6_support](result_pc6_support.json) | paired_cube_variant | 12 | 160 | 40 | 133611920469539/1000000000000000000 |
| [pc7](result_pc7.json) | paired_cube | 14 | 280 | 280 | 94107852646903/200000000000000000 |
| [sx12](result_sx12.json) | simplex3 | 12 | 220 | 220 | 281544208256109/1000000000000000000 |
| [sx14](result_sx14.json) | simplex3 | 14 | 364 | 546 | 367124313373059/1000000000000000000 |
| [tri_all](result_tri_all.json) | triples_all | 7 | 35 | -70 | AssertionError('no positive root: deficit -70, maxchild 16, m 35') |
| [tri_steiner](result_tri_steiner.json) | triples_steiner | 7 | 7 | -77 | AssertionError('no positive root: deficit -77, maxchild 16, m 35') |

The [decoder screen](decoders_p567.log) records infeasible candidates as well as successful baseline checks.
At p=7, pair-union centres deliver 0/280 targets despite an attractive formal deficit; half-stars deliver 64/280;
no-centre and pair-avoider candidates fail. The Walsh H8 reduction has F2 rank 1 rather than 8.
These are finite feasibility screens, not general impossibility theorems.

[Earlier p=5/6 log](decoders_p5_p6.log) and [screen implementation](decoders.py) are also retained.
The generic compiler specification is preserved as [historical source material](ARCH-SPEC.md).
