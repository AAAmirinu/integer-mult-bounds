"""Replay changed rank151 + targetmix + two prefix factors; no optimizer/network."""
from pathlib import Path
import os,sys,json,hashlib,shutil,subprocess,time,importlib.util
assert __debug__
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve();assert not OUT.exists() and not OUT.is_relative_to(ROOT)
OUT.mkdir(parents=True);(OUT/'bin').mkdir();steps=[];start=time.monotonic()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONINTMAXSTRDIGITS='0',PYTHONPATH=os.pathsep.join(map(str,[ROOT/'vendor/runtime',ROOT/'vendor/complex',ROOT/'code'])),TMP=str(OUT/'bin'),TEMP=str(OUT/'bin'));env.pop('PYTHONOPTIMIZE',None)
def run(name,args):
 print('RUN',name,flush=True);t=time.monotonic();p=OUT/(name+'.log')
 with p.open('w',encoding='utf-8')as f:r=subprocess.run(list(map(str,args)),env=env,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,(name,p.read_text(encoding='utf-8')[-4000:])
 steps.append(dict(name=name,seconds=round(time.monotonic()-t,3),log_sha256=sha(p)));print('PASS',name,flush=True)
def py(name,path,*args):run(name,[sys.executable,'-B',path,*args])
py('targetmix',ROOT/'vendor/runtime/mix_target.py',ROOT/'inputs/rank151.json.gz',OUT/'mixed.json')
spec=importlib.util.spec_from_file_location('prefix',ROOT/'code/prefix.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
w,rec=mod.construct(read(OUT/'mixed.json'));raw=json.dumps(w,sort_keys=True,separators=(',',':')).encode();(OUT/'word.json').write_bytes(raw);(OUT/'PREFIX.json').write_text(json.dumps(rec,indent=2))
assert hashlib.sha256(raw).hexdigest()=='94f1afe2aae90793e8143ea4d35a2a38c9ad41fcb75cc764d558710e05dde29e'
cxx=os.environ.get('CXX')or shutil.which('g++')or shutil.which('clang++')
if not cxx and Path('C:/mingw64/bin/g++.exe').exists():cxx='C:/mingw64/bin/g++.exe'
assert cxx,'Set CXX to a C++17 compiler'
includes=[ROOT/'vendor/native'];boost=os.environ.get('BOOST_INCLUDE')
if boost:includes.append(Path(boost))
for name,file,defs in [('legality','legality_h.cpp',['NCOPY=9']),('columns','columns_h.cpp',['NCOPY=9','VPORTS=120','RHELP=740']),('columns_k5','columns_k.cpp',['NCOPY=9','VPORTS=120','RHELP=740','KPAIRS=5'])]:
 run('compile-'+name,[cxx,'-O2','-std=c++17','-DHDIM=8',*['-D'+d for d in defs],*['-I'+str(p)for p in includes],'-o',OUT/'bin'/(name+('.exe'if os.name=='nt'else'')),ROOT/'vendor/native'/file])
def exe(n):return OUT/'bin'/(n+('.exe'if os.name=='nt'else''))
py('records',ROOT/'vendor/runtime/export_records.py',OUT/'word.json',OUT/'records')
py('mix-check',ROOT/'vendor/runtime/mix_check.py',OUT/'word.json',OUT/'records')
py('cohort',ROOT/'vendor/runtime/stage_cohort.py',OUT/'records',OUT/'records',OUT/'cin',OUT/'cout')
run('legality',[exe('legality'),OUT/'cin',OUT/'cout',OUT/'cout/legality.json'])
for n in ['columns','columns_k5']:run(n,[exe(n),OUT/'cout/COHORT249-RECORDS.bin',OUT/'cout'/(n+'.json')])
py('gram',ROOT/'vendor/native/gram_frames.py',OUT/'records','--gram','e8ham','--h',8,'--positive')
py('geometry',ROOT/'vendor/runtime/geometry_k.py','--source',ROOT/'inputs/geometry','--out',OUT/'nine','--stages',11,'--no-timing')
py('global',ROOT/'vendor/runtime/global_k.py','--word',OUT/'word.json','--local-check',OUT,'--out',OUT/'nine','--isometries',ROOT/'inputs/residual-isometries.json','--stages',11,'--replicas',8,'--no-banks')
py('hosted',ROOT/'code/emit_whole.py',OUT/'nine',OUT,ROOT/'inputs/bit-selection.json',OUT/'hosted')
py('independent',ROOT/'code/audit_whole.py',OUT,OUT/'hosted',OUT/'hosted/AUDIT.json')
(OUT/'RECEIPT.json').write_text(json.dumps(dict(status='PASS_CHANGED_BIT151_COMPOSITION',seconds=time.monotonic()-start,steps=steps),indent=2))
