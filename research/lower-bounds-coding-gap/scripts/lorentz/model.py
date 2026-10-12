"""model.py -- assume the a-centred P,T subsystem is P_xy = s_x - s_y, T_axy = s_x + s_y (s = basis of Q^10,
the Lorentz shape written in the 'sigma basis').  Force Q_x and S_xyz by the clique rule (F2) over centre-a
cliques, then test every condition of the fitting-matrix rule exactly over Q."""
import itertools, sys
import sympy as sp
from fam import setup

n = int(sys.argv[1]) if len(sys.argv) > 1 else 11
names, lab, vec, G, K, Z = setup(n)
v = len(names)
a = n - 1
X = list(range(n - 1))
d = n - 1
idx = {nm: i for i, nm in enumerate(names)}
def tri(*s): return idx[('T',) + tuple(sorted(s))]
def pair(x, y): return idx[('P',) + tuple(sorted((x, y)))]
E = sp.eye(d)
g = {}
for x, y in itertools.combinations(X, 2):
    g[pair(x, y)] = E[:, x] - E[:, y]
    g[tri(a, x, y)] = E[:, x] + E[:, y]


def matchings(s):
    if not s:
        yield []
        return
    x = s[0]
    for i in range(1, len(s)):
        for m in matchings(s[1:i] + s[i + 1:]):
            yield [(x, s[i])] + m


def clique(M):
    return [pair(*e) for e in M] + [tri(a, *e) for e in M]


def intersect(spaces):
    W = spaces[0]
    for S in spaces[1:]:
        ns = W.row_join(-S).nullspace()
        if not ns:
            return sp.zeros(d, 0)
        W = sp.Matrix.hstack(*[W * v_[:W.shape[1], :] for v_ in ns])
        cs = W.columnspace()
        W = sp.Matrix.hstack(*cs) if cs else sp.zeros(d, 0)
        if W.shape[1] == 0:
            return W
    return W

Ms = list(matchings(X))
print('n=%d, %d centre-a matchings' % (n, len(Ms)))
import random
random.seed(1)
sample = random.sample(Ms, min(len(Ms), 60))
for U in range(v):
    if U in g:
        continue
    spaces = []
    for M in sample:
        C = clique(M)
        if U in C:
            continue
        S = [g[T] for T in C if K[U, T]]
        spaces.append(sp.Matrix.hstack(*S))
    W = intersect(spaces)
    if W.shape[1] != 1:
        print('vertex', names[U], 'feasible dim', W.shape[1])
        if W.shape[1] == 0:
            print('CONTRADICTION: no place for', names[U]); sys.exit()
        continue
    w = W[:, 0]
    w = w / [c for c in w if c != 0][0]
    g[U] = w
print('forced:', len(g), 'of', v)
for U in sorted(g)[:0]:
    pass
ex = [names[U] for U in g if names[U][0] == 'P' and a in names[U][1:]][:2]
for nm in ex: print(nm, list(g[idx[nm]]))
ex = [nm for nm in names if nm[0] == 'T' and a not in nm[1:]][:2]
for nm in ex: print(nm, list(g[idx[nm]]))
# full check: span Z(U) must be a hyperplane not containing g_U
bad = 0
for U in range(v):
    M = sp.Matrix.hstack(*[g[V] for V in range(v) if Z[U, V]])
    rk = M.rank()
    rk2 = M.row_join(g[U]).rank()
    if not (rk == d - 1 and rk2 == d):
        bad += 1
        if bad <= 5:
            print('violation at', names[U], 'rank Z =', rk, 'with g_U', rk2)
print('violations:', bad)
