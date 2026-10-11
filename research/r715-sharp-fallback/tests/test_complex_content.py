"""Synthetic content protocol fixtures only; no scientific supplier executes."""
from pathlib import Path
import gzip,hashlib,json,platform,sys,tempfile,time
SELF=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SELF/'code'))
import protocol as P

def write(path,value,mtime=0):
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
    path.write_bytes(gzip.compress(data,mtime=mtime) if path.name.endswith('.gz') else data)

def fixture(root,mtime):
    parent=root/'synthetic-parent';provider=parent/'provider'
    for name in P.COMPLEX_FILES[:-1]:write(provider/name,{'fixture_only':True,'name':name,'count':9007199254740993},mtime)
    template={'fixture_only':True,'live':89,'source_bindings':{key:P.sha(provider/name) for key,name in P.COMPLEX_SOURCE_BINDINGS},'calls':[{'local_word_sha256':P.sha(provider/'provider/CANONICAL-WORD.json.gz')}],'arithmetic':{'rank':9}}
    write(provider/P.COMPLEX_FILES[-1],template,mtime)
    fix_records(provider)
    content,raw,template_hash=P.measure_complex(provider)
    write(parent/'COMPLEX-CONTENT-RECEIPT.json',dict(fixture_only=True,status='FIXTURE_CONTENT_PASS',content_sha256=content,actual_file_sha256=raw,actual_template_sha256=template_hash,mutations_rejected={'changed live stock':'REJECTED','changed source binding':'REJECTED','changed local provider':'REJECTED'}))
    return parent,content,{'complex_content_receipt_status':'FIXTURE_CONTENT_PASS'}

def fix_records(provider):
    digest=hashlib.sha256(gzip.decompress((provider/P.COMPLEX_FILES[-1]).read_bytes())).hexdigest()
    for name in ['GLOBAL.json','AUDIT.json','PHYSICAL-AUDIT.json']:write(provider/'complex'/name,{'fixture_only':True,'template_sha256':digest})

def main():
    start=time.monotonic();controls=[]
    def reject(name,action,reason):
        try:action()
        except ValueError as error:
            P.require(reason in str(error),'wrong content fixture rejection: '+str(error));controls.append({'name':name,'reason':str(error)})
        else:raise ValueError('content negative accepted '+name)
    with tempfile.TemporaryDirectory(prefix='sharp-content-fixture-',dir=Path.cwd()) as temp:
        root=Path(temp);a,expected,pin=fixture(root/'a',0);b,b_expected,b_pin=fixture(root/'b',178)
        ba=P.complex_content_binding(a,expected,pin);bb=P.complex_content_binding(b,expected,b_pin)
        P.require(P.exact(expected,b_expected),'gzip header changes altered canonical fixture content')
        P.require(ba['actual_file_sha256']!=bb['actual_file_sha256'],'header fixture did not alter raw hashes')
        P.require(ba['actual_template_sha256']!=bb['actual_template_sha256'],'header consequence did not alter actual template')
        template=a/'provider/complex/GLOBAL-TEMPLATE.json.gz';original=template.read_bytes();record_paths=[a/'provider/complex'/n for n in ['GLOBAL.json','AUDIT.json','PHYSICAL-AUDIT.json']];records=[p.read_bytes() for p in record_paths]
        value=json.loads(gzip.decompress(original));value['live']+=1;write(template,value);fix_records(a/'provider')
        reject('live_inventory_change',lambda:P.complex_content_binding(a,expected,pin),'canonical complex content')
        template.write_bytes(original)
        for path,data in zip(record_paths,records):path.write_bytes(data)
        value=json.loads(gzip.decompress(original));value['source_bindings']['kernel_word']='0'*64;write(template,value);fix_records(a/'provider')
        reject('source_binding_change',lambda:P.complex_content_binding(a,expected,pin),'live source binding')
        template.write_bytes(original)
        for path,data in zip(record_paths,records):path.write_bytes(data)
        value=json.loads(gzip.decompress(original));value['calls'][0]['local_word_sha256']='0'*64;write(template,value);fix_records(a/'provider')
        reject('local_program_change',lambda:P.complex_content_binding(a,expected,pin),'canonical complex content')
        template.write_bytes(original)
        for path,data in zip(record_paths,records):path.write_bytes(data)
        receipt=a/'COMPLEX-CONTENT-RECEIPT.json';original_receipt=receipt.read_bytes();bad=json.loads(original_receipt);bad['actual_file_sha256'][P.COMPLEX_FILES[0]]='0'*64;write(receipt,bad)
        reject('checker_raw_receipt_change',lambda:P.complex_content_binding(a,expected,pin),'actual raw receipt');receipt.write_bytes(original_receipt)
        bad=json.loads(original_receipt);bad['actual_template_sha256']='0'*64;write(receipt,bad)
        reject('checker_actual_template_change',lambda:P.complex_content_binding(a,expected,pin),'actual complex template receipt');receipt.write_bytes(original_receipt)
        bad=json.loads(original_receipt);bad['status']='FIXTURE_INCOMPLETE';write(receipt,bad)
        reject('checker_incomplete',lambda:P.complex_content_binding(a,expected,pin),'checker did not pass');receipt.write_bytes(original_receipt)
        bad=json.loads(original_receipt);bad['content_sha256'][P.COMPLEX_FILES[0]]='0'*64;write(receipt,bad)
        reject('checker_canonical_receipt_change',lambda:P.complex_content_binding(a,expected,pin),'canonical content receipt');receipt.write_bytes(original_receipt)
    result=dict(status='PASS_COMPLEX_CONTENT_FIXTURES_ONLY',scientific_supplier_or_assembler_run=False,controls=controls,positive='Synthetic gzip headers change raw hashes and consequent template references; exact mathematical content remains pinned.',checker_sha256=P.sha(Path(__file__)),protocol_sha256=P.sha(SELF/'code/protocol.py'),python=platform.python_version(),command=sys.argv,elapsed_seconds=time.monotonic()-start)
    if len(sys.argv)>1:
        out=Path(sys.argv[1]);P.require(not out.exists(),'fixture receipt exists');write(out,result)
    print(result['status'],len(controls),'negative controls')
if __name__=='__main__':main()
