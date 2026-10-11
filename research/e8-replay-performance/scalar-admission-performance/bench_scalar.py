"""Fresh scalar-only diagnostic with exact source inputs and CPU timings."""
import argparse
import cProfile
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import pstats
import resource
import sys
import time

ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT.parent/'e8-pipeline-profile/pr358-source/vendor/source353354/pkg'
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def main():
    assert __debug__
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--profile',action='store_true')
    ap.add_argument('--variant',choices=('baseline','optimized'),default='baseline')
    args=ap.parse_args()
    out=args.output.resolve();assert not out.exists();out.mkdir(parents=True)
    os.environ.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    sys.path.insert(0,str(PACKAGE))
    prepare=load('bench_prepare',PACKAGE/'prepare.py')
    context=prepare.prepare()
    physical=load('bench_physical',PACKAGE/'code/physical527.py').run(dict(context),context['SOURCE_TEXT'])
    parity=load('bench_parity',PACKAGE/'parity_transform.py').run(physical)
    scalar=load('bench_scalar',PACKAGE/'scalar_check.py')
    if args.variant=='optimized':
        from scalar_adapter import install
        install(scalar)
    begin=time.perf_counter();cpu=time.process_time()
    if args.profile:
        profiler=cProfile.Profile()
        result=profiler.runcall(scalar.run,context,parity['records'],print,len(parity['initial_state']))
        profiler.dump_stats(str(out/'scalar.prof'))
        stats=pstats.Stats(str(out/'scalar.prof'))
        functions=[dict(file=file,line=line,name=name,calls=calls,own_seconds=own,cumulative_seconds=cumulative)
            for (file,line,name),(primitive,calls,own,cumulative,callers) in stats.stats.items()]
        (out/'profile.json').write_text(json.dumps(sorted(functions,key=lambda x:-x['cumulative_seconds'])[:60],indent=2)+'\n')
    else:result=scalar.run(context,parity['records'],print,len(parity['initial_state']))
    elapsed=time.perf_counter()-begin;cpu=time.process_time()-cpu
    (out/'source-scalar.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    report=dict(seconds=elapsed,cpu_seconds=cpu,variant=args.variant,profile=args.profile,
        implementation_sha256=SHA(__file__),scalar_sha256=SHA(PACKAGE/'scalar_check.py'),
        word_sha256=SHA(PACKAGE/'scalar/word.py'),peak_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    if args.variant=='optimized':report['adapter']=scalar._performance_report()
    (out/'BENCHMARK.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report,flush=True)

if __name__=='__main__':main()
