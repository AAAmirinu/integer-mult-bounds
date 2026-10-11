"""Full native PR358 replay, with the same two-worker source-proof schedule.

Reference mode runs the existing measured parallel driver. Sharing mode only
replaces the source353354 verifier launch with the external prefix adapter.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import threading
import time

ROOT=Path(__file__).resolve().parent
PROFILE=ROOT.parent/'e8-pipeline-profile'
SOURCE=PROFILE/'pr358-source'
COMMIT='e76d7a94e6ad819e2aa9dc99083ecfa3e7842e0b'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def verify_source():
    meta=json.loads((PROFILE/'pr358-tree.json').read_text())
    assert meta['commit']==COMMIT
    expected={x['path']:x for x in meta['files']}
    paths=list(SOURCE.rglob('*'))
    assert not any(p.is_symlink() for p in paths)
    assert {p.relative_to(SOURCE).as_posix() for p in paths if p.is_file()}==set(expected)
    for name,row in expected.items():
        data=(SOURCE/name).read_bytes()
        assert len(data)==row['size']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['sha'],name


def main():
    if not __debug__:
        raise RuntimeError('assertions required')
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--mode',choices=('reference','shared'),required=True)
    ap.add_argument('--cxx',required=True)
    ap.add_argument('--boost-include',required=True)
    args=ap.parse_args()
    out=args.output.resolve()
    if out.exists() or out.is_relative_to(SOURCE):
        ap.error('fresh external output required')
    begin=time.perf_counter()
    verify_source()
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',
             OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',E8_PROFILE_SOURCE=str(SOURCE))
    env.pop('PYTHONOPTIMIZE',None)
    os.environ.update(env)
    driver=PROFILE/'parallel_verify358.py'
    # This driver itself pins the immutable original verify.py before executing.
    driver_sha=sha(driver)
    namespace=runpy.run_path(str(driver),run_name='native_prefix_driver')
    original_run=subprocess.run
    lock=threading.Lock()
    calls=[]
    target=SOURCE/'vendor/source353354/verify_source.py'
    def dispatch(command,*pos,**kw):
        original=list(map(str,command))
        actual=original
        if str(target) in original:
            assert original[:3]==[sys.executable,'-B',str(target)]
            assert len(original)==5 and original[3]=='--output'
            if args.mode=='shared':
                actual=[sys.executable,'-B',str(ROOT/'share_source.py'),
                        '--source',str(target.parent),'--output',original[4]]
        start=time.perf_counter()
        try:
            result=original_run(actual,*pos,**kw)
            status=result.returncode
        except subprocess.CalledProcessError as e:
            status=e.returncode
            raise
        finally:
            if str(target) in original:
                with lock:
                    calls.append(dict(original=original,executed=actual,seconds=time.perf_counter()-start))
        return result
    subprocess.run=dispatch
    sys.argv=[str(driver),'--output',str(out),'--cxx',args.cxx,'--boost-include',args.boost_include]
    try:
        namespace['main']()
    finally:
        subprocess.run=original_run
    elapsed=time.perf_counter()-begin
    verify_source()
    assert sha(driver)==driver_sha
    verification=json.loads((out/'VERIFICATION.json').read_text())
    assert len(verification['fresh_stages'])==24 and verification['inputs_unchanged']
    assert len(calls)==1
    report=dict(status='PASS_FULL_NATIVE_PR358_PREFIX_EXPERIMENT',mode=args.mode,
                seconds=elapsed,source_commit=COMMIT,source_files_checked=839,
                source_files_unchanged=True,driver_sha256=driver_sha,
                runner_sha256=sha(__file__),source_launch=calls[0],
                kappa=verification['kappa'],word_sha256=verification['word_sha256'],
                scope=verification['scope'],python=sys.version)
    if args.mode=='shared':
        report['prefix_adapter_sha256']=sha(ROOT/'share_source.py')
        report['prefix_statistics']=json.loads((out/'source353354/PREFIX-SHARING.json').read_text())
    (out/'NATIVE-PREFIX-RUN.json').write_text(json.dumps(report,indent=2)+'\n')
    print(args.mode,round(elapsed,3),'seconds',flush=True)


if __name__=='__main__':
    main()
