# 1a. Obliviousness audit of #109's multiplier, procedure by procedure [A]

Companion table to note 1, §1.2. Sources: `upstream/build/sections/*.tex` (02–08 and 11; 09 and 10 are corollaries
and out of scope) and the Harvey–van der Hoeven manuscript that #109 cites
(https://www.texmacs.org/joris/nlogn/nlogn.pdf: §2.1–2.6, Lemmas 2.1–2.5 and 2.12–2.14, Prop. 4.7, Lemmas 4.8–4.12,
Remark 4.10). This is a reading audit, not a formal check.

Sufficient conditions used: **(N)** inputs are functions of n; **(A)** the scan extent is fixed by addresses,
descriptors or counters; **(F)** fixed-width arithmetic with carries, signs and rounding in finite control.

| # | Procedure (file / source) | Head movement determined by n? | Notes |
|---|---|---|---|
| 1 | Input: copy x#y, count n (`08` §Input) | **Yes** (A) | The promise fixes both operand lengths at n. Leading zeros are kept explicitly. |
| 2 | Parameters b, p, d, K, T, r, ℓ, α, γ; binary search for d (`08`) | **Yes** (N) | |
| 3 | Prime search by trial division (`08` §Prime source lengths) | **Yes** (N) | Its control flow depends on primality of n-determined candidates only. |
| 4 | Radix-digit formation, padding, Φ (CRT) layout and its inverse (`08` §cyclic-convolution layout) | **Yes** (A) | Validity tests a_i < s_i are on address counters. Offsets μ_i Σ a_j P_j come from address digits. |
| 5 | Elementary streams: digit permutations, splits/merges, row-cyclic splits, counters (`02` Lemma elementary-streams) | **Yes** (A) | All splits are on specified address digits or row indices. Counter ripple lengths are functions of the count, not of data. |
| 6 | Controlled shifts and rational scalings (`02` Lemma ordered-affine-streams) | **Yes** (A) | The offset a(controls) is a function of address control fields. Negation is a stack reversal of fixed-length blocks. |
| 7 | Fixed-point add/sub/shift with finite-control carries (`02` end) | **Yes** (F) | Widths are fixed by descriptors. |
| 8 | Lower-triangular factorization, matrix shear, power-width interchange, arbitrary-width chunk swap, fixed-tape DFS schedule (`04`) | **Yes** (A) | The circuit gates are fixed pointwise bit gates applied at matching addresses (XOR of data bits writes symbols only). Padding rows and parking-stack lengths are functions of the shape. "Independent of all field lengths and of the data" is accurate. |
| 9 | Packed selected-bit addition: eight rotations, exceptional set 𝓑, radix sort, reinsertion (`05` Lemma packed-selected-bit-rectangle; `11` grouped version) | **Yes** (A) | **Key check.** 𝓑 is defined by guard values of the y, z *address chunks*. Membership is computed from the record-rank counter. Destination ranks q′ = T₀S₀⁻¹(q) are functions of addresses. The stable LSD radix sort is keyed by these ranks, so its split pattern is n-determined. "Skip when the extracted bank is empty" is also n-determined. |
| 10 | Simultaneous butterfly layer: phase frames, row split into W roles, recursion, individual C kernels, guard widths, final truncation (`05` Prop. simultaneous-layer) | **Yes** (A+F) | The recursion tree, row padding and role splits are functions of (p, d, r, D, P, S). Guard width Δ = ⌈C₀d^{C₁}⌉ is fixed. The sign changes Z^{⊗f} use *address* parities. Truncation Q_p toward zero is a fixed-width sign-magnitude shift; see D4. |
| 11 | Synthetic transform layout, rounds, twiddles y^E (`06` Lemma synthetic-transform-cost) | **Yes** (A) | E is computed from address bits ("depends on the address, not on coefficient values"). The monomial is a split at r−s, which is n-determined. |
| 12 | Signed Kronecker packing / unpacking (`06` Lemma signed-ring-product) | **Yes after D4 fix** | The blocks have fixed 4p width, and the carries γ_j ∈ {−1,0} and ρ_j ∈ {0,1} stay in finite control. "If γ_r = −1, complement and increment; **otherwise retain them**" is a sign-dependent extra scan. Fix: always perform the scan, XOR-ing with the sign bit. Cost O(1). The magnitudes |A_u| are passed at the fixed width 4pr, so the multiplier call has an n-determined length. |
| 13 | "Established O(N log N) multiplier" = HvdH Thm 1.1 (`06`, `07`, `08`) | **Not established; replaceable** | HvdH work with "standard binary representation" (§2.1), i.e. variable-length integers (D2). Their Lemma 2.2 (Scaling) branches on the data, "if a ≤ 2^{2p} … otherwise compute b := a^{1/2} …" (D3), and it is used inside their Thm 3.1 and §5. Both are obliviousizable at O(1) (fixed widths; compute both branches and select). The cleaner route is to replace the multiplier by oblivious Schönhage–Strassen (§3). |
| 14 | Gaussian weights x_j, d̃_ℓ via HvdH Lemmas 2.13, 2.14, complex exponentials via Lemma 2.12 (`07`, `08` chirps and twists) | **Yes** (N) | The inputs j, k, s, t, α are all n-determined. The test "j > kp" in Lemma 2.13 is on n-determined integers. |
| 15 | HvdH Lemma 4.8 (D̃): d̃_ℓ · u_ℓ via Cor. 2.10 | **Yes after D1/D2 fix** | Per coordinate: one n-determined weight and one p-bit complex product with ρ-rounding. With fixed-width operands this is (F). |
| 16 | HvdH Lemma 4.9 (S̃) plus Remark 4.10 window jumps | **Yes after D1/D2 fix** | The window \|j − sk/t\| < m with m = ⌈√p/α⌉ and the cyclic boundary jumps are n-determined. The sums Σ a_j have O(p)-bit accumulators. The output bound \|T̃_k\| ≤ 1 is *proved*, not tested at run time, so there is no clipping branch. |
| 17 | HvdH Lemma 4.11 (Ẽ) | **Yes after D1/D2 fix** | Same structure: exactly 2m terms, with n-determined weights. |
| 18 | HvdH Lemma 4.12 (J̃, Neumann series) | **Yes after D1/D2 fix** | The iteration count n_J = ⌈p/(α²θ)⌉ is fixed, with no convergence test or early termination. Rounding v⁽⁰⁾ = ρ(u/2) is a fixed shift. |
| 19 | Selection C, index generation q_j (`07`) | **Yes** (N+A) | The counters e_j, f_j are n-determined. |
| 20 | **Record adapters to and from the HvdH routines (`07` "Record conversion and tape movement")** | **No, as written (D1)** | "emits the signed magnitude **after removing leading zeroes**", with "a fixed separator for each integer"; "Separators identify the next source field". The layout of the vectors fed to Lemmas 4.8–4.12 therefore depends on the bit-lengths of data numerators, and every later window scan has data-dependent head positions. **Fix:** keep each numerator as a sign plus a magnitude zero-padded to p+1 bits (or keep the w_c-bit two's-complement word) and run the quoted arithmetic at fixed width. The bounds are unchanged, since records are Θ(p) bits in the worst case anyway. Cost O(1). |
| 21 | Tensor interface: expand / compress axes, valid lines, zero lines, axis moves (`07` Lemma tensor-resampling) | **Yes** (A) | Validity is a predicate on coordinates. |
| 22 | Chirp construction and chirp transform; complex convolution by twist (`08`) | **Yes** (N, plus F after D4) | The phase numerators are n-determined. The products in Q_p(θ̃·f) are fixed-width p-bit products with sign handling (D4). |
| 23 | Removal of sign-extension bits w_M → w_c and w_c+γ → w_c (`08`) | **Yes** (A) | Both the source and target widths are fixed. Removal is a fixed-position truncation, valid by the proved magnitude bounds; it is not a leading-zero search. |
| 24 | Pointwise products z = Q_p(Ũ·Ṽ), scalings by S and 2^{2b+4}, rounding to the nearest integer (`08` steps 3–5) | **Yes after D4 fix** | The widths w_c+b and w_c+4b+4 are fixed. "Inspect its low p bits, apply the rounding carry" is a fixed-width increment, which must be run over the full width rather than stopped early (F). |
| 25 | Radix carries and output of exactly 2n bits (`08` final) | **Yes** (F) | Carry width O(b) is fixed. The scan length S·b is fixed. Exactly 2n bits are output, with leading zeros kept. |
| 26 | Exceptional-stream accounting across calls, parking stacks, descriptor stacks (`08` §Setup and exceptional streams; `05` batching) | **Yes** (A) | Visit counts and stack contents are functions of the shape. |
| 27 | Cutoff: schoolbook below a fixed n₀ (`08` end) | **Yes** | Schoolbook multiplication on fixed n is oblivious. |
| — | Bluestein | n/a | #109 does not run Bluestein as a separate procedure. It uses the chirp identity (`07` Lemma chirp-permutation), whose kernel a_j is n-determined (rows 14, 22). HvdH's own Bluestein step (Thm 3.1) lives only inside the replaced multiplier (row 13). |
| — | Kronecker substitution | Yes | See row 12. HvdH Lemma 2.5 has the same structure ("zero-padding (or one-padding in the case of negative coefficients) plus some carry and sign handling"), which is D4-type and fixable at O(1). |
| — | Corollary sections 09 (Newton division / sqrt) and 10 (transposition) | not part of the multiplier | 09 does normalise by a leading-bit search ("finds the significant bits of a positive input"), so that corollary machine is *not* oblivious. It is irrelevant to Theorem 1. |

**Looked for and not found in the multiplier:**
- data-keyed sorting (the only sorts are the radix sort in row 9, keyed by addresses, and HvdH's label-and-sort for P_t and P_s⁻¹, keyed by n-determined labels, which #109 removes anyway);
- convergence tests or early termination;
- floating-point normalisation or leading-zero counts on data, apart from D1;
- run-time clipping or overflow tests (every disk bound is proved, not tested);
- data-dependent recursion.
