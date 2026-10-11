"""Generate/check the exact pending extension record without promoting selection."""
import argparse,hashlib,json,pathlib,sys
from fractions import Fraction as Q
from decimal import Decimal,localcontext
ROOT=pathlib.Path(__file__).resolve().parent;REPO=ROOT.parents[1]
DESTINATION=REPO/'certificates/candidates/e8-clean-reuse-extension.json'
def record():
    from verify import manifests
    manifests();expected=json.loads((ROOT/'data/EXPECTED.json').read_text(encoding='utf-8'))
    k=Q(expected['kappa']);old=Q(expected['prior_pr389']);assert k>old and Q(expected['absolute_gain'])==k-old
    assert Q(expected['bit_reuse_kappa_gain'])>0 and expected['conditional']
    assert Q(expected['fair_old_bit_kappa'])+Q(expected['bit_reuse_kappa_gain'])==k
    assert Q(expected['bit_coarse'])>Q(expected['complex_coarse'])
    with localcontext()as ctx:ctx.prec=70;decimal=format(Decimal(k.numerator)/Decimal(k.denominator),'f')
    assert decimal in(REPO/'README.md').read_text(encoding='utf-8')
    return dict(format='conditional-candidate-record/1',date='2026-10-11',contributor='ai-nanachi',assistance='Substantial OpenAI Codex assistance',review_status='Pending maintainer review',scope='Finite conditional witness. Full theorem, all-size compiler, recursive supplier, compressed Clifford windows, dirty banking/cover, restored-row, routing, fixed tape, precision/recovery and analytic interfaces remain assumed.',package='research/e8-clean-reuse-extension',verification='make e8-clean-reuse-verify',manifest_sha256=hashlib.sha256((ROOT/'MANIFEST.json').read_bytes()).hexdigest(),source_pins_sha256=hashlib.sha256((ROOT/'SOURCE-PINS.json').read_bytes()).hexdigest(),upstream_main='12a4934d15006e8c10f9b2264f13f8f341be802b',prior_pr389_commit='b3c45822ca847aec8c0c019bb04db30881fc2966',kappa_decimal=decimal,**expected)
if __name__=='__main__':
    if sys.flags.optimize:raise SystemExit('Assertions must remain enabled')
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();result=record()
    if a.write:DESTINATION.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
    else:assert json.loads(DESTINATION.read_text(encoding='utf-8'))==result,'Pending extension record is stale'
    print('PASS pending extension record',result['kappa'])
