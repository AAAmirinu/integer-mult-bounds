"""e8-sequential-enlarged: checker-clean composition of #409's ordered sequential entrance gauges, #410's entrance
enlargements, our re-pivoting, padding fusion (sinks 301/387) and our #402 target re-synthesis, on #404's R781 E8 word.
usage: compose410.py PKGDIR GXDIR OUTDIR
  A. controls (all words own re-implementations; the PRs are read as data only): #406, #408, #409, #410 frozen hashes
     reproduced; #409's, #408's and #410's b and kappa reproduced exactly from OUR emission (#390 bracket) with their
     own replica counts and bank patterns.  Recorded: Sussman's gx.check1 and gxcore reject all four words (E4, from
     #404's 124/125 recovery); without the recovery gxcore still rejects #409's word (E5 sixths, register 275, from
     its own plans 51/195) and #410's (E5, register 947, #404's pivot 555).
  B. ours: #404's 194 gauges with our four re-pivotings, #410's eight enlargements (the 1020 one carried by our
     re-pivoted row of 1001), #409's four sequential groups with two new re-pivotings (1010 -> 739, 910 -> 531); full
     raw operator == #398's times the literal entrance prefix (all 1021 columns, retained totals); all 204 gauged
     response columns zero; gx.check1 + gxcore PASS.  No 124/125 recovery (it violates gx E4).
  C. sinks 301/387 fused (quarter of 1019/1020, even-coefficient donors), 177/220 re-synthesised (#402 designs relocated
     as #406 does); x/y rows and retained totals unchanged; gx.check1 + gxcore PASS.
  D. local program both orientations, mutation controls.
  E. banks (32 replicas, own greedy patterns; fused occurrences own slot 0 of distinct rank-1-padded banks) and price."""
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
ld = lambda p: json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
D = PKG + '/data/'
base = ld(D + 'pr398/signed25.json.gz'); sel4 = ld(D + 'pr404/selection194.json'); r404 = ld(D + 'pr404/RESULT.json')
s9 = ld(D + 'pr409/SELECTION.json'); pat9 = ld(D + 'pr409/PATTERNS.json'); en = ld(D + 'pr410/enlarged205.json'); pat10 = ld(D + 'pr410/bank-patterns.json')
s205 = ld(D + 'pr408/selection205.json'); pat8 = ld(D + 'pr408/bank-patterns.json')
RPV = ld(D + 'repivot-e8.json'); RPS = ld(D + 'repivot-e8seq.json')
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
            def m5(x):
                j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and ('L', 739) in e[2][1:3]); x.pop(j)
            c2.append(rej('drop_sequential_entrance_shear', m5))
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
def control(name, word, T, pats, want):
    q = {k: len(x) for k, x in queues(word, T).items()}; need = Counter()
    for p in pats:
        for k, x in p.items():
            if k.startswith('r'): need[int(k[1:])] += x * p['count']
    assert dict(need) == q, (q, need)
    b, _, k, _, _, live, banks = price(emitted(word, []), T, pats, 0); assert str(k) == want, (name, k)
    print('   %s: b = %s and kappa = %s = %.18f reproduced from our emission (%d replicas, its own %d banks/stage)' % (name, b, k, float(k), T, banks))
    return b, k

print('== A. controls: #406, #408, #409, #410 words re-implemented; their kappas from our emission; Sussman\'s checkers')
w4, info = E4.build(base, sel4); assert info['final_sha'] == E4.FINAL_SHA
w6 = rbuild(w4, SE.relocate(ref, w4, DES)); assert SE.sha(w6) == SE.SHA['w406']
w9c, g9, _ = SE.sequential(w6, s9); assert SE.sha(w9c) == SE.SHA['w409'] and len(g9) == 51 and len(w9c['ext']) == 204
c8, _, _ = E4.shared(base, s205); c8 = E4.frame376(E4.dual(c8)); w8 = rbuild(c8, SE.relocate(ref, c8, DES)); assert SE.sha(w8) == SE.SHA['w408']
assert SE.enlarge(s205, en['changes']) ['plans'] == en['plans']
c10, _, _ = E4.shared(base, en); c10 = SE.promote760(c10); assert SE.sha(c10) == SE.SHA['w410prom']
c10 = E4.frame376(E4.dual(c10)); w10 = rbuild(c10, SE.relocate(ref, c10, DES)); assert SE.sha(w10) == SE.SHA['w410']
print('   frozen hashes reproduced: #406 3f67e51a..., #408 7a5d0d09..., #409 e775f810..., #410 5243b69b... (and #410 promotion 39c360dd...);')
print('   #410\'s enlarged205.json == our enlarge(#408 selection205, its 8 changes)')
E4REC = 'E4: a pivot is the target of a gate reading y'
for nm, w_ in (('#406', w6), ('#408', w8), ('#409', w9c), ('#410', w10)): assert checks(w_) == [E4REC, E4REC], nm
c, _, _ = E4.shared(base, sel4); n9, _, _ = SE.sequential(rbuild(E4.frame376(c), SE.relocate(ref, E4.frame376(c), DES)), s9)
e9 = checks(n9); assert e9 == [None, 'E5: an entry needs a denominator beyond sixths (register 275)'], e9
c, _, _ = E4.shared(base, en); c = E4.frame376(SE.promote760(c)); e10 = checks(rbuild(c, SE.relocate(ref, c, DES)))
assert e10 == [None, 'E5: an entry needs a denominator beyond sixths (register 947)'], e10
print('   recorded: gx.check1 AND gxcore reject #406, #408, #409 and #410 as published (%s; #404\'s 124/125 recovery);' % E4REC)
print('   with the recovery removed, gxcore still rejects #409 (%s) and #410 (%s)' % (e9[1], e10[1]))
b9, k9 = control('#409', w9c, 32, pat9, '508625250464133/500000000000000000')
b8, k8 = control('#408', w8, 64, pat8, '1017022657082799/1000000000000000000')
b10, k10 = control('#410', w10, 16, pat10, '508781072593909/500000000000000000')

print('== B. ours: #404 gauges re-pivoted (4), #410 enlargements (8), #409 sequential groups re-pivoted (2)')
sel = sel4
for s in RPV['swaps']: sel = RP.swap(sel, s['plan'], s['out'], s['into'])
sel = SE.enlarge(sel, en['changes'], {1020: 1001}); RP.check_global(sel)
print('   our #407 re-pivots %s; #410 enlargements of %s (1020 -> its re-pivoted row 1001; same relation and roles)' % ([(s['out'], s['into']) for s in RPV['swaps']], [c_['pivot'] for c_ in en['changes']]))
s9r = copy.deepcopy(s9)
for sw in RPS['swaps']:
    i = next(i for i, p in enumerate(s9r) if p['vector'] == sw['plan_vector']); old = s9r[i]
    piv = sorted(sw['into'] if p['pivot'] == sw['out'] else p['pivot'] for p in old['pivots'])
    s9r[i] = SE.repivot_rows(old, piv); assert s9r[i] is not None
    a = RP.rows(old); b_ = RP.rows(s9r[i]); cols = sorted({k for r in list(a.values()) + list(b_.values()) for k in r})
    def rank(rows):
        M = [[r.get(k, Q(0)) for k in cols] for r in rows]; rk = 0
        for j in range(len(cols)):
            p = next((x for x in range(rk, len(M)) if M[x][j]), None)
            if p is None: continue
            M[rk], M[p] = M[p], M[rk]
            for x in range(len(M)):
                if x != rk and M[x][j]: f = M[x][j] / M[rk][j]; M[x] = [u - f * v for u, v in zip(M[x], M[rk])]
            rk += 1
        return rk
    assert rank(list(a.values())) == rank(list(b_.values())) == rank(list(a.values()) + list(b_.values())) == len(a)
    print('   #409 group [%d]: pivot %d -> %d (same relation span): %s' % (sw['plan_vector'], sw['out'], sw['into'], sw['why']))
c0, nsh, _ = E4.shared(base, sel); w = E4.frame376(c0)
w9, g, new = SE.sequential(w, s9r); piv = {p for p, _ in w9['ext']}; assert len(piv) == 204 and len(new) == 10
gxok(w9, 'our gauged word')
ob, tb = op(base); o9, t9 = op(w9); want = copy.deepcopy(ob); wtot = copy.deepcopy(tb)
pref = w9['A'][:len(g) + nsh]; assert pref == g + w['A'][:nsh] and all(x[0] == 'in' and len(x[3]) == 1 for x in pref)
for gate in reversed(pref):
    _, f, d, ((p, a, b),) = gate; q = Q(a, b)
    for row in list(want) + list(wtot.values()):
        z = row.get(p, Q(0)) + q * row.get(d, Q(0))
        if z: row[p] = z
        else: row.pop(p, None)
assert o9 == want and t9 == wtot and all(p not in o9[t] for p in piv for t in range(V, 2 * V))
written = set()
for gate in pref:
    (s_, a, b), = gate[3]; assert s_ not in written; written.add(gate[2])
print('   %d entrance unit shears (%d sequential + %d shared-donor); full raw operator and retained totals == #398\'s times the literal prefix on all %d columns;' % (len(pref), len(g), nsh, N))
print('   all 204 gauged response columns zero; every sequential source is read before any entrance write to it')

print('== C. sinks 301/387 and re-synthesis 177/220')
a0 = SK.analyse(w9); ins = []
for r, don in ((301, 1019), (387, 1020)):
    gs = SK.find(w9, r, an=a0); assert len(gs) == 1; u = {x: Q(a, b) for x, a, b in gs[0]['uncompute']}
    assert u[don] == Q(-1, 4) and SK.find(w9, r, exclude={don}, an=a0) is None; ins += sixths(gs)
ws = insert(w9, ins); gxok(ws, 'gauged word + sinks 301, 387')
os_, ts = op(ws); assert ts == t9 and all(os_[r] == o9[r] for r in range(2 * V))
ours = rbuild(ws, SE.relocate(ref, ws, DES)); gxok(ours, 'ours')
oo, to = op(ours); assert oo == os_ and to == ts
dd = hist(ours); dd.subtract(hist(ws)); dd = {k: x for k, x in sorted(dd.items()) if x}; assert dd == {2: 2, 3: -2, 5: -2, 6: 2}, dd
print('   sinks: each needs exactly -1/4 of 1019 / 1020 (even-coefficient donors after re-pivoting); x/y rows and totals unchanged')
print('   re-synthesis: full raw operator identical (all %d columns), block histogram delta %s' % (N, dd))
json.dump(dict(ours, derived_from=ours['derived_from'] + ' | #404 gauges re-pivoted, #410 enlargements, #409 sequential groups re-pivoted, sinks 301/387, targets 177/220 (chafreaky)'),
          gzip.open(os.path.join(OD, 'gcert1-e8seqenlarged.json.gz'), 'wt'))

print('== D. local program (#390 bracket, both orientations)')
paid = emitted(ours, FUSED, controls=True)

print('== E. banks and price')
T = 32; Q_ = queues(ours, T); inv = {k: len(x) for k, x in Q_.items()}; pats = packer.patterns(inv)
assert inv == {9: 18464, 8: 4896, 7: 288, 5: 608, 4: 736} and pats[0] == {'count': 1495, 'r9': 8, 'padding': 1}
pk9 = packer.patterns({k: len(x) for k, x in queues(w9c, 32).items()}); assert sorted(map(str, pk9)) == sorted(map(str, pat9))
fz = [(rep, r) for rep in range(T) for r in FUSED]; rest = [x for x in Q_[9] if x[1] not in FUSED]; q9 = []
for k in range(len(fz)): q9 += [fz[k]] + rest[7 * k:7 * k + 7]
q9 += rest[7 * len(fz):]; Q_[9] = q9; Q_ = {k: deque(x) for k, x in Q_.items()}; asg = {}; padding = {}; bank = 0
for pat in pats:
    for _ in range(pat['count']):
        off = 0
        for key, num in sorted(((k, x) for k, x in pat.items() if k.startswith('r')), key=lambda z: -int(z[0][1:])):
            rk = int(key[1:])
            for _ in range(num): role = Q_[rk].popleft(); asg[role] = (bank, list(range(off, off + rk))); off += rk
        assert off + pat['padding'] == m
        if off < m: padding[bank] = list(range(off, m))
        bank += 1
assert all(not x for x in Q_.values()) and len(asg) == T * R
fb = [asg[x][0] for x in fz]; assert len(set(fb)) == len(fz) == 64 and all(padding.get(b) == [72] and asg[x][1] == list(range(9)) for b, x in zip(fb, fz))
print('   %d replicas: inventory %s in %d width-73 banks/stage: %s' % (T, inv, bank, [(p['count'], {k: v for k, v in p.items() if k.startswith('r')}, p['padding']) for p in pats]))
print('   64 fused occurrences (301, 387 x 32 replicas) own slot 0 of 64 distinct rank-1-padded banks (padding on coordinate 72, paid in the sink\'s final climb)')
b, u, k, rej, P1, live, banks = price(paid, T, pats, len(fz))
assert C_BIT > b
print('   local paid %s; live %d; profile %s' % (dict(sorted(paid.items())), live, dict(sorted(P1.items()))))
print('   b = %s = %.15e; #404 bit c = %.15e > b: complex-bound' % (b, float(b), float(C_BIT)))
print('   kappa = %s = %.18f (six bootstrap levels, 47 strict constraints; rejected %s)' % (k, float(k), rej))
print('   vs #410 %+.6e, vs #409 %+.6e, vs #408 %+.6e' % (float(k - k10), float(k - k9), float(k - k8)))
sweep = {}
for TT in (16, 64):
    pp = packer.patterns({kk: len(x) for kk, x in queues(ours, TT).items()}); sweep[TT] = str(price(paid, TT, pp, 2 * TT)[2])
assert Q(sweep[64]) == k > Q(sweep[16])
print('   replica sweep: 16 -> %s, 64 -> %s (= 32; 64-replica banks add nothing here)' % (sweep[16], sweep[64]))
json.dump(dict(b=str(b), b_upper=str(u), b_float=float(b), c=str(C_BIT), kappa=str(k), kappa_float=float(k), binding='complex',
               kappa_409=str(k9), kappa_408=str(k8), kappa_410=str(k10), b_409=str(b9), b_410=str(b10),
               profile={str(r): n for r, n in sorted(P1.items())}, live=live, m=m, T=T, banks_per_stage=banks, patterns=pats,
               local_paid={str(a): x for a, x in sorted(paid.items())}, fused_sinks=FUSED, gauges=204,
               repivots_404=[[s['plan'], s['out'], s['into']] for s in RPV['swaps']], repivots_409=[[s['plan_vector'], s['out'], s['into']] for s in RPS['swaps']],
               enlargements_410=[c_['pivot'] for c_ in en['changes']], replica_sweep=sweep),
          open(os.path.join(OD, 'kappa.json'), 'w'), indent=1)
