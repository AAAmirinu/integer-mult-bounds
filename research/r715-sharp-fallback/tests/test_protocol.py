"""Protocol fixtures only: these tests do not execute or certify suppliers.
Each synthetic parent and receipt is labelled FIXTURE_ONLY in its content.
"""
from pathlib import Path
import contextlib,copy,gzip,hashlib,io,json,platform,sys,tempfile,time

SELF=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SELF/'code'))
import protocol as P

def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def fixture(root):
    parent=root/'synthetic-parent';provider=parent/'provider'
    fields={'kappa':'1/1000','bit_lower':'1/999','complex_lower':'1/990','binding_component':'bit',
            'bit_profile':{'1':3},'complex_profile':{'1':4},'bit':{'live':1},'complex':{'live':1},'emitted_program_sha256':'synthetic-bit-program'}
    for side,directory,profile,program in [('bit',parent/'bit',fields['bit_profile'],'synthetic-bit-program'),('complex',provider/'complex',fields['complex_profile'],'synthetic-complex-program')]:
        template=json.dumps({'fixture_only':True,'side':side,'operators':[]},sort_keys=True).encode()
        directory.mkdir(parents=True);(directory/'GLOBAL-TEMPLATE.json.gz').write_bytes(gzip.compress(template,mtime=0))
        digest=hashlib.sha256(template).hexdigest();fields[side+'_template_sha256']=digest
        record={'fixture_only':True,'template_sha256':digest,'emitted_program_sha256':program,'profile':profile}
        write(directory/'GLOBAL.json',record);write(directory/'AUDIT.json',record)
    write(parent/'RESULT.json',dict(fields,fixture_only=True));write(provider/'RESULT.json',{'fixture_only':True})
    (provider/'provider-step.log').write_text('FIXTURE_ONLY provider log\n')
    write(provider/'RECEIPT.json',{'fixture_only':True,'status':'FIXTURE_PROVIDER_COMPLETE','manifest_sha256':'fixture-provider-manifest','steps':[{'name':'provider-step','log_sha256':P.sha(provider/'provider-step.log')}]})
    build=provider/'provider';write(build/'proof.json',{'fixture_only':True,'count':9007199254740993})
    write(build/'BUILD-RECEIPT.json',{'fixture_only':True,'files':{'proof.json':P.sha(build/'proof.json')},'sources':{'fixture.py':'fixture-source-hash'}})
    (parent/'parent-step.log').write_text('FIXTURE_ONLY parent log\n')
    pin={'parent_receipt_status':'FIXTURE_PARENT_COMPLETE','provider_receipt_status':'FIXTURE_PROVIDER_COMPLETE','parent_manifest_sha256':'fixture-parent-manifest','parent_source_sha256':'fixture-parent-source','provider_manifest_sha256':'fixture-provider-manifest'}
    write(parent/'RECEIPT.json',{'fixture_only':True,'status':'FIXTURE_PARENT_COMPLETE','manifest_sha256':pin['parent_manifest_sha256'],'source_sha256':pin['parent_source_sha256'],'provider_receipt_sha256':P.sha(provider/'RECEIPT.json'),'steps':[{'name':'parent-step','log_sha256':P.sha(parent/'parent-step.log')}]})
    return parent,fields,pin,{'files':{'code/fixture.py':'fixture-source-hash'}}

def main():
    started=time.monotonic();controls=[]
    def rejection(name,operation,reason):
        try:operation()
        except ValueError as error:
            P.require(reason in str(error),'fixture negative failed for wrong reason: '+name)
            controls.append({'name':name,'reason':str(error)})
        else:raise ValueError('fixture negative accepted: '+name)
    with tempfile.TemporaryDirectory(prefix='sharp-protocol-fixtures-',dir=Path.cwd()) as temporary:
        root=Path(temporary);parent,expected,pin,closure=fixture(root)
        actual,bindings=P.parent_binding(parent,expected,pin,closure)
        P.require(bindings['nested_bindings_checked']==3,'fixture nested receipt inventory wrong')
        # Tampering fails because of a bound mathematical/output value or byte
        # dependency, rather than a final archived report hash alone.
        provider_log=parent/'provider/provider-step.log';original=provider_log.read_bytes();provider_log.write_bytes(b'FIXTURE_ONLY corrupted nested log\n')
        rejection('nested_provider_log_corruption',lambda:P.parent_binding(parent,expected,pin,closure),'nested step log hash');provider_log.write_bytes(original)
        proof=parent/'provider/provider/proof.json';original=proof.read_bytes();proof.write_bytes(b'{"fixture_only":true,"count":1}')
        rejection('nested_build_artifact_corruption',lambda:P.parent_binding(parent,expected,pin,closure),'nested artifact hash');proof.write_bytes(original)
        result=parent/'RESULT.json';original=result.read_bytes();bad=json.loads(original);bad['bit_profile']['1']=3.0;write(result,bad)
        rejection('integer_count_changed_to_float',lambda:P.parent_binding(parent,expected,pin,closure),'types/values');result.write_bytes(original)
        template=parent/'bit/GLOBAL-TEMPLATE.json.gz';original=template.read_bytes();template.write_bytes(gzip.compress(b'{"fixture_only":true,"altered":true}',mtime=0))
        rejection('template_actual_bytes_corruption',lambda:P.parent_binding(parent,expected,pin,closure),'decompressed template bytes');template.write_bytes(original)
        rejection('receipt_path_escape',lambda:P.safe(parent,'../../outside.json'),'escapes')
        receipt=parent/'RECEIPT.json';original=receipt.read_bytes();bad=json.loads(original);bad['status']='FIXTURE_COMPONENT_REUSE';write(receipt,bad)
        rejection('component_receipt_not_full_parent',lambda:P.parent_binding(parent,expected,pin,closure),'fresh full');receipt.write_bytes(original)
        source=root/'fixture-source';file=source/'research/fixture/code.py';file.parent.mkdir(parents=True);file.write_text('fixture_only = True\n')
        capital=file.parent/'A.py';capital.write_text('fixture_only = True\n')
        source_pin={'files':{'research/fixture/code.py':P.sha(file),'research/fixture/A.py':P.sha(capital)},'package_inventories':{'research/fixture':['A.py','code.py']}}
        P.require(P.source_closure(source,source_pin)==2,'mixed-case fixture source positive failed')
        bad_order=copy.deepcopy(source_pin);bad_order['package_inventories']['research/fixture']=['code.py','A.py']
        rejection('nonlexical_source_inventory',lambda:P.source_closure(source,bad_order),'inventory changed')
        original=file.read_bytes();file.write_bytes(b'fixture_only = False\n')
        rejection('original_source_byte_change',lambda:P.source_closure(source,source_pin),'source bytes changed');file.write_bytes(original)
        extra=file.parent/'unlisted.py';extra.write_text('fixture_only = True\n')
        rejection('original_source_inventory_extension',lambda:P.source_closure(source,source_pin),'inventory changed')
        huge=9007199254740993;P.require(type(json.loads(json.dumps(huge))) is int and json.loads(json.dumps(huge))==huge and int(float(huge))!=huge,'large integer corruption control failed')
    result={'status':'PASS_PROTOCOL_FIXTURES_ONLY','scientific_supplier_or_assembler_run':False,'controls':controls,
            'positive':'synthetic completed-parent binding, nested log/build files and template bytes; no supplier algorithms executed',
            'checker_sha256':P.sha(Path(__file__)),'protocol_sha256':P.sha(SELF/'code/protocol.py'),'python':platform.python_version(),'command':sys.argv,'elapsed_seconds':time.monotonic()-started}
    if len(sys.argv)>1:
        target=Path(sys.argv[1]);P.require(not target.exists(),'fixture receipt exists');write(target,result)
    print(result['status'],len(controls),'negative controls')

if __name__=='__main__':main()
