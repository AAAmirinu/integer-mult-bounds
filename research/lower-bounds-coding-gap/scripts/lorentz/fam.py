"""fam.py -- the I_{n,1} triples+pairs family (Sussman's tools/e8/e8.py ordering), knowing graph, cliques.

Vertices: C(n,3) triples then C(n,2) pairs (lexicographic, as e8.family()).  Labels: triple -> its 3-set,
pair {i,j} -> complement.  S knows T  <=>  S != T and |label_S & label_T| even.
Fitting-matrix rule (gx.py E5 + E1, derived in directions/G-lorentzian.md): B[S][S] = 1, B[S][T] = 0 if T != S and
S does not know T, free otherwise.  Z[S] = set of T != S that S does not know (the forced zeros)."""
import itertools
import numpy as np


def family(n):
    names, lab, vec = [], [], []
    full = (1 << n) - 1
    for T in itertools.combinations(range(n), 3):
        names.append(('T',) + T)
        lab.append(sum(1 << i for i in T))
        vec.append([1 if i in T else 0 for i in range(n)] + [1])
    for i, j in itertools.combinations(range(n), 2):
        names.append(('P', i, j))
        lab.append(full ^ (1 << i) ^ (1 << j))
        a = [0] * (n + 1)
        a[i], a[j] = 1, -1
        vec.append(a)
    return names, lab, vec


def lgram(vec):
    V = np.array(vec, dtype=np.int64)
    n = V.shape[1] - 1
    J = np.diag([1] * n + [-1])
    return V @ J @ V.T


def knows_matrix(lab):
    v = len(lab)
    K = np.zeros((v, v), dtype=bool)
    for a in range(v):
        for b in range(v):
            if a != b and bin(lab[a] & lab[b]).count('1') % 2 == 0:
                K[a, b] = True
    return K


def setup(n):
    names, lab, vec = family(n)
    G = lgram(vec)
    K = knows_matrix(lab)
    Z = ~K
    np.fill_diagonal(Z, False)
    return names, lab, vec, G, K, Z


def max_cliques_Z(Z, size):
    """all cliques of the forced-zero graph Z of the given size (Bron-Kerbosch with pivoting via networkx)"""
    import networkx as nx
    g = nx.Graph()
    v = Z.shape[0]
    g.add_nodes_from(range(v))
    g.add_edges_from((a, b) for a in range(v) for b in range(a + 1, v) if Z[a, b])
    return [c for c in nx.find_cliques(g) if len(c) >= size]
