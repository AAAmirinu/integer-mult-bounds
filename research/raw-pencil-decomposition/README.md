# Raw finite-field pencil decomposition

This package extracts every singular and regular Kronecker block from two
arbitrary rectangular finite-field matrices. It returns exact row and column
maps and does not need an invertible base-field slice. It supplies the raw
input boundary left by the supplied-model character packages.

Read [PROOF.md](PROOF.md) for the algorithm, conventions, scope and credit.
Read [RESULT.json](RESULT.json) for exact evidence and [SOURCES.json](SOURCES.json)
for retained bytes. `decompose.decompose(A,B,m,n,field)` returns `(blocks,R,Q)`
with `A Q=R A0` and `B Q=R B0`. Field elements use the retained module's
base-p digit encoding. The slice map is the identity.

```sh
python3.12 -B scripts/research_package.py --package research/raw-pencil-decomposition
```

Expected: `PASS_RAW_PENCIL_DECOMPOSITION` and `PASS_REGISTERED_RESEARCH_PACKAGE`.
Python 3.12 and the standard library suffice. No physical supplier or new
kappa is claimed. The selected frontier is unchanged. Ali Romman with
substantial OpenAI Codex assistance; no subagents. Apache-2.0.
