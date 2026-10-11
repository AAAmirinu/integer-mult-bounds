"""Independent dense residuals, genuine Gaussian Schur cases and layout controls."""
from copy import deepcopy
from fractions import Fraction as Q
from itertools import product as cartesian
from pathlib import Path
import sys

from batched import compile_coupling, coupling, counter, grid, prepare, product, solve, strassen

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO/'references/semantic-bulk/rad20/code'))
from review_banded_inverse import inverse, multiply, norm


def max_entry(a):
    return max((abs(x) for row in a for x in row), default=Q(0))


def sub(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def outward(x, bits=144):
    return str(Q(-(-(x*(1 << bits)).numerator//(x*(1 << bits)).denominator), 1 << bits))


def gap(a):
    return min(row[i]-sum((abs(x) for j, x in enumerate(row) if j != i), Q(0))
               for i, row in enumerate(a))


def signed_case(n, width, near=False):
    a = [[Q(i == j) for j in range(n)] for i in range(n)]
    for i in range(n):
        for d in range(1, width+1):
            for sign in (-1, 1):
                j = (i+sign*d) % n
                a[i][j] = Q(((i*13+j*7)%7)-3, 32*width)
    if near:
        # Disjoint nearly singular wrapped pairs attain a large inverse norm.
        a = [[Q(i == j) for j in range(n)] for i in range(n)]
        pairs = [(0, n-1)]+[(i, i+1) for i in range(1, n-2, 2)]
        for i, j in pairs:
            a[i][j] = a[j][i] = 1-Q(1, 1 << 20)
    assert gap(a) > 0 and norm(a) < 2
    return a


def gaussian_schur(s, t, u, w, bits):
    """Reconstruct the pinned rounded H, then independently eliminate interiors."""
    from downstream_banded_inverse import nearest_data, phi
    from downstream_blocked_gaussian import gaussian_interval, pi_interval
    from downstream_phase_inverse import cells_for
    rho, beta = nearest_data(s, t)
    cells = cells_for(s, t)
    assert all(len(c) > 2*w for c in cells)
    pi = pi_interval(bits+64)
    cache = {}
    def lower(f):
        if f not in cache:
            lo, hi = gaussian_interval(f, pi, bits+24)
            assert hi-lo < Q(1, 1 << bits)
            value = lo*(1 << bits)
            cache[f] = Q(value.numerator//value.denominator, 1 << bits)
        return cache[f]
    fs = [u*(Q(1, 4)-x*x)/(rho-1) for x in beta]
    weights = [lower(f) for f in fs]
    assert min(weights) > 0
    kernel = [Q(1)]+[lower(u*rho*j*j) for j in range(1, w+1)]
    owner = {j: i for i, cell in enumerate(cells) for j in cell}
    a = [[Q(i == j) for j in range(s)] for i in range(s)]
    identities = 0
    for i in range(s):
        for d in range(-w, w+1):
            if not d:
                continue
            j = (i+d) % s
            f = u*phi(rho, beta, i, d)
            if owner[i] == owner[j] and abs(i-j) <= w:
                assert f == u*rho*d*d+fs[i]-fs[j]
                a[i][j] = weights[i]*kernel[abs(d)]/weights[j]
                identities += 1
            else:
                a[i][j] = lower(f)
    boundary = [j for cell in cells for j in cell[:w]+cell[-w:]]
    interior = [j for j in range(s) if j not in boundary]
    take = lambda rows, cols: [[a[i][j] for j in cols] for i in rows]
    ii = inverse(take(interior, interior))
    bi, ib = take(boundary, interior), take(interior, boundary)
    schur = sub(take(boundary, boundary), multiply(multiply(bi, ii), ib))
    assert gap(schur) >= gap(a) > 0
    assert all(schur[i][j] == 0 for i in range(len(boundary)) for j in range(len(boundary))
               if min(abs(i-j), len(boundary)-abs(i-j)) > 2*w)
    return schur, dict(a=a, ii=ii, bi=bi, ib=ib, boundary=boundary, cells=cells,
                       interior=interior, identities=identities, gaussian_values=len(cache))


def check_solve(name, a, width, bits=192):
    n = len(a)
    b = [[Q(i == j) for j in range(n)]+[Q((i*17)%23-11, 8), Q(1)] for i in range(n)]
    exact = multiply(inverse(a), b)
    table = prepare(a, width, bits)
    count = counter()
    got = solve(table, b, count)
    err = max_entry(sub(got, exact))
    residual = max_entry(sub(multiply(a, got), b))
    assert err <= residual/gap(a)
    assert err < Q(1, 1 << 96)
    # Algebraic verification of the complete unrounded blocked program.
    exact_table = prepare(a, width, None)
    exact_count = counter()
    assert solve(exact_table, b, exact_count) == exact
    h = table['h']
    assert count['scalar_products'] == count['tiles']*7**(h.bit_length()-1)
    return dict(name=name, dimension=n, bandwidth=width, block_width=h,
                rhs=n+2, work_bits=bits, entries=n*(n+2), gap=str(gap(a)),
                inverse_norm_upper=outward(norm(inverse(a))),
                error_upper=outward(err), residual_upper=outward(residual),
                counter=count), (table, b, exact)


def full_schur(a, case, width, bits=192):
    from batched import grid
    n = len(case['a'])
    b = [[Q(i == j) for j in range(n)]+[Q((i*11)%17-8, 8)] for i in range(n)]
    bi = [b[i] for i in case['interior']]
    bb = [b[i] for i in case['boundary']]
    local = multiply(case['ii'], bi)  # Exact local reference, NOT a new GS claim.
    h = 1 << (width-1).bit_length()
    count = counter()
    bg = [[j for j, i in enumerate(case['boundary']) if i in cell] for cell in case['cells']]
    ig = [[j for j, i in enumerate(case['interior']) if i in cell] for cell in case['cells']]
    bp = compile_coupling(case['bi'], bg, ig, h, bits)
    ip = compile_coupling(case['ib'], ig, bg, h, bits)
    assert coupling(bp, local, counter()) == grid(multiply(grid(case['bi'], bits), local), bits)
    rhs = grid(sub(bb, coupling(bp, local, count)), bits)
    xb = solve(prepare(a, width, bits), rhs, count)
    xi = multiply(case['ii'], sub(bi, coupling(ip, xb, count)))
    got = [[Q(0)]*len(b[0]) for _ in range(n)]
    for i, row in zip(case['boundary'], xb):
        got[i] = row
    for i, row in zip(case['interior'], xi):
        got[i] = row
    expected = multiply(inverse(case['a']), b)
    err = max_entry(sub(expected, got))
    assert err < Q(1, 1 << 80)
    return dict(dimension=n, rhs=n+1, compared_entries=n*(n+1),
                error_upper=outward(err), local_inverse='exact dense reference',
                boundary_and_couplings='rounded batched products',
                coupling_pages=len(bp['pages'])+len(ip['pages']),
                coupling_max_page_entries=max(len(p['rows'])*len(p['cols']) for p in bp['pages']+ip['pages']))


def layout_checks():
    """Actual stable binary partitions on complete records; undo each move."""
    cases = entries = moves = 0
    for axis, spectator, h, tail in cartesian((5, 8, 11), (9, 16, 19), (2, 4, 8), (1, 3)):
        padded = 1 << (spectator-1).bit_length()
        assert padded % h == 0
        # One spectator field is padded; original values retain unique labels.
        original = [(a, b, c) if b < spectator else None
                    for a in range(axis) for b in range(padded) for c in range(tail)]
        # Move axis past the high spectator bits. Each stable split moves one
        # complete binary field across the entire axis without random lookup.
        groups = [original]
        high_bits = (padded//h).bit_length()-1
        for bit in reversed(range(high_bits)):
            new = []
            # Maintain explicit coordinates alongside padded-zero records.
            # At each level the current spectator high-bit prefix is fixed.
            group_span = padded >> (high_bits-1-bit)
            for group in groups:
                half = group_span//2
                left, right = [], []
                for a in range(axis):
                    chunk = group[a*group_span*tail:(a+1)*group_span*tail]
                    left.extend(chunk[:half*tail])
                    right.extend(chunk[half*tail:])
                new.extend([left, right])
                moves += len(group)
            groups = new
        got = [x for group in groups for x in group]
        expected = [(a, block*h+b, c) if block*h+b < spectator else None
                    for block in range(padded//h) for a in range(axis)
                    for b in range(h) for c in range(tail)]
        assert got == expected
        # Reverse the exact two-tape split chronology by complete chunk merges.
        for level in reversed(range(high_bits)):
            group_span = padded >> level
            half = group_span//2
            merged = []
            for i in range(0, len(groups), 2):
                left, right = groups[i:i+2]
                merged.append([x for a in range(axis)
                               for chunk in (left[a*half*tail:(a+1)*half*tail],
                                             right[a*half*tail:(a+1)*half*tail]) for x in chunk])
            groups = merged
        assert groups == [original]
        assert padded < 2*spectator
        cases += 1
        entries += len(original)
    return dict(cases=cases, padded_records=entries, forward_record_moves=moves,
                checked_inverse=True, one_field_padding=True)


def mutations(table, b, exact):
    tests = []
    def reject(name, t, rhs=b):
        got = solve(t, rhs, counter())
        discrepancy = max_entry(sub(got, exact))
        scaled = discrepancy*(1 << 80)
        lower = Q(scaled.numerator//scaled.denominator, 1 << 80)
        assert lower > Q(1, 1 << 60), name
        tests.append(dict(name=name, discrepancy_lower=str(lower)))
    t = deepcopy(table)
    for block in t['low']['blocks']:
        block['a'] = [[-x for x in row] for row in block['a']]
    reject('wrong-forward-transfer-sign', t)
    t = deepcopy(table)
    t['support'] = []
    reject('omit-cyclic-correction', t)
    t = deepcopy(table)
    t['ki'] = list(reversed(t['ki']))
    reject('wrong-border-order', t)
    t = deepcopy(table)
    for block in t['high']['blocks']:
        block['c'] = list(map(list, zip(*block['c'])))
    reject('transpose-diagonal-inverse', t)
    reject('wrong-rhs-row-order', table, list(reversed(b)))
    t = deepcopy(table)
    t['bits'] = t['low']['bits'] = t['high']['bits'] = 16
    reject('insufficient-output-precision', t)
    return tests


def run():
    multiplication = []
    for n in (1, 2, 4, 8, 16):
        a = [[Q((i*7+j*11)%13-6, 8) for j in range(n)] for i in range(n)]
        b = [[Q((i*5-j*3)%17-8, 16) for j in range(n)] for i in range(n)]
        count = counter()
        assert strassen(a, b, count) == multiply(a, b)
        assert count['scalar_products'] == 7**(n.bit_length()-1)
        assert count['scalar_additions'] == 6*(count['scalar_products']-n*n)
        multiplication.append(dict(n=n, entries=n*n, **count))
    cases = []
    mut_source = None
    for n, w in ((4, 2), (6, 3), (8, 4), (5, 1), (9, 2), (17, 3), (24, 4)):
        for near in (False, True):
            row, sources = check_solve(f'signed-{n}-{w}-{near}', signed_case(n, w, near), w)
            cases.append(row)
            if (n, w, near) == (17, 3, False):
                mut_source = sources
    row, _ = check_solve('identity-no-wrap', [[Q(i == j) for j in range(9)] for i in range(9)], 2)
    cases.append(row)
    gaussian, compositions = [], []
    for s, t, u, w in ((24, 26, 4, 1), (48, 50, 4, 2)):
        raw, ctx = gaussian_schur(s, t, u, w, 256)
        a = grid(raw, 256)
        assert gap(a) > gap(raw)/2
        row, _ = check_solve(f'gaussian-{s}-{t}-{u}-{w}', a, 2*w, 256)
        row.update(source_shape=[s, t, u, w], gaussian_values=ctx['gaussian_values'],
                   phase_identities=ctx['identities'])
        gaussian.append(row)
        compositions.append(full_schur(a, ctx, 2*w, 256))
    # Exact dyadic exponent certificate: log_2(7)<45/16.
    assert 7**16 < 2**45
    # Uniform inequalities after the elementary p<=2^p bound, p>=101.
    assert 35+9*101-32768*101 < -1
    assert 10-32*101 < -2 and 209-64*101 < -2 and 11-64*101 < -2
    exponent_rows = []
    for r in (Q(1, 1000000), Q(1, 1000), Q(1, 20), Q(1, 5)):
        old, new = r, 1-Q(29, 32)*(1-r)
        assert new-old == Q(3, 32)*(1-r) > 0
        exponent_rows.append(dict(r=str(r), old_boundary_margin=str(old),
                                  new_boundary_margin=str(new)))
    return dict(strassen=multiplication, cyclic_cases=cases, gaussian_cases=gaussian,
                complete_schur=compositions, layouts=layout_checks(),
                rejected_mutants=mutations(*mut_source), exponent_rows=exponent_rows,
                scalar_exponent_upper='45/16', boundary_exponent='29*(1-r)/32',
                kappa_claim=None, all_size_status='conditional written transfer; not finite proof')


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
