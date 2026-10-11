"""Generate/check the pending candidate record without promoting reviewed results."""
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import argparse,hashlib,json,sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
DESTINATION=REPO/'certificates/candidates/e8-coupled-bit-retiming.json'

def record():
    from verify import manifests
    manifests()
    expected=json.loads((ROOT/'data/EXPECTED.json').read_text(encoding='utf-8'))
    k=Q(expected['kappa']);old=Q(expected['prior_pr384'])
    assert k>old>Q(1,1024) and Q(expected['absolute_gain'])==k-old
    assert expected['retiming_kappa_gain']=='0'
    assert expected['baseline_composed_kappa']==expected['kappa']
    assert Q(expected['bit_coarse'])-Q(expected['baseline_bit_coarse'])==Q(expected['bit_component_gain'])>0
    with localcontext() as context:
        context.prec=70
        decimal=format(Decimal(k.numerator)/Decimal(k.denominator),'f')
    assert decimal in (REPO/'README.md').read_text(encoding='utf-8')
    return dict(format='conditional-candidate-record/1',date='2026-10-11',
        contributor='ai-nanachi',assistance='Substantial OpenAI Codex assistance',
        review_status='Pending maintainer review',
        scope='Finite conditional witness; upstream all-size compiler, recursive suppliers, compressed Clifford windows, banking, routing, restored-row, Gaussian recovery and analytic interfaces remain assumed. Not a formal proof of the complete theorem.',
        package='research/e8-coupled-bit-retiming',verification='make e8-coupled-verify',
        manifest_sha256=hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest(),
        source_pins_sha256=hashlib.sha256((ROOT/'SOURCE-PINS.json').read_bytes()).hexdigest(),
        upstream_main='12a4934d15006e8c10f9b2264f13f8f341be802b',
        kappa_decimal=decimal,**expected)

if __name__=='__main__':
    if sys.flags.optimize:raise SystemExit('Assertions must remain enabled')
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    result=record()
    if args.write:
        DESTINATION.parent.mkdir(parents=True,exist_ok=True)
        DESTINATION.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    else:assert json.loads(DESTINATION.read_text(encoding='utf-8'))==result,'Candidate record is stale'
    print('PASS pending candidate record',result['kappa'])
