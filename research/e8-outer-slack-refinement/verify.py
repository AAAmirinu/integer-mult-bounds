#!/usr/bin/env python3
"""Full pinned PR384 replay, followed by the exact changed assembly witness."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,hashlib,json,os,subprocess,sys
sys.dont_write_bytecode=True
sys.set_int_max_str_digits(0)
ROOT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def integrity():
    manifest=read(ROOT/'MANIFEST.json')
    assert {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}==set(manifest)|{'MANIFEST.json'}
    for name,h in manifest.items():assert sha(ROOT/name)==h,name
    assert sha(ROOT/'source384/MANIFEST.sha256')==read(ROOT/'SOURCE.json')['manifest_sha256']
def main():
    assert __debug__,'Assertions must stay enabled'
    ap=argparse.ArgumentParser();ap.add_argument('output',type=Path);args=ap.parse_args();out=args.output.resolve()
    assert not out.exists() and out!=ROOT and ROOT not in out.parents
    integrity();out.mkdir(parents=True);(out/'tmp').mkdir()
    script=(ROOT/'source384/verify.sh').read_text();old='HERE=$(cd "$(dirname "$0")" && pwd)';oldpy='PY="${PYTHON:-python3} -I -B"'
    assert script.count(old)==1 and script.count(oldpy)==1
    script=script.replace(old,'HERE=$SOURCE384').replace('set -euo pipefail',"set -euo pipefail\nIFS=$'\\n\\t'")
    script=script.replace(oldpy,'PY=py; py() { "$VERIFY_PYTHON" -I -B "$@"; }')
    (out/'baseline.sh').write_text(script)
    env=dict(os.environ,SOURCE384=str(ROOT/'source384'),VERIFY_PYTHON=sys.executable,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(out/'tmp'))
    print('RUN full PR384 replay and regeneration',flush=True)
    with (out/'baseline.log').open('w') as f:subprocess.run(['bash',str(out/'baseline.sh'),str(out/'baseline')],cwd=out,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    baseline=read(out/'baseline/kappa.json');source=read(ROOT/'SOURCE.json')
    assert baseline['kappa']==source['kappa'] and baseline['binding']=='complex'
    from refine import refine
    from coarse_precision import certify
    precision=certify(baseline['profile'],73,14727,Q(baseline['b']))
    assert precision==read(ROOT/'EXPECTED-COARSE-PRECISION.json')
    (out/'COARSE-PRECISION.json').write_text(json.dumps(precision,indent=2)+'\n')
    witness=refine(Q(precision['coarse_lower']),Q(baseline['c']))
    upper=Q(precision['coarse_upper'])
    assert upper/(1+upper)<Q(witness['kappa'])+Q(1,10**18)
    assert witness==read(ROOT/'EXPECTED-WITNESS.json')
    k=Q(witness['kappa']);before=Q(baseline['kappa']);assert k>before
    (out/'WITNESS.json').write_text(json.dumps(witness,indent=2,default=str)+'\n')
    integrity();result=dict(status='PASS_EXACT_OUTER_SLACK_REFINEMENT',kappa=str(k),kappa_float=float(k),baseline_kappa=str(before),absolute_gain=str(k-before),relative_gain_percent=float(100*(k/before-1)),strict_constraints=47,negative_controls=len(witness['negative_controls_rejected']),next_grid_above_fixed_complex_outer_ceiling=True,bootstrap_rounds=witness['bootstrap_rounds'],gain_over_previous_three_round=str(k-Q(witness['previous_three_round_kappa'])),gain_over_previous_six_round=str(k-Q(witness['previous_six_round_kappa'])),coarse_constructions_unchanged=True,coarse_precision_digits=24,two_moment_engines=True,next_grid_above_unrounded_moment_ceiling=True,scope='Same conditional supplier assumptions and open obligations as PR384. Fixed six-level PR185 ordinary bootstrap, strict witness parameters and 24-place coarse moment enclosure; inherited completed-leaf/restored-row/analytic interfaces remain conditional. No coarse circuit change or Lean proof.')
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
