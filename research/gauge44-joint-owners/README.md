# Joint-call owners: conditional κ = 0.001652704716932828

This improves [PR #649](https://github.com/CrocSwap/integer-mult-bounds/pull/649)
by jointly reassigning whole-helper owners on its Gauge44 map, retaining the
same reviewed [PR #589](https://github.com/CrocSwap/integer-mult-bounds/pull/589)
bit supplier. The complex circuit and physical controller are retained from
[PR #645](https://github.com/CrocSwap/integer-mult-bounds/pull/645).

| Quantity | PR649 | Joint-call owners |
| --- | ---: | ---: |
| Conditional κ | 0.001652528731617094 | **0.001652704716932828** |
| Complex saving b | 0.001655264103105891409910 | **0.001655440671539283540487** |
| Bit saving c | 0.001733427039589844234749 | unchanged |
| Helper roles | 35,424 | 35,424 |
| Live / physical families | 7,168 / 7,670 | unchanged |
| Global paid rank / deficit | 520,704 / 2,560 | unchanged |
| Paid children | 260,986 | 260,960 |

The exponent gain is **0.0106494557%** over the pinned PR649 submission. The
complex side binds. This does not reach κ = 2^-8 = 0.00390625. The conservative
complex recurrence also passes, at κ = 0.001652704714052949.

## Mechanism and scope

Callwise optimization holds the other 71 calls fixed. We release two calls
together, group their eligible idle families by capacity and call eligibility,
and nominate an integer reassignment. Starting from PR649's actual owner map,
one bounded pass considering 120 nominated pairs accepted 22 strict improvements.

Every accepted move passes exact integer checks after the solver returns. The
submitted explicit map is verified without a solver. Its idle-remainder
distribution strictly majorizes both predecessor maps: stoploss differences
are nonnegative at every integer threshold and positive at some thresholds,
with the same total rank and family catalogue. This lowers the
complex moment for every exponent in (0,1); see [PROOF.md](PROOF.md). Neither the
search nor its endpoint is claimed globally optimal.

The complete paid profile is:

```json
{"1":181029,"2":29091,"3":32312,"4":11521,"5":4032,"7":27,
 "8":577,"16":4,"20":1,"32":9,"48":2357}
```

This remains a **conditional finite witness**. It retains the all-size compiler,
common-label/mutable-source realization, whole-call hosting, precision/tape,
exact recovery, analytic transfer and bit H1–H5 assumptions. It is not an
unconditional integer-multiplication theorem or a complete Lean proof. PR589's
bit circuit is cited unchanged; its exact profile, bad-residue surcharge,
393-bit coefficient bound, 512-bit charge and interface guards are freshly
checked here, but its circuit is not independently rebuilt by this package.

## Immutable inputs

| Input | Commit | Use |
| --- | --- | --- |
| Main | `17ce0c79b7b51c2634b439ea5a2b754f09909693` | Pinned retained dependencies |
| PR645 | `638a5171dd1aca89ff50d07dcbe288b567769804` | Gauge44 circuit, geometry, physical verifiers |
| PR635 | `a6895a69f8ad98ab45777b03e9e6f48888c39f6f` | Local construction dependency |
| PR649 | `1b931ee055d738753778e1051300140c16ae219d` | Retained seed owner map |
| PR589 | `a5afc8c6169ea61ba7c51dfd3cade02cc7b13b46` | Stronger bit supplier, already imported on main |

PR589's `tune/EXPECTED.json` is consumed at main's
`research/e8-bit-p111-tuned/tune/EXPECTED.json`, SHA-256
`b9f0e5ca038abe837b0007c8fe006f366a6f02009244ac57705a8a200e2301f4`.
The two explicit adapters in `code/` pin this input and replace PR543's bit
parameters. The exact moment engines and 47 outer constraints are retained.

## Reproduce

Use Python 3.11+ with assertions enabled. Required verification uses only the
standard library. Main dependency file hashes are checked before replay.
Fetch the immutable construction packages into separate directories:

```sh
git fetch https://github.com/CrocSwap/integer-mult-bounds.git 638a5171dd1aca89ff50d07dcbe288b567769804
mkdir -p /tmp/joint-pr645
git archive FETCH_HEAD research/gauge44-global | tar -x -C /tmp/joint-pr645
git fetch https://github.com/CrocSwap/integer-mult-bounds.git a6895a69f8ad98ab45777b03e9e6f48888c39f6f
mkdir -p /tmp/joint-pr635
git archive FETCH_HEAD research/complex-571-cold14-st2 | tar -x -C /tmp/joint-pr635

python3 -B research/gauge44-joint-owners/verify.py \
  --main . --parent /tmp/joint-pr645/research/gauge44-global \
  --pr635 /tmp/joint-pr635 --out /tmp/joint-owner-replay
```

The output directory must be new and outside the input checkouts. The driver
checks both package manifests, rebuilds the retained scalar circuit, both
native ledgers, wrappers and exact phases, audits the owners against both
predecessors, and runs the PR645 global controller, actual 73-column charts,
finite invoice, two exact moment engines, 47 strict outer constraints and
admission controls. Independent pricing checks the reported exponent again.
A rebuilt native directory may be supplied with `--local`; that incremental
mode does not claim to regenerate the local word or phases.

Owner data, PLAN bookkeeping and frozen SPEC values are staged in a temporary
copy of PR645. Its physical checking programs remain byte-identical; the only
Python replacement is the disclosed bit-input adapter `code/assemble.py`.
No discovery mode runs during admission. The inherited global driver's scope
string still names PR543; the selected supplier is determined by the pinned
adapter and its fresh assembly receipt, and the package-level receipt states
the actual scope.

The optional search needs NumPy and SciPy (discovery used 2.4.3 and 1.17.1):

```sh
GAUGE44_PARENT=/tmp/joint-pr645/research/gauge44-global \
  python3 -B research/gauge44-joint-owners/search/joint_owner_passes.py \
  --owners research/gauge44-joint-owners/data/PR649-OWNERS.json.gz \
  --source-head 1b931ee055d738753778e1051300140c16ae219d \
  --pairs 120 --passes 1 --seconds 2 --out /tmp/joint-owner-search
```

Solver choices and timing may change the discovered map. The frozen submitted
map requires no optimization to verify. The compressed search receipt records
the accepted moves and exact endpoint; it is not a proof of joint optimality.

## Attribution

Prepared for Jay Mosley with substantial OpenAI Codex assistance. Gauge44 and
exact callwise matching are from icekylinx's PR645, which credits OpenAI GPT-6
Astra. The seed dissolve repacking and the same bit composition are
jeremykothe2's PR649, prepared with Claude Code; its lineage credits vectorsss /
Chi Zhao's PR638 relocation method. The bit supplier is DreamingOfClouds's
PR589, including its credited eumemic lineage and Claude assistance. PR635 and
all retained construction, controller, invoice and rational-engine contributors
remain credited through the pinned packages. Their notices and Apache-2.0
licensing remain in force.
