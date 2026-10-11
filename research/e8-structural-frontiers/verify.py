"""Freshly replay scoped obstructions without altering any supplier input."""
import argparse,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifests():
    actual={p.relative_to(ROOT).as_posix():sha(p) for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json'}
    assert actual==read(ROOT/'MANIFEST.json'),'Structural appendix manifest mismatch'
    for z in read(ROOT/'SOURCE-PINS.json')['files']:
        p=ROOT/z['path'] if z['path'].startswith('vendor/') else ROOT.parent/z['path']
        assert sha(p)==z['sha256'],z['path']
def main(out):
    manifests();out=out.resolve()
    assert not out.exists() and ROOT not in out.parents
    assert ROOT.parent/'e8-clean-reuse-extension' not in out.parents
    assert ROOT.parent/'e8-coupled-bit-retiming' not in out.parents
    out.mkdir(parents=True)
    env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    checked=[]
    for script,result in [('center_rank_obstructions.py','CENTER-RANK-OBSTRUCTIONS.json'),('static_firstframe_bound.py','STATIC-FIRSTFRAME-BOUND.json'),('vendor/universal_rank8_span.py','UNIVERSAL-RANK8-SPAN.json')]:
        command=[sys.executable,'-B',str(ROOT/script),'--output',str(out/result)]
        if script.startswith('vendor/'):
            command+=['--source',str(ROOT.parent/'e8-clean-reuse-extension/data/kernel-base.json.gz'),'--budget-source',str(ROOT.parent/'e8-clean-reuse-extension/data/complex-candidate.json.gz'),'--moment-engine',str(ROOT.parent/'e8-coupled-bit-retiming/vendor/source381/code/pricing/moment.py'),'--immutable-root',str(ROOT.parents[1])]
        with (out/(pathlib.Path(script).name+'.log')).open('w',encoding='utf-8') as log:
            subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        fresh=read(out/result);fresh.pop('source',None);fresh.pop('pricer',None)
        assert fresh==read(ROOT/'data'/result),('Fresh mathematical record differs',result)
        checked.append(dict(producer=script,result=result,status=fresh['status']))
    manifests()
    z=dict(status='PASS_FRESH_SCOPED_E8_STRUCTURAL_OBSTRUCTIONS',checks=checked,manifest_sha256=sha(ROOT/'MANIFEST.json'),supplier_inputs_unchanged=True,new_supplier=False,new_kappa=False,scope='Finite source-support theorem and a necessary moment bound for an explicitly fixed family; no global optimality or multiplication lower bound.')
    (out/'RESULT.json').write_text(json.dumps(z,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    print(z['status'])
if __name__=='__main__':
    if sys.flags.optimize:raise SystemExit('Assertions must remain enabled')
    ap=argparse.ArgumentParser();ap.add_argument('output',type=pathlib.Path);a=ap.parse_args();main(a.output)
