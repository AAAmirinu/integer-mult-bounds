"""Exact coarse savings and PR #315's outer assembly for an E8 bit word in the seven-stage bridged word B_3, paired with
jacklightChen's PR #377 nine-stage E8 complex component.
Bit: (2K+1) x local histogram (our exact replay) + 2v x B_K idle climbs at h = 8 (our layout reimplementation), m = 8(2K+1),
W = 2Kv + sum (8 - sigma)/8 (x T = 8 when fractional), deficit 2Kv - (2K+1) x 72; split at (m-1)//2 (halving degree 1) or
unsplit (least t with m^t > 2 max^t). Complex: b re-certified by our engines from #377's own receipt profile (GLOBAL-REVIEW.json:
m = 73, live W = 14727, deficit 2496). Both rational engines, 1e-16 fallback, next grid point excluded; kappa by
outer.assembly (47 strict constraints, adjacent kappa rejected).
usage: kappa.py WORD.json.gz INPUT370.json.gz PR377_GLOBAL_REVIEW.json OUT.json"""
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e8core import coarse, kappa, price_word, load_word, Q
from layout_bk import layout


def bit_bk(word, K, split):
    p = price_word(word); h, v = 8, 120; s = 2 * K + 1; m = s * h; resid = p['resid']
    T = 1 if resid % h == 0 else h
    lay = layout(K, h, split=(m - 1) // 2 if split else None)
    H = Counter({r: T * s * c for r, c in p['H'].items()})
    for r in lay['blocks']: H[r] += T * 2 * v
    W = (2 * K * v * h + resid) * T // h; assert (2 * K * v * h + resid) * T % h == 0
    assert m * W - sum(r * c for r, c in H.items()) == T * (2 * K * v - s * 72), 'deficit'
    mx = max(H); t = 1
    while m ** t <= 2 * mx ** t: t += 1
    assert m <= 72
    return coarse(H, m, W), mx, t, m, lay['per_pair']


g = json.load(open(sys.argv[3])); Hc = {int(k): x for k, x in g['profile'].items()}; mc, Wc = g['m'], g['live']
assert mc * Wc - sum(r * n for r, n in Hc.items()) == g['deficit'] == 2496
b = coarse(Hc, mc, Wc); assert b == Q(999240641319551, 10**18), b
mx = max(Hc); t = 1
while mc ** t <= 2 * mx ** t: t += 1
print('   complex (#377 receipt, re-certified): m %d, W %d, deficit %d, max child %d, halving degree %d: b = %s = %.15e' % (mc, Wc, g['deficit'], mx, t, b, float(b)))
out = dict(b=str(b))
for name, path in (('pr370', sys.argv[2]), ('ours', sys.argv[1])):
    w = load_word(path)
    for split in (True, False):
        c, mxb, tb, m, idle = bit_bk(w, 3, split)
        k, bd = kappa(c, b)
        key = '%s_%s' % (name, 'split' if split else 'unsplit')
        print('   %-14s B_3 %s (m %d, max child %d, halving degree %d): c = %s = %.15e | kappa = %s = %.15e (%s-bound)'
              % (key, 'split at 27' if split else 'unsplit', m, mxb, tb, c, float(c), k, float(k), bd))
        out[key] = dict(c=str(c), kappa=str(k), kappa_float=float(k), binding=bd, halving_degree=tb)
assert out['pr370_split']['c'] == '968197503705007/1000000000000000000'   # = #373
json.dump(out, open(sys.argv[4], 'w'), indent=1)
