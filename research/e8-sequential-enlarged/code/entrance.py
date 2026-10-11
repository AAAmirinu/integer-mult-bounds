"""Own re-implementation of Dugongue's PR #401 entrance-gauge construction (read as data; none of #401's scripts run).
For each of the 26 plans a new frame E (the plan's F2 basis) is registered; every pivot starts at E, and the unit
entrance shears h_d += c*h_p (donor d, pivot p, at frame E) are prepended to A, grouped by (donor, frame) in sorted
order with unit numerators.  The result must equal #401's frozen candidate (sha256 3b78069c...)."""
import copy, hashlib, json, os, sys
from fractions import Fraction as Q
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cxkernel import rehist
CANDIDATE_SHA256 = '3b78069c4ce032e95f757a2f79fa5557af923c947430b638b0eb6859be659866'


def build(base, sel):
    r = copy.deepcopy(base); head = defaultdict(list); ext = []
    for plan in sel['plans']:
        fid = len(r['frames']); r['frames'].append(plan['basis'])
        for e in plan['pivots']:
            p = e['pivot']; assert r['start'][p] == 0; r['start'][p] = fid; ext.append([p, fid])
            for d, a in e['coefficients'].items():
                a = Q(str(a)).limit_denominator(10000); assert a.denominator in (1, 2)
                head[int(d), fid].append([p, a.numerator, a.denominator])
    gates = []
    for (d, f), terms in sorted(head.items()):
        for p, a, b in sorted(terms): gates += [['in', f, d, [[p, 1 if a > 0 else -1, b]]] for _ in range(abs(a))]
    assert len(gates) == 240 and len(ext) == 119
    r['A'] = gates + r['A']; r['ext'] = sorted(ext)
    r = rehist(r)
    assert hashlib.sha256(json.dumps(r, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == CANDIDATE_SHA256
    return r
