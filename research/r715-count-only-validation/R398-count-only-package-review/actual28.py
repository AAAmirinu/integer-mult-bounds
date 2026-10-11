"""Independent actual count-only response28 receipt binding; no producer imports."""
import pathlib,json,hashlib,sys
from fractions import Fraction as Q
R=pathlib.Path(__file__).parent;PK=R/'snapshot-28-001';P=pathlib.Path('F:/integer-mult-frontier/work/R385-response28-full/data/full-002');read=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def exact(a,b):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(exact(a[k],b[k])for k in a)
 if isinstance(a,list):return len(a)==len(b)and all(exact(x,y)for x,y in zip(a,b))
 return a==b
def main():
 sharp=pathlib.Path(sys.argv[1]);admission_path=pathlib.Path('F:/integer-mult-frontier/work/R396-response-actual-review/ACTUAL-PARENT-NORMAL-001.json');prior=read(admission_path);need(prior['status']=='PASS_INDEPENDENT_ACTUAL_FRESH_RESPONSE28_PARENT_ADMISSION','actual parent not admitted')
 need(prior['parent_receipt_sha256']==sha(P/'RECEIPT.json')and prior['actual_result_sha256']==sha(P/'RESULT.json'),'admitted parent changed')
 for name,h in list(prior['bindings'].items())+list(prior['complex_raw'].items()):need(sha(P/name)==h,'admitted parent payload changed '+name)
 parent=read(P/'RESULT.json');final=read(sharp/'RESULT.json');receipt=read(sharp/'RECEIPT.json');expected=read(PK/'EXPECTED.json');need(receipt['status']=='PASS_SHARP_RESPONSE28_COMPLETED_FULL_PARENT_REUSED'and receipt['mode']=='completed_full_parent_reuse','sharp mode')
 for field,name in [('package_manifest_sha256','MANIFEST.json'),('package_source_sha256','SOURCE.json'),('closure_sha256','pins/CLOSURE.json')]:need(receipt[field]==sha(PK/name),'final package binding')
 need(receipt['result_sha256']==sha(sharp/'RESULT.json')and receipt['assembler_log_sha256']==sha(sharp/'sharp-assemble.log'),'actual sharp result/log')
 copied={}
 for name in ['assemble.py','sharp_bit_moment.py']:
  need((sharp/'code'/name).read_bytes()==(PK/'code'/name).read_bytes(),'actual code copy');copied[name]=sha(sharp/'code'/name)
 for name,h in receipt['parent_bindings']['files_sha256'].items():
  f=(P/name).resolve();need(f.is_relative_to(P.resolve()),'path escape');need(sha(f)==h,'actual parent raw binding '+name)
 cb=receipt['parent_bindings']['complex_content'];need(exact(cb['actual_file_sha256'],prior['complex_raw'])and exact(cb['content_sha256'],prior['complex_content'])and cb['actual_template_sha256']==prior['actual_complex_template_sha256'],'actual full canonical contract')
 for name,h in cb['record_file_sha256'].items():need(sha(P/name)==h,'actual full typed record binding')
 for key in ['complex_lower','binding_component','bit_profile','complex_profile','bit','complex','bit_template_sha256','complex_template_sha256','emitted_program_sha256','bank_assignments','route_extra','dispatch_overhead','halving_depth','external_row_allowance']:
  need(exact(final[key],parent[key]),'physical invoice or supplier changed '+key)
 for key in ['kappa','bit_lower','complex_lower','binding_component','strict_outer_constraints','bootstrap']:need(exact(final[key],expected[key]),'actual sharp mathematics '+key)
 need(expected['fallback_children']==146478 and expected['bad_fraction']=='1/10000000000000000','unchanged O bad law');need(Q(final['kappa'])-Q(parent['kappa'])==Q(expected['gain_over_pinned_parent'])==Q(728599,10**18),'gain');need(len(final['strict_outer_constraints'])==47 and all(Q(x)>0 for x in final['strict_outer_constraints'].values()),'47 strict inequalities');need(final['bit']['charged_prefix_bits']==2112 and final['bit']['charged_two_level_coefficient_bits']==6272 and final['bit']['row_coefficient']==19434,'source physical bills')
 result=dict(status='PASS_INDEPENDENT_ACTUAL_CORRECTED_COUNT_ONLY_RESPONSE28',package_manifest_sha256=sha(PK/'MANIFEST.json'),package_source_sha256=sha(PK/'SOURCE.json'),parent_admission_sha256=sha(admission_path),parent_receipt_sha256=sha(P/'RECEIPT.json'),sharp_receipt_sha256=sha(sharp/'RECEIPT.json'),sharp_result_sha256=sha(sharp/'RESULT.json'),actual_proposal_sha256=copied,kappa=final['kappa'],gain=expected['gain_over_pinned_parent'],bad_fraction=expected['bad_fraction'],fallback_children=146478,checker_sha256=sha(pathlib.Path(__file__)),scope='Actual count-only sharp assembly against completed original fresh28 supplier and immutable reviewed package; O bad-class law remains inherited conditional assumption. No new O theorem or GL transfer.')
 (R/sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n');print(result['status'],final['kappa'])
if __name__=='__main__':main()
