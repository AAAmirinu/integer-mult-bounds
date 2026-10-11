import pathlib,json,hashlib,re
R=pathlib.Path(__file__).parent;W=R.parent;P=W/'R404-corrected-publication/publish';V=P/'research/r715-count-only-validation'
def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
old=read(R/'STAGING-REVIEW-001.json');mf=read(V/'MANIFEST.json');actual={p.relative_to(V).as_posix():sha(p) for p in V.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
need(mf==actual,'final complete validation bytes')
for name,h in old['raw_copies'].items():need(actual[name]==h,'prior raw evidence changed '+name)
new={};generated=[]
for name,h in actual.items():
 if name in old['raw_copies'] or name in {'ACCEPTANCE.json','README.md'}:continue
 parts=name.split('/')
 if parts[0]=='docs-only-actual':
  root=W/'R406-docs-revision-actual'/parts[1];tail='/'.join(parts[2:]);orig=root/('data/'+tail if parts[2] in {'normal-001','optimized-001'} or parts[2].startswith('launcher-') else tail)
 elif parts[0]=='required-checks':
  if parts[1]=='STATUS.json':generated.append(name);continue
  orig=W/'R393-required-repository-checks'/parts[1]
 else:raise ValueError('unmapped addition '+name)
 need(orig.read_bytes()==(V/name).read_bytes(),'new raw copy '+name);new[name]=h
acc=read(V/'ACCEPTANCE.json');need(acc['docs_only_revision002_actual']['status']=='PASS_FOUR_ACTUAL_COMPLETED_PARENT_REUSE_ASSEMBLIES','002 status');need('reused explicitly' in acc['docs_only_revision002_actual']['scope'],'full parent reuse honest')
need('no all-checks-pass claim' in acc['required_baseline_checks'],'required-check limitation');baseline=read(V/'required-checks/STATUS.json');need(baseline['status']=='REQUIRED_BASELINE_CHECKS_NOT_ALL_PASS','baseline status')
for kind,key in [('84','replica84'),('28','response28')]:
 for mode in ['normal','optimized']:
  pub=V/'docs-only-actual'/kind/(mode+'-001');rr=read(pub/'RECEIPT.json');need(rr['package_manifest_sha256']==old['packages'][key]['manifest_revision002'],'002 raw manifest');need(rr['result_sha256']==sha(pub/'RESULT.json'),'002 actual bytes')
 need((V/'docs-only-actual'/kind/'normal-001/RESULT.json').read_bytes()==(V/'docs-only-actual'/kind/'optimized-001/RESULT.json').read_bytes(),'002 result equality')
hits=[]
for p in P.rglob('*'):
 if p.is_file():
  s=p.read_bytes().decode('utf8')
  if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|Bearer\s+[A-Za-z0-9._-]{20,}|AKIA[0-9A-Z]{16}',s):hits.append(p.relative_to(P).as_posix())
need(not hits,'credential shaped publication contents')
inventory={p.relative_to(P).as_posix():sha(p) for p in P.rglob('*') if p.is_file()}
out={'status':'PASS_FINAL_CORRECTED_PUBLICATION_SNAPSHOT_SCOPED','validation_manifest_sha256':sha(V/'MANIFEST.json'),'acceptance_sha256':sha(V/'ACCEPTANCE.json'),'new_raw_copies':new,'new_generated_metadata':generated,'published_file_inventory':inventory,'actual_revision002_independent_receipts':['84-ACTUAL-NORMAL-002.json','84-ACTUAL-OPTIMIZED-002.json','28-ACTUAL-NORMAL-002.json','28-ACTUAL-OPTIMIZED-002.json','REVISION002-TERMINALS-001.json'],'required_baseline_all_pass':False,'publication_scope':'Count-only matched source improvement conditional on inherited O-cover and compiler/hosting; distinct current frontier and broad required baseline checks. Later staging mutations require new snapshot binding.','checker_sha256':sha(pathlib.Path(__file__))}
(R/'FINAL-SNAPSHOT-001.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(inventory),len(new))
