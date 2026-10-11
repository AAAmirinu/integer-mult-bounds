# Twelve early helper resets in the split-centre construction

κ = 1.128922474816875e-3 = 1806275959707/1600000000000000.

This conditional finite construction starts from frozen PR433 and reuses twelve
bit helper rows after an exact reset at their final earlier use. It reduces the
bit helper count from 758 to 746, recomputes all dirty compensation and inverse
cleanup, and combines the changed supplier with PR433's split-centre complex
supplier. The bit side remains the limiting component.

Run with **Python 3.14 or later**, using only the standard library:

```sh
python3 -B research/early-reset-source-banks/verify.py --output /tmp/early-reset-full
```

Use a new output directory outside the package. No network access is needed.
The full verifier regenerates the pinned parent and all its Gaussian phases,
reconstructs twelve selected resets, checks both local orientations and reset
mutations, exports the actual bit record stream, checks every global owner,
recalculates both supplier profiles and finite invoices, and rechecks the exact
outer assembly independently. Every source file is hashed before and after.

The parent package is byte-for-byte pinned to PR433 commit
`2992f234bcb2538cb70f4d026aa8d08250b1040c`. Python 3.11 was found to emit a
different gzip OS header for identical canonical contents; this wrapper requires
3.14+ to reproduce the original byte pins. It does not alter the parent manifest.

The changed bit word has 986 formal input columns, 53,712 bank assignments,
14,394 live families and 14,403 physical families. Its fresh prefix bound needs
226 bits, charged at 256; the two-level coefficient needs 488 bits, charged at
512. All 47 strict outer inequalities hold, and the next 10^-18 grid point fails.

The result retains the inherited all-size compiler, arbitrary correlated dirty
banks, compressed windows, restored rows, fixed tape/common grid, precision and
analytic interfaces. It is not an unconditional multiplication theorem or a new
Lean proof. See `PROOF.md`, `NOTICE.md` and the preserved parent proofs/notices.

Prepared for eumemic with substantial OpenAI Codex assistance.
