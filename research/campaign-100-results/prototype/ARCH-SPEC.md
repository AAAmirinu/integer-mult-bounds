# ARCH-SPEC — describing a word architecture for the generic synthesizer (S-synth)

Files: `/tmp/radical/S/archlib.py` (the builder = the spec), `synth.py` (architecture -> physical word -> exact κ),
`arch_paired_cube.py` (the paired cube in the spec; reproduces #325 byte-for-byte), `arch_example_triples.py`
(a minimal non-cube example), `price.py`, `make_template.py` / `pkg_template/` (the #325 package with its
admission pipeline generalised to this spec). Python: `"/Volumes/SP AI 01_16/CodexWorkspaces/imb-venv/bin/python" -B`.

```
python -B /tmp/radical/S/synth.py MY_ARCH.py OUTDIR --tag NAME [--arg key=value ...] [--compare REF_DIR] [--no-price]
```
runs: `MY_ARCH.architecture(**args)` -> graph -> producer compile (carrier matching solved, frozen, recompiled) ->
gauges -> virtual profile -> make_physical (reuse pairs, bank parity) -> descent -> install in a package copy ->
`price.py` (prepare -> physical527 -> parity_transform -> five-stage ledger -> moment.certify -> outer chain).
Output: `OUTDIR/result_NAME.json` (κ, bit root, ledger, R, entrances, J, timings), `final_NAME/` (the five selected
files = the physical word in the pinned format), `pkg_NAME/` (package copy with the word installed, priceable by
any other tool), `synth_NAME.log`. One run uses one core: p = 6 (v = 160) 4 s, p = 7 (v = 280) 9 s, p = 10
(v = 960) 76 s; memory < 1 GB. The word's κ is the same number verify.py would certify (the pricing block is
physical_eval.py's).

## 1. The interface

An architecture is a Python module exposing

```python
def architecture(**kw) -> archlib.Arch      # kw are the --arg key=value strings (parse them yourself)
```

`Arch` is the builder; `synth.py` calls `Arch.graph()` which checks the decoder and emits the generator graph.

```python
from archlib import Arch, load_module_json
B = Arch(h, labels, chi=None, cov=None, family='myfamily', p=None, meta=None)
```

| element | call | meaning |
|---|---|---|
| ambient space | `h` | labels live in Q^h; `p` (file naming only) defaults to `h // 2`; h need not be even |
| ports | `labels` | list of v index sets `[j1, j2, ...]` ⊂ [h] (chi_S = indicator) — or pass `chi=` explicit integer vectors of length h and let `labels` be `None` (then labels := supports). Ports are the sources AND the targets (index 0..v-1); the word computes y_T += x_T for every T. Labels must be nonzero and distinct. |
| target caps | `cov` | optional list of integer covectors; the cap of T is ker(cov_T), dim h-1. Default `cov_T = (9 chi_T − |chi_T|·1)/gcd` = the G-orthogonal complement of chi_T for the fixed Gram G = I − J/9 (= `3 chi_T − 1` for 3-sets, the paired-cube cap). |
| addition DAG | `B.add(a, b)` | node a + b; operands must have disjoint port supports; hash-consed on the pair (a, b) (two different trees with the same support are two different nodes, both allowed). `B.sum([...])` balanced fold. `B.module(data, inputs)` instantiates `{input_count, args, roots}` (args[i] = None for inputs, [a, b] otherwise; e.g. `load_module_json('pm_p10.json')`, w320 `modules.restricted_pairs(n)`, `all_but_one(n)`) and returns its root nodes. |
| centre | `B.center(node, targets, coordinate=None, name=None)` | a copied centre: support = ports of `node`; its frame is span{chi_S : S in support}; it is copied once per stage at rank dim(frame) and read by the listed targets. ANY target may read any centre (no cap rule). `coordinate=c` marks a star (support must be exactly the ports containing c; keeps the paired-cube root record byte-identical). |
| side channel | `B.side(node, targets, channel)` | the node value is delivered to every listed target at the targets' common cap. Cap rule: every port S in the support of `node` must satisfy cov_T · chi_S = 0 for every listed T. |
| partner mix | `B.mix(carrier, passive, receivers)` | source registers c, d (G-orthogonal: 9 chi_c·chi_d = |chi_c||chi_d|) are summed on c at the mix frame span{chi_c, chi_d}, delivered to the receivers at their shared level-2 cap, undone at the full frame. The receivers must be exactly the target set of an earlier 2-target side root. Each source in at most one mix. Optional (an architecture with no mixes is fine: unpaired sources climb 1 → h once). |
| graph | `B.graph()` | runs `B.check()` (below) and returns the dict compile_word consumes. `meta` keys are merged in (`pair_module_sha256` is recorded in the word file). |

Decoder (checked mod 2 by `B.check()` and again by the package verifier): for every target T

    XOR_{centres read by T} support(centre)  ⊕  XOR_{side roots delivering to T} support(node)  ⊕  XOR_{mixes received by T} {c, d}  =  {T}.

Root order matters: `synth` reads the roots in the order you emitted them. Centre roots are read first (at D_0, before
any target moves), then side roots in order, and a mix is delivered right after the level-2 root of its receivers.

## 2. What the compiler and the verifier enforce (and therefore what the spec forbids)

Everything below is checked, not assumed; a violation aborts with the message in quotes.

Geometry (exact over Q, ranks mod 2^127−1, nondegeneracy by integer determinants):
* `'target cap'` / `'root physical compatibility'`: a side root's node span must lie in the common cap of its targets
  — i.e. the cap rule. Side channels can only carry ports G-orthogonal to all their targets. (Centres are exempt:
  they are copied to D_0.)
* `'target retreat'`: for each target the caps of its successive side roots (in root order) must be nested
  ascending (a root with more targets has a smaller cap: emit broad roots before narrow ones; see the paired cube:
  face0 (4 targets) → edge12 (2) → singles (1)). Mixes are delivered at the level-2 cap, hence "receivers = a
  2-target root".
* `'span inside frame'`, `'operand nesting'`: every addition's frame (the join of the annihilators of all its uses)
  contains its operands' frames and the span of its support; automatically true for a positive DAG whose roots
  satisfy the two rules above, but a node used by roots with incompatible caps is forced up to the full frame.
* `'G-nondegenerate node and root frames'` (9I − J): every node frame, root frame, source line, centre frame, gauge
  frame and descent frame must be nondegenerate for G = I − J/9. A port label with 9|chi|² = (Σchi)² (e.g. any
  9-subset indicator) is a degenerate source line and is impossible; a centre whose support span is degenerate is
  impossible; gauges whose frame is degenerate are simply not selected. For 3-set labels nothing is degenerate at
  the line level; for other port sizes test early (`B.graph()` does not test G-nondegeneracy; synth does).
* `'unused node'`: every node, including every port leaf, must be reachable from some root (a port read by no
  root makes the word ill-formed: every source register must be consumed).
* `'support-disjoint addition'` (positive DAG, no cancellation), `'mod-2 unit coefficients'`.

Decoder (mod 2, the only payload the verifier checks — the integer decoder is "producer evidence"):
* `'decoder identity at target %d'` — the identity above.
* `'cap rule: side root reads only ports in the cap of target'`, `'cap rule: partner delivery inside the cap'`.
* `'declared centre support'` / `'star support'`; `'centre frame = support span'` (copy rank = dim of the support's
  label span — you cannot pay less than the span).
* mixes: `'carrier and passive G-orthogonal'`, `'mix frame = span{chi_c, chi_d}'` (dim 2, nondegenerate),
  `'each source in at most one partner pair'`, `'partner delivery at own receiver root'`.
* For the paired-cube family (all centres are stars, default chi/cov) the historical strict checks also run
  (`stars read by target = coordinates of T`, `side part = Σ_{|S∩T|=1} x_S`).

Physical layer (unchanged producer rules, applied to every architecture): registers = 2v + R (R = virtual roles:
one per source leaf, one per addition, extra copies for multiple uses minus carrier-matched arcs); plain frames
for additions of span ≤ 8; PR144 chronological gauges with the G filter; late reuse pairs (recipient = rank h−3
gauge, donor dead before the read, donor end frame inside the gauge frame); bank parity (trailing pairs dropped
until 60·width ≡ 0 mod 5h — at some h this can never be restored by rank-3 drops, cf. p = 9); endpoint descent
(join/meet moves with one-row repairs); nested role chains, copy lifetimes (one centre copy open at a time, read
at D_0 exactly scatter_reads times), monotone target chains ending at the cap.

Five-stage ledger (price.py): m = 5h, 60 replicas, idle ranks (2h−2, h−1, 2h+2, 4) at 2v each, h-independent
rule; copied centres: one transform of rank dim(frame) per centre and stage; deficit 4v − 5ℓ with
ℓ = Σ_centres dim(frame). A certificate exists only if **4v − 5ℓ > 0** (ℓ < 0.8 v) and every child rank < m.
So the first number to compute for a new family is ℓ/v: the paired cube has ℓ = h(h−2) = 3v/(p−2)
(0.375 at p = 10); star centres on all triples of [h] have ℓ = h·(h−1) ≫ v for small h (example file);
agent N's lemma search found nothing below h(h−2) for the cube ports.

What the spec cannot express: non-F2 (signed/integer) decoders beyond "integer DAG whose F2 reduction is the
identity", a target reading a centre at a frame other than D_0, more than one copy transform per centre per
stage, mixes of more than two sources or on non-source registers, side deliveries outside a target's cap, a
different Gram (the verifier's G = I − J/9 is fixed; port sizes ≠ 3 only change which labels are orthogonal),
a different stage count / replica count / idle-rank layout (five-stage, 60 replicas fixed in the package).

## 3. Worked example 1 — the paired cube (abridged from `arch_paired_cube.py`)

```python
def architecture(p=10, pm=..., qmod=..., design=..., orient=..., merge=True):
    h = 2*p; cubes = [orient.get(I, I) for I in combinations(range(p), 3)]
    allb = list(product(range(2), repeat=3))
    labels = [tuple(2*i + b for i, b in zip(I, bits)) for I in cubes for bits in allb]   # v = 8 C(p,3) triples
    source = {(I, bits): 8*j + k for j, I in enumerate(cubes) for k, bits in enumerate(allb)}
    B = Arch(h, [list(l) for l in labels], family='paired_cube', p=p)
    # local channels per cube: A[I,i,a] = sum of the 4 sources with selector a at position i, G[I,i,j,m] = the 4
    # with s_i ^ s_j = m, each built by the recipe tree of local_design_pP.json with B.add
    # global modules: for every coordinate i and selector bit, the pair module on the C(p-1,2) inputs A[.,i,bit]
    #   -> Pm[I,i,bit] (sum over the cubes sharing exactly pair i), extra root = star(2i+bit) = centre
    # for every pair (i,j) and mode, all_but_one(p-2) on the G[.,i,j,mode] -> Qm[I,i,j,mode]
    for I in cubes:                                  # decoder, root order = delivery order
        for a in (0,1): B.side(Pm[I,I[0],a], [source[I,b] for b in allb if b[0]==a], 'face0')          # 4 targets
        for a in (0,1):
            for m12 in (0,1): B.side(Qm[I,I[1],I[2],1-m12], [... b[0]==a and b[1]^b[2]==m12 ...], 'edge12')  # 2 targets
        for b in allb:                                                                                 # singles
            B.side(B.add(Pm[I,I[1],b[1]], Qm[I,I[0],I[1],1-(b[0]^b[1])]), [source[I,b]], 'u01')
            B.side(B.add(Pm[I,I[2],b[2]], Qm[I,I[0],I[2],1-(b[0]^b[2])]), [source[I,b]], 'w02')
            B.side(source[I,(b[0],1-b[1],1-b[2])], [source[I,b]], 'partner')
        for par in (0,1):
            for a in (0,1):                          # partner-pair mixing, receivers = the edge12 root's 2 targets
                pair_ = sorted(b for b in allb if sum(b)%2==par and b[0]==a)
                recv  = sorted(b for b in allb if sum(b)%2==par and b[0]==1-a)
                B.mix(source[I,pair_[0]], source[I,pair_[1]], [source[I,r] for r in recv])
    for c in range(h):                               # 2p star centres (rank h-2), read by the 3v/h targets containing c
        B.center(star[c], [t for t, lab in enumerate(labels) if c in lab], coordinate=c)
    return B
```

Run (reproduces #325 exactly: all five selected files byte-identical, κ = 7.69684039e-4):

```
D=/private/tmp/imbwork/w325/research/five-stage-p10b-banks/bitword/producer/data
python -B synth.py arch_paired_cube.py out --tag pc10 --arg p=10 --arg pm=$D/pm_p10.json --arg qmod=$D/qmod_p10.json \
   --arg design=$D/local_design_p10.json --arg orient=$D/cube_orient_p10.json --arg merge=1 \
   --compare /private/tmp/imbwork/w325/research/five-stage-p10b-banks/bitword/selected/bit
```
Generic modules for other p: `/tmp/radical/H/out/pkg_pP/bitword/producer/data/{pm,qmod,local_design}_pP.json`
(p = 5, 6, 7) and `/tmp/radical/A/mods/` (p = 8..14); `--arg qmod=generic` gives all_but_one(p−2).
Variants for testing the generic paths: `--arg mixes=0` (pair sums as level-2 side roots, no source mixing:
κ 1.3047e-4 vs 1.3361e-4 at p = 6), `--arg star_coord=0` (centres by support), `--arg scale_chi=2` (explicit chi).

## 4. Worked example 2 — any 3-uniform family (`arch_example_triples.py`)

```python
def architecture(h=7, family='all'):
    ports = [tuple(t) for t in combinations(range(h), 3)]            # or an STS, or the cube triples
    B = Arch(h, [list(t) for t in ports], family='triples_'+family)
    for T in range(len(ports)):                                       # side: the ports orthogonal to T
        orth = [S for S in range(len(ports)) if len(set(ports[S]) & set(ports[T])) == 1]
        B.side(B.sum(orth), [T], 'orth')
    for c in range(h):                                                # centres: the h stars
        members = [S for S in range(len(ports)) if c in ports[S]]
        B.center(B.sum(members), targets=members, coordinate=c)
    return B
```
Identity: Σ_{c∈T} star(c) = {T} ⊕ Σ_{|S∩T|=1} S mod 2 for any 3-uniform family. It runs through the whole
admission pipeline (PASS PHYSICAL / PASS parity) but has no certificate (ℓ = 42 > 0.8·35 at h = 7): the
example of a family whose centre mass kills it before any word is built — compute 4v − 5ℓ first.

## 5. Reading the result

`result_NAME.json`: `price.kappa_float` (exact κ, the bit-binding value), `price.bit_root`, `price.R`
(physical registers per vertex), `price.entrances` (gauge ranks), `price.literal_stock`, `price.paid_hist`,
`price.J_phys_chains` (Σ r ln(m/r) over physical chains incl. centre copies: descent's objective; ≈ 1.2e-9 κ per
unit at p = 10) and `price.J_five_stage`; `virtual` (R, loss = ℓ, virtual deficit, gauges, matched arcs, plain
frames, float root of the 3h ledger); `shape` (ℓ, centre ranks, reads, five-stage deficit); `seconds` per stage.
`price.error = 'no positive root: ...'` means deficit ≤ 0 or a child rank ≥ m — no certificate for this word.
Baseline to beat: #325, κ = 7.696840e-4 (bit root 7.7028e-4, complex cap 7.72714e-4: nothing above
κ ≈ 7.7212e-4 is reachable by a bit word alone).

Levers visible from the ledger, in order of size (from A's and H's reports): the five-stage deficit 4v − 5ℓ (ℓ/v
of the centre set), R/v (addition count per source after carrier matching: module quality, ~1.2e-4 at p = 10
between generic and annealed modules), gauge entrances (rank h−3/h−4 chronological gauges + late reuse), and
last the frame assignment (≤ 0.15 % of J).
