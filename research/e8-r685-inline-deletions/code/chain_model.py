"""Exact register-chain model (min path cover with host links) for the read events of a bit hierarchy, solved as a 0/1 ILP with HiGHS (scipy.optimize.milp).

Read events of a symbol u (rule reads, low deliveries, high deliveries) are ordered by PR #370's compile2 key (phase, dim, kind, id).  Two events can be
served by ONE register iff the earlier precedes the later in that key order and their frames are equal or nested (a high delivery ends the register's
life).  A register's life is a path: consecutive events are linked either on the SAME symbol (chain continuation) or by a HOST link (the register is
consumed by rule w and then carries w).  Constraints: at most one successor and one predecessor per event, at most one host link into each rule, and
every source keeps one register that never hosts (x_s must survive).  The objective (number of links) minimises the helper registers of the fixed
DAG; compile2 itself assigns chains greedily (Dilworth per symbol), the ILP chains are optimal and are handed to compile2 through
`chains_override`.

Derived from the project's path-cover scout (`pcm2.py`, DreamingOfClouds with Claude, via Claude Code); the ILP is unchanged.  Apache-2.0.
"""
import numpy as np
from collections import defaultdict
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix

class ChainModel:
    def __init__(self, h, lowset, phase, Fm, V=120):
        """h: hierarchy object (kids, dim, frame, need, content); lowset: PR #370's low-read set {(t,u)}; phase: {rule: 'A'|'B'}; Fm: PR #370 frames module"""
        self.h, self.low, self.ph, self.Fm, self.V = h, lowset, phase, Fm, V
        self.dl = defaultdict(list)
        for t in range(V):
            for u in h.need[t]: self.dl[u].append((t, (t, u) in lowset))
    def events(self, kids):
        h, V, Fm = self.h, self.V, self.Fm
        EV = []; byu = defaultdict(list); cons = defaultdict(list)
        for w, ks in kids.items():
            for c in ks: cons[c].append(w)
        for u in sorted(set(kids) | set(range(V))):
            if not (cons[u] or self.dl[u]): continue
            for w in cons[u]:
                po = 0 if self.ph[w] == 'A' else 1
                EV.append((u, ('R', h.dim[w], h.frame[w], w, po)))
            for t, lo in self.dl[u]:
                EV.append((u, ('lo', h.dim[u], h.frame[u], t, 1) if lo else ('hi', 7, Fm.HYP[t], t, 1)))
        for i, (u, e) in enumerate(EV): byu[u].append(i)
        return EV, byu
    @staticmethod
    def key(e): return (e[4], e[1], 0 if e[0] == 'R' else 1, e[3])
    def prec(self, a, b):
        if a[0] == 'hi': return False
        if self.key(a) >= self.key(b): return False
        return a[2] == b[2] or (a[1] < b[1] and self.Fm.inside(a[2], b[2]))
    def solve(self, kids, tl=300):
        V = self.V
        EV, byu = self.events(kids)
        links = []
        for u, L in byu.items():
            for i in L:
                for j in L:
                    if i != j and self.prec(EV[i][1], EV[j][1]): links.append((i, j, 0, None))
        for i, (u, e) in enumerate(EV):
            if e[0] == 'R':
                for j in byu.get(e[3], []): links.append((i, j, 1, e[3]))
        nl = len(links); succ = defaultdict(list); pred = defaultdict(list); hostw = defaultdict(list)
        for k, (i, j, kd, w) in enumerate(links):
            succ[i].append(k); pred[j].append(k)
            if kd == 1: hostw[w].append(k)
        rows = []; cols = []; vals = []; lo = []; hi = []; r = 0
        for grp in list(succ.values()) + list(pred.values()) + list(hostw.values()):
            for k in grp: rows.append(r); cols.append(k); vals.append(1.0)
            lo.append(-np.inf); hi.append(1); r += 1
        for u, L in byu.items():       # a source keeps a register that never hosts
            if u < V and L:
                for i in L:
                    for k in succ.get(i, []): rows.append(r); cols.append(k); vals.append(1.0)
                lo.append(-np.inf); hi.append(len(L) - 1); r += 1
        A = coo_matrix((vals, (rows, cols)), shape=(r, nl)).tocsr()
        res = milp(-np.ones(nl), constraints=LinearConstraint(A, lo, hi), integrality=np.ones(nl), bounds=Bounds(0, 1), options=dict(time_limit=tl, disp=False))
        assert res.status == 0, ('chain ILP not solved to optimality', res.status)
        x = np.round(res.x).astype(int)
        nxt = {}
        for k, (i, j, kd, w) in enumerate(links):
            if x[k]: nxt[i] = (j, kd)
        nsrc = sum(1 for u in byu if u < V)
        return EV, nxt, len(EV) - len(nxt) - nsrc
    def chains(self, kids, tl=300):
        """-> (chains, objective): chains[u] = list of chains, each a list of event keys (po, dim, kind, who) in register order"""
        EV, nxt, hp = self.solve(kids, tl)
        haspred = set(j for j, _ in nxt.values())
        chains = defaultdict(list)
        for i in range(len(EV)):
            if i in haspred: continue
            cur = None; j = i
            while True:
                u, e = EV[j]
                if cur is None or cur[0] != u:
                    cur = (u, []); chains[u].append(cur[1])
                cur[1].append((e[4], e[1], 0 if e[0] == 'R' else 1, e[3]))
                if j in nxt: j = nxt[j][0]
                else: break
        return {u: c for u, c in sorted(chains.items())}, hp
