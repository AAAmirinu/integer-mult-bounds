"""Aggregate distinct freshly compiled replay code objects without loss.

The usual pstats dictionary overwrites entries with identical file/name/line
keys when each corruption recompiles the scalar source. Keep their sum too.
"""
import cProfile
import hashlib
import json
from pathlib import Path
import runpy
import sys

ROOT=Path(__file__).resolve().parent
Original=cProfile.Profile

class CompleteProfile(Original):
    def dump_stats(self,filename):
        aggregate={}
        for entry in self.getstats():
            code=entry.code
            if isinstance(code,str):file,line,name='~',0,code
            else:file,line,name=code.co_filename,code.co_firstlineno,code.co_name
            key=(file,line,name)
            row=aggregate.setdefault(key,dict(file=file,line=line,name=name,calls=0,own_seconds=0.,cumulative_seconds=0.))
            row['calls']+=entry.callcount
            row['own_seconds']+=entry.inlinetime
            row['cumulative_seconds']+=entry.totaltime
        output=Path(filename).parent
        (output/'complete-profile.json').write_text(json.dumps(sorted(aggregate.values(),key=lambda r:-r['cumulative_seconds']),indent=2)+'\n')
        super().dump_stats(filename)

def main():
    cProfile.Profile=CompleteProfile
    sys.argv=[str(ROOT/'bench_scalar.py'),'--profile',*sys.argv[1:]]
    try:runpy.run_path(str(ROOT/'bench_scalar.py'),run_name='__main__')
    finally:cProfile.Profile=Original

if __name__=='__main__':main()
