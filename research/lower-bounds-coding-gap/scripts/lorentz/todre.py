import sys
from fam import setup
n = int(sys.argv[1])
names, lab, vec, G, K, Z = setup(n)
v = len(lab)
out = ['n=%d g' % v]
for a in range(v):
    out.append(' '.join(str(b) for b in range(a + 1, v) if K[a, b]) + ';')
out.append('x')
open('k%d.dre' % n, 'w').write('\n'.join(out) + '\n')
