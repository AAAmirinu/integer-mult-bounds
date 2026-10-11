"""Compare complete fresh outputs and revalidate every normalized hash binding.

The original two-worker driver and the final optimized variant are the default
full-package comparison. scalar-baseline versus scalar isolates that stage.
Prepared with OpenAI Codex assistance; Apache-2.0.
"""
import argparse,gzip,hashlib,inspect,json,runpy,sys
from pathlib import Path
from fetch import verify,SOURCE
from replay import integrity
ROOT=Path(__file__).resolve().parent
READ=lambda p:json.loads(Path(p).read_text())
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def scalar_equal(a,b,without_time):
    a,b=without_time(a),without_time(b)
    x,y=a['majorant'],b['majorant']
    assert x['residual_bound']==y['residual_bound']==23954
    assert x['packing_bits']==24 and y['packing_bits']==16
    assert 2**y['packing_bits']>2*y['residual_bound']
    y['packing_bits']=x['packing_bits']
    assert a==b,'source receipt changed beyond time and exact encoding width'

def main():
    if not __debug__:raise RuntimeError('assertions required')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('baseline',type=Path);ap.add_argument('candidate',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();left,right=a.baseline.resolve(),a.candidate.resolve()
    if a.output.exists():ap.error('fresh comparison output required')
    if a.output.resolve().is_relative_to(ROOT) and not a.output.resolve().is_relative_to(ROOT/'build'):ap.error('package output must be under build/')
    pin=integrity();verify(SOURCE)
    sys.path.insert(0,str(ROOT/'predecessor-performance'))
    helper=runpy.run_path(str(ROOT/'predecessor-performance/analyze.py'),run_name='packaged_comparison')
    text=inspect.getsource(helper['compare'])
    needle="for p in (a/'predecessor').glob('*.json')}"
    assert text.count(needle)==1
    text=text.replace(needle,"for p in (a/'predecessor').glob('*.json') if p.name!='PERFORMANCE-ADAPTER.json'}")
    ns=dict(helper['compare'].__globals__);exec(compile(text,__file__+'::comparison','exec'),ns)
    comparison=ns['compare'](left,right)
    receipts=[]
    for p in (left/'source353354/newbase-source-admission').glob('*.json'):
        relative=p.relative_to(left);old,new=READ(p),READ(right/relative)
        if p.name=='source-scalar.json':scalar_equal(old,new,helper['without_time'])
        elif p.name=='ADMISSION.json':
            scalar_equal(old.pop('source_scalar'),new.pop('source_scalar'),helper['without_time'])
            assert helper['without_time'](old)==helper['without_time'](new)
        else:assert helper['without_time'](old)==helper['without_time'](new),str(relative)
        receipts.append(str(relative))
    assert len(receipts)==6
    ignored={'PRODUCER-TIMINGS.json','GENERATOR-PERFORMANCE.json'}
    def inventory(root):return {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name not in ignored}
    l,r=left/'source353354/producer-regeneration',right/'source353354/producer-regeneration'
    producer=inventory(l);assert producer==inventory(r)
    for name in producer:
        a0,b0=(l/name).read_bytes(),(r/name).read_bytes()
        if name.endswith('.gz'):a0,b0=gzip.decompress(a0),gzip.decompress(b0)
        assert a0==b0,name
    stats=READ(right/'source353354/SCALAR-PERFORMANCE.json')['adapter']
    assert stats['flags']==dict(geometry=True,unit_add=True,packing=True,transcript=True)
    assert [x['passed'] for x in stats['replays']]==[True]*4+[False]*11
    assert [x['args'] for x in stats['replays'][:4]]==[['F2'],['bound'],['Z',1,16],['Z',-1,16]]
    assert all(x['kwargs']['bits']==24 for x in stats['replays'][4:])
    runs={}
    for label,directory in [('baseline',left),('optimized',right)]:
        run=READ(directory/'PACKAGE-RUN.json');assert run['manifest_sha256']==pin and run['stages']==24
        assert run['source_commit']=='e76d7a94e6ad819e2aa9dc99083ecfa3e7842e0b'
        stages=READ(directory/'VERIFICATION.json')['fresh_stages'];events=[]
        for row in stages:events.extend([(row['started_seconds'],1),(row['finished_seconds'],-1)])
        active=peak=0
        for _,delta in sorted(events):active+=delta;peak=max(active,peak)
        assert active==0 and peak==2
        # Validate every implementation path/hash before using its receipt.
        for name in ('NATIVE-PERFORMANCE-RUN.json','predecessor/PERFORMANCE-ADAPTER.json'):
            p=directory/name
            if p.exists():
                report=READ(p)
                for field in ('implementation_hashes','source_implementation_hashes','implementation_files_unchanged'):
                    for path,digest in report.get(field,{}).items():assert SHA(path)==digest,path
        runs[label]=dict(seconds=run['seconds'],cpu_seconds=run['process_tree_cpu_seconds'],variant=run['variant'],
            python=run['python'],platform=run['platform'],maximum_stage_workers=peak,stages=stages)
    assert runs['baseline']['python']==runs['optimized']['python'] and runs['baseline']['platform']==runs['optimized']['platform']
    assert runs['optimized']['variant']=='scalar' and runs['baseline']['variant'] in ('original','scalar-baseline')
    result=dict(status='PASS_PACKAGED_FULL_NATIVE_AB',source_commit=run['source_commit'],manifest_sha256=pin,
        kappa=run['kappa'],word_sha256=run['word_sha256'],runs=runs,comparison=comparison,
        source_admission_receipts=sorted(receipts),identical_producer_files=sorted(producer),
        full_wall_time_reduction_percent=100*(1-runs['optimized']['seconds']/runs['baseline']['seconds']),
        cpu_time_reduction_percent=100*(1-runs['optimized']['cpu_seconds']/runs['baseline']['cpu_seconds']),
        clean_packing_width=[24,16],adverse_controls=11,negative_control_width=24,
        scope='One same-host sequential pair; all original checks and fresh receipt bindings. No new kappa or current-frontier throughput claim.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','full_wall_time_reduction_percent','cpu_time_reduction_percent')},indent=2))

if __name__=='__main__':main()
