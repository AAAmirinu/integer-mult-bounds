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

COMPLEX_RECORDS=['complex/GLOBAL.json','complex/AUDIT.json','complex/PHYSICAL-AUDIT.json','complex/INDEPENDENT-ROUTES.json']

def normalized_complex_records(parent,content,raw,template_hash):
    bindings={raw[name]:content[name] for name in COMPLEX_FILES}
    bindings[template_hash]=content[COMPLEX_FILES[-1]]
    return {name:content_replace(read(Path(parent)/name),bindings) for name in COMPLEX_RECORDS}

def complex_payload_binding(parent,expected_content,expected_records):
    content,raw,template_hash=measure_complex(parent)
    require(exact(content,expected_content),'pinned canonical complex content differs')
    records=normalized_complex_records(parent,content,raw,template_hash)
    # Compare full typed dictionaries, not saved margins or selected fields.
    require(exact(records,expected_records),'complete typed canonical complex records differ')
    return {'status':'PASS_COMPLETE_TYPED_COMPLEX_CONTENT_AND_ACTUAL_BYTE_BINDINGS','content_sha256':content,'actual_file_sha256':raw,'actual_template_sha256':template_hash,'record_file_sha256':{name:sha(Path(parent)/name) for name in COMPLEX_RECORDS}}

def parent_binding(parent,expected,pin,closure,expected_content,expected_records):
    parent=Path(parent);receipt=read(parent/'RECEIPT.json')
    require(receipt['status']==pin['parent_receipt_status'],'completed fresh full response28 parent required')
    require(receipt['manifest_sha256']==pin['parent_manifest_sha256'],'parent source manifest pin differs')
    bit_receipt=read(parent/'bit/RECEIPT.json')
    require(bit_receipt['status']==pin['bit_receipt_status'],'completed changed bit supplier required')
    require(receipt['kappa']==expected['kappa'],'full parent receipt kappa differs')
    content_binding=complex_payload_binding(parent,expected_content,expected_records)
    result=read(parent/'RESULT.json')
    # Source EXPECTED covers the entire original assembler result. Only the
    # complex template's byte hash uses the explicitly measured content rule.
    require(result.keys()==expected.keys(),'full original RESULT schema differs')
    for key,value in expected.items():
        if key=='complex_template_sha256':continue
        require(exact(result[key],value),'full original RESULT types/values differ: '+key)
    require(result['complex_template_sha256']==content_binding['actual_template_sha256'],'RESULT actual complex template differs')
    bit=parent/'bit/hosted';bg=read(bit/'GLOBAL.json');ba=read(bit/'AUDIT.json');cg=read(parent/'complex/GLOBAL.json');ca=read(parent/'complex/AUDIT.json')
    require(bg['template_sha256']==ba['template_sha256']==result['bit_template_sha256'],'bit template record binding differs')
    require(bg['emitted_program_sha256']==ba['emitted_program_sha256']==result['emitted_program_sha256'],'bit emitted-program record binding differs')
    require(cg['template_sha256']==ca['template_sha256']==result['complex_template_sha256'],'complex template record binding differs')
    require(cg['emitted_program_sha256']==ca['emitted_program_sha256'],'complex emitted-program record binding differs')
    require(exact(ba['profile'],result['bit_profile']) and exact(ca['profile'],result['complex_profile']),'actual audited profile differs')
    require(bg['m']==78 and bg['replicas']==28 and bg['halving_depth']==3,'actual bit dimensions differ')
    for key in ['live','physical','rank_mass','maxchild']:
        require(exact(ba[key],result['bit'][key]),'actual bit invoice binding differs: '+key)
    require(ba['physical_prefix_bits']==result['bit']['prefix_bits'] and ba['charged_prefix_bits']==bg['charged_prefix_bits']==result['bit']['charged_prefix_bits'],'actual bit prefix invoice differs')
    require(ba['bank_assignments']==result['bank_assignments']==0,'whole-owner bank summary differs')
    bound=receipt_tree(parent,closure['files'])
    bound['complex_content']=content_binding
    for name in ['RESULT.json','bit/hosted/GLOBAL.json','bit/hosted/AUDIT.json','bit/hosted/GEOMETRY.json','bit/nine/GLOBAL.json','bit/nine/GEOMETRY.json']+COMPLEX_RECORDS:
        bound['files_sha256'][name]=sha(parent/name)
    bound['bit_template']=template_binding(bit,bg)
    bound['complex_template']=template_binding(parent/'complex',cg)
    bound['files_sha256']['bit/hosted/GLOBAL-TEMPLATE.json.gz']=bound['bit_template']['compressed_sha256']
    for name,h in content_binding['actual_file_sha256'].items():bound['files_sha256'][name]=h
    return result,bound
