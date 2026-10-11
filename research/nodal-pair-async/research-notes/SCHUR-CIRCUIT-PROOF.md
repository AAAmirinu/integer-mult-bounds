# Exact Schur splice and live-pivot exchange

The source family is OpenAI's AlgorithmicThinTrees rational Schur history. MatrixRealization.schurEntry explicitly constructs a_ij - a_i0 a_0j / a_00; SchurHistory records every pivot and bounds intermediate rational encodings. These statements are source-inspected, not re-certified here. Our adaptation is an explicit linear circuit transformation, rather than an inference that the source automatically reduces multiplication complexity.

Maintain one removed logical register h as h = sum_j c_j x_j in the surviving current registers. Initially its clean value is zero. Every ordinary invertible update of a survivor changes the coefficients contragrediently, so this relation remains exact on all surviving input variables, including their arbitrary initial dirt.

For t <- t + q h, put d = 1 + q c_t. If d is nonzero, implement t <- d t + q sum_(j != t) c_j x_j. Its new representation of h has every coefficient divided by d. This is the scalar Schur complement. Every fill-in addition and scaling is emitted and billed. The current implementation rejects non-power-of-two scales and non-dyadic fills because the retained scalar lowering does not admit them for free.

If d is zero and t is an internal noncentre helper, change the eliminated variable instead. Explicitly replace the surviving physical t slot by the former h = c_t t + sum_(j != t)c_j x_j; c_t = -1/q is nonzero. This is an invertible shear/scale sequence. Name that slot h, and represent the new eliminated t as q sum_(j != t)c_j x_j. This is an exact live-pivot exchange. It is not an uncharged copy and does not identify arbitrary dirty registers.

For each emitted scalar gate, both actual operands must have one common frame. We tested both the old required frames and least-forward joins of the actual current frames. Final data hyperplanes and all centre-copy frames remain hard conditions. The complete candidate would additionally need its recomputed dirty compensation, cleanup, exact Gaussian phases, full owner inventory and global moment checked; a reduced scalar instruction count alone is not an exponent improvement.

## Bounded screens on PR507

All557 noncentre helper choices were tested. Fixed-frame fill-in failed all557 on a nonmonotone frame. Re-synthesis with forward frame joins left154 singular pivots,386 target-frame conflicts,14 nondyadic scales and3 centre conflicts. Adding explicit internal live-pivot exchange eliminated the first obstacle but left484 target-frame conflicts,56 locked data/centre pivots,14 nondyadic scales and3 centre conflicts. No candidate passed, so no gain is claimed. These screens do not exclude block elimination, another packet network or a differently scheduled scalar word.

The constructors and exact rejection counts are preserved beside this note. The independent kernel lane's new Newton-pair factory changes the dependency geometry; the same finite gate may be tested there without rerunning the old search.

## Combined Newton-pair screen

The strongest live-pivot gate was rerun on the changed block-0-09 raw factory. Its557 choices again produced484 target-frame conflicts,56 locked pivots,14 nondyadic scales and3 centre conflicts, with zero legal candidate. The exact source hash is recorded in newton-pivot-factory/SCHUR-SCREEN.json. This is a tested combination, not an additional numerical ingredient of the winning pair-cover construction.
