"""Exact head-travel, sparse-volume and operator controls for dyadic halos."""
from fractions import Fraction as Q
from itertools import product
from math import prod

from halo import axis, axis_stream, bad, direct, fused_main, pipeline, variation_formula


def counts(axes):
    nominal = prod(a['nominal'] for a in axes)
    total = prod(a['tiles'] for a in axes)
    good = prod(max(0, a['nominal']-1) for a in axes)
    tile_volume = prod(a['side'] for a in axes)
    return dict(main_records=nominal*tile_volume, all_records=total*tile_volume,
                bad_records=(total-good)*tile_volume, good_records=good*tile_volume)


def small_travel():
    results = []
    for dimensions in (1, 2, 3, 4):
        for sides in ((4,)*dimensions, (8,)*dimensions):
            if dimensions == 4 and sides[0] == 8:
                continue
            axes = [axis(side*(2 if i % 2 == 0 else 4), side, 1)
                    for i, side in enumerate(sides)]
            size = prod(a['t'] for a in axes)
            emitted, actual = fused_main(axes, list(range(1, size+1)))
            expected = []
            for coord in product(*[axis_stream(a) for a in axes]):
                if None in coord:
                    expected.append(Q(0))
                else:
                    index = 0
                    for x, a in zip(coord, axes):
                        index = index*a['t']+x
                    expected.append(index+1)
            assert emitted == expected
            formula = variation_formula(axes)
            assert all(actual[k] == v for k, v in formula.items())
            results.append(dict(shape=[a['t'] for a in axes], sides=list(sides),
                                actual=actual, formula=formula))
    return results


def large_census():
    results = []
    # Only per-axis lists are visited. Huge tensor volumes are counted exactly,
    # not executed. These cases meet D*A/L<=1/64 and Q_i>=2.
    for dimensions in (2, 4, 8, 16):
        for halo in (1, 3):
            side = 1 << (128*dimensions*halo-1).bit_length()
            axes = [axis(side*(4 if i % 2 else 2), side, halo) for i in range(dimensions)]
            assert Q(dimensions*halo, side) <= Q(1, 64)
            formula, volume = variation_formula(axes), counts(axes)
            assert formula['total_travel'] < 4*volume['main_records']
            # Closed sparse-volume accounting, no assumption of a small fraction
            # at these intentionally small coarse cardinalities.
            u = sum((Q(4*a['halo'], a['side'])+Q(a['side'], a['t']) for a in axes), Q(0))
            if u < Q(1, 2):
                upper = volume['main_records']*(2*u+2*sum(Q(a['side'], a['t']) for a in axes))
                assert volume['bad_records'] <= upper
            results.append(dict(dimensions=dimensions, side=side, halo=halo,
                                tensor_executed=False, per_axis_entries=sum(a['t'] for a in axes),
                                travel_ratio=str(Q(formula['total_travel'], volume['main_records'])),
                                **formula, **volume))
    # Sparse fractions in the actual asymptotic parameter family, all integer.
    for p in (101, 128, 257, 1024):
        d = p
        side = 1 << (p**12-1).bit_length()
        halo = 4096*p**3
        t = 1 << (p**24-1).bit_length()
        nominal, core = t//side, side-2*halo
        tiles = (t+core-1)//core
        # Compute normalized volumes using rational powers, no enormous arrays.
        bad_fraction = Q(tiles, nominal)**d-Q(nominal-1, nominal)**d
        upper = 8*Q(d*halo, side)+4*Q(d*side, t)
        assert d*halo*64 < side and bad_fraction <= upper
        assert upper < Q(1, p**5)
        results.append(dict(p=p, dimensions=d, side=side, halo=halo, t=t,
                            tensor_executed=False, fraction_upper=str(upper),
                            fraction_below='p^-5', exact_power_inequality=True))
    return results


def operator_controls():
    rows = []
    for target, source, side, halo, full_basis in [
        ([16], [15], 8, 2, True),
        ([16, 16], [15, 13], 8, 2, True),
        ([16, 32], [13, 29], 8, 2, False),
        ([16, 16, 16], [15, 13, 11], 8, 2, False),
        ([32, 32], [29, 31], 16, 2, False),
    ]:
        axes = [axis(t, side, halo) for t in target]
        size = prod(target)
        probes = [[Q((i*17)%23-11, 16) for i in range(size)], [Q(1)]*size]
        if full_basis:
            probes += [[Q(i == j) for i in range(size)] for j in range(size)]
        else:
            probes += [[Q(i == j) for i in range(size)] for j in (0, size//2, size-1)]
        for data in probes:
            got, trace = pipeline(axes, source, data)
            assert [i for i, _ in got] == list(range(prod(source)))
            assert [x for _, x in got] == direct(axes, source, data)
        volume = counts(axes)
        assert volume['good_records'] > 0 and trace['sparse']['requests'] == volume['bad_records']
        rows.append(dict(target=target, source=source, side=side, halo=halo,
                         probes=len(probes), all_basis_columns=full_basis,
                         output_entries=prod(source)*len(probes), volume=volume,
                         last_trace=trace))
    return rows


def mutations():
    axes = [axis(16, 8, 2), axis(16, 8, 2)]
    shape = [15, 13]
    data = [Q((i*17)%23-11, 16) for i in range(256)]
    exact = direct(axes, shape, data)
    result = []
    for mutation in ('omit-wrap', 'omit-tail', 'prefer-main-over-repair'):
        got, _ = pipeline(axes, shape, data, mutation)
        ids = [i for i, _ in got]
        wrong = sum(value != exact[i] for i, value in got)
        missing = prod(shape)-len(ids)
        assert wrong or missing, mutation
        result.append(dict(name=mutation, wrong_rows=wrong, missing_rows=missing))
    # A core stride L would discard the overlap underlying the constant-volume
    # halo. The exact main stream changes while the claimed dyadic shape does not.
    original = axis_stream(axes[0])
    altered = dict(axes[0], core=axes[0]['side'])
    assert axis_stream(altered) != original
    result.append(dict(name='use-side-as-core-stride', changed_axis_entries=sum(a != b for a, b in zip(original, axis_stream(altered)))))
    return result


def run():
    travel = small_travel()
    census = large_census()
    operators = operator_controls()
    return dict(explicit_streams=travel, symbolic_census=census, operator_cases=operators,
                mutants=mutations(), kappa_claim=None,
                scope='fused compression-halo layout; local contraction fixture only')


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2, sort_keys=True))
