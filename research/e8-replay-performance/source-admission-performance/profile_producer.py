"""Time every original producer subprocess; retain the complete regeneration."""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
import time

def main():
    assert __debug__ and sys.argv[1]=='--script'
    script=Path(sys.argv[2]).resolve()
    frozen=Path(__file__).resolve().parent.parent/'e8-pipeline-profile/pr358-source/vendor/source353354/pkg/bitword/producer/regenerate.py'
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha(script)==sha(frozen)
    sys.argv=[str(script),*sys.argv[3:]]
    assert len(sys.argv)==3 and sys.argv[1]=='--work'
    output=Path(sys.argv[2])
    original=subprocess.run
    rows=[]
    def timed(command,*args,**kwargs):
        before=time.perf_counter()
        result=original(command,*args,**kwargs)
        rows.append(dict(command=list(map(str,command)),seconds=time.perf_counter()-before,returncode=result.returncode))
        return result
    subprocess.run=timed
    try:runpy.run_path(str(script),run_name='__main__')
    finally:subprocess.run=original
    assert len(rows)==3 and all(r['returncode']==0 for r in rows)
    (output/'PRODUCER-TIMINGS.json').write_text(json.dumps(dict(stages=rows,
        implementation_sha256=sha(Path(__file__)),original_script_sha256=sha(script)),indent=2)+'\n')

if __name__=='__main__':main()
