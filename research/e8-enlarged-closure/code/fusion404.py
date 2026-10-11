"""e8-repivot-fusion: response-gauge re-pivoting, two fused zero-row sinks and two exact target re-syntheses on
Dugongue's #404 shared-donor R781 E8 complex program, compiled with #390's dirty-preconditioned bracket.
usage: fusion404.py PKGDIR GXDIR OUTDIR [--regen]
  A. #404's word, own re-implementation (shared-donor gauges, 124/125 recovery, #376 frame edit): both frozen #404
     hashes reproduced; #404's b and kappa reproduced from OUR emission of its word (control).  Recorded: Sussman's
     checkers reject #404's word (gxcore E5 sixths at register 947 from pivot 555's half dirt; E4 at target 125).
  B. our base: #404's gauges with four exact re-pivotings (data/repivot-e8.json); each keeps its plan's relation span,
     so the raw operator is #398's * diag(I, I, S') with all 194 pivot response columns zero; #376 edit kept; the
     124/125 recovery is not used (it violates gx E4).  gx.check1 + gxcore PASS.
  C. sinks 301 and 387 fused (unique quarter of 1019/1020, now +-2-coefficient donors: sixths hold); 324 rejected
     (quarter of 1018, the single donor of pivot 941).  (--regen) the free-sink scan finds exactly 301/324/387, and the
     sink-isolation premise a_G = b_G = 0 (b = A^-1 e_s) holds for 301 and 387 on our gauges.
  D. target re-synthesis of 177 and 220 (exact; (--regen) discovery regenerates exactly them); full raw operator
     identical to the sinked base.
  E. local program, both orientations, all 1021 live columns, for #404's word (control) and ours; mutation controls.
  F. banks: #404's patterns (738 width-73 banks, 394 rank-1 paddings); the 16 fused occurrences own slot 0 of 16
     distinct rank-1-padded banks, padding on coordinate 72.
  G. price: #404 control, then ours (both PR #315 engines, 10^-16 fallback, six bootstrap levels).  Bit side: #404's
     pinned bit coarse bound (c > b: complex-bound)."""
import sys, os, json, gzip, copy
from collections import Counter, deque
from fractions import Fraction as Q
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PKG, GXD, OD = sys.argv[1], sys.argv[2], sys.argv[3]; REGEN = '--regen' in sys.argv
sys.path.insert(0, GXD); import gx, gxcore
import emit as EM
import sinks as SK
import entrance404 as E4
import repivot as RP
from word import insert, origmap, sixths
from redesign import build, from_json
from search import Search
from bootstrap import certify24, refine
ld = lambda p: json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
base = ld(PKG + '/data/pr398/signed25.json.gz'); sel4 = ld(PKG + '/data/pr404/selection194.json')
pats = ld(PKG + '/data/pr404/bank-patterns.json'); r404 = ld(PKG + '/data/pr404/RESULT.json')
RPV = ld(PKG + '/data/repivot-e8.json'); ZS = ld(PKG + '/data/sinks-e8repivot.json'); DES = from_json(ld(PKG + '/data/designs-e8repivot.json'))
src = open(HERE + '/cxop.py').read().split('\na, ta = op(')[0]; ns = {}; exec(compile(src, 'cxop.py', 'exec'), ns); op = ns['op']
R = base['R']; EM.setR(R); V, N = EM.V, EM.N; h, m, T, L = 9, 73, 8, 9
FUSED = sorted({s['sink_helper'] for s in ZS}); assert FUSED == [301, 387] and sorted(DES) == [177, 220]

def hist(c):
    H = Counter()
    for w_ in c['blocks'].values():
        for r, n in w_.items(): H[int(r)] += n
    return H
def gxok(c, name):
    gx.check1(copy.deepcopy(c), scalar=True)
    assert gxcore.mirror(gxcore.normal(copy.deepcopy(c)))['hist'] == dict(hist(c))
    print('   %s: gx.check1 PASS (E0-E7 incl. exact scalar E5 and gauged-dirt rule), gxcore mirror PASS (sixths), gates A/B %d/%d' % (name, len(c['A']), len(c['B'])))
def gxfail(c):
    for f in (lambda: gx.check1(copy.deepcopy(c), scalar=True), lambda: gxcore.mirror(gxcore.normal(copy.deepcopy(c)))):
        try: f()
        except Exception as e: return str(e)
    return None

print('== A. #404 word (own re-implementation, #404 read as data)')
w4, info = E4.build(base, sel4)
assert info['unit'] == 484 and info['dual_sha'] == E4.DUAL_SHA and info['final_sha'] == E4.FINAL_SHA == r404['candidate_sha256']
print('   194 shared-donor gauges (484 unit shears), 124/125 recovery and #376 frame edit: both frozen #404 hashes reproduced (65b0f9dd..., d18ccdc5...)')
c4s, _, _ = E4.shared(base, sel4)
e1 = gxfail(c4s); e2 = gxfail(w4)
assert e1 == 'E5: an entry needs a denominator beyond sixths (register 947)' and e2 == 'E4: a pivot is the target of a gate reading y', (e1, e2)
print('   recorded: Sussman\'s checkers reject #404\'s gauges (%s) and its 124/125 recovery (%s)' % (e1, e2))

print('== B. our base: #404 gauges with four exact re-pivotings, #376 edit, no 124/125 recovery')
sel = sel4
for s in RPV['swaps']:
    new = RP.swap(sel, s['plan'], s['out'], s['into'])
    a, b = RP.rows(sel['plans'][s['plan']]), RP.rows(new['plans'][s['plan']])
    cols = sorted({k for r in a.values() for k in r} | {k for r in b.values() for k in r})
    def rank(rows):
        M = [[r.get(k, Q(0)) for k in cols] for r in rows]; rk = 0
        for j in range(len(cols)):
            p = next((i for i in range(rk, len(M)) if M[i][j]), None)
            if p is None: continue
            M[rk], M[p] = M[p], M[rk]
            for i in range(len(M)):
                if i != rk and M[i][j]: f = M[i][j] / M[rk][j]; M[i] = [x - f * y for x, y in zip(M[i], M[rk])]
            rk += 1
        return rk
    assert rank(list(a.values())) == rank(list(b.values())) == rank(list(a.values()) + list(b.values())) == len(a)
    sel = new
    print('   plan %d: pivot %d -> %d (same relation span, %d relations): %s' % (s['plan'], s['out'], s['into'], len(a), s['why']))
RP.check_global(sel)
c0, nsh, seln = E4.shared(base, sel); w = E4.frame376(c0); piv = {p for p, _ in w['ext']}
assert nsh == 500 and len(piv) == 194
gxok(w, 'our base')
ob, tb = op(base); ow, tw = op(w)
for r in range(N):
    want = dict(ob[r])
    for _, p, cm in seln:
        z = want.get(p, 0) + sum(a * ob[r].get(d, 0) for d, a in cm.items())
        if z: want[p] = z
        else: want.pop(p, None)
    assert want == ow[r], r
assert all(p not in ow[t] for p in piv for t in range(V, 2 * V))
o4, t4 = op(w4); xy = lambda row: {k: q for k, q in row.items() if k < 2 * V}
assert all(xy(o4[r]) == xy(ow[r]) for r in range(2 * V))
d = hist(w); d.subtract(hist(w4)); d = {k: x for k, x in sorted(d.items()) if x}
print('   raw operator == #398\'s * diag(I, I, S\') on all %d columns; all 194 pivot response columns zero; x/y rows == #404\'s word;' % N)
print('   %d unit shears (denominators 1, 2); paid histogram vs #404\'s word %s (the omitted 124/125 recovery)' % (nsh, d))

print('== C. free sinks')
a0 = SK.analyse(w)
if REGEN:
    hits = {r: SK.find(w, r, an=a0) for r in range(2 * V, N) if a0[5][r] > 0}; hits = {r: g for r, g in hits.items() if g}
    assert sorted(hits) == [301, 324, 387]
    print('   free-sink scan over all %d lifting helpers of our base: exactly 301, 324, 387' % sum(1 for r in range(2 * V, N) if a0[5][r] > 0))
q = {}
for r, don in ((301, 1019), (324, 1018), (387, 1020)):
    gs = SK.find(w, r, an=a0); assert len(gs) == 1; u = {x: Q(a, b) for x, a, b in gs[0]['uncompute']}; q[r] = u
    assert u[don] == Q(-1, 4) and SK.find(w, r, exclude={don}, an=a0) is None
    if r != 324: assert SK.find_adv(w, r, exclude={don}, an=a0) == (None, None)
dirt = {}
for _, p, cm in seln:
    for dd, a in cm.items(): dirt.setdefault(dd, {})[p] = a
assert all(x.denominator == 1 and x.numerator % 2 == 0 for x in dirt[1019].values()) and all(x.denominator == 1 and x.numerator % 2 == 0 for x in dirt[1020].values())
assert 1018 not in piv and dirt[1018] == {941: 1} and [cm for _, p, cm in seln if p == 941] == [{1018: Q(1)}]
print('   each same-frame sink needs exactly -1/4 of one helper (none without it; for 301/387 none even with advanced donors): 301 <- 1019, 324 <- 1018, 387 <- 1020')
print('   1019/1020 are now donors with entrance coefficients %s / %s (even): a quarter of their gauged dirt stays in sixths' % (sorted(map(str, dirt[1019].values())), sorted(map(str, dirt[1020].values()))))
print('   324 not fused: 1018 is the only donor of pivot 941 (relation e941 + e1018), so 1/4 of 941\'s unit dirt reaches 324 (gxcore E5)')
bad = insert(w, ZS + sixths(SK.find(w, 324, an=a0))); e3 = gxfail(bad); assert e3 == 'E5: an entry needs a denominator beyond sixths (register 324)', e3
ws = insert(w, ZS); gxok(ws, 'base + sinks 301, 387')
d = hist(ws); d.subtract(hist(w)); assert not any(d.values())
an = SK.analyse(ws); assert all(not an[7][r] for r in FUSED)
os_, ts = op(ws); assert ts == tw and all(os_[r] == ow[r] for r in range(2 * V))
print('   sinks: clean x-rows of 301 and 387 zero; paid histogram unchanged; x/y rows and retained totals unchanged; 324 control rejected')
if REGEN:
    o = ow; H_ = list(range(2 * V, N)); ix = {r: i for i, r in enumerate(H_)}; n = len(H_)
    M = [[Q(0)] * n + [Q(int(H_[i] == s)) for s in FUSED] for i in range(n)]
    for r in H_:
        for c_, x in o[r].items():
            if c_ >= 2 * V: M[ix[r]][ix[c_]] = x
    oa = ow
    assert all(not any(c_ in piv for c_ in oa[s] if c_ >= 2 * V) for s in FUSED)
    for col in range(n):
        p = next(i for i in range(col, n) if M[i][col]); M[col], M[p] = M[p], M[col]; pv = M[col][col]
        if pv != 1: M[col] = [x / pv for x in M[col]]
        rc = M[col]; nz = [j for j, x in enumerate(rc) if x]
        for i in range(n):
            if i != col and M[i][col]:
                f = M[i][col]; ri = M[i]
                for j in nz: ri[j] -= f * rc[j]
    for k, s in enumerate(FUSED):
        bcol = {H_[i]: M[i][n + k] for i in range(n) if M[i][n + k]}
        assert bcol[s] == Q(1, 2) and not set(bcol) & piv
    print('   sink isolation (#404 notes\' one-sink constructor premise): a_G = b_G = 0 for 301 and 387 under our 194 gauges, b_s = 1/2')

print('== D. target re-synthesis (177, 220)')
ours = build(ws, DES); gxok(ours, 'ours')
oo, to = op(ours); assert oo == os_ and to == ts
SW = Search(ws, gauged=piv); SO = Search(ours, gauged=piv)
walks = {i: (SW.walk(i), SO.walk(i)) for i in sorted(DES)}
assert walks == {177: ((3, 5), (6, 2)), 220: ((3, 5), (6, 2))} and all(SO.walk(i) == SW.walk(i) for i in range(V, 2 * V) if i not in DES)
dd = hist(ours); dd.subtract(hist(ws)); dd = {k: x for k, x in sorted(dd.items()) if x}; assert dd == {2: 2, 3: -2, 5: -2, 6: 2}, dd
print('   full raw operator (all 1021 columns, incl. every helper-dirt column) and retained totals IDENTICAL to the sinked base; walks', walks, 'histogram delta', dd)
if REGEN:
    D5, rep = SW.discover(); assert D5 == DES
    print('   regeneration: exact discovery over all %d targets regenerates exactly 177 and 220 (%d improvable, %d blocked by existing restores)'
          % (V, len(rep), sum(e['read_by_existing_gate'] for e in rep.values())))
json.dump(dict(ours, derived_from=ours['derived_from'] + ' | #404 shared-donor gauges (Dugongue) re-pivoted, #376 frame edit, sinks 301/387, targets 177/220 re-synthesised (chafreaky)'),
          gzip.open(os.path.join(OD, 'gcert1-e8repivot404.json.gz'), 'wt'))

print('== E. local program (#390 bracket, both orientations)')
paid = {}
for name, word, zs in [('#404 word', w4, set()), ('ours', ours, set(FUSED))]:
    pw = EM.prewhite(word, zs)
    for ori in ['forward', 'backward']:
        ev = list(EM.emit(word, ori, {}, zs, pw)); r = EM.validate(ev, word, ori, {}, zs); paid[(name, ori)] = r['paid_hist']
        print('   %s %s: PASS all %d live columns, private work erased, common exact labels, %d events%s' % (name, ori, N, r['events'],
              ', fused padded climbs %s' % [e[1:] for e in ev if e[0] == 'climb_pad72'] if zs else ''))
        if name == 'ours':
            def rej(nm, mut):
                x = list(ev); mut(x)
                try: EM.validate(x, word, ori, {}, zs)
                except (AssertionError, KeyError): return nm
                raise SystemExit('control accepted: ' + nm)
            c2 = []
            def m1(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 177) in e[2][1:3]); x.pop(j)
            c2.append(rej('drop_resynth_delivery', m1))
            def m2(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 301) in e[2][1:3] and ('L', 276) in e[2][1:3]); x.pop(j)
            c2.append(rej('drop_uncompute_add', m2))
            def m3(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'climb_pad72'); e = x[j]; x[j] = e[:5] + (e[4],)
            c2.append(rej('padding_not_paid', m3))
            def m4(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'old_response'); e = x[j]; o_ = e[2]; x[j] = (e[0], e[1], o_[:3] + (-o_[3],), e[3])
            c2.append(rej('flip_precancellation', m4))
            print('     controls rejected:', c2)
    assert paid[(name, 'forward')] == paid[(name, 'backward')]

print('== F. banks (#404 patterns, fused occurrences on rank-1-padded banks)')
EXT = dict(w['ext']); queues = {}
for rep in range(T):
    for r in range(2 * V, N): queues.setdefault(h - len(w['frames'][EXT[r]]) if r in EXT else h, []).append((rep, r))
assert {k: len(x) for k, x in queues.items()} == {4: 120, 5: 216, 7: 72, 8: 1144, 9: 4696}
fz = [(rep, r) for rep in range(T) for r in FUSED]; rest = [x for x in queues[9] if x[1] not in FUSED]
assert pats[0] == {'count': 394, 'r9': 8, 'padding': 1}
q9 = []
for k in range(len(fz)): q9 += [fz[k]] + rest[7 * k:7 * k + 7]
q9 += rest[7 * len(fz):]; queues[9] = q9
queues = {k: deque(x) for k, x in queues.items()}; asg = {}; padding = {}; bank = 0
for pat in pats:
    for _ in range(pat['count']):
        off = 0
        for key, num in sorted(((k, x) for k, x in pat.items() if k.startswith('r')), key=lambda z: -int(z[0][1:])):
            rk = int(key[1:])
            for _ in range(num): role = queues[rk].popleft(); asg[role] = (bank, list(range(off, off + rk))); off += rk
        assert off + pat['padding'] == m
        if off < m: padding[bank] = list(range(off, m))
        bank += 1
assert all(not x for x in queues.values()) and len(asg) == T * R and bank == 738
assert Counter(len(x) for x in padding.values()) == Counter({1: 394})
fb = [asg[x][0] for x in fz]
assert len(set(fb)) == len(fz) == 16 and all(padding.get(b) == [72] and asg[x][1] == list(range(9)) for b, x in zip(fb, fz))
print('   738 banks/stage, 394 rank-1 paddings (coordinate 72); 16 fused occurrences (301, 387 x 8 replicas) own slot 0 of 16 distinct padded banks %s;'
      % sorted(fb))
print('   paddings per stage 394 -> %d (each fused padding is paid inside the sink\'s final climb, validated above)' % (394 - len(fz)))

print('== G. price')
IDLE = [16, 8, 32, 8, 48, 8, 48, 32, 16]
def profile(ph, nz):
    P = Counter({int(r): L * T * n for r, n in ph.items()})
    for r in IDLE: P[r] += 240 * T
    P[1] += L * 394 - L * T * nz; return P
live = 2 * 4 * V * T + L * bank; assert live == 14322
c = Q(r404['bit_coarse']); assert c == Q(255384852701747, 250000000000000000)
P0 = profile(paid[('#404 word', 'forward')], 0); assert m * live - sum(r * n for r, n in P0.items()) == 2496
b0, _ = certify24(P0, m, live); assert str(b0) == r404['complex_coarse']
k0, _ = refine(b0, c); assert str(k0) == r404['kappa'] == '1016422320428301/1000000000000000000'
print('   control: #404 b = %s and kappa = %s = %.18f reproduced from our emission of its word under #390\'s bracket' % (b0, k0, float(k0)))
P1 = profile(paid[('ours', 'forward')], len(FUSED)); mass = sum(r * n for r, n in P1.items())
assert m * live - mass == 2496 and max(P1) == 48 and m ** 2 > 2 * 48 ** 2
b, u = certify24(P1, m, live); k, rej = refine(b, c); assert c > b and k > k0
print('   ours: profile delta', {r: P1[r] - P0[r] for r in sorted(set(P1) | set(P0)) if P1[r] != P0[r]})
print('   b = %s = %.15e (+%.6e over #404); #404 bit c = %.15e > b: complex-bound' % (b, float(b), float(b - b0), float(c)))
print('   kappa = %s = %.18f (+%.6e over #404; six bootstrap levels, 47 strict constraints; rejected %s)' % (k, float(k), float(k - k0), rej))
json.dump(dict(b=str(b), b_upper=str(u), b_float=float(b), c=str(c), kappa=str(k), kappa_float=float(k), binding='complex',
               kappa_404=str(k0), b_404=str(b0), profile={str(r): n for r, n in sorted(P1.items())}, live=live, m=m, T=T,
               banks_per_stage=bank, local_paid=paid[('ours', 'forward')], fused_sinks=FUSED, resynthesised_targets=sorted(DES),
               repivots=[[s['plan'], s['out'], s['into']] for s in RPV['swaps']]),
          open(os.path.join(OD, 'kappa.json'), 'w'), indent=1)
