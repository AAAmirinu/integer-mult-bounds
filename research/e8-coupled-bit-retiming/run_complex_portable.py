"""Run the pinned supplier entry point with only its regeneration subprocess adapted."""
from pathlib import Path
import runpy,sys,subprocess
SCRIPT=Path(sys.argv[1]).resolve();ADAPTER=Path(__file__).with_name('regen_portable.py')
original_run=subprocess.run
def portable_run(args,*a,**kw):
    if isinstance(args,(list,tuple)) and any(str(x).endswith('regen_check_e8.py') for x in args):
        target=next(x for x in args if str(x).endswith('regen_check_e8.py'))
        args=[sys.executable,'-B',str(ADAPTER),str(target)]
    return original_run(args,*a,**kw)
subprocess.run=portable_run
sys.argv=[str(SCRIPT)]
runpy.run_path(str(SCRIPT),run_name='__main__')
