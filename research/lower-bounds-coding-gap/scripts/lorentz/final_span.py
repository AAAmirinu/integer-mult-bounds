"""final_span.py -- the last step of the non-existence proof, exactly over Q (sympy).
sigma-model (forced by Lemmas A, B + patsat): with s_x the basis (x in X, |X| = n-1), centre a:
  P_xy = s_x - s_y,  T_axy = s_x + s_y,  Q_v = g_{av} = sum_{u != v} s_u - s_v.
For U = triple {x,y,z} not containing a, Z(U) contains P_uw (u,w in Y = X - U), P_e (e in U),
T_auw (u in U, w in Y), Q_v (v in Y).  Their span must be a hyperplane; we print its rank (n-1 = full => contradiction).
Also checks every listed vector really is non-knowing to U (label rule)."""
import itertools, sympy as sp
from fam import setup
for n in (9, 11, 13):
    names, lab, vec, G, K, Z = setup(n)
    idx = {nm: i for i, nm in enumerate(names)}
    d = n - 1; a = n - 1; X = list(range(d)); E = sp.eye(d)
    U = (0, 1, 2); Y = [u for u in X if u not in U]
    vecs, members = [], []
    for u, w in itertools.combinations(Y, 2):
        vecs.append(E[:, u] - E[:, w]); members.append(('P', u, w))
    for u, w in itertools.combinations(U, 2):
        vecs.append(E[:, u] - E[:, w]); members.append(('P', u, w))
    for u in U:
        for w in Y:
            vecs.append(E[:, u] + E[:, w]); members.append(('T',) + tuple(sorted((a, u, w))))
    for v in Y:
        vecs.append(sp.Matrix([1] * d) - 2 * E[:, v]); members.append(('P', v, a))
    iU = idx[('T',) + U]
    assert all(Z[iU, idx[m]] for m in members), 'membership'
    M = sp.Matrix.hstack(*vecs)
    print('n=%d: rank of these %d members of Z(U) = %d (hyperplane needs <= %d); det-factor n-9 = %d' % (n, len(vecs), M.rank(), d - 1, n - 9))
