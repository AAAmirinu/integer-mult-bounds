import pathlib,json,hashlib,subprocess,re
R=pathlib.Path(__file__).parent;W=R.parent;S=W/'R404-corrected-publication/publish';V=S/'research/r715-count-only-validation'
def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def files(p):return {x.relative_to(p).as_posix():x for x in p.rglob('*') if x.is_file() and '__pycache__' not in x.parts}
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a],stderr=subprocess.STDOUT,timeout=30)
mf=json.loads((V/'MANIFEST.json').read_bytes());vf=files(V);need(set(mf)==set(vf)-{'MANIFEST.json'},'complete validation inventory');need(all(sha(vf[k])==h for k,h in mf.items()),'validation byte hashes')
mapped={};generated=[]
for name,p in vf.items():
 if name in {'ACCEPTANCE.json','README.md','MANIFEST.json'}:generated.append(name);continue
 parts=name.split('/');first=parts[0];tail='/'.join(parts[1:])
 if first.startswith('R39'):
  orig=W/first/tail
 elif first in {'sharp84','sharp28'}:
  base=W/('R397-count84-actual' if first=='sharp84' else 'R392-response28-actual')
  orig=base/('data/'+tail if parts[1] in {'normal-001','optimized-001'} or parts[1].startswith('launcher-') else tail)
 elif first in {'parent84','parent28'}:
  base=W/('R378-pr473-replica84' if first=='parent84' else 'R385-response28-full')/'data'
  orig=base/tail if parts[1].startswith('launcher-') else base/('full-001' if first=='parent84' else 'full-002')/tail
 elif first=='docs-only':orig=W/'R395-count-only-correction'/parts[1]/'revision-002'/parts[2]
 elif name=='COVER-CORRECTION-001.json':orig=W/'R372-integration'/name
 else:raise ValueError('unmapped copy '+name)
 need(orig.is_file() and p.read_bytes()==orig.read_bytes(),'raw copy '+name);mapped[name]=sha(orig)
packs={}
for kind,leaf in [('replica84','r715-sharp-fallback'),('response28','r715-sharp-response28')]:
 base=W/'R395-count-only-correction'/kind;one=base/'revision-001/research'/leaf;two=base/'revision-002/research'/leaf;pub=S/'research'/leaf
 a,b,c=files(one),files(two),files(pub);need(set(a)==set(b)==set(c),'package inventories')
 changed=[k for k in a if a[k].read_bytes()!=b[k].read_bytes()];need(sorted(changed)==['MANIFEST.json','README.md'],'only docs changed')
 need(all(b[k].read_bytes()==c[k].read_bytes() for k in b),'publication exact package')
 manifest=json.loads((two/'MANIFEST.json').read_bytes());need(set(manifest)==set(b)-{'MANIFEST.json'},'package complete manifest');need(all(sha(b[k])==h for k,h in manifest.items()),'package byte manifest')
 readme=(two/'README.md').read_text();need('research/'+leaf+'/verify.py' in readme and 'research/MATCHED-MATH' not in readme,'CLI corrected')
 repo=R/('git-002-'+kind);need(not repo.exists(),'new Git fixture');repo.mkdir();git(repo,'init');git(repo,'config','core.autocrlf','true');patch=base/'revision-002/contribution.patch';git(repo,'-c','core.autocrlf=false','apply','--whitespace=nowarn',str(patch));git(repo,'add','research/'+leaf)
 for k,p in b.items():
  path='research/'+leaf+'/'+k;need((repo/path).read_bytes()==p.read_bytes(),'patch working '+path);need(git(repo,'show',':'+path)==p.read_bytes(),'patch index '+path)
 packs[kind]={'manifest_revision001':sha(one/'MANIFEST.json'),'manifest_revision002':sha(two/'MANIFEST.json'),'patch_sha256':sha(patch),'changed_files':sorted(changed),'git_exact_files':len(b),'code_math_expected_source_unchanged':True}
acc=json.loads((V/'ACCEPTANCE.json').read_bytes());need(acc['claim'].find('inherited O-cover fraction1/10^16 retained')>=0,'cover conditional');need('No current-record or unconditional/all-size proof claim' in acc['claim'],'scope')
for kind,num,den,gain in [('replica84',1295629943312713,10**18,725591),('response28',648305991611853,5*10**17,728599)]:
 need(acc[kind]['kappa']==str(num)+'/'+str(den),'exact kappa');need(acc[kind]['gain']==str(gain)+'/'+str(10**18),'exact gain');need(acc['published_package_manifests'][kind]==packs[kind]['manifest_revision002'],'published manifest explicit')
 hist=S/'research/r715-sharp-fallback-validation';need((hist/'ACCEPTANCE-WITHDRAWN.json').read_bytes()==(W/'R372-integration/publish/research/r715-sharp-fallback-validation/ACCEPTANCE.json').read_bytes(),'immutable historical acceptance');need(json.loads((hist/'ACCEPTANCE.json').read_bytes())['status']=='WITHDRAWN_PROBABILITY_TRANSFER_ACCEPTANCE','withdrawal override')
# Scan content without displaying any possible secret. Local/container provenance
# paths and author attribution are expected scientific metadata, not credentials.
patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{30,}',r'Bearer\s+[A-Za-z0-9._-]{20,}',r'AKIA[0-9A-Z]{16}']
hits=[]
for k,p in files(S).items():
 text=p.read_bytes().decode('utf8')
 for i,pat in enumerate(patterns):
  if re.search(pat,text):hits.append({'path':k,'pattern':i})
need(not hits,'credential-shaped content found')
out={'status':'PASS_DOCS_ONLY_BYTE_AND_STAGING_INTEGRITY_PENDING_FRESH_REVISION002_BINDING','scientific_replay':False,'validation_manifest_sha256':sha(V/'MANIFEST.json'),'acceptance_sha256':sha(V/'ACCEPTANCE.json'),'raw_copies':mapped,'generated_metadata':generated,'packages':packs,'credentials_scan_hits':hits,'old_actual_scope':'revision001 only; independent exact README/MANIFEST delta permits code/math transfer but does not rewrite actual manifest receipts','checker_sha256':sha(pathlib.Path(__file__))}
(R/'STAGING-REVIEW-001.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(mapped),packs)
