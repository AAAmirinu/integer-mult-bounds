"""Verify a fresh full replay and retain its complete certificate/log evidence."""
from pathlib import Path
import argparse,hashlib,json,shutil
P=Path(__file__).resolve().parent;S=P.parent/'prime-power-cyclic-scan'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
ap=argparse.ArgumentParser();ap.add_argument('--work',required=True,type=Path);ap.add_argument('--platform',required=True);a=ap.parse_args()
W=a.work.resolve();R=read(W/'RECEIPT.json');T=read(W/'STAGES.json')
need(R['status']=='PASS_ALL_FRESH_CYCLIC_SCAN_CERTIFICATES','receipt status')
need(R['manifest_sha256']==sha(S/'MANIFEST.json'),'package pin')
need(T==R['stages'] and len(T)==9 and all(x['exit_code']==0 for x in T),'full fresh successful stages')
for name,value in R['artifacts'].items():need(sha(W/name)==value,'artifact hash '+name)
for row in T:
    need(sha(W/(row['script']+'.log'))==row['log_sha256'],'stage log hash')
    need((W/row['certificate']).read_bytes()==(S/row['certificate']).read_bytes(),'deterministic certificate')
G=read(W/'GENERIC-CHECK.json');M=read(W/'CHECK.json');B=read(W/'BUDGETS.json');L=read(W/'LAYOUT-CHECK.json')
WGT=read(W/'WEIGHTED-CHECK.json')
D=read(W/'DIRTY-CHECK.json');DC=read(W/'DIRTY-CONTROLS.json');DK=read(W/'DIRTY-KERNELS.json');DB=read(W/'DIRTY-BUDGETS.json')
coverage=dict(generic_cases=len(G['cases']),mixed_cases=len(M['cases']),mixed_dense_comparisons=sum(x['dense_comparison'] for x in M['cases']),budget_cases=len(B['records']),stride_mappings=L['mapping_cases'],stride_executions=len(L['execution_cases']),weighted_generic_cases=len(WGT['generic']),weighted_kernel_cases=len(WGT['cases']),weighted_dense_comparisons=sum(x['dense'] for x in WGT['generic']+WGT['cases']),dirty_generic_cases=len(D['generic']),dirty_compositions=len(D['cases']),dirty_kernel_cases=len(DK['cases']),dirty_budget_cases=len(DB['records']))
need(coverage==R['coverage'],'actual certificate coverage')
controls=sum(len(x['controls']) for x in (G,M,B,L,WGT,D,DC,DB));need(controls==48,'negative controls')
dest=P/a.platform;need(not dest.exists(),'destination exists');dest.mkdir(parents=True)
files=sorted(set(['RECEIPT.json',*R['artifacts'],*[x['script']+'.log' for x in T]]))
for name in files:shutil.copy2(W/name,dest/name)
out=dict(status='PASS_VERIFIED_FULL_PLATFORM',manifest_sha256=R['manifest_sha256'],receipt_sha256=sha(W/'RECEIPT.json'),seconds=R['seconds'],python=R['python'],platform=R['platform'],coverage=coverage,rejected_controls=controls,retained_files={name:sha(dest/name) for name in files})
(dest/'VERIFIED.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
