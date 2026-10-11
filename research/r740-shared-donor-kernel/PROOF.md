# Finite R740 response-kernel composition

The exact conditional exponent saving is

`κ = 142050466976941 / 125000000000000000 = 0.001136403735815528`.

This document states the changed finite construction. The historical PR #438 proof and README are retained under `proofs/PR438-*`; their earlier values and source-centre bit word are historical and are not the present result.

## 1. Pinned starting word

`code/bit_construct.py` calls the unchanged PR #436 reconstruction: PR #370's producer with the frozen PR #436 parameters, elimination reuse, and six retiming sweeps. It compares the resulting JSON and reuse ledger to the pinned PR #436 copies. The canonical word hash is `d6ec8811541d6ab59a3bbbaaa15bccc8918b3b43b23d9f593198cfe90826fd20`.

The base has h = 8, 120 ports, 740 dirty helpers and nine sequential retained copies at the full frame. The original source/target decoder and dirty restoration are replayed on all 980 independent binary columns. This package does not apply PR #433's source-centre conversion or PR #434's eleven resets to that base.

## 2. New kernel witness

`stages/kernel-selection.json` is bound to that input hash. The construction uses the shared-donor response-kernel mechanism of PR #417. A pivot p starts at a root-closed entrance E contained in the first frame of p and every donor. Its frame-zero completion reads are removed. Each donor adds the appropriate pivot at E before its first A gate, and adds the same pivot after C at the full frame.

The completion response of each pivot equals the XOR of its donor responses. The 112 selected entries use 100 donor slots; their total entrance rank is 136. Every pivot is distinct, no pivot is a donor, and a donor is assigned consistently to one entrance. The exact reconstruction, response identities, source spans, nested frames and scalar decoder are checked, including arbitrary helper dirt. The kernel content hash is `b5789bffbf7bafe77a222366ea9a125b1d4a6f9d84b96afc4bb3c509d6b89b1a`.

Expand each multi-source gate into its ordered primitive ADDs, preserving the exact scalar sequence. The expanded input hash is `cb2afa377baeb8578e867ecda0f81caa68b2dac9cca805f41247754cfe91deb5`. The frozen retiming witness changes only the frames of 57 distinct A gates; all destinations and sources remain identical. The final word hash is `bae58f0692326f180ba49642360fd55557f59a93a96a8fa62bf7babd55d2384e`. The full decoder, dirty restoration and integer source-span legality are replayed again after these changes. The ordered primitive-retiming idea is credited to concurrent PR #434; this selection is derived independently on the R740 kernel word.

All 944 frames remain in the pinned rational frame family. There are 104 rank-one entrances, eight rank-four entrances, and 628 helpers with zero entrance. The actual local paid profile, including nine rank-eight retained copies, is

`{1:2500, 2:990, 3:326, 4:389, 5:90, 8:9}`.

The exported scalar record stream is rebuilt after primitive retiming; exact event counts appear in the emitted GLOBAL receipt. Reversing the actual stream and complementing frames gives the reflected program; each reflected ERASE becomes a fresh COPY. Both programs restore all independent helper columns and close each copied register. Their paid profiles agree. Exact rational spans and frame inclusion imply the corresponding commuting orthogonal-projector difference identities in both orientations under the inherited positive form.

## 3. Mixed residual banks and nine-stage word

Use the compressed PR #386 windows with ambient width 64, nine stages and eight replicas. A helper with entrance rank e requires a residual block of width 8-e. Each stage therefore has 832 width-seven slots, 64 width-four slots and 5,024 width-eight slots. The exact tiling uses 104 banks of eight width-seven plus one width-eight slot, four banks of sixteen width-four slots, and 615 banks of eight width-eight slots. That is 723 banks per stage and 5,920 assignments per stage.

Every coordinate of every bank is occupied once. The generated owner map and an independent audit check disjointness, coverage, stage/replica identity and reflected orientation. For all 15 distinct entrance frames, the package generates a matrix N with integer entries and N N^T = 4I. Its first e rows span the actual entrance and its remaining rows span the residual. N/2 is a coordinate permutation, checked by replaying at most seven swaps. Extended by identity on 56 exterior coordinates and followed by at most 64 coordinate swaps, it gives an explicit residual-to-bank isometry valid over every inherited odd address prime. The verifier checks the actual frame ID on every owner and rejects altered bases, frames and omitted factors. This closes the finite residual-isometry obligation highlighted by PR #439. The cover construction and correlated-dirty-bank semantics remain inherited all-size interfaces.

There are `W = 64·120 + 9·723 = 14187` live families, plus nine private centres. All nine local invocations replay 7,620 independent unbanked scalar columns, and the integer eight-bank macro identity includes all eighteen signed bridge shears and the terminal exchange. Omitting each bridge fails.

The complete paid profile is obtained by summing all 72 emitted local invocations and the actual idle children:

`{1:180000, 2:71280, 3:23472, 4:28008, 5:6480, 7:5760, 8:648, 14:3840, 28:3840, 42:3840}`.

It satisfies `64·W - sum(r·H[r]) = 2496`. The maximum child is 42 and `64² > 2·42²`. No saving is inferred solely from a helper count or a prospective histogram.

## 4. Complex supplier and finite invoices

The complex side is the unchanged PR #433 split-centre program. The package rebuilds its scalar word, both orientations, bank ownership, padding and complete paid profile. The `--replay-phases` mode also reconstructs every selected Gaussian phase pair and checks the exact recipe bytes. Two rational moment engines certify `b = 1183986549206329/10^18` with the inherited bad-branch allowance.

The bit finite invoice adds a conservative 144 elementary factors to every helper route, exceeding the seven local and 64 bank-coordinate swaps. The bit finite invoice is recomputed from emitted additions, owner assignments, geometry, copied-centre episodes, actual prefix bounds, compiler charges and selectors. It checks the retained two-level `2^512` coefficient allowance, row coefficient `18355 < 20161`, and the maximum-child inequality. Both rational moment engines, including the `10^-16` bad-branch allowance, certify

`c = 1137696618503020372244/10^24`.

The bit component binds. Exact counts and coefficient sizes appear in `CERTIFICATE.json`, and are recomputed by `code/combined.py`.

## 5. Exact outer assembly

Set eta = beta = `10^-18`, and

`s = min(c, (1-beta)b) - 10^-24`.

Starting at `a0 = 384599/10^10`, use six ordinary bootstrap levels `a[j+1] = (1-s)s + s·a[j]`. Each positive gap and finite cutoff is checked exactly with the charged 512-bit coefficient reserve. Put `q = a6(1-2eta)` and choose the largest `10^-18` grid point strictly below `(1-eta)q/(1+q)`.

The resulting κ above satisfies all 47 strict outer inequalities. The next κ grid point, zero eta, zero beta and unit beta are rejected. The result composes both actual supplier programs; independently quoted improvements are not added numerically.

All-size compiler, restored-work, tape, common-grid precision, correlated-dirty-bank and analytic transfer assumptions remain conditional. This finite computation is not an unconditional multiplication theorem or a Lean-kernel proof.
