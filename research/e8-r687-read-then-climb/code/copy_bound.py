"""Copy anatomy and the transversal-cover lower bound for a frozen hierarchy (README, 'Copies: a lower bound').
Recomputes, independently of compile2's greedy chain cover, the minimum number of nested register chains chi(u) of every
symbol (Dilworth: uses = rule consumers in the given phase, then deliveries; a use may follow another on one register iff
its frame contains the earlier frame, strictly larger in dimension or equal), and the per-symbol transversal-cover bound
cov(u): a chain whose FIRST use is at frame G serves only targets in G^perp, so chi(u) >= the least number of proper sections
G^perp (G > F_u) covering the downstream targets not reached through a use at F_u itself (such a chain may climb on
and serve one section, so it is not counted separately).
usage: copy_bound.py REPO_RESEARCH_DIR HIERARCHY.json [allA|rtc]      prints JSON.
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
import os, sys, json, itertools
from collections import Counter, defaultdict
from fractions import Fraction as Fr
os.environ['E8COORD'] = 'ham'
R, hpath = sys.argv[1:3]; mode = sys.argv[3] if len(sys.argv) > 3 else 'rtc'
sys.path[:0] = [os.path.join(R, 'e8-r740-replica32/parent436/code/bit/producer')]
import e8lib as E, frames as Fm, compile2 as C2
V = E.V; Lv = E.LINES
d = json.load(open(hpath)); mask = lambda L: sum(1 << s for s in L)
class H: pass
h = H(); h.content = [mask(s) for s in d['symbols']]; h.frame = [mask(f) for f in d['frames']]
h.kids = [tuple(k) if k else None for k in d['kids']]; h.need = [set(n) for n in d['need']]; h.dim = [Fm.closure(f)[1] if f else 0 for f in h.frame]
needed = C2.needed_symbols(h); low = C2.choose_low(h, needed, None); lows = {u for t, u in low}
ph = {}
def get(u):
    if u < V: return 'S'
    if u not in ph:
        ks = [get(c) for c in h.kids[u]]
        ph[u] = 'B' if mode == 'rtc' and (any(k == 'B' for k in ks) or any(c in lows for c in h.kids[u])) else 'A'
    return ph[u]
for u in needed:
    if u >= V: get(u)
uses = defaultdict(list); cons = defaultdict(list); deliv = defaultdict(list)
for w in needed:
    if w >= V:
        for c in h.kids[w]: uses[c].append((0 if ph[w] == 'A' else 1, h.dim[w], 0, h.frame[w], ('r', w))); cons[c].append(w)
for t in range(V):
    for u in h.need[t]:
        deliv[u].append(t)
        uses[u].append((1, h.dim[u], 1, h.frame[u], ('lo', t)) if (t, u) in low else (1, 7, 1, Fm.HYP[t], ('hi', t)))
def before(a, b):          # a may precede b on one register: compile2's event order (phase, dimension, rule-before-delivery), nested frames
    if a[4][0] == 'hi' or a[:3] > b[:3]: return False
    return a[3] == b[3] or (a[1] < b[1] and Fm.inside(a[3], b[3]))
def width(E_):
    E_ = sorted(E_, key=lambda e: e[:3])   # a strict order: equal keys chain in list order
    n = len(E_); adj = [[j for j in range(i + 1, n) if before(E_[i], E_[j])] for i in range(n)]; match = [-1] * n
    def aug(i, seen):
        for j in adj[i]:
            if j in seen: continue
            seen.add(j)
            if match[j] < 0 or aug(match[j], seen): match[j] = i; return True
        return False
    return n - sum(1 for i in range(n) if aug(i, set()))
memo = {}
def down(u):
    if u not in memo:
        s = set(deliv[u])
        for w in cons[u]: s |= down(w)
        memo[u] = frozenset(s)
    return memo[u]
def rank(ts):
    rows = []
    for t in ts:
        x = [Fr(a) for a in Lv[t]]
        for r in rows:
            p = next(k for k in range(8) if r[k])
            if x[p]: f = x[p] / r[p]; x = [a - f * b for a, b in zip(x, r)]
        if any(x): rows.append(x)
    return len(rows)
def cover(T, k):           # least number of parts of rank <= k-1 (exact for |T| <= 14; else 1 or 2 as a valid lower bound)
    T = sorted(T)
    if not T: return 0
    if rank(T) < k: return 1
    if len(T) > 14: return 2
    def ok(rem, m):
        if not rem: return True
        if m == 1: return rank(rem) <= k - 1
        f, rest = rem[0], rem[1:]
        for r in range(len(rest) + 1):
            for S in itertools.combinations(rest, r):
                if rank([f, *S]) <= k - 1 and ok([x for x in rest if x not in S], m - 1): return True
        return False
    m = 2
    while not ok(T, m): m += 1
    return m
chi = {}; bound = {}; cls = lambda u: '%d/%d' % (bin(h.content[u]).count('1'), h.dim[u])
for u in needed:
    if u < V: continue
    chi[u] = width(uses[u])
    own = {t for t in deliv[u] if (t, u) in low}
    for w in cons[u]:
        if h.frame[w] == h.frame[u]: own |= down(w)
    rest = {t for t in deliv[u] if (t, u) not in low}
    for w in cons[u]:
        if h.frame[w] != h.frame[u]: rest |= down(w)
    rest -= own
    bound[u] = max(1, cover(rest, 8 - h.dim[u]))   # an own-frame chain may climb on and serve one of the sections
    assert bound[u] <= chi[u], ('bound exceeds chain cover', u)
carriers = sum(width(uses[s]) - 1 for s in range(V))
by = defaultdict(lambda: [0, 0])
for u in chi: by[cls(u)][0] += chi[u] - 1; by[cls(u)][1] += bound[u] - 1
print(json.dumps(dict(status='PASS_COPY_ANATOMY_AND_BOUND', phase_rule=mode, copies=sum(c - 1 for c in chi.values()), carriers=carriers,
                      transversal_cover_bound=sum(b - 1 for b in bound.values()), chi_histogram=dict(sorted(Counter(chi.values()).items())),
                      by_class={k: dict(copies=v[0], bound=v[1]) for k, v in sorted(by.items()) if v[0] or v[1]}), sort_keys=True))
