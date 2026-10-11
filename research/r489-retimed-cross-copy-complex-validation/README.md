# Validation of `research/r489-retimed-cross-copy-complex`

## Component certification (done)

`component/` is the output of the following command. Six files are left out: the copy of the input word
(`data/complex/FULL-WORD.json.gz`) and five large generated files, namely the hosted template (0.5 MB) and the word's
canonical form, programs, adapted programs and phase recipes (`word/split-centres/`). Their
digests are in `component.sha256` (the template's is also in `RESULT.json`), and the verifier regenerates them.

    PYTHONDONTWRITEBYTECODE=1 PYTHONINTMAXSTRDIGITS=0 python3 -B research/r489-retimed-cross-copy-complex/verify.py OUT \
      --parent-output /abs/completed/pr494/output

The run used Python 3.13.16 on this branch. The parent was a complete, fresh `verify.py` output of PR #494 at
`419907c71246c050f1c3fd2a504469b74bf7798e` (status `PASS_FULL_R489_BIT_CROSS_COPY_COMPLEX_COMPOSITION`). The
verifier checked that parent's receipt status, manifest digest, every step-log digest and its result against PR #494's
`EXPECTED.json` before reusing it.

It then ran all five steps of this package:
- the word rebuild with PR #495's scripts;
- the hosted template;
- the finite invoice;
- the independent audit, which rejected 20 of 20 mutations;
- the exact assembly.

Receipt status: `PASS_COMPONENTS_WITH_VERIFIED_PR494_REUSE`, with κ = 726474255625747/500000000000000000.

## Full clean rerun (in progress)

`verify.py OUT` without reuse, on a fresh clone of this branch, reruns PR #494 from scratch (PR #493's `verify.sh`,
PR #442's complete verifier, PR #448's hosting) and then this package. Its receipt, together with `make verify` and
`make gen4-bank-verify` on this branch, will be added here when done.
