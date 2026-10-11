"""Response-layout protocol fixtures only; no supplier algorithm executes."""
from pathlib import Path
import copy,gzip,hashlib,json,platform,sys,tempfile,time
import test_complex_content as F
P=F.P;SELF=F.SELF;write=F.write
def fixture(root):
    parent,content,records=F.fixture(root);bit=parent/'bit/hosted';data=json.dumps({'fixture_only':True,'operators':[]},sort_keys=True).encode();bit.mkdir(parents=True);(bit/'GLOBAL-TEMPLATE.json.gz').write_bytes(gzip.compress(data,mtime=0));digest=hashlib.sha256(data).hexdigest()
    invoice=dict(live=33600,physical=33609,rank_mass=2609376,maxchild=56,prefix_bits=2060,charged_prefix_bits=2112,charged_two_level_coefficient_bits=6272)
    fields=dict(fixture_only=True,kappa='1/1000',bit_lower='1/999',complex_lower='1/990',binding_component='bit',bit_profile={'1':3},complex_profile={'1':4},bit=invoice,complex={'fixture_only':True,'live':89},bit_template_sha256=digest,complex_template_sha256=P.measure_complex(parent)[2],emitted_program_sha256='fixture-bit-program',bank_assignments=0,strict_outer_constraints={'fixture_only':'1'})
    record=dict(fixture_only=True,template_sha256=digest,emitted_program_sha256='fixture-bit-program',profile=fields['bit_profile'],m=78,replicas=28,halving_depth=3,physical_prefix_bits=2060,bank_assignments=0,**invoice)
    write(bit/'GLOBAL.json',record);write(bit/'AUDIT.json',record);write(bit/'GEOMETRY.json',{'fixture_only':True});write(parent/'bit/nine/GLOBAL.json',record);write(parent/'bit/nine/GEOMETRY.json',{'fixture_only':True});write(parent/'RESULT.json',fields)
    pin=dict(parent_receipt_status='FIXTURE_FULL_RESPONSE_PARENT',bit_receipt_status='FIXTURE_CHANGED_BIT_COMPLETE',parent_manifest_sha256='fixture-manifest')
    for directory,status in [(parent,pin['parent_receipt_status']),(parent/'bit',pin['bit_receipt_status'])]:
        (directory/'step.log').write_text('FIXTURE_ONLY log\n');write(directory/'RECEIPT.json',dict(fixture_only=True,status=status,kappa=fields['kappa'],manifest_sha256=pin['parent_manifest_sha256'],steps=[dict(name='step',log_sha256=P.sha(directory/'step.log'))]))
    write(parent/'provider/proof.json',{'fixture_only':True,'count':9007199254740993});write(parent/'provider/BUILD-RECEIPT.json',dict(fixture_only=True,files={'proof.json':P.sha(parent/'provider/proof.json')},sources={'fixture.py':'fixture-source'}))
    return parent,fields,pin,{'files':{'code/fixture.py':'fixture-source'}},content,records
def main():
    started=time.monotonic();controls=[]
    def reject(name,action,reason):
        try:action()
        except ValueError as error:P.require(reason in str(error),'wrong protocol rejection');controls.append(dict(name=name,reason=str(error)))
        else:raise ValueError('negative accepted '+name)
    with tempfile.TemporaryDirectory(prefix='response-protocol-fixture-',dir=Path.cwd()) as temp:
        root=Path(temp);args=fixture(root);parent=args[0];_,bindings=P.parent_binding(*args);P.require(bindings['nested_bindings_checked']==3,'nested fixture receipt inventory wrong')
        for name,path,bad,reason in [('nested_log',parent/'bit/step.log',b'FIXTURE_ONLY corrupt','nested step log'),('build_artifact',parent/'provider/proof.json',b'{}','nested artifact'),('bit_template',parent/'bit/hosted/GLOBAL-TEMPLATE.json.gz',gzip.compress(b'{}'), 'decompressed template')]:
            old=path.read_bytes();path.write_bytes(bad);reject(name,lambda:P.parent_binding(*args),reason);path.write_bytes(old)
        result=parent/'RESULT.json';original=result.read_bytes();bad=json.loads(original);bad['bit_profile']['1']=3.0;write(result,bad);reject('float_profile',lambda:P.parent_binding(*args),'types/values');result.write_bytes(original)
        bad=json.loads(original);bad['new_math_field']=1;write(result,bad);reject('unlisted_result_field',lambda:P.parent_binding(*args),'schema differs');result.write_bytes(original)
        receipt=parent/'RECEIPT.json';original=receipt.read_bytes();bad=json.loads(original);bad['status']='FIXTURE_COMPLEX_REUSED';write(receipt,bad);reject('component_reuse_not_full',lambda:P.parent_binding(*args),'fresh full');receipt.write_bytes(original)
        reject('path_escape',lambda:P.safe(parent,'../../escape'),'escapes')
        source=root/'source';source.mkdir();(source/'A.py').write_text('fixture_only=True');(source/'code.py').write_text('fixture_only=True')
        closure=dict(files={n:P.sha(source/n) for n in ['A.py','code.py']},package_inventories={'':['A.py','code.py']});P.require(P.source_closure(source,closure)==2,'source closure mixed-case fixture failed')
        bad=copy.deepcopy(closure);bad['package_inventories']['']=['code.py','A.py'];reject('nonlexical_inventory',lambda:P.source_closure(source,bad),'inventory changed')
        (source/'code.py').write_text('fixture_only=False');reject('source_byte_change',lambda:P.source_closure(source,closure),'source bytes')
    result=dict(status='PASS_RESPONSE_PROTOCOL_FIXTURES_ONLY',scientific_supplier_or_assembler_run=False,controls=controls,checker_sha256=P.sha(Path(__file__)),protocol_sha256=P.sha(SELF/'code/protocol.py'),python=platform.python_version(),command=sys.argv,elapsed_seconds=time.monotonic()-started)
    if len(sys.argv)>1:
        out=Path(sys.argv[1]);P.require(not out.exists(),'fixture receipt exists');write(out,result)
    print(result['status'],len(controls),'negatives')
if __name__=='__main__':main()
