import sys, pickle, numpy as np
from collections import Counter
from fam import setup, max_cliques_Z
n = int(sys.argv[1])
names, lab, vec, G, K, Z = setup(n)
v = len(lab)
cl = [sorted(c) for c in max_cliques_Z(Z, n - 1)]
print('n', n, '#max cliques', len(cl))
pickle.dump(cl, open('cliques%d.pkl' % n, 'wb'))
# swaps: C - T + T'
cnt = Counter()
for C in cl[:200]:
    Cs = set(C)
    for T in C:
        rest = [x for x in C if x != T]
        cand = [u for u in range(v) if u not in Cs and Z[u, rest].all()]
        cnt[len(cand)] += 1
print('number of T\' replacing one element (sample)', sorted(cnt.items()))
C = cl[0]
print('clique 0:', [names[c] for c in C])
print('|K(U) cap C0| distribution', sorted(Counter(int(K[u, C].sum()) for u in range(v) if u not in C).items()))
