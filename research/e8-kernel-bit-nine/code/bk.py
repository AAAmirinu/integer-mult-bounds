"""B_K pricing of an E8 bit word with our engines: (2K+1) x local histogram + 2v x B_K idle climbs (unsplit by default),
m = 8(2K+1), W = (2Kvh + resid) T / h with T the least replica count giving integral W and an exact width-m tiling."""
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e8core import *
from layout_bk import layout
import tile_m

def resid_census(c, L, masks):
    v = c['v']; n = 2 * v + c['R']
    return Counter(8 - L.dim(masks[c['start'][r]]) for r in range(2 * v, n))

def choose_T(res, m, h=8, Tmax=72):
    tot = sum(k * x for k, x in res.items())
    for T in range(1, Tmax + 1):
        if (T * tot) % h: continue
        try: tile_m.tile({r: T * k for r, k in res.items() if r > 0}, m); return T
        except AssertionError: pass
    return None

def price_bk(c, K=4, unsplit=True, T=None, r=None, fast=False):
    r = r or replay(c, span_mode='z'); h, v = 8, c['v']; s = 2 * K + 1; m = s * h
    res = resid_census(c, r['L'], r['masks']); resid = sum(k * x for k, x in res.items())
    if T is None: T = choose_T(res, m)
    lay = layout(K, h, split=None if unsplit else (m - 1) // 2)
    H = Counter({j: T * s * x for j, x in r['H'].items()})
    for b in lay['blocks']: H[b] += T * 2 * v
    W = (2 * K * v * h + resid) * T // h; assert (2 * K * v * h + resid) * T % h == 0
    dfc = m * W - sum(a * b for a, b in H.items())
    mx = max(H); t = 1
    while m ** t <= 2 * mx ** t: t += 1
    if fast:
        root = moment.certify(dict(H), m, W, True); cc = Q(root['lower'])
    else: cc = coarse(H, m, W)
    return dict(c=cc, H=H, W=W, m=m, T=T, maxchild=mx, t=t, deficit=dfc, res=res, local=r['H'], viol=r['viol'])

if __name__ == '__main__':
    c = load_word(sys.argv[1]); K = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    p = price_bk(c, K)
    print('K', K, 'T', p['T'], 'W', p['W'], 'm', p['m'], 'maxchild', p['maxchild'], 't', p['t'], 'deficit', p['deficit'], 'viol', len(p['viol']))
    print('c =', p['c'], float(p['c'])); print('residuals', dict(sorted(p['res'].items())))
