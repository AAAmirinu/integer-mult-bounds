# Ceiling for further scheduling of this frozen word

Keep the partial-own kernel84 local word at all 72 invocations, m=73,
W=7680, deficit 2496, and pending children of rank at most 48. The local
children have total rank mass 492624; the remaining children must therefore
have mass 65520.

For every b>0 and every remaining child rank r≤48,

`r (73/r)^b ≥ r (73/48)^b`.

Consequently their total contribution to the normalized moment is at least
that of 1365 rank-48 children. Their number is also at least 1365, so the
bad-cover fallback charged per child cannot be smaller than in that ideal
profile. The local children are fixed. Thus the full moment of any allowed
allocation is at least the moment of the fixed local profile plus 1365
rank-48 children. This holds for every invocation order and whole-owner map
within the stated architecture, without assuming any optimizer found an
optimum. The ideal profile need not be physically attainable.

Both independent exact rational moment engines give a value strictly above
one at

`b = 0.001448157050078593686264`.

The moment is increasing with b. Therefore every admitted construction under
these fixed assumptions has b strictly below that endpoint. The current
candidate is within 4.19% of this deliberately generous bound. The retained
outer assembly also has κ < b/(1+b), as recorded exactly in the receipt.

This does not bound a changed local word, different dimensions/stocks, merged
or shared child computations, a different recursion, or another multiplication
algorithm. In particular it is not an impossibility result for κ=1. It shows
that scheduling this same local word cannot reach that goal.
