# Strict witness and the retained family's grid ceiling

Let b=999632926176283/10^18, c=251726760077483/250000000000000000, and a0=384599/10^10. Set beta=eta=10^-18 and s=(1-beta)b-10^-24. Exact rational comparison gives 0<s<c and s<(1-beta)b<b<1/32.

Retain the same three rounds a[j+1]=F_s(a[j]), where F_s(x)=s(1-s+x). They increase from a0 and remain below s. The pinned outer assembly sets q=a3(1-2 eta), epsilon=(1-eta)/(1+q), and its minimum performance margin is M=epsilon q. All 47 strict inequalities are checked in exact arithmetic, including the leaf gap, reservations, geometry, seven performance margins, and finite/row guards. No constraint is removed or relaxed.

The emitted kappa is the greatest 10^-18 multiple strictly below M. Four controls reject the next grid point, zero eta, zero beta, and unit beta.

For any allowed positive beta and backoff, s<b. F_s(x) is increasing in x since its x derivative is s>0; it is increasing in s on this domain since 1-2s+x>0 for x>=0 and s<1/32. By induction, any such three-round chain is bounded above by A=F_b(F_b(F_b(a0))). Positive eta gives q<a3, and epsilon q<q/(1+q)<A/(1+A). Exact comparison in the verifier proves

`kappa < M < A/(1+A) < kappa+10^-18`.

Thus no different positive slack choice in this retained three-round family reaches the next grid point. This is not an upper bound for more bootstrap rounds or a different assembly. The suppliers' mathematical interfaces and open obligations remain exactly those stated in #384.
