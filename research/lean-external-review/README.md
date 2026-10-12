# External review: one literal PR442 R747 invocation

This package contains Task A (a multi-host contract with exact single-host
recovery) and Task B (its connection to one literal PR442 forward invocation).
The contribution is prepared on a new local branch based on upstream
`db0e57bc7f36b5ac0fc844ad7ce1396165ee6647`. This snapshot is prepared for
a draft PR. The earlier public branch is unchanged.

The human participant initiated and coordinated this AI-assisted verification
effort and does not claim independent derivation or personal checking of the
mathematics. Codex agents developed the proofs, ran checks, and prepared reviews.
Agent reviews are not human audits.

## Scope and review entry points

- [Task A](../lean-multi-host-framework/README.md): abstract multi-host completion
  and exact recovery of the previous single-host theorem.
- [Task B](../lean-multi-host-source/README.md) and its
  [statement review](../lean-multi-host-source/EXTERNAL-CLAIM-REVIEW.md): literal
  endpoint, ownership, coordinate transformations and chronological clean-work guards.
- [Validation](VALIDATION.md): current receipts and fresh-versus-historical evidence.
- [Merged-work comparison](MERGED-OVERLAP.md), [draft PR](DRAFT-PR.md), and
  [privacy/provenance](PRIVACY-AND-PROVENANCE.md).

The selected invocation is stage 2, replica 0, pair 0 at PR442 commit
`4e16d001d505d4f21dd2bcfc44591f9be4c279bd`: 19,002 events, 987 live
Boolean payload streams, and one explicitly initialized clean private temporary.
The statements quantify over arbitrary dirty helper payloads, an address field
with `2 ≠ 0`, and an invertible invocation chart. The comparison retains every
affected host/data stream and the exterior of the active owners. Actual
old-bank outputs are threaded as auxiliary state.

The multi-host theorem is applied to **one complete invocation**;
cross-invocation disjointness is not exercised. The remaining pending-coordinate
ranges 15..21 and 1..28 are hand-supplied. Lean checks that they contain the
target masks; nothing binds those choices to the source schedule. Completion
performs the remaining pending swaps immediately.

Python extraction is reproducibly checked, not a formally verified compiler.
The local input embeddings are explicit. No full cover sweep, later recursive
schedule, arbitrary global allocation equivalence, physical cost bill, all-size
compiler, analytic transfer, or κ result is proved. PR448's split-helper gain
remains unestablished.

## Delivery and patch order

The new branch is `lean/pr442-invocation-review`. Its final commit is recorded
in an exported `delivery.json`; embedding that commit's own hash in a tracked
file would be circular. The historical public checkpoint
[`377012d`](https://github.com/cheesegrader/integer-mult-bounds/tree/377012d9e1d350c29fc47669e82415249429f60c)
does not contain this new validation.

**Apply only the supplied cumulative `review.patch**, once, to this exact base:

```sh
git clone https://github.com/CrocSwap/integer-mult-bounds.git review-checkout
cd review-checkout
git checkout --detach db0e57bc7f36b5ac0fc844ad7ce1396165ee6647
git apply --check /absolute/path/to/review.patch
git apply /absolute/path/to/review.patch
python3 research/lean-external-review/verify_package.py --allow-pending-task-b
```

Alternatively, unpack the supplied `integer-mult-lean-review.tar.gz`, enter
`integer-mult-lean-review/`, and run `sha256sum -c SHA256SUMS` followed by the
same package check. This archive already contains the complete sources; do not
apply the patch inside it. No private checkout or historical commit is needed.
The explicit pending option reports `PENDING_TASK_B` while the fresh build is
unfinished; it does not assert a Task B proof PASS.

Both routes include all local dependencies, particularly
`research/lean-whole-residual-hosting/CoordinateSwap.lean`, `Hosting.lean`,
and `PhysicalHosting.lean`. Task A builds six modules. Task B builds 50 own
modules plus `CoordinateSwap` and `MultiHosting`, for 52 total.

## Install the public dependencies

The Linux x86-64 commands require Git, Python 3.12, venv/pip, curl, tar, zstd
and a normal build environment. Lean and Mathlib are external public
dependencies; their binaries are not bundled.

```sh
python3 -m venv /tmp/lean-review-python
/tmp/lean-review-python/bin/python -m pip install -r research/lean-external-review/requirements.txt

mkdir -p /tmp/lean-review-deps
curl -fL https://github.com/leanprover/lean4/releases/download/v4.33.0/lean-4.33.0-linux.tar.zst \
  -o /tmp/lean-review-deps/lean-4.33.0-linux.tar.zst
echo '4b3fb03c29a1e0a253fb1d11f9bae3725f19a0dc6fc09b3ea16d2c9df3349e2c  /tmp/lean-review-deps/lean-4.33.0-linux.tar.zst' | sha256sum -c -
tar --zstd -xf /tmp/lean-review-deps/lean-4.33.0-linux.tar.zst -C /tmp/lean-review-deps
export PATH="/tmp/lean-review-deps/lean-4.33.0-linux/bin:$PATH"
lean --githash
# Expected: d8b18978322de05a8f3dba51ef03cf5461676c17

git clone https://github.com/leanprover-community/mathlib4.git /tmp/lean-review-deps/mathlib4
git -C /tmp/lean-review-deps/mathlib4 checkout --detach db584cd6d46c92f209a44c0f1c829460d327499d
cmp research/lean-multi-host-source/mathlib-lake-manifest.json /tmp/lean-review-deps/mathlib4/lake-manifest.json
```

From that Mathlib checkout, obtain the manifest-pinned dependencies and build
the required library targets:

```sh
lake build Mathlib.Data.Matrix.Mul Mathlib.Algebra.BigOperators.Fin \
  Mathlib.Tactic.FieldSimp Mathlib.Tactic.Ring Mathlib.Tactic.NormNum
```

Mathlib's official cache is optional. A source build works without that cache.
No project-specific compiled artifact is required.

Upstream's incorporated #509/#516 packages use Lean 4.21.0 and Mathlib
`308445d7985027f538e281e18df29ca16ede2ba3`. This package uses Lean 4.33.0
and Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`; the environments
must remain separate. See the [port estimate](MERGED-OVERLAP.md). No port is included.

## Reproduce both tasks fresh

From the review root after dependency setup:

```sh
/tmp/lean-review-python/bin/python research/lean-external-review/reproduce.py \
  --allow-pending-task-b \
  --lean /tmp/lean-review-deps/lean-4.33.0-linux/bin/lean \
  --mathlib /tmp/lean-review-deps/mathlib4 \
  --build-dir /tmp/lean-review-task-b-fresh \
  --receipt-dir /tmp/lean-review-receipts-fresh
```

The last two paths must be new. The command checks package integrity, regenerates
source literals, freshly compiles Task A and Task B, and audits the named
declarations with `lean -t 0`. Task A audits 21 declarations. Task B audits
931, including `SourceInvocation.actualContract`. It records installed
toolchain/library fingerprints and requires them to remain unchanged during
execution. Only standard Lean axioms are accepted.
The pending flag permits reproduction from this snapshot while its packaged
Task B receipt is absent. It does not enable reuse or bypass an invalid receipt.

The current validation uses no resume option. An interrupted future build may
use the runner's separately documented resume facility; its receipt must say
resumed and must not replace this package's fresh-evidence claim. Historical
receipts remain context only. Current receipt hashes must match current
manifests directly; no metadata-reanchoring exception is used.

## Export and validate a committed package

From a clean, committed Git checkout:

```sh
python3 research/lean-external-review/export_review.py --allow-pending-task-b \
  --output-dir /tmp/lean-review-delivery
python3 research/lean-external-review/validate_delivery.py \
  --allow-pending-task-b \
  --delivery-dir /tmp/lean-review-delivery \
  --receipt /tmp/lean-review-delivery/delivery-validation.json
```

The exporter creates one cumulative patch, a portable archive, exact commit IDs,
and checksums. The validator checks the extracted package, regenerates source
literals, and requires isolated patch application to reproduce the committed
tree. These are delivery checks, separate from Lean compilation. Neither
command pushes, publishes, or opens a pull request.
