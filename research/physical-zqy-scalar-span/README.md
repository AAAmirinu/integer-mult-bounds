# Actual-phase native history scalar spans

This package resolves the physical scalar-span question left open by
[Mark/Matarener's #5427](https://github.com/CrocSwap/integer-mult-bounds/pull/5427).
At **every positive tensor width**, no nonzero pure-Y observation is a scalar
combination of all retained full-frame versions of the frozen #5402 backward
word or either orientation of the final #4610 word. All original inputs remain
independent. The complete history is granted, including versions after an exit.

The new point is the actual operator algebra. The 215 signed operators have
one genuine four-term linear relation at width one. After including that
relation the observation still does not exist. A full-rank tensor-square Gram
certificate and the shared zero-state anchor cover every larger width. Exact
rational projection ranks and nonzero modular minors play separate roles;
modular nonmembership alone is not used as a rational exclusion.

**This is a restricted negative theorem, with no new kappa.** It does not close
the history under independently chosen free left monomial maps, including the
concrete Z-ABI transports. It does not exclude changed native schedules,
partial-frame histories, new paid queries or an endogenous observer in those
larger models. The independent inputs, observation version and these limits
are part of the claim. See [PROOF.md](PROOF.md).

## Reproduce

Python 3.12, standard library only, read-only default:

```sh
python3 -B scripts/research_package.py --package research/physical-zqy-scalar-span
```

Expected mathematical marker:

```text
PASS_ALL_WIDTH_PHYSICAL_NATIVE_SCALAR_SPAN_NO_NEW_KAPPA
```

The registered checks recompute the finite ABI left-image certificate, all
source-bound row ranks, the one-column operator relation/rank and the tensor-square Gram certificate, in normal and
optimized modes. The separate phase audit compares actual columns against the
retained exact Clifford implementation. `--write` explicitly regenerates the
local result; ordinary replay compares it without writing. Mathematical/runtime
checks are recorded in VALIDATION.md; publication byte/export transport results
are recorded in the PR. [INTERNAL-REVIEW.md](INTERNAL-REVIEW.md) separates internal
corroboration from external acceptance. No full native admission, selected cold
replay, compiler/outer, precision/tape, Lean or Docker run is claimed.

## Concrete Z-ABI left-image extension

A separate bounded continuation grants each backward-provider version one
left image from `{I, Kp_i, Km_a, Km_a^-1 Kp_i}`. The 1,012 distinct physical
maps and 59 actual history operators give 59,708 pairwise nonproportional
products, with exact F9 commutation and phase checks. The resulting span has
no nonzero pure-Y observation for **every f>=59,707**. Thus this fixed bank
cannot implement an all-width observer. This does not assert small-width
nonmembership or closure under arbitrary further products. The proof and
[ABI-CLOSURE.json](ABI-CLOSURE.json) state this as a separate theorem.

## Open next questions

1. Modify the native word to retain pure Ry before Dx is mixed in. Price every
   new observer job, storage slot and eventual termination. A supplied-observer
   invoice is not its construction.
2. Supply a genuinely new, versioned nonfree observation from another paid
   caller event, keeping disjoint mode ownership and every original input.
   Reconstruct one actual current-Y exit before extending the caller.
3. Test a different producer or partial-frame interface with its own exact
   arbitrary-input operator and complete bill. These theorems provide no
   price lower bound for that changed construction.

## Provenance and credit

Prepared by THU New Media Research Center (@thu-nmrc) with substantial OpenAI
Codex assistance from a lead and separate algebra/phase reviewers. These agents
are not independent human reviewers or a proof kernel. Apache-2.0.

- [Mark/Matarener, #5427](https://github.com/CrocSwap/integer-mult-bounds/pull/5427),
  head `389578f2d3ef075495ce76f08100ac50e18f7d40`: formal-word question,
  input/ownership/event/version semantics and the explicit physical follow-up.
  `native.py` adapts those semantics with actual signed operator composition.
- [Dillon Amburgey/dillona, #5402](https://github.com/CrocSwap/integer-mult-bounds/pull/5402):
  unrestricted coupled provider and all original mode inputs.
- [Cao Yifan/intqwq, #4610](https://github.com/CrocSwap/integer-mult-bounds/pull/4610):
  final native word and phase evidence. Cinna Davis/1337isnot1337, zxv,
  Dugongue, Jacob Alan Sussman and retained source authors supply its native,
  query, frame, tensor, compiler and analytic lineage.
- [zxv, #5415](https://github.com/CrocSwap/integer-mult-bounds/pull/5415) and
  [#5419](https://github.com/CrocSwap/integer-mult-bounds/pull/5419): current-Y
  observation contract, physical normalizers and consumer/cost obligations.
- [Ali Romman, #5377](https://github.com/CrocSwap/integer-mult-bounds/pull/5377):
  retained native row conventions. Chris R/Clear1nsight's provider and caller
  reviews remain separate from this scoped result.

Frozen upstream packages, scientific receipts and selected-frontier files are
unchanged. Exact canonical input blobs and hashes are in SOURCES.json.
