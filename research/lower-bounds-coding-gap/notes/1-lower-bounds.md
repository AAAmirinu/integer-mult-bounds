# 1. #109 and the known lower bounds: consistency, an oblivious machine, circuits, and on-line versus off-line

Status labels: **[K]** known and cited; **[P]** proof written here (checked only by the authors of this note, not
independently reviewed, not formalised); **[A]** audit or reading claim; **[C]** conjecture.

Every statement is conditional on #109's Theorem 1 (OpenAI, *Integer multiplication below n log n*, September 2026,
vendored here as `upstream/`), at whatever κ > 0 that theorem or a community witness supplies. Nothing here is
evidence for or against #109, and nothing bounds κ for the hub's construction.

## 1.1 No contradiction with the unconditional bounds [A]

Each known lower bound for multiplication fails for #109 on a stated hypothesis. Section references are to
`upstream/build/sections/`.

| Bound | Model | Why it does not apply to #109 |
|---|---|---|
| Cook–Aanderaa 1969; Paterson–Fischer–Meyer 1974 (Ω(n log n), mean time) | **on-line** multitape TM | #109 is off-line: no product bit is written before the forward transforms of both inputs (`00`, §1.3; `08`). |
| Clifford–Jalsenius, ICALP 2011 | on-line / streaming cell probe | same |
| Bryant 1991; Ponzio 1998; Sauerhoff–Woelfel 2003 | OBDDs, read-once and linear-length branching programs | they bound BP size or space under read restrictions, not multitape time |
| Pippenger–Fischer 1979 | general TM → circuit, O(T log T) | gives circuits of size n(log n)^{2−κ}, above n log n; see §1.2 for the oblivious route |
| Morgenstern 1973 | bounded-coefficient linear circuits | the layers are normalised (`05`): \|det H₀^{⊗d}\| = 2^{−d·2^{d−1}} < 1, so the determinant bound is vacuous; rescaling by 2^d is a relabelling of bit positions in the bit model (`02`) |
| Bürgisser–Lotz 2004 | bounded-coefficient bilinear circuits over ℂ | same normalisation; the products are bit-level Kronecker products, not bilinear gates |
| Ailon 2013–2016 | well-conditioned linear FFT circuits | the guard width Δ = ⌈C₀d^{C₁}⌉ (`05`) allows condition number 2^{poly(d)}; a speedup *needs* ill-conditioning, which #109 has |
| Harvey–van der Hoeven, FOCS 2025 (arXiv 2503.22848) | transposition ⇒ multiplication lower bound | #109 already notes its address procedure uses XOR and so lies outside data-movement models (`01`, "Lower-bound scope") |
| Afshani–Freksen–Kamma–Larsen, ICALP 2019 (arXiv 1902.10935) | bounded-degree circuits, **conditional on the Li–Li conjecture** | the conjecture is false (§1.4), so the bound is void |

On the Ailon row: #621 (merged) and #628 (open), both no-κ packages, prove conditioning bounds for the prime-power cyclic inverses
that do not depend on the cyclic length but grow exponentially in the kernel order r. That is consistent with the row: such bounds
are allowed by the guard width, and they are far outside the well-conditioned regime Ailon's bound needs.

No unconditional superlinear lower bound is known for off-line multiplication on multitape TMs or for Boolean
circuits [K].

## 1.2 An oblivious machine at the same κ (Lemma B′) [P, given an audit A]

A multitape machine is *oblivious* if every head position at every step, and the halting time, depend on n only.

**Lemma 0 [P; folklore, cf. Schnorr 1976, Pippenger–Fischer 1979].** An oblivious k-tape TM running in time T(n)
yields fan-in-2 Boolean circuits with bounded out-degree and O(T(n) + n) gates. (One constant-size gadget per step;
the symbol under head j at step t is wired from the last earlier visit to that cell, which is fixed because heads
depend on n only. Each written symbol is read by at most the next visit and the output read, so fan-out ≤ 2.)

**Audit [A].** #109's machine, *as written*, is not literally oblivious. We read every section of the multiplier
(`02`–`08`, `11`) and the Harvey–van der Hoeven routines it cites (nlogn.pdf §2, Prop. 4.7, Lemmas 4.8–4.12). Data
influence head movement in four places only:

- **D1.** The record adapter writes "the ordinary binary magnitude … and a fixed separator for each integer"
  (`07-resampling.tex`, around line 215), so field lengths depend on the data.
- **D2.** The quoted HvdH routines use variable-length integers.
- **D3.** HvdH Lemma 2.2 branches on the data ("if a ≤ 2^{2p} … otherwise …").
- **D4.** Sign-conditional scans: "complement and increment the blocks …; otherwise retain them"
  (`06-transforms.tex`:522; also `08-assembly.tex`:759).

Everything else is address-, descriptor- or counter-driven. That includes the exceptional set 𝓑 and its radix
sort (keyed by address-determined ranks), the guard widths, the Neumann iteration count (fixed, with no convergence
test) and the final carries. The per-procedure table is in [1a-oblivious-audit-table.md](1a-oblivious-audit-table.md).

**Lemma B′ [P modulo the audit].** If #109's Theorem 1 holds with exponent κ, then some oblivious multitape machine
multiplies n-bit integers in time O(n(log n)^{1−κ}), with the same κ. It is obtained by three changes:

1. encode every scalar at fixed width: sign plus a magnitude zero-padded to p+1 bits (fixes D1, D2);
2. replace each sign or overflow branch by "compute both, select by a bit" in finite control (fixes D3, D4);
3. replace the "established O(N log N) multiplier" by Schönhage–Strassen at fixed length, O(N log N log log N),
   whose only data branches are O(1)-local and are handled as in change 2.

Changes 1 and 2 cost O(1) factors. Change 3 costs log log(rp) = O(log p) on the O(rp)-bit Kronecker products, and
`08-assembly.tex`:996 already reserves this margin: "Any fixed power of log p is at most p^κ eventually". The
O(p)-bit products have budget O(p^{1+δ}), so any multiplier made oblivious by Pippenger–Fischer fits. The community
witnesses change only finite network constants, not stream primitives, so the same argument applies to them.

Our confidence in the audit is high but not complete: we read the procedures, not a formal TM. For the corollary
below, obliviousness of the multiplier subroutine is not even needed. A circuit for it, spliced in at n-determined
positions, suffices, and HvdH state that their results "also hold in the Boolean circuit model".

**Corollary B″ (circuits) [P, given Lemma B′].** If #109's Theorem 1 holds with exponent κ, multiplication of n-bit
integers has fan-in-2, bounded-fan-out Boolean circuits of size O(n(log n)^{1−κ}), below the O(n log n) circuits
of Harvey–van der Hoeven (2021).

## 1.3 On-line versus off-line (Corollary D) [P, given #109]

Let R(n) be on-line and M(n) off-line multitape time for multiplication. Paterson–Fischer–Meyer give
R(n) = Ω(n log n). So #109 implies

  R(n) / M(n) = Ω((log n)^κ),

a conditional separation of on-line from off-line multiplication on multitape TMs. Two consequences:

- **No conflict with existing results.** The generic conversion of Fischer–Stockmeyer (1974) loses a log n factor.
  Van der Hoeven's relaxed multiplication bounds (ISSAC 2014) are algebraic and FFT-specific; for integers they give
  O(I(n) log n). No black-box R ≤ M·(log n)^{o(1)} on TMs has been claimed.
- **A constraint on future work.** Any relaxed (on-line) variant of #109's transforms must lose at least
  (log n)^κ on multitape TMs, or it contradicts PFM.

## 1.4 Li–Li: already refuted, so no error signal [K]

AFKL show that the undirected multiple-unicast conjecture of Li and Li (2004) implies an Ω(n log n) lower bound for
bounded-degree multiplication circuits. Combined with Corollary B″, #109 would therefore refute Li–Li.

That conclusion is now moot. The conjecture was refuted unconditionally on 2026-10-07 by:

- X. Zhang, B. Li and Z. Li, *Network Coding Can Beat Routing in Undirected Multiple-Unicast Networks*,
  arXiv 2610.09367. This is already cited by the hub in `docs/research/stronger-rank-screens.md`.
- M. Braverman and Z. He, *The Multiple Unicast Conjecture is False*, arXiv 2610.10108.
- [dysfunctor/network-coding-counterexample](https://github.com/dysfunctor/network-coding-counterexample)
  (created 2026-10-07): a 33-vertex network **built from #109's XOR swap**, with coding rate 1 against routing
  ≤ 149/150. Its write-up notes that the counterexample does not depend on #109 being correct.

So "Li–Li ⇒ #109 is wrong" is vacuous, and the implied gap (log N)^κ is consistent with the published
(log n)^c families. What this section adds is Lemma B′ and Corollaries B″ and D. We found no prior statement of them
in the preprint, the hub (PRs and comments through #618), openai/math, AFKL, HvdH 2021/2025, or the public
discussion we searched.

## 1.5 Open

- A conditional upper bound on κ in terms of the coding/flow gap. With γ = limsup log g(N)/log log N for the
  worst undirected gap g(N) on N edges, the AFKL argument gives κ ≤ γ for every bounded-degree circuit family
  [P, short]. Since Li–Li is false, γ > 0, and no useful value of γ is known.
- A line-by-line formal obliviousness check of `07-resampling.tex` and the cited HvdH procedures.

## References

- P. Afshani, C. B. Freksen, L. Kamma, K. G. Larsen, *Lower bounds for multiplication via network coding*, ICALP 2019,
  arXiv 1902.10935.
- N. Ailon, *Tighter Fourier transform lower bounds*, ICALP 2015, arXiv 1404.1741.
- P. Bürgisser, M. Lotz, *Lower bounds on the bounded coefficient complexity of bilinear maps*, J. ACM 51(3) 2004.
- S. A. Cook, S. O. Aanderaa, *On the minimum computation time of functions*, Trans. AMS 142 (1969).
- M. J. Fischer, L. J. Stockmeyer, *Fast on-line integer multiplication*, JCSS 9(3) (1974).
- D. Harvey, J. van der Hoeven, *Integer multiplication in time O(n log n)*, Annals of Math. 193 (2021); FOCS 2025,
  arXiv 2503.22848.
- J. van der Hoeven, *Faster relaxed multiplication*, ISSAC 2014.
- J. Morgenstern, *Note on a lower bound of the linear complexity of the fast Fourier transform*, J. ACM 20(2) (1973).
- M. S. Paterson, M. J. Fischer, A. R. Meyer, *An improved overlap argument for on-line multiplication*, SIAM-AMS
  Proc. 7 (1974).
- N. Pippenger, M. J. Fischer, *Relations among complexity measures*, J. ACM 26(2) (1979).
- R. Clifford, M. Jalsenius, *Lower bounds for online integer multiplication and convolution in the cell-probe
  model*, ICALP 2011.
