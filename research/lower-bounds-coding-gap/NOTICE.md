# Notice

Prepared by ShikeChen01 with substantial assistance from Claude Opus 5.5 (Anthropic), via Claude Code. The
arguments, the audit and the scripts were drafted by AI agents; the submitter is responsible for the content. Apache-2.0 (`LICENSE`, copied
from the repository root).

## New in this package

Everything in this directory: `README.md`, `notes/`, `scripts/`, `proofs/`, `verify.sh`, `requirements.txt` and
`MANIFEST.sha256`. Nothing is vendored.

## Used, not copied

- **From main (read at run time):** `research/complex-571-hpeq5/data/EXPECTED.json` (#596, jeremykothe2, the
  selected complex supplier) and `research/e8-bit-p111-tuned/tune/EXPECTED.json` (#589, DreamingOfClouds) are read
  by `scripts/loss_chain.py`. The historical profiles typed into that script come from
  `research/community-pr279-audit/certificate.json` (gen4: #276, #279) and from #501's
  `research/r489-pooled-retimed-complex/EXPECTED.json` (eumemic, head 1dc0564). #493 (eumemic) is the bit word.
- **dysfunctor/network-coding-counterexample @ 2ad45b0** (no license file): `scripts/mcf33.py` reads the edge table
  printed by that repository's own `scripts/verify-network-coding-33.py --print-edges`. No file of that repository
  is included here.
- **Jacob Sussman, wht-power-saving-lean @ 9c94857** (Apache-2.0): the I_{n,1} family ordering in
  `scripts/lorentz/fam.py` follows `tools/e8/e8.py`, and the fitting-matrix rule is read off `tools/gx/gx.py`. No
  code is copied.
- **Upstream preprint (#109, OpenAI):** cited by section and line from `upstream/build/sections/`.
- `scripts/piece_count.py` and `scripts/loss_chain.py` use the hub's moment equation, written out afresh; no
  moment-engine code is copied.
