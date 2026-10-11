"""Keep previous prefix/generator gains; instrument or optimize scalar replay."""
import hashlib
import json
import os
from pathlib import Path
import resource
import runpy
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'source-admission-performance'
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    assert SHA(PREVIOUS/'share_source.py')=='d6633b529216350547df4dd54e24dd7124240a66d7795a4c521864de740581ff'
    variant=os.environ['SCALAR_ADMISSION_VARIANT']
    assert variant in ('baseline','optimized')
    output=Path(sys.argv[sys.argv.index('--output')+1]).resolve()
    namespace=runpy.run_path(str(PREVIOUS/'share_source.py'),run_name='scalar_source_adapter')
    original_load=namespace['base']['load']
    def load(name,path):
        loaded=original_load(name,path)
        if name=='fresh_admission':
            source_load=loaded.load
            def load_scalar(name,path):
                scalar=source_load(name,path)
                if name=='src353_scalar':
                    if variant=='optimized':
                        from scalar_adapter import install
                        install(scalar)
                    original=scalar.run
                    def checked(*args,**kwargs):
                        began=time.perf_counter();cpu=time.process_time()
                        result=original(*args,**kwargs)
                        report=dict(status='PASS_FRESH_SCALAR_ADMISSION',variant=variant,
                            seconds=time.perf_counter()-began,cpu_seconds=time.process_time()-cpu,
                            peak_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                            implementation_sha256=SHA(__file__),
                            majorant=result['majorant'],original_controls=len(result['controls']))
                        if variant=='optimized':report['adapter']=scalar._performance_report()
                        (output/'SCALAR-PERFORMANCE.json').write_text(json.dumps(report,indent=2)+'\n')
                        return result
                    scalar.run=checked
                return scalar
            loaded.load=load_scalar
        return loaded
    namespace['base']['load']=load
    original_run=subprocess.run
    def dispatch(command,*args,**kwargs):
        cmd=list(map(str,command))
        if len(cmd)>2 and cmd[2]==str(PREVIOUS/'profile_producer.py'):
            cmd[2]=str(PREVIOUS/'profile_producer_fast.py')
        return original_run(cmd,*args,**kwargs)
    subprocess.run=dispatch
    try:namespace['main']()
    finally:subprocess.run=original_run

if __name__=='__main__':main()
