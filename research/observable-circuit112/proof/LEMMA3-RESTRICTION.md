# Constructive packet restriction and stable-carrier quotient

## Statement 1: exact isolated-register restriction

Let K be any field. Let a finite straight-line program consist of invertible elementary additions z_t <- z_t + c z_s (t != s) and nonzero scalings z_t <- c z_t. Partition its registers into retained R and deleted J. Suppose every addition has both its source and destination in R, or both in J. A scaling belongs to the set containing its destination. Delete the J instructions and rename R injectively. Then for every initial state, including arbitrary dirty helper values, every retained prefix state is the restriction of the corresponding original prefix state. In particular the final operator is exactly the R diagonal block, and every restoration equation on retained registers is unchanged.

Proof. Induct on instructions. A J instruction leaves the R restriction fixed. For an R instruction, its old-state operands and destination all lie in R, so evaluation and update commute with restriction. Injective renaming commutes with these same old-state evaluations and distinct destinations. This proves the prefix claim and hence the final claim. The full program is a direct sum because the identical argument also applies to J. No clean-input assumption or equality of output rows is used.

If instructions carry register-local frame labels, unchanged retained instructions retain precisely their old frame obligations. This alone does not establish a smaller physical cover, normalized endpoint, or recurrence: those require an explicit new physical construction and invoice. In particular deleting logical coordinates is not permission to split a recursive owner.

## Statement 2: stable-carrier quotient with rebuilt dirty correction

This second sufficient transformation is useful when the isolation test fails, but it did not pass the present finite lifetime screen.

Separate the registers into target y, protected source x, and arbitrary dirty internal d. Consider an internal preparation A, a delivery word B, and the reverse of the entire internal word. Internal gates never read targets. B may change targets and may have internal gates, but let two chosen internal registers a,b be read-only throughout B. Let b not be a protected source or a centre requiring an external copy/erase protocol. Suppose:

1. During A no retained register reads b: every addition with source b has destination b or a deleted register; in the single-register version below self-additions are excluded by the elementary-gate convention, so there are no such additions.
2. Every B read of b goes directly to a target, and b has no B writes. The kept a also has no B writes.
3. On the zero-dirty preparation, b = lambda*a as linear forms in x, where nonzero lambda and all resulting gate coefficients are permitted exact scalars (dyadic for this construction).
4. Removing b leaves all source/helper restoration stages available by literally reversing the new internal word. The new target-only linear block T is invertible; here T is the same elementary target word as before.
5. An explicit legal frame schedule is built for the changed word and every newly required frame increment, final climb, normalizer, centre protocol and scalar operation is charged.

Delete every A gate with destination b; redirect each delivery y_t <- y_t+c*b to y_t <- y_t+(c*lambda)*a; delete b and reindex injectively. Regenerate the reverse internal word. Compute the new target map exactly as T*y+A0*x+B0*d. Execute the explicit input correction y <- T^(-1)*y - T^(-1)*B0*d before this word. The final map is y <- y+A0*x with all remaining internal registers restored for every dirty state. On clean data, A0 equals the original desired source-to-target map.

Proof. Since b has no retained readers in preparation, deleting its writes changes no retained A state. The clean relation in condition 3 therefore remains true for a, and replacing each target read preserves the clean B computation by induction; condition 2 prevents any intervening destructive state alias. All retained internal gates are invertible and target-independent, so reversing them restores the initial x,d exactly. Exact symbolic propagation yields T,A0,B0. Substitution of the displayed correction gives T*(T^(-1)*y-T^(-1)*B0*d)+A0*x+B0*d = y+A0*x. T^(-1) is constructed by reversing its elementary target gates, so this is an explicit finite algorithm rather than an assumed linear-system oracle. Rebuild every kernel/gauge compensation that used the deleted variable; the old compensation cannot be silently retained.

A sufficient frame-construction check starts from actual initial frames and intrinsic gate constraints. At every gate form the span of all touched current frames and the intrinsic gate frame. Accept only when that span lies in every touched register's endpoint cap and all centre checkpoint constraints are obeyed. Raise each touched register to this common frame and charge its dimension increment. Induction proves monotonicity and cap inclusion. If any test fails, this sufficient construction is rejected. This does not assert that every semantically valid scalar quotient admits this frame construction, nor that any quotient is profitable.

## Exact instantiation and finite screens

- The selected sliced 92-pivot word's eight coordinate source ports 0..7 and eight targets 120..127 have exactly eight touching instructions, all internal to that deleted set, and zero cross-boundary gates. The literal restriction constructor and independent source-bound checker examine every actual instruction. Statement 1 therefore applies to the entire precondition/A/cut/B/cleanup scalar word on all arbitrary input columns.
- This specialization implements the puncture mechanism of upstream PR523; it is not presented as an independent discovery of that numerical improvement. Its physical cover, 112-port controller, and recurrence accounting must be supplied and checked by the new assembly.
- The raw rank-sector preparation contains 90 proportional packet groups and 180 ordered candidate pairs. Of these, 135 fail the no-retained-reader condition and 45 fail the stable-B condition. There are no candidates satisfying this strict sufficient lifetime rule.
- Repeating this exact screen on the kernel lane's observable slice (210 A writes and their inverses deleted) gives the same 135/45 split and no candidate. This excludes only this frozen sufficient rule on these words; it does not exclude compensated overwrite, target-chain redesign, or other packet circuits.

No independent numerical gain is attributed to Statement 2. Both statements are proved here as construction lemmas; no claim of global mathematical novelty or Lean certification is made. Equal clean packet rows alone never justify aliasing destructive updates or sharing physical owner families.
