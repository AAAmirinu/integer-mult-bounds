"""e8-r779-retimed-closure: our #424 layers re-implemented on ai-nanachi's #426 R779 gauged word (#426 read as data),
plus fixed-scalar gate-frame retimings (rediscovered by our own search; the same bases as eumemic's #427/#428) and a new
target-172 prefix; on the R779 E8 complex program.  Own constructor.
usage: compose426.py PKGDIR GXDIR OUTDIR [--regen]
  A. #426's gauged R779 word (202 gauges; pinned blob): gx.check1 + gxcore pass; every gauged response column zero;
     control: OUR emission + price at #426's 8 replicas and bank patterns reproduce #426's complex coefficient and
     kappa exactly.
  B. our #424 promotions mapped to R779 (helper ids r >= 240 -> r - #{556, 577 below r}): #414 group, #416 three
     closure promotions + our 947 re-pivot, #420 672, #421 435/367 (11 new pivots, 213 gauges); literal unit shears with
     frame closure; full raw operator == #426's word times the literal prefix; all gauged response columns zero;
     reverting any raised frame fails gx E1.
  C. the 14 enlargements of #424 (13 of eumemic's #423 + our 838), mapped; operator unchanged on all 1019 columns.
  D. sinks 301/387 fused (unique free sinks, quarter donors 1017/1018 as in #407), #402's 177/220 re-synthesis
     relocated (restore source y221: #426's signed layer makes y180 a pivot of a y read, so y180 cannot be a restore
     source under gx E4), our target-124 prefix, 14 fixed-scalar gate-frame retimings (12 single gates, 2 blocks),
     our target-172 prefix.  Each step: gx.check1 + gxcore; x / helper rows and retained totals unchanged; only the
     ungauged dirt of the touched y rows changes.  (--regen) our retiming search on the post-124 word finds these 14;
     every other candidate (and every candidate on the final word) is rejected by gx/gxcore or the emitter.
  E. local program both orientations with mutation controls; banks (64 replicas); price; replica sweep."""
import sys, os, json, gzip, copy
from collections import Counter, deque
from fractions import Fraction as Q
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PKG, GXD, OD = sys.argv[1], sys.argv[2], sys.argv[3]; REGEN = '--regen' in sys.argv
sys.path.insert(0, GXD); import gx, gxcore
import emit as EM, sinks as SK, packer
from word import insert, sixths
from redesign import build as rbuild, from_json
from bootstrap import certify24, refine
from cxkernel import rehist, inside, responses
ld = lambda p: json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
D = PKG + '/data/'
G426 = ld(D + 'pr426/gauged-candidate.json.gz'); X426 = ld(D + 'pr426/EXPECTED.json'); PAT426 = ld(D + 'pr426/bank-patterns.json')
r404 = ld(D + 'pr404/RESULT.json'); G414 = ld(D + 'pr414/selection.json'); C211 = ld(D + 'pr416/closure211-SELECTION.json')
C214 = ld(D + 'pr416/closure214-SELECTION.json'); PRO = ld(D + 'promote-e8closure.json'); PRX = ld(D + 'promote-e8enlarged.json')
CL215 = ld(D + 'pr423/closure215-SELECTION.json'); CP217 = ld(D + 'pr423/capacity217-SELECTION.json')
EN423 = ld(D + 'pr423/enlarged217-SELECTION.json'); GR423 = ld(D + 'pr423/grouped217-SELECTION.json')
DES = from_json(ld(D + 'designs-e8resynth401.json')); LAY = ld(D + 'r779-layers.json')
RT428 = ld(D + 'pr428/retimed217-SELECTION.json'); BL427 = ld(D + 'pr428/block217-SELECTION.json')
src = open(HERE + '/cxop.py').read().split('\na, ta = op(')[0]; ns = {}; exec(compile(src, 'cxop.py', 'exec'), ns); op = ns['op']
R = G426['R']; assert R == 779; EM.setR(R); V, N = EM.V, EM.N; h, m, L = 9, 73, 9; IDLE = [16, 8, 32, 8, 48, 8, 48, 32, 16]
C_BIT = Q(r404['bit_coarse']); assert C_BIT == Q(255384852701747, 250000000000000000)
REMOVED = LAY['removed_r781']; assert REMOVED == [556, 577]
def mp(r):
    r = int(r); assert r not in REMOVED, r
    return r - sum(1 for d in REMOVED if d < r) if r >= 2 * V else r
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
def fid(c, E):
    f = next((i for i, e in enumerate(c['frames']) if len(e) == len(E) and inside(E, e)), None)
    if f is None: c['frames'].append(list(E)); f = len(c['frames']) - 1
    return f
def promote(w, plans):
    """prepend literal unit shears d += c*p at the entrance frame of each new pivot p (p starts there), then raise every
    gate frame that does not contain its operands' current frames to their span, propagating through all later touches"""
    c = copy.deepcopy(w); head = []; ext = set(dict(c['ext']))
    for pl in plans:
        E = pl['basis']; f = fid(c, E)
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
                old = g[1]; g[1] = fid(c, union); changed.append((part, i, old, g[1]))
            for r in rs: cur[r] = g[1]
    for r in range(len(cur)): assert inside(c['frames'][cur[r]], c['frames'][c['final'][r]])
    return rehist(c), head, changed
def enlarge(w, plans):
    c = copy.deepcopy(w); ex = dict(c['ext'])
    for pl in plans:
        p = pl['pivot']; E = canonical(pl['basis']); assert p in ex, ('not a gauge on our word', p)
        old = c['frames'][c['start'][p]]; assert inside(old, E) and len(E) == len(old) + 1, p
        c['start'][p] = fid(c, E); ex[p] = c['start'][p]
    c['ext'] = sorted([r, f] for r, f in ex.items())
    out, hd, ch = promote(c, []); assert not hd; return out, ch
def prefix(c, t, replaced, deliveries):
    """B writes of target t at indices `replaced` become source-touching empty markers; deliveries (slot, frame, helper,
    q) are inserted before B gate `slot` (list order kept)"""
    v = c['v']; d = copy.deepcopy(c); at = {}
    for slot, f, s, q in deliveries:
        assert 0 <= slot < len(c['B']) and 2 * v <= s and q.denominator <= 2
        at.setdefault(slot, []).append(['in', f, t, [[s, q.numerator, q.denominator]]])
    B = []
    for bi, g in enumerate(c['B']):
        B.extend(at.get(bi, []))
        if bi in replaced:
            assert g[0] == 'in' and g[2] == t and len(g[3]) == 1; B.extend(['out', g[1], s, [], []] for s, _, _ in g[3])
        else: B.append(copy.deepcopy(g))
    d['B'] = B; return rehist(d)
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
            def find(x, ph, a, b):
                return next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == ph and e[2][0] == 'add' and ('L', a) in e[2][1:3] and ('L', b) in e[2][1:3])
            def first(x, a): return next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', a) in e[2][1:3])
            c2 = [rej('drop_resynth_delivery', lambda x: x.pop(first(x, 177))), rej('drop_uncompute_add', lambda x: x.pop(find(x, 'main', 301, 276)))]
            def m3(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'climb_pad72'); e = x[j]; x[j] = e[:5] + (e[4],)
            c2.append(rej('padding_not_paid', m3))
            def m4(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'old_response'); e = x[j]; o_ = e[2]; x[j] = (e[0], e[1], o_[:3] + (-o_[3],), e[3])
            c2.append(rej('flip_precancellation', m4))
            c2.append(rej('drop_426_entrance_shear', lambda x: x.pop(first(x, mp(739)))))
            c2.append(rej('drop_promotion_shear_892', lambda x: x.pop(first(x, mp(892)))))
            c2.append(rej('drop_closure_shear_672', lambda x: x.pop(first(x, mp(672)))))
            c2.append(rej('drop_prefix_delivery_124', lambda x: x.pop(find(x, 'main', 124, mp(563)))))
            c2.append(rej('drop_prefix_delivery_172', lambda x: x.pop(find(x, 'main', 172, mp(563)))))
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
def same_rows(a, b, ext):
    """x rows, helper rows and retained totals identical; y rows identical on x, y and gauged columns"""
    oa, ta = op(a); ob, tb = op(b); pr = lambda row_: {k: q for k, q in row_.items() if k < 2 * V or k in ext}
    assert ta == tb and all(oa[r] == ob[r] for r in list(range(V)) + list(range(2 * V, N)))
    assert all(pr(oa[r]) == pr(ob[r]) for r in range(V, 2 * V))
    return [r for r in range(V, 2 * V) if oa[r] != ob[r]]

print('== A. #426 gauged R779 word (ai-nanachi, pinned data)')
w0 = G426; gxok(w0, '#426 word'); e0 = dict(w0['ext']); zr = responses(w0)
assert len(e0) == X426['complex_gauges'] == 202 and all(not zr[p] for p in e0)
p0 = emitted(w0, [])
b0, u0, k0, _, P0, live0, banks0 = price(p0, 8, PAT426, 0)
assert {k: len(x) for k, x in queues(w0, 8).items()} == {9: 4616, 8: 1208, 7: 72, 5: 152, 4: 184} and banks0 == X426['complex_banks_per_stage'] and live0 == X426['complex_live']
assert b0 == Q(X426['complex_coarse']) and {str(r): n for r, n in P0.items() if n} == X426['complex_profile']
assert k0 <= Q(X426['kappa']) < k0 + Q(1, 10**18)
print('   202 gauges, all gauged response columns zero; our emission + price at 8 replicas with #426\'s patterns reproduce #426\'s complex coefficient b = %s and profile exactly;' % b0)
print('   our outer refinement (10^-18 grid) gives kappa = %s, #426\'s %s on its finer grid (same complex-bound value)' % (k0, X426['kappa']))

print('== B. our #424 promotions on R779 (#414 [48], #416 892/669/644 + 947 re-pivot, #420 672, #421 435/367)')
def mplan(pl): return dict(basis=pl['basis'], pivots=[dict(pivot=mp(p['pivot']), coefficients={str(mp(d)): a for d, a in p['coefficients'].items()}) for p in pl['pivots']])
PL = [mplan(p) for p in [G414, C211, C214[0], C214[2], PRO['plan947']] + CL215 + CP217]
wp, head, changed = promote(w0, PL); ext = dict(wp['ext']); assert len(ext) == 213
gxok(wp, 'promoted word')
ob, tb = op(w0); oP, tP = op(wp); want = copy.deepcopy(ob); wtot = copy.deepcopy(tb)
for gate in reversed(head):
    _, f, d, ((p, a, b),) = gate; q = Q(a, b)
    for row_ in list(want) + list(wtot.values()):
        z = row_.get(p, Q(0)) + q * row_.get(d, Q(0))
        if z: row_[p] = z
        else: row_.pop(p, None)
assert oP == want and tP == wtot and all(p not in oP[t] for p in ext for t in range(V, 2 * V))
print('   %d literal shears for 11 new pivots (213 gauges); raw operator and retained totals == #426 x literal prefix on all %d columns; all gauged response columns zero' % (len(head), N))
for part, i, old, nf in changed:
    bad = copy.deepcopy(wp); bad[part][i][1] = old
    try: gx.check1(rehist(bad)); raise SystemExit('reverted frame accepted')
    except AssertionError as e: assert str(e).startswith('E1'), str(e)
print('   frame closure raised %d gate frames; reverting any one fails gx E1' % len(changed))

print('== C. 14 entrance enlargements of #424 (13 of #423 + our 838), mapped')
ENL = [dict(pivot=mp(p['pivot']), basis=p['basis']) for p in [p for p in EN423 if p['pivot'] not in PRX['excluded423']] + GR423 + [PRX['enlarge838']]]
we, ech = enlarge(wp, ENL); gxok(we, 'enlarged word')
oE, tE = op(we); assert oE == oP and tE == tP
for part, i, old, nf in ech:
    bad = copy.deepcopy(we); bad[part][i][1] = old
    try: gx.check1(rehist(bad)); raise SystemExit('reverted frame accepted')
    except AssertionError as e: assert str(e).startswith('E1'), str(e)
print('   operator unchanged on all %d columns; closure raised %d gate frames, each reversion fails gx E1' % (N, len(ech)))

print('== D. sinks 301/387, 177/220 re-synthesis, target-124 prefix, 14 retimings, target-172 prefix')
a0 = SK.analyse(we); ins = []
for r, don in ((301, mp(1019)), (387, mp(1020))):
    gs = SK.find(we, r, an=a0); assert len(gs) == 1; u = {x_: Q(a, b) for x_, a, b in gs[0]['uncompute']}
    assert u[don] == Q(-1, 4) and SK.find(we, r, exclude={don}, an=a0) is None; ins += sixths(gs)
ws = insert(we, ins); gxok(ws, 'enlarged word + sinks 301, 387')
os_, ts = op(ws); assert ts == tP and all(os_[r] == oP[r] for r in range(2 * V))
A_ = LAY['designs']['anchors']; RS = {int(a): b for a, b in LAY['designs']['restore'].items()}; nA = len(ws['A'])
RELOC = {t: [(nA + A_[str(pos)] + 1, f, RS.get(s, mp(s)), q) for pos, f, s, q in dl] for t, dl in DES.items()}
from entrance import build as e401
REF = e401(ld(D + 'pr398/signed25.json.gz'), ld(D + 'pr401/selection.json'))
def mgate(g):
    if g[0] == 'in': return ['in', g[1], mp(g[2]), [[mp(s), a, b] for s, a, b in g[3]]]
    return ['out', g[1], mp(g[2]), [[mp(t), a, b] for t, a, b in g[3]], [mp(x) for x in g[4]]]
for t, dl in DES.items():
    for pos, f, s, q in dl:
        anchor = ws['B'][A_[str(pos)]]; was = mgate(REF['B'][pos - len(REF['A']) - 1])
        if s in RS: assert was == ['in', 892, 180, [[mp(801), 1, 2]]] and anchor == ['in', 892, mp(221), [[mp(801), 1, 2]]], (was, anchor)
        else: assert anchor == was, (anchor, was)
bad = rbuild(ws, {t: [(p_, f, (180 if s == 221 else s), q) for p_, f, s, q in dl] for t, dl in RELOC.items()})
e180 = checks(bad); assert e180[0].startswith('E4'), e180
wr = rbuild(ws, RELOC); gxok(wr, "+ 177/220 re-synthesis"); assert same_rows(ws, wr, ext) == []
print('   #402 designs relocated by anchors; restore source y180 -> y221 (with y180 gx rejects: %s); the full raw operator is unchanged (all 1019 rows)' % e180[0])
def dl_(spec): return [(s_, f_, r_, Q(a, b)) for s_, f_, r_, a, b in spec['deliveries']]
P4 = LAY['prefix124']; w4 = prefix(wr, 124, set(P4['replaced']), dl_(P4)); gxok(w4, '+ target-124 prefix')
assert same_rows(wr, w4, ext) == [124, 171], same_rows(wr, w4, ext)
d4 = hist(w4); d4.subtract(hist(wr)); d4 = {k: x_ for k, x_ in sorted(d4.items()) if x_}
print('   124 prefix: writes B%s -> markers; helper %d/2 at frame 336 and -helper 253/2 at frame 723; histogram delta %s' % (P4['replaced'], mp(563), d4))
for nm, mut in (('omit_delivery', lambda b: b.pop(next(j for j, g in enumerate(b) if g[0] == 'in' and g[2] == 124 and g[3][0][0] == mp(563)))),):
    bad = copy.deepcopy(w4); mut(bad['B']); e = checks(rehist(bad)); assert e[0] and e[0].startswith('E5'), (nm, e)
G4 = w4['A'] + w4['B']; nA4 = len(w4['A']); wt = copy.deepcopy(w4); rlog = []
for rt in LAY['retime']:
    f = fid(wt, rt['basis'])
    for part, i in rt['gates']: rlog.append((part, i, wt[part][i][1], f)); wt[part][i][1] = f
wt = rehist(wt); gxok(wt, '+ 14 fixed-scalar gate-frame retimings')
assert [[g[0]] + g[2:] for g in wt['A'] + wt['B']] == [[g[0]] + g[2:] for g in G4] and op(wt) == op(w4) and wt['start'] == w4['start'] and wt['final'] == w4['final']
dt = hist(wt); dt.subtract(hist(w4)); dt = {k: x_ for k, x_ in sorted(dt.items()) if x_}; assert sum(k * x_ for k, x_ in dt.items()) == 0
print('   scalar words, order, start/final frames and the full raw operator unchanged; %d gate frames changed; histogram delta %s' % (len(rlog), dt))
mine = [tuple(rt['basis']) for rt in LAY['retime']]; theirs = sorted({tuple(x['new_basis']) for x in RT428} | {tuple(x['basis']) for x in BL427})
assert sorted(mine[:13]) == theirs and mine[13] not in theirs
print('   13 of the 14 new bases coincide with eumemic\'s #428 (11 single) and #427 (2 blocks) bases on #423\'s word (independent rediscovery on ours); B1157 -> rank 7 is new')
P7 = LAY['prefix172']; ours = prefix(wt, 172, set(P7['replaced']), dl_(P7)); gxok(ours, 'ours (+ target-172 prefix)')
assert same_rows(wt, ours, ext) == [125, 172], same_rows(wt, ours, ext)
d7 = hist(ours); d7.subtract(hist(wt)); d7 = {k: x_ for k, x_ in sorted(d7.items()) if x_}
for nm, mut in (('omit_delivery', lambda b: b.pop(next(j for j, g in enumerate(b) if g[0] == 'in' and g[2] == 172 and g[3][0][0] == mp(563)))),):
    bad = copy.deepcopy(ours); mut(bad['B']); e = checks(rehist(bad)); assert e[0] and e[0].startswith('E5'), (nm, e)
print('   172 prefix: writes B%s -> markers; -helper %d/2 at frame 336, helper 358/2 at frame 904 (its next frame), -helper 367/2 at 904, -helper 280/2 at 724; delta %s; omitted delivery fails gx E5' % (P7['replaced'], mp(563), d7))
json.dump(dict(ours, derived_from=ours['derived_from'] + ' | chafreaky e8-r779-retimed-closure: #424 layers (#414/#416/947/#420/#421 promotions, 14 enlargements, sinks 301/387, 177/220, target-124 prefix) on #426 R779, 14 gate-frame retimings (bases as #427/#428), target-172 prefix'),
          gzip.open(os.path.join(OD, 'gcert1-e8r779.json.gz'), 'wt'))

print('== E. local program (#390 bracket, both orientations)')
paid = emitted(ours, FUSED, controls=True)
def price_b(paid_, T, pats, nfz):
    pad = Counter()
    for p in pats:
        if p['padding']: pad[p['padding']] += p['count']
    P_ = Counter({int(r): L * T * n for r, n in paid_.items()})
    for r in IDLE: P_[r] += 240 * T
    for r, n in pad.items(): P_[r] += L * n
    P_[1] -= L * nfz
    return certify24(P_, m, 2 * 4 * V * T + L * sum(p['count'] for p in pats))[0]
def bof(w):
    return price_b(emitted(w, FUSED), 64, packer.patterns({k: len(x_) for k, x_ in queues(w, 64).items()}), 128)
b4, bt, bo = bof(w4), bof(wt), bof(ours)
assert b4 < bt < bo
for rt in LAY['retime']:
    one = copy.deepcopy(w4); f = fid(one, rt['basis'])
    for part, i in rt['gates']: one[part][i][1] = f
    assert bof(rehist(one)) > b4
print('   b: after 124 prefix %.15e < after retimings %.15e < with 172 prefix %.15e; each retiming alone raises b' % (b4, bt, bo))
if REGEN:
    import retime as RT
    def gainer(w):
        pd = emitted(w, FUSED); pats = packer.patterns({k: len(x_) for k, x_ in queues(w, 64).items()}); base_ = price_b(pd, 64, pats, 128); cache = {}
        def gain(old, new):
            d = Counter(new); d.subtract(Counter(old)); key = tuple(sorted((k, x_) for k, x_ in d.items() if x_))
            if not key: return Q(0)
            if key not in cache:
                q = Counter(pd); q.update(dict(key)); cache[key] = price_b({k: x_ for k, x_ in q.items() if x_}, 64, pats, 128) - base_
            return cache[key]
        return gain
    found = RT.search(w4, gainer(w4)); nA4 = len(w4['A'])
    got = sorted((tuple(('A', j) if j < nA4 else ('B', j - nA4) for j in blk), tuple(E)) for gn, blk, E in found)
    want = sorted((tuple(tuple(x) for x in rt['gates']), tuple(rt['basis'])) for rt in LAY['retime'])
    def admissible(w, blk, E):
        one = copy.deepcopy(w); f = fid(one, E); nA_ = len(one['A'])
        for j in blk: (one['A'] if j < nA_ else one['B'])[j if j < nA_ else j - nA_][1] = f
        one = rehist(one)
        if checks(one) != [None, None]: return False
        try: emitted(one, FUSED); return True
        except AssertionError: return False
    got = [(tuple(tuple(x) for x in a), b_) for a, b_ in got]; extra = [x for x in got if x not in want]
    assert all(x in got for x in want)
    bad = [(gn, blk, E) for gn, blk, E in found if (tuple(('A', j) if j < nA4 else ('B', j - nA4) for j in blk), tuple(E)) in extra]
    assert len(bad) == len(extra) and not any(admissible(w4, blk, E) for gn, blk, E in bad)
    fin = RT.search(ours, gainer(ours)); assert not any(admissible(ours, blk, E) for gn, blk, E in fin)
    print('   (--regen) retiming search on the post-124 word finds these 14 plus %d candidates rejected by gx/gxcore or the emitter; on our final word %d candidates, all rejected' % (len(extra), len(fin)))
print('== F. banks and price')
T = 64; Q_ = queues(ours, T); inv = {k: len(x_) for k, x_ in Q_.items()}; pats = packer.patterns(inv)
assert pats[0]['r9'] == 8 and pats[0]['padding'] == 1 and pats[0]['count'] >= 2 * T
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
print('   128 fused occurrences (301, 387 x 64 replicas) own slot 0 of 128 distinct rank-1-padded banks (padding on coordinate 72)')
b, u, k, rej, P1, live, banks = price(paid, T, pats, len(fz))
assert C_BIT > b
K424 = Q(1018509848057013, 10**18); K426 = Q(X426['kappa']); K429 = Q(63727910972469, 62500000000000000); K425 = 1.048005508e-3
print('   local paid %s; live %d; profile %s' % (dict(sorted(paid.items())), live, dict(sorted(P1.items()))))
print('   b = %s = %.15e; #404 bit c = %.15e > b: complex-bound' % (b, float(b), float(C_BIT)))
print('   kappa = %s = %.18f (six bootstrap levels, 47 strict constraints; rejected %s)' % (k, float(k), rej))
print('   vs #426 %+.6e, vs #429 (price-only) %+.6e, vs our #424 %+.6e' % (float(k - K426), float(k - K429), float(k - K424)))
sweep = {}
for TT in (8, 16, 32, 48, 96, 128):
    pp = packer.patterns({kk: len(x_) for kk, x_ in queues(ours, TT).items()})
    try: sweep[TT] = str(price(paid, TT, pp, 2 * TT)[2])
    except AssertionError: sweep[TT] = 'outer grid assertion (not used)'
print('   replica sweep:', {t: (float(Q(s_)) if '/' in s_ else s_) for t, s_ in sweep.items()})
assert all(Q(s_) <= k for s_ in sweep.values() if '/' in s_)
json.dump(dict(b=str(b), b_upper=str(u), b_float=float(b), c=str(C_BIT), kappa=str(k), kappa_float=float(k), binding='complex',
               profile={str(r): n for r, n in sorted(P1.items())}, live=live, m=m, T=T, banks_per_stage=banks, patterns=pats,
               local_paid={str(a): x_ for a, x_ in sorted(paid.items())}, fused_sinks=FUSED, gauges=len(ext), R=R,
               raised_frames=[list(x_) for x_ in changed], enlarged_raised=[list(x_) for x_ in ech], retimed=[list(x_) for x_ in rlog],
               control426=dict(b=str(b0), kappa=str(k0)), replica_sweep=sweep),
          open(os.path.join(OD, 'kappa.json'), 'w'), indent=1)
