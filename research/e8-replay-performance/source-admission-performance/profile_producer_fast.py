"""Keep producer timing/comparison, substitute only exact generator inverses."""
from pathlib import Path
import runpy
import subprocess
import sys

ROOT=Path(__file__).resolve().parent

def main():
    original=subprocess.run
    def dispatch(command,*args,**kwargs):
        cmd=list(map(str,command))
        if len(cmd)>2 and Path(cmd[2]).name=='paired_cube_bit_word.py':
            assert cmd[:2]==[sys.executable,'-B'] and cmd[3]=='--p' and cmd[4]=='10' and cmd[5]=='--out' and len(cmd)==7
            receipt=Path(cmd[6]).parent/'GENERATOR-PERFORMANCE.json'
            cmd=[sys.executable,'-B',str(ROOT/'generator_adapter.py'),
                 '--script',cmd[2],'--inverse','euclid','--receipt',str(receipt),*cmd[3:]]
        return original(cmd,*args,**kwargs)
    subprocess.run=dispatch
    try:runpy.run_path(str(ROOT/'profile_producer.py'),run_name='__main__')
    finally:subprocess.run=original

if __name__=='__main__':main()
