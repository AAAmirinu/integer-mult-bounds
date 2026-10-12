"""Replay and compare every deterministic certificate in a clean output directory."""
from pathlib import Path
import argparse,hashlib,json,platform,subprocess,sys,time

P=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def pins():
    manifest=json.loads((P/'MANIFEST.json').read_text())
    actual={str(p.relative_to(P)) for p in P.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
    need(actual==set(manifest),'manifest file coverage')
    for name,value in manifest.items():need(sha(P/name)==value,'source hash '+name)
    return sha(P/'MANIFEST.json')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path);ap.add_argument('--check-pins',action='store_true');a=ap.parse_args()
    manifest_hash=pins()
    if a.check_pins:print(json.dumps(dict(status='PASS_PINS',manifest_sha256=manifest_hash)));return
    need(a.work is not None,'--work is required')
    work=a.work.resolve();work.mkdir(parents=True,exist_ok=True);need(not any(work.iterdir()),'output directory must be empty')
    stages=[];start=time.monotonic()
    for script,certificate in [('scan.py','GENERIC-CHECK.json'),('check.py','CHECK.json'),('check_budgets.py','BUDGETS.json'),('check_layout.py','LAYOUT-CHECK.json'),('weighted.py','WEIGHTED-CHECK.json'),('dirty.py','DIRTY-CHECK.json'),('dirty_controls.py','DIRTY-CONTROLS.json'),('dirty_kernels.py','DIRTY-KERNELS.json'),('dirty_budgets.py','DIRTY-BUDGETS.json')]:
        stage_start=time.monotonic();log=work/(script+'.log')
        with log.open('w') as output:
            result=subprocess.run([sys.executable,'-I','-O','-B',str(P/script),'--out',str(work/certificate)],cwd=work,stdout=output,stderr=subprocess.STDOUT)
        row=dict(script=script,certificate=certificate,exit_code=result.returncode,seconds=time.monotonic()-stage_start,log_sha256=sha(log))
        stages.append(row);(work/'STAGES.json').write_text(json.dumps(stages,indent=2)+'\n')
        need(result.returncode==0,'stage failed: '+script)
        need((work/certificate).read_bytes()==(P/certificate).read_bytes(),'certificate differs: '+certificate)
        print(json.dumps(dict(status='PASS_STAGE',**row)),flush=True)
    need(pins()==manifest_hash,'source changed during replay')
    receipt=dict(status='PASS_ALL_FRESH_CYCLIC_SCAN_CERTIFICATES',manifest_sha256=manifest_hash,
                 python=sys.version,platform=platform.platform(),seconds=time.monotonic()-start,stages=stages,
                 artifacts={name:sha(work/name) for name in ['GENERIC-CHECK.json','CHECK.json','BUDGETS.json','LAYOUT-CHECK.json','WEIGHTED-CHECK.json','DIRTY-CHECK.json','DIRTY-CONTROLS.json','DIRTY-KERNELS.json','DIRTY-BUDGETS.json','STAGES.json']},
                 coverage=dict(generic_cases=108,mixed_cases=480,mixed_dense_comparisons=240,budget_cases=345,stride_mappings=8384,stride_executions=43,weighted_generic_cases=36,weighted_kernel_cases=80,weighted_dense_comparisons=72,dirty_generic_cases=36,dirty_compositions=120,dirty_kernel_cases=24,dirty_budget_cases=1035),
                 scope='Finite and symbolic-budget evidence; no new kappa, physical tape benchmark, Pan implementation or complete multiplication theorem.')
    (work/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt),flush=True)
if __name__=='__main__':main()
