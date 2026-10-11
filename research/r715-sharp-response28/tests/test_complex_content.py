"""Synthetic complete payload fixtures; no supplier or assembler executes."""
from pathlib import Path
import gzip,hashlib,json,platform,sys,tempfile,time,copy
SELF=Path(__file__).resolve().parents[1];sys.path.insert(0,str(SELF/'code'))
import protocol as P
def write(path,value,mtime=0):
    path.parent.mkdir(parents=True,exist_ok=True);data=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
    path.write_bytes(gzip.compress(data,mtime=mtime) if path.name.endswith('.gz') else data)
def fixture(root,mtime=0):
    parent=root/'synthetic-parent'
    for name in P.COMPLEX_FILES[:-1]:write(parent/name,{'fixture_only':True,'name':name,'count':9007199254740993},mtime)
    template={'fixture_only':True,'live':89,'source_bindings':{key:P.sha(parent/name) for key,name in P.COMPLEX_SOURCE_BINDINGS},'calls':[{'local_word_sha256':P.sha(parent/'provider/CANONICAL-WORD.json.gz')}],'arithmetic':{'rank':9}}
    write(parent/P.COMPLEX_FILES[-1],template,mtime);fix_records(parent)
    content,raw,digest=P.measure_complex(parent);records=P.normalized_complex_records(parent,content,raw,digest)
    return parent,content,records
def fix_records(parent):
    digest=hashlib.sha256(gzip.decompress((parent/P.COMPLEX_FILES[-1]).read_bytes())).hexdigest()
    for name in P.COMPLEX_RECORDS:write(parent/name,{'fixture_only':True,'template_sha256':digest,'emitted_program_sha256':'fixture-complex-program','profile':{'1':4},'large_count':9007199254740993})
def main():
    start=time.monotonic();controls=[]
    def reject(name,action,reason):
        try:action()
        except ValueError as error:P.require(reason in str(error),'wrong content rejection');controls.append({'name':name,'reason':str(error)})
        else:raise ValueError('negative accepted '+name)
    with tempfile.TemporaryDirectory(prefix='response-content-fixture-',dir=Path.cwd()) as temp:
        a,expected,records=fixture(Path(temp)/'a',0);b,other,other_records=fixture(Path(temp)/'b',178)
        first=P.complex_payload_binding(a,expected,records);second=P.complex_payload_binding(b,expected,records)
        P.require(P.exact(expected,other) and P.exact(records,other_records),'gzip changed complete canonical data')
        P.require(first['actual_file_sha256']!=second['actual_file_sha256'] and first['actual_template_sha256']!=second['actual_template_sha256'],'raw gzip fixture did not change')
        template=a/P.COMPLEX_FILES[-1];original=template.read_bytes();record_data={n:(a/n).read_bytes() for n in P.COMPLEX_RECORDS}
        for name,path,value,reason in [('live_inventory_change',['live'],90,'canonical complex content'),('source_binding_change',['source_bindings','kernel_word'],'0'*64,'live source binding'),('local_program_change',['calls',0,'local_word_sha256'],'0'*64,'canonical complex content')]:
            changed=json.loads(gzip.decompress(original));node=changed
            for key in path[:-1]:node=node[key]
            node[path[-1]]=value;write(template,changed);fix_records(a)
            reject(name,lambda:P.complex_payload_binding(a,expected,records),reason)
            template.write_bytes(original)
            for n,data in record_data.items():(a/n).write_bytes(data)
        record=a/'complex/GLOBAL.json';original_record=record.read_bytes();changed=json.loads(original_record);changed['large_count']=9007199254740992;write(record,changed)
        reject('complete_record_integer_change',lambda:P.complex_payload_binding(a,expected,records),'complete typed canonical');record.write_bytes(original_record)
        changed=json.loads(original_record);changed['large_count']=float(changed['large_count']);write(record,changed)
        reject('complete_record_float_type_change',lambda:P.complex_payload_binding(a,expected,records),'complete typed canonical');record.write_bytes(original_record)
        changed=json.loads(original_record);changed['unknown_math_field']={'new':1};write(record,changed)
        reject('unknown_record_field_retained',lambda:P.complex_payload_binding(a,expected,records),'complete typed canonical')
    result=dict(status='PASS_RESPONSE_COMPLEX_CONTENT_FIXTURES_ONLY',scientific_supplier_or_assembler_run=False,controls=controls,checker_sha256=P.sha(Path(__file__)),protocol_sha256=P.sha(SELF/'code/protocol.py'),python=platform.python_version(),command=sys.argv,elapsed_seconds=time.monotonic()-start)
    if len(sys.argv)>1:
        out=Path(sys.argv[1]);P.require(not out.exists(),'fixture receipt exists');write(out,result)
    print(result['status'],len(controls),'negatives')
if __name__=='__main__':main()
