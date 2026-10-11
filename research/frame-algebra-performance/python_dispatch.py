"""External PYTHON launcher for the pinned shell verifier; log command timings."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
args = sys.argv[1:]
script_args = args[1:] if args and args[0] == '-B' else args
original = [sys.executable, *args]
command = original
source = Path(os.environ['FRAME_ALGEBRA_SOURCE'])
if os.environ['FRAME_ALGEBRA_MODE'] == 'fast' and script_args and script_args[0] == str(source/'code/stages.py'):
    if len(script_args) != 6 or script_args[1] not in ('kernel', 'retime', 'reorder'):
        raise ValueError('unexpected stages.py invocation')
    command = [sys.executable, '-B', str(root/'stage_adapter.py'), *script_args[1:]]
start = time.perf_counter()
result = subprocess.run(command)
row = dict(original_command=original, executed_command=command,
           seconds=time.perf_counter()-start, returncode=result.returncode)
with Path(os.environ['FRAME_ALGEBRA_COMMAND_LOG']).open('a') as output:
    output.write(json.dumps(row)+'\n')
sys.exit(result.returncode)
