# R740 bit word with a shared-donor kernel and explicit residual bank routes

The conditional saving is **κ = 56696402193643 / 50000000000000000 = 0.001133928043872860**.
It is 0.4380% above PR #436 and 0.07303% above PR #434 at commit
`a6c34f0ebb0e58588993c52a46a796aea02cd57f`.

We apply our PR #417 shared-donor kernel to eumemic's PR #436 R740 bit word.
The frozen selection has 115 pivots, total entrance rank 136 and 103 donor slots.
Its residuals fill 723 dimension-64 banks per stage instead of 740. All 15
entrance frames have explicit rational orthogonal completions; in this selected
family they are coordinate permutations. Their elementary factors are replayed.
The global integration derives from PR #436/#386; PR #435 supplies the prior
mixed-residual bank composition idea.

| Quantity | Result |
| --- | ---: |
| Helpers in the local word | 740 |
| Local arbitrary input columns | 980 |
| Banks per stage | 723 |
| Live / physical stock | 14,187 / 14,196 |
| Unbanked global scalar columns | 7,620 |
| Helper owner assignments | 53,280 |
| Rank deficit | 2,496 |
| Exact bit lower endpoint | 1135215296333206583339 / 10^24 |
| Cited complex lower endpoint (#433) | 1183986549206329 / 10^18 |
| Binding side | Bit |

## Reproduction

Python 3.11 or newer, numpy, mpmath, sympy, a C++17 compiler and Boost headers:

```sh
python3 -m pip install -r research/e8-r740-kernel/parent436/requirements.txt
bash research/e8-r740-kernel/verify.sh /tmp/e8-r740-kernel-full
```

Set `PYTHON`, `CXX` or `BOOST_INCLUDE` when needed. `--quick` skips only the
parent's historical regressions. Every mode verifies the parent manifest and
source blobs, reconstructs PR #436, reconstructs our kernel from its frozen
selection, checks local and global arbitrary-dirt columns, reflected copy
chronology, exact frame projectors, bank tiling and residual isometries,
nondegeneracy, mutation controls, two rational moments, the fresh finite invoice,
six bootstrap levels and all 47 strict outer inequalities. The next grid point
and three invalid outer parameter choices are rejected.

## Scope

This is a finite conditional construction for the retained
`T(n) = O(n (log n)^(1-κ))` assembly. The complex supplier is cited from #433,
including its #425 mutable-basis interface; its construction and Gaussian-phase
audits are not rerun here. Astronomical cover enumeration, all-size compiler,
correlated dirty-bank, restored-work, precision, tape/common-grid and analytic
interfaces remain assumptions. This is not a Lean proof or an unconditional
integer-multiplication theorem. κ = 1 remains open.

The search used floating-point scores to choose candidates. All admitted
witnesses, costs, maps and strict comparisons use integers or exact rationals.
Search scores are not certificates. See `PROOF.md`, `NOTICE.md`, `SOURCE.json`
and the unchanged parent package for the dependency chain.
