"""Eleven chronological clean resets (rohanarun / OpenAI Codex, PR #434): R758 -> R747, applied with #434's own
reconstruction (vendor/pr434/replay.py and its frozen SELECTION.json) before the kernel stage."""
import os, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
D = Path(os.environ['E8_OUTPUT']) / 'bit426-source-centres'
src = D / 'bit-source-centres.json'; pre = D / 'bit-source-centres-r758.json'; pre.write_bytes(src.read_bytes())
r = subprocess.run([sys.executable, '-B', str(HERE / 'vendor/pr434/replay.py'), str(pre), str(src)], capture_output=True, text=True)
print(r.stdout); assert r.returncode == 0, r.stderr[-2000:]
