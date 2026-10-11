# Shared-donor response kernel on #433's R758 bit word: conditional κ = 0.001128832830332521

κ = 1128832830332521/10¹⁸ = 0.001128832830332521, **+0.712 % over #433** (0.001120864952258278). The bit supplier still
binds; the complex supplier (#433's split-centre construction, b = 0.001183986549206329) is unchanged.

**Change (bit side only).** chafreaky's #417 shared-donor response kernel (#320/#329 lineage), re-derived with #417's own
discovery tools on #433's R758 source-centre word and scored at m = 64: 128 entries (pivots entering at root-closed frames
of rank 1 and 4, total entrance rank 200), 124 donor slots, no new frames. Each pivot starts at its entrance and leaves the
frame-0 completion gates; each donor pays d += p at the entrance at the start of A and again at FULL after C
(response(p) = XOR responses(donors) over F2). `code/bit_kernel.py` applies the frozen selection
(`stages/kernel-selection.json`), re-runs #417's exact replay (legality, F2 on all 998 columns, source spans; two
assertions widened for #433's source-row destinations and source-row retained totals) and binds the output hash.

**Compressed geometry with entrances.** A helper entering at rank e has residual width 8 − e. Per stage the 8 × 758 helper
slots are tiled exactly into width-64 banks (eight width-7 slots plus one width-8 slot; sixteen width-4 slots; eight width-8
slots): 733 banks per stage instead of 758. The live stock is 7,680 + 9·733 = 14,277 and the rank deficit stays 2,496 (each
pivot's entrance saving in all 72 calls equals the stock it releases). `bit_global.py` and the independent `bit_audit.py`
check every owner route (bank, offset, width = 8 − entrance rank) and that every bank is covered exactly once, no padding;
the profile is read from the emitted program.

Bit lower 0.00113010853394748 (was 0.001122122700265139); κ from the same six bootstrap levels and 47 strict outer
inequalities (next grid point and invalid parameters rejected).
Verify: `python3 -B research/split-centres-kernel/verify.py /tmp/out` (about 30 s, standard library) → `PASS conditional kappa 0.001128832830332521`.

Credits: icekylinx (#433), chafreaky (#417 kernel mechanism and discovery code, vendored under `vendor/kernel417`,
Apache-2.0), ai-nanachi (#426), Zhihao Chen / jacklightChen (#425, #386), Dylan Crow (#370), J. Sussman (E8); rohanarun
with Anthropic Claude assistance for this composition. #433's README follows.

---

# Conditional κ = 0.001120864952258278

This package combines a split-centre Hamming complex construction with a
source-centre bit construction in compressed nine-stage windows. The resulting
conditional exponent saving is

$$
\kappa=\frac{560432476129139}{500000000000000000}
       =0.001120864952258278.
$$

This is approximately **6.9522% above PR425**. Both components change:

| Component | Helpers | Ambient width | Certified saving |
|---|---:|---:|---:|
| Complex | 560 | 73 | 0.001183986549206329 |
| Bit | 758 | 64 | 0.001122122700265139220566 |

The bit component limits the final assembly. The complex construction removes
coordinate contributions that cancel in the decoder, replacing eight full
centres with eight rank-eight and eight rank-one copies. The bit construction
starts from PR426's R767 word, computes its nine retained forms reversibly in
source rows, and uses PR386's compressed windows.

## Verification

Python 3.11+ and its standard library suffice. Use a new output directory:

```sh
python3 -B research/split-centres-global/verify.py /tmp/split-centres-check
```

The default replays both changed words, reflected/inverse-transpose programs,
bank ownership, costs, two rational moment engines and 47 strict outer
inequalities. Exact complex phase evidence is reused only when the regenerated
canonical word and complete recipe hashes match. To regenerate every selected
Gaussian phase pair as well:

```sh
python3 -B research/split-centres-global/verify.py /tmp/split-centres-full-phases --replay-phases
```

The unchanged historical repository suite and PDF build are not required by
this package. `EXPECTED.json` binds the result to both emitted global templates;
`MANIFEST.json` binds the package files; `SOURCES.json` pins imported sources.

## Scope

[PROOF.md](PROOF.md) supplies the changed finite construction. The all-size
compressed-window and correlated dirty-bank semantics, recursive compiler,
restored-work/tape/common-grid precision, and analytic transfer interfaces remain
conditional. This does not claim unchanged legacy gx/gxcore acceptance, a new
Lean proof, or an unconditional multiplication theorem.

Contributor history and AI assistance are recorded in [NOTICE.md](NOTICE.md).
Original notices and the inherited proofs are retained separately.
