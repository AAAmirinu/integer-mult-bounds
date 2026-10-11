"""Keep native checker receipt paths ASCII-relative on Windows."""
from pathlib import Path
import os,subprocess,sys
def arguments(args,cwd=None):
    cwd=Path(cwd or os.getcwd()).resolve();result=[]
    for i,value in enumerate(args):
        path=Path(str(value))
        if i and path.is_absolute() and path.is_relative_to(cwd):value=path.relative_to(cwd).as_posix()
        result.append(str(value))
    return result
if __name__=='__main__':raise SystemExit(subprocess.run(arguments(sys.argv[1:])).returncode)
