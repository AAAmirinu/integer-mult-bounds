"""Halving-degree guard (#375 form) for an E8 bit word in B_K at the bit parameters. usage: guard9.py WORD.json.gz K"""
import sys, os
from math import prod
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e8core import replay, load_word, Lat, to_masks
from layout_bk import layout
w = load_word(sys.argv[1]); K = int(sys.argv[2]); r = replay(w); h, v = 8, w['v']; s = 2 * K + 1; m = s * h; R = w['R']
resid = sum(h - r['sig'][x] for x in range(2 * v, 2 * v + R))
lay = layout(K, h); mx = max(list(r['H']) + lay['blocks']); t = 1
while m ** t <= 2 * mx ** t: t += 1
W = 2 * K * v + -(-resid // h); physical = W + R + h + 1
group = (1 << (m - 1 + (m // 2 - 1) ** 2)) * prod((1 << (2 * i)) - 1 for i in range(1, m // 2))
row = t * (group * W).bit_length() + 9909 + 252; rowp = t * (group * physical).bit_length() + 9909 + 252; gap = 2 * (m - mx) - 1
assert m <= 72 and row <= rowp < 20161 and gap >= 1
print('guard B_%d unsplit: m %d max child %d t %d stock bits %d/%d row %d/%d < 20161 gap %d B: PASS' % (K, m, mx, t, (group * W).bit_length(), (group * physical).bit_length(), row, rowp, gap))
