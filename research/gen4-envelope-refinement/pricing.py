#!/usr/bin/env python3
"""Exact conditional parameter and fallback-envelope refinement of selected PR279.

Prepared with substantial OpenAI Codex assistance. Apache-2.0.
The two unchanged, pinned moment engines establish arithmetic enclosures;
they do not establish physical realizability or the inherited all-size theorem.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import importlib.util
import json
import sys

if not __debug__:
    raise SystemExit('Assertions required; refusing -O')
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
PACKAGE = 'research/five-stage-gen4-banks/'
SOURCE_PINS = {
    'research/community-pr279-audit/certificate.json': '6a457a34b4db57417e5b253cf1c169da2bd6aff4c21363a31fd85dc931d49589',
    'research/community-pr279-audit/finite.json': '39f63a42b23b2f8820ccca0bc925d0868ffde9c4a35102f2bb5df0953d69a609',
    PACKAGE+'MANIFEST.json': '99e202d9ffe5baf89e02796edbfc7095b2b227622eccf7b61afa01fd61aeb385',
    PACKAGE+'outer.py': 'c1ebb52163a7219504c728a5c2b098bf1e50bf20148a2879c5a74c3cadc7c03c',
    PACKAGE+'moment.py': '9d465c716c6b910ff66e1453e3bf0057608a787b5f5361be93781f42cb3370f7',
    PACKAGE+'base_two_moment.py': 'aee70c242a2f1d225528fabe2002e1564d1dc884797c07d28a831c7878ee9098',
    PACKAGE+'finite_check.py': '693a93308edcb44bc649b33a6ece1de4d93daefcead2eac36215d7c18730edbd',
    PACKAGE+'proof/FINITE_BIT_ACCOUNTING.md': '602923520af184670170bf159fde7b4c72e79a72570eddd7746b7c97bc51fc5b',
    PACKAGE+'proof/three-stage-cover-bit.tex': '47123a756f823c83a0d48cca2bf5add6472cd88410b13aed345e70c8834fb511',
    PACKAGE+'proof/three-stage-cover-rows.tex': '6ad97a5cd7d6aecf978a81226e1c2763d37840caca130c61f3bf5c4ac111c5c8',
}
BASE_KAPPA = Q(90446448750933, 125000000000000000)
BASE_COARSE = Q(181023881305063, 250000000000000000)
BASE_LEAF = Q(384599, 10**10)
Q_MIN = 2**80
DEFAULT_BETA = Q(1, 10**9)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def serial(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return list(map(serial, value))
    return value


def decimal(value):
    with localcontext() as context:
        context.prec = 70
        return str(Decimal(value.numerator)/Decimal(value.denominator))


def pinned_bytes(path, expected):
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == expected, 'Source pin mismatch: '+path.name)
    return raw


def validate_profile(profile):
    m, W = profile['m'], profile['W']
    H = {int(rank): count for rank, count in profile['histogram'].items()}
    require(type(m) is int and type(W) is int and m > 1 and W > 0, 'Invalid profile dimensions')
    require(all(0 < rank < m and type(n) is int and n > 0 for rank, n in H.items()), 'Improper child')
    require(sum(H.values()) == profile['calls'], 'Child count mismatch')
    require(sum(rank*n for rank, n in H.items()) == profile['rank_mass'], 'Rank mass mismatch')
    require(m*W-profile['rank_mass'] == profile['deficit'], 'Profile deficit mismatch')
    require(max(H) == profile['maxchild'], 'Maximum child mismatch')
    return H


def source_inputs(root=ROOT):
    root = Path(root)
    files = {name: pinned_bytes(root/name, digest) for name, digest in SOURCE_PINS.items()}
    certificate = json.loads(files['research/community-pr279-audit/certificate.json'])
    finite = json.loads(files['research/community-pr279-audit/finite.json'])
    bit, complex_profile = certificate['bit_profile'], certificate['complex_profile']
    validate_profile(bit)
    validate_profile(complex_profile)
    require(Q(certificate['kappa']) == BASE_KAPPA and Q(certificate['bit_coarse']) == BASE_COARSE,
            'Unexpected selected witness')
    require((bit['m'], bit['W'], bit['rank_mass'], bit['physical_replicas'], bit['literal_stock'])
            == (120, 256607, 30740040, 60, 1283035), 'Unexpected bit profile')
    require((complex_profile['m'], complex_profile['W'], complex_profile['calls'], complex_profile['rank_mass'])
            == (110, 14692, 361405, 1613040), 'Unexpected complex profile')
    require(bit['literal_children'] == 5*bit['calls'] and bit['literal_rank_mass'] == 5*bit['rank_mass'],
            'Literal realization and normalization detached')
    invoice = finite['paid_inventory']
    require(invoice['extra_bank_selector_calls'] == 502915820400 and
            invoice['literal_stock'] == bit['literal_stock'] and invoice['physical_replicas'] == 60 and
            invoice['positive_rank_children'] == bit['literal_children'] and
            invoice['rank_mass'] == bit['literal_rank_mass'], 'Physical invoice detached')
    coefficient = sum(invoice[name] for name in ('unit_expanded_additions', 'high_affine_factors',
        'low_transposition_coefficient', 'generic_wrappers', 'matrix_preparation',
        'copy_erase_episodes', 'positive_rank_children', 'extra_bank_selector_calls')) + 16*120**3+1
    require(coefficient == finite['q_power_bound']['coefficient'] == 92133599684450401,
            'Incomplete retained primitive invoice')
    require(finite['row_reserve']['external_complex_coefficient'] == certificate['finite_bridge']['rows']['coefficient'] == 20161,
            'External complex row reserve detached')
    require(finite['bootstrap']['chain'] == certificate['ordinary_bootstrap_chain'], 'Detached baseline leaves')
    bridge = dict(certificate['finite_bridge'])
    bridge['rows'] = dict(bridge['rows'])
    bridge['rows']['degree_gap'] = Q(bridge['rows']['degree_gap'])
    return dict(certificate=certificate, finite=finite, bit_profile=bit, complex_profile=complex_profile,
                bridge=bridge, primitive_coefficient=coefficient)


@lru_cache(None)
def engines():
    result = {}
    for name in ('moment', 'base_two_moment', 'outer', 'finite_check'):
        path = ROOT/PACKAGE/(name+'.py')
        pinned_bytes(path, SOURCE_PINS[PACKAGE+name+'.py'])
        spec = importlib.util.spec_from_file_location('gen4_refinement_'+name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result[name] = module
    return result


def envelope(kind, m=120):
    require(m == 120, 'Only the selected bit profile is admitted')
    N = 2*m
    exact = 6*N*(N-1)+3*N+6*(N-1)
    require(exact == 346314, 'Gaussian fallback arithmetic')
    table = {
        'legacy': (32*m*m, Q(1, 10**16), False),
        'exact_fallback': (exact, Q(1, 10**16), False),
        'prime_threshold': (32*m*m, Q(2*m**3, Q_MIN), False),
        'combined': (exact, Q(2*m**3, Q_MIN), False),
        'tight_conditioning': (exact, Q(m**3*(Q_MIN-1), Q_MIN*(Q_MIN-2)), False),
        'disjoint': (exact, Q(m**3*(Q_MIN-1), Q_MIN*(Q_MIN-2)), True),
    }
    require(kind in table, 'Unsupported envelope')
    fallback, bad, disjoint = table[kind]
    return dict(kind=kind, fallback_count=fallback, bad_fraction=bad,
                disjoint_good_bad=disjoint, prime_lower_bound=Q_MIN)


def validate_envelope(spec):
    require(spec == envelope(spec['kind']), 'Unproved envelope parameters')
    require(0 < spec['bad_fraction'] < 1, 'Improper rare fraction')


def validate_dominance(max_rank, fallback_count, coarse):
    require(type(max_rank) is int and max_rank >= 1 and
            type(fallback_count) is int and fallback_count >= max_rank and 0 <= coarse < 1,
            'Fallback need not dominate every good child at the two induction powers')


def moment_bounds(coarse, spec, inputs=None):
    inputs = source_inputs() if inputs is None else inputs
    validate_envelope(spec)
    require(0 <= coarse < 1, 'Moment exponent outside range')
    bp = inputs['bit_profile']; H = validate_profile(bp)
    m, W, calls = bp['m'], bp['W'], bp['calls']
    fallback, bad = spec['fallback_count'], spec['bad_fraction']
    # For each rank r and tau=1-coarse in (0,1), F >= r >= r**tau.
    # Thus the full fallback cost dominates the good child, permitting the
    # per-edge bad-probability bound in the disjoint mixture.
    validate_dominance(bp['maxchild'], fallback, coarse)
    good_factor = 1-bad if spec['disjoint_good_bad'] else Q(1)
    modules = engines()
    good = modules['moment'].moment(H, m, W, coarse, False)
    bad_part = modules['moment'].moment({1: fallback*calls}, m, W, coarse, False)
    independent_good = modules['base_two_moment'].moment(m, W, list(H.items()), coarse)
    independent_bad = modules['base_two_moment'].moment(m, W, [(1, fallback*calls)], coarse)
    combine = lambda g, f: tuple(good_factor*g[i]+bad*f[i] for i in (0, 1))
    return dict(mercator=combine(good, bad_part), base_two=combine(independent_good, independent_bad))


def refine_coarse(spec, grid=10**24, inputs=None):
    inputs = source_inputs() if inputs is None else inputs
    validate_envelope(spec)
    require(grid in (10**18, 10**24), 'Unreviewed coarse grid')
    bp = inputs['bit_profile']; H = validate_profile(bp)
    m, W = bp['m'], bp['W']
    # Decimal only proposes endpoints; both rational engines must enclose
    # strict opposite signs before the candidate is admitted.
    with localcontext() as context:
        context.prec = 70
        D = lambda x: Decimal(x.numerator)/Decimal(x.denominator)
        b = spec['bad_fraction']
        good_factor = 1-b if spec['disjoint_good_bad'] else Q(1)
        terms = [(D(good_factor*Q(r*n, m*W)), D(Q(m, r)).ln()) for r, n in H.items()]
        extra = D(b*Q(spec['fallback_count']*bp['calls'], m*W))
        lm = Decimal(m).ln(); lower, upper = Decimal(0), Decimal('.003')
        for _ in range(210):
            point = (lower+upper)/2
            value = sum(p*(point*l).exp() for p, l in terms)+extra*(point*lm).exp()
            if value < 1:
                lower = point
            else:
                upper = point
        ticks = int(lower*grid)
    coarse = Q(ticks, grid)
    lower_bounds = moment_bounds(coarse, spec, inputs)
    upper_bounds = moment_bounds(coarse+Q(1, grid), spec, inputs)
    require(all(pair[1] < 1 for pair in lower_bounds.values()), 'Coarse endpoint not proved contracting')
    require(all(pair[0] > 1 for pair in upper_bounds.values()), 'Adjacent coarse endpoint not excluded')
    return dict(coarse=coarse, grid=grid, moments=lower_bounds, adjacent_moments=upper_bounds)


def validate_ordinary_step(coarse, old, new):
    require(new == (1-coarse)*coarse+coarse*old, 'Detached ordinary recurrence step')
    ds = dict(atom=coarse-new, borrowing=1-new-coarse,
              remainder=1-new-coarse*(1-old), stock=1-coarse)
    require(old < new < coarse < 1-new and min(ds.values()) > 0, 'Invalid finite ordinary step')
    return ds


def finite_chain(coarse, depth, inputs):
    require(type(depth) is int and 1 <= depth <= 16, 'Only explicit bounded finite depths admitted')
    chain = [BASE_LEAF]; gaps = []
    for j in range(depth):
        old = chain[-1]
        new = (1-coarse)*coarse+coarse*old
        require(new == coarse-coarse**(j+1)*(coarse-BASE_LEAF), 'Finite closed form mismatch')
        ds = validate_ordinary_step(coarse, old, new)
        delta = min(ds.values())
        L = engines()['finite_check'].cutoff_log2(delta, inputs['primitive_coefficient'])
        require(Q(L)*delta**2 >= 36 and Q(L)*delta >= 2*(4+(inputs['primitive_coefficient']-1).bit_length()),
                'Insufficient finite cutoff')
        gaps.append(dict(stage=j+1, gaps=ds, minimum_gap=delta,
            cutoff_log2_at_charged_coefficient=L,
            full_cutoff_rule='Apply the same cutoff(delta,C_full), where C_full bounds the retained coefficient times every inherited primitive, wrapper and preceding fixed-level constant.'))
        chain.append(new)
    return chain, gaps


def validate_ordinary_saving(ordinary, coarse):
    require(BASE_LEAF < ordinary < coarse < 1-ordinary,
            'A completed finite ordinary saving must stay strictly below its coarse rate')


def strict_grid_below(bound, grid):
    require(type(bound) is Q and bound > 0 and type(grid) is int and grid > 0,
            'Positive rational bound and positive integer grid required')
    ticks = bound*grid
    result = Q((ticks.numerator-1)//ticks.denominator, grid)
    require(result < bound <= result+Q(1, grid), 'Incorrect strict grid rounding')
    return result


def build_candidate(coarse, spec, depth, eta, beta=DEFAULT_BETA, headline_grid=10**18, inputs=None):
    inputs = source_inputs() if inputs is None else inputs
    validate_envelope(spec)
    require(type(eta) is Q and eta > 0, 'Positive exact eta required')
    require(type(beta) is Q and 0 < beta < 1, 'Interior exact beta required')
    require(headline_grid in (10**18, 10**24), 'Unreviewed headline grid')
    bounds = moment_bounds(coarse, spec, inputs)
    require(all(pair[1] < 1 for pair in bounds.values()), 'Uncertified coarse saving')
    chain, gaps = finite_chain(coarse, depth, inputs)
    ordinary = chain[-1]; b = Q(inputs['certificate']['complex_coarse'])
    validate_ordinary_saving(ordinary, coarse)
    q = ordinary*(1-2*eta); minimum = (1-eta)*q/(1+q)
    kappa = strict_grid_below(minimum, headline_grid)
    assembly = engines()['outer'].assembly(ordinary, b, inputs['bridge'], kappa, eta=eta, beta=beta)
    try:
        engines()['outer'].assembly(ordinary, b, inputs['bridge'], kappa+Q(1, headline_grid), eta=eta, beta=beta)
    except AssertionError:
        pass
    else:
        raise ValueError('Adjacent headline point was not excluded')
    require(kappa < ordinary/(1+ordinary) < coarse/(1+coarse), 'Unsupported limiting endpoint')
    return dict(parameters=dict(coarse=coarse, depth=depth, eta=eta, beta=beta, headline_grid=headline_grid),
                envelope=spec, ordinary_bootstrap_chain=chain, finite_gaps=gaps, assembly=assembly,
                kappa=kappa, kappa_decimal=decimal(kappa), gain_over_selected= kappa-BASE_KAPPA,
                adjacent_headline_rejected=True, coarse_parameter_ceiling=coarse/(1+coarse))


def compact(candidate):
    return {key: candidate[key] for key in ('parameters', 'envelope', 'kappa', 'kappa_decimal',
                                           'gain_over_selected', 'adjacent_headline_rejected')}


def analyze(inputs=None):
    inputs = source_inputs() if inputs is None else inputs
    certificate = inputs['certificate']; modules = engines()
    bp = inputs['bit_profile']; cp = inputs['complex_profile']
    baseline = build_candidate(BASE_COARSE, envelope('legacy'), 3, Q(1, 10**12), inputs=inputs)
    require(baseline['kappa'] == BASE_KAPPA and serial(baseline['assembly']) == certificate['assembly'],
            'Selected baseline arithmetic did not reproduce')
    require(serial(baseline['ordinary_bootstrap_chain']) == certificate['ordinary_bootstrap_chain'],
            'Selected ordinary chain did not reproduce')
    original_bit = modules['moment'].moment(validate_profile(bp), bp['m'], bp['W'], BASE_COARSE, True)
    require(serial(original_bit) == certificate['bit_moment_interval'], 'Selected bit moment changed')
    complex_saving = Q(certificate['complex_coarse'])
    cm = modules['moment'].moment(validate_profile(cp), cp['m'], cp['W'], complex_saving, False)
    cm2 = modules['base_two_moment'].moment(cp['m'], cp['W'], list(validate_profile(cp).items()), complex_saving)
    require(serial(cm) == certificate['complex_moment_interval'] and cm[1] < 1 and cm2[1] < 1,
            'Retained complex moment failed')
    cycles = []; incumbent = baseline

    def cycle(number, hypothesis, arguments, predecessor=None):
        nonlocal incumbent
        before = incumbent; admitted = []; attempts = []
        for kwargs in arguments:
            try:
                candidate = build_candidate(inputs=inputs, **kwargs)
            except (ValueError, AssertionError) as error:
                attempts.append(dict(parameters=kwargs, status='REJECTED', reason=str(error)))
            else:
                attempts.append(dict(status='PASS_EXACT_ARITHMETIC', **compact(candidate)))
                admitted.append(candidate)
        best = max([before]+admitted, key=lambda item: item['kappa'])
        incumbent = best
        cycles.append(dict(cycle=number, hypothesis=hypothesis,
            predecessor=predecessor if predecessor is not None else number-1,
            incumbent_before=before['kappa'], incumbent_after=best['kappa'],
            improved=best['kappa'] > before['kappa'], attempts=attempts))

    def args(coarse=BASE_COARSE, kind='legacy', depth=3, eta=Q(1, 10**15),
             beta=DEFAULT_BETA, headline_grid=10**18):
        return dict(coarse=coarse, spec=envelope(kind), depth=depth, eta=eta, beta=beta,
                    headline_grid=headline_grid)

    cycle(1, 'Reduce strictly positive outer backoff at the unchanged three finite levels.', [args()])
    cycle(2, 'Search fixed finite ordinary depths 4,5,6,8; constants may depend on the selected depth.',
          [args(depth=d) for d in (4, 5, 6, 8)])
    chosen_depth = incumbent['parameters']['depth']
    cycle(3, 'Search outer backoff at the admitted finite depth.',
          [args(depth=chosen_depth, eta=Q(1, 10**power)) for power in (12, 18, 24)])
    eta = incumbent['parameters']['eta']
    cycle(4, 'Probe whether the outer complex-leaf allocation beta binds the headline.',
          [args(depth=chosen_depth, eta=eta, beta=beta) for beta in (Q(1,1000), Q(1,100), Q(3,100), Q(1,25), Q(1,2))])
    roots = {}
    for kind in ('legacy', 'exact_fallback', 'prime_threshold', 'combined', 'tight_conditioning', 'disjoint'):
        roots[kind] = refine_coarse(envelope(kind), inputs=inputs)
    cycle(5, 'Refine the strictly certified coarse and headline grids from 10^-18 to 10^-24.',
          [args(coarse=roots['legacy']['coarse'], depth=chosen_depth, eta=eta, headline_grid=10**24)])
    for number, kind, description, predecessor in (
        (6, 'exact_fallback', 'Replace 32m^2 by the proved exact full Gaussian fallback count.', 5),
        (7, 'prime_threshold', 'Use 2m^3/2^80 from the already required prime threshold; keep 32m^2.', 5),
        (8, 'combined', 'Compose the exact full fallback count and retained prime-threshold probability.', [6,7]),
        (9, 'tight_conditioning', 'Use the elementary GL invertibility lower bound in place of the factor two.', 8),
        (10, 'disjoint', 'Use the disjoint good/bad partition while retaining the complete fallback on every bad class.', 9)):
        cycle(number, description,
              [args(coarse=roots[kind]['coarse'], kind=kind, depth=chosen_depth, eta=eta, headline_grid=10**24)],
              predecessor=predecessor)
    cycle(11, 'Joint bounded search of fixed ordinary depth and positive backoff, with strict boundary controls.',
          [args(coarse=roots['disjoint']['coarse'], kind='disjoint', depth=d,
                eta=Q(1, 10**power), headline_grid=10**24)
           for d in (3, 4, 5, 6, 7, 8) for power in (12, 15, 18, 21, 24, 27)])
    selected = incumbent
    selected['bit_moments'] = moment_bounds(selected['parameters']['coarse'], selected['envelope'], inputs)
    require(all(pair[1] < 1 for pair in selected['bit_moments'].values()), 'Selected bit moment failed')
    selected['coarse_grid'] = roots[selected['envelope']['kind']]['grid']
    selected['adjacent_coarse_moments'] = roots[selected['envelope']['kind']]['adjacent_moments']
    selected['complex_moments'] = dict(mercator=cm, base_two=cm2)
    selected['retained_primitive_coefficient'] = inputs['primitive_coefficient']
    selected['retained_extra_bank_selector_calls'] = inputs['finite']['paid_inventory']['extra_bank_selector_calls']
    selected['retained_external_complex_row_coefficient'] = 20161
    good_linear = Q(bp['rank_mass'], bp['m']*bp['W'])
    bad_probability = selected['envelope']['bad_fraction']
    good_factor = 1-bad_probability if selected['envelope']['disjoint_good_bad'] else Q(1)
    linear = good_factor*good_linear + bad_probability*Q(
        selected['envelope']['fallback_count']*bp['calls'], bp['m']*bp['W'])
    delta_linear = 1-linear
    delta_tau = min(1-pair[1] for pair in selected['bit_moments'].values())
    require(delta_linear > 0 and delta_tau > 0, 'Induction lacks a positive moment gap')
    selected['induction'] = dict(
        linear_moment_upper=linear, delta_linear=delta_linear, delta_tau_lower=delta_tau,
        majorant='A*(n+n^(1-c)*w^(1-a_old))',
        A='C*(1+1/delta_linear+1/delta_tau_lower)',
        interpretation='The envelope bounds the two power moments of the actual child operator after substitution of the induction majorant. Its synthetic good/bad coefficients are not an upper recurrence for arbitrary T.')

    rejected = []
    def reject(name, call):
        try:
            call()
        except (ValueError, AssertionError):
            rejected.append(name)
        else:
            raise ValueError('Negative control accepted: '+name)
    p = selected['parameters']; spec = selected['envelope']
    reject('zero outer backoff', lambda: build_candidate(p['coarse'], spec, p['depth'], Q(0), inputs=inputs))
    reject('unbounded ordinary depth', lambda: finite_chain(p['coarse'], float('inf'), inputs))
    reject('zero cutoff gap', lambda: modules['finite_check'].cutoff_log2(Q(0), inputs['primitive_coefficient']))
    bad_spec = dict(spec); bad_spec['fallback_count'] -= 1
    reject('unproved missing fallback child', lambda: validate_envelope(bad_spec))
    bad_spec2 = dict(spec); bad_spec2['bad_fraction'] = Q(0)
    reject('omitted rare class', lambda: validate_envelope(bad_spec2))
    bad_profile = dict(bp); bad_profile['histogram'] = dict(bp['histogram'])
    bad_profile['histogram']['1'] += 1
    reject('altered child profile with unchanged mass', lambda: validate_profile(bad_profile))
    reject('coarse endpoint used as ordinary saving', lambda: validate_ordinary_saving(p['coarse'], p['coarse']))
    reject('detached ordinary saving', lambda: validate_ordinary_step(
        p['coarse'], BASE_LEAF, (1-p['coarse'])*p['coarse']+p['coarse']*BASE_LEAF+Q(1, 10**30)))
    reject('noncontracting adjacent coarse point', lambda: build_candidate(
        p['coarse']+Q(1, selected['coarse_grid']), spec, p['depth'], p['eta'], inputs=inputs))
    require(len(cycles) == 11 and selected['kappa'] > BASE_KAPPA, 'Incomplete investigation')
    return serial(dict(schema='gen4-envelope-refinement/v1', source_sha256=SOURCE_PINS,
        baseline=compact(baseline), cycles=cycles, coarse_search=roots, selected=selected,
        negative_controls=rejected,
        scope='Conditional exact arithmetic and finite-composition refinement of the pinned selected PR279. Physical realization and all-size interfaces are inherited; no global record or practical multiplication claim.'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = analyze()
    payload = json.dumps(report, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_bytes(payload.encode('utf-8'))
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
