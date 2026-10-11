"""Fresh PR358 comparison: producer sharing, faster predecessor, idle-slot use."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parent
PREFIX = ROOT.parent/'producer-prefix-sharing'
PROFILE = ROOT.parent/'e8-pipeline-profile'
SOURCE = PROFILE/'pr358-source'
COMMIT = 'e76d7a94e6ad819e2aa9dc99083ecfa3e7842e0b'
DRIVER_PIN = 'fbeb4e343101401bb478e8f2454a0a2a2b834891ca85320ccb8dfa5da714088d'
PREFIX_PIN = '3cf6098047ae7c87a967a10ecc7b96acee2e7b5a312918f0611891baadbc1596'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
verify_source = runpy.run_path(str(PREFIX/'run_native.py'))['verify_source']


def scheduled_namespace(driver, early_results, after_reference):
    """Change only the reference worker and fresh early-stage dispatch.

    Original argument expressions, all checks, and recorded stage order remain.
    The early results are futures from this run, never receipts from a prior run.
    """
    assert sha(driver) == DRIVER_PIN
    tree = ast.parse(driver.read_text())
    main = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    execute = next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='execute')
    inserted = ast.parse("""
if label in _early_results:
    expected, row = _early_results[label]
    assert list(map(str,args)) == expected, 'early job command changed'
    return row
""").body
    execute.body[0:0] = inserted
    count = 0
    for node in ast.walk(main):
        if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='reference' for t in node.targets):
            call = node.value
            assert ast.dump(call.func)==ast.dump(ast.parse('pool.submit',mode='eval').body)
            assert len(call.args)==3 and isinstance(call.args[0],ast.Name) and call.args[0].id=='execute'
            call.args[0:1] = [ast.Name(id='_after_reference',ctx=ast.Load()),ast.Name(id='execute',ctx=ast.Load())]
            count += 1
    assert count == 1
    # These C++ jobs read the admitted base/candidate but write disjoint bank/
    # and charts/ directories. Geometry admission consumes both after the join.
    body=next(n for n in main.body if isinstance(n,ast.Try)).body
    pairs=0
    for i in range(len(body)-1):
        nodes=body[i:i+2]
        if all(isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)
               and isinstance(n.value.func,ast.Name) and n.value.func.id=='run'
               for n in nodes):
            calls=[n.value for n in nodes]
            if [ast.literal_eval(c.args[0]) for c in calls]==['bank-frames-and-assignment','changed-charts']:
                replacement=ast.parse("""
with ThreadPoolExecutor(max_workers=2) as geometry_pool:
    bank_job=geometry_pool.submit(execute)
    chart_job=geometry_pool.submit(execute)
    stages.extend([bank_job.result(),chart_job.result()])
""").body
                replacement[0].body[0].value.args.extend(calls[0].args)
                replacement[0].body[1].value.args.extend(calls[1].args)
                body[i:i+2]=replacement
                pairs+=1
                break
    assert pairs==1
    ns = dict(__name__='scheduled_native_driver',__file__=str(driver),
              _early_results=early_results,_after_reference=after_reference)
    exec(compile(ast.fix_missing_locations(tree),str(driver),'exec'),ns)
    return ns


def main():
    assert __debug__
    ap = argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--mode',choices=('baseline','predecessor','scheduled'),required=True)
    ap.add_argument('--cxx',required=True)
    ap.add_argument('--boost-include',type=Path,required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert not out.exists() and not out.is_relative_to(SOURCE)
    begin = time.perf_counter()
    verify_source()
    assert sha(PREFIX/'share_source.py')==PREFIX_PIN
    os.environ.update(PYTHONDONTWRITEBYTECODE='1',PYTHONNOUSERSITE='1',
        OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',E8_PROFILE_SOURCE=str(SOURCE))
    os.environ.pop('PYTHONOPTIMIZE',None)
    driver = PROFILE/'parallel_verify358.py'
    assert sha(driver)==DRIVER_PIN
    early = {}
    def after_reference(execute,label,command):
        row = execute(label,command)
        jobs = [('immutable-complex-reserve',[sys.executable,'-B',str(SOURCE/'vendor/complex-reserve/verify.py'),'--output',str(out/'complex-reserve')])]
        for name in ('legality','columns','changed-charts','banks','invoice'):
            cmd = [args.cxx,'-O2','-std=c++17','-I',str(SOURCE/'vendor/native'),
                   '-I',str(args.boost_include.resolve()),str(SOURCE/'code'/(name+'.cpp')),'-o',str(out/'bin'/name)]
            jobs.append(('compile-'+name,cmd))
        for name,cmd in jobs:
            early[name]=(cmd,execute(name,cmd))
        return row
    ns = scheduled_namespace(driver,early,after_reference) if args.mode=='scheduled' else runpy.run_path(str(driver),run_name='native_predecessor_driver')
    original_run = subprocess.run
    calls = []
    lock = threading.Lock()
    source_script = SOURCE/'vendor/source353354/verify_source.py'
    proof_script = SOURCE/'vendor/predecessor/verify.py'
    def dispatch(command,*pos,**kw):
        old = list(map(str,command)); new = old
        kind = None
        if str(source_script) in old:
            assert len(old)==5 and old[:3]==[sys.executable,'-B',str(source_script)] and old[3]=='--output'
            kind = 'source'
            new=[sys.executable,'-B',str(PREFIX/'share_source.py'),'--source',str(source_script.parent),'--output',old[4]]
        elif str(proof_script) in old:
            assert len(old)==5 and old[:3]==[sys.executable,'-B',str(proof_script)] and old[3]=='--output'
            kind = 'predecessor'
            if args.mode!='baseline':
                new=[sys.executable,'-B',str(ROOT/'proof_adapter.py'),'--output',old[4]]
        start = time.perf_counter()
        try:
            return original_run(new,*pos,**kw)
        finally:
            if kind:
                with lock:
                    calls.append(dict(kind=kind,original=old,executed=new,seconds=time.perf_counter()-start))
    subprocess.run = dispatch
    sys.argv = [str(driver),'--output',str(out),'--cxx',args.cxx,'--boost-include',str(args.boost_include.resolve())]
    try:
        ns['main']()
    finally:
        subprocess.run = original_run
    elapsed = time.perf_counter()-begin
    verify_source()
    assert sha(driver)==DRIVER_PIN and sha(PREFIX/'share_source.py')==PREFIX_PIN
    v = json.loads((out/'VERIFICATION.json').read_text())
    assert len(v['fresh_stages'])==24 and v['inputs_unchanged']
    assert sorted(x['kind'] for x in calls)==['predecessor','source']
    if args.mode=='scheduled':
        assert len(early)==6
    pins = {str(p):sha(p) for p in (Path(__file__),ROOT/'proof_adapter.py',ROOT/'fast_transcript.py',ROOT/'integer_factors.py',PREFIX/'share_source.py',driver)}
    report = dict(status='PASS_FULL_NATIVE_PREDECESSOR_EXPERIMENT',mode=args.mode,seconds=elapsed,
                  source_commit=COMMIT,source_files_checked=839,source_files_unchanged=True,
                  implementation_hashes=pins,launches=calls,early_jobs=list(early),
                  kappa=v['kappa'],word_sha256=v['word_sha256'],scope=v['scope'],python=sys.version)
    (out/'NATIVE-PERFORMANCE-RUN.json').write_text(json.dumps(report,indent=2)+'\n')
    print(args.mode,round(elapsed,3),'seconds',flush=True)


if __name__=='__main__':
    main()
