"""Recompute the balanced outer inequalities without the assembly module."""
from fractions import Fraction as Q


def outer(c, b):
    eta=beta=Q(1,10**18)
    s=min(c,(1-beta)*b)-Q(1,10**24)
    a=Q(384599,10**10)
    steps=[]
    for _ in range(6):
        old=a
        a=s*(1-s+old)
        gaps=(s-a,1-a-s,1-a-s*(1-old),1-s)
        gap=min(gaps)
        assert old<a<s and a+s<1 and gap>0
        steps.append(dict(gap=str(gap)))
    assert b>a>0
    q=a*(1-2*eta)
    epsilon=(1-eta)/(1+q)
    minimum=epsilon*q
    kappa=Q(minimum.numerator*10**18//minimum.denominator,10**18)
    if kappa==minimum:kappa-=eta
    assert kappa<minimum<=kappa+eta
    reservation=q+eta/4
    alpha=minimum+eta/2
    delta=eta/8
    average=(a+q)/2
    leaf_saving=(1-beta)*b
    slacks={
        'bit_positive':a,'complex_above_bit':b-a,
        'complex_below_one_over32':Q(1,32)-b,
        'beta_positive':beta,'beta_below_one':1-beta,
        'leaf_saving_above_bit':leaf_saving-a,
        'q_positive':q,'q_below_internal':a-q,'q_below_leaf':leaf_saving-q,
        'c_positive':reservation,'c_below_one':1-reservation,
        'q_below_reservations':eta/4,
        'lambda_above_tau':a-average,'lambda_above_sigma':b-average,
        'lambda_above_internal':a-average,'lambda_prime_above_lambda':average-q,
        'compact_leaf':leaf_saving-q,'compact_reservations':eta/4,
        'lambda_prime_below_one':q,'epsilon_positive':epsilon,
        'epsilon_below_one':minimum+eta,'guard_width':minimum+eta,
        'K_geometry':eta*(1-epsilon/4),'K_dominates_log':epsilon*reservation,
        'record_suffix':minimum+eta,'phase_local':minimum+7*eta/8,
        'phase_boundary':minimum+3*eta/8,'gamma_sublinear':eta/2,
        'cell_above_band':epsilon-(1-alpha)/2,
        'prime_interval_packing':minimum+eta,'alpha_positive':alpha,
        'alpha_below_one':1-alpha,'alpha_below_one_fourth':Q(1,4)-alpha,
        'delta_positive':delta,'delta_below_one_eighth':Q(1,8)-delta,
        'short_record_fallback':epsilon-a,'small_field_exposure':eta,
        'artificial_boundary':8-epsilon+alpha-delta-minimum,
        'literal_scalar_guard':Q(1),'row_product_gap':Q(10**6)-Q(51*20161,25)}
    margins={'balanced_prefix':minimum+eta,'coordinate_movement':a,
        'compact_phase_layer':minimum,'bulk_exposure':a,
        'Gaussian_arithmetic':minimum+3*eta/8,'scalar_work':minimum+7*eta/8,
        'dimension':epsilon}
    slacks.update({key+'_above_kappa':value-kappa for key,value in margins.items()})
    assert len(slacks)==47 and all(v>0 for v in slacks.values())
    assert minimum==min(margins.values()) and minimum-kappa<=eta
    return dict(kappa=kappa,bootstrap=steps,strict_outer_constraints=slacks,
                effective_bit=a,supplier_backoff=s,minimum_margin=minimum,
                binding_component='bit' if c<(1-beta)*b else 'complex')
