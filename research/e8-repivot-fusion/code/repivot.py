"""Re-pivot one relation of a response-gauge plan: pivot p leaves, donor x (coefficient c in p's relation) becomes the
pivot.  Relations are rows e_p + sum c_d e_d; the new row for x is (row_p)/c, and every other row of the plan that
uses x is reduced by it.  The relation span (hence every zero response column) is unchanged."""
import copy, json
from fractions import Fraction as Q
def rows(plan):
    return {e['pivot']: {**{int(d): Q(str(a)).limit_denominator(10000) for d, a in e['coefficients'].items()}, e['pivot']: Q(1)} for e in plan['pivots']}
def tojson(R, piv):
    out = []
    for p in piv:
        r = R[p]; assert r[p] == 1 and all(r.get(q, 0) == 0 for q in piv if q != p)
        out.append({'pivot': p, 'coefficients': {str(d): (int(a) if a.denominator == 1 else float(a)) for d, a in sorted(r.items()) if d != p and a}})
    return out
def swap(sel, i, p, x):
    sel = copy.deepcopy(sel); plan = sel['plans'][i]; R = rows(plan)
    rp = R.pop(p); c = rp[x]; rx = {d: a / c for d, a in rp.items()}
    for q, r in R.items():
        if r.get(x):
            f = r[x]
            for d, a in rx.items():
                z = r.get(d, 0) - f * a
                if z: r[d] = z
                else: r.pop(d, None)
    R[x] = rx
    piv = [x if e['pivot'] == p else e['pivot'] for e in plan['pivots']]
    plan['pivots'] = tojson(R, piv)
    plan['donors'] = sorted({int(d) for e in plan['pivots'] for d in e['coefficients']})
    return sel
def check_global(sel):
    piv = [e['pivot'] for pl in sel['plans'] for e in pl['pivots']]; don = {int(d) for pl in sel['plans'] for e in pl['pivots'] for d in e['coefficients']}
    assert len(piv) == len(set(piv)) and not set(piv) & don
    assert all(Q(str(a)).limit_denominator(10000).denominator in (1, 2) for pl in sel['plans'] for e in pl['pivots'] for a in e['coefficients'].values())
