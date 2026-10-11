"""e8clean3: bank-padding fusion (our #394) on Dugongue's #398 signed target-prefix R781 E8 complex program, with
#398's frozen-K/cleanup bracket (#352's) replaced by #390's dirty-preconditioned bracket (re-implemented in emit.py).
usage: clean.py PKGDIR GXDIR OUT.json [--regen]
  A. #398's word (signed25.json.gz, byte-pinned): gx.check1 + gxcore mirror; its x->y operator and retained totals in
     x equal #378's far word.  Under #398's own bracket every one of the 781 helpers is touched by a non-y gate, hence by
     the FULL cleanup after its final climb: fusion is impossible there.  Ours = #398's word + three free-sink uncomputes:
     gx.check1 + gxcore; paid local histogram unchanged; sink rows zero; x/y operator rows and retained totals == #398's;
     (--regen) the free-sink search over all lifting helpers of #398's word finds exactly our gates.
  B. our bracket compiler reproduces #390's prewhite.json on #390's own word (regression); on #398's word and ours both
     orientations are replayed on all 1021 live columns, private work erased, common exact labels, no event on a fused
     sink after its padded climb; mutation controls rejected.
  C. #398's whole-bank rule (bank, slot = divmod(rep*R + helper, 8), T = 8): every fused occurrence lies in a distinct
     bank, each bank has one rank-1 padding on coordinate 72, and every slot route fixes coordinate 72.
  D. profile from the validated paid events (#398's formula). Control: #398's own 24-digit coarse root and kappa are
     reproduced from our emission of its word (VALIDATION.json). Ours priced the same way (#392/#398 six-level outer)."""
import sys, os, json, gzip, copy
from collections import Counter
from fractions import Fraction as Q
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
PKG, GXD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]; REGEN = '--regen' in sys.argv
sys.path.insert(0, GXD); import gx, gxcore
import emit as EM
from word import insert, origmap, sixths
import sinks as SK
from e8core import coarse, price_word, load_word
from bootstrap import certify24, refine
from layout_bk import layout
ld = lambda p: json.load(gzip.open(p)) if p.endswith('.gz') else json.load(open(p))
far = ld(PKG + '/data/gcert1-e8-r783-far.json.gz'); base = ld(PKG + '/data/pr398/signed25.json.gz')
VAL = ld(PKG + '/data/pr398/VALIDATION.json'); ours = ld(PKG + '/data/sinks-e8clean3.json')
p18 = ld(PKG + '/data/pr390/prefix18.json.gz'); a390 = ld(PKG + '/data/pr390/sink-audit.json')['accepted']; pw390 = ld(PKG + '/data/pr390/prewhite.json')
FUSED = sorted({s['sink_helper'] for s in ours}); assert FUSED == [301, 324, 387]
OD = os.path.dirname(os.path.abspath(OUT)); H390 = {}

def hist(c):
    H = Counter()
    for w in c['blocks'].values():
        for r, n in w.items(): H[int(r)] += n
    return H

def gxok(c, name):
    st = {}; gx.check1(copy.deepcopy(c), scalar=True, stats=st)
    assert gxcore.mirror(gxcore.normal(copy.deepcopy(c)))['hist'] == dict(hist(c))
    print('   %s: gx.check1 PASS (E0-E7 incl. exact scalar E5), gxcore mirror histogram PASS, gates A/B %d/%d' % (name, len(c['A']), len(c['B'])))
    return st

src = open(HERE + '/cxop.py').read().split('\na, ta = op(')[0]; ns = {}; exec(compile(src, 'cxop.py', 'exec'), ns)
print('== B0. bracket regression on #390\'s own word (R = 783)')
EM.setR(783)
w390 = insert(p18, a390); pw = EM.prewhite(w390, {a['sink_helper'] for a in a390})
for mine, key in zip(pw, ['pre_target_dirty_cancellation_gates', 'pre_helper_inverse_gates', 'post_full_helper_clean_repair_gates']):
    assert [(t, s, q) for t, s, q in mine] == [(t, s, Q(a, b)) for t, s, a, b in pw390[key]], key
print('   our bracket compiler reproduces #390 prewhite.json exactly (%d/%d/%d gates)' % tuple(map(len, pw)))

print('== A. words')
R = base['R']; assert (R, base['v'], base['h']) == (781, 120, 9); EM.setR(R); V, N = EM.V, EM.N
gxok(base, '#398 word (R781 + 25 signed target-prefix pairs)')
oa, ta = ns['op'](far); ob, tb = ns['op'](base)
xo = lambda row: {k: q for k, q in row.items() if k < V}
assert all(xo(oa[r]) == xo(ob[r]) for r in range(2 * V)) and {k: xo(t) for k, t in ta.items()} == {k: xo(t) for k, t in tb.items()}
print('   x -> (x, y) operator and retained totals in x of #398\'s word == #378 far word (same product)')
touched = set()
for g in base['A'] + base['B']:
    for r, a, b in g[3]:
        t, s = (r, g[2]) if g[0] == 'out' else (g[2], r)
        if not (V <= t < 2 * V): touched |= {z for z in (t, s) if z >= 2 * V}
assert touched == set(range(2 * V, N))
print('   under #398\'s own frozen-K/cleanup bracket all %d helpers are touched by a non-y gate (FULL cleanup after the final climb): no fusion there' % R)
wour = insert(base, ours); st = gxok(wour, 'ours')
wour_out = dict(wour, derived_from=wour['derived_from'] + ' | e8clean3 free sinks 301/324/387 (chafreaky)')
json.dump(wour_out, gzip.open(os.path.join(OD, 'gcert1-e8clean3.json.gz'), 'wt'))
d = hist(wour); d.subtract(hist(base)); assert not any(d.values()); print('   paid local histogram of ours == #398 word (our uncomputes need no climb)')
an = SK.analyse(wour); val = an[7]; fin = an[5]
for r in FUSED: assert not val[r], r
print('   clean x-rows of helpers 301, 324, 387 are exactly zero; final lifts:', [fin[r] for r in FUSED])
oc, tc = ns['op'](wour)
assert tb == tc and all(ob[r] == oc[r] for r in range(2 * V)); print('   x and y rows of the full rational operator (all 1021 inputs variable) and retained totals == #398 word')
if REGEN:
    cur = base; found = []; an0 = SK.analyse(cur)
    cands = [r for r in range(2 * V, N) if an0[5][r] > 0]
    for r in cands:
        gs = SK.find(cur, r, exclude={s['sink_helper'] for s in found}, an=SK.analyse(cur) if found else an0)
        if not gs: continue
        om = origmap(base, found)
        for g in gs: g['cut_group'] = om[g['cut_group']]
        trial = insert(base, found + gs); at = SK.analyse(trial)
        dd = hist(trial); dd.subtract(hist(base))
        if all(not at[7][s['sink_helper']] for s in found + gs) and not any(dd.values()):
            found += sixths(gs); cur = insert(base, found)
    assert found == ours, found
    print('   regeneration: free-sink search over all %d lifting helpers of #398\'s word finds exactly our three uncomputes' % len(cands))

print('== B. local program (both orientations)')
pwb = EM.prewhite(base, set())
for ori in ['forward', 'backward']:
    r = EM.validate(list(EM.emit(base, ori, {}, set(), pwb)), base, ori, {}, set())
    print('   #398 word, %s: PASS all %d live columns, private work erased, common exact labels, %d events' % (ori, N, r['events']))
pb = r['paid_hist']; assert {int(k): n for k, n in pb.items()} == dict(hist(base))
pw = EM.prewhite(wour, set(FUSED)); paid = {}; res = {}
for ori in ['forward', 'backward']:
    ev = list(EM.emit(wour, ori, H390, set(FUSED), pw)); r = EM.validate(ev, wour, ori, H390, set(FUSED)); paid[ori] = r['paid_hist']; res[ori] = r
    print('   %s: PASS all %d live columns, private work erased, common exact labels, %d events, fused padded climbs %s' % (ori, N, r['events'], [e[1:] for e in ev if e[0] == 'climb_pad72']))
    def reject(name, mut):
        x = list(ev); mut(x)
        try: EM.validate(x, wour, ori, H390, set(FUSED))
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

print('== C. banks (#398 whole-bank rule, T = 8)')
T, L, m = 8, 9, 73; live = 7680 + 9 * R
def perm(slot):  # #398 bank_perm: swap local coordinates 0..8 with block slot*9..slot*9+8
    p = list(range(m))
    if slot:
        for i in range(9): p[i], p[slot * 9 + i] = p[slot * 9 + i], p[i]
    return p
assign = {(rep, h): divmod(rep * R + h, 8) for rep in range(T) for h in range(R)}
assert sorted(Counter(b for b, _ in assign.values()).values()) == [8] * R
fb = [assign[(rep, h - 2 * V)][0] for rep in range(T) for h in FUSED]  # #398 owners index helpers r = register - 2v
assert len(set(fb)) == len(fb) == T * len(FUSED)
assert all(perm(s)[72] == 72 for s in range(8))
print('   %d fused occurrences per stage in %d distinct banks (one rank-1 padding on coordinate 72 each); every slot route fixes coordinate 72; paddings per stage %d -> %d' % (len(fb), len(set(fb)), R, R - len(fb)))

print('== D. price')
def profile(ph, nfused):
    H = Counter({int(r): 72 * n for r, n in ph.items()})
    for r in [16, 8, 32, 8, 48, 8, 48, 32, 16]: H[r] += 1920
    H[1] += L * R - L * T * nfused; return H
H0 = profile(pb, 0); H = profile(paid['forward'], len(FUSED))
for X in (H0, H): assert (m * live - sum(r * n for r, n in X.items()), max(X)) == (2496, 48) and m ** 2 > 2 * 48 ** 2
b0, u0 = certify24(H0, m, live); assert str(b0) == VAL['complex_coarse'], b0
c398 = Q(VAL['bit_coarse']); k0, rej0 = refine(b0, c398); assert str(k0) == VAL['kappa'] == '125311832453733/125000000000000000'
print('   control: #398 b = %s (24 digits, both engines) and kappa = %s = %.18f reproduced from our emission of its word (rejected %s)' % (b0, k0, float(k0), rej0))
b, u = certify24(H, m, live); mass = sum(r * n for r, n in H.items())
print('   b = %s = %.15e  (+%.6e over #398)' % (b, float(b), float(b - b0)))
def bit_c(word, K=3):
    p = price_word(word); h, v = 8, 120; s = 2 * K + 1; mm = s * h; resid = p['resid']
    T8 = 1 if resid % h == 0 else h; lay = layout(K, h)
    Hb = Counter({r: T8 * s * c for r, c in p['H'].items()})
    for r in lay['blocks']: Hb[r] += T8 * 2 * v
    W8 = (2 * K * v * h + resid) * T8 // h
    assert mm * W8 - sum(r * c for r, c in Hb.items()) == T8 * (2 * K * v - s * 72)
    return coarse(Hb, mm, W8)
c = bit_c(load_word(PKG + '/data/bit/bitE8-kernel.json.gz')); assert c == Q(251726760077483, 25 * 10**16)
print('   bit c (our #382 word, B3 unsplit) = %s = %.15e  (> b: complex-bound)' % (c, float(c)))
k, rej = refine(b, c); kb, _ = refine(b, c398); assert k == kb and k > k0 and c > b
print('   kappa = %s = %.18f (complex-bound; same with #398\'s bit c), +%.6e over #398; rejected %s' % (k, float(k), float(k - k0), rej))
json.dump(dict(b=str(b), b_upper=str(u), b_float=float(b), b_398=str(b0), c=str(c), kappa=str(k), kappa_float=float(k), binding='complex', kappa_398=str(k0),
               profile={str(r): n for r, n in sorted(H.items())}, live=live, m=m, deficit=m * live - mass, local_paid=paid['forward'],
               fused_sinks=FUSED, gx_stats=st), open(OUT, 'w'), indent=1)
