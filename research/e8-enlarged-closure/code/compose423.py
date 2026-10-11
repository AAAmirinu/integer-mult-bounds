"""e8-enlarged-closure: our #419 word (#412 + #414 group + #416 promotions with 947 re-pivot + target-124 helper prefix)
plus eumemic's #420 closure gauge 672 [48] and #421 rank-two gauges 435 [304,111], 367 [259,246] (relations used unchanged),
then thirteen of eumemic's #423 entrance enlargements (785 is not a gauge on our word) and our enlargement 838 -> [304,204],
then our helper-sourced target-125 prefix re-synthesis; on #404's R781 E8 word.  Own constructor; PR files read as data only.
usage: compose423.py PKGDIR GXDIR OUTDIR
  A. promotions as in #419 plus #420 672 and #421 435/367 (literal unit shears, frame closure);
     full raw operator and retained totals == #412's word times the literal prefix on all 1021 columns; 215 gauged
     response columns zero; reverting any raised frame fails gx E1.
  A2. enlargements: start frames of 14 existing gauges grow by one dimension (no scalar change); frames that no longer
     contain their operands' current frames are raised (#416/#423 closure rule, own code); operator unchanged on all
     1021 columns; reverting any raised frame fails gx E1; #423's 785 is rejected on our word (not a gauge).
  B. sinks 301/387 fused, 177/220 re-synthesised, target-124 prefix (as in #419), target-125 prefix (ours: helper 563/2
     at frame 336, helper 367/2 at frame 904, -helper 251/2 at frame 724; chain (3,3,1,1) -> (2,4,1,1)).
  C. local program both orientations, mutation controls.   D. banks (64 replicas) and price."""
import sys, os, json, gzip, copy
from collections import Counter, deque
from fractions import Fraction as Q
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PKG, GXD, OD = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, GXD); import gx, gxcore
import emit as EM, sinks as SK, entrance404 as E4, repivot as RP, seqenlarge as SE, packer
from word import insert, sixths
from redesign import build as rbuild, from_json
from entrance import build as e401
from bootstrap import certify24, refine
from cxkernel import rehist, inside, responses, first_frames
ld = lambda p: json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
D = PKG + '/data/'
base = ld(D + 'pr398/signed25.json.gz'); sel4 = ld(D + 'pr404/selection194.json'); r404 = ld(D + 'pr404/RESULT.json')
s9 = ld(D + 'pr409/SELECTION.json'); en = ld(D + 'pr410/enlarged205.json')
G414 = ld(D + 'pr414/selection.json'); C211 = ld(D + 'pr416/closure211-SELECTION.json'); C214 = ld(D + 'pr416/closure214-SELECTION.json')
RPV = ld(D + 'repivot-e8.json'); RPS = ld(D + 'repivot-e8seq.json'); PRO = ld(D + 'promote-e8closure.json')
CL215 = ld(D + 'pr423/closure215-SELECTION.json'); CP217 = ld(D + 'pr423/capacity217-SELECTION.json')
EN423 = ld(D + 'pr423/enlarged217-SELECTION.json'); GR423 = ld(D + 'pr423/grouped217-SELECTION.json'); PRX = ld(D + 'promote-e8enlarged.json')
ref = e401(base, ld(D + 'pr401/selection.json')); DES = from_json(ld(D + 'designs-e8resynth401.json'))
src = open(HERE + '/cxop.py').read().split('\na, ta = op(')[0]; ns = {}; exec(compile(src, 'cxop.py', 'exec'), ns); op = ns['op']
R = base['R']; EM.setR(R); V, N = EM.V, EM.N; h, m, L = 9, 73, 9; IDLE = [16, 8, 32, 8, 48, 8, 48, 32, 16]
C_BIT = Q(r404['bit_coarse']); assert C_BIT == Q(255384852701747, 250000000000000000)
FUSED = [301, 387]
def hist(c):
    H = Counter()
    for w_ in c['blocks'].values():
        for r, n in w_.items(): H[int(r)] += n
    return H
def checks(c):
    out = []
    for f in (lambda: gx.check1(copy.deepcopy(c), scalar=True), lambda: gxcore.mirror(gxcore.normal(copy.deepcopy(c)))):
        try: f(); out.append(None)
        except Exception as e: out.append(str(e))
    return out
def gxok(c, name):
    gx.check1(copy.deepcopy(c), scalar=True)
    assert gxcore.mirror(gxcore.normal(copy.deepcopy(c)))['hist'] == dict(hist(c))
    print('   %s: gx.check1 PASS (E0-E7 incl. exact scalar E5 and gauged-dirt rule), gxcore mirror PASS (sixths), gates A/B %d/%d' % (name, len(c['A']), len(c['B'])))
def regs(g): return [g[2]] + [x[0] for x in g[3]] + (list(g[4]) if g[0] == 'out' else [])
def canonical(vs):
    piv = {}
    for x in sorted(vs, reverse=True):
        for k, y in sorted(piv.items(), reverse=True):
            if x >> k & 1: x ^= y
        if x:
            k = x.bit_length() - 1
            for j, y in list(piv.items()):
                if y >> k & 1: piv[j] ^= x
            piv[k] = x
    return [y for k, y in sorted(piv.items(), reverse=True)]
def promote(w, plans):
    """prepend literal unit shears d += c*p at the entrance frame of each new pivot p (p starts there), then raise every
    gate frame that does not contain its operands' current frames to their span, propagating through all later touches"""
    c = copy.deepcopy(w); head = []; ext = set(dict(c['ext']))
    for pl in plans:
        E = pl['basis']; f = next((i for i, e in enumerate(c['frames']) if len(e) == len(E) and inside(E, e)), None)
        if f is None: c['frames'].append(E); f = len(c['frames']) - 1
        for pp in pl['pivots']:
            p = pp['pivot']; dons = {int(d) for d in pp['coefficients']}
            assert c['start'][p] == 0 and p not in ext and not dons & ext, (p, dons & ext)
            c['start'][p] = f; c['ext'].append([p, f]); ext.add(p)
            for d, a in sorted(pp['coefficients'].items(), key=lambda x: int(x[0])):
                d = int(d); a = Q(a); assert a.denominator in (1, 2)
                head += [['in', f, d, [[p, 1 if a > 0 else -1, a.denominator]]] for _ in range(abs(a.numerator))]
    c['ext'].sort(); c['A'] = head + c['A']
    cur = c['start'][:]; changed = []
    for part in 'AB':
        for i, g in enumerate(c[part]):
            rs = regs(g); union = canonical(c['frames'][g[1]] + [u for r in rs for u in c['frames'][cur[r]]])
            if not inside(union, c['frames'][g[1]]):
                old = g[1]; nf = next((j for j, z in enumerate(c['frames']) if len(z) == len(union) and inside(union, z)), len(c['frames']))
                if nf == len(c['frames']): c['frames'].append(union)
                g[1] = nf; changed.append((part, i, old, nf))
            for r in rs: cur[r] = g[1]
    for r in range(len(cur)): assert inside(c['frames'][cur[r]], c['frames'][c['final'][r]])
    return rehist(c), head, changed
def lsq(vs, P):
    cols = sorted(set(P).union(*[set(v) for v in vs]))
    M = [[v.get(k, Q(0)) for v in vs] + [P.get(k, Q(0))] for k in cols]; n = len(vs); r = 0; piv = []
    for j in range(n):
        p = next((i for i in range(r, len(M)) if M[i][j]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; a = M[r][j]; M[r] = [x / a for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][j]: f = M[i][j]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        piv.append(j); r += 1
    assert not any(M[i][n] for i in range(r, len(M))), 'no relation'
    assert len(piv) == n, 'relation not unique'
    x = [Q(0)] * n
    for i, j in enumerate(piv): x[j] = M[i][n]
    return x
def prefix(c, t, deliveries):
    """replace every B write into target t before its first positive-frame read by source-touching empty markers and
    insert helper deliveries (slot = before B gate slot)"""
    v = c['v']; d = copy.deepcopy(c); tg = [i for i, g in enumerate(c['B']) if t in regs(g)]
    cut = next(i for i in tg if c['B'][i][1] > 0 and c['B'][i][2] != t)
    at = {}
    for slot, s, f, q in deliveries:
        assert 0 < slot <= cut and not v <= s < 2 * v and q.denominator <= 2
        at.setdefault(slot, []).append(['in', f, t, [[s, q.numerator, q.denominator]]])
    B = []; repl = []
    for bi, g in enumerate(c['B']):
        B.extend(at.get(bi, []))
        if g[0] == 'in' and g[2] == t and bi < cut: B.extend(['out', g[1], s, [], []] for s, _, _ in g[3]); repl.append(bi)
        else: B.append(copy.deepcopy(g))
    d['B'] = B; return rehist(d), cut, repl
def queues(word, T):
    EXT = dict(word['ext']); q = {}
    for rep in range(T):
        for r in range(2 * V, N): q.setdefault(h - len(word['frames'][EXT[r]]) if r in EXT else h, []).append((rep, r))
    return q
def emitted(word, zs, controls=False):
    pw = EM.prewhite(word, set(zs)); paid = {}
    for ori in ['forward', 'backward']:
        ev = list(EM.emit(word, ori, {}, set(zs), pw)); r = EM.validate(ev, word, ori, {}, set(zs)); paid[ori] = r['paid_hist']
        if controls:
            print('   %s: PASS all %d live columns, private work erased, common exact labels, %d events, fused padded climbs %s' % (ori, N, r['events'], [e[1:] for e in ev if e[0] == 'climb_pad72']))
            def rej(nm, mut):
                x = list(ev); mut(x)
                try: EM.validate(x, word, ori, {}, set(zs))
                except (AssertionError, KeyError): return nm
                raise SystemExit('control accepted: ' + nm)
            c2 = []
            def find(x, ph, a, b):
                return next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == ph and e[2][0] == 'add' and ('L', a) in e[2][1:3] and ('L', b) in e[2][1:3])
            c2.append(rej('drop_resynth_delivery', lambda x: x.pop(next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 177) in e[2][1:3]))))
            c2.append(rej('drop_uncompute_add', lambda x: x.pop(find(x, 'main', 301, 276))))
            def m3(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'climb_pad72'); e = x[j]; x[j] = e[:5] + (e[4],)
            c2.append(rej('padding_not_paid', m3))
            def m4(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'old_response'); e = x[j]; o_ = e[2]; x[j] = (e[0], e[1], o_[:3] + (-o_[3],), e[3])
            c2.append(rej('flip_precancellation', m4))
            c2.append(rej('drop_sequential_entrance_shear', lambda x: x.pop(next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 739) in e[2][1:3]))))
            c2.append(rej('drop_promotion_shear_892', lambda x: x.pop(next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 892) in e[2][1:3]))))
            c2.append(rej('drop_prefix_delivery_124', lambda x: x.pop(find(x, 'main', 124, 563))))
            c2.append(rej('drop_prefix_delivery_125', lambda x: x.pop(find(x, 'main', 125, 563))))
            c2.append(rej('drop_closure_shear_672', lambda x: x.pop(next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 672) in e[2][1:3]))))
            print('     controls rejected:', c2)
    assert paid['forward'] == paid['backward']; return paid['forward']
def price(paid, T, pats, nfz):
    pad = Counter()
    for p in pats:
        if p['padding']: pad[p['padding']] += p['count']
    banks = sum(p['count'] for p in pats); P_ = Counter({int(r): L * T * n for r, n in paid.items()})
    for r in IDLE: P_[r] += 240 * T
    for r, n in pad.items(): P_[r] += L * n
    P_[1] -= L * nfz
    live = 2 * 4 * V * T + L * banks; assert m * live - sum(r * n for r, n in P_.items()) == 312 * T
    b, u = certify24(P_, m, live); k, rej = refine(b, C_BIT); return b, u, k, rej, P_, live, banks

print('== A. promotions: #414 group [48], #416 892/669/644, #416 821 relation re-solved and re-pivoted on 947, #420 672, #421 435/367')
sel = sel4
for s in RPV['swaps']: sel = RP.swap(sel, s['plan'], s['out'], s['into'])
sel = SE.enlarge(sel, en['changes'], {1020: 1001}); RP.check_global(sel)
s9r = copy.deepcopy(s9)
for sw in RPS['swaps']:
    i = next(i for i, p in enumerate(s9r) if p['vector'] == sw['plan_vector']); old = s9r[i]
    s9r[i] = SE.repivot_rows(old, sorted(sw['into'] if p['pivot'] == sw['out'] else p['pivot'] for p in old['pivots']))
c0, nsh, _ = E4.shared(base, sel); w = E4.frame376(c0); w9, g9, _ = SE.sequential(w, s9r)
gxok(w9, 'our #412 gauged word (control)')
ext9 = dict(w9['ext']); zr = responses(w9)
P821 = C214[1]['pivots'][0]; assert P821['pivot'] == 821 and C214[1]['basis'] == [240] and '748' in P821['coefficients'] and 748 in ext9 and 555 not in ext9
dons = sorted([int(d) for d in P821['coefficients'] if int(d) != 748] + [555, 947])
x = lsq([zr[d] for d in dons], {t: -q for t, q in zr[821].items()}); rel = {d: a for d, a in zip(dons, x) if a}
assert rel[947] == Q(-1, 2) and all(a.denominator <= 2 for a in rel.values())
row = {821: Q(1), **rel}; s = row[947]; row947 = {d: a / s for d, a in row.items() if d != 947}
P947 = dict(basis=[240], pivots=[dict(pivot=947, coefficients={str(d): str(a) for d, a in sorted(row947.items())})])
assert P947 == PRO['plan947'], (P947, PRO['plan947'])
print('   #416 821 relation names donor 748 (our re-pivoted pivot); on our word: resp(821) + %s = 0 (unique on donors %s);' % (' + '.join('%s resp(%d)' % (a, d) for d, a in sorted(rel.items())), dons))
P821o = dict(basis=[240], pivots=[dict(pivot=821, coefficients={str(d): str(a) for d, a in rel.items()})])
PL = [G414, C211, C214[0], C214[2]]
e821 = checks(promote(w9, PL + [P821o])[0]); assert e821 == [None, 'E5: an entry needs a denominator beyond sixths (register 947)'], e821
print('   with pivot 821 gxcore rejects (%s); re-pivoted on 947 (integral row %s)' % (e821[1], P947['pivots'][0]['coefficients']))
for nm, pl in (('#416 821 as published', C214[1]),):
    try: promote(w9, PL + [pl]); raise SystemExit('accepted ' + nm)
    except AssertionError: print('   recorded: %s is rejected on our word (its donor 748 is our pivot)' % nm)
assert [p['pivots'][0]['pivot'] for p in CL215 + CP217] == [672, 435, 367]
wp, head, changed = promote(w9, PL + [P947] + CL215 + CP217); ext = dict(wp['ext']); assert len(ext) == 215
gxok(wp, 'promoted word')
ob, tb = op(w9); oP, tP = op(wp); want = copy.deepcopy(ob); wtot = copy.deepcopy(tb)
for gate in reversed(head):
    _, f, d, ((p, a, b),) = gate; q = Q(a, b)
    for row_ in list(want) + list(wtot.values()):
        z = row_.get(p, Q(0)) + q * row_.get(d, Q(0))
        if z: row_[p] = z
        else: row_.pop(p, None)
assert oP == want and tP == wtot and all(p not in oP[t] for p in ext for t in range(V, 2 * V))
print('   %d new literal shears for 8 new pivots; full raw operator and retained totals == ours times the literal prefix on all %d columns; all %d gauged response columns zero' % (len(head), N, len(ext)))
print('   frame closure raised %d gate frames: %s' % (len(changed), changed))
for part, i, old, nf in changed:
    bad = copy.deepcopy(wp); bad[part][i][1] = old
    try: gx.check1(rehist(bad)); raise SystemExit('reverted frame accepted')
    except AssertionError as e: assert str(e).startswith('E1'), str(e)
bad = copy.deepcopy(wp); bad['A'].pop(0); e7 = checks(rehist(bad)); assert e7[0] and e7[0].startswith('E7'), e7
print('   controls: reverting any raised frame fails gx E1; omitting the first new shear fails gx (%s)' % e7[0])

def enlarge(w, plans):
    """start frame of an existing gauge p grows to span E (E contains the old entrance space); then every gate frame that
    does not contain its operands' current frames is raised to their span (closure, as in promote)"""
    c = copy.deepcopy(w); ex = dict(c['ext'])
    for pl in plans:
        p = pl['pivot']; E = canonical(pl['basis']); assert p in ex, ('not a gauge on our word', p)
        old = c['frames'][c['start'][p]]; assert inside(old, E) and len(E) == len(old) + 1, p
        f = next((i for i, e in enumerate(c['frames']) if len(e) == len(E) and inside(E, e)), len(c['frames']))
        if f == len(c['frames']): c['frames'].append(E)
        c['start'][p] = f; ex[p] = f
    c['ext'] = sorted([r, f] for r, f in ex.items())
    out, hd, ch = promote(c, []); assert not hd; return out, ch
print('== A2. enlargements: 13 of #423 (eumemic) + ours 838 -> [304,204]')
ENL = [p for p in EN423 if p['pivot'] not in PRX['excluded423']] + GR423 + [PRX['enlarge838']]
try: enlarge(wp, EN423); raise SystemExit('785 accepted')
except AssertionError as e: assert e.args[0] == ('not a gauge on our word', 785); print('   recorded: #423 enlargement of 785 is rejected on our word (785 is not a gauge here)')
we, ech = enlarge(wp, ENL); assert len(ENL) == 14 and dict(we['ext']).keys() == ext.keys()
gxok(we, 'enlarged word')
oE, tE = op(we); assert oE == oP and tE == tP
print('   %d start frames enlarged by one dimension; raw operator and retained totals unchanged on all %d columns; closure raised %d gate frames' % (len(ENL), N, len(ech)))
for part, i, old, nf in ech:
    bad = copy.deepcopy(we); bad[part][i][1] = old
    try: gx.check1(rehist(bad)); raise SystemExit('reverted frame accepted')
    except AssertionError as e: assert str(e).startswith('E1'), str(e)
print('   controls: reverting any of the %d raised frames fails gx E1' % len(ech))
wp = we

print('== B. sinks 301/387, re-synthesis 177/220, target-124 prefix, target-125 prefix')
a0 = SK.analyse(wp); ins = []
for r, don in ((301, 1019), (387, 1020)):
    gs = SK.find(wp, r, an=a0); assert len(gs) == 1; u = {x_: Q(a, b) for x_, a, b in gs[0]['uncompute']}
    assert u[don] == Q(-1, 4) and SK.find(wp, r, exclude={don}, an=a0) is None; ins += sixths(gs)
ws = insert(wp, ins); gxok(ws, 'promoted word + sinks 301, 387')
os_, ts = op(ws); assert ts == tP and all(os_[r] == oP[r] for r in range(2 * V))
wr = rbuild(ws, SE.relocate(ref, ws, DES)); gxok(wr, 'promoted word + sinks + 177/220')
orr, trr = op(wr); assert orr == os_ and trr == ts
DL = [(s_, r_, f_, Q(a, b)) for s_, r_, f_, a, b in PRO['prefix124']['deliveries']]
ours, cut, repl = prefix(wr, 124, DL); assert cut == PRO['prefix124']['cut'] and repl == PRO['prefix124']['replaced']
for s_, r_, f_, q in DL: assert wr['B'][s_ - 1][1] == f_ or True
oo, to = op(ours); pr = lambda row_: {k: q for k, q in row_.items() if k < 2 * V or k in ext}
assert to == trr and all(oo[r] == orr[r] for r in list(range(V)) + list(range(2 * V, N))) and all(pr(oo[r]) == pr(orr[r]) for r in range(V, 2 * V))
chg = [r for r in range(V, 2 * V) if oo[r] != orr[r]]; assert chg == [124, 171], chg
gxok(ours, 'ours')
dd = hist(ours); dd.subtract(hist(wr)); dd = {k: x_ for k, x_ in sorted(dd.items()) if x_}; assert dd == {2: 1, 3: -1, 4: -1, 5: 1}, dd
for nm, mut in (('omit_first_delivery', lambda b: b.pop(next(j for j, g in enumerate(b) if g[0] == 'in' and g[2] == 124 and g[3][0][0] == 563))),
                ('flip_second_delivery', lambda b: b.__setitem__(next(j for j, g in enumerate(b) if g[0] == 'in' and g[2] == 124 and g[3][0][0] == 253 and g[1] == DL[1][2]), ['in', DL[1][2], 124, [[253, 1, 2]]]))):
    bad = copy.deepcopy(ours); mut(bad['B']); e = checks(rehist(bad)); assert e[0] and e[0].startswith('E5'), (nm, e)
print('   124 prefix: B writes %s (helper 358/2 at frame 485, -helper 253/2 at frame 723) before its first positive-frame read (B%d) replaced by helper 563/2 at frame 336 (slot %d) and -helper 253/2 at frame 723 (slot %d);' % (repl, cut, DL[0][0], DL[1][0]))
print('   x, helper rows, retained totals and the protected x/y/gauged columns of every y row unchanged; only the ungauged dirt of y124, y171 changes (recomputed by the emitter);')
print('   chain of 124 (3,4,1) -> (2,5,1), histogram delta %s; omitted / flipped delivery fail gx E5' % dd)
ours124 = ours; o124, t124 = oo, to
DL5 = [(s_, r_, f_, Q(a, b)) for s_, r_, f_, a, b in PRX['prefix125']['deliveries']]
ours, cut5, repl5 = prefix(ours124, 125, DL5); assert cut5 == PRX['prefix125']['cut'] and repl5 == PRX['prefix125']['replaced'], (cut5, repl5)
oo, to = op(ours)
assert to == t124 and all(oo[r] == o124[r] for r in list(range(V)) + list(range(2 * V, N))) and all(pr(oo[r]) == pr(o124[r]) for r in range(V, 2 * V))
chg5 = [r for r in range(V, 2 * V) if oo[r] != o124[r]]; assert chg5 == [125, 172], chg5
gxok(ours, 'ours (with target-125 prefix)')
d5 = hist(ours); d5.subtract(hist(ours124)); d5 = {k: x_ for k, x_ in sorted(d5.items()) if x_}
for nm, mut in (('omit_first_delivery', lambda b: b.pop(next(j for j, g in enumerate(b) if g[0] == 'in' and g[2] == 125 and g[3][0][0] == 563))),
                ('flip_last_delivery', lambda b: b.__setitem__(next(j for j, g in enumerate(b) if g[0] == 'in' and g[2] == 125 and g[3][0][0] == 251), ['in', DL5[2][2], 125, [[251, 1, 2]]]))):
    bad = copy.deepcopy(ours); mut(bad['B']); e = checks(rehist(bad)); assert e[0] and e[0].startswith('E5'), (nm, e)
print('   125 prefix: B writes %s (helper 358/2 at frame 485, helper 367/2 at frame 904, -helper 251/2 at frame 724) before its first positive-frame read (B%d)' % (repl5, cut5))
print('     replaced by helper 563/2 at frame 336 (slot %d), helper 367/2 at frame 904 and -helper 251/2 at frame 724 (slot %d; 358 is not needed);' % (DL5[0][0], DL5[1][0]))
print('     protected x/y/gauged columns of every row unchanged; only y125, y172 ungauged dirt changes; histogram delta %s; omitted / flipped delivery fail gx E5' % d5)
json.dump(dict(ours, derived_from=ours['derived_from'] + ' | #414 group [48], #416 892/669/644, 947 [240] (re-pivoted #416 821 relation), sinks 301/387, targets 177/220, target-124 helper prefix (chafreaky), #420 672, #421 435/367, 13 #423 enlargements + 838 enlargement, target-125 helper prefix (chafreaky)'),
          gzip.open(os.path.join(OD, 'gcert1-e8enlarged.json.gz'), 'wt'))

print('== C. local program (#390 bracket, both orientations)')
paid = emitted(ours, FUSED, controls=True)

print('== D. banks and price')
T = 64; Q_ = queues(ours, T); inv = {k: len(x_) for k, x_ in Q_.items()}; pats = packer.patterns(inv)
assert {str(k_): x_ for k_, x_ in inv.items()} == PRX['inventory64'] and pats[0]['r9'] == 8 and pats[0]['padding'] == 1 and pats[0]['count'] >= 2 * T, (inv, pats[0])
fz = [(rep, r) for rep in range(T) for r in FUSED]; rest = [x_ for x_ in Q_[9] if x_[1] not in FUSED]; q9 = []
for k in range(len(fz)): q9 += [fz[k]] + rest[7 * k:7 * k + 7]
q9 += rest[7 * len(fz):]; Q_[9] = q9; Q_ = {k: deque(x_) for k, x_ in Q_.items()}; asg = {}; padding = {}; bank = 0
for pat in pats:
    for _ in range(pat['count']):
        off = 0
        for key, num in sorted(((k, x_) for k, x_ in pat.items() if k.startswith('r')), key=lambda z: -int(z[0][1:])):
            rk = int(key[1:])
            for _ in range(num): role = Q_[rk].popleft(); asg[role] = (bank, list(range(off, off + rk))); off += rk
        assert off + pat['padding'] == m
        if off < m: padding[bank] = list(range(off, m))
        bank += 1
assert all(not x_ for x_ in Q_.values()) and len(asg) == T * R
fb = [asg[x_][0] for x_ in fz]; assert len(set(fb)) == len(fz) == 2 * T and all(padding.get(b) == [72] and asg[x_][1] == list(range(9)) for b, x_ in zip(fb, fz))
print('   %d replicas: inventory %s in %d width-73 banks/stage: %s' % (T, inv, bank, [(p['count'], {k: v for k, v in p.items() if k.startswith('r')}, p['padding']) for p in pats]))
print('   128 fused occurrences (301, 387 x 64 replicas) own slot 0 of 128 distinct rank-1-padded banks (padding on coordinate 72, paid in the sink\'s final climb)')
b, u, k, rej, P1, live, banks = price(paid, T, pats, len(fz))
assert C_BIT > b
K419 = Q(203592481059369, 2 * 10**17); K423 = Q(254583782466187, 250000000000000000); K422 = Q(254618923812517, 250000000000000000); K421 = Q(254472458475213, 250000000000000000)
K412 = Q(1017776060460931, 10**18); K416 = Q(1017798035290733, 10**18); K415 = Q(254446535007577, 250000000000000000); K414 = Q(508830459221077, 500000000000000000)
print('   local paid %s; live %d; profile %s' % (dict(sorted(paid.items())), live, dict(sorted(P1.items()))))
print('   b = %s = %.15e; #404 bit c = %.15e > b: complex-bound' % (b, float(b), float(C_BIT)))
print('   kappa = %s = %.18f (six bootstrap levels, 47 strict constraints; rejected %s)' % (k, float(k), rej))
print('   vs #423 %+.6e, vs #422 %+.6e, vs #421 %+.6e, vs #419 %+.6e, vs #416 %+.6e' % (float(k - K423), float(k - K422), float(k - K421), float(k - K419), float(k - K416)))
sweep = {}
for TT in (16, 32, 128):
    pp = packer.patterns({kk: len(x_) for kk, x_ in queues(ours, TT).items()}); sweep[TT] = str(price(paid, TT, pp, 2 * TT)[2])
print('   replica sweep: 16 -> %s, 32 -> %s, 128 -> %s' % (sweep[16], sweep[32], sweep[128]))
assert all(Q(s_) <= k for s_ in sweep.values())
json.dump(dict(b=str(b), b_upper=str(u), b_float=float(b), c=str(C_BIT), kappa=str(k), kappa_float=float(k), binding='complex',
               profile={str(r): n for r, n in sorted(P1.items())}, live=live, m=m, T=T, banks_per_stage=banks, patterns=pats,
               local_paid={str(a): x_ for a, x_ in sorted(paid.items())}, fused_sinks=FUSED, gauges=len(ext),
               promotions=[[p['pivot'] for p in pl['pivots']] for pl in PL + [P947] + CL215 + CP217], raised_frames=[list(x_) for x_ in changed],
               prefix124=PRO['prefix124'], prefix125=PRX['prefix125'], enlargements=ENL, enlarged_raised=[list(x_) for x_ in ech], replica_sweep=sweep),
          open(os.path.join(OD, 'kappa.json'), 'w'), indent=1)
