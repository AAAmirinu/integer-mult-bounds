"""Randomized shared-donor kernel packing on an E8 bit word, scored by the linearised B_K moment ledger
chi(r) = r((m/r)^a - 1) (exact first-order change of the root equation sum n chi(r) = deficit; the pivot's W change
cancels in the deficit since m = 8(2K+1)). Phase 1: NSEED randomised greedy packings (entrance order key gain*(1+NOISE*u)).
Phase 2: iterated local search from the best: drop a random fraction of entrance groups, re-pack greedily with noise,
accept if chi improves. usage: ils.py IN.json.gz OUTSEL.json NOISE SEED NSEED ITERS"""
import sys, os, json, math, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code'))
from kernel import plan_E, Model
from census import census, candidates
from bk import *

def setup(c, a, m=72):
    M = Model(c); d = M.L.dim
    chi = lambda r: 0.0 if r <= 0 else r * (math.exp(a * math.log(m / r)) - 1)
    dread, first = census(c, M); ret = set(c['ret'])
    H = [h for h in first if h not in ret]
    cand = sorted(candidates(c, M, first, ret))
    groups = {E: [h for h in H if E & ~first[h] == 0] for E in cand}
    groups = {E: g for E, g in groups.items() if len(g) >= 2}
    return dict(M=M, d=d, chi=chi, dread=dread, first=first, H=H, cand=sorted(groups), groups=groups)

def chi_total(ctx, sel):
    d, chi, first = ctx['d'], ctx['chi'], ctx['first']; tot = 0.0; seen = set()
    for E, p, D in sel:
        e = d(E); tot += chi(d(first[p])) - chi(d(first[p]) - e)
        for x in D:
            if x not in seen: seen.add(x); tot -= chi(e) + chi(d(first[x]) - e) - chi(d(first[x]))
    return tot

def greedy(ctx, rng, NZ, preload=()):
    d, chi, dread, first, groups = ctx['d'], ctx['chi'], ctx['dread'], ctx['first'], ctx['groups']
    avail_p = set(ctx['H']); avail_d = set(ctx['H']); donor_at = {}; chosen = list(preload)
    for E, p, D in preload:
        avail_p.discard(p); avail_d.discard(p)
        for x in D: donor_at[x] = E; avail_p.discard(x); avail_d.discard(x)
    plans = {}; fac = {}
    def refresh(E):
        plans[E] = plan_E(E, groups[E], dread, first, d, chi, avail_p, avail_d, donor_at); fac[E] = 1 + NZ * rng.random()
    for E in ctx['cand']: refresh(E)
    member = {}
    for E, g in groups.items():
        for h in g: member.setdefault(h, []).append(E)
    while True:
        live = [(pl[0] * fac[E], E) for E, pl in plans.items() if pl]
        if not live: break
        _, E = max(live); g, ents = plans[E]
        touched = set()
        for p, D in ents:
            chosen.append((E, p, D)); avail_p.discard(p); avail_d.discard(p); touched.add(p)
            for x in D: donor_at[x] = E; avail_p.discard(x); avail_d.discard(x); touched.add(x)
        for E2 in sorted({E2 for h in touched for E2 in member.get(h, ())} | {E}):
            if plans.get(E2) is not None or E2 == E: refresh(E2)
    return chosen

if __name__ == '__main__':
    c = load_word(sys.argv[1]); out = sys.argv[2]; NZ = float(sys.argv[3]); seed = int(sys.argv[4]); NS = int(sys.argv[5]); IT = int(sys.argv[6])
    a = float(price_bk(c, 4, fast=True)['c']); t0 = time.time()
    ctx = setup(c, a); rng = random.Random(seed); print('setup %.1fs' % (time.time() - t0), flush=True)
    best = greedy(ctx, rng, 0.0); bv = chi_total(ctx, best); print('greedy chi %.6f' % bv, flush=True)
    if os.environ.get('START'):
        best = [(E, p, D) for E, p, D in json.load(open(os.environ['START']))]; bv = chi_total(ctx, best); print('start chi %.6f' % bv, flush=True)
    for s in range(NS):
        sel = greedy(ctx, rng, NZ); v = chi_total(ctx, sel)
        if v > bv: best, bv = sel, v; print('seed-pack', s, 'chi %.6f' % bv, len(best), flush=True)
    groupsE = lambda S: sorted({E for E, p, D in S})
    for it in range(IT):
        Es = groupsE(best); frac = rng.choice(tuple(float(x) for x in os.environ.get('FRACS', '0.05,0.1,0.2,0.35').split(',')))
        drop = set(rng.sample(Es, max(1, int(frac * len(Es)))))
        keep = [x for x in best if x[0] not in drop]
        sel = greedy(ctx, rng, rng.choice((0.0, 0.5, 2.0, 10.0)), keep); v = chi_total(ctx, sel)
        if v > bv + 1e-12:
            best, bv = sel, v; print('ils', it, 'frac', frac, 'chi %.6f' % bv, len(best), flush=True)
            json.dump([[E, p, D] for E, p, D in best], open(out, 'w'))
    json.dump([[E, p, D] for E, p, D in best], open(out, 'w'))
    print('final chi %.6f entries %d rank %d' % (bv, len(best), sum(ctx['d'](E) for E, p, D in best)))
