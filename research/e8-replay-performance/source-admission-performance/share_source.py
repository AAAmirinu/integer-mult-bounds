"""Reuse the freshly admitted prefix, with scalar admission isolated by fork.

The original source verifier, complete admission, producer regeneration and six
consumers still run. No saved receipt substitutes for an execution.
"""
import contextlib
import hashlib
import json
import os
from pathlib import Path
import pickle
import runpy
import subprocess
import sys
import threading
import time
import traceback

ROOT = Path(__file__).resolve().parent
OLD = ROOT.parent/'producer-prefix-sharing/share_source.py'
SHA = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert SHA(OLD)=='3cf6098047ae7c87a967a10ecc7b96acee2e7b5a312918f0611891baadbc1596'
base = runpy.run_path(str(OLD),run_name='admission_prefix_base')
FROZEN = base['FROZEN']
ADMISSION_PIN = 'bf96be3744852d68cd3a8321f76601cb14f7958c9602d09cab2f0e815bb6f453'
OriginalBank = base['PrefixBank']


def equal_packages(frozen, copied):
    """Require identical input bytes and file sets, including discovery pins."""
    def inventory(root):
        paths = list(root.rglob('*'))
        assert all(not p.is_symlink() for p in paths)
        return {p.relative_to(root).as_posix(): SHA(p) for p in paths if p.is_file()}
    left,right=inventory(frozen),inventory(copied)
    assert left==right,'copied producer inputs differ from admitted package'
    return hashlib.sha256(json.dumps(left,sort_keys=True).encode()).hexdigest()


def isolated_value(callback, stdout):
    """Return a fresh child result without allowing mutation of retained objects.

    Pickle only transports a value freshly made by this child over a private
    pipe. There is no file or external pickle input. Read before wait to avoid
    blocking a child with a result larger than the pipe buffer.
    """
    assert threading.active_count()==1
    sys.stdout.flush();sys.stderr.flush();stdout.flush()
    reader,writer=os.pipe()
    pid=os.fork()
    if pid==0:
        os.close(reader)
        status=0
        try:
            os.dup2(stdout.fileno(),1);os.dup2(stdout.fileno(),2)
            value=callback()
            with os.fdopen(writer,'wb') as stream:
                pickle.dump(value,stream,protocol=5)
        except BaseException:
            traceback.print_exc();status=1
        finally:
            sys.stdout.flush();sys.stderr.flush()
        os._exit(status)
    os.close(writer)
    try:
        with os.fdopen(reader,'rb') as stream:
            value=pickle.load(stream)
    except EOFError:
        value=None
    finally:
        _,status,usage=os.wait4(pid,0)
    assert os.waitstatus_to_exitcode(status)==0,'isolated scalar admission failed'
    return value,usage.ru_maxrss


class AdmissionBank(base['PrefixBank']):
    def admit(self, command, stdout):
        assert not self.initialized and not self.prefixes
        assert command==[sys.executable,'-B',str(FROZEN/'source_admission.py'),
                         '--output',str(self.pkg.parent/'newbase-source-admission')]
        assert SHA(FROZEN/'source_admission.py')==ADMISSION_PIN
        package_pin=equal_packages(FROZEN/'pkg',self.pkg)
        module=base['load']('fresh_admission',FROZEN/'source_admission.py')
        original_load=module.load
        seen=[]
        scalar=[]
        def capture(name,path):
            loaded=original_load(name,path)
            specs={'src353_prepare':('prepare','prepare'),
                   'src353_physical':('run','physical'),
                   'src353_parity':('run','parity')}
            if name in specs:
                attr,label=specs[name]
                original=getattr(loaded,attr)
                def fresh(*args,**kwargs):
                    value=self.timed(label,lambda:original(*args,**kwargs))
                    seen.append(label)
                    if label=='prepare':self.prepared=value
                    elif label=='physical':self.physical=value
                    else:
                        self.prefixes['parity']=value
                        self.initialized=True
                    return value
                setattr(loaded,attr,fresh)
            elif name=='src353_scalar':
                original=loaded.run
                def checked(*args,**kwargs):
                    before=self.fingerprint()
                    begin=time.perf_counter()
                    value,rss=isolated_value(lambda:original(*args,**kwargs),stdout)
                    assert self.fingerprint()==before
                    scalar.append(dict(seconds=time.perf_counter()-begin,
                        parent_fingerprint=before,parent_fingerprint_unchanged=True,
                        child_peak_rss_platform_units=rss))
                    return value
                loaded.run=checked
            return loaded
        module.load=capture
        with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stdout):
            module.admission(FROZEN/'pkg',Path(command[-1]))
        assert seen==['prepare','physical','parity'] and len(scalar)==1
        assert hashlib.sha256(self.prefixes['parity']['records'].tobytes()).hexdigest()=='e7d20c66176ff94e435e1462f749699316e392912ba04658318c1b36784400ea'
        assert equal_packages(FROZEN/'pkg',self.pkg)==package_pin
        # Future consumers import the copied package. Existing admitted objects
        # retain their original module globals; both pin tables are byte-equal.
        copied_pins=base['load']('word_pins',self.pkg/'word_pins.py')
        assert copied_pins.RECORD is None
        sys.path.insert(0,str(self.pkg))
        self.admission=dict(status='PASS_FRESH_ADMISSION_PREFIX_HANDOFF',
            input_inventory_sha256=package_pin,scalar=scalar,
            admission_source_sha256=ADMISSION_PIN,
            implementation_sha256=SHA(__file__),
            inherited_prefix_fingerprint=self.fingerprint(),
            scope='Original complete admission; fresh scalar replay in an isolated child; byte-equal package inputs.')
        (self.pkg.parent/'ADMISSION-PREFIX.json').write_text(json.dumps(self.admission,indent=2)+'\n')
        return 0


def main():
    assert __debug__
    mode=os.environ.get('SOURCE_PREFIX_MODE','admission')
    assert mode in ('baseline','admission')
    banks=[]
    def bank_factory(*args,**kwargs):
        bank=(AdmissionBank if mode=='admission' else OriginalBank)(*args,**kwargs)
        banks.append(bank)
        return bank
    base['main'].__globals__['PrefixBank']=bank_factory
    original_run=subprocess.run
    def dispatch(command,*args,**kwargs):
        cmd=list(map(str,command))
        if mode=='admission' and len(cmd)>2 and cmd[2]==str(FROZEN/'source_admission.py'):
            assert len(banks)==1 and not args
            assert set(kwargs)=={'stdout','stderr','env'} and kwargs['stderr']==subprocess.STDOUT
            return subprocess.CompletedProcess(cmd,banks[0].admit(cmd,kwargs['stdout']))
        if len(cmd)>2 and Path(cmd[2]).name=='regenerate.py':
            cmd=[sys.executable,'-B',str(ROOT/'profile_producer.py'),'--script',cmd[2],*cmd[3:]]
        return original_run(cmd,*args,**kwargs)
    subprocess.run=dispatch
    try:
        base['main']()
    finally:
        subprocess.run=original_run


if __name__=='__main__':main()
