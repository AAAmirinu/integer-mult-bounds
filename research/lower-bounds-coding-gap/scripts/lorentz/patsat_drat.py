"""patsat_drat.py -- the SAT step of note 3 (Lemma B), with a checkable DRUP/DRAT proof.

Same encoding as patsat.py (points X = {0..N-1}, N = n-1; for each pair e the points T_e, P_e are of
type 0 (= s_u), 1 (= s_w) or 2 (generic); z[x][u] = "coordinate u of Q_x is nonzero").

Claim checked here: every model has all T_e, P_e generic.  The script
  (1) writes the base CNF and checks that it is SATISFIABLE (calibration: the all-generic pattern exists);
  (2) adds one clause "some T_e or P_e is a basis point" and checks UNSAT with Glucose 4 proof logging,
      writing <out>/patsat-N.cnf and <out>/patsat-N.drat for an external checker (drat-trim).
Usage: python patsat_drat.py N OUTDIR
"""
import sys, itertools, os
from pysat.solvers import Glucose4

N = int(sys.argv[1]); out = sys.argv[2]
X = range(N)
cnt = [0]
def new():
    cnt[0] += 1; return cnt[0]
pairs = list(itertools.combinations(X, 2))
T = {e: [new() for _ in range(3)] for e in pairs}
P = {e: [new() for _ in range(3)] for e in pairs}
z = {(x, u): new() for x in X for u in X}
cl = []
for e in pairs:
    for V in (T[e], P[e]):
        cl.append(V[:])
        for a, b in itertools.combinations(V, 2):
            cl.append([-a, -b])
    cl.append([-T[e][0], -P[e][0]]); cl.append([-T[e][1], -P[e][1]])
def rel(V, zu, zw):
    cl.append([-V[2], -zu, zw]); cl.append([-V[2], zu, -zw])
    cl.append([-V[0], -zw]); cl.append([-V[1], -zu])
for x in X:
    cl.append([z[x, u] for u in X])
    for (u, w) in pairs:
        rel(T[u, w] if x not in (u, w) else P[u, w], z[x, u], z[x, w])

with Glucose4(bootstrap_with=cl) as s:
    sat = s.solve()
    m = set(l for l in s.get_model() if l > 0) if sat else set()
generic = sat and all(V[2] in m for e in pairs for V in (T[e], P[e]))
print('N=%d base formula: %s (model all-generic: %s)' % (N, 'SAT' if sat else 'UNSAT', generic))
assert sat and generic

degenerate = [V[i] for e in pairs for V in (T[e], P[e]) for i in (0, 1)]
cl2 = cl + [degenerate]
os.makedirs(out, exist_ok=True)
cnf = os.path.join(out, 'patsat-%d.cnf' % N); drat = os.path.join(out, 'patsat-%d.drat' % N)
with open(cnf, 'w') as f:
    f.write('p cnf %d %d\n' % (cnt[0], len(cl2)))
    for c in cl2:
        f.write(' '.join(map(str, c)) + ' 0\n')
with Glucose4(bootstrap_with=cl2, with_proof=True) as s:
    res = s.solve()
    proof = s.get_proof()
print('N=%d with "some point degenerate": %s; proof lines %d -> %s' % (N, 'SAT' if res else 'UNSAT', len(proof), drat))
assert res is False
with open(drat, 'w') as f:
    f.write('\n'.join(proof) + '\n')
