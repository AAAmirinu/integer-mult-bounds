"""Our far-piece-relocation search (cxfar.py: far relocation, single/block retiming, in-group piece relocation), with the
chi ledger and the price taken in #377's nine-stage setting (m = 73, pooled profile of nine.py) instead of B_3 at m = 63.
usage: far9.py CERT.json.gz GXDIR OUT.json.gz [passes]"""
import sys, os, json, gzip, random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cxfar import far_pass, piece_pass, split, CX, rehist, to_cert, bsweep
from cxsplit import single_sweep
from e8core import coarse


def price9(c):
    H = Counter()
    for bl in c['blocks'].values():
        for r, n in bl.items(): H[int(r)] += 72 * n
    for r in (16, 8, 32, 8, 48, 8, 48, 32, 16): H[r] += 1920
    H[1] += 7047; return coarse(H, 73, 14727)


if __name__ == '__main__':
    sys.path.insert(0, sys.argv[2]); import gx
    src = json.load(gzip.open(sys.argv[1]))
    c, tag = (src['cert'], [tuple(t) for t in src['tag']]) if 'cert' in src else split(src)
    m = 73; b0 = price9(c); a = float(b0); rng = random.Random(1); print('start b9', b0, float(b0), flush=True)
    for p in range(int(sys.argv[4]) if len(sys.argv) > 4 else 120):
        c, tag, g = far_pass(c, tag, a, m); M = CX(c)
        for s in range(10):
            m1, _ = single_sweep(M, a, m, rng); m2, _ = bsweep(M, a, m, rng)
            if not (m1 or m2): break
        c = rehist(to_cert(M)); c, tag, g2 = piece_pass(c, tag, a, m)
        b = price9(c); print('pass', p, 'far/a %.3f piece/a %.3f' % (g / a, g2 / a), 'b9', b, '%.15e' % float(b), flush=True)
        if g == 0 and g2 == 0: break
    gx.check1(c, scalar=True); print('gx.check1 PASS')
    json.dump(dict(cert=c, tag=[list(t) for t in tag]), gzip.open(sys.argv[3], 'wt'))
