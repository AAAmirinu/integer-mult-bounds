# Two-layer target interval substitution

All inherited compiler and hosting interfaces remain conditional. The finite transformation below is explicit and sufficient for replacing the local word under those interfaces.

## Exact binary identity

Let a receiver u and donor d hold arbitrary values. At the interval entrance replace u by u+d. If the original receiver increment over the interval is A and donor increment is B, replace the receiver increment by A+B, cancelling repeated binary terms. At exit add the donor again. The final receiver is

    (u+d) + (A+B) + (d+B) = u+A.

The donor and all other registers have their original endpoints. This is valid for arbitrary dirty inputs. Intermediate receiver reads must either be excluded or accounted for; the frozen witness is independently replayed on every formal input column. Each operand must have the same current frame at every actual addition. The constructor checks monotone frame chains and rational ranks, plus integer support of all operands.

The first layer uses 17 disjoint receiver/donor pairs and includes 17 correction terms. The second layer reuses target registers in a new restored interval; it is applied to the complete first-layer word and checked afresh. It adds one correction term. The two frozen selections are independently reconstructed, and removing each setup, recovery or correction is rejected: 54 controls total.

## Paid profile and universal improvement

Relative to pinned PR470, the final local profile difference is

    -10[1] -[2] -3[3] -18[4] +15[5] +3[6].

Rank mass is unchanged. For every p strictly between 0 and 1, the change in sum r^p is

    14(5^p-4^p-1) + 3(6^p+1-4^p-3^p)
      + (5^p+1-4^p-2^p) < 0.

The first term is negative by strict subadditivity. For each other term, the increase of x^p on the higher interval is smaller than on the lower interval of equal length, by strict concavity. Thus this construction strictly improves the recurrence moment independently of floating search scores.

## Whole-owner composition

Only the B phase changes. All helper entrances, exits, lines, frame catalogue, copy/scatter instructions and retained helpers are unchanged. Substitute the changed full local program into all 88 invocations of PR470's controller. The same residual isometries and whole-owner assignments apply; every helper still has its original complete endpoint and complementary dimension. The independent physical audit checks the actual emitted program and freshly recomputes intermediate growth. No residual is split across owner families.

The complex supplier is our unchanged PR471 construction. Its detailed sufficient monomial normalization and same-owner spectator argument is retained in research-notes/previous-complex-proof.md. Fresh local and global checks are available in the portable verifier.

## Novelty and scope

The new contribution is this source-bound two-layer word and its checked composition. The interval search admits correction terms and a sequential layer that reuses earlier targets. However, a control search found related elementary cost improvements using historical strict-prefix factoring. We do not claim a new fundamental identity, first use of Schur elimination, or a unique tensor-isomorphism discovery. The separate affine-controller theorem in research-notes is a future route; its physical transport condition has not been instantiated and contributes no claimed saving here.
