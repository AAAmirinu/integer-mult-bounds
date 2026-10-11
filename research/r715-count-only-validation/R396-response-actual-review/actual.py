"""Independent actual response28 admission; no producer imports or new native replay."""
import pathlib,json,hashlib,gzip,sys
from fractions import Fraction as Q
R=pathlib.Path(__file__).parent;P=pathlib.Path('F:/integer-mult-frontier/work/R385-response28-full/data/full-002');S=pathlib.Path('F:/integer-mult-frontier/work/R383-response-transfer/source/research/r715-response-replica28');PK=pathlib.Path('F:/integer-mult-frontier/work/R390-response-package-review/snapshot-001');read=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def req(x,m):
 if not x:raise ValueError(m)
def exact(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(exact(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(exact(x,y)for x,y in zip(a,b))
 return a==b
def norm(v,known):
 if isinstance(v,dict):return {k:norm(x,known)for k,x in v.items()}
 if isinstance(v,list):return [norm(x,known)for x in v]
 return known.get(v,v)if isinstance(v,str)else v
def safe(b,n):
 p=(b/n).resolve();req(p.is_relative_to(b.resolve()),'path escape');return p
def main():
 receipt=read(P/'RECEIPT.json');launcher=read(P.parent/'launcher-result-002.json');req(receipt['status']=='PASS_RESPONSE_REPLICA28_FULL_COMPOSITION','full parent enum');req(launcher['status']=='TERMINAL_REPLAY_PASS'and launcher['exit_code']==0 and launcher['timed_out']is False,'actual terminal controller');req(launcher['head']=='f43a0e9ad04a7b3683498274854ae2e35d4a8d7c','head');req(receipt['manifest_sha256']==sha(S/'MANIFEST.json'),'manifest')
 actual={f.relative_to(S).as_posix():sha(f)for f in S.rglob('*')if f.is_file()and f!=S/'MANIFEST.json'and'__pycache__'not in f.parts};req(exact(actual,read(S/'MANIFEST.json')),'source remains unchanged')
 req(read(P/'bit/RECEIPT.json')['status']=='PASS_CHANGED_RESPONSE_FLAG_COMPOSITION','changed bit full enum');bindings={};count=0
 for path in sorted(set(P.rglob('RECEIPT.json'))|set(P.rglob('BUILD-RECEIPT.json'))):
  data=read(path);bindings[path.relative_to(P).as_posix()]=sha(path)
  for step in data.get('steps',[]):
   if 'log_sha256'in step:
    log=safe(path.parent,step['name']+'.log');req(sha(log)==step['log_sha256'],'log');bindings[log.relative_to(P).as_posix()]=sha(log);count+=1
  for name,h in data.get('files',{}).items():
   f=safe(path.parent,name);req(sha(f)==h,'build payload');bindings[f.relative_to(P).as_posix()]=h;count+=1
  for name,h in data.get('sources',{}).items():req(any(pathlib.Path(n).name==name and v==h for n,v in actual.items()),'build source outside closure')
 for path in [P/'bit/word.json',P/'bit/nested/word.json']:req(path.read_bytes()==(S/'bit470/data/word.json').read_bytes(),'actual constructed word')
 ordered=['provider/FULL-WORD.json.gz','provider/CANONICAL-WORD.json.gz','provider/LOCAL-PROGRAMS.json.gz','provider/NORMALIZED-PROGRAMS.json.gz','provider/SCALAR-FRAME-AUDIT.json','provider/CANONICAL-WRAPPERS.json','provider/LOCAL-CHECKS.json','provider/NORMALIZED-CHECKS.json','provider/CLIFFORD-RECIPES.json','provider/CLIFFORD-REVIEW.json','complex/DATA-PHASES.json','complex/GLOBAL-TEMPLATE.json.gz'];known={};content={};raw={}
 for name in ordered:
  f=P/name;raw[name]=sha(f);u=gzip.decompress(f.read_bytes())if name.endswith('.gz')else f.read_bytes();v=json.loads(u);content[name]=hashlib.sha256(json.dumps(norm(v,known),sort_keys=True,separators=(',',':')).encode()).hexdigest()
  if name==ordered[-1]:th=hashlib.sha256(u).hexdigest();template=v
  else:known[raw[name]]=content[name]
 req(exact(content,read(PK/'pins/COMPLEX-CONTENT.json')),'full canonical artifacts');known={raw[n]:content[n]for n in ordered};known[th]=content[ordered[-1]];names=['complex/GLOBAL.json','complex/AUDIT.json','complex/PHYSICAL-AUDIT.json','complex/INDEPENDENT-ROUTES.json'];records={n:norm(read(P/n),known)for n in names};req(exact(records,read(PK/'pins/COMPLEX-RECORDS.json')),'all full typed canonical records')
 for key,name in [('kernel_word','provider/CANONICAL-WORD.json.gz'),('kernel_canonical_word','provider/CANONICAL-WORD.json.gz'),('kernel_normalized_programs','provider/NORMALIZED-PROGRAMS.json.gz'),('kernel_normalized_checks','provider/NORMALIZED-CHECKS.json'),('kernel_local_audit','provider/SCALAR-FRAME-AUDIT.json'),('kernel_wrapper','provider/CANONICAL-WRAPPERS.json'),('data_phase','complex/DATA-PHASES.json')]:req(template['source_bindings'][key]==raw[name],'actual raw source payload binding')
 x=read(P/'RESULT.json');expected=read(S/'EXPECTED.json');req(x.keys()==expected.keys(),'full RESULT schema');req(all(exact(v,expected[k])for k,v in x.items()if k!='complex_template_sha256'),'full RESULT mathematical types and values');req(x['complex_template_sha256']==th,'RESULT actual template')
 bg=read(P/'bit/hosted/GLOBAL.json');ba=read(P/'bit/hosted/AUDIT.json');cg=read(P/'complex/GLOBAL.json');ca=read(P/'complex/AUDIT.json');bt=gzip.decompress((P/'bit/hosted/GLOBAL-TEMPLATE.json.gz').read_bytes());req(hashlib.sha256(bt).hexdigest()==bg['template_sha256']==ba['template_sha256']==x['bit_template_sha256'],'bit template');req(bg['emitted_program_sha256']==ba['emitted_program_sha256']==x['emitted_program_sha256'],'physical bit program');req(cg['template_sha256']==ca['template_sha256']==th and cg['emitted_program_sha256']==ca['emitted_program_sha256'],'complex actual program')
 recon=read(pathlib.Path('F:/integer-mult-frontier/work/R387-response28-audit/RECONSTRUCTION-001.json'));req(exact(ba['profile'],recon['profile'])and ba['hosted_residuals']==recon['occurrences'],'independent inventory');req(ba['local_audit']['entrance_rank']==129 and ba['local_audit']['residual_isometries']==16,'actual changed flags');req(ba['physical_prefix_bits']==x['bit']['prefix_bits']==2060 and ba['charged_prefix_bits']==x['bit']['charged_prefix_bits']==2112,'actual prefix');req(x['bit']['charged_two_level_coefficient_bits']==6272 and x['bit']['row_coefficient']==19434,'actual invoice');req(ba['bank_assignments']==0 and ba['physical']==33609 and ba['emitted_events']==6020168,'actual physical family/program');req(len(x['strict_outer_constraints'])==47 and all(Q(v)>0 for v in x['strict_outer_constraints'].values()),'47 actual margins')
 for name in ['RESULT.json','bit/hosted/GLOBAL.json','bit/hosted/AUDIT.json','bit/hosted/GLOBAL-TEMPLATE.json.gz','bit/hosted/GEOMETRY.json']+names:bindings[name]=sha(P/name)
 result=dict(status='PASS_INDEPENDENT_ACTUAL_FRESH_RESPONSE28_PARENT_ADMISSION',parent_receipt_sha256=sha(P/'RECEIPT.json'),launcher_sha256=sha(P.parent/'launcher-result-002.json'),manifest_sha256=sha(S/'MANIFEST.json'),actual_seconds=launcher['actual_seconds'],actual_result_sha256=sha(P/'RESULT.json'),bindings=bindings,nested_bindings=count,complex_raw=raw,complex_content=content,actual_bit_template_sha256=x['bit_template_sha256'],actual_complex_template_sha256=th,bit_program_sha256=x['emitted_program_sha256'],kappa=x['kappa'],checker_sha256=sha(pathlib.Path(__file__)),scope='Completed fresh source-specific original suppliers and actual outputs/hash/type/whole-family invoice admission. Retained O-cover law/all-size contracts remain conditional; corrected count-only sharp run separate.')
 (R/sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n');print(result['status'],count,x['kappa'])
if __name__=='__main__':main()
