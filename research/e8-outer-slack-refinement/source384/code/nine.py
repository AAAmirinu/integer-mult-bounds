"""Exact coarse savings for jacklightChen's PR #377 nine-stage complex component with the local E8 certificate swapped,
our bit word (PR #382) in B_3 unsplit, and PR #315's outer assembly.
#377's paid profile (its complex_candidate.py / global_nine.py, read as data) is
    L*T * (sum over all local blocks x, y, s, c of the certificate's child histogram)    [L = 9 stages, T = 8 replicas]
  + 2*v*T * (idle ranks 2j(h-1), h-1 for j = 1..k-1, and 2(k-j)(h-1) for j = 1..k)       [k = 4 pairs]
  + L*R paid rank-1 bank paddings,
with m = 73, live W = 8*v*T + L*R = 14727. Only the pooled local histogram depends on the certificate.
usage: nine.py ORIG.json.gz OURS.json.gz PR377_GLOBAL_REVIEW.json BITWORD.json.gz OUT.json"""
import sys, os, json, gzip
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e8core import coarse, kappa, price_word, load_word, Q
from layout_bk import layout

k, L, T = 4, 9, 8


def nine_profile(c):
    h, v, R = c['h'], c['v'], c['R']; assert (h, v, R, c['cst']) == (9, 120, 783, 72)
    H = Counter()
    for block in c['blocks'].values():
        for r, n in block.items(): H[int(r)] += L * T * n
    idle = [x for j in range(1, k) for x in (2 * j * (h - 1), h - 1)] + [2 * (k - j) * (h - 1) for j in range(1, k + 1)]
    assert idle == [16, 8, 32, 8, 48, 8, 48, 32, 16, 0]
    for r in idle:
        if r: H[r] += 2 * v * T
    H[1] += L * R
    m, W = h + 8 * (L - 1), 8 * v * T + L * R; assert (m, W) == (73, 14727)
    assert m * W - sum(r * n for r, n in H.items()) == T * (2 * k * v - L * c['cst']) == 2496
    return H, m, W


def degree(H, m):
    mx = max(H); t = 1
    while m ** t <= 2 * mx ** t: t += 1
    return mx, t


def bit_bk_unsplit(word, K=3):
    p = price_word(word); h, v = 8, 120; s = 2 * K + 1; m = s * h; resid = p['resid']
    T8 = 1 if resid % h == 0 else h
    lay = layout(K, h)
    H = Counter({r: T8 * s * c for r, c in p['H'].items()})
    for r in lay['blocks']: H[r] += T8 * 2 * v
    W = (2 * K * v * h + resid) * T8 // h; assert (2 * K * v * h + resid) * T8 % h == 0
    assert m * W - sum(r * c for r, c in H.items()) == T8 * (2 * K * v - s * 72), 'deficit'
    mx, t = degree(H, m); assert m <= 72
    return coarse(H, m, W), mx, t, m


load = lambda p: json.load(gzip.open(p))
orig, ours, g = load(sys.argv[1]), load(sys.argv[2]), json.load(open(sys.argv[3]))
H0, m, W = nine_profile(orig)
assert {str(r): n for r, n in sorted(H0.items())} == g['profile'] and (g['m'], g['live'], g['deficit']) == (m, W, 2496)
print('   #377 profile rebuilt from Sussman\'s certificate equals GLOBAL-REVIEW.json field for field (m %d, W %d, deficit 2496)' % (m, W))
H1, _, _ = nine_profile(ours)
d = {r: H1.get(r, 0) - H0.get(r, 0) for r in sorted(set(H0) | set(H1)) if H1.get(r, 0) != H0.get(r, 0)}
print('   profile with the re-timed certificate:', dict(sorted(H1.items())))
print('   profile delta (= 72 x pooled local delta):', d)
assert all(x % 72 == 0 for x in d.values()) and sum(r * x for r, x in d.items()) == 0
mx0, t0 = degree(H0, m); mx1, t1 = degree(H1, m); assert (mx0, t0) == (mx1, t1) == (48, 2)
b0 = coarse(H0, m, W); assert b0 == Q(999240641319551, 10**18), b0
b1 = coarse(H1, m, W)
print('   b (#377, Sussman\'s unit)      = %s = %.15e  [= #377]' % (b0, float(b0)))
print('   b (#377 with our re-timed unit) = %s = %.15e  (+%.6e)' % (b1, float(b1), float(b1 - b0)))
assert b1 > b0
word = load_word(sys.argv[4]); c, mxb, tb, mb = bit_bk_unsplit(word)
assert c == Q(251726760077483, 25 * 10**16) and (mxb, tb, mb) == (34, 2, 56), (c, mxb, tb)
print('   bit c (PR #382 word, B_3 unsplit, m %d, max child %d, halving degree %d) = %s = %.15e' % (mb, mxb, tb, c, float(c)))
k0, bd0 = kappa(c, b0); k1, bd1 = kappa(c, b1)
assert k0 == Q(998243154231047, 10**18) and bd0 == 'complex'
print('   kappa with #377 as shipped = %s = %.15e (%s-bound)  [= PR #382]' % (k0, float(k0), bd0))
print('   kappa with the re-timed unit = %s = %.15e (%s-bound)' % (k1, float(k1), bd1))
json.dump(dict(b_377=str(b0), b=str(b1), b_float=float(b1), c=str(c), kappa_382=str(k0), kappa=str(k1), kappa_float=float(k1), binding=bd1,
               profile={str(r): n for r, n in sorted(H1.items())}, profile_delta={str(r): x for r, x in d.items()}, max_child=mx1, halving_degree=t1),
          open(sys.argv[5], 'w'), indent=1)
