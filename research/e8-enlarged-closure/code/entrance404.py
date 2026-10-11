"""Own re-implementation of Dugongue's PR #404 word (read as data; none of #404's scripts are run):
  shared(): the 194 shared-donor entrance gauges of shared/selection194.json on #398's signed781 word (pivots start at
            their entrance frame; unit shears h_d += c*h_p sorted by (entrance dimension, frame, donor, term));
  dual():   #404's 124/125 output-basis recovery (setup 125 -= 124 at frame 0, 125's frame-485 feed of helper 358
            dropped, restore 125 += 124 after its frame-904 feed);
  frame376(): #376's frame edit target201 += helper491/2 at frame 203 -> 942.
build() must reproduce #404's frozen hashes after dual() (65b0f9dd...) and after frame376() (d18ccdc5...)."""
import copy, hashlib, json, sys, os
from fractions import Fraction as Q
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cxkernel import rehist
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'complex', 'gx')); import gxcore as G
FINAL_SHA = 'd18ccdc580e78bde51575daec812cdbfaa92d1a700bf4d6a140b028f0424325a'
DUAL_SHA = '65b0f9dd2b233a0337c443e944529e6d85f35481672f3c1f0f815c158fb2e211'
def sha(c): return hashlib.sha256(json.dumps(c, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
def inside(a, b):
    return all(G.reduce(u, b) == 0 for u in a)
def shared(base, sel):
    c = copy.deepcopy(base); pivs = set(); seln = []
    for plan in sel['plans']:
        e = plan['basis']; dim = len(e)
        f = next((i for i, a in enumerate(c['frames']) if len(a) == dim and inside(e, a)), len(c['frames']))
        if f == len(c['frames']): c['frames'].append(e)
        for entry in plan['pivots']:
            p = entry['pivot']; assert p not in pivs and base['start'][p] == 0; pivs.add(p)
            cm = {int(r): Q(str(x)).limit_denominator(10000) for r, x in entry['coefficients'].items()}
            seln.append((f, p, cm)); c['start'][p] = f
    unit = []
    for f, p, cm in seln:
        for d, a in cm.items(): unit += [['in', f, d, [[p, 1 if a > 0 else -1, a.denominator]]] for _ in range(abs(a.numerator))]
    unit.sort(key=lambda g: (len(c['frames'][g[1]]), g[1], g[2], g[3]))
    c['A'] = unit + base['A']; c['ext'] = sorted([p, f] for f, p, _ in seln)
    return rehist(c), len(unit), seln
def dual(z):
    assert z['B'][860] == ['in', 485, 125, [[358, 1, 2]]] and z['B'][1164] == ['in', 904, 125, [[367, 1, 2]]]
    n = copy.deepcopy(z)
    n['B'].insert(1165, ['in', 904, 125, [[124, 1, 1]]]); n['B'].pop(860); n['B'].insert(25, ['in', 0, 125, [[124, -1, 1]]])
    return rehist(n)
def frame376(c):
    b = copy.deepcopy(c); hits = [(part, i) for part in ['A', 'B'] for i, g in enumerate(b[part]) if g == ['in', 203, 201, [[491, 1, 2]]]]
    assert len(hits) == 1; part, i = hits[0]; b[part][i][1] = 942
    return rehist(b)
def build(base, sel):
    c, nu, seln = shared(base, sel); assert nu == 484 and len(c['ext']) == 194
    d = dual(c); s1 = sha(d)
    f = frame376(d); s2 = sha(f)
    return f, dict(unit=nu, dual_sha=s1, final_sha=s2, seln=seln)
if __name__ == '__main__':
    base = json.load(open(sys.argv[1])); sel = json.load(open(sys.argv[2]))
    f, info = build(base, sel); print(info['dual_sha'] == DUAL_SHA, info['final_sha'] == FINAL_SHA, info['final_sha'][:12])
