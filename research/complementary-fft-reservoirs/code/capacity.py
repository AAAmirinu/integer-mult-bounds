"""Literal complete-field layouts and compressed eventual-capacity bounds."""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[3]


def ceil(x):
    return -((-x.numerator)//x.denominator)


def clog(value, base):
    power, count = 1, 0
    while power < value:
        power *= base
        count += 1
    return count


def fields(d, K, G, m, W, active):
    D = d-1
    q0 = clog(W, 2)*clog(2*d, m)
    qF, qB = ceil(Q(2*d*G, K)), ceil(Q(d*G, K))
    opposite = D-active
    assert opposite >= q0+qF+qB
    widths = [('row', q0*K), ('front0', d*G), ('front1', d*G),
              ('front_spectator', (opposite-qB-q0)*K-2*d*G),
              ('active', active*K), ('back', d*G),
              ('back_spectator', qB*K-d*G)]
    start, intervals = 0, {}
    for name, width in widths:
        assert width >= 0
        intervals[name] = (start, start+width)
        start += width
    assert start == D*K
    assert intervals['row'][1] <= intervals['front0'][0]
    assert intervals['front1'][1] <= intervals['active'][0]
    assert intervals['active'][1] <= intervals['back'][0]
    assert q0*K >= clog(W, 2)*clog(d, m)
    result = dict(d=d, K=K, G=G, m=m, W=W, active=active, opposite=opposite,
                  q0=q0, qF=qF, qB=qB, intervals=intervals,
                  address_bits=start, new_coordinate_bits=0)
    audit_fields(result)
    return result


def audit_fields(row):
    intervals = row['intervals']
    occupied = sorted((a, b, name) for name, (a, b) in intervals.items() if a != b)
    assert occupied[0][0] == 0 and occupied[-1][1] == row['address_bits']
    assert all(a < b for a, b, name in occupied)
    assert all(left[1] == right[0] for left, right in zip(occupied, occupied[1:]))
    assert row['address_bits'] == (row['d']-1)*row['K'] and row['new_coordinate_bits'] == 0
    for name in ('front0', 'front1', 'back'):
        a, b = intervals[name]
        assert b-a == row['d']*row['G']
    assert intervals['active'][1]-intervals['active'][0] == row['active']*row['K']
    assert intervals['row'][1] <= intervals['front0'][0]
    assert intervals['front1'][1] <= intervals['active'][0]
    assert intervals['active'][1] <= intervals['back'][0]
    assert intervals['row'][1]-intervals['row'][0] >= clog(row['W'], 2)*clog(row['d'], row['m'])


def top_fields(n, d, K, G, m, W, f):
    assert 0 <= f <= d
    row = clog(W, 2)*clog(2*d, m)*K
    needed = row+3*d*G+f*K
    assert needed <= n
    intervals, start = {}, 0
    for name, width in [('row', row), ('front0', d*G), ('front1', d*G),
                        ('active', f*K), ('back', d*G), ('remainder', n-needed)]:
        intervals[name] = (start, start+width)
        start += width
    assert start == n and sum(b-a for a, b in intervals.values()) == n
    assert all(b >= a for a, b in intervals.values())
    assert needed-f <= n-f  # all fillers and reservoirs are unselected slots
    return dict(n=str(n), d=d, K=K, G=G, selected_top_bits=f,
                needed_bits=needed, intervals=intervals, new_coordinate_bits=0)


def cutoff(eps, c, B, A=Q(1, 16)):
    """For every L=ceil(log2 p)>=L0, with d=floor(p^eps).

    K=floor(d^c) >= 2^(eps*c*L-4), d/8 >= 2^(eps*L-5).
    For integer t>=4, 2^t>=t^2 (base 4 and induction). The rational
    inequalities below dominate the required linear functions of L.
    They establish a uniform eventual bound, not only one sampled p.
    """
    assert 0 < eps < 1 and 0 < c < 1 and eps*(1+c) < 1 and B >= 1
    e = eps*c
    gap = 1-eps*(1+c)
    assert A > 0
    requirements = [Q(32)/e, Q(4096)/(e*e), Q(16*(3*B+2))/(eps*eps),
                    1+Q(8)/gap, Q(32)]
    top = [(1-e, 9*B/A), (1-eps, Q(126)/A), (gap, Q(3)/A)]
    for power_gap, coefficient in top:
        assert power_gap > 0
        requirements += [16/power_gap, 16*coefficient/power_gap**2]
    L = ceil(max(requirements))
    assert e*L >= 32 and e*e*L/4 >= 1024
    assert eps*L >= 32 and eps*eps*L/4 >= 4*(3*B+2)
    assert gap*(L-1) >= 8
    # Finite compressed consistency control at the cutoff. No 2^L expanded.
    t = (e*L).numerator//(e*L).denominator-4
    u = (eps*L).numerator//(eps*L).denominator-5
    assert t >= 4 and t*t >= 512*L
    assert u >= 4 and u*u >= B*(L+2)+2
    top_controls = []
    for power_gap, coefficient in top:
        z = (power_gap*(L-1)).numerator//(power_gap*(L-1)).denominator
        assert z >= 4 and z*z >= coefficient*L
        assert power_gap**2*L/4 >= coefficient and power_gap*L >= 16
        top_controls.append(dict(power_gap=str(power_gap), linear_coefficient=str(coefficient),
                                 compressed_exponent=str(z)))
    return dict(c=str(c), epsilon=str(eps), ceil_log2_p_cutoff=str(L),
                row_log2_W_upper=B, K_log2_lower=str(t),
                d_over8_log2_lower=str(u), geometry_gap=str(gap),
                address_volume_lower=str(A)+' * p', top_capacity=top_controls,
                uniform_argument='2^t >= t^2 for integer t>=4; linear t lower bounds and positive geometry gap hold for every L>=L0')


def run():
    layouts, top_layouts = [], []
    for logp in (48, 64, 96, 128, 256):
        G = 4*(logp+1)+6
        for logd in (16, 18, 20):
            d = 1 << logd
            K = 64*G
            if K >= d or (d-1)*K >= 1 << logp:
                continue
            q0 = clog(10178, 2)*clog(2*d, 89)
            assert q0+2 <= Q(d, 8)
            for Kactual in (K, K+1, 2*K-1):
                for active in ((d-1)//2, (d-1)-(d-1)//2):
                    row = fields(d, Kactual, G, 89, 10178, active)
                    assert row['q0']+row['qF']+row['qB'] <= Q(11*d, 64)
                    layouts.append(row)
                for f in (1, d//2, d-1, d):
                    n = (d-1)*((1 << logp)//d)
                    top_layouts.append(top_fields(n, d, Kactual, G, 89, 10178, f))
    rejected = []
    try:
        fields(64, 8, 16, 89, 10178, 32)
    except AssertionError:
        rejected.append('insufficient opposite-set capacity')
    else:
        raise AssertionError('bad capacity accepted')
    example = layouts[0]
    corrupted = dict(example, intervals=dict(example['intervals']))
    corrupted['intervals']['front0'] = corrupted['intervals']['row']
    try:
        audit_fields(corrupted)
    except AssertionError:
        rejected.append('row and compact-field alias')
    else:
        raise AssertionError('aliased fields accepted')
    try:
        top_fields(128, 64, 16, 16, 89, 10178, 32)
    except AssertionError:
        rejected.append('insufficient existing top-layout address volume')
    else:
        raise AssertionError('top volume expansion accepted')

    source = ROOT/'research/e8-r740-replica32/code/engines/outer.py'
    spec = importlib.util.spec_from_file_location('retained_outer_engine', source)
    outer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(outer)
    prior = json.loads((ROOT/'research/e8-r715-whole-hosted/EXPECTED.json').read_text())
    a = Q(prior['strict_outer_constraints']['bit_positive'])
    b, k = Q(prior['complex_lower']), Q(prior['kappa'])
    eta = beta = Q(1, 10**18)
    bridge = {'semantic': {'C0': {'base': 2, 'exponent': 210000}, 'strict_literal_gap': 1},
              'rows': {'degree_gap': Q(10**6)-Q(51*20161, 25)}}
    old = outer.assembly(a, b, bridge, k, eta, beta)
    assert {n: str(v) for n, v in old['strict_constraints'].items()} == prior['strict_outer_constraints']
    eps, q = old['parameters']['epsilon'], old['parameters']['q']
    witnesses = []
    for divisor in (2, 4, 16, 1024):
        c = q/divisor
        slacks = dict(old['strict_constraints'])
        slacks.update(c_positive=c, c_below_one=1-c, q_below_reservations=c-q,
                      compact_reservations=c-q, K_geometry=1-eps*(1+c),
                      K_dominates_log=eps*c)
        failed = sorted(n for n, v in slacks.items() if v <= 0)
        assert failed == ['compact_reservations', 'q_below_reservations']
        removed = failed + ['balanced_prefix_above_kappa']
        retained = {n: v for n, v in slacks.items() if n not in removed}
        assert len(retained) == 44 and all(v > 0 for v in retained.values())
        witnesses.append(dict(q=str(q), c=str(c), unchanged_kappa=str(k),
                              old_rejections=failed, removed_obligations=removed,
                              retained_strict_count=44,
                              capacity_cutoffs=[cutoff(eps, c, B) for B in (14, 4000)]))
    for ell in range(2, 257):
        assert Q(2*ell, 4)+1 <= ell
    # Still no improvement to the currently binding seven exponent margins.
    assert max(Q(w['unchanged_kappa']) for w in witnesses) == k
    return dict(status='PASS', literal_layout_count=len(layouts), layouts=layouts,
                top_layout_count=len(top_layouts), top_layouts=top_layouts,
                mutations_rejected=rejected, parameter_witnesses=witnesses,
                unchanged_kappa=str(k), precision_inequalities_checked=255,
                scope='Capacity and retained-constraint arithmetic; no new multiplication exponent or machine-time measurement.')
