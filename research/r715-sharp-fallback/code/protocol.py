"""Source and completed-output bindings, with exact JSON types; Codex assistance."""
from pathlib import Path
import gzip,hashlib,json

def require(test,message):
    if not test:raise ValueError(message)

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path):return json.loads(Path(path).read_bytes())

def exact(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(exact(a[k],v) for k,v in b.items())
    if isinstance(a,list):return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b

def safe(base,name):
    path=(Path(base)/name).resolve();base=Path(base).resolve()
    require(path.is_relative_to(base),'receipt path escapes its output directory')
    return path

def inventory(base):
    return {p.relative_to(base).as_posix():sha(p) for p in Path(base).rglob('*') if p.is_file() and '__pycache__' not in p.parts}

def source_closure(repo,closure):
    repo=Path(repo)
    for name,h in closure['files'].items():require(sha(safe(repo,name))==h,'original source bytes changed: '+name)
    for name,files in closure['package_inventories'].items():
        require(sorted(inventory(safe(repo,name)))==files,'original package inventory changed: '+name)
    return len(closure['files'])

def package_integrity(package):
    actual=inventory(package);actual.pop('MANIFEST.json',None)
    require(actual==read(Path(package)/'MANIFEST.json'),'sharp contribution package manifest differs')

def receipt_tree(parent,source_hashes):
    parent=Path(parent);bound={};checked=0
    # provider-source is a byte-pinned copy of historical inputs, not executed
    # supplier output. Its complete inventory is checked separately by verify.py.
    receipts=sorted(p for p in set(parent.rglob('RECEIPT.json'))|set(parent.rglob('BUILD-RECEIPT.json')) if 'provider-source' not in p.relative_to(parent).parts)
    require(bool(receipts),'no completed receipt tree')
    for path in receipts:
        data=read(path);bound[path.relative_to(parent).as_posix()]=sha(path)
        for step in data.get('steps',[]):
            if 'log_sha256' in step:
                log=safe(path.parent,step['name']+'.log')
                require(sha(log)==step['log_sha256'],'nested step log hash differs: '+str(log.relative_to(parent)))
                bound[log.relative_to(parent).as_posix()]=sha(log);checked+=1
        for name,h in data.get('files',{}).items():
            artifact=safe(path.parent,name)
            require(sha(artifact)==h,'nested artifact hash differs: '+name)
            bound[artifact.relative_to(parent).as_posix()]=sha(artifact);checked+=1
        for name,h in data.get('sources',{}).items():
            require(any(Path(p).name==name and x==h for p,x in source_hashes.items()),'nested source hash outside pinned closure: '+name)
    return {'files_sha256':bound,'nested_bindings_checked':checked}

def template_binding(directory,global_record):
    path=Path(directory)/'GLOBAL-TEMPLATE.json.gz'
    raw=gzip.decompress(path.read_bytes())
    require(hashlib.sha256(raw).hexdigest()==global_record['template_sha256'],'actual decompressed template bytes differ')
    return {'compressed_sha256':sha(path),'uncompressed_sha256':hashlib.sha256(raw).hexdigest()}

COMPLEX_FILES=['provider/FULL-WORD.json.gz','provider/CANONICAL-WORD.json.gz','provider/LOCAL-PROGRAMS.json.gz','provider/NORMALIZED-PROGRAMS.json.gz','provider/SCALAR-FRAME-AUDIT.json','provider/CANONICAL-WRAPPERS.json','provider/LOCAL-CHECKS.json','provider/NORMALIZED-CHECKS.json','provider/CLIFFORD-RECIPES.json','provider/CLIFFORD-REVIEW.json','complex/DATA-PHASES.json','complex/GLOBAL-TEMPLATE.json.gz']
COMPLEX_SOURCE_BINDINGS=[('kernel_word','provider/CANONICAL-WORD.json.gz'),('kernel_canonical_word','provider/CANONICAL-WORD.json.gz'),('kernel_normalized_programs','provider/NORMALIZED-PROGRAMS.json.gz'),('kernel_normalized_checks','provider/NORMALIZED-CHECKS.json'),('kernel_local_audit','provider/SCALAR-FRAME-AUDIT.json'),('kernel_wrapper','provider/CANONICAL-WRAPPERS.json'),('data_phase','complex/DATA-PHASES.json')]

def content_replace(value,bindings):
    if isinstance(value,dict):return {k:content_replace(v,bindings) for k,v in value.items()}
    if isinstance(value,list):return [content_replace(v,bindings) for v in value]
    if isinstance(value,str):return bindings.get(value,value)
    return value

def measure_complex(provider):
    """Reproduce upstream's exact normalization with checks active under -O.

    Only hashes of explicitly read earlier files are replaced by content hashes.
    Every numeric, program and unknown field stays in the canonical hash.
    """
    provider=Path(provider);bindings={};content={};raw_hashes={}
    for name in COMPLEX_FILES:
        data=(provider/name).read_bytes();raw_hashes[name]=hashlib.sha256(data).hexdigest()
        unpacked=gzip.decompress(data) if name.endswith('.gz') else data
        value=json.loads(unpacked)
        normalized=content_replace(value,bindings)
        digest=hashlib.sha256(json.dumps(normalized,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        content[name]=digest
        if name==COMPLEX_FILES[-1]:template=value;template_hash=hashlib.sha256(unpacked).hexdigest()
        else:bindings[raw_hashes[name]]=digest
    for key,name in COMPLEX_SOURCE_BINDINGS:
        require(template['source_bindings'][key]==raw_hashes[name],'complex live source binding differs: '+key)
    for name in ['complex/GLOBAL.json','complex/AUDIT.json','complex/PHYSICAL-AUDIT.json']:
        require(read(provider/name)['template_sha256']==template_hash,'complex actual template record differs: '+name)
    return content,raw_hashes,template_hash

def complex_content_binding(parent,expected_content,pin):
    parent=Path(parent);path=parent/'COMPLEX-CONTENT-RECEIPT.json';receipt=read(path)
    require(receipt['status']==pin['complex_content_receipt_status'],'upstream complex content checker did not pass')
    content,raw,template_hash=measure_complex(parent/'provider')
    require(exact(content,expected_content),'pinned canonical complex content differs')
    require(exact(receipt['content_sha256'],content),'upstream canonical content receipt differs')
    require(exact(receipt['actual_file_sha256'],raw),'upstream complex actual raw receipt differs')
    require(receipt['actual_template_sha256']==template_hash,'upstream actual complex template receipt differs')
    require(exact(receipt['mutations_rejected'],{'changed live stock':'REJECTED','changed source binding':'REJECTED','changed local provider':'REJECTED'}),'upstream complex checker controls differ')
    return {'receipt_sha256':sha(path),'content_sha256':content,'actual_file_sha256':raw,'actual_template_sha256':template_hash}

def parent_binding(parent,expected,pin,closure,expected_content=None):
    parent=Path(parent);receipt=read(parent/'RECEIPT.json')
    require(receipt['status']==pin['parent_receipt_status'],'completed fresh full original parent receipt required')
    require(receipt['manifest_sha256']==pin['parent_manifest_sha256'] and receipt['source_sha256']==pin['parent_source_sha256'],'parent source/manifest pins differ')
    provider=parent/'provider';provider_receipt=read(provider/'RECEIPT.json')
    require(receipt['provider_receipt_sha256']==sha(provider/'RECEIPT.json'),'parent provider receipt hash differs')
    require(provider_receipt['status']==pin['provider_receipt_status'],'completed full provider receipt required')
    require(provider_receipt['manifest_sha256']==pin['provider_manifest_sha256'],'provider adapted manifest pin differs')
    result=read(parent/'RESULT.json')
    fields=['kappa','bit_lower','complex_lower','binding_component','bit_profile','complex_profile','bit','complex','bit_template_sha256','complex_template_sha256','emitted_program_sha256']
    complex_bound=None
    if expected_content is not None:
        require('complex_content_receipt_status' in pin,'source pin has no complex content contract')
        complex_bound=complex_content_binding(parent,expected_content,pin)
        fields.remove('complex_template_sha256')
        require(result['complex_template_sha256']==complex_bound['actual_template_sha256'],'RESULT actual complex template differs')
    for key in ['strict_outer_constraints','bootstrap','halving_depth','external_row_allowance','route_extra','dispatch_overhead','complex_wrapper_extra_primitives_per_entry','bank_assignments']:
        if key in expected:fields.append(key)
    for key in fields:require(exact(result[key],expected[key]),'completed result types/values differ: '+key)
    bg=read(parent/'bit/GLOBAL.json');ba=read(parent/'bit/AUDIT.json');cg=read(provider/'complex/GLOBAL.json');ca=read(provider/'complex/AUDIT.json')
    require(bg['template_sha256']==ba['template_sha256']==result['bit_template_sha256'],'bit template record binding differs')
    require(cg['template_sha256']==ca['template_sha256']==result['complex_template_sha256'],'complex template record binding differs')
    require(bg['emitted_program_sha256']==ba['emitted_program_sha256']==result['emitted_program_sha256'],'bit emitted-program record binding differs')
    require(cg['emitted_program_sha256']==ca['emitted_program_sha256'],'complex emitted-program record binding differs')
    require(exact(ba['profile'],result['bit_profile']) and exact(ca['profile'],result['complex_profile']),'actual audited profile differs')
    bound=receipt_tree(parent,closure['files'])
    if complex_bound:
        bound['complex_content']=complex_bound
        bound['files_sha256']['COMPLEX-CONTENT-RECEIPT.json']=complex_bound['receipt_sha256']
        for name,h in complex_bound['actual_file_sha256'].items():bound['files_sha256']['provider/'+name]=h
        bound['files_sha256']['provider/complex/PHYSICAL-AUDIT.json']=sha(provider/'complex/PHYSICAL-AUDIT.json')
    for name in ['RESULT.json','bit/GLOBAL.json','bit/AUDIT.json','provider/RESULT.json','provider/complex/GLOBAL.json','provider/complex/AUDIT.json']:
        bound['files_sha256'][name]=sha(parent/name)
    bound['bit_template']=template_binding(parent/'bit',bg)
    bound['complex_template']=template_binding(provider/'complex',cg)
    bound['files_sha256']['bit/GLOBAL-TEMPLATE.json.gz']=bound['bit_template']['compressed_sha256']
    bound['files_sha256']['provider/complex/GLOBAL-TEMPLATE.json.gz']=bound['complex_template']['compressed_sha256']
    return result,bound
