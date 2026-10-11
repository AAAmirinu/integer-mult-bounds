"""Retiming descent scored for B_K (m = 72): usage rt9.py IN OUT [sweeps] [seed] [K]"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code'))
from retime import Model, sweep
from bk import *
c = load_word(sys.argv[1]); sweeps = int(sys.argv[3]) if len(sys.argv) > 3 else 30
rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 1); K = int(sys.argv[5]) if len(sys.argv) > 5 else 4
m = 8 * (2 * K + 1)
p0 = price_bk(c, K, fast=True); a = float(p0['c']); print('start c %.9e' % a, flush=True)
M = Model(c)
for s in range(sweeps):
    mv, g = sweep(M, a, rng, m=m)
    print('sweep', s, 'moved', mv, 'phi gain %.4f' % g, flush=True)
    if mv == 0: break
w = M.to_word(); p = price_bk(w, K)
assert not p['viol']
print('end c', p['c'], '%.9e' % float(p['c']), 'delta %.4e' % float(p['c'] - p0['c']), 'T', p['T'])
save_word(w, sys.argv[2])
