import pathlib,json,hashlib
B=pathlib.Path(__file__).resolve().parent;H=B.parent;sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
for name,old,pkg in [('response28','R384-response-sharp-review','research/r715-response-replica28'),('replica84','R379-sharp84-review','research/r715-replica84-complex79')]:
 lock=json.loads((H/old/'source-lock-001.json').read_bytes())
 for row in lock['files']:
  if row['path'] not in (pkg+'/PROOF.md',pkg+'/code/assemble.py',pkg+'/MANIFEST.json') and not row['path'].endswith('parent436/code/bit/checkers/finite_k.py'):continue
  data=(H/old/'sources'/row['path']).read_bytes()
  if sha(data)!=row['sha256'] or hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=row['git_blob_sha1']:raise ValueError('proof source mismatch')
  dest=B/'proof-sources'/name/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
  rows.append(dict(profile=name,head=lock['head'],canonical_repository='rohanarun/integer-mult-bounds',**row))
(B/'PROOF-SOURCE-LOCK-001.json').write_text(json.dumps({'files':rows,'scope':'Supplementary proof/source authentication, append-only to arithmetic lock'},indent=2)+'\n')
x=json.loads((B/'normal-001.json').read_bytes());y=json.loads((B/'optimized-001.json').read_bytes())
if x['profiles']!=y['profiles'] or x['checker_sha256']!=y['checker_sha256']:raise ValueError('normal/OO differ')
bindings={p.name:sha(p.read_bytes()) for p in [B/'independent.py',B/'SOURCE-LOCK-001.json',B/'PROOF-SOURCE-LOCK-001.json',B/'normal-001.json',B/'optimized-001.json']}
(B/'BINDINGS-001.json').write_text(json.dumps({'sha256':bindings,'normal_optimized_exact_profiles_identical':True},indent=2)+'\n')
print(json.dumps(bindings,indent=2))
