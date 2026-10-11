"""Run the unchanged stages.py with only its two exact helpers substituted."""
import os
from pathlib import Path
import runpy
import sys

from common import SOURCE, sha
from exact_rows import key_of, rank_q

if not __debug__:
    raise RuntimeError('verification requires assertions enabled')
source = Path(os.environ['FRAME_ALGEBRA_SOURCE']).resolve()
code = source/'code'
for name in ('stagelib.py', 'stages.py'):
    if sha(code/name) != SOURCE['files']['code/'+name]:
        raise ValueError('adapter source hash mismatch: '+name)
sys.path.insert(0, str(code))
import stagelib
stagelib.rank_q = rank_q
stagelib.key_of = key_of
sys.argv = [str(code/'stages.py'), *sys.argv[1:]]
runpy.run_path(str(code/'stages.py'), run_name='__main__')
