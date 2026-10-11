"""Fixed-scalar gate-frame retiming search (own code; idea credited to eumemic #427/#428).  For a single gate, or a
block of gates sharing one frame whose touches are contiguous for every operand, any frame E with
join(incoming operand frames) <= E <= meet(outgoing operand frames) keeps every operand walk nested; the scalar word is
unchanged.  Candidates are scored by the exact moment bound of the changed climb histogram (gain > 0 kept)."""
import copy
from collections import Counter
from cxkernel import inside, echelon
def regs(g): return [g[2]] + [x[0] for x in g[3]] + (list(g[4]) if g[0] == 'out' else [])
def red(u, B):
    for b in B:
        if u >> (b.bit_length() - 1) & 1: u ^= b
    return u
def meet(a, b):
    vals = [0]
    for x in a: vals += [y ^ x for y in vals]
    return echelon([x for x in vals if inside([x], b)])
def subspaces(lo, up, maxq=8):
    lo = echelon(lo); q = []; B = list(lo)
    for u in up:
        x = red(u, echelon(B))
        if x: B.append(x); q.append(x)
    if len(q) > maxq: return []
    vecs = [0]
    for x in q: vecs += [y ^ x for y in vecs]
    out = {tuple(lo)}; frontier = {tuple(lo)}
    for _ in range(len(q)):
        nf = set()
        for S in frontier:
            for v in vecs[1:]:
                E = tuple(echelon(list(S) + [v]))
                if len(E) == len(S) + 1 and E not in out: out.add(E); nf.add(E)
        frontier = nf
    return [list(E) for E in out]
def blocks(W):
    G = W['A'] + W['B']; byf = {}
    for j, g in enumerate(G): byf.setdefault(g[1], []).append(j)
    bl = [[j] for j in range(len(G))] + [v for f, v in byf.items() if len(v) > 1 and f != 0]
    j = 0
    while j < len(G):
        k = j
        while k + 1 < len(G) and G[k + 1][1] == G[j][1]: k += 1
        if k > j: bl.append(list(range(j, k + 1)))
        j = k + 1
    return bl
def search(W, gain):
    """gain(old_climbs, new_climbs) -> exact change of the bound; returns [(gain, block, E)] with gain > 0"""
    G = W['A'] + W['B']; nA = len(W['A']); fr = W['frames']; dim = [len(f) for f in fr]; touches = {}
    for j, g in enumerate(G):
        for r in regs(g): touches.setdefault(r, []).append(j)
    pinned = {max(j for j in touches[r] if j < nA) for _, r, f in W['ret']}
    out = []; seen = set()
    for blk in blocks(W):
        if tuple(blk) in seen or any(j in pinned for j in blk): continue
        seen.add(tuple(blk)); f0 = G[blk[0]][1]; inb = set(blk); lo = []; up = None; ends = []; ok = True
        for r in set(r for j in blk for r in regs(G[j])):
            t = touches[r]; ks = [k for k, j in enumerate(t) if j in inb]
            if ks != list(range(ks[0], ks[-1] + 1)): ok = False; break
            pf = G[t[ks[0] - 1]][1] if ks[0] > 0 else W['start'][r]; nf = G[t[ks[-1] + 1]][1] if ks[-1] + 1 < len(t) else W['final'][r]
            lo = echelon(lo + fr[pf]); up = fr[nf] if up is None else meet(up, fr[nf]); ends.append((pf, nf))
        if not ok or not inside(lo, up): continue
        old = [x for pf, nf in ends for x in (dim[f0] - dim[pf], dim[nf] - dim[f0]) if x]
        for E in subspaces(lo, up):
            if len(E) == dim[f0] and inside(E, fr[f0]): continue
            new = [x for pf, nf in ends for x in (len(E) - dim[pf], dim[nf] - len(E)) if x]
            gn = gain(old, new)
            if gn > 0: out.append((gn, blk, E))
    out.sort(key=lambda x: -x[0]); return out
