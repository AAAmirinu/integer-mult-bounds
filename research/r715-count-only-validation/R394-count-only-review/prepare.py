import pathlib,json,hashlib
B=pathlib.Path(__file__).resolve().parent
H=pathlib.Path('F:/integer-mult-frontier/work')
sha=lambda x:hashlib.sha256(x).hexdigest()
entries=[]
for name,old,pkg,head in [('response28','R384-response-sharp-review','research/r715-response-replica28','f43a0e9ad04a7b3683498274854ae2e35d4a8d7c'),('replica84','R379-sharp84-review','research/r715-replica84-complex79','c7590f1d861f0eaae725cc79901445385aab9125')]:
 lockraw=(H/old/'source-lock-001.json').read_bytes(); lock=json.loads(lockraw)
 chosen=[r for r in lock['files'] if r['path']==pkg+'/EXPECTED.json' or r['path']=='notes/three-stage-cover-bit.tex' or r['path'].endswith('/finite_k.py')]
 for row in chosen:
  data=(H/old/'sources'/row['path']).read_bytes()
  if sha(data)!=row['sha256'] or hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()!=row['git_blob_sha1']:raise ValueError('source hash mismatch')
  dest=B/'sources'/name/row['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
  entries.append(dict(profile=name,head=head,canonical_repository='rohanarun/integer-mult-bounds',original_review_lock_sha256=sha(lockraw),**row))
 (B/(name+'-EXPECTED.json')).write_bytes((H/old/'sources'/pkg/'EXPECTED.json').read_bytes())
(B/'SOURCE-LOCK-001.json').write_text(json.dumps({'files':entries,'scope':'Raw EXPECTED and Gaussian child-count derivation sources; canonical repository corrected from earlier retrieval fork attribution'},indent=2)+'\n')
text=(H/'R384-response-sharp-review'/'independent.py').read_text().split('def main():')[0]
text='import sys\nsys.dont_write_bytecode=True\n'+text
(B/'independent.py').write_text(text+(B/'main-fragment.txt').read_text())
