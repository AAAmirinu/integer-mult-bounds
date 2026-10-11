"""Private independent full bit replay for arbitrary changed helper count."""
import argparse,gzip,hashlib,importlib.util,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent
P=ROOT.parent/'e8-coupled-bit-retiming'
CODE=P/'vendor/source375/code';BIT=CODE/'bit';CK=BIT/'checkers';HK=P/'vendor/source381/code/bit/checkers'
def read(p):return json.loads(pathlib.Path(p).read_text())
def dump(p,z):pathlib.Path(p).write_text(json.dumps(z,indent=2)+'\n')
def main(word,complex_receipt,out,baseline_bin):
    c=json.loads(gzip.decompress(word.read_bytes()));R=c['R'];out.mkdir(exist_ok=False);(out/'bin').mkdir();stages=[]
    env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    def run(name,args):
        print('RUN',name,flush=True);t=time.monotonic()
        command=[str(x.relative_to(out).as_posix())if i and isinstance(x,pathlib.Path)and x.is_relative_to(out)else str(x)for i,x in enumerate(args)]
        with(out/(name+'.log')).open('w',encoding='utf-8')as f:subprocess.run(command,cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
        stages.append({'name':name,'log_sha256':hashlib.sha256((out/(name+'.log')).read_bytes()).hexdigest()});print('PASS',name,round(time.monotonic()-t,2),flush=True)
    def py(script,*args):return[sys.executable,'-B',P/'run_pinned.py',script,*args]
    rec=out/'records';run('export',py(BIT/'export_records.py',word,rec))
    run('independent-word',py(BIT/'independent/checkword.py',word,CODE/'pricing'))
    run('word-controls',py(BIT/'independent/mutate.py',word,CODE/'pricing'))
    run('cohort',py(BIT/'regression/stage_cohort.py',rec,rec,out/'cin',out/'cout'))
    cxx=os.environ.get('CXX','g++');base=pathlib.Path(baseline_bin);exe=lambda p:p.with_suffix('.exe')if sys.platform=='win32'else p
    for name,source,extra in [('columns_h','columns_h.cpp',[]),('columns_k2','columns_k.cpp',['-DKPAIRS=2']),('columns_k3','columns_k.cpp',['-DKPAIRS=3'])]:
        run(name+'-compile',[cxx,'-O2','-std=c++17','-DHDIM=8','-DNCOPY=9','-DVPORTS=120',f'-DRHELP={R}',*extra,'-I'+str(CK),'-o',exe(out/'bin'/name),CK/source])
    run('legality',[exe(base/'legality'),out/'cin',out/'cout',out/'legality.json'])
    for name in ('columns_h','columns_k2','columns_k3'):run(name,[exe(out/'bin'/name),out/'cout/COHORT249-RECORDS.bin',out/(name+'.json')])
    col=read(out/'columns_k3.json');assert col['formal_columns_checked']==720+R and len(col['stages'])==7
    assert len(col['negative_controls'])==12 and all(z['rejected']for z in col['negative_controls'])
    h,k=read(out/'columns_h.json'),read(out/'columns_k2.json');h.pop('seconds');k.pop('seconds');assert h==k
    run('record-controls',py(BIT/'mutate_records.py',rec,out/'cin',out/'cout',exe(base/'legality'),exe(out/'bin/columns_k3'),exe(base/'legality_ncopy_h')))
    run('gram',py(CK/'gram_frames.py',rec,'--gram','e8ham','--h',8,'--positive'))
    run('geometry',py(HK/'geometry_k.py',3,word,'unsplit'));run('banks',py(CK/'tile_k.py',rec,3,8,7))
    b=read(complex_receipt)['coarse'];run('pricing',py(HK/'certify_bit_k.py',rec,b,3,8,7,out/'priced.json','unsplit'))
    run('finite-input',py(BIT/'receipts_k.py',word,rec,out/'legality.json',out/'columns_k3.json',out/'priced.json',out/'finite-input.json'))
    run('finite',py(HK/'finite_k.py','e8',out/'finite-input.json',out/'finite.json'))
    p,f=read(out/'priced.json'),read(out/'finite.json');assert p['W']==7*(720+R)and p['m']==56
    assert p['maxchild']<=39 and p['halving_degree']==2 and f['row_reserve']['internal_coefficient']==6274
    assert f['route']['all_ports']['ports']==120
    result={'status':'PASS_FRESH_CLEAN_REUSE_BIT_SUPPLIER','R':R,'local_columns':240+R,'global_columns':720+R,'coarse':p['bit_coarse'],'live':p['W'],'word_sha256':hashlib.sha256(word.read_bytes()).hexdigest(),'stages':stages,'scope':'Conditional finite supplier, inherited all-size interfaces retained.'};dump(out/'VERIFICATION.json',result);print(json.dumps(result),flush=True)
