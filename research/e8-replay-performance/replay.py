"""Portable entry point for complete offline PR358 performance replays.

All variants use the same two-worker starting driver. The scalar-baseline and
scalar pair isolate scalar admission; original and scalar compare the complete
accumulated execution changes. Every output directory must be new.
Prepared with OpenAI Codex assistance; Apache-2.0.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import time
from fetch import verify,SOURCE

ROOT=Path(__file__).resolve().parent

def integrity():
    expected=json.loads((ROOT/'MANIFEST.json').read_text())
    for path,digest in expected.items():
        p=ROOT/path
        if p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
            raise ValueError('package file changed: '+path)
    # Frozen source is acquired separately. Generated outputs belong in build/
    # or outside the package, and cannot enter the pinned implementation set.
    # Publication evidence is an output, never a replay input or cached proof.
    skip={'build','evidence','__pycache__','.venv'}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
            and not any(x in skip for x in p.relative_to(ROOT).parts)
            and not p.is_relative_to(SOURCE) and p.name!='MANIFEST.json' and p.suffix!='.pyc'}
    if actual!=set(expected):raise ValueError('unexpected/missing package files')
    return hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest()

def main():
    if not __debug__:raise RuntimeError('assertions must remain enabled')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--variant',choices=('original','shared','predecessor','scheduled','admission','combined','scalar-baseline','scalar'),required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--cxx',default='c++')
    ap.add_argument('--boost-include',type=Path,required=True)
    a=ap.parse_args();out=a.output.resolve()
    if out.exists() or out.is_relative_to(SOURCE):ap.error('fresh output outside frozen source required')
    if out.is_relative_to(ROOT) and not out.is_relative_to(ROOT/'build'):ap.error('outputs inside package must be under build/')
    if not hasattr(os,'fork') or not hasattr(os,'wait4'):ap.error('POSIX fork/wait4 required')
    compiler=shutil.which(a.cxx)
    if not compiler:ap.error('C++17 compiler not found')
    boost=a.boost_include.resolve()
    if not (boost/'boost/multiprecision/cpp_int.hpp').is_file():ap.error('Boost include root missing cpp_int.hpp')
    pin=integrity();verify(SOURCE)
    common=['--output',str(out),'--cxx',compiler,'--boost-include',str(boost)]
    if a.variant in ('original','shared'):
        command=[ROOT/'producer-prefix-sharing/run_native.py','--mode','reference' if a.variant=='original' else 'shared',*common]
    elif a.variant in ('predecessor','scheduled'):
        command=[ROOT/'predecessor-performance/run_native.py','--mode',a.variant,*common]
    elif a.variant=='admission':
        command=[ROOT/'source-admission-performance/run_native.py','--variant','admission',*common]
    elif a.variant=='combined':command=[ROOT/'source-admission-performance/run_combined.py',*common]
    else:command=[ROOT/'scalar-admission-performance/run_native.py','--variant','baseline' if a.variant=='scalar-baseline' else 'optimized',*common]
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',PYTHONHASHSEED='0',
        OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',E8_PROFILE_SOURCE=str(SOURCE))
    # Ensure even direct module loads use the copied exact admission package.
    env['PYTHONPATH']=str(SOURCE/'vendor/source353354')
    env.pop('PYTHONOPTIMIZE',None)
    before=resource.getrusage(resource.RUSAGE_CHILDREN);began=time.perf_counter()
    subprocess.run([sys.executable,'-B',*map(str,command)],check=True,env=env)
    seconds=time.perf_counter()-began;after=resource.getrusage(resource.RUSAGE_CHILDREN)
    verify(SOURCE)
    if integrity()!=pin:raise ValueError('package changed during replay')
    v=json.loads((out/'VERIFICATION.json').read_text())
    result=dict(status='PASS_PACKAGED_FULL_NATIVE_REPLAY',variant=a.variant,seconds=seconds,
        process_tree_cpu_seconds=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime),
        python=sys.version,platform=sys.platform,manifest_sha256=pin,source_commit='e76d7a94e6ad819e2aa9dc99083ecfa3e7842e0b',
        source_blobs=839,stages=len(v['fresh_stages']),kappa=v['kappa'],word_sha256=v['word_sha256'],
        command=[sys.executable,'-B',*map(str,command)],scope=v['scope'])
    (out/'PACKAGE-RUN.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2),flush=True)

if __name__=='__main__':main()
