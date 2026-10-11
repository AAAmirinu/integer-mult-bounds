"""Shared-donor response kernel on a bitE8/1 word (our #320/#329 mechanism, ported to the E8 frames).
An entry: pivot p, entrance E (root-spanned, inside p's first frame and every donor's first frame), donors D with
resp(p) = XOR resp(D) over F2 (resp = the targets whose frame-0 completion reads read the helper).
Transform: p starts at E and loses its completion reads; at the start of A each donor climbs to E and pays d += p
(one gate per donor at E); after C each donor pays d += p again at FULL (F2: d -= p).
Selection: greedy max net gain over entrances with helper exclusivity (pivots never donors; a donor serves one E).
Gain ledger chi(r) = r((m/r)^a - 1): pivot chi(d_p) - chi(d_p - e); donor chi(e) + chi(d_d - e) - chi(d_d).
usage: kernel.py IN.json.gz OUT.json.gz [maxentries] [trimmod]
Chafik Boukhalfa (chafreaky) with Anthropic Claude assistance; Apache-2.0."""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(1, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code'))
from census import *


import random as _random
_R = _random.Random(int(os.environ.get('SEED', '1')) + 7)


def reduce_vec(x, basis):
    """basis: dict hb -> (vec, combo mask over donor slots); returns (residual, combo)"""
    cm = 0
    while x:
        hb = x.bit_length() - 1
        if hb not in basis: return x, cm
        bv, bc = basis[hb]; x ^= bv; cm ^= bc
    return 0, cm


def plan_E(E, G, dread, first, d, chi, avail_p, avail_d, donor_at):
    e = d(E)
    def dcost(h):
        if h in donor_at: return 0.0 if donor_at[h] == E else None
        return chi(e) + chi(d(first[h]) - e) - chi(d(first[h]))
    def pgain(h): return chi(d(first[h])) - chi(d(first[h]) - e)
    mem = []
    for h in G:
        dc = dcost(h) if (h in avail_d or donor_at.get(h) == E) else None
        pg = pgain(h) if h in avail_p else None
        if dc is None and pg is None: continue
        mem.append((h, dc, pg))
    # order: cheap donors first; among equal, lower pivot gain first (keep high-gain members as pivots)
    pz = float(os.environ.get('PNOISE', '0'))
    mem.sort(key=lambda t: ((t[1] * (1 + pz * _R.random()) if pz else t[1]) if t[1] is not None else 1e9, t[2] if t[2] is not None else -1))
    basis = {}; slots = []; piv = []
    for h, dc, pg in mem:
        r, cm = reduce_vec(dread[h], basis)
        if r == 0 and pg is not None and pg > 0:
            piv.append((h, cm, pg))
        elif r and dc is not None:
            k = len(slots); slots.append((h, dc)); basis[r.bit_length() - 1] = (r, cm ^ (1 << k))
            # keep basis reduced-ish: fine for correctness (combos track exact donor sets)
    if not piv: return None
    # prune: a pivot is worth it only if its donors' costs are covered; iterative pruning
    used = {}
    for h, cm, pg in piv:
        for k in range(len(slots)):
            if cm >> k & 1: used.setdefault(k, []).append(h)
    gain = sum(pg for _, _, pg in piv); cost = sum(slots[k][1] for k in used)
    keep = list(piv)
    while keep:
        # drop pivot whose removal frees the most cost relative to its gain
        best = None
        for i, (h, cm, pg) in enumerate(keep):
            freed = sum(slots[k][1] for k in range(len(slots)) if cm >> k & 1 and len(used[k]) == 1)
            if freed > pg and (best is None or freed - pg > best[0]): best = (freed - pg, i)
        if best is None: break
        h, cm, pg = keep.pop(best[1])
        for k in range(len(slots)):
            if cm >> k & 1:
                used[k].remove(h)
                if not used[k]: del used[k]
    gain = sum(pg for _, _, pg in keep); cost = sum(slots[k][1] for k in used)
    if gain - cost <= 1e-15: return None
    entries = [(h, [slots[k][0] for k in range(len(slots)) if cm >> k & 1]) for h, cm, pg in keep]
    return gain - cost, entries


def select(c, M, a, maxentries=10**9, exclude=()):
    d = M.L.dim; v = c["v"]; m = int(os.environ.get("MW", "72"))
    chi = lambda r: 0.0 if r <= 0 else r * (math.exp(a * math.log(m / r)) - 1)
    dread, first = census(c, M); ret = set(c['ret']) | set(exclude)
    H = [h for h in first if h not in ret]
    cand = candidates(c, M, first, ret)
    groups = {E: [h for h in H if E & ~first[h] == 0] for E in cand}
    avail_p = set(H); avail_d = set(H); donor_at = {}
    chosen = []; total = 0.0
    import heapq
    plans = {}
    import random
    NZ = float(os.environ.get('NOISE', '0')); rng = random.Random(int(os.environ.get('SEED', '1'))); fac = {}
    def refresh(E):
        plans[E] = plan_E(E, groups[E], dread, first, d, chi, avail_p, avail_d, donor_at)
        fac[E] = 1 + NZ * rng.random()
    for E in sorted(cand): refresh(E)
    while len(chosen) < maxentries:
        best = max((p[0] * fac[E], E) for E, p in plans.items() if p) if any(plans.values()) else None
        if not best: break
        _, E = best; g, ents = plans[E]
        for p, D in ents:
            chosen.append((E, p, D)); avail_p.discard(p); avail_d.discard(p)
            for x in D:
                donor_at[x] = E; avail_p.discard(x); avail_d.discard(x)
        total += g
        touched = {p for p, _ in ents} | {x for _, D in ents for x in D}
        for E2 in sorted(cand):
            if plans.get(E2) is not None or E2 == E:
                if any(h in touched for h in groups[E2]): refresh(E2)
    return chosen, total, first


def apply(c, chosen, L):
    c = json.loads(json.dumps(c)); v = c['v']; n = 2 * v + c['R']; FULL = (1 << v) - 1
    fl = c['frames']; key = {}
    for k, fr in enumerate(fl): key.setdefault(sum(1 << i for i in fr), k)
    def fid(mk):
        if mk not in key: key[mk] = len(fl); fl.append([i for i in range(v) if mk >> i & 1])
        return key[mk]
    piv = {p: E for E, p, D in chosen}
    for p, E in piv.items(): c['start'][p] = fid(E)
    c['D'] = [[f, t, [s for s in srcs if s not in piv]] for f, t, srcs in c['D']]
    byd = {}
    for E, p, D in chosen:
        for x in D: byd.setdefault((x, E), []).append(p)
    head = [[fid(E), x, sorted(ps)] for (x, E), ps in sorted(byd.items())]
    tail = [[fid(FULL), x, sorted(ps)] for (x, E), ps in sorted(byd.items())]
    c['A'] = head + c['A']; c['C'] = c['C'] + tail
    return c


if __name__ == '__main__':
    c = load_word(sys.argv[1]); M = Model(c)
    p0 = price_word(c); a = float(p0['c'])
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    chosen, tot, first = select(c, M, a, mx)
    d = M.L.dim
    print('entries', len(chosen), 'chi gain %.6f' % tot, 'entrance ranks', Counter(d(E) for E, p, D in chosen),
          'donors', len({x for E, p, D in chosen for x in D}), 'donors/entry', Counter(len(D) for E, p, D in chosen))
    w = apply(c, chosen, M.L)
    json.dump([[E, p, D] for E, p, D in chosen], open(sys.argv[2] + '.sel.json', 'w'))
    save_word(w, sys.argv[2])
