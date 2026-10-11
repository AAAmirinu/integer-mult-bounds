"""Reject materializing the unweighted tensor kernel on the scalar P-grid.

The dense toy really checks its full 64-by-64 operator. The enormous legal
parameter rows are symbolic exponent certificates, not tensor executions.
"""
from fractions import Fraction as Q
from itertools import product
from math import prod
from branchfree import factors, rounded


def run():
    n, dimensions, bits, target = 4, 3, 14, 8
    q = Q(1, 1 << (n+1))
    weights = [Q(1, 1 << (j*(n-j))) for j in range(n)]
    _, h = factors(q, n)
    labels = list(product(range(n), repeat=dimensions))
    errors = {}
    erased = 0
    for work in (bits, 30):
        maxrow = Q(0)
        for i in labels:
            row = Q(0)
            for j in labels:
                kernel = prod((h[b-a] for a, b in zip(i, j)), start=Q(1)) if all(a <= b for a, b in zip(i, j)) else Q(0)
                ratio = prod((weights[a]/weights[b] for a, b in zip(i, j)), start=Q(1))
                got = rounded(kernel, work)*ratio
                exact = kernel*ratio
                row += abs(got-exact)
                if work == bits and got == 0 and abs(exact) > Q(1, 1 << target):
                    erased += 1
            maxrow = max(maxrow, row)
        errors[str(work)] = str(maxrow)
    assert Q(errors[str(bits)]) > Q(1, 1 << target)
    assert erased > 0
    assert Q(errors['30']) < Q(1, 1 << target)
    guard = (max(weights)/min(weights))**dimensions
    assert len(labels)*guard*Q(1, 1 << 30) < Q(1, 1 << target)

    # Universal bounds in the appendix use X=2^(3a)>=128 and a>=26.
    weighted_ratio_bound = (Q(8)+Q(1,2048)+Q(7,128))/128+Q(1,128**2)
    assert weighted_ratio_bound < Q(1,8)
    assert Q(3*2**26,4096)-Q(1,2) > 32768
    assert 2**26 > 8+Q(1,2048)+9
    rows = []
    for a in (26,27,32,64):
        m, x, p = 1 << (4*a), 1 << (3*a), 1 << (10*a)
        d, u = m, m
        dimensions = d-1
        w, k, work = 4*x+2, x//2048, 32768*p
        unweighted_exponent = dimensions*(3*m*k-1)
        weighted_exponent = 16*dimensions*k*(2*w+k+3)+dimensions+1
        assert unweighted_exponent > work
        assert weighted_exponent < p//8
        assert d-2 > 2*w+k+3 and u*d <= p
        assert u >= 3+10*a
        assert (w-2)**2*u == 16*p
        assert dimensions*k < p
        assert work-16*m-2 >= 100*p
        assert dimensions*(3*p).bit_length() < p
        rows.append(dict(a=a, log2_p=10*a, log2_u=4*a, log2_d=4*a,
                         work_precision_ratio=32768,
                         unweighted_exponent_over_work=str(Q(unweighted_exponent,work)),
                         weighted_exponent_over_p=str(Q(weighted_exponent,p)),
                         scope='symbolic parameter inequalities only; no payload tensor executed'))
    return dict(dense_toy=dict(shape=[n]*3, operator_entries=len(labels)**2,
                              scalar_target_bits=target, failed_work_bits=bits,
                              accepted_work_bits=30, erased_significant_entries=erased,
                              operator_error_by_precision=errors,
                              scope='small rational geometry; not the asymptotic p>=101 setting'),
                symbolic_rows=rows,
                uniform_weighted_ratio_bound=str(weighted_ratio_bound),
                claim='P-grid materialization of the unweighted tensor kernel can fail after reweighting',
                excluded_claims=['no FFT lower bound','no barrier for implicit or adaptive-precision kernels',
                                 'no counterexample to the per-axis evaluator'])
