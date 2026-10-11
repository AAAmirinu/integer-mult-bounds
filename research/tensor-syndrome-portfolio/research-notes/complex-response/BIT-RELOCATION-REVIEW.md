# Independent mathematical review of the successful bit relocation

Source inspected: kernel_codes/retime_constructor.py and RETIME-AUDIT-11.json.
This is a source-level mathematical review, not an independent native/global replay.

Let A_i be helper shears, let the source vector x be immutable throughout A, and let P select the final target output after the cut and B. At a cut c and destination d define R(c,d) as the complete downstream response to adding one unit to helper d at that cut. Suppose the original program injects x_s into helper d at cut c. Delete this injection and instead inject x_s into helper e at cut c'. If R(c,d)=R(c',e), the new target map equals the old one on every source and dirty-helper input.

Proof: both additions read the same immutable x_s. Neither change can alter the operand of the other injection. The target difference is therefore exactly x_s(R(c',e)-R(c,d)), with no higher-order cross term. Changing the cleanup to the literal inverse of the new helper word restores every dirty helper and leaves sources unchanged. The target dirty compensation remains equal if the two complete target maps agree, although a final all-column check should still enforce the actual emitted convention.

The constructor enforces this key restriction explicitly: every A destination is at least 2v, both old and new injections read the same singleton source below v, and every B destination is a target. It computes responses through the whole actual B, scatter and suffix A, not through only a local module. The nonzero-response condition makes the deletion-only/insertion-only controls meaningful.

The emitted relocation changes the paid child multiset by removing ranks1 and3 and adding rank4, without changing total rank mass. For 0<b<1, put p=1-b in (0,1). Strict subadditivity gives 4^p<1^p+3^p. Therefore the recurrence moment strictly decreases at every admissible positive b (after multiplication by m^-p), provided the physical construction realizes the claimed profile. This is an exact sufficient improvement, not an entropy approximation. It survives composition with a hosting assignment only after source-bound provider selection, actual owner slots, paid complements, and the whole emitted profile are checked.

The accompanying finite exact audit covers955 scalar columns, rational frame ranks, monotonicity and integer operand spans. The independent native checker, phase/owner contracts, finite invoice and two rational moment engines remain distinct final release checks; this review does not replace them.
