"""Private full replay of the integrated prefix + exact two-donor candidate.

Derivation follows applecrusher PR376 and ai-nanachi PR389. The Y->Y
compiler extension follows Dugongue PR390, with an independently rerun full
raw-operator equality and frozen literal response/cleanup from the new
same-dimension base. Original source bytes stay immutable. No result claimed
until every stage, owner, phase and finite invoice passes.
"""
import argparse, copy, difflib, gzip, hashlib, importlib.util, json, os, pathlib, shutil, subprocess, sys, time
from collections import Counter
from fractions import Fraction as Q
sys.set_int_max_str_digits(0)
HERE=pathlib.Path(__file__).resolve().parent
PACKAGE=HERE.parent/'e8-coupled-bit-retiming'
SOURCE=PACKAGE/'vendor/source377'
CX='work/native358/vendor/complex-reserve/upstream/pr352/code/complex'
ODD='work/odd-stages'

def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def read(p):
    p=pathlib.Path(p);raw=p.read_bytes();return json.loads(gzip.decompress(raw)if p.suffix=='.gz'else raw)
def dump(p,z):pathlib.Path(p).write_text(json.dumps(z,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def rawmap(c):
    n=2*c['v']+c['R'];rows=[{i:Q(1)}for i in range(n)]
    def add(t,s,q):
        for k,v in list(s.items()):
            z=rows[t].get(k,Q(0))+q*v
            if z:rows[t][k]=z
            else:rows[t].pop(k,None)
    def run(gs):
        for g in gs:
            for r,a,b in g[3]:
                t,s=(r,g[2])if g[0]=='out'else(g[2],r);add(t,rows[s],Q(a,b))
    run(c['A']);tot={k:dict(rows[r])for k,r,f in c['ret']}
    for t,es in enumerate(c['scat']['table']):
        for k,a,b in es:add(c['v']+t,tot[k],Q(a,b))
    run(c['B']);return rows,tot
def helperword(c):
    out=[]
    for g in c['A']+c['B']:
        for r,a,b in g[3]:
            t,s=(r,g[2])if g[0]=='out'else(g[2],r)
            if not c['v']<=t<2*c['v']:out.append((t,s,Q(a,b)))
    return out

def main(candidate,base,out):
    c=read(candidate);old=read(base);R=c['R'];N=240+R;LIVE=7680+9*R;PHYSICAL=LIVE+R+10
    assert rawmap(c)==rawmap(old),'ALL independent raw columns and copied totals'
    assert helperword(c)==helperword(old),'EXACT source/helper subword'
    for k in ['h','v','R','cst','N','ports','start','final','ext','ret','scat']:assert c[k]==old[k],k
    assert c['h']==9 and c['v']==120 and R==779
    original_manifest=read(SOURCE/'MANIFEST.json')['files']
    assert {p.relative_to(SOURCE).as_posix():sha(p)for p in SOURCE.rglob('*')if p.is_file()and p!=SOURCE/'MANIFEST.json'}==original_manifest
    assert not out.exists();out.mkdir();shutil.copytree(SOURCE/'work',out/'work');(out/'logs').mkdir();changes=[];stages=[]
    def execute(name,script,args=(),env=None):
        print('RUN',name,flush=True);start=time.monotonic()
        with(out/'logs'/(name+'.log')).open('w',encoding='utf-8',newline='\n')as f:
            subprocess.run([sys.executable,'-B',str(PACKAGE/'run_pinned.py'),str(script),*map(str,args)],cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
        stages.append({'name':name,'log_sha256':sha(out/'logs'/(name+'.log'))});print('PASS',name,round(time.monotonic()-start,2),flush=True)
    def change(path,data,why):
        p=out/path;before=p.read_bytes()if p.exists()else None;raw=data.encode()if isinstance(data,str)else data;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        changes.append({'path':path,'before_sha256':hashlib.sha256(before).hexdigest()if before is not None else None,'after_sha256':sha(p),'reason':why,'unified_diff':''.join(difflib.unified_diff(before.decode().splitlines(True),raw.decode().splitlines(True),fromfile='original/'+path,tofile='derived/'+path))if before is not None and not path.endswith('.gz')else None})
    def edits(path,pairs,why):
        text=(out/path).read_text(encoding='utf-8')
        for before,after,count in pairs:assert text.count(before)==count,(path,before,text.count(before));text=text.replace(before,after)
        change(path,text,why)
    sys.path.insert(0,str(HERE/'vendor/source376'))
    from transport import deterministic_gzip
    data=json.dumps(c,sort_keys=True,separators=(',',':')).encode();z=deterministic_gzip(data)
    pins=read(out/CX/'inputs/complex/source-pins.json');certpath=CX+'/'+pins['certificate']['path'];previous=copy.deepcopy(pins['certificate'])
    change(certpath,z,'Integrated fixed prefix + aliases + two donor inlines, independently admitted gcert')
    change('work/pr361/complex/gcert1-e8-r783.json.gz',z,'One exact candidate consumed by every geometry and phase audit')
    change(CX+'/code/kernel-base.json.gz',deterministic_gzip(json.dumps(old,sort_keys=True,separators=(',',':')).encode()),'Explicit same-width frozen response and cleanup word; full raw matrix equality checked')
    pins['certificate'].update(compressed_sha256=hashlib.sha256(z).hexdigest(),uncompressed_sha256=hashlib.sha256(data).hexdigest(),source_pin='derived-prefix-alias-inline',derived_from=previous)
    pins['certificate'].pop('url',None);change(CX+'/inputs/complex/source-pins.json',json.dumps(pins,indent=2,sort_keys=True)+'\n','Bind actual new input, preserving immutable original attribution')
    edits(CX+'/code/complex_scalars.py',[
        ('t!=s and kind(s)!="Y" and not(kind(s)=="S" and kind(t)=="X")','t!=s and (kind(s)!="Y" or kind(t)=="Y") and not(kind(s)=="S" and kind(t)=="X")',1),
        ('    K=list(old_positive(A,B,c))','    baseline=json.loads(gzip.decompress((Path(__file__).parent/"kernel-base.json.gz").read_bytes()))\n    oldA=flat(baseline["A"]);oldB=flat(baseline["B"])\n    need([(t,s,q) for t,s,q in A+B if kind(t)!="Y"]==[(t,s,q) for t,s,q in oldA+oldB if kind(t)!="Y"],"frozen source/helper cleanup mismatch")\n    K=list(old_positive(oldA,oldB,baseline))',1),
        ('("cleanup",cleanup(orientation,A+B))','("cleanup",cleanup(orientation,oldA+oldB))',1),
        ('projection requires Y never read and no helper-to-X gate','main Y reads require a Y target; helper-to-X remains forbidden',1)
    ],'Sufficient main-only Y->Y extension with explicit independently matching old response and cleanup; no guard removed')
    edits(CX+'/code/complex_splice.py',[
        ("t!=s and role(s)!='Y' and (role(s),role(t))!=('S','X')","t!=s and (role(s)!='Y' or role(t)=='Y') and (role(s),role(t))!=('S','X')",1),
        ("A=list(flat(c['A']));B=list(flat(c['B']));cur=c['start'].copy()","baseline=json.loads(gzip.decompress((Path(__file__).parent/'kernel-base.json.gz').read_bytes()))\n    A=list(flat(baseline['A']));B=list(flat(baseline['B']));cur=c['start'].copy()",1)
    ],'Literal response/cleanup use the exact new baseline; main walks the new candidate and retains every incidence and lifecycle check')
    seed={'H':9,'V':120,'R':R,'cst':72,'N':c['N'],'frames':len(c['frames'])};dump(out/'seed.json',seed)
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CX_PINS=str(out/'seed.json'),CX_RECORD=str(out/'recorded.json'))
    env.pop('CX_SOURCE_PINS',None);env.pop('PYTHONOPTIMIZE',None)
    execute('fresh-local-census',out/CX/'portable_complex.py',env=env)
    fresh=seed|read(out/'recorded.json');change(CX+'/pins-e8.json',json.dumps(fresh,indent=2,sort_keys=True)+'\n','Exact new census and bill recorded once, then frozen for independent admission')
    edits('work/native358/vendor/complex-reserve/finite_guard.py',[("assert (h,v,R)==(9,120,783)",f"assert (h,v,R)==(9,120,{R})",1)],'Rebind dimension to the independently reconstructed helper count')
    edits(ODD+'/complex_candidate.py',[('(9,120,783,72)',f'(9,120,{R},72)',1),('banks=783','banks=R',1)],'Rebuild every finite data route and whole residual bank for new count')
    edits(ODD+'/global_nine.py',[
        ('h,v,R=9,120,783;k,L,T,m=4,9,8,73;live=14727;physical=live+R+h+1',f"h,v,R=c['h'],c['v'],c['R'];assert (h,v,R)==(9,120,{R});k,L,T,m=4,9,8,73;live=2*k*v*T+L*R;physical=live+R+h+1;assert (live,physical)==({LIVE},{PHYSICAL})",1),
        ("local_children=raw['label_checks']['invocation_calls'];assert local_children==3974","local_children=raw['label_checks']['invocation_calls'];assert local_children==sum(sum(block.values()) for block in c['blocks'].values())",1)
    ],'New owners, live stock and exact paid events are derived from the new certificate')
    path=ODD+'/audit_nine_template.py';text=(out/path).read_text();needle="c=json.load(gzip.open('work/pr361/complex/gcert1-e8-r783.json.gz'))";assert text.count(needle)==1
    text=text.replace(needle,needle+f"\nassert (c['h'],c['v'],c['R'],c['cst'])==(9,120,{R},72)\nR=c['R'];N=2*c['v']+R;LIVE=8*c['v']*8+9*R;PHYSICAL=LIVE+R+c['h']+1\nassert (N,LIVE,PHYSICAL)==({N},{LIVE},{PHYSICAL})")
    for before,after,count in [('14727','LIVE',11),('15520','PHYSICAL',1),('1023','N',2),('r*783','r*R',1),('s*783','s*R',1)]:
        assert text.count(before)==count,(before,text.count(before));text=text.replace(before,after)
    # The independent audit's old fixed expected price is rebound after the
    # separate fresh geometric producer certifies the actual new profile.
    old_price='assert b==Q(999240641319551,10**18)';assert text.count(old_price)==1
    text=text.replace(old_price,"assert b==Q(json.loads(Path('EXPECTED-PRICE.json').read_text())['coarse'])")
    change(path,text,'Independent read-back derives dimensions and source cardinalities; exact moment equality will bind the separately computed new price')
    dump(out/'DERIVATION.json',{'source_manifest_sha256':sha(SOURCE/'MANIFEST.json'),'candidate_sha256':hashlib.sha256(data).hexdigest(),'baseline_json_sha256':sha(base),'full_raw_columns':N,'changed_files':changes})
    vendor=out/'work/native358/vendor/complex-reserve';native=out/'work/complex-nine-native'
    execute('independent-local-admission',vendor/'admit.py',['--source',vendor/'upstream/pr352','--output',native/'local-admission'])
    execute('finite-data-geometry-banks',out/ODD/'complex_candidate.py')
    priced=read(out/ODD/'COMPLEX-NINE-CANDIDATE.json');dump(out/'EXPECTED-PRICE.json',{'coarse':priced['coarse_candidate']})
    for name,script in [('all-canonical-clifford-phases','verify_clifford_frames.py'),('data-and-cover-phases','data_phases.py'),('global-template-finite-invoice','global_nine.py'),('independent-template-two-moments','audit_nine_template.py')]:execute(name,out/ODD/script)
    g=read(native/'GLOBAL-REVIEW.json');a=read(native/'INDEPENDENT-TEMPLATE-AUDIT.json');d=read(native/'local-admission/INDEPENDENT-AUDIT.json');f=read(native/'CLIFFORD-REVIEW.json')
    assert all(z['independent_live_columns']==N and z['all_live_rows_correct'] and z['all_private_work_restored_zero']for z in d['scalar_words'].values())
    assert (g['m'],g['live'],g['physical'],g['deficit'])==(73,LIVE,PHYSICAL,2496)
    assert g['profile']==a['paid_profile'] and a['coarse_complex']==priced['coarse_candidate']
    assert f['frames']==len(c['frames'])and f['all_child_equalities_include_global_phase']
    assert {p.relative_to(SOURCE).as_posix():sha(p)for p in SOURCE.rglob('*')if p.is_file()and p!=SOURCE/'MANIFEST.json'}==original_manifest
    result={'status':'PASS_FRESH_PREFIX_ALIAS_TWO_DONOR_COMPLEX_COMPONENT','coarse':a['coarse_complex'],'local_columns':N,'R':R,'frames':len(c['frames']),'live':LIVE,'physical':PHYSICAL,'profile':g['profile'],'finite_invoice':g['finite_invoice'],'stages':stages,'scope':'Conditional finite supplier; inherited all-size and main-only target-shear interface retained. No full multiplication claim.'}
    dump(out/'VERIFICATION.json',result);print(result['status'],result['coarse'],flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('candidate',type=pathlib.Path);ap.add_argument('base',type=pathlib.Path);ap.add_argument('output',type=pathlib.Path);a=ap.parse_args()
    main(a.candidate.resolve(),a.base.resolve(),a.output.resolve())
