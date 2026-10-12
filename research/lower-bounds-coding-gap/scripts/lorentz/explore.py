import sys, numpy as np
from collections import Counter
from fam import setup, max_cliques_Z
n = int(sys.argv[1])
names, lab, vec, G, K, Z = setup(n)
v = len(lab)
# sanity: G==0 off-diagonal <=> Z
off = ~np.eye(v, dtype=bool)
print('n=%d v=%d  Z == (G==0) off diag: %s ; G diag %s ; rank_Q G = %d' % (n, v, np.array_equal(Z, (G == 0) & off), set(np.diag(G)), np.linalg.matrix_rank(G)))
print('knowing degree', Counter(K.sum(1)))
cl = max_cliques_Z(Z, 1)
sz = Counter(len(c) for c in cl)
print('maximal Z-cliques by size', sorted(sz.items()))
mx = max(sz)
C = [c for c in cl if len(c) == mx]
print('max clique size', mx, 'count', len(C))
# min |N(U) cap C| over max cliques
mins = Counter()
for U in range(v):
    m = min(int(K[U, c].sum()) for c in C if U not in c) if any(U not in c for c in C) else None
    mins[m] += 1
print('distribution over U of min_C |knowing(U) cap C|:', sorted(mins.items()))
