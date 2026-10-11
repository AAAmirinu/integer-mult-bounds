"""Halving-degree guard for the bit side in B_3, in the form of DaysSky's #375 generalised finite-bridge guard
(t = least integer with m^t > 2 max_child^t; row coefficient t * bitlength(stock) + 9909 + 252 <= 20161 for the live and
the physical stock, stock = group * W with group = 2^(m-1+(m/2-1)^2) prod_{i<m/2} (2^(2i)-1), physical = W + R + h + 1;
cover bound m <= 72; completed-child induction gap 2(m - max_child) - 1 >= 1). Evaluated here at the bit parameters.
usage: guard.py WORD.json.gz"""
import sys, os
from math import prod
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e8core import price_word, load_word
from layout_bk import layout
w = load_word(sys.argv[1]); p = price_word(w); h, v, K = 8, 120, 3; s = 2 * K + 1; m = s * h; R = w['R']
for split in (True, False):
    lay = layout(K, h, split=(m - 1) // 2 if split else None)
    mx = max(list(p['H']) + lay['blocks'])
    t = 1
    while m ** t <= 2 * mx ** t: t += 1
    W = 2 * K * v + -(-p['resid'] // h)          # live stock per vertex, rounded up
    physical = W + R + h + 1
    group = (1 << (m - 1 + (m // 2 - 1) ** 2)) * prod((1 << (2 * i)) - 1 for i in range(1, m // 2))
    row = t * (group * W).bit_length() + 9909 + 252; rowp = t * (group * physical).bit_length() + 9909 + 252
    gap = 2 * (m - mx) - 1
    assert m <= 72 and row <= rowp < 20161 and gap >= 1
    print('   bit B_3 %-7s m %d, max child %d, least halving degree t = %d (%d^%d = %d > 2*%d^%d = %d), live/physical stock bits %d/%d, row coefficient %d / %d < 20161, induction gap %d B, m <= 72: PASS'
          % ('split' if split else 'unsplit', m, mx, t, m, t, m ** t, mx, t, 2 * mx ** t, (group * W).bit_length(), (group * physical).bit_length(), row, rowp, gap))
