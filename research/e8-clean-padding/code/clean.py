"""e8clean: bank-padding fusion on top of PR #390's dirty-preconditioned E8 complex program.
usage: clean.py PKGDIR GXDIR OUT.json [--regen]
Steps (all exact, standard library only):
  A. rebuild #390's main word (prefix18 + its two sink uncomputes, from #390's sink-audit.json) and ours (+ our three
     free-sink uncomputes); gx.check1 + gxcore mirror on both; paid local histogram unchanged by our gates; our three
     sinks have exactly zero clean x-row; x/y operator rows and retained totals unchanged; (--regen) the free-sink search
     from #390's word finds exactly our three gates.
  B. our reimplementation of #390's bracket reproduces #390's prewhite.json gate for gate (regression); our bracket;
     both orientations of the full local program replayed on all 1023 live columns, private work erased, every
     scalar at a common exact label, no event on a fused sink after its padded climb; mutation controls rejected.
  C. #390's bank assignment rebuilt; every fused occurrence lies in a distinct ordinary (padded) bank whose route fixes
     coordinate 72.
  D. global profile from the validated paid events; b by both PR #315 engines; #390's own b reproduced; bit c of our
     #382 word; PR #315 outer assembly -> kappa."""
import sys, os, json, gzip, copy
from collections import Counter
from fractions import Fraction as Q
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PKG, GXD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; REGEN = '--regen' in sys.argv
sys.path.insert(0, GXD); import gx, gxcore
from word import insert, origmap, sixths
import sinks as SK
from emit import prewhite, emit, validate, N, V
from e8core import coarse, kappa, price_word, load_word
from layout_bk import layout
ld = lambda p: json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
base = ld(PKG + '/data/pr390/prefix18.json.gz'); a390 = ld(PKG + '/data/pr390/sink-audit.json')['accepted']
ours = ld(PKG + '/data/sinks-e8clean.json'); pw390 = ld(PKG + '/data/pr390/prewhite.json')
far = ld(PKG + '/data/gcert1-e8-r783-far.json.gz')
H390 = {a['sink_helper']: a['frame'] for a in a390}; FUSED = sorted({s['sink_helper'] for s in ours})
assert FUSED == [301, 324, 387] and set(H390) == {355, 403}
R = {}

def hist(c):
    H = Counter()
    for w in c['blocks'].values():
        for r, n in w.items(): H[int(r)] += n
    return H

def gxok(c, name):
    st = {}; gx.check1(copy.deepcopy(c), scalar=True, stats=st)
    assert gxcore.mirror(gxcore.normal(copy.deepcopy(c)))['hist'] == dict(hist(c))
    c2 = copy.deepcopy(c);     print('   %s: gx.check1 PASS (E0-E7 incl. exact scalar E5), gxcore mirror histogram PASS, gates A/B %d/%d' % (name, len(c['A']), len(c['B'])))
    return st

print('== A. words')
w390 = insert(base, a390); wour = insert(base, a390 + ours)
gxok(w390, '#390 main word (prefix18 + sinks 355/403)'); st = gxok(wour, 'ours')
wour_out = dict(wour, derived_from=wour['derived_from'] + ' | PR #390 (Dugongue) sinks 355/403 | e8clean free sinks 301/324/387 (chafreaky)')
json.dump(wour_out, gzip.open(os.path.join(os.path.dirname(os.path.abspath(OUT)), 'gcert1-e8clean.json.gz'), 'wt'))
d = hist(wour); d.subtract(hist(w390)); assert not any(d.values()); print('   paid local histogram of ours == #390 word (our uncomputes need no climb)')
d = hist(w390); d.subtract(hist(base)); assert dict(+d) == {1: 4, 3: 4} and dict(-d) == {4: 4}
an = SK.analyse(wour); val = an[7]; fin = an[5]
for r in FUSED + list(H390): assert not val[r], r
print('   clean x-rows of helpers 301, 324, 387 (ours) and 355, 403 (#390) are exactly zero; final lifts of ours:', [fin[r] for r in FUSED])
# operator: x and y rows and retained totals identical to #378's far word (helper rows are garbage and change)
sys.argv_save = sys.argv
import importlib.util
spec = importlib.util.spec_from_file_location('cxop_lib', HERE + '/cxop.py')
src = open(HERE + '/cxop.py').read().split('\na, ta = op(')[0]; ns = {}; exec(compile(src, 'cxop.py', 'exec'), ns)
oa, ta = ns['op'](far); ob, tb = ns['op'](wour)
assert ta == tb and all(oa[r] == ob[r] for r in range(2 * V)); print('   x and y rows of the full rational operator (all 1023 inputs variable) and retained totals == #378 far word')
if REGEN:
    cur = w390; found = []; an0 = SK.analyse(cur)
    cands = [r for r in range(2 * V, N) if an0[5][r] > 0 and r not in H390]
    for r in cands:
        gs = SK.find(cur, r, exclude=set(H390) | {s['sink_helper'] for s in found}, an=SK.analyse(cur) if found else an0)
        if not gs: continue
        om = origmap(base, a390 + found)
        for g in gs: g['cut_group'] = om[g['cut_group']]
        trial = insert(base, a390 + found + gs); at = SK.analyse(trial)
        dd = hist(trial); dd.subtract(hist(w390))
        if all(not at[7][s['sink_helper']] for s in a390 + found + gs) and not any(dd.values()):
            found += sixths(gs); cur = insert(base, a390 + found)
    assert found == ours, found
    print('   regeneration: free-sink search over all %d lifting helpers of #390\'s word finds exactly our three uncomputes' % len(cands))

print('== B. local program (both orientations)')
pw = prewhite(w390, set(H390))
for mine, key in zip(pw, ['pre_target_dirty_cancellation_gates', 'pre_helper_inverse_gates', 'post_full_helper_clean_repair_gates']):
    assert [(t, s, q) for t, s, q in mine] == [(t, s, Q(a, b)) for t, s, a, b in pw390[key]], key
print('   regression: our bracket compiler reproduces #390 prewhite.json exactly (%d/%d/%d gates)' % tuple(map(len, pw)))
pw = prewhite(wour, set(H390) | set(FUSED)); paid = {}; res = {}
for ori in ['forward', 'backward']:
    ev = list(emit(wour, ori, H390, set(FUSED), pw)); r = validate(ev, wour, ori, H390, set(FUSED)); paid[ori] = r['paid_hist']; res[ori] = r
    print('   %s: PASS all 1023 live columns, private work erased, common exact labels, %d events, fused padded climbs %s' % (ori, r['events'], [e[1:] for e in ev if e[0] == 'climb_pad72']))
    def reject(name, mut):
        x = list(ev); mut(x)
        try: validate(x, wour, ori, H390, set(FUSED))
        except (AssertionError, KeyError) as e: return name
        raise SystemExit('control accepted: ' + name)
    ctr = []
    i = next(i for i, e in enumerate(ev) if e[0] == 'scalar' and e[1] == 'cleanup')
    def m1(x):  # cleanup touching a fused sink after its padded climb
        e = x[i]; op = e[2]; x[i] = (e[0], e[1], (op[0], ('L', FUSED[0]) if ori == 'forward' else op[1], op[2] if ori == 'forward' else ('L', FUSED[0]), op[3]), e[3])
    ctr.append(reject('cleanup_on_fused_sink', m1))
    def m2(x):  # padded climb moved before the sink's last main use
        j = next(j for j, e in enumerate(x) if e[0] == 'climb_pad72'); e = x.pop(j)
        k = max(j for j, y in enumerate(x) if y[0] == 'scalar' and y[1] == 'main' and ('L', e[1]) in y[2][1:3]); x.insert(k, e)
    ctr.append(reject('padded_climb_before_last_use', m2))
    def m3(x):  # drop one of our uncompute adds
        j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'main' and e[2][0] == 'add' and e[2][1 if ori == 'forward' else 2] == ('L', 301) and e[2][2 if ori == 'forward' else 1] == ('L', 276)); x.pop(j)
    ctr.append(reject('drop_uncompute_add', m3))
    def m4(x):  # flip the sign of one target precancellation
        j = next(j for j, e in enumerate(x) if e[0] == 'scalar' and e[1] == 'old_response'); e = x[j]; op = e[2]; x[j] = (e[0], e[1], op[:3] + (-op[3],), e[3])
    ctr.append(reject('flip_precancellation', m4))
    def m5(x):  # padded climb priced without the padding coordinate
        j = next(j for j, e in enumerate(x) if e[0] == 'climb_pad72'); e = x[j]; x[j] = e[:5] + (e[4],)
    ctr.append(reject('padding_not_paid', m5))
    print('   controls rejected:', ctr)
assert paid['forward'] == paid['backward'] and res['forward']['edges'] == res['backward']['edges']

print('== C. banks (#390 assignment, T = 32)')
full = [(rep, h) for rep in range(32) for h in range(2 * V, N) if h not in H390]
small = [(rep, h) for rep in range(32) for h in range(2 * V, N) if h in H390]
assign = {}; fi = 0
for bank in range(8):
    assign[full[fi]] = (bank, 0); fi += 1
for bank in range(8, 3131):
    for j in range(8): assign[full[fi]] = (bank, 9 * j); fi += 1
assert fi == len(full) == 24992 and len(small) == 64
def perm(off):  # #390's perm(src=0..8, offset): local i -> off+i, remaining coordinates in increasing order
    p = [-1] * 73; used = set(range(off, off + 9))
    for i in range(9): p[i] = off + i
    z = 0
    for i in range(73):
        if p[i] < 0:
            while z in used: z += 1
            p[i] = z; used.add(z)
    return p
fb = [assign[(rep, h)][0] for rep in range(32) for h in FUSED]
assert len(set(fb)) == len(fb) == 96 and min(fb) >= 8
assert all(perm(assign[(rep, h)][1])[72] == 72 for rep in range(32) for h in FUSED)
print('   96 fused occurrences per stage in 96 distinct ordinary banks; each route fixes coordinate 72; paddings per stage 3123 -> %d' % (3123 - 96))

print('== D. price')
T, L, m, banks = 32, 9, 73, 3131; live = 8 * V * T + 9 * banks
def profile(ph, nfused):
    H = Counter({int(r): 288 * n for r, n in ph.items()})
    for r in [16, 8, 32, 8, 48, 8, 48, 32, 16]: H[r] += 2 * V * T
    H[1] += L * (banks - 8 - T * nfused); return H
H = profile(paid['forward'], len(FUSED)); mass = sum(r * n for r, n in H.items())
assert (live, m * live - mass, max(H)) == (58899, 9984, 48) and m ** 2 > 2 * 48 ** 2
# regression: #390's own program (no fusion) through the same pipeline
pwb = prewhite(w390, set(H390)); pb = validate(list(emit(w390, 'forward', H390, set(), pwb)), w390, 'forward', H390, set())['paid_hist']
b390 = coarse(profile(pb, 0), m, live); assert b390 == Q(40048866680681, 4 * 10**16), b390
print('   regression: #390 b = %s = %.15e reproduced from its emitted program' % (b390, float(b390)))
b = coarse(H, m, live)
print('   b = %s = %.15e  (+%.6e over #390)' % (b, float(b), float(b - b390)))
def bit_c(word, K=3):
    p = price_word(word); h, v = 8, 120; s = 2 * K + 1; mm = s * h; resid = p['resid']
    T8 = 1 if resid % h == 0 else h; lay = layout(K, h)
    Hb = Counter({r: T8 * s * c for r, c in p['H'].items()})
    for r in lay['blocks']: Hb[r] += T8 * 2 * v
    W = (2 * K * v * h + resid) * T8 // h
    assert mm * W - sum(r * c for r, c in Hb.items()) == T8 * (2 * K * v - s * 72)
    return coarse(Hb, mm, W)
c = bit_c(load_word(PKG + '/data/bit/bitE8-kernel.json.gz')); assert c == Q(251726760077483, 25 * 10**16)
print('   bit c (our #382 word, B3 unsplit) = %s = %.15e' % (c, float(c)))
k, bind = kappa(c, b); k390, _ = kappa(c, b390)
assert k390 == Q(125027527861191, 125 * 10**15)
print('   kappa (#390 b, same assembly) = %s = %.15e  [= #390]' % (k390, float(k390)))
print('   kappa = %s = %.15e (%s-bound), +%.6e over #390' % (k, float(k), bind, float(k - k390)))
json.dump(dict(b=str(b), b_float=float(b), b_390=str(b390), c=str(c), kappa=str(k), kappa_float=float(k), binding=bind, kappa_390=str(k390),
               profile={str(r): n for r, n in sorted(H.items())}, live=live, m=m, deficit=m * live - mass, local_paid=paid['forward'],
               fused_sinks=FUSED, gx_stats=st), open(OUT, 'w'), indent=1)
