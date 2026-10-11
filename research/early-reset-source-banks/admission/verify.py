"""Fresh variable-R admission on the frozen PR433 compressed geometry.
Source claims are conditional; every changed local/global stream is regenerated.
OpenAI Codex assistance, 2026-10-11; retained notices apply.
"""
from pathlib import Path
import argparse,json,gzip,hashlib,shutil,os,subprocess,sys,time
from fractions import Fraction as Q
assert __debug__ and sys.version_info>=(3,11)
sys.dont_write_bytecode=True
p=argparse.ArgumentParser();p.add_argument('--word',type=Path,required=True);p.add_argument('--expected-sha256',required=True);p.add_argument('--base-source',type=Path,required=True);p.add_argument('--complex-proof',type=Path,required=True);p.add_argument('--work',type=Path,required=True);a=p.parse_args()
HERE=Path(__file__).resolve().parent;SRC=a.base_source.resolve();PRIOR=a.complex_proof.resolve();OUT=a.work.resolve();assert not OUT.exists()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();read=lambda p:json.loads(Path(p).read_text());ug=lambda p:json.loads(gzip.decompress(Path(p).read_bytes()))
assert sha(a.word)==a.expected_sha256
sm=read(SRC/'MANIFEST.json');assert {p.relative_to(SRC).as_posix():sha(p)for p in SRC.rglob('*')if p.is_file()and p.name!='MANIFEST.json'}==sm['files']
w=read(a.word);base=read(PRIOR/'bit426-source-centres/bit-source-centres.json');assert (w['format'],w['h'],w['v'])==(base['format'],8,120)
for key in['lines','frames','form']:assert w[key]==base[key],key
assert len(w['start'])==len(w['final'])==240+w['R']
assert w['start'][:240]==base['start'][:240]and w['final'][:240]==base['final'][:240]
full=w['final'][0];assert all(x==full for x in w['final'][240:]);assert all(not w['frames'][x] for x in w['start'][240:])
OUT.mkdir();B=OUT/'bit426-source-centres';B.mkdir();shutil.copyfile(a.word,B/'bit-source-centres.json')
def cp(src,dst,unzip=False):
 dst=OUT/dst;dst.parent.mkdir(parents=True,exist_ok=True);raw=Path(src).read_bytes();dst.write_bytes(gzip.decompress(raw)if unzip else raw)
cp(SRC/'inputs/e8-r865.json.gz','work/pr370-source/research/e8-bit/data/bit/bitE8-r865.json.gz');cp(SRC/'inputs/bit-geometry.json.gz','inherited/bit-geometry.json.gz')
for n in['moment','base_two_moment','outer']:cp(SRC/f'vendor/engines/{n}.py',f'work/pr361/code/engines/{n}.py')
cx=read(PRIOR/'split-centres/INTEGRATION.json');ca=read(PRIOR/'split-centres/INDEPENDENT-REPLAY.json');raw=gzip.decompress((PRIOR/'split-centres/GLOBAL-TEMPLATE.json.gz').read_bytes());ch=hashlib.sha256(raw).hexdigest();assert ch==cx['global_template_sha256']==ca['template_sha256']==read(SRC/'EXPECTED.json')['complex_template_sha256'];assert Q(ca['complex_b'])==Q('1183986549206329/1000000000000000000')
for f in['INTEGRATION.json','INDEPENDENT-REPLAY.json','GLOBAL-TEMPLATE.json.gz','CANONICAL-WORD.json.gz','CLIFFORD-REVIEW.json']:cp(PRIOR/'split-centres'/f,'split-centres/'+f)
assert sha(OUT/'split-centres/CANONICAL-WORD.json.gz')==cx['canonical_word_sha256'];phase=read(OUT/'split-centres/CLIFFORD-REVIEW.json');assert phase['canonical_word_sha256']==cx['canonical_word_sha256'] and phase['all_child_equalities_include_global_phase']
checks=[];env=dict(os.environ,E8_OUTPUT=str(OUT),PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
def run(name,script,*args):
 print('RUN',name,flush=True);t=time.monotonic();log=OUT/(name+'.log')
 with log.open('w')as f:r=subprocess.run([sys.executable,'-B',str(HERE/'code'/script),*map(str,args)],cwd=OUT,env=env,stdout=f,stderr=subprocess.STDOUT)
 assert r.returncode==0,(name,r.returncode,str(log));checks.append(dict(name=name,exit_code=0,seconds=time.monotonic()-t,log_sha256=sha(log)));print('PASS',name,flush=True)
try:
 run('export','export_records.py',B/'bit-source-centres.json',B/'records')
 run('emitted-global','bit_global.py','--source',B,'--local-check',B,'--out',B/'global')
 run('independent-global','bit_audit.py','--local-check',B,'--out',B/'global')
 run('two-exact-moments','bit_price.py')
 run('both-invoices-outer','combined.py')
 result=read(OUT/'RESULT.json');assert len(result['strict_outer_constraints'])==47 and all(Q(z)>0 for z in result['strict_outer_constraints'].values());assert sha(a.word)==a.expected_sha256
 result.update(status='PASS_CHANGED_VARIABLE_R_BIT_FULL_FINITE_ADMISSION',candidate_sha256=a.expected_sha256,R=w['R'],base_source_manifest_sha256=sha(SRC/'MANIFEST.json'),complex_source_template_sha256=ch,fresh_checks=checks,script_hashes={p.name:sha(p)for p in sorted((HERE/'code').glob('*.py'))},all_size_claim=False)
 (OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['kappa_decimal'],result['bit_invoice'],flush=True)
except BaseException as e:
 (OUT/'FAILURE.json').write_text(json.dumps(dict(error=str(e),checks=checks),indent=2)+'\n');raise
