"""Fresh full predecessor and changed finite supplier admission; no cached PASS."""
import argparse,gzip,hashlib,importlib.util,json,os,pathlib,subprocess,sys
from fractions import Fraction as Q
ROOT=pathlib.Path(__file__).resolve().parent
PARENT=ROOT.parent/'e8-coupled-bit-retiming'
spec=importlib.util.spec_from_file_location('clean_reuse_outer_assembly',ROOT/'assembly.py')
assembly=importlib.util.module_from_spec(spec);spec.loader.exec_module(assembly)
import construct,complex_native,bit_native
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))
def dump(p,z):pathlib.Path(p).write_text(json.dumps(z,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def manifests():
    expected=read(ROOT/'MANIFEST.json')
    actual={p.relative_to(ROOT).as_posix():sha(p)for p in ROOT.rglob('*')if p.is_file()and p!=ROOT/'MANIFEST.json'}
    assert actual==expected,'Extension manifest mismatch'
    pins=read(ROOT/'SOURCE-PINS.json')
    assert sha(PARENT/'MANIFEST.json')==pins['parent']['manifest_sha256']
    old=read(PARENT/'MANIFEST.json');oldactual={p.relative_to(PARENT).as_posix():sha(p)for p in PARENT.rglob('*')if p.is_file()and p!=PARENT/'MANIFEST.json'}
    assert old==oldactual,'Frozen predecessor changed'
    for item in pins['files']:assert sha(ROOT/item['path'])==item['sha256'],item['path']
def main(out,shell,boost):
    manifests();assert not out.exists()and ROOT not in out.parents and PARENT not in out.parents
    out.mkdir(parents=True);env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    if boost:os.environ['CPLUS_INCLUDE_PATH']=str(boost);env['CPLUS_INCLUDE_PATH']=str(boost)
    command=[sys.executable,'-B',str(PARENT/'verify.py'),str(out/'predecessor'),'--shell',shell]
    if boost:command+=['--boost-include',str(boost)]
    print('RUN full frozen predecessor suppliers and controls',flush=True)
    with(out/'predecessor.log').open('w',encoding='utf-8')as f:subprocess.run(command,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    prior=read(out/'predecessor/candidate/RESULT.json');expected=read(ROOT/'data/EXPECTED.json');assert prior['kappa']==expected['prior_pr389']
    regeneration=construct.emit(out/'reconstructed');assert len(regeneration['negative_controls'])==4
    c=out/'reconstructed/complex-candidate.json.gz';base=out/'reconstructed/kernel-base.json.gz';bit=out/'reconstructed/bit-candidate.json.gz'
    complex_native.main(c,base,out/'complex')
    cx=read(out/'complex/VERIFICATION.json')
    bit_native.main(bit,out/'complex/VERIFICATION.json',out/'bit',out/'predecessor/baseline/bin')
    b=read(out/'bit/VERIFICATION.json');p=read(out/'bit/priced.json');f=read(out/'bit/finite.json')
    result=assembly.run(PARENT/'vendor/source381',p,f);dump(out/'ASSEMBLY.json',result)
    assert len(result['assembly']['strict_constraints'])==47
    # Fair control: same new complex supplier, unchanged old bit component.
    oldp=read(out/'predecessor/candidate/priced.json');oldp['complex_coarse']=cx['coarse']
    control=assembly.run(PARENT/'vendor/source381',oldp,read(out/'predecessor/candidate/finite.json'));dump(out/'FAIR-OLD-BIT-ASSEMBLY.json',control)
    assert result['kappa']==control['kappa']and Q(b['coarse'])>Q(oldp['bit_coarse'])
    assert p['m']<=73 and p['W']<=cx['live']and f['row_reserve']['internal_coefficient']<20161
    fresh=dict(status='PASS_FRESH_E8_CLEAN_REUSE_AND_SIGNED_COMPOSITION',kappa=result['kappa'],prior_pr389=prior['kappa'],absolute_gain=str(Q(result['kappa'])-Q(prior['kappa'])),complex_coarse=cx['coarse'],bit_coarse=b['coarse'],complex_R=cx['R'],bit_R=b['R'],complex_local_columns=cx['local_columns'],bit_local_columns=b['local_columns'],bit_global_columns=b['global_columns'],complex_live=cx['live'],complex_physical=cx['physical'],complex_profile=cx['profile'],complex_finite_invoice=cx['finite_invoice'],bit_live=b['live'],bit_profile=p['normalized_histogram'],bit_finite_coefficient=f['coefficient'],bit_component_gain=str(Q(b['coarse'])-Q(prior['bit_coarse'])),bit_reuse_kappa_gain='0',conditional=True)
    assert fresh==expected,('Updated record differs from fresh admission',fresh)
    dump(out/'RESULT.json',fresh);manifests();print(fresh['status'],fresh['kappa'],flush=True)
if __name__=='__main__':
    if sys.flags.optimize:raise SystemExit('Assertions must remain enabled')
    ap=argparse.ArgumentParser();ap.add_argument('output',type=pathlib.Path);ap.add_argument('--shell',default='bash');ap.add_argument('--boost-include',type=pathlib.Path);a=ap.parse_args();main(a.output.resolve(),a.shell,a.boost_include.resolve()if a.boost_include else None)
