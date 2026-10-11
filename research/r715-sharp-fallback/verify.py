"""Additive sharp bit invoice; default fresh original suppliers or explicit reuse.
Source closure is pinned by bytes, allowing descendant repository commits.
Prepared with substantial OpenAI Codex AI assistance; Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,json,os,shutil,signal,subprocess,sys,time

SELF=Path(__file__).resolve().parent
sys.path.insert(0,str(SELF/'code'))
from protocol import require,sha,read,exact,inventory,source_closure,package_integrity,parent_binding

def windows_job():
    import ctypes
    from ctypes import wintypes as W
    class Basic(ctypes.Structure):
        _fields_=[('ProcessTime',ctypes.c_longlong),('JobTime',ctypes.c_longlong),('Flags',W.DWORD),('Min',ctypes.c_size_t),('Max',ctypes.c_size_t),('Active',W.DWORD),('Affinity',ctypes.c_size_t),('Priority',W.DWORD),('Scheduling',W.DWORD)]
    class IO(ctypes.Structure):
        _fields_=[(name,ctypes.c_ulonglong) for name in ['ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes']]
    class Extended(ctypes.Structure):
        _fields_=[('Basic',Basic),('IO',IO),('ProcessMemory',ctypes.c_size_t),('JobMemory',ctypes.c_size_t),('PeakProcess',ctypes.c_size_t),('PeakJob',ctypes.c_size_t)]
    api=ctypes.WinDLL('kernel32',use_last_error=True)
    api.CreateJobObjectW.argtypes=[ctypes.c_void_p,W.LPCWSTR];api.CreateJobObjectW.restype=W.HANDLE
    api.SetInformationJobObject.argtypes=[W.HANDLE,ctypes.c_int,ctypes.c_void_p,W.DWORD];api.SetInformationJobObject.restype=W.BOOL
    api.AssignProcessToJobObject.argtypes=[W.HANDLE,W.HANDLE];api.AssignProcessToJobObject.restype=W.BOOL
    api.TerminateJobObject.argtypes=[W.HANDLE,W.UINT];api.TerminateJobObject.restype=W.BOOL
    api.CloseHandle.argtypes=[W.HANDLE];api.CloseHandle.restype=W.BOOL
    job=api.CreateJobObjectW(None,None);require(bool(job),'Windows Job Object creation failed')
    limits=Extended();limits.Basic.Flags=0x2000|0x200;limits.JobMemory=2<<30
    if not api.SetInformationJobObject(job,9,ctypes.byref(limits),ctypes.sizeof(limits)):
        api.CloseHandle(job);raise RuntimeError('Windows Job Object limit setup failed')
    return api,job

def run_group(cmd,log,env,timeout):
    """Bound the entire process group; preserve its log on failure/timeout."""
    options={'env':env,'stdout':log,'stderr':subprocess.STDOUT}
    api=job=None
    if os.name=='nt':
        api,job=windows_job();options['creationflags']=subprocess.CREATE_NEW_PROCESS_GROUP
    else:options['start_new_session']=True
    process=subprocess.Popen(list(map(str,cmd)),**options)
    if job and not api.AssignProcessToJobObject(job,int(process._handle)):
        process.kill();process.wait(timeout=5);api.CloseHandle(job)
        raise RuntimeError('Windows child could not enter bounded Job Object')
    try:return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name=='nt':
            require(bool(api.TerminateJobObject(job,1)),'Windows process-tree termination failed')
        else:
            try:os.killpg(process.pid,signal.SIGTERM)
            except ProcessLookupError:pass
            # The leader may exit on TERM while a grandchild ignores it. The
            # whole original group must be killed after the grace interval.
            time.sleep(5)
            try:os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        process.wait(timeout=5);raise RuntimeError('bounded process group timed out')
    finally:
        if job:api.CloseHandle(job)
        elif os.name!='nt':
            try:os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:pass

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    ap.add_argument('--research-root',type=Path,default=SELF.parent)
    ap.add_argument('--parent-output',type=Path,help='explicitly reuse a completed fresh full original PR473 replay')
    ap.add_argument('--fresh-timeout',type=int,default=1800)
    a=ap.parse_args();start=time.monotonic();out=a.output.resolve();research=a.research_root.resolve();repo=research.parent
    require(a.fresh_timeout>0,'timeout must be positive')
    require(not out.exists() and not out.is_relative_to(repo),'output must be new and outside the source checkout')
    if a.parent_output:require(not out.is_relative_to(a.parent_output.resolve()),'output must be outside reused parent output')
    package_integrity(SELF);pin=read(SELF/'SOURCE.json');closure=read(SELF/'pins/CLOSURE.json')
    require(sha(SELF/'pins/CLOSURE.json')==pin['closure_sha256'],'closure pin changed')
    source_closure(repo,closure)
    parent_package=repo/pin['parent_package'];up=parent_package/'upstream478'
    for source_name,cached in [('MANIFEST.json','parent-MANIFEST.json'),('SOURCE.json','parent-SOURCE.json'),('EXPECTED.json','parent-EXPECTED.json'),('UPSTREAM-INVENTORY.json','parent-UPSTREAM-INVENTORY.json'),('ADAPTED-PROVIDER-MANIFEST.json','parent-ADAPTED-PROVIDER-MANIFEST.json'),('COMPLEX-CONTENT.json','parent-COMPLEX-CONTENT.json')]:
        require(sha(parent_package/source_name)==sha(SELF/'pins'/cached),'cached original pin differs: '+source_name)
    out.mkdir(parents=True);steps=[]
    env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
    env.pop('PYTHONOPTIMIZE',None)
    try:
        parent=a.parent_output.resolve() if a.parent_output else out/'parent'
        if not a.parent_output:
            cmd=[sys.executable,'-B',repo/pin['parent_entrypoint'],parent,'--research-root',research]
            with (out/'fresh-original-parent.log').open('w',encoding='utf-8') as log:code=run_group(cmd,log,env,a.fresh_timeout)
            require(code==0,'fresh original parent failed; see preserved log/output')
            steps.append({'name':'fresh-original-parent','command':list(map(str,cmd)),'log_sha256':sha(out/'fresh-original-parent.log')})
        require(sha(SELF/'pins/parent-COMPLEX-CONTENT.json')==pin['complex_content_pin_sha256'],'canonical complex pin changed')
        # The original checker is in the immutable source closure. Re-run it
        # without optimization, then bind both its receipt and actual bytes.
        cmd=[sys.executable,'-B',parent_package/'verify_complex_content.py',parent/'provider',SELF/'pins/parent-COMPLEX-CONTENT.json',out/'COMPLEX-CONTENT-RECHECK.json']
        with (out/'complex-content-recheck.log').open('w',encoding='utf-8') as log:code=run_group(cmd,log,env,180)
        require(code==0,'fresh canonical complex recheck failed')
        require(exact(read(out/'COMPLEX-CONTENT-RECHECK.json'),read(parent/'COMPLEX-CONTENT-RECEIPT.json')),'original and repeated complex checker receipts differ')
        steps.append({'name':'complex-content-recheck','command':list(map(str,cmd)),'log_sha256':sha(out/'complex-content-recheck.log'),'receipt_sha256':sha(out/'COMPLEX-CONTENT-RECHECK.json')})
        baseline,bound=parent_binding(parent,read(SELF/'pins/parent-EXPECTED.json'),pin,closure,read(SELF/'pins/parent-COMPLEX-CONTENT.json'))
        provider_source=parent/'provider-source'
        provider_inventory=inventory(provider_source)
        provider_inventory.pop('MANIFEST.json',None)
        require(provider_inventory==read(SELF/'pins/parent-ADAPTED-PROVIDER-MANIFEST.json'),'actual copied provider source bytes differ')
        require(sha(provider_source/'MANIFEST.json')==pin['provider_manifest_sha256'],'actual provider manifest adapter differs')
        adapted=out/'code';adapted.mkdir()
        for name in ['assemble.py','sharp_bit_moment.py']:shutil.copyfile(SELF/'code'/name,adapted/name)
        env['PYTHONPATH']=str(up/'code')+(os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
        cmd=[sys.executable,'-B',adapted/'assemble.py',parent,parent/'bit',parent/'bit/AUDIT.json',out/'RESULT.json',
             '--complex',parent/'provider/complex','--engines',up/'engines','--inherited',up/'inherited',
             '--route-extra','6','--nine','bit','--label','Pinned replica84 PR473','--parent-kappa',baseline['kappa']]
        with (out/'sharp-assemble.log').open('w',encoding='utf-8') as log:code=run_group(cmd,log,env,180)
        require(code==0,'sharp complete invoice/outer assembly failed')
        result=read(out/'RESULT.json');expected=read(SELF/'EXPECTED.json')
        for key in ['kappa','bit_lower','complex_lower','binding_component','strict_outer_constraints']:
            require(exact(result[key],expected[key]),'sharp result differs: '+key)
        for key in ['complex_lower','binding_component','bit_profile','complex_profile','bit','complex','bit_template_sha256','complex_template_sha256','emitted_program_sha256']:
            require(exact(result[key],baseline[key]),'physical program/invoice unexpectedly changed: '+key)
        require(Q(result['kappa'])>Q(baseline['kappa']),'sharp kappa does not improve pinned parent')
        # Recheck all original sources after execution; a changed dependency invalidates the receipt.
        source_closure(repo,closure);package_integrity(SELF)
        receipt={'status':'PASS_SHARP_BIT_INVOICE_COMPLETED_FULL_PARENT_REUSED' if a.parent_output else 'PASS_SHARP_BIT_INVOICE_FRESH_FULL_PARENT',
                 'mode':'completed_full_parent_reuse' if a.parent_output else 'fresh_full_original_parent',
                 'kappa':result['kappa'],'reference_head':pin['reference_head'],'source_binding':'Exact unchanged original file closure; current repository HEAD may be a descendant.',
                 'package_manifest_sha256':sha(SELF/'MANIFEST.json'),'package_source_sha256':sha(SELF/'SOURCE.json'),'closure_sha256':sha(SELF/'pins/CLOSURE.json'),
                 'parent_output':str(parent),'parent_bindings':bound,'result_sha256':sha(out/'RESULT.json'),'assembler_log_sha256':sha(out/'sharp-assemble.log'),
                 'assembler_command':list(map(str,cmd)),'steps':steps,'python':sys.version,'elapsed_seconds':time.monotonic()-start,
                 'scope':'Changed sharper bit fallback arithmetic with complete original suppliers freshly replayed or explicitly reused; unchanged whole-owner programs/invoices. All retained all-size interfaces remain conditional.'}
        (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(receipt['status'],result['kappa'])
    except BaseException as error:
        (out/'FAILURE.json').write_text(json.dumps({'status':'NOT_COMPLETED','error':repr(error),'steps':steps,'scope':'No completed sharp scientific receipt is issued.'},indent=2)+'\n',encoding='utf-8');raise

if __name__=='__main__':main()
