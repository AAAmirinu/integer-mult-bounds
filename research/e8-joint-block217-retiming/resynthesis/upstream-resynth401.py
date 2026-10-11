"""e8-response-resynth: two exact target re-syntheses on Dugongue's #401 response-subspace R781 E8 complex program,
compiled with #390's dirty-preconditioned bracket (our emission reproduces #401's b and kappa exactly).
usage: fusion401.py PKGDIR GXDIR OUTDIR [--regen]
  A. #401's word: own re-implementation of its entrance construction on #398's word, equal to #401's frozen candidate
     hash; gx.check1 (incl. E7: no gauged dirt reaches a target) + gxcore; raw operator = #398's * diag(I, I, S).
  B. (--regen) negative check: the only same-frame zero-row sinks (301/324/387) need a quarter of a #401-gauged
     register, which gxcore's sixths rule rejects; padding fusion is therefore not composed.
  C. target re-synthesis of 177 and 220 (exact, preserving x, y AND the 119 gauged helper-dirt columns of every target).
     (--regen: the exact discovery over all 120 targets with the K_p = 0 constraint regenerates exactly these two.)
  D. local program, both orientations, all 1021 live columns, for #401's word (control), and ours; mutation controls.
  E. #401's bank patterns (748 banks/stage, 482 rank-1 + 1 rank-10 paddings), re-implemented.
  F. price: #401's 24-digit complex root and kappa reproduced from OUR emission of its word under #390's bracket
     (control); ours priced the same way.  Bit side: #401's pinned bit coarse bound (it binds nowhere: c > b)."""
import sys, os, json, gzip, copy
from collections import Counter, deque
from fractions import Fraction as Q
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PKG, GXD, OD = sys.argv[1], sys.argv[2], sys.argv[3]; REGEN = '--regen' in sys.argv
sys.path.insert(0, GXD); import gx, gxcore
import emit as EM
import sinks as SK
from word import insert, origmap, sixths
from redesign import build, from_json
from search import Search
from entrance import build as entrance
from bootstrap import certify24, refine
ld = lambda p: json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
base = ld(PKG + '/data/pr398/signed25.json.gz'); sel = ld(PKG + '/data/pr401/selection.json'); pats = ld(PKG + '/data/pr401/BANK-PATTERNS.json')
r401 = ld(PKG + '/data/pr401/RESULT.json'); DES = from_json(ld(PKG + '/data/designs-e8resynth401.json'))
src = open(HERE + '/cxop.py').read().split('\na, ta = op(')[0]; ns = {}; exec(compile(src, 'cxop.py', 'exec'), ns); op = ns['op']
R = base['R']; EM.setR(R); V, N = EM.V, EM.N; h, m, T, L = 9, 73, 8, 9
Z = []; assert sorted(DES) == [177, 220]

def hist(c):
    H = Counter()
    for w_ in c['blocks'].values():
        for r, n in w_.items(): H[int(r)] += n
    return H
def gxok(c, name):
    gx.check1(copy.deepcopy(c), scalar=True)
    assert gxcore.mirror(gxcore.normal(copy.deepcopy(c)))['hist'] == dict(hist(c))
    print('   %s: gx.check1 PASS (E0-E7 incl. exact scalar E5 and gauged-dirt rule), gxcore mirror PASS, gates A/B %d/%d' % (name, len(c['A']), len(c['B'])))

print('== A. #401 word (own re-implementation of its entrance gauges on #398\'s word)')
w = entrance(base, sel); gxok(w, '#401 word'); EXT = dict(w['ext']); piv = set(EXT)
print('   equals #401\'s frozen candidate (sha256 3b78069c...): 26 new frames, 119 pivots, 240 unit entrance shears')
ob, tb = op(base); ow, tw = op(w)
S = {}
for plan in sel['plans']:
    for e in plan['pivots']: S[e['pivot']] = {int(d): Q(str(a)).limit_denominator(10000) for d, a in e['coefficients'].items()}
for r in range(N):
    want = dict(ob[r])
    for p, cm in S.items():
        z = want.get(p, 0) + sum(a * ob[r].get(d, 0) for d, a in cm.items())
        if z: want[p] = z
        else: want.pop(p, None)
    assert want == ow[r], r
assert all(p not in ow[t] for p in piv for t in range(V, 2 * V))
print('   raw operator of #401\'s word == #398\'s * diag(I, I, S) on all %d registers; all 119 gauged response columns are zero' % N)

print('== B. free sinks (negative check)')
ws = w; os_, ts = ow, tw
if REGEN:
    a0 = SK.analyse(w); gauged = piv | {g[2] for g in w['A'][:240]}
    hits = {r: SK.find(w, r, an=a0) for r in range(2 * V, N) if a0[5][r] > 0}; hits = {r: g for r, g in hits.items() if g}
    assert sorted(hits) == [301, 324, 387] and all(any(u in gauged for g in gs for u, _, _ in g['uncompute']) for gs in hits.values())
    assert not [r for r in range(2 * V, N) if a0[5][r] > 0 and SK.find(w, r, exclude=gauged, an=a0)]
    print('   same-frame zero-row sinks on #401\'s word: only 301/324/387, and each needs a quarter of a #401-gauged register (1018/1019/1020),')
    print('   which leaves 1/4 of gauged dirt in the sink: gxcore\'s sixths rule (E5) rejects it, so padding fusion is NOT composed here')
print('== C. target re-synthesis (177, 220)')
ours = build(ws, DES); gxok(ours, 'ours')
oo, to = op(ours); assert to == ts
keep = lambda row: {k: q for k, q in row.items() if k < 2 * V or k in piv}
moved = 0
for r in range(N):
    if V <= r < 2 * V:
        assert keep(oo[r]) == keep(os_[r]), r; moved += sum(1 for k in set(oo[r]) | set(os_[r]) if oo[r].get(k) != os_[r].get(k))
    else: assert oo[r] == os_[r], r
SW = Search(ws, gauged=piv); SO = Search(ours, gauged=piv)
walks = {i: (SW.walk(i), SO.walk(i)) for i in sorted(DES)}
assert walks == {177: ((3, 5), (6, 2)), 220: ((3, 5), (6, 2))} and all(SO.walk(i) == SW.walk(i) for i in range(V, 2 * V) if i not in DES)
dd = hist(ours); dd.subtract(hist(ws)); dd = {k: x for k, x in sorted(dd.items()) if x}; assert dd == {2: 2, 3: -2, 5: -2, 6: 2}, dd
assert moved == 0 and oo == os_
print('   full raw operator (every register, all 1021 input columns incl. all helper-dirt columns, so #401\'s K too) and retained totals IDENTICAL to #401\'s word;')
print('   walks', walks, 'others unchanged; histogram delta', dd, '')
ctr = []
def reject(name, word, kind):
    try:
        if kind == 'op':
            o2, _ = op(word)
            for r in range(V, 2 * V): assert keep(o2[r]) == keep(os_[r])
        else: gx.check1(copy.deepcopy(word), scalar=True)
    except AssertionError: ctr.append(name); return
    raise SystemExit('control accepted: ' + name)
bad = copy.deepcopy(ours); j = next(j for j, g in enumerate(bad['B']) if g[0] == 'in' and g[2] == 177 and g[3][0][0] == 180 and g[1] == 0); bad['B'].pop(j)
reject('omitted_y_setup', bad, 'op')
D2 = copy.deepcopy(DES); p, f, s_, q = D2[220][-1]; D2[220][-1] = (p, f, s_, -q); reject('flipped_delivery', build(ws, D2), 'op')
D4 = copy.deepcopy(DES); p, f, s_, q = D4[220][-1]; D4[220][-1] = (p, 892, s_, q); reject('delivery_off_frame', build(ws, D4), 'gx')
print('   controls rejected:', ctr)
if REGEN:
    D5, rep = SW.discover(); assert D5 == DES, sorted(D5)
    print('   regeneration: exact discovery (K_p = 0 kept) over all %d targets: %d improvable, %d blocked by existing #398 restores, regenerates exactly 177 and 220'
          % (V, len(rep), sum(e['read_by_existing_gate'] for e in rep.values())))
json.dump(ours, gzip.open(os.path.join(OD, 'gcert1-e8resynth401.json.gz'), 'wt'))

print('== D. local program (#390 bracket, both orientations)')
paid = {}
for name, word, zs in [('#401 word', w, set()), ('ours', ours, set(Z))]:
    pw = EM.prewhite(word, zs)
    for ori in ['forward', 'backward']:
        ev = list(EM.emit(word, ori, {}, zs, pw)); r = EM.validate(ev, word, ori, {}, zs); paid[(name, ori)] = r['paid_hist']
        print('   %s %s: PASS all %d live columns, private work erased, common exact labels, %d events' % (name, ori, N, r['events']))
        if name == 'ours':
            def rej(nm, mut):
                x = list(ev); mut(x)
                try: EM.validate(x, word, ori, {}, zs)
                except (AssertionError, KeyError): return nm
                raise SystemExit('control accepted: ' + nm)
            c2 = []
            def m2(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 177) in e[2][1:3]); x.pop(j)
            c2.append(rej('drop_resynth_delivery', m2))
            def m3(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'climb' and e[2] == 177); e = x[j]; x[j] = e[:5] + (e[5] - 1,)
            c2.append(rej('resynth_climb_underpaid', m3))
            def m4(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'old_response'); e = x[j]; o = e[2]; x[j] = (e[0], e[1], o[:3] + (-o[3],), e[3])
            c2.append(rej('flip_precancellation', m4))
            print('     controls rejected:', c2)
    assert paid[(name, 'forward')] == paid[(name, 'backward')]

print('== E. banks (#401 patterns, re-implemented; unchanged by target re-synthesis)')
queues = {}
for rep in range(T):
    for r in range(2 * V, N): queues.setdefault(h - len(w['frames'][EXT[r]]) if r in EXT else h, []).append((rep, r))
queues = {k: deque(v) for k, v in queues.items()}; asg = {}; padding = []; bank = 0
for pat in pats:
    for _ in range(pat['count']):
        off = 0
        for key, num in sorted(((k, x) for k, x in pat.items() if k.startswith('r')), key=lambda z: -int(z[0][1:])):
            rk = int(key[1:])
            for _ in range(num): role = queues[rk].popleft(); asg[role] = (bank, list(range(off, off + rk))); off += rk
        assert off + pat['padding'] == m
        if off < m: padding.append((bank, list(range(off, m))))
        bank += 1
assert all(not q for q in queues.values()) and len(asg) == T * R and bank == 748
assert Counter(len(ax) for _, ax in padding) == Counter({1: 482, 10: 1})
print('   residual inventory per stage %s in %d width-73 banks; paddings %s (helpers only; targets carry no bank residual)'
      % (dict(sorted(Counter(len(ax) for ax in [a for _, a in asg.values()]).items())), bank, dict(Counter(len(ax) for _, ax in padding))))
print('== F. price')
IDLE = [16, 8, 32, 8, 48, 8, 48, 32, 16]
def profile(ph, nz):
    P = Counter({int(r): L * T * n for r, n in ph.items()})
    for r in IDLE: P[r] += 240 * T
    for _, ax in padding: P[len(ax)] += L
    P[1] -= L * T * nz; return P
live = 2 * 4 * V * T + L * bank
c = Q(r401['bit_coarse']); assert c == Q(255384852701747, 250000000000000000)
P0 = profile(paid[('#401 word', 'forward')], 0); assert live == 14412 and m * live - sum(r * n for r, n in P0.items()) == 2496
b0, _ = certify24(P0, m, live); assert b0 == Q(r401['complex_coarse'])
k0, _ = refine(b0, c); assert str(k0) == r401['kappa'] == '101331088745971/100000000000000000'
print('   control: #401 b = %s and kappa = %s = %.18f reproduced from our emission of its word under #390\'s bracket' % (b0, k0, float(k0)))
P1 = profile(paid[('ours', 'forward')], 0); mass = sum(r * n for r, n in P1.items())
assert m * live - mass == 2496 and max(P1) == 48 and m ** 2 > 2 * 48 ** 2
b, u = certify24(P1, m, live); k, rej = refine(b, c); assert c > b and k > k0
print('   ours: profile delta', {r: P1[r] - P0[r] for r in sorted(set(P1) | set(P0)) if P1[r] != P0[r]})
print('   b = %s = %.15e (+%.6e over #401); #401 bit c = %.15e > b: complex-bound' % (b, float(b), float(b - b0), float(c)))
print('   kappa = %s = %.18f (+%.6e over #401; six bootstrap levels, 47 strict constraints; rejected %s)' % (k, float(k), float(k - k0), rej))
json.dump(dict(b=str(b), b_upper=str(u), b_float=float(b), c=str(c), kappa=str(k), kappa_float=float(k), binding='complex',
               kappa_401=str(k0), b_401=str(b0), profile={str(r): n for r, n in sorted(P1.items())}, live=live, m=m, T=T,
               banks_per_stage=bank, local_paid=paid[('ours', 'forward')], resynthesised_targets=sorted(DES)),
          open(os.path.join(OD, 'kappa.json'), 'w'), indent=1)
