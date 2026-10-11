"""Pivot-selection data for the exact kernel certificate (matroid formulation): a word is split into primitive gates and retimed
exactly as by the kernel step (PR #436 retime); for every non-retained helper h: its frame-line list fl(h) (frame lines inside its
first nonzero frame: the rank-1 entrance classes it may join) and its response resp(h) (the targets whose dirt compensation reads
it).  A selection assigns each candidate to one class; a class with members S yields |S| - rank(resp(S)) pivots, so the maximum
number of pivots is |C| - (min over assignments of the summed class ranks): a min-sum-rank list partition.  The linear matroid
splits into connected components (fundamental circuits), solved separately by code/exactgen.py.
usage: pivot_data.py REPO_RESEARCH_DIR WORD OUT_DATA.json OUT_COMPS.json
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code (matroid formulation and components from the
project's matroid scout).  Apache-2.0."""
import os, sys, json, copy
os.environ['E8COORD'] = 'ham'
R, src, out_data, out_comps = sys.argv[1:5]
P443 = os.path.join(R, 'e8-r740-replica32')
sys.path[:0] = [P443 + '/code', P443 + '/parent436/code/bit/producer', P443 + '/parent436/code/reuse']
from e8core import load_word, Lat, to_masks
from stages import occurrences
import retime as RT
w = load_word(src); prim = copy.deepcopy(w)
for ph in ('D', 'A', 'B', 'C'): prim[ph] = [[f, d, [s]] for f, d, ss in w[ph] for s in ss]
ret, mv = RT.retime(prim, sweeps=6, M=64)
L = Lat(ret['lines']); masks = to_masks(ret, L); v = ret['v']; n = 2 * v + ret['R']; occ = occurrences(ret, masks)
gm = {(ph, k): masks[g[0]] for ph in ('D', 'A', 'B', 'C') for k, g in enumerate(ret[ph])}
first = {h: next(x if kind == 'p' else gm[x] for kind, x in occ[h][1:] if (x if kind == 'p' else gm[x]) != 0) for h in range(2 * v, n)}
resp = {h: 0 for h in range(2 * v, n)}
for f, t, ss in ret['D']:
    for s in ss: resp[s] ^= 1 << (t - v)
retset = set(ret['ret']); H = [h for h in range(2 * v, n) if h not in retset]
FRAMEL = [i for i in range(v) if sum(1 for x in ret['lines'][i] if x) == 1]
fl = {h: [i for i in FRAMEL if first[h] >> i & 1] for h in H}; C = [h for h in H if fl[h]]
json.dump(dict(FRAMEL=FRAMEL, H=H, C=C, fl={str(h): fl[h] for h in H}, resp={str(h): resp[h] for h in H}, first={str(h): first[h] for h in H}, v=v, R=ret['R']), open(out_data, 'w'))
par = {h: h for h in C}
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
basis = []
for h in C:
    y, cm = resp[h], {h}
    for bv, bs in basis:
        if y >> (bv.bit_length() - 1) & 1: y ^= bv; cm = cm ^ bs
    if y: basis.append((y, cm)); basis.sort(key=lambda z: -z[0])
    else:
        cm = list(cm)
        for x in cm[1:]:
            a, b = find(cm[0]), find(x)
            if a != b: par[a] = b
comp = {}
for h in C: comp.setdefault(find(h), []).append(h)
comps = sorted(comp.values(), key=len, reverse=True)
json.dump(comps, open(out_comps, 'w'))
print(json.dumps(dict(status='PASS_PIVOT_DATA', R=ret['R'], helpers=len(H), candidates=len(C), rank=len(basis), components=[len(c) for c in comps if len(c) > 1], coloops=sum(1 for c in comps if len(c) == 1))))
