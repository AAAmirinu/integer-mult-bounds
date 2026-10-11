"""Independent identities, rounded source transfer and complete Schur solves."""
from copy import deepcopy
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import sys
from branchfree import apply, counter, factors, packed_lower, prepare, rounded
from precision_guard import run as precision_guard

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO/'references/semantic-bulk/rad20/code'))
sys.path.insert(0, str(REPO/'research/batched-gaussian-boundary/code'))
from review_banded_inverse import inverse, multiply, norm
from batched import compile_coupling, coupling, grid, prepare as boundary_prepare, solve, counter as boundary_counter
spec = importlib.util.spec_from_file_location('boundary_checks', REPO/'research/batched-gaussian-boundary/code/check.py')
boundary_checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(boundary_checks)


def transpose(a):
    return list(map(list, zip(*a)))


def diff(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def maxentry(a):
    return max((abs(x) for row in a for x in row), default=Q(0))


def outward(x, bits=160):
    scaled = x*(1 << bits)
    return str(Q(-(-scaled.numerator//scaled.denominator), 1 << bits))


def gaussian(q, n, weights=None, cutoff=None):
    weights = weights or [Q(1)]*n
    return [[weights[i]*q**((i-j)**2)/weights[j] if cutoff is None or abs(i-j) <= cutoff else Q(0)
             for j in range(n)] for i in range(n)]


def operator(table):
    n = len(table['f'])
    return transpose([apply(table, [Q(i == j) for i in range(n)], counter()) for j in range(n)])


def identities():
    rows = []
    for n in range(1, 13):
        for q in (Q(1, 4), Q(1, 16), Q(1, 256)):
            f, h = factors(q, n)
            low = [[q**((i-j)**2)*f[i]/(f[j]*f[i-j]) if i >= j else Q(0)
                    for j in range(n)] for i in range(n)]
            lf = [[v*f[j] for j, v in enumerate(row)] for row in low]
            g = gaussian(q, n)
            assert multiply(lf, transpose(low)) == g
            got = operator(prepare(q, [Q(1)]*n, None))
            assert multiply(g, got) == [[Q(i == j) for j in range(n)] for i in range(n)]
            assert got == inverse(g)
            assert min(f) >= Q(14, 15) and sum(map(abs, h)) <= Q(10, 7)
            rows.append(dict(n=n, q=str(q), ldl_entries=n*n, inverse_entries=n*n))
    return rows


def rounded_cases():
    rows = []
    for n in (3, 8, 17, 24):
        for direction in (1, -1):
            # A large similarity guard tests absolute, not relative, error.
            weights = [Q(1, 1 << (5*(i if direction == 1 else n-1-i))) for i in range(n)]
            q, bits = Q(1, 256), 384
            table = prepare(q, weights, bits)
            probes = [[Q(i == j) for i in range(n)] for j in range(n)]
            probes += [[Q((13*i)%19-9, 8) for i in range(n)], [Q(1)]*n]
            ref = inverse(gaussian(q, n, weights))
            count = counter()
            got = transpose([apply(table, v, count) for v in probes])
            exact = multiply(ref, transpose(probes))
            error = maxentry(diff(got, exact))
            assert error < Q(1, 1 << 200)
            assert count['convolutions'] == 2*len(probes)
            assert count['integer_products'] == 8*len(probes)
            # Independently check packing for signed coefficients/data.
            x = probes[-2]
            h = table['h']
            packed = packed_lower(h, x, bits, counter())
            dense = [rounded(sum((h[i-j]*x[j] for j in range(i+1)), Q(0)), bits) for i in range(n)]
            assert packed == dense
            rows.append(dict(n=n, direction=direction, reciprocal_guard_bits=5*(n-1),
                             work_bits=bits, probes=len(probes), entries=n*len(probes),
                             error_upper=outward(error, 240), counts=count))
    return rows


def tensor_and_weighted():
    """Exact algebra/conditioning only; no fast weighted tensor evaluator."""
    def kron(a, b):
        return [[x*y for x in ar for y in br] for ar in a for br in b]
    def diagonal(v):
        return [[x if i == j else Q(0) for j in range(len(v))] for i, x in enumerate(v)]
    tensors = []
    for shape in ((2, 3), (3, 4), (2, 3, 4)):
        stages = [[[Q(1)]] for _ in range(5)]
        expected = [[Q(1)]]
        for axis, n in enumerate(shape):
            q = Q(1, 4**(axis+1))
            f, h = factors(q, n)
            th = [[h[i-j] if i >= j else Q(0) for j in range(n)] for i in range(n)]
            fs = (diagonal([1/x for x in f]), transpose(th), diagonal(f), th, diagonal([1/x for x in f]))
            stages = [kron(old, new) for old, new in zip(stages, fs)]
            expected = kron(expected, inverse(gaussian(q, n)))
        got = stages[0]
        for stage in stages[1:]:
            got = multiply(got, stage)
        assert got == expected
        tensors.append(dict(shape=list(shape), stages=5, entries=len(got)**2))
    weighted = []
    for m in (4, 8, 16):
        for base in (Q(1, 2), Q(3, 4), Q(7, 8)):
            q = base**(m+1)
            if q > Q(1, 4):
                continue
            # theta=1/m, beta=j/m-1/2 and base=exp(-pi*u*theta).
            weights = [base**(j*(m-j)) for j in range(m)]
            f, h = factors(q, m)
            lower = [[weights[i]*h[i-j]/weights[j] if i >= j else Q(0) for j in range(m)] for i in range(m)]
            upper = [[weights[i]*h[j-i]/weights[j] if j >= i else Q(0) for j in range(m)] for i in range(m)]
            bound = Q(15, 14)/(1-base*base)
            assert norm(lower) <= bound and norm(upper) <= bound
            for a in (lower, upper):
                assert all(abs(a[i][j]) <= Q(15,14)*base**(abs(i-j)*(abs(i-j)+1))
                           for i in range(m) for j in range(m))
            invf = diagonal([1/x for x in f])
            got = multiply(multiply(multiply(multiply(invf, upper), diagonal(f)), lower), invf)
            assert got == inverse(gaussian(q, m, weights))
            weighted.append(dict(n=m, base=str(base), entries=2*m*m, norm_upper=outward(bound),
                                 maximum_measured_norm=outward(max(norm(lower), norm(upper)))))
    return dict(tensor_identities=tensors, weighted_factors=weighted,
                scope='exact identities and norm bounds, no fast joint evaluator')


def complete_case(s, t, u, w, bits=256):
    from downstream_banded_inverse import nearest_data
    from downstream_blocked_gaussian import gaussian_interval, pi_interval
    schur, ctx = boundary_checks.gaussian_schur(s, t, u, w, bits)
    rho, beta = nearest_data(s, t)
    pi = pi_interval(bits+64)
    def lower(f):
        lo, hi = gaussian_interval(f, pi, bits+24)
        assert hi-lo < Q(1, 1 << bits)
        return rounded(lo, bits)
    weights = [lower(u*(Q(1, 4)-b*b)/(rho-1)) for b in beta]
    q = lower(u*rho)
    groups = [[j for j, i in enumerate(ctx['interior']) if i in cell] for cell in ctx['cells']]
    tables, models, local_rows = [], [], []
    for group in groups:
        physical = [ctx['interior'][j] for j in group]
        aw = [weights[i] for i in physical]
        table = prepare(q, aw, bits)
        model = gaussian(q, len(group), aw)
        source = [[ctx['a'][i][j] for j in physical] for i in physical]
        # Source is independently rounded AND truncated. It is not the model.
        perturb = norm(diff(model, source))
        assert perturb > 0
        ka = max(aw)/min(aw)
        n = len(group)
        tail = 2*q**((w+1)**2)/(1-q**(2*w+3))
        perturb_bound = ka*(8*n*(n*n+1)*Q(1, 1 << bits)+tail)
        assert perturb <= perturb_bound
        old_inv, new_inv = inverse(source), inverse(model)
        measured = norm(diff(old_inv, new_inv))
        resolvent = norm(old_inv)*norm(new_inv)*perturb
        assert measured <= resolvent
        rounded_op = operator(table)
        round_error = norm(diff(rounded_op, new_inv))
        assert round_error < Q(1, 1 << 120)
        tables.append(table)
        models.append(model)
        local_rows.append(dict(n=n, perturbation_upper=outward(perturb),
                               perturbation_bound=outward(perturb_bound),
                               inverse_difference_upper=outward(measured),
                               resolvent_upper=outward(resolvent),
                               rounded_operator_error_upper=outward(round_error),
                               changed_source=True))
    rhs = [[Q(i == j) for j in range(s)]+[Q((i*11)%17-8, 8), Q(1)] for i in range(s)]
    bi, bb = [rhs[i] for i in ctx['interior']], [rhs[i] for i in ctx['boundary']]
    bc, lc = boundary_counter(), counter()
    def local(b):
        out = [[Q(0)]*len(b[0]) for _ in b]
        for group, table in zip(groups, tables):
            x = transpose([apply(table, col, lc) for col in zip(*(b[i] for i in group))])
            for i, row in zip(group, x):
                out[i] = row
        return out
    width = 2*w
    h = 1 << (width-1).bit_length()
    bg = [[j for j, i in enumerate(ctx['boundary']) if i in cell] for cell in ctx['cells']]
    bp = compile_coupling(ctx['bi'], bg, groups, h, bits)
    ip = compile_coupling(ctx['ib'], groups, bg, h, bits)
    y = local(bi)
    rb = grid(diff(bb, coupling(bp, y, bc)), bits)
    xb = solve(boundary_prepare(schur, width, bits), rb, bc)
    xi = local(grid(diff(bi, coupling(ip, xb, bc)), bits))
    got = [[Q(0)]*len(rhs[0]) for _ in range(s)]
    for i, row in zip(ctx['interior'], xi):
        got[i] = row
    for i, row in zip(ctx['boundary'], xb):
        got[i] = row
    exact = multiply(inverse(ctx['a']), rhs)
    error = maxentry(diff(got, exact))
    residual = maxentry(diff(multiply(ctx['a'], got), rhs))
    assert error <= residual/boundary_checks.gap(ctx['a'])
    assert error < Q(1, 1 << 24)
    # No changed global H or Schur complement is used anywhere above.
    return dict(shape=[s, t, u, w], local_cells=local_rows, rhs=len(rhs[0]),
                entries=s*len(rhs[0]), error_upper=outward(error), residual_upper=outward(residual),
                local_counts=lc, boundary_counts=bc, global_matrix='unchanged truncated H',
                schur='exactly the original H Schur, rounded by the pinned solver')


def mutants():
    n, q, bits = 8, Q(1, 4), 192
    weights = [Q(1, 1 << i) for i in range(n)]
    base = prepare(q, weights, bits)
    exact = inverse(gaussian(q, n, weights))
    rows = []
    for name in ('drop-middle-f', 'reverse-h', 'drop-signs', 'omit-weight-reciprocal'):
        bad = deepcopy(base)
        if name == 'drop-middle-f': bad['f'] = [Q(1)]*n
        if name == 'reverse-h': bad['h'].reverse()
        if name == 'drop-signs': bad['h'] = list(map(abs, bad['h']))
        if name == 'omit-weight-reciprocal': bad['inva'] = [Q(1)]*n
        error = norm(diff(operator(bad), exact))
        assert error > Q(1, 1 << 16)
        rows.append(dict(name=name, discrepancy_lower='1/65536'))
    # The tempting exact-substitution assertion is demonstrably false.
    truncated = gaussian(q, n, weights, cutoff=1)
    residual = norm(diff(multiply(truncated, operator(prepare(q, weights, None))),
                         [[Q(i == j) for j in range(n)] for i in range(n)]))
    assert residual > Q(1, 1 << 16)
    rows.append(dict(name='declare-truncated-source-inverse-exact', discrepancy_lower='1/65536'))
    return rows


def uniform_bounds():
    # Affine exponent differences: slope >= 0 and positive at p=101 proves all p>=101.
    # p^2<=2^p (p>=4), p^k<=2^(kp), and 200<=2p are stated in PROOF.md.
    rows = [
        ('rounded-source term below 2^-40p', 32768-8-3-40, -12),
        ('tail below half 2^-39p', 1, -4),
        ('resolvent smallness 8p*2^-39p<1/2', 38, -4),
        ('inverse perturbation <=2^-37p', 1, -7),
        ('rounded local <=2^-37p', 32768-32-8-37, 0),
        ('composition local <=2^-34p', 1, -10),
        ('boundary composition <=2^-34p', 32768-44-34, 0),
        ('final 2^-32p below 2^-p-10', 31, -10),
    ]
    for _, slope, intercept in rows:
        assert slope >= 0 and slope*101+intercept > 0
    return [dict(name=name, slope=slope, intercept=intercept,
                 gap_at_p101=slope*101+intercept) for name, slope, intercept in rows]


def run():
    return dict(identities=identities(), rounded=rounded_cases(),
                tensor_and_weighted=tensor_and_weighted(),
                tensor_precision_guard=precision_guard(),
                complete_schur=[complete_case(*x) for x in ((24,26,4,1),(48,50,4,2))],
                rejected_mutants=mutants(), uniform_bounds=uniform_bounds(),
                kappa_claim=None,
                scope='local branch-free replacement and retained Schur error transfer; no joint-axis evaluator')


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
