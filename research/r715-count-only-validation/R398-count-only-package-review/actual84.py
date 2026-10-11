"""Independent completed-output consistency review, no producer imports."""
import pathlib,json,hashlib,gzip,sys
from fractions import Fraction as Q
R=pathlib.Path(__file__).parent;PACKAGE=R/'snapshot-84-001'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def read(p):return json.loads(pathlib.Path(p).read_bytes())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def exact(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(exact(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(exact(x,y)for x,y in zip(a,b))
 return a==b
def safe(base,rel):
 p=(base/rel).resolve();need(p.is_relative_to(base.resolve()),'path escape');return p
def norm(v,known):
 if isinstance(v,dict):return {k:norm(x,known)for k,x in v.items()}
 if isinstance(v,list):return [norm(x,known)for x in v]
 return known.get(v,v)if isinstance(v,str)else v
def main():
 parent=pathlib.Path(sys.argv[1]);sharp=None if sys.argv[2]=='--parent-only'else pathlib.Path(sys.argv[2]);pin=read(PACKAGE/'SOURCE.json');baseline=read(parent/'RESULT.json');receipt=read(parent/'RECEIPT.json');expected=read(PACKAGE/'pins/parent-EXPECTED.json')
 need(receipt['status']=='PASS_FULL_REPLICA84_COMPLEX79_COMPOSITION','parent is not terminal full fresh')
 need(receipt['manifest_sha256']==pin['parent_manifest_sha256']and receipt['source_sha256']==pin['parent_source_sha256'],'parent source binding')
 provider=parent/'provider';pr=read(provider/'RECEIPT.json');need(pr['status']=='PASS_R715_NEXT_FULL_COMPOSITION','provider not full')
 need(pr['manifest_sha256']==pin['provider_manifest_sha256']and receipt['provider_receipt_sha256']==sha(provider/'RECEIPT.json'),'provider source binding')
 closure=read(PACKAGE/'pins/CLOSURE.json');sourcecopy=parent/'provider-source'
 inv={p.relative_to(sourcecopy).as_posix():sha(p)for p in sourcecopy.rglob('*')if p.is_file()and'__pycache__'not in p.parts};inv.pop('MANIFEST.json',None)
 need(exact(inv,read(PACKAGE/'pins/parent-ADAPTED-PROVIDER-MANIFEST.json'))and sha(sourcecopy/'MANIFEST.json')==pin['provider_manifest_sha256'],'actual source-copy inventory')
 bindings={};logs=0
 for p in sorted(set(parent.rglob('RECEIPT.json'))|set(parent.rglob('BUILD-RECEIPT.json'))):
  if 'provider-source'in p.relative_to(parent).parts:continue
  data=read(p);bindings[p.relative_to(parent).as_posix()]=sha(p)
  for step in data.get('steps',[]):
   if 'log_sha256'in step:
    log=safe(p.parent,step['name']+'.log');need(sha(log)==step['log_sha256'],'actual step log');bindings[log.relative_to(parent).as_posix()]=sha(log);logs+=1
  for n,h in data.get('files',{}).items():
   f=safe(p.parent,n);need(sha(f)==h,'actual build payload');bindings[f.relative_to(parent).as_posix()]=sha(f)
  for name,h in data.get('sources',{}).items():need(any(pathlib.Path(n).name==name and x==h for n,x in closure['files'].items()),'actual build source outside closure')
 # Independently reproduce the raw/content gzip contract with every JSON field.
 ordered=['provider/FULL-WORD.json.gz','provider/CANONICAL-WORD.json.gz','provider/LOCAL-PROGRAMS.json.gz','provider/NORMALIZED-PROGRAMS.json.gz','provider/SCALAR-FRAME-AUDIT.json','provider/CANONICAL-WRAPPERS.json','provider/LOCAL-CHECKS.json','provider/NORMALIZED-CHECKS.json','provider/CLIFFORD-RECIPES.json','provider/CLIFFORD-REVIEW.json','complex/DATA-PHASES.json','complex/GLOBAL-TEMPLATE.json.gz']
 known={};content={};raw={};template=None
 for name in ordered:
  b=(provider/name).read_bytes();raw[name]=hashlib.sha256(b).hexdigest();unpacked=gzip.decompress(b)if name.endswith('.gz')else b;obj=json.loads(unpacked)
  content[name]=hashlib.sha256(json.dumps(norm(obj,known),sort_keys=True,separators=(',',':')).encode()).hexdigest()
  if name==ordered[-1]:template=obj;th=hashlib.sha256(unpacked).hexdigest()
  else:known[raw[name]]=content[name]
 need(exact(content,read(PACKAGE/'pins/parent-COMPLEX-CONTENT.json')),'actual canonical complex content')
 cr=read(parent/'COMPLEX-CONTENT-RECEIPT.json');need(cr['status']=='PASS_FRESH_BYTE_BINDINGS_AND_PINNED_CONTENT','content checker status')
 need(exact(cr['content_sha256'],content)and exact(cr['actual_file_sha256'],raw)and cr['actual_template_sha256']==th,'content receipt raw/payload binding')
 for key,name in [('kernel_word','provider/CANONICAL-WORD.json.gz'),('kernel_canonical_word','provider/CANONICAL-WORD.json.gz'),('kernel_normalized_programs','provider/NORMALIZED-PROGRAMS.json.gz'),('kernel_normalized_checks','provider/NORMALIZED-CHECKS.json'),('kernel_local_audit','provider/SCALAR-FRAME-AUDIT.json'),('kernel_wrapper','provider/CANONICAL-WRAPPERS.json'),('data_phase','complex/DATA-PHASES.json')]:need(template['source_bindings'][key]==raw[name],'template source payload binding')
 keys=['kappa','bit_lower','complex_lower','binding_component','bit_profile','complex_profile','bit','complex','bit_template_sha256','emitted_program_sha256','strict_outer_constraints','bootstrap','halving_depth','external_row_allowance','route_extra','dispatch_overhead','complex_wrapper_extra_primitives_per_entry','bank_assignments']
 for k in keys:need(exact(baseline[k],expected[k]),'baseline current witness '+k)
 need(baseline['complex_template_sha256']==th,'baseline fresh complex hash')
 for component,directory in [('bit',parent/'bit'),('complex',provider/'complex')]:
  global_=read(directory/'GLOBAL.json');audit=read(directory/'AUDIT.json');data=gzip.decompress((directory/'GLOBAL-TEMPLATE.json.gz').read_bytes());digest=hashlib.sha256(data).hexdigest()
  need(global_['template_sha256']==audit['template_sha256']==baseline[component+'_template_sha256']==digest,'actual template '+component)
  need(global_['emitted_program_sha256']==audit['emitted_program_sha256'],'actual program records '+component)
  need(exact(audit['profile'],baseline[component+'_profile']),'actual audited profile '+component)
 r377=read('F:/integer-mult-frontier/work/R377-replica84-audit/EXACT-NORMAL-001.json');need(exact(r377['profile'],baseline['bit_profile']),'independent reconstructed84 profile')
 if sharp is None:
  out=dict(status='PASS_ACTUAL_COMPLETED_FULL_PARENT_CONSISTENCY_REVIEW',checker_sha256=sha(pathlib.Path(__file__)),parent_receipt_sha256=sha(parent/'RECEIPT.json'),parent_result_sha256=sha(parent/'RESULT.json'),actual_step_logs_checked=logs,nested_payload_bindings=bindings,actual_canonical_content=content,scope='Completed original full parent consistency only; no actual sharp reuse yet.')
  (R/sys.argv[3]).write_text(json.dumps(out,indent=2)+'\n');print(out['status'],logs);return
 final=read(sharp/'RESULT.json');sr=read(sharp/'RECEIPT.json')
 need(sr['status']=='PASS_SHARP_BIT_INVOICE_COMPLETED_FULL_PARENT_REUSED'and sr['mode']=='completed_full_parent_reuse','sharp scientific status/mode')
 need(sr['package_manifest_sha256']==sha(PACKAGE/'MANIFEST.json')and sr['package_source_sha256']==sha(PACKAGE/'SOURCE.json')and sr['closure_sha256']==sha(PACKAGE/'pins/CLOSURE.json'),'sharp final source binding')
 need(sr['result_sha256']==sha(sharp/'RESULT.json')and sr['assembler_log_sha256']==sha(sharp/'sharp-assemble.log'),'sharp payload/log binding')
 proposal={}
 for n in ['assemble.py','sharp_bit_moment.py']:
  need((sharp/'code'/n).read_bytes()==(PACKAGE/'code'/n).read_bytes(),'actual copied proposal changed');proposal[n]=sha(sharp/'code'/n)
 for rel,h in sr['parent_bindings']['files_sha256'].items():need(sha(safe(parent,rel))==h,'sharp parent payload binding')
 for k in ['bit','complex','bit_profile','complex_profile','complex_lower','binding_component','bit_template_sha256','complex_template_sha256','emitted_program_sha256']:need(exact(final[k],baseline[k]),'changed physical invoice '+k)
 candidate=read(PACKAGE/'EXPECTED.json')
 for k in ['kappa','bit_lower','complex_lower','binding_component','strict_outer_constraints']:need(exact(final[k],candidate[k]),'sharp candidate '+k)
 need(len(final['strict_outer_constraints'])==47 and all(Q(v)>0 for v in final['strict_outer_constraints'].values()),'strict assembly')
 need(Q(final['kappa'])-Q(baseline['kappa'])==Q(candidate['gain_over_pinned_parent']),'exact source-specific improvement')
 out=dict(status='PASS_ACTUAL_COMPLETED_PARENT_AND_SHARP_REUSE_CONSISTENCY_REVIEW',checker_sha256=sha(pathlib.Path(__file__)),python=sys.version,parent_receipt_sha256=sha(parent/'RECEIPT.json'),sharp_receipt_sha256=sha(sharp/'RECEIPT.json'),sharp_result_sha256=sha(sharp/'RESULT.json'),package_manifest_sha256=sha(PACKAGE/'MANIFEST.json'),actual_copied_proposal_sha256=proposal,actual_step_logs_checked=logs,nested_payload_bindings=bindings,actual_canonical_content=content,kappa=final['kappa'],scope='Completed-output source/payload/invoice consistency with independently reviewed84 inventory and R390 matched count-only arithmetic; full producer replay supplied by R378 and corrected sharp R397, inherited all-size assumptions remain conditional.')
 (R/sys.argv[3]).write_text(json.dumps(out,indent=2)+'\n');print(out['status'],final['kappa'],logs)
if __name__=='__main__':main()
