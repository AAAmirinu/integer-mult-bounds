# Lemma: reversible observable slicing with dirty background restoration

This lemma is used as an actual source-to-source transformation. On the selected 92-pivot
rank-sector word it removes 210 forward scalar instructions and their 210 inverse
cleanup instructions. It preserves the full paid child-rank profile. The 420
removed instructions are a concrete simplification, not an exponent improvement.

## Statement

Let a finite register space over a field K split as X direct-sum Y. X contains
source and auxiliary registers, with arbitrary initial values; Y contains the
observable target registers. Let a finite program P consist of invertible
coordinate additions and nonzero coordinate scalings. Assume:

1. Every instruction that writes X reads only X.
2. Every instruction in the distinguished center/scatter segment writes Y.
3. Cleanup reverses, in reverse order, precisely the X-writing instructions of P.
   Y-writing instructions are omitted from cleanup.

Select an X-writing instruction g whose written coordinate t has zero column in
the linear map from the state just after g to final observed Y. Delete g, and
regenerate cleanup from the remaining X-writing instructions. Repeated deletions
satisfying this condition preserve the complete map on X direct-sum Y, including
all arbitrary auxiliary dirt. Every X register is restored exactly. A fixed
preconditioner and a fixed initial dirty-response compensation can be retained.

## Proof

Write each instruction in block form with X first. An X-writing instruction has
matrix diag(A,I), where A is an invertible elementary matrix. A Y-writing
instruction has matrix [[I,0],[B,D]], with D invertible. Thus the entire body has
matrix [[F,0],[G,L]], where F is the ordered product of the X-writing elementary
matrices. Cleanup has matrix diag(F^{-1},I). Their composition is
[[I,0],[G,L]]. This argument includes arbitrary initial X; no clean-zero premise
is used and no unknown restoration gadget is assumed.

Let H be the suffix's observed row matrix just after g. For an addition
z_t <- z_t + q*z_s, H*g differs from H only by adding q times column t of H to
column s. For a scaling z_t <- q*z_t, H*g differs only by multiplying column t
by q. If that column is zero, H*g=H in both cases. Therefore deleting g preserves
the body's entire observed map [G,L]. The modified background product F' remains
invertible and reads no Y. Regenerated cleanup is diag((F')^{-1},I), so the full
modified map is again [[I,0],[G,L]]. This proves one deletion. Induction proves
any sequence, using the actual current suffix map at each deletion.

Prepending the same invertible target preconditioner preserves equality.
Similarly, the same initial dirty-response compensation remains valid because
the observed maps agree on every background input column, not merely on clean
source columns. The two complete maps are identical, so their inverse-transpose
maps are identical as well.

The background-read condition is essential: reversing X updates while omitting
Y updates need not restore X when an X update reads a Y value that changed in the
body. The implementation checks this condition rather than assuming it.

## Constructive implementation

`slice_reversible.py INPUT_WORD.json.gz NEW_OUTPUT_DIRECTORY` reads the actual
port count and auxiliary count. It initializes suffix-response column r to the
corresponding target unit vector for Y registers and zero for X registers, then
scans B, scatter, and A backwards. The exact rational updates are:

- addition t += q*s: suffix_column[s] += q*suffix_column[t];
- scaling t *= q: suffix_column[t] *= q.

An X-writing operation with zero suffix_column[t] is omitted. Target writes are
retained. This is exact adjoint observability, not forward clean-state zeroing.
The script generates the inverse background cleanup, verifies the old cleanup
matches its claimed contract, checks exact full matrix equality on all input
columns, and verifies the identity on every background output. Dyadic additive
coefficients and signed power-of-two scales are checked on the resulting word.
Existing frames and center metadata are retained. Physical frame legality,
child-rank pricing, and global owner routing are separate acceptance checks;
fewer scalar operations alone are never priced as a kappa improvement.

For a monotone frame segment, deleting an intermediate instruction leaves a
subsequence of its admitted frame chain. This supplies the elementary frame
legality argument; the actual compiler remains authoritative for special
center/scatter boundaries and the complete paid invoice.

## Actual checked application

Input: the selected 92-pivot word from Lemma 1, 120 ports, 560 helpers, 800 registers.
All background-writing additions read only background registers. Every addition
has distinct source and destination and every scale is nonzero.
The removed instructions are 140 additions and 70 scalings, all in A. Their
210 inverse cleanup instructions are removed too. No center/scatter or B event
is removed. Exact equality is checked on all 800 columns, including all arbitrary
helper dirt; the independent scalar audit checks both orientations and all 92
omitted-correction controls.

The complete local profile remains
{1:2459,2:182,3:522,4:88,5:238,6:128,7:1,8:17}.
The ordered residual widths are unchanged (18 width seven, 154 width eight,
388 width nine). See source120/base/sliced/SLICE-RECEIPT.json and
 audit/KERNEL-SCALAR.json in the replay directory.

The earlier S100 experiment also removed 420 scalar instructions, but is not
the selected source. Its profile and 100-control result are not reused as the
current source's evidence. Frame-lowering experiments found no additional paid
gain; the final construction retains the original frame labels. This lemma
simplifies the actual executed program but does not itself increase kappa.

This is a mathematical proof with finite exact replay, not new Lean certification.
Equal clean rows are never substituted for arbitrary-state restoration.
