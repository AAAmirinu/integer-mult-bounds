"""Build the R685 bit word from the frozen R687 hierarchy (PR #504, research/e8-r687-read-then-climb/data/hierarchy-r687.json).

Stage 1  D4(c) INLINE.  Fifteen rules change their kid lists (data/inline-kids.json): the 14 D4(c) sums (8 lines, dim 4) are built from their four
         pairs directly instead of from two L's (28 inlines), and one 12-line sum reads two source lines instead of one pair (1 inline).  Each inlined
         kid is replaced by ITS kids, so the content of every rule is unchanged (checked).  The 28 L's that fed D4(c) lose their third, D4, reader:
         chi 3 -> 2, 28 L copies fewer.
Stage 2  CHAINS.  PR #370's compile2 assigns register chains greedily.  Here the chains are the optimum of the exact path-cover ILP (code/chain_model.py),
         pinned in data/chains-inline.json and handed to compile2 through an override of ONE statement (the chain loop; the patch is applied to
         PR #370's compile2.py source at run time, each anchor must occur exactly once).  Phases are read-then-climb exactly as in #504.  Then PR #370's
         fullword, PR #443's reuse and PR #436's retime, unchanged.   (--solve recomputes the chains with HiGHS and compares the objective.)
Stage 3  COPY DELETIONS.  code/copy_sweep.py: the two D4(c) copies (class 8/4) all of whose reads can take other registers at a legal frame are deleted
         in the raw word; reuse and retime run again.  (A third redundant copy, the 16/6 high read, is left in: deleting it costs two kernel pivots.)
usage: r685_word.py REPO_RESEARCH_DIR OUT_DIR [--solve]
writes OUT_DIR/{inline_raw,inline_reused,inline,raw,reused,word}.json.gz, OUT_DIR/chains.json (with --solve), OUT_DIR/deletions.json; prints a JSON summary.
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
import os, sys, json, gzip, types
os.environ['E8COORD'] = 'ham'
R, out = sys.argv[1:3]
solve = '--solve' in sys.argv[3:]
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE); BIT = os.path.join(R, 'e8-r687-read-then-climb')
P436 = os.path.join(R, 'e8-r740-replica32/parent436/code')
sys.path[:0] = [os.path.join(P436, 'bit/producer'), os.path.join(P436, 'reuse'), HERE]
import e8lib as E, frames as Fm, compile as C, fullword, reuse as RU, retime as RT
import copy_sweep
os.makedirs(out, exist_ok=True)
V = E.V
d = json.load(open(os.path.join(BIT, 'data/hierarchy-r687.json')))
assert d['format'] == 'e8bit-hierarchy/1' and d['coords'] == 'ham' and d['v'] == V
mask = lambda L: sum(1 << s for s in L)
class H: pass
h = H()
h.content = [mask(s) for s in d['symbols']]; h.frame = [mask(f) for f in d['frames']]
h.kids = [tuple(k) if k else None for k in d['kids']]; h.need = [set(n) for n in d['need']]
h.dim = []
for u, (c, f) in enumerate(zip(h.content, h.frame)):
    cf, dm = Fm.closure(f) if f else (0, 0)
    assert cf == f and c & ~f == 0, ('frame', u); h.dim.append(dm)
# ---- stage 1: the inline (every changed rule: new kids = old kids with some rule kids replaced by their own kids)
ik = {int(k): v for k, v in json.load(open(os.path.join(PKG, 'data/inline-kids.json')))['kids'].items()}
old = list(h.kids)
for w, nk in ik.items():
    expanded = [c for c in old[w] if c not in nk]
    exp = []
    for c in old[w]: exp.extend(old[c] if c in expanded else [c])
    assert expanded and exp == nk, ('not an inline of the old kids', w)
    assert all(old[c] for c in expanded)
    h.kids[w] = tuple(nk)
d2 = dict(d); d2['kids'] = [list(k) if k else None for k in h.kids]
json.dump(d2, open(os.path.join(out, 'hierarchy-r685.json'), 'w'))
n_inl = sum(len([c for c in old[w] if c not in nk]) for w, nk in ik.items())
def acyclic(u, seen, stack):
    if u in seen: return
    stack.add(u)
    for c in h.kids[u] or ():
        assert c not in stack, ('cycle', u, c); acyclic(c, seen, stack)
    stack.discard(u); seen.add(u)
seen = set()
for u, k in enumerate(h.kids):
    if not k: continue
    acyclic(u, seen, set()); x = 0
    for c in k:
        x ^= h.content[c]; assert h.frame[c] & ~h.frame[u] == 0, ('kid frame not inside', u, c)
    assert x == h.content[u], ('content is not the sum of kids', u)
for t in range(V):
    x = 0
    for u in h.need[t]:
        x ^= h.content[u]; assert h.frame[u] & ~Fm.HYP[t] == 0
    assert x == Fm.HYP[t]
# ---- compile2 with a chain override (one statement of PR #370's compile2.py patched at run time)
src = open(os.path.join(P436, 'bit/producer/compile2.py')).read()
a1 = "V=E.V\n"; a2 = "    chains={}; chain_of={}\n    for u in needed:\n        ev=sorted(uses[u],"
assert src.count(a1) == 1 and src.count(a2) == 1
src = src.replace(a1, a1 + "OVERRIDE=[None]\n").replace(a2, "    chains={}; chain_of={}\n    if OVERRIDE[0] is not None: chains,chain_of=OVERRIDE[0](h,needed,uses)\n    for u in (needed if OVERRIDE[0] is None else ()):\n        ev=sorted(uses[u],")
C2 = types.ModuleType('compile2_chains'); exec(compile(src, 'compile2_chains', 'exec'), C2.__dict__)
needed = C2.needed_symbols(h)
lowset = C2.choose_low(h, needed, None)
lowsyms = {u for (t, u) in lowset}
def phases_read_then_climb(h_, needed_):
    ph = {}
    def get(u):
        if u < V: return 'S'
        if u in ph: return ph[u]
        ks = [get(c) for c in h_.kids[u]]
        ph[u] = 'B' if (any(k == 'B' for k in ks) or any(c in lowsyms for c in h_.kids[u])) else 'A'
        return ph[u]
    for u in needed_:
        if u >= V: get(u)
    return ph
C2.phases = phases_read_then_climb
ph = phases_read_then_climb(h, needed)
chain_p = os.path.join(PKG, 'data/chains-inline.json')
pinned = json.load(open(chain_p)) if os.path.exists(chain_p) else None
info = {}
if solve:
    from chain_model import ChainModel
    kids = {w: list(h.kids[w]) for w in needed if w >= V}
    chains_, hp = ChainModel(h, lowset, ph, Fm).chains(kids)
    json.dump(dict(objective=hp, chains={str(u): c for u, c in chains_.items()}), open(os.path.join(out, 'chains.json'), 'w'))
    solved = dict(objective=hp, chains={str(u): c for u, c in chains_.items()})
    if pinned is None: pinned = solved             # bootstrap: generating data/chains-inline.json
    else:
        info.update(chain_ilp_objective=hp, chains_equal_pinned=(solved == pinned))
        assert hp == pinned['objective'], ('chain ILP objective differs from the pinned one', hp, pinned['objective'])
chains_spec = {int(u): c for u, c in pinned['chains'].items()}
def override(h_, needed_, uses):
    chains, chain_of = {}, {}
    for u in needed_:
        cl = []
        for ci, ch in enumerate(chains_spec[u]):
            ev = []
            for (po, dm, kind, who) in ch:
                fr = h_.frame[who] if kind == 0 else (Fm.HYP[who] if dm == 7 else h_.frame[u])
                ev.append((po, dm, kind, fr, who)); chain_of[(u, kind, who)] = ci
            cl.append(ev)
        assert sorted(e for ch in cl for e in ch) == sorted(uses[u]), ('pinned chains do not cover the read events', u)
        chains[u] = cl
    return chains, chain_of
C2.OVERRIDE[0] = override
W = C2.compile2(h, lowset=lowset)
assert [len(z) for z in C.f2_check(W)] == [0, 0]
raw = fullword.build(W); fullword.save(raw, os.path.join(out, 'inline_raw.json.gz'))
re_, n = RU.reuse(raw); fullword.save(re_, os.path.join(out, 'inline_reused.json.gz'))
fin, mv = RT.retime(re_, sweeps=6, M=64); fullword.save(fin, os.path.join(out, 'inline.json.gz'))
info.update(inline_moves=n_inl, rules_changed=len(ik), stage_inline=dict(compile2=W.stats, raw_R=raw['R'], reuse_helpers=n['helpers'], reuse_totals=n['totals'], reused_R=re_['R'], retime_moves=mv, final_R=fin['R']))
# ---- stage 3: word-level copy deletions
w2, log = copy_sweep.delete_copies(raw, Fm, RU, {'8/4'})
fullword.save(w2, os.path.join(out, 'raw.json.gz'))
re2, n2 = RU.reuse(w2); fullword.save(re2, os.path.join(out, 'reused.json.gz'))
fin2, mv2 = RT.retime(re2, sweeps=6, M=64); fullword.save(fin2, os.path.join(out, 'word.json.gz'))
json.dump(log, open(os.path.join(out, 'deletions.json'), 'w'), sort_keys=True)
info.update(status='PASS_R685_WORD_BUILT', deletions=dict(removable_by_class=log['removable_by_class'], deleted=[(e['copy_register'], e['cls']) for e in log['deleted']], raw_R=log['raw_R']),
            stage_delete=dict(raw_R=w2['R'], reuse_helpers=n2['helpers'], reuse_totals=n2['totals'], reused_R=re2['R'], retime_moves=mv2, final_R=fin2['R']))
print(json.dumps(info, sort_keys=True))
