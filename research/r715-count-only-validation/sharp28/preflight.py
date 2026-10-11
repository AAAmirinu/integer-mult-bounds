from pathlib import Path
import json,hashlib
B=Path('F:/integer-mult-frontier/work');H=Path(__file__).resolve().parent
P=B/'R386-response-contribution/revision-001/research/r715-sharp-response28';C=json.loads((P/'pins/CLOSURE.json').read_bytes())
T=json.loads((B/'R372-integration/pr473-f43-tree-001.json').read_bytes());entries={x['path']:x['sha']for x in T['tree']if x['type']=='blob'}
dest=H/'repo';dest.mkdir(exist_ok=False);rows=[]
for rel,expected in C['files'].items():
 p=B/'R383-response-transfer/source'/rel;raw=p.read_bytes();s=hashlib.sha256(raw).hexdigest();g=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
 if s!=expected or entries[rel]!=g:raise ValueError('immutable source mismatch '+rel)
 q=dest/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);rows.append({'path':rel,'sha256':s,'git_blob_sha1':g,'bytes':len(raw)})
(H/'data').mkdir(exist_ok=False)
(H/'SOURCE-PREFLIGHT-001.json').write_text(json.dumps({'status':'PASS_EXACT_198_FILE_SOURCE','head':C['reference_head'],'files':rows},indent=2)+'\n')
print('PASS',len(rows),'source files')
