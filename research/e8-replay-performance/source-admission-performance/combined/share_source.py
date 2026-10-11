"""Combine the admitted prefix with the exact generator inverse change."""
from pathlib import Path
import runpy
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent

def main():
    original=subprocess.run
    def dispatch(command,*args,**kwargs):
        cmd=list(map(str,command))
        if len(cmd)>2 and cmd[2]==str(ROOT/'profile_producer.py'):
            cmd[2]=str(ROOT/'profile_producer_fast.py')
        return original(cmd,*args,**kwargs)
    subprocess.run=dispatch
    try:runpy.run_path(str(ROOT/'share_source.py'),run_name='__main__')
    finally:subprocess.run=original

if __name__=='__main__':main()
