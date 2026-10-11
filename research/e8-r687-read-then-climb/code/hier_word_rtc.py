"""Compile the frozen R687 hierarchy into the bit word with READ-THEN-CLIMB phases.
PR #370's compile2 + fullword are used unchanged except for ONE substituted function: the phase rule.  PR #370 puts every rule
built from sources in phase A (before the scatter), so a low read of a symbol at its own frame (phase B, after the scatter)
can never share a register with a rule that consumes the same symbol at a larger frame (the register would already have
climbed).  Read-then-climb: a rule that consumes a LOW-READ symbol (or a phase-B symbol) goes to phase B, after the
deliveries at that symbol's frame; its register is low-read at F_u first and then climbs to the consumer's frame.  compile2's
chain cover, carriers, deliveries and fullword's dirt compensation/cleanup are otherwise unchanged; PR #443's elimination
reuse and #436 retiming follow unchanged.  The hierarchy is checked first exactly as for R715 (content = kid sum, frames
closed and nested, every target's reads sum to its 63 in-cap lines inside its hyperplane).
usage: hier_word_rtc.py REPO_RESEARCH_DIR HIERARCHY.json OUT_RAW OUT_REUSED OUT_FINAL
Hierarchy: PR #370 Hamming design (Dylan Crow) with frame-pair D4 sums, cancelling re-expressions, and coset-split pi-pairings
(one coset of each block reads a different pairing partition, so 56 M sums are read at their own D5 frame by two targets
each); prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
import os, sys, json
os.environ['E8COORD'] = 'ham'
R, hpath, out_raw, out_reused, out_final = sys.argv[1:6]
P436 = os.path.join(R, 'e8-r740-replica32/parent436/code')
sys.path[:0] = [os.path.join(P436, 'bit/producer'), os.path.join(P436, 'reuse')]
import e8lib as E, frames as Fm, compile2 as C2, compile as C, fullword, reuse as RU, retime as RT
d = json.load(open(hpath)); V = E.V
assert d['format'] == 'e8bit-hierarchy/1' and d['coords'] == 'ham' and d['v'] == V
mask = lambda L: sum(1 << s for s in L)
class H: pass
h = H()
h.content = [mask(s) for s in d['symbols']]; h.frame = [mask(f) for f in d['frames']]
h.kids = [tuple(k) if k else None for k in d['kids']]; h.need = [set(n) for n in d['need']]
h.dim = []
for u, (c, f) in enumerate(zip(h.content, h.frame)):
    cf, dm = Fm.closure(f) if f else (0, 0)
    assert cf == f, ('frame not closed', u)
    assert c & ~f == 0, ('content outside frame', u)
    h.dim.append(dm)
for s in range(V): assert h.content[s] == 1 << s and h.frame[s] == Fm.LINE[s] and h.kids[s] is None
def acyclic(u, seen, stack):
    if u in seen: return
    stack.add(u)
    for c in h.kids[u] or ():
        assert c not in stack, ('cycle', u, c); acyclic(c, seen, stack)
    stack.discard(u); seen.add(u)
seen = set()
for u, k in enumerate(h.kids):
    if not k: continue
    acyclic(u, seen, set())
    x = 0
    for c in k:
        x ^= h.content[c]; assert h.frame[c] & ~h.frame[u] == 0, ('kid frame not inside', u, c)
    assert x == h.content[u], ('content is not the sum of kids', u)
for t in range(V):
    x = 0
    for u in h.need[t]:
        x ^= h.content[u]; assert h.frame[u] & ~Fm.HYP[t] == 0, ('read frame outside target hyperplane', t, u)
    assert x == Fm.HYP[t], ('target junk', t)
needed = C2.needed_symbols(h)
lowset = C2.choose_low(h, needed, None)          # PR #370's flag choice (longest nested chain of reads per target), unchanged
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
W = C2.compile2(h, lowset=lowset)
assert [len(z) for z in C.f2_check(W)] == [0, 0]
raw = fullword.build(W); fullword.save(raw, out_raw)
re_, n = RU.reuse(raw); fullword.save(re_, out_reused)
fin, mv = RT.retime(re_, sweeps=6, M=64); fullword.save(fin, out_final)
print(json.dumps(dict(status='PASS_HIERARCHY_COMPILED_READ_THEN_CLIMB', compile2=W.stats, raw_R=raw['R'], reuse_helpers=n['helpers'], reuse_totals=n['totals'],
                      reused_R=re_['R'], retime_moves=mv, final_R=fin['R'])))
