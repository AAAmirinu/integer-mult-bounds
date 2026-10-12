#!/bin/sh
# Fresh replay of the retained exact-head PR627 input package.
# Chi Zhao, with substantial OpenAI Codex assistance; Apache-2.0.
# Python >=3.10, stdlib only.
set -eu
WORK=${1:?usage: run_replay.sh NEW_WORK_DIRECTORY}
HERE=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
REPO=$(CDPATH='' cd -- "$HERE/../.." && pwd)
PYTHON=${PYTHON:-python3}
"$PYTHON" - "$HERE/inputs/pr627-package.tar.gz" <<'PY'
import hashlib
import sys
from pathlib import Path
if sys.version_info < (3, 10):
    raise SystemExit('Python >=3.10 required')
expected = '411790745f7c7d014b54648a3eff2b82c83cf0d4d2cc153c2b47edfe65937661'
if hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest() != expected:
    raise SystemExit('Frozen PR627 package archive SHA-256 mismatch')
PY
test ! -e "$WORK"
mkdir -p "$WORK/input"
tar -xzf "$HERE/inputs/pr627-package.tar.gz" -C "$WORK/input"
PKG="$WORK/input/complex-571-cold14-k492b"
"$PYTHON" -B "$PKG/verify.py" --jobs 2 --work "$WORK/replay" \
  --source multicold="$REPO/research/complex-multicold" \
  --source structural_gain="$REPO/research/structural-gain" \
  --source larger_gain="$REPO/research/complex-k492-owner-repair/vendor/larger_gain" \
  --source joint_prefix="$REPO/research/complex-joint-prefix" \
  --source frame_coalescing="$REPO/research/kernel-frame-coalescing" \
  --source direct_delivery="$REPO/research/direct-delivery504-global"
"$PYTHON" -B "$HERE/check_native_owners.py" --package "$PKG" \
  --replay "$WORK/replay" --repository "$REPO" --out "$WORK/INDEPENDENT-OWNERS.json"
ROUTING="$REPO/research/complex-multicold/vendor/pr558/vendor/pr552/complex-local/inputs/phase-baseline/CANONICAL-WORD.json.gz"
"$PYTHON" -B "$HERE/inputs/contributor_check_new_helpers.py" --package "$PKG" \
  --word "$WORK/replay/jp8-step6-cold_end/FULL-WORD.json.gz" --routing "$ROUTING" \
  --out "$WORK/focused-controls"
"$PYTHON" -B "$HERE/check_extra_tail_controls.py" --package "$PKG" \
  --word "$WORK/replay/jp8-step6-cold_end/FULL-WORD.json.gz" --routing "$ROUTING" \
  --out "$WORK/extra-controls"
