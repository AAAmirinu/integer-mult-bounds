"""Exact bit coarse savings in DaysSky's nine-stage bridged word B_4 (unsplit idle climbs, halving degree two, #381's layout)
and the outer assembly with cited complex savings.
Bit: 9 x local histogram (our exact replay) + 2v x B_4 idle climbs [50] | [14,7,36] | [28,7,22] | [42,7,8] (our layout
reimplementation), m = 72, W = (8vh + resid) T / h; both PR #315 engines, 1e-16 fallback, next grid point excluded (e8core.coarse).
Controls: PR #370's word (= #381's bit) and PR #376's R822 word (= #390/#401/#404/#409/#410's bit) are priced by the same code.
kappa: our reimplementation (bootstrap.refine) of #392's refined pricing tail, as used by #395/#407/#409/#410: complex-bound
whenever c > (1 - beta) b.
usage: kappa.py FINAL.json.gz WORD370.json.gz WORD376.json.gz COMPLEX_B.json OUT.json"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bk import price_bk
from e8core import load_word, Q
from bootstrap import refine
fin, w370, w376, cb, outp = sys.argv[1:6]
want = {'pr381_bit_pr370_word': '249162322049641/250000000000000000', 'pr390_bit_pr376_word': '255384852701747/250000000000000000'}
out = dict(bit={}, kappa={})
for name, path in (('pr381_bit_pr370_word', w370), ('pr390_bit_pr376_word', w376), ('ours', fin)):
    w = load_word(path)
    for unsplit in (True, False):
        p = price_bk(w, 4, unsplit=unsplit)
        key = name + ('' if unsplit else '_split')
        out['bit'][key] = dict(c=str(p['c']), c_float=float(p['c']), m=p['m'], W=p['W'], T=p['T'], max_child=p['maxchild'], halving_degree=p['t'], deficit=p['deficit'])
        print('   %-26s B_4 %-7s (m %d, T %d, W %d, max child %d, halving degree %d, deficit %d): c = %s = %.15e'
              % (name, 'unsplit' if unsplit else 'split', p['m'], p['T'], p['W'], p['maxchild'], p['t'], p['deficit'], p['c'], float(p['c'])))
for k, v in want.items(): assert out['bit'][k]['c'] == v, (k, out['bit'][k]['c'])
c = Q(out['bit']['ours']['c']); c0 = Q(want['pr390_bit_pr376_word'])
print('   controls: #381 (9.96649e-4) and #390 (1.021539e-3) bit savings reproduced exactly; ours is %+.4f%% over #390\'s bit' % (100 * float(c / c0 - 1)))
for s in json.load(open(cb))['suppliers']:
    b = Q(s['b']); k, rej = refine(b, c); k0, _ = refine(b, c0)
    assert c > b and k == k0
    out['kappa'][s['name']] = dict(b=str(b), kappa=str(k), kappa_float=float(k), binding='complex', rejected=rej)
    print('   with %s b = %.12e: kappa = %s = %.15e (complex-bound; identical with #390\'s bit; bit headroom c/b - 1 = %.3f%%)'
          % (s['name'], float(b), k, float(k), 100 * float(c / b - 1)))
json.dump(out, open(outp, 'w'), indent=1)
