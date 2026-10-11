"""Exact symbolic sweep of a RAW bit word (PR #370 fullword.build output, before reuse), and word-level deletion of redundant copies.

Every register content is an exact F2 form; here only the x-part matters (helper dirt is rebuilt exactly by PR #443's reuse step, which recomputes D and C).
Frame legality is the usual one: along a register's life frames only climb and every gate reads at one common frame.  So an extra read of register q at
time t at gate frame f is legal iff  cur(q,t) <= f <= nxt(q,t)  (frame of q's last touch before t, frame of its first touch after t; final frame if none).

A COPY gate (q += p, q fresh) is redundant iff every read of the copy's content can instead take a set S (|S| <= 3) of other registers holding that
content in x-part, with each member legal at that read's own gate frame.  Replacing the reads and deleting the copy gate keeps the word exact (the
check is the F2 replay of the stock checker).  Frame choice: the original gate frame is kept.  Among the alternatives the one with least extra climbing
(r ln(40/r) step costs, PR #443's ecost table) and then fewest members is taken; the first in pool order breaks ties.

Classes are '<lines>/<dim>' of the copied symbol, e.g. '8/4' = the D4(c) sums (Bcw).
usage: copy_sweep.py REPO_RESEARCH_DIR RAW.json.gz OUT_RAW.json.gz CLASSES(comma list or '-' for report only) > log.json
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
import os, sys, json, gzip, bisect
from collections import defaultdict, Counter
os.environ.setdefault('E8COORD', 'ham')

def setup(R):
    P436 = os.path.join(R, 'e8-r740-replica32/parent436/code')
    sys.path[:0] = [os.path.join(P436, 'bit/producer'), os.path.join(P436, 'reuse')]
    import frames as Fm, reuse as RU
    return Fm, RU

class Sweep:
    def __init__(self, w, Fm, RU):
        self.w, self.Fm, self.RU = w, Fm, RU
        v = self.v = w['v']; R = w['R']; n = self.n = 2 * v + R; self.X = (1 << v) - 1
        self.fm = [sum(1 << s for s in f) for f in w['frames']]
        self.A = w['A']; self.B = w['B']; self.nA = len(self.A)
        self._dim = {0: 0}
        self.gates = [('A', i, g) for i, g in enumerate(self.A)] + [('B', i, g) for i, g in enumerate(self.B)]
        # time: A gates 0..nA-1, scatter at nA, B gate j at nA+1+j
        self.time = [i if ph == 'A' else self.nA + 1 + i for ph, i, g in self.gates]
        self.start = [self.fm[f] for f in w['start']]; self.final = [self.fm[f] for f in w['final']]
        self.touch = defaultdict(list)
        for (ph, i, (f, d, ss)), t in zip(self.gates, self.time):
            for q in [d] + ss: self.touch[q].append((t, self.fm[f]))
        self.tt = {q: [a for a, _ in L] for q, L in self.touch.items()}
    def dim(self, m):
        if m not in self._dim: self._dim[m] = self.Fm.closure(m)[1]
        return self._dim[m]
    def cur(self, q, t):
        L = self.tt.get(q)
        if not L: return self.start[q]
        i = bisect.bisect_left(L, t)
        return self.touch[q][i - 1][1] if i else self.start[q]
    def nxt(self, q, t):
        L = self.tt.get(q)
        if not L: return self.final[q]
        i = bisect.bisect_right(L, t)
        return self.touch[q][i][1] if i < len(L) else self.final[q]
    def replay(self):
        """x-part versions of the helper registers; snapshots of all x-parts before every gate that reads a copy"""
        v, n, X = self.v, self.n, self.X
        xc = [0] * n
        for q in range(v): xc[q] = 1 << q
        self.snap = {}
        self.vers = []               # dicts: reg, gate index, src (x-part after), kind, reads [(gate index, host?)]
        curv = {}
        for gi, ((ph, i, (f, d, ss)), t) in enumerate(zip(self.gates, self.time)):
            self.snap[gi] = list(xc)
            pre = xc[d]
            if d >= 2 * v:
                for q in ss:
                    if q in curv: self.vers[curv[q]]['reads'].append((gi, False))
                if pre and d in curv: self.vers[curv[d]]['reads'].append((gi, True))
            else:
                for q in ss:
                    if q in curv: self.vers[curv[q]]['reads'].append((gi, False))
            post = pre
            for q in ss: post ^= xc[q]
            xc[d] = post
            if d >= 2 * v:
                spre = [self.snap[gi][q] for q in ss]
                if len(ss) == 1 and pre == 0 and ss[0] >= 2 * v and post == spre[0] and post: kind = 'copy'
                elif len(ss) == 1 and pre == 0 and ss[0] < v: kind = 'carrier'
                else: kind = 'rule'
                self.vers.append(dict(reg=d, gate=gi, src=post, kind=kind, reads=[], frame=self.fm[f]))
                curv[d] = len(self.vers) - 1
        return self
    def alternatives(self, content, gi, banned, maxk=3):
        """window-feasible sets S (|S|<=maxk) of registers (helpers and sources) whose x-parts XOR to `content`, legal at gate gi's own frame"""
        v, n = self.v, self.n
        ph, i, (f, d, ss) = self.gates[gi]; t = self.time[gi]; fm = self.fm[f]
        X_ = self.snap[gi]; pool = []
        for r in list(range(v)) + list(range(2 * v, n)):
            if r in banned or X_[r] == 0: continue
            if self.cur(r, t) & ~fm or fm & ~self.nxt(r, t): continue
            pool.append((r, X_[r]))
        byx = defaultdict(list)
        for r, x in pool: byx[x].append(r)
        res = []
        for r in byx.get(content, ()): res.append((r,))
        seen = set()
        for r, x in pool:
            for r2 in byx.get(content ^ x, ()):
                if r2 != r and (min(r, r2), max(r, r2)) not in seen: seen.add((min(r, r2), max(r, r2))); res.append((r, r2))
        if maxk >= 3:
            for a, (r, x) in enumerate(pool):
                for r2, x2 in pool[a + 1:]:
                    for r3 in byx.get(content ^ x ^ x2, ()):
                        if r3 not in (r, r2):
                            key = tuple(sorted((r, r3, r2)))
                            if key not in seen: seen.add(key); res.append(key)
        return res
    def cost(self, S, gi):
        ph, i, (f, d, ss) = self.gates[gi]; t = self.time[gi]; fm = self.fm[f]; step = self.RU._step; c = 0
        df = self.dim(fm)
        for a in S:
            cu, nx = self.cur(a, t), self.nxt(a, t)
            c += step(self.dim(cu), df) + step(df, self.dim(nx)) - step(self.dim(cu), self.dim(nx))
        return c
    def removable(self, maxk=3):
        """copies all of whose reads can be replaced: list of dict(vi, reg, cls, reads=[(gate index, host?, chosen S)])"""
        out = []
        for vi, x in enumerate(self.vers):
            if x['kind'] != 'copy': continue
            q = x['reg']; reads = []
            for gi, host in x['reads']:
                ph, i, (f, d, ss) = self.gates[gi]
                banned = {q} | set(ss) | {d} if not host else {q} | set(ss)
                alts = self.alternatives(x['src'], gi, banned, maxk)
                if not alts: reads = None; break
                S = min(alts, key=lambda S_: (self.cost(S_, gi), len(S_)))
                reads.append((gi, host, S))
            if reads is None or not x['reads']: continue
            cls = '%d/%d' % (bin(x['src']).count('1'), self.dim(x['frame']))
            out.append(dict(vi=vi, reg=q, cls=cls, gate=x['gate'], reads=reads))
        return out

def delete_copies(w, Fm, RU, classes, maxk=3):
    """returns (new raw word, log).  classes: set of '<lines>/<dim>' strings; None = report only"""
    sw = Sweep(w, Fm, RU).replay(); rem = sw.removable(maxk)
    report = Counter(r['cls'] for r in rem)
    log = dict(removable_by_class=dict(sorted(report.items())), deleted=[])
    if not classes: return None, log
    v = w['v']
    A = [[f, d, list(ss)] for f, d, ss in w['A']]; B = [[f, d, list(ss)] for f, d, ss in w['B']]
    drop = set()
    for r in rem:
        if r['cls'] not in classes: continue
        ent = dict(copy_register=r['reg'], cls=r['cls'], birth_gate=r['gate'], reads=[])
        drop.add(r['gate'])
        for gi, host, S in r['reads']:
            ph, i, _ = sw.gates[gi]; g = (A if ph == 'A' else B)[i]
            if host: g[2] = list(g[2]) + list(S)       # the rule register now starts at this gate
            else: g[2] = [x for x in g[2] if x != r['reg']] + list(S)
            ent['reads'].append(dict(phase=ph, index=i, dest=g[1], host=host, replaced_by=list(S), sources_after=list(g[2])))
        log['deleted'].append(ent)
    A2 = [g for gi, g in enumerate(A) if gi not in drop]
    used = sorted({r for gl in (A2, B) for f, d, ss in gl for r in [d] + ss if r >= 2 * v} | set(w['ret']))
    newid = {r: 2 * v + k for k, r in enumerate(used)}
    for k in range(2 * v): newid[k] = k
    ren = lambda gl: [[f, newid[d], [newid[x] for x in ss]] for f, d, ss in gl]
    w2 = dict(w); w2['A'] = ren(A2); w2['B'] = ren(B); w2['ret'] = [newid[q] for q in w['ret']]
    w2['R'] = len(used); w2['start'] = w['start'][:2 * v] + [w['start'][2 * v]] * len(used); w2['final'] = w['final'][:2 * v] + [w['final'][2 * v]] * len(used)
    w2['D'] = []; w2['C'] = []       # rebuilt exactly by the reuse step
    log['raw_R'] = [w['R'], w2['R']]
    return w2, log

if __name__ == '__main__':
    R, raw_p, out_p, classes = sys.argv[1:5]
    Fm, RU = setup(R)
    w = json.load(gzip.open(raw_p, 'rt'))
    w2, log = delete_copies(w, Fm, RU, None if classes == '-' else set(classes.split(',')))
    if w2 is not None:
        with open(out_p, 'wb') as fh:
            with gzip.GzipFile(filename='', mode='wb', fileobj=fh, mtime=0) as gz: gz.write(json.dumps(w2, separators=(',', ':'), sort_keys=True).encode())
    print(json.dumps(log, sort_keys=True))
