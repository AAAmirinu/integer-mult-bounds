"""Own re-implementations (read as data; none of the source PRs' scripts are run) of
  relocate():  #406's (rohanarun) transfer of our #402 target 177/220 re-synthesis onto a changed word (matching each
               delivery anchor to its unique B gate by an exact longest-matching-block alignment, stdlib difflib);
  sequential(): #409's (rohanarun) ordered sequential entrance gauges: for each group (sorted by decreasing gain,
               role-disjoint groups only) the pivots start at the group's rank-1 entrance frame and unit shears
               h_d += c*h_p are PREPENDED to A; a promoted pivot may be a donor of an older #404 group (it is read
               before any later entrance gate writes it);
  enlarge():   #410's (eumemic) entrance enlargement: a frozen pivot leaves its group, keeping its relation, and becomes
               a one-pivot group on a strictly larger entrance space;
  promote760(): #410's single sequential promotion of donor 760 in the rank-1 entrance [240] (control only).
Expected hashes of the frozen words (sha256 of compact sorted-key JSON) are pinned below."""
import copy, difflib, hashlib, json, os, sys
from fractions import Fraction as Q
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cxkernel import rehist, inside, first_frames
SHA = dict(w406='3f67e51a9de00a52983010aa74b16e48a230d39dc62dc7d7380ac8abc8981315',
           w409='e775f8106e736d2087f748b750e45f66b6e2b3c763d1ac48eb686e23d84c4c00',
           w408='7a5d0d0922b835eb818aa9cdbf06e51ef9c257ce05ae9dcb216422021c0652ce',
           w410prom='39c360dd4fc763b7fccff7ec5e2a3e8b50ae90e50d8ac50e062315253c2b411b',
           w410='5243b69bd3beec4b7632b49e9fc86cd0f2f84ec0736e173b06abeec8b1b7bb90')
def sha(c): return hashlib.sha256(json.dumps(c, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def relocate(ref, word, design):
    key = lambda g: json.dumps(g, separators=(',', ':')); a = list(map(key, ref['B'])); b = list(map(key, word['B']))
    mp = {i + k: j + k for i, j, n in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_matching_blocks() for k in range(n)}
    out = {}
    for t, dl in design.items():
        out[t] = []
        for pos, f, s, q in dl:
            o = pos - len(ref['A']) - 1; cur = mp[o]; assert a[o] == b[cur] and [i for i, g in enumerate(b) if g == a[o]] == [cur]
            out[t].append((len(word['A']) + cur + 1, f, s, q))
    return out
def sequential(c0, sel):
    c = copy.deepcopy(c0); plans = sorted(sel, key=lambda p: -p['gain']); used = set(); ext = dict(c0['ext']); gates = []; first = first_frames(c0); new = []
    for plan in plans:
        roles = set(plan['donors']) | {p['pivot'] for p in plan['pivots']}
        if roles & used: continue
        assert not roles & set(ext)
        E = plan['basis']; fid = next((i for i, e in enumerate(c['frames']) if e == E), len(c['frames']))
        if fid == len(c['frames']): c['frames'].append(E)
        for s in roles: assert inside(E, c0['frames'][first[s]])
        for p in plan['pivots']:
            pv = p['pivot']; co = {int(k): Q(str(v)).limit_denominator(10000) for k, v in p['coefficients'].items()}
            assert all(q.denominator in (1, 2) for q in co.values())
            c['start'][pv] = fid; ext[pv] = fid; new.append((fid, pv, co))
            for d, q in co.items(): gates += [['in', fid, d, [[pv, 1 if q > 0 else -1, q.denominator]]] for _ in range(abs(q.numerator))]
        used |= roles
    c['A'] = gates + c['A']; c['ext'] = sorted([p, f] for p, f in ext.items())
    return rehist(c), gates, new
def enlarge(sel, changes, rename={}):
    sel = copy.deepcopy(sel)
    for ch in changes:
        p = rename.get(ch['pivot'], ch['pivot'])
        i = next(i for i, pl in enumerate(sel['plans']) if any(e['pivot'] == p for e in pl['pivots']))
        pl = sel['plans'][i]; assert pl['basis'] == ch['old'], (p, pl['basis'], ch['old'])
        e = next(e for e in pl['pivots'] if e['pivot'] == p); pl['pivots'].remove(e)
        pl['donors'] = sorted({int(d) for x in pl['pivots'] for d in x['coefficients']})
        assert len(ch['new']) > len(ch['old'])
        sel['plans'].append(dict(basis=ch['new'], ed=len(ch['new']), donors=sorted(int(d) for d in e['coefficients']), pivots=[e]))
    return sel
PROM760 = (760, [240], {896: Q(-1), 998: Q(-1), 955: Q(-2), 898: Q(-1), 1003: Q(-1), 836: Q(-1)})
def promote760(c0):
    p, entry, cm = PROM760; c = copy.deepcopy(c0); f = next(i for i, e in enumerate(c['frames']) if len(e) == 1 and inside(entry, e)); assert c['start'][p] == 0
    c['start'][p] = f; c['ext'] = sorted(c['ext'] + [[p, f]])
    head = []
    for d, q in sorted(cm.items()): head += [['in', f, d, [[p, 1 if q > 0 else -1, q.denominator]]] for _ in range(abs(q.numerator))]
    c['A'] = head + c['A']; return rehist(c)
def repivot_rows(pl, S):
    """re-express a group's relations with pivot set S (same relation span); None if a coefficient leaves {1, 1/2}."""
    R = [{**{int(d): Q(str(a)).limit_denominator(10000) for d, a in e['coefficients'].items()}, e['pivot']: Q(1)} for e in pl['pivots']]
    cols = sorted({k for r in R for k in r}); M = [[r.get(k, Q(0)) for k in cols] for r in R]; n = len(M)
    for i, s in enumerate(S):
        j = cols.index(s); p = next((a for a in range(i, n) if M[a][j]), None)
        if p is None: return None
        M[i], M[p] = M[p], M[i]; pv = M[i][j]; M[i] = [x / pv for x in M[i]]
        for a in range(n):
            if a != i and M[a][j]: f = M[a][j]; M[a] = [x - f * y for x, y in zip(M[a], M[i])]
    out = []
    for i, s in enumerate(S):
        co = {cols[j]: M[i][j] for j in range(len(cols)) if M[i][j] and cols[j] != s}
        if any(x.denominator not in (1, 2) for x in co.values()): return None
        out.append({'pivot': s, 'coefficients': {str(d): (int(a) if a.denominator == 1 else float(a)) for d, a in sorted(co.items())}})
    q = copy.deepcopy(pl); q['pivots'] = out; q['donors'] = sorted({int(d) for e in out for d in e['coefficients']}); return q
