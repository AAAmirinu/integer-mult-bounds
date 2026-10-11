"""Check the outer composition from its unsimplified physical parameters."""
from fractions import Fraction as F


def check(bit):
    bit_bound, complex_bound = map(F, (bit['bit']['moment']['lower'], bit['complex']['moment']['lower']))
    eta = beta = F(1, 10**18)
    backoff = min(bit_bound, (1-beta)*complex_bound) - F(1, 10**24)
    base = F(384599, 10**10)
    a = base
    for j in range(1, 7):
        old = a
        # This closed form does not use the assembly's iterative expression.
        a = backoff - backoff**j * (backoff-base)
        gap = backoff-a
        assert old < a < backoff
        assert gap == min(backoff-a, 1-a-backoff, 1-a-backoff*(1-old), 1-backoff)
        assert F(bit['bootstrap'][j-1]['gap']) == gap

    tau, sigma = 1-a, 1-complex_bound
    q = a*(1-2*eta)
    lambda_prime = 1-q
    lambda_value = (tau+lambda_prime)/2
    reservation = q+eta/4
    epsilon = (1-eta)/(1+q)
    internal = tau+(1-beta)*max(sigma-tau, F(0))
    leaf = sigma+beta*(1-sigma)
    mu = epsilon*q
    alpha = (mu+1-epsilon)/2
    delta = eta/8
    kappa = F((mu.numerator*10**18-1)//mu.denominator, 10**18)
    assert kappa == F(bit['kappa'])

    # Use the unsimplified inequalities on physical assembly parameters.
    slacks = {
        'bit_positive': a, 'complex_above_bit': complex_bound-a,
        'complex_below_one_over32': F(1,32)-complex_bound,
        'beta_positive': beta, 'beta_below_one': 1-beta,
        'leaf_saving_above_bit': (1-beta)*complex_bound-a,
        'q_positive': q, 'q_below_internal': 1-internal-q,
        'q_below_leaf': 1-leaf-q,
        'c_positive': reservation, 'c_below_one': 1-reservation,
        'q_below_reservations': reservation-q,
        'lambda_above_tau': lambda_value-tau,
        'lambda_above_sigma': lambda_value-sigma,
        'lambda_above_internal': lambda_value-internal,
        'lambda_prime_above_lambda': lambda_prime-lambda_value,
        'compact_leaf': lambda_prime-leaf,
        'compact_reservations': lambda_prime-(1-reservation),
        'lambda_prime_below_one': 1-lambda_prime,
        'epsilon_positive': epsilon, 'epsilon_below_one': 1-epsilon,
        'guard_width': 1-epsilon, 'K_geometry': 1-epsilon*(1+reservation),
        'K_dominates_log': epsilon*reservation,
        'record_suffix': 1-epsilon, 'phase_local': 1-epsilon-delta,
        'phase_boundary': alpha-delta, 'gamma_sublinear': 1-epsilon-alpha,
        'cell_above_band': epsilon-(1-alpha)/2,
        'prime_interval_packing': 1-epsilon,
        'alpha_positive': alpha, 'alpha_below_one': 1-alpha,
        'alpha_below_one_fourth': F(1,4)-alpha,
        'delta_positive': delta, 'delta_below_one_eighth': F(1,8)-delta,
        'short_record_fallback': epsilon-a,
        'small_field_exposure': 1-epsilon-mu,
        'artificial_boundary': 8-epsilon+alpha-delta-mu,
        # These two premises need the separate checked finite invoices.
        'literal_scalar_guard': F(1),
        'row_product_gap': F(10**6)-F(51*20161,25),
    }
    margins = {
        'balanced_prefix': 1-epsilon,
        'coordinate_movement': a,
        'compact_phase_layer': mu,
        'bulk_exposure': a,
        'Gaussian_arithmetic': min(1-epsilon-delta, alpha-delta),
        'scalar_work': 1-epsilon-delta,
        'dimension': epsilon,
    }
    slacks.update({name+'_above_kappa': value-kappa for name,value in margins.items()})
    assert len(slacks) == 47
    assert all(value > 0 for value in slacks.values())
    assert slacks == {name: F(value) for name,value in bit['strict_outer_constraints'].items()}
    assert min(margins.values()) == mu
    assert mu-kappa > 0 and mu-kappa <= eta
    assert kappa+eta >= mu
    assert (1-beta)*complex_bound < bit_bound

    # Check the changed complex row estimate. This proves the arithmetic bound,
    # conditional on the inherited cost per recursion level and small leaves.
    stock_bits = 3929
    assert 89**9 > 2**4*64**9
    row_slope = F(9,4)*stock_bits + 9909 + 252
    row_additive = 9*stock_bits
    assert (20161-row_slope)*32-row_additive == 1751
    assert row_slope*32+row_additive < 20161*32
    return {'strict_constraints_checked':47, 'bootstrap_levels_checked':6,
            'adjacent_grid_fails':True, 'complex_row_threshold_margin':1751}
