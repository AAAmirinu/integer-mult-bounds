"""Complete physical replay of PR384's unit in PR377, following PR385's derivation.

Original suppliers stay immutable. Every derived input/assertion change is
recorded; scalar, lifetime, Clifford, global and finite checks are retained.
Prepared with substantial OpenAI Codex assistance; Apache-2.0.
"""
from pathlib import Path
import argparse,gzip,hashlib,json,os,shutil,subprocess,sys
sys.set_int_max_str_digits(0)
ROOT=Path(__file__).resolve().parent
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')

def prepare(out):
    out=Path(out).resolve();out.mkdir(parents=True,exist_ok=False)
    shutil.copytree(ROOT/'vendor/source377/work',out/'work')
    C=out/'work/native358/vendor/complex-reserve/upstream/pr352/code/complex'
    changes={}
    def modify(path,data):
        changes[path.relative_to(out).as_posix()]=dict(before=sha(path),after=hashlib.sha256(data).hexdigest())
        path.write_bytes(data)
    cert=(ROOT/'vendor/source384/data/gcert1-e8-r783-far.json.gz').read_bytes()
    raw=gzip.decompress(cert)
    modify(C/'inputs/e8/tools/certificate/gcert1-e8-r783.json.gz',cert)
    modify(out/'work/pr361/complex/gcert1-e8-r783.json.gz',cert)
    pins=read(C/'inputs/complex/source-pins.json')
    pins['certificate'].update(compressed_sha256=hashlib.sha256(cert).hexdigest(),uncompressed_sha256=hashlib.sha256(raw).hexdigest(),source_pin='fd81a16a1e4e82acfb4d45752cba17450644fde6',url='https://github.com/CrocSwap/integer-mult-bounds/pull/384')
    modify(C/'inputs/complex/source-pins.json',(json.dumps(pins,indent=2)+'\n').encode())
    original=read(C/'pins-e8.json');fresh=read(ROOT/'data/FAR-PINS.json')
    for key in ('V','R','H','cst','N','scatter','centre_ranks','stock_bits'):assert fresh[key]==original[key],key
    assert sum(fresh['label_histogram'].values())==3973
    modify(C/'pins-e8.json',(json.dumps(fresh,indent=2)+'\n').encode())
    for name,old,new in [('global_nine.py','local_children==3974','local_children==3973'),('audit_nine_template.py','999240641319551','999632926176283')]:
        p=out/'work/odd-stages'/name;s=p.read_text(encoding='utf-8');assert s.count(old)==1
        modify(p,s.replace(old,new).encode())
    write(out/'DERIVATION.json',dict(changes=changes,scope='Retimed certificate, its exact input/census/bill pins, local child count and expected price only. All algorithms and controls are retained.'))
    return C

def run(out,baseline):
    out=Path(out).resolve();baseline=Path(baseline).resolve();C=prepare(out)
    def execute(script,args,name):
        print('RUN_FAR',name,flush=True)
        with (out/(name+'.log')).open('w',encoding='utf-8',newline='\n') as stream:
            subprocess.run([sys.executable,'-B',str(ROOT/'run_pinned.py'),str(script),*map(str,args)],cwd=out,stdout=stream,stderr=subprocess.STDOUT,check=True)
    cert=ROOT/'vendor/source384/data/gcert1-e8-r783-far.json.gz'
    original=ROOT/'vendor/source377/work/pr361/complex/gcert1-e8-r783.json.gz'
    execute(ROOT/'vendor/source384/code/cxcheck.py',[cert,ROOT/'vendor/source384/complex/gx'],'reference-checks')
    execute(ROOT/'vendor/source384/code/cxop.py',[original,cert],'all-rational-columns')
    native=out/'work/complex-nine-native';vendor=out/'work/native358/vendor/complex-reserve'
    execute(vendor/'admit.py',['--source',vendor/'upstream/pr352','--output',native/'local-admission'],'local-admission')
    guard=read(native/'local-admission/UPSTREAM-GUARD.json');admission=read(native/'local-admission/INDEPENDENT-AUDIT.json')
    assert guard['label_checks']['invocation_calls']==3973
    assert all(x['all_live_rows_correct'] and x['all_private_work_restored_zero'] for x in admission['scalar_words'].values())
    stages=['complex_candidate.py','verify_clifford_frames.py','data_phases.py','global_nine.py','audit_nine_template.py']
    for name in stages:execute(out/'work/odd-stages'/name,[],name)
    result=read(native/'GLOBAL-REVIEW.json');audit=read(native/'INDEPENDENT-TEMPLATE-AUDIT.json')
    old=read(baseline/'work/complex-nine-native/GLOBAL-REVIEW.json')
    assert audit['status']=='PASS_INDEPENDENT_EMITTED_TEMPLATE_AUDIT_AND_TWO_MOMENTS'
    assert audit['coarse_complex']=='999632926176283/1000000000000000000'
    for key in ('m','live','physical','invocations','rank_mass','deficit','whole_residual_assignments','bank_padding_calls','bridge_additions','terminal_shift_calls','terminal_complete_stream_movements','cover_correction_calls'):assert result[key]==old[key],key
    before={int(r):n for r,n in old['profile'].items()};after={int(r):n for r,n in result['profile'].items()}
    delta={r:after.get(r,0)-before.get(r,0) for r in before.keys()|after.keys() if after.get(r,0)!=before.get(r,0)}
    assert delta=={1:144,2:144,3:432,4:-1512,6:720}
    assert result['paid_calls']==old['paid_calls']-72
    assert read(native/'CLIFFORD-REVIEW.json')['all_child_equalities_include_global_phase']
    receipt=dict(status='PASS_FRESH_FAR_RETIMED_NINE_STAGE_COMPONENT',complex_coarse=audit['coarse_complex'],global_receipt_sha256=sha(native/'GLOBAL-REVIEW.json'),audit_sha256=sha(native/'INDEPENDENT-TEMPLATE-AUDIT.json'),derivation_sha256=sha(out/'DERIVATION.json'),all_rational_columns=1023,local_and_global_checks_fresh=True,stages=stages,profile_delta=delta)
    write(out/'VERIFICATION.json',receipt);return receipt

if __name__=='__main__':
    if sys.flags.optimize:raise SystemExit('Assertions must remain enabled')
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('baseline',type=Path);a=p.parse_args()
    print(json.dumps(run(a.output,a.baseline)),flush=True)
