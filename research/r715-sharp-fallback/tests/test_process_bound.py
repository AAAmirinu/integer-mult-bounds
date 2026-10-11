"""Harmless process-group timeout fixtures; no scientific replay."""
from pathlib import Path
import importlib.util,json,os,platform,sys,tempfile,time
SELF=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sharp_process_wrapper',SELF/'verify.py');wrapper=importlib.util.module_from_spec(spec);spec.loader.exec_module(wrapper)

def main():
    started=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='sharp-process-fixture-',dir=Path.cwd()) as temporary:
        root=Path(temporary);env=dict(os.environ)
        with (root/'positive.log').open('w') as log:
            status=wrapper.run_group([sys.executable,'-c','print("FIXTURE_ONLY positive")'],log,env,5)
        wrapper.require(status==0,'positive harmless process fixture failed')
        sentinel=root/'child-survived.txt'
        if os.name=='nt':child='import pathlib,time;time.sleep(2);pathlib.Path('+repr(str(sentinel))+').write_text("FIXTURE_ONLY survived")'
        else:child='import pathlib,time,signal;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(7);pathlib.Path('+repr(str(sentinel))+').write_text("FIXTURE_ONLY survived")'
        parent='import subprocess,sys,time;subprocess.Popen([sys.executable,"-c",'+repr(child)+']);print("FIXTURE_ONLY tree",flush=True);time.sleep(30)'
        with (root/'timeout.log').open('w') as log:
            try:wrapper.run_group([sys.executable,'-c',parent],log,env,0.5)
            except RuntimeError as error:wrapper.require('timed out' in str(error),'wrong timeout error')
            else:raise ValueError('process timeout fixture accepted')
        time.sleep(2.5)
        wrapper.require(not sentinel.exists(),'timed-out child survived process-group termination')
        normal_sentinel=root/'orphan-survived.txt'
        child='import pathlib,time;time.sleep(1);pathlib.Path('+repr(str(normal_sentinel))+').write_text("FIXTURE_ONLY orphan")'
        parent='import subprocess,sys;subprocess.Popen([sys.executable,"-c",'+repr(child)+']);print("FIXTURE_ONLY leader exit",flush=True)'
        with (root/'normal-leader-exit.log').open('w') as log:
            status=wrapper.run_group([sys.executable,'-c',parent],log,env,5)
        wrapper.require(status==0,'normal leader exit failed');time.sleep(1.5)
        wrapper.require(not normal_sentinel.exists(),'grandchild survived normal leader exit cleanup')
    result={'status':'PASS_PROCESS_GROUP_FIXTURES_ONLY','scientific_supplier_or_assembler_run':False,'positive_exit':0,'timeout_tree_rejected':True,'child_did_not_write_after_timeout':True,'normal_exit_orphan_cleaned':True,'term_ignoring_child_control':os.name!='nt','python':platform.python_version(),'wrapper_sha256':wrapper.sha(SELF/'verify.py'),'checker_sha256':wrapper.sha(Path(__file__)),'elapsed_seconds':time.monotonic()-started}
    if len(sys.argv)>1:
        out=Path(sys.argv[1]);wrapper.require(not out.exists(),'fixture receipt exists');out.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])

if __name__=='__main__':main()
