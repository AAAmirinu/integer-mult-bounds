"""Full pinned PR375 replay, PR376 reuse, new bit frames and PR377 composition.

Prepared with substantial OpenAI Codex assistance; Apache-2.0. All inherited
conditional proof obligations remain. No network or cached PASS is required.
"""
from pathlib import Path
from fractions import Fraction as Q
import argparse,gzip,hashlib,importlib.util,json,os,subprocess,sys
import baseline
from audit_cost import audit
ROOT=Path(__file__).resolve().parent
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def manifests():
    for item in read(ROOT/'SOURCE-PINS.json')['files']:
        assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
    expected=read(ROOT/'MANIFEST.json')
    for path,digest in expected.items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert actual==set(expected)|{'MANIFEST.json'},'Unlisted package file'

def candidate(out,base):
    out=Path(out).resolve();base=Path(base).resolve();out.mkdir(parents=True,exist_ok=False)
    code=ROOT/'vendor/source375/code';bit=code/'bit';ck=bit/'checkers';cx=code/'complex'
    halving=ROOT/'vendor/source381/code';hk=halving/'bit/checkers'
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
    def run(args,log,extra=None):
        print('RUN',log,flush=True)
        with (out/log).open('w',encoding='utf-8',newline='\n') as stream:
            command=[]
            for position,argument in enumerate(args):
                if position and isinstance(argument,Path) and argument.is_relative_to(out):argument=argument.relative_to(out).as_posix()
                command.append(str(argument))
            if log=='complex.json':
                with (out/'complex-progress.log').open('w',encoding='utf-8',newline='\n') as errors:
                    subprocess.run(command,cwd=out,env=dict(env,**(extra or {})),stdout=stream,stderr=errors,check=True)
            else:subprocess.run(command,cwd=out,env=dict(env,**(extra or {})),stdout=stream,stderr=subprocess.STDOUT,check=True)
    def py(script,*args):return [sys.executable,'-B',ROOT/'run_pinned.py',script,*args]
    word=ROOT/'data/retimed.json.gz';original=ROOT/'data/reused-baseline.json.gz'
    assert (ROOT/'data/baseline.json.gz').read_bytes()==(ROOT/'vendor/source375/data/bit/bitE8-r865.json.gz').read_bytes()
    run(py(ROOT/'generate.py',out/'regenerated.json.gz'),'generation.log')
    assert json.load(gzip.open(out/'regenerated.json.gz','rt'))==json.load(gzip.open(word,'rt'))
    rec=out/'records'
    run(py(bit/'export_records.py',word,rec),'export.log')
    run(py(bit/'export_records.py',original,out/'baseline-records'),'baseline-export.log')
    run(py(bit/'independent/checkword.py',original,code/'pricing'),'baseline-independent.log')
    run(py(bit/'independent/checkword.py',word,code/'pricing'),'independent.log')
    run(py(bit/'independent/mutate.py',word,code/'pricing'),'word-controls.log')
    run(py(bit/'regression/stage_cohort.py',rec,rec,out/'cin',out/'cout'),'cohort.log')
    (out/'bin').mkdir()
    R=json.load(gzip.open(word,'rt'))['R'];v=120
    cxx=os.environ.get('CXX','g++')
    for name,source,extra in [('columns_h','columns_h.cpp',[]),('columns_k2','columns_k.cpp',['-DKPAIRS=2']),('columns_k3','columns_k.cpp',['-DKPAIRS=3'])]:
        exe=out/'bin'/name
        if sys.platform=='win32':exe=exe.with_suffix('.exe')
        run([cxx,'-O2','-std=c++17','-DHDIM=8','-DNCOPY=9','-DVPORTS=120',f'-DRHELP={R}',*extra,'-I'+str(ck),'-o',exe,ck/source],name+'-compile.log')
    def executable(name):
        path=(out if name.startswith('columns_') else base)/'bin'/name
        return path.with_suffix('.exe') if sys.platform=='win32' else path
    run([executable('legality'),out/'cin',out/'cout',out/'legality.json'],'legality.log')
    for name in ('columns_h','columns_k2','columns_k3'):
        run([executable(name),out/'cout/COHORT249-RECORDS.bin',out/(name+'.json')],name+'.log')
    columns=read(out/'columns_k3.json')
    assert columns['formal_columns_checked']==6*v+R==1542 and len(columns['stages'])==7
    assert len(columns['negative_controls'])==12 and all(x['rejected'] for x in columns['negative_controls'])
    a,b=read(out/'columns_h.json'),read(out/'columns_k2.json')
    for d in (a,b):d.pop('seconds')
    assert a==b
    run(py(bit/'mutate_records.py',rec,out/'cin',out/'cout',executable('legality'),executable('columns_k3'),executable('legality_ncopy_h')),'record-controls.log')
    run(py(ck/'gram_frames.py',rec,'--gram','e8ham','--h',8,'--positive'),'gram.log')
    run(py(hk/'geometry_k.py',3,word,'unsplit'),'geometry.log')
    run(py(ck/'tile_k.py',rec,3,8,7),'banks.log')
    cost=load('retiming_cost',ck/'cost.py')
    def hist(folder):
        s,fr,dim,records=cost.load_snapshot(str(folder));h,resid,v=cost.local_profile(records,s,dim,h=8)
        assert (resid,v)==(6576,120);return dict(h)
    dominance=audit(json.load(gzip.open(original,'rt')),json.load(gzip.open(word,'rt')),hist(out/'baseline-records'),hist(rec))
    write(out/'dominance.json',dominance)
    # PR377's original verifier runs all eight stages and both moment engines.
    # The envelope comparison follows PR380's source-bound composition.
    run(py(ROOT/'vendor/source377/verify.py','--work',out/'nine-complex'),'complex-component.log')
    receipt=read(out/'nine-complex/VERIFICATION.json')
    assert receipt['status']=='PASS_PORTABLE_NINE_STAGE_COMPLEX_FINITE_COMPONENT'
    assert len(receipt['fresh_stages'])==8 and all(x['returncode']==0 for x in receipt['fresh_stages'])
    co=out/'nine-complex/work/complex-nine-native'
    complex_b=Q(read(co/'INDEPENDENT-TEMPLATE-AUDIT.json')['coarse_complex'])
    assert complex_b==Q(999240641319551,10**18)
    run(py(ROOT/'complex_replay.py',out/'far-complex',out/'nine-complex'),'far-complex-component.log')
    fresh=read(out/'far-complex/VERIFICATION.json')
    assert fresh['status']=='PASS_FRESH_FAR_RETIMED_NINE_STAGE_COMPONENT'
    assert fresh['all_rational_columns']==1023 and len(fresh['stages'])==5
    co=out/'far-complex/work/complex-nine-native'
    complex_b=Q(read(co/'INDEPENDENT-TEMPLATE-AUDIT.json')['coarse_complex'])
    assert complex_b==Q(999632926176283,10**18)
    global_=read(co/'GLOBAL-REVIEW.json');invoice=global_['finite_invoice']
    assert (global_['m'],global_['live'],global_['physical'],global_['deficit'])==(73,14727,15520,2496)
    assert (invoice['G_exponent'],invoice['E_exponent'],invoice['C0_exponent'])==(30000,100000,210000)
    assert invoice['router_bits']<=30000 and invoice['literal_bits']<=100000 and invoice['required_C0_bits']<=210000
    assert invoice['physical_row_coefficient']==15445<invoice['retained_row_coefficient']==20161
    assert invoice['halving_degree']==2 and invoice['induction_gap_multiple_B']==49
    assert (code/'pricing/outer.py').read_bytes()==(ROOT/'vendor/source377/work/pr361/code/engines/outer.py').read_bytes()
    write(out/'common-envelope.json',invoice)
    run(py(hk/'certify_bit_k.py',rec,complex_b,3,8,7,out/'priced.json','unsplit'),'pricing.log')
    priced=read(out/'priced.json')
    run(py(bit/'receipts_k.py',word,rec,out/'legality.json',out/'columns_k3.json',out/'priced.json',out/'finite-input.json'),'finite-input.log')
    run(py(hk/'finite_k.py','e8',out/'finite-input.json',out/'finite.json'),'finite.log')
    from assembly import run as refine
    finite=read(out/'finite.json')
    assert priced['maxchild']==34 and priced['halving_degree']==2
    assert (priced['m'],priced['T'],priced['W'])==(56,7,10794)
    assert finite['row_reserve']['internal_coefficient']==6274<20161
    assert finite['row_reserve']['halving_degree']==2
    assert finite['route']['all_ports']['ports']==120
    assert 56<=global_['m'] and 10794<=global_['live'] and 1512<=global_['deficit']
    refined=refine(ROOT/'vendor/source381',priced,finite);write(out/'assembly.json',refined)
    # Fair control: compose PR376's unchanged bit component with the same b.
    run(py(hk/'certify_bit_k.py',out/'baseline-records',complex_b,3,8,7,out/'baseline-priced.json','unsplit'),'baseline-pricing.log')
    run(py(bit/'receipts_k.py',original,out/'baseline-records',out/'legality.json',out/'columns_k3.json',out/'baseline-priced.json',out/'baseline-finite-input.json'),'baseline-finite-input.log')
    run(py(hk/'finite_k.py','e8',out/'baseline-finite-input.json',out/'baseline-finite.json'),'baseline-finite.log')
    baseline_priced=read(out/'baseline-priced.json')
    comparison=refine(ROOT/'vendor/source381',baseline_priced,read(out/'baseline-finite.json'));write(out/'baseline-assembly.json',comparison)
    assert Q(refined['kappa'])==Q(comparison['kappa'])>Q(1,1024)
    assert Q(priced['bit_coarse'])>Q(baseline_priced['bit_coarse'])
    assert Q(499,500)<=1-Q(priced['bit_coarse'])<1-Q(baseline_priced['bit_coarse'])<=Q(9999,10000)
    result=dict(status='PASS_SOURCE_BOUND_E8_BIT_RETIMING_AND_ASSEMBLY',kappa=refined['kappa'],complex_coarse=str(complex_b),bit_coarse=priced['bit_coarse'],prior_pr384='998634656132003/1000000000000000000',absolute_gain=refined['absolute_gain'],baseline_composed_kappa=comparison['kappa'],baseline_bit_coarse=baseline_priced['bit_coarse'],bit_component_gain=str(Q(priced['bit_coarse'])-Q(baseline_priced['bit_coarse'])),retiming_kappa_gain='0',changed_gates=dominance['changed_gates'],local_histogram={str(k):v for k,v in hist(rec).items()},local_columns=1062,global_columns=1542,finite_coefficient=finite['coefficient'],complex_unit='PR384 far retiming, full derived physical replay',conditional=True)
    expected=read(ROOT/'data/EXPECTED.json')
    assert result==expected,('Record does not match fresh reconstruction',result)
    write(out/'RESULT.json',result);print(json.dumps(result,indent=2),flush=True);return result

def main():
    if sys.flags.optimize:raise SystemExit('Assertions must remain enabled')
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);ap.add_argument('--shell',default='bash');ap.add_argument('--boost-include',type=Path);a=ap.parse_args()
    out=a.output.resolve();assert out!=ROOT and ROOT not in out.parents and not out.exists(),'Choose fresh output outside package'
    manifests();out.mkdir(parents=True)
    base=baseline.run(out/'baseline',a.shell,a.boost_include)
    if a.boost_include:os.environ['CPLUS_INCLUDE_PATH']=str(a.boost_include.resolve())
    candidate(out/'candidate',base);manifests()
if __name__=='__main__':main()
