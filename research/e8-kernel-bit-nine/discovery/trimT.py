"""Trim a kernel selection so the residual census tiles width-72 banks with T replicas (T in 1, 3, 9): drop the entries of
least ledger value (pivot gain minus donor costs freed) by exact DP on rank, then exact re-price.
usage: trimT.py PRE.json.gz SEL.json OUTPREFIX"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code'))
from ils import setup, chi_total
from bk import *
from kernel import apply
c = load_word(sys.argv[1]); sel = [tuple(x) for x in json.load(open(sys.argv[2]))]; pre = sys.argv[3]
a = float(price_bk(c, 4, fast=True)['c']); ctx = setup(c, a); d = ctx['d']
R8 = 8 * c['R']; rank = sum(d(E) for E, p, D in sel); base = chi_total(ctx, sel)
loss = []
for i in range(len(sel)):
    loss.append(base - chi_total(ctx, sel[:i] + sel[i + 1:]))
res = []
for T, mod in ((1, 72), (3, 24), (9, 8)):
    need = (rank - R8) % mod   # rank to drop (mod mod) so that resid total = 0 mod mod
    for target in (need, need + mod, need + 2 * mod):
        best = {0: (0.0, ())}
        for i, (E, p, D) in enumerate(sel):
            e = d(E); nb = dict(best)
            for r, (l, ix) in best.items():
                if r + e <= target and (r + e not in nb or nb[r + e][0] > l + loss[i]): nb[r + e] = (l + loss[i], ix + (i,))
            best = nb
        if target not in best: print("unreachable", T, target); continue
        l, ix = best[target]; keep = [s for i, s in enumerate(sel) if i not in set(ix)]
        w = apply(c, keep, ctx['M'].L)
        try: p = price_bk(w, 4, T=T)
        except AssertionError as ex: print("price fail", T, target, repr(ex)[:200]); continue
        rs = resid_census(w, Lat(w['lines']), to_masks(w, Lat(w['lines'])))
        try: tile_m.tile({r: T * k for r, k in rs.items() if r > 0}, 72); ok = True
        except AssertionError: ok = False
        print('T', T, 'drop rank', target, 'entries', len(ix), 'chi loss %.6f' % l, 'tiles', ok, 'c %.12e' % float(p['c']), flush=True)
        if ok:
            res.append((p['c'], T, keep)); break
cbest, T, keep = max(res, key=lambda x: (x[0], -x[1]))
for cc, TT, kk in res: json.dump([[E, p, D] for E, p, D in kk], open('%s-T%d.json' % (pre, TT), 'w'))
print('best T', T, 'c', cbest, float(cbest))
