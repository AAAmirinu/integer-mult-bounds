# Continued sprint: modular lifting of the same cyclic kernels

Authorized continuation on 2026-10-12 America/Los_Angeles,
starting 2026-10-13 03:24 UTC. Branch head at start:
`5020edec5c293cc0c733ff83a742952d1e52ba3b`; upstream remains
`66849e1475c930fd7732b1a0067ffee7e1e95f60`. Retain assignment seed **82**
and its independent-verification track; extend the same PR #666.

## Narrow claim

Test the following mechanism: for r=s*p^a, p prime, p not dividing s,
reducing a primitive r-th root modulo p collapses the integral kernel to
`z^(r-s) f_s(z)` and its conjugate reciprocal to `f_s*(z)`. If the two
base polynomials are coprime modulo p, the larger resultant is nonzero
in characteristic zero. A small exact base certificate could consequently
establish a uniform circle bound for infinitely many composite radices.

Deliverable: a precise written lifting argument or counterexample, a
standard-library modular identity checker with meaningful excluded-prime
controls, exact small-base certificates, and a revision of the existing
PR only if verified. Do not extrapolate from finite checks to all exponents.
Target initial bases s=2,3,4, using their independently checked denominators
3,43,37 respectively; no new multiplication kappa claim.

Three continuation candidates were considered: additional finite radices
(rejected as more computation without a new mechanism), rounded inversion
(already actively developed in #628 and audited in #663), and modular
lifting (selected as a structural use for the existing certificate method).
The new #668 uses split-prime CRT for prime-power resultants through 27;
its method and domain are distinct and retain credit as concurrent work.
All 488 open PR bodies through #668 were checked for overlap. No pinned
coordination issue exists, so the claim remains local.

Bound the experiment to roughly one hour, reserving its final quarter for
verification and handoff. Independently, attempt the omitted root
`make verify` with isolated dependencies and installed Boost headers.
Record actual completion or failures without relabelling unrelated failures
as passes. No intermediate speculative revision will be pushed.

## Completed mathematical result

Three integral seed identities with d=3,43,37 give the admitted families
r=2*p^a, 3*p^a and 4*p^a for all a>=1 and p not dividing the respective
s*d. LIFTING.md supplies the all-exponent proof, including the reciprocal
degree drop and characteristic-zero reduction. The original six tighter
fixed-radix certificates remain byte-identical. The quantitative bound and
Fourier transfer retain #621's attribution; there is still no new κ.

The standard-library check passes 54 finite diagnostics, three genuine
excluded-prime modular witnesses, and 173 rejection controls. Both public
receipts and all 16 focused tests pass on Python 3.9.6, 3.11.13 and 3.13.4.
Both optional generator modes reproduce their certificates byte for byte.
Separate Codex agents reviewed the mathematics and checker; this does not
constitute independent human review. Final overlap refresh covered 500 open
PRs through #680, with no duplicate lifting mechanism identified and no
pinned coordination issue. Broader repository execution is recorded in
VALIDATION.md separately from these completed package checks.
