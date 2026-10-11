"""PR358/source353354: fresh producer prefixes shared by isolated consumers.

POSIX experiment. Each original consumer runs in a fresh forked child. Its
three identical prefix-building calls are substituted by inherited fresh values.
Optional deeper prefixes run once after their selections have been regenerated.
No admission checks, searches or downstream consumers are skipped.
"""
import argparse
import ast
import contextlib
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import runpy
import subprocess
import sys
import threading
import time
import traceback

ROOT=Path(__file__).resolve().parent
PROFILE=ROOT.parent/'e8-pipeline-profile'
FROZEN=PROFILE/'pr358-source/vendor/source353354'
READ=lambda p:json.loads(Path(p).read_text())
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

# Exact AST expressions at the pinned source commit. Each must occur once.
EXPRESSIONS={
 'base-export':[
  "load('p527prep', P / 'prepare.py').prepare()",
  "phys.run(context, context['SOURCE_TEXT'], output_dir=None)",
  "load('p527par', P / 'parity_transform.py').run(prod, output_dir=None)"],
 'descent-selection':[
  "load('portable527_prepare', root / 'prepare.py').prepare()",
  "phys.run(dict(context), context['SOURCE_TEXT'], output_dir=None)",
  "load('portable527_parity', root / 'parity_transform.py').run(producer, output_dir=None)"],
 'target-selection':[
  "load('portable527_prepare', root / 'prepare.py').prepare()",
  "load('portable527_physical', root / 'code/physical527.py').run(dict(context), context['SOURCE_TEXT'], output_dir=None)",
  "load('portable527_parity', root / 'parity_transform.py').run(producer, output_dir=None)"],
 'restore-selection':[
  "load('portable527_prepare', ROOT / 'prepare.py').prepare()",
  "load('portable527_physical', ROOT / 'code/physical527.py').run(dict(ctx), ctx['SOURCE_TEXT'], output_dir=None)",
  "load('portable527_parity', ROOT / 'parity_transform.py').run(producer)"],
 'sink-selection':[
  "load('portable527_prepare', ROOT / 'prepare.py').prepare()",
  "load('portable527_physical', ROOT / 'code/physical527.py').run(dict(ctx), ctx['SOURCE_TEXT'], output_dir=None)",
  "load('portable527_parity', ROOT / 'parity_transform.py').run(producer)"],
 'stages-export':[
  "load('portable527_prepare', P / 'prepare.py').prepare()",
  "load('portable527_physical', P / 'code/physical527.py').run(context, context['SOURCE_TEXT'], output_dir=None)",
  "load('portable527_parity', P / 'parity_transform.py').run(run)"],
}
RELATIVES={
 'base-export':'code/export_p10.py',
 'descent-selection':'pkg/discovery/descent_search.py',
 'target-selection':'pkg/discovery/target_search.py',
 'restore-selection':'pkg/discovery/build_restore_selection.py',
 'sink-selection':'pkg/discovery/build_sink_selection.py',
 'stages-export':'code/export_stages.py',
}
DEEP={
 'target-selection':("load('portable527_descent', root / 'descent_transform.py').run(pr, output_dir=None, selection_path=dsel)","_shared_stage('descent')"),
 'restore-selection':("load('portable527_' + st, ROOT / (st + '.py')).run(run)","_shared_stage(st.removesuffix('_transform'))"),
 'sink-selection':("load('portable527_' + st, ROOT / (st + '.py')).run(run)","_shared_stage(st.removesuffix('_transform'))"),
 'stages-export':("load('portable527_' + st, P / (st + '_transform.py')).run(run)","_shared_stage(st)"),
}


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    sys.modules[name]=result
    spec.loader.exec_module(result)
    return result


def compile_consumer(label,path,deep):
    tree=ast.parse(path.read_text())
    replacements={ast.dump(ast.parse(expr,mode='eval').body):replacement
                  for expr,replacement in zip(EXPRESSIONS[label],
                      ('_shared_prepare()','_shared_physical()','_shared_parity()'))}
    if deep and label in DEEP:
        expr,replacement=DEEP[label]
        replacements[ast.dump(ast.parse(expr,mode='eval').body)]=replacement
    counts={key:0 for key in replacements}
    class Replace(ast.NodeTransformer):
        def visit_Call(self,node):
            key=ast.dump(node)
            if key in replacements:
                counts[key]+=1
                return ast.copy_location(ast.parse(replacements[key],mode='eval').body,node)
            return self.generic_visit(node)
    tree=Replace().visit(tree)
    if any(count!=1 for count in counts.values()):
        raise ValueError('unexpected consumer prefix syntax: '+label)
    return compile(ast.fix_missing_locations(tree),str(path),'exec'),len(counts)


class PrefixBank:
    def __init__(self,pkg,deep):
        self.pkg=pkg
        self.deep=deep
        self.prefixes={}
        self.fresh=[]
        self.consumers=[]
        self.initialized=False
        self.expected=READ(FROZEN/'EXPECTED.json')

    def timed(self,name,callback):
        begin=time.perf_counter()
        value=callback()
        self.fresh.append(dict(prefix=name,seconds=time.perf_counter()-begin))
        return value

    def advance(self,label):
        if not self.initialized:
            sys.path.insert(0,str(self.pkg))
            import word_pins
            assert Path(word_pins.__file__).resolve()==self.pkg/'word_pins.py'
            assert word_pins.RECORD is None
            self.prepared=self.timed('prepare',lambda:load('prefix_prepare',self.pkg/'prepare.py').prepare())
            self.physical=self.timed('physical',lambda:load('prefix_physical',self.pkg/'code/physical527.py').run(dict(self.prepared),self.prepared['SOURCE_TEXT'],output_dir=None))
            self.prefixes['parity']=self.timed('parity',lambda:load('prefix_parity',self.pkg/'parity_transform.py').run(self.physical))
            assert hashlib.sha256(self.prefixes['parity']['records'].tobytes()).hexdigest()=='e7d20c66176ff94e435e1462f749699316e392912ba04658318c1b36784400ea'
            self.initialized=True
        if not self.deep:
            return
        needed={'target-selection':'descent','restore-selection':'target','sink-selection':'restore'}.get(label)
        if needed is not None:
            before={'descent':'parity','target':'descent','restore':'target'}[needed]
            assert before in self.prefixes and needed not in self.prefixes
            assert SHA(self.pkg/(needed+'-selection.json'))==self.expected['selection/'+needed+'-selection.json']
            module=load('prefix_'+needed,self.pkg/(needed+'_transform.py'))
            self.prefixes[needed]=self.timed(needed,lambda:module.run(self.prefixes[before]))

    def fingerprint(self):
        current=self.prefixes[list(self.prefixes)[-1]]
        W,C=current['W'],current['C']
        digest=hashlib.sha256()
        for name,value in self.prefixes.items():
            digest.update(name.encode())
            digest.update(value['records'].tobytes())
            digest.update(json.dumps(value['initial_state'],sort_keys=True).encode())
        for value in (C.B,C.A,C.dimf,sorted((f,B) for B,f in W.frame_ids.items())):
            digest.update(json.dumps(value,sort_keys=True,default=str,separators=(',',':')).encode())
        return digest.hexdigest()

    def stage(self,name):
        if name in self.prefixes:
            return self.prefixes[name]
        # Only sink is not reused by the exporter: it must run freshly there.
        assert name=='sink' and 'restore' in self.prefixes
        return load('prefix_child_sink',self.pkg/'sink_transform.py').run(self.prefixes['restore'])

    def execute(self,label,script,argv,stdout):
        assert label==list(RELATIVES)[len(self.consumers)]
        with contextlib.redirect_stdout(stdout):
            self.advance(label)
        code,replaced=compile_consumer(label,script,self.deep)
        before=self.fingerprint()
        sys.stdout.flush();sys.stderr.flush();stdout.flush()
        assert threading.active_count()==1,'fork worker must have one Python thread'
        begin=time.perf_counter()
        pid=os.fork()
        if pid==0:
            status=0
            try:
                os.dup2(stdout.fileno(),1);os.dup2(stdout.fileno(),2)
                sys.argv=[str(script),*argv]
                namespace={'__name__':'__main__','__file__':str(script),'__package__':None,
                    '_shared_prepare':lambda:self.prepared,
                    '_shared_physical':lambda:self.physical,
                    '_shared_parity':lambda:self.prefixes['parity'],
                    '_shared_stage':self.stage}
                exec(code,namespace)
            except BaseException:
                traceback.print_exc();status=1
            finally:
                sys.stdout.flush();sys.stderr.flush()
            os._exit(status)
        _,wait_status,usage=os.wait4(pid,0)
        status=os.waitstatus_to_exitcode(wait_status)
        assert self.fingerprint()==before,'child modified parent prefix'
        self.consumers.append(dict(consumer=label,seconds=time.perf_counter()-begin,
            returncode=status,ast_calls_substituted=replaced,parent_fingerprint_unchanged=True,
            parent_fingerprint=before,child_peak_rss_platform_units=usage.ru_maxrss,
            child_user_cpu_seconds=usage.ru_utime,child_system_cpu_seconds=usage.ru_stime,
            original_script_sha256=SHA(script)))
        return status


def main():
    if not __debug__:
        raise RuntimeError('assertions required')
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--depth',choices=('parity','stages'),default='stages')
    args=ap.parse_args()
    source=args.source.resolve();out=args.output.resolve()
    assert source==FROZEN
    assert hasattr(os,'fork') and hasattr(os,'wait4'),'POSIX experiment requires fork/wait4'
    assert os.environ.get('OPENBLAS_NUM_THREADS')==os.environ.get('OMP_NUM_THREADS')=='1'
    assert not out.exists()
    pinned=READ(source/'MANIFEST.json')['files']
    namespace=runpy.run_path(str(source/'verify_source.py'),run_name='prefix_source_verifier')
    namespace['integrity']()
    bank=PrefixBank(out/'pkg',deep=args.depth=='stages')
    scripts={}
    for label,relative in RELATIVES.items():
        path=out/relative if relative.startswith('pkg/') else source/relative
        scripts[str(path)]=label
    original_run=subprocess.run
    def dispatch(command,*pos,**kw):
        cmd=list(map(str,command))
        if len(cmd)>=3 and cmd[2] in scripts:
            assert cmd[:2]==[sys.executable,'-B'] and not pos
            label=scripts[cmd[2]]
            relative=RELATIVES[label]
            assert SHA(cmd[2])==pinned[relative]
            assert kw.get('stderr')==subprocess.STDOUT and set(kw)=={'stdout','stderr','env'}
            assert kw['env']['PYTHONDONTWRITEBYTECODE']=='1'
            status=bank.execute(label,Path(cmd[2]),cmd[3:],kw['stdout'])
            return subprocess.CompletedProcess(cmd,status)
        return original_run(command,*pos,**kw)
    subprocess.run=dispatch
    try:
        namespace['verify'](out)
    finally:
        subprocess.run=original_run
    assert [r['consumer'] for r in bank.consumers]==list(RELATIVES)
    assert all(r['returncode']==0 for r in bank.consumers)
    namespace['integrity']()
    report=dict(status='PASS_FRESH_PREFIX_SHARING_SIX_ISOLATED_CONSUMERS',depth=args.depth,
        source_commit='e76d7a94e6ad819e2aa9dc99083ecfa3e7842e0b',
        fresh_prefixes=bank.fresh,consumers=bank.consumers,
        parent_peak_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        implementation_sha256=SHA(__file__),prefixes_retained=list(bank.prefixes),
        scope='Fresh producer, selection regeneration and all original source checks; POSIX fork prototype.')
    (out/'PREFIX-SHARING.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],flush=True)


if __name__=='__main__':
    main()
