# Fixed-word whole-owner packing ceiling

The exact certificate rejects b = 0.0013911431 for every whole-helper packing
that retains this 84-pivot local word, 72 complete invocations, m=73, W=7680,
the original idle-child stock, and one paid remainder per original idle child.
The retained outer composition consequently has
κ < 0.001389210509385420986354238107500992935434721242043707466459616223462083.
This is less than 0.0062% above the exhibited κ = 0.001389125582984265.

The restriction to the local word matters: PR514 subsequently reports a different
92-pivot word above this bound. This certificate says nothing against that change,
other local circuits, split-child interfaces, or other multiplication algorithms.

## Optimistic relaxation

There are 3,840 idle children each of ranks 16, 32, 48 and 5,760 of rank 8. All 72 calls
require 396 helpers of width 9, 146 of width 8 and 18 of width 7. Drop every time-window,
per-invocation collision, coordinate-chart and ordering restriction. A pattern
for one rank-r idle child is any nonnegative integer tuple p=(p7,p8,p9) with
7p7+8p8+9p9<=r. Its paid remainder has rank l=r-7p7-8p8-9p9. Exhaustive enumeration
gives 112 patterns. Every admitted whole-helper owner map induces a feasible
nonnegative count of these patterns, even though many feasible patterns cannot
be realized in a physical controller.

For b>0 define C(l)=l(73/l)^b + (32*73^2/10^16)*73^b when l>0 and C(0)=0.
This includes the inherited fallback cost once per nonzero remainder.
Set c(l)=C(l)-l. The total remainder rank is the invariant 64,944. Let lambda_w
and eta_r be the published rational dual coefficients. The checker independently
regenerates every pattern and proves, using rational lower bounds from BOTH
moment engines,

    eta_r + sum_w p_w lambda_w <= c(l).

Multiply by the nonnegative number of each pattern and add. The total remainder
cost is at least 64,944 + sum_r stock_r eta_r + sum_w (72*count_w)lambda_w.
Add the fixed local cost (including its count-linear fallback) and divide by
73*7680. Both independent interval engines give a strictly positive margin above 1
at the published rejected b. All terms are increasing in b, so larger rates are
also rejected. The retained strict outer constraints imply κ<b/(1+b).

`check_packing_ceiling.py` performs only exact rational calculations and uses no
optimizer. `packing_ceiling.py` is the discovery procedure: floating LP output
only nominated width dual coefficients; rank dual coefficients were repaired by
an exact minimum over every pattern. Solver optimality is never an acceptance
premise. The checker rejects five deliberate certificate corruptions.

After the main package completes, run:

```sh
python3.14 -B check_packing_ceiling.py   /path/to/fresh-output/coordinated/gauge80-kernel42   PACKING-CEILING.json /absolute/new/check-result.json
```

The weaker rank-only ideal ceiling is retained for comparison. Source hashes in
the certificate bind the actual local programs' paid profile and owner stock.
