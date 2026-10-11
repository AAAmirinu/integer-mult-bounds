"""Interpreter/LF transport for immutable upstream Python entry points.

Scientific code is unchanged. Windows text writes use canonical LF; subprocess
python3 resolves to the selected interpreter; regeneration uses the explicit
path/newline adapter, which still requires all 25 expected files to match.
"""
from pathlib import Path
import builtins,io,runpy,subprocess,sys
ROOT=Path(__file__).resolve().parent
original_run=subprocess.run
def portable_run(args,*a,**kw):
    if isinstance(args,(list,tuple)):
        args=list(args)
        if str(args[0]) in ('python3','python3.exe'):args[0]=sys.executable
        if sys.platform=='win32' and Path(str(args[0])).stem in ('legality','legality_ncopy_h','columns_h','columns_k2','columns_k3','leg_orig','leg_gen','col_orig','col_gen'):
            from native_transport import arguments
            args=arguments(args,kw.get('cwd'))
        target=next((x for x in args if str(x).endswith('regen_check_e8.py')),None)
        if target is not None:args=[sys.executable,'-B',str(ROOT/'regen_portable.py'),str(target)]
    return original_run(args,*a,**kw)
subprocess.run=portable_run
def canonical_open(original):
    def opened(file,mode='r',*args,**kw):
        if 'b' not in mode and any(x in mode for x in 'wax') and len(args)<4 and 'newline' not in kw:
            kw['newline']='\n'
        return original(file,mode,*args,**kw)
    return opened
if sys.platform=='win32':
    builtins.open=canonical_open(builtins.open);io.open=canonical_open(io.open)
args=sys.argv[1:]
if args[0]=='-c':
    sys.argv=['-c',*args[2:]]
    exec(compile(args[1],'<upstream-inline>','exec'),{'__name__':'__main__'})
else:
    sys.argv=args;sys.path.insert(0,str(Path(args[0]).resolve().parent))
    runpy.run_path(args[0],run_name='__main__')
