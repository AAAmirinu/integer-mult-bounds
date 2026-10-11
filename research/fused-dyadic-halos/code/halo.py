"""Finite model of a fused clipped-halo stream and sparse request/join repair."""
from fractions import Fraction as Q
from itertools import product
from math import prod


def strides(shape):
    return [prod(shape[i+1:]) for i in range(len(shape))]


def address(coords, shape):
    return sum(x*s for x, s in zip(coords, strides(shape)))


def axis(t, side, halo):
    assert side & (side-1) == 0 and t % side == 0 and side >= 4*halo > 0
    core = side-2*halo
    nominal = t//side
    tiles = (t+core-1)//core
    return dict(t=t, side=side, halo=halo, core=core, nominal=nominal, tiles=tiles)


def axis_stream(a):
    return [x if 0 <= x < a['t'] else None
            for k in range(a['nominal'])
            for x in range(k*a['core']-a['halo'], k*a['core']-a['halo']+a['side'])]


def fused_main(axes, data):
    """One original tape head. Padding emits zero without moving that head."""
    shape = [a['t'] for a in axes]
    assert len(data) == prod(shape)
    step = strides(shape)
    position = [0]*len(axes)
    f = [-a['halo'] for a in axes]
    invalid = len(axes)
    formal = sum(x*s for x, s in zip(f, step))
    initial = formal
    overlap_jump = [(1-2*a['halo'])*s for a, s in zip(axes, step)]
    last = [a['nominal']*a['core']+a['halo']-1 for a in axes]
    wrap_jump = [(-a['halo']-x)*s for a, x, s in zip(axes, last, step)]
    out, head, travel, valid, updates = [], 0, 0, 0, 0
    for _ in range(prod(shape)):
        if invalid:
            out.append(Q(0))
        else:
            assert 0 <= formal < len(data)
            travel += abs(formal-head)
            head = formal
            out.append(data[formal])
            valid += 1
        for i in reversed(range(len(axes))):
            a = axes[i]
            was_invalid = not 0 <= f[i] < a['t']
            position[i] += 1
            carry = position[i] == a['t']
            if carry:
                position[i] = 0
                f[i] = -a['halo']
                formal += wrap_jump[i]
            elif position[i] % a['side'] == 0:
                f[i] += 1-2*a['halo']
                formal += overlap_jump[i]
            else:
                f[i] += 1
                formal += step[i]
            invalid += (not 0 <= f[i] < a['t'])-was_invalid
            updates += 1
            if not carry:
                break
    assert position == [0]*len(axes) and f == [-a['halo'] for a in axes]
    assert formal == initial and invalid == len(axes) and updates < 2*len(out)
    return out, dict(records=len(out), valid_records=valid,
                     adjacent_record_travel=travel, final_rewind=head,
                     total_travel=travel+head, axis_updates=updates,
                     complete_control_period_restored=True)


def variation_formula(axes):
    """Exact closed census of a Cartesian iterator; no tensor enumeration."""
    shape = [a['t'] for a in axes]
    fs = [[x for x in axis_stream(a) if x is not None] for a in axes]
    counts = list(map(len, fs))
    step = strides(shape)
    variation = 0
    for i, f in enumerate(fs):
        suffix_span = sum((g[-1]-g[0])*s for g, s in zip(fs[i+1:], step[i+1:]))
        variation += prod(counts[:i])*sum(abs((y-x)*step[i]-suffix_span)
                                         for x, y in zip(f, f[1:]))
    first = sum(f[0]*s for f, s in zip(fs, step))
    last = sum(f[-1]*s for f, s in zip(fs, step))
    assert first == 0
    return dict(valid_records=prod(counts), adjacent_record_travel=variation,
                final_rewind=last, total_travel=variation+last)


def route_main(axes, stream):
    """Named-slot permutation on a COMPLETE binary main tensor, finite model."""
    dims = [v for a in axes for v in (a['nominal'], a['side'])]
    positions = list(range(0, len(dims), 2))+list(range(1, len(dims), 2))
    out = [None]*len(stream)
    target = [dims[i] for i in positions]
    for coord, value in zip(product(*[range(n) for n in dims]), stream):
        out[address([coord[i] for i in positions], target)] = value
    assert None not in out
    return out


def return_main(axes, stream):
    dims = [v for a in axes for v in (a['nominal'], a['side'])]
    positions = list(range(0, len(dims), 2))+list(range(1, len(dims), 2))
    target = [dims[i] for i in positions]
    return [stream[address([coord[i] for i in positions], target)]
            for coord in product(*[range(n) for n in dims])]


def tile_stream(axes, data, key, periodic=True):
    shape = [a['t'] for a in axes]
    choices = [range(k*a['core']-a['halo'], k*a['core']-a['halo']+a['side'])
               for k, a in zip(key, axes)]
    out = []
    for c in product(*choices):
        if periodic:
            out.append(data[address([x % n for x, n in zip(c, shape)], shape)])
        else:
            out.append(data[address(c, shape)] if all(0 <= x < n for x, n in zip(c, shape)) else Q(0))
    return out


def bad(key, axes):
    return any(k == 0 or k >= a['nominal'] for k, a in zip(key, axes))


def requests(axes):
    """Explicit sparse gathers, sorted by source, joined once, then by target."""
    shape = [a['t'] for a in axes]
    all_keys = product(*[range(a['tiles']) for a in axes])
    wanted = []
    bad_keys = []
    for key in all_keys:
        if not bad(key, axes):
            continue
        bad_keys.append(key)
        for local in product(*[range(a['side']) for a in axes]):
            original = [(k*a['core']-a['halo']+x) % a['t']
                        for k, x, a in zip(key, local, axes)]
            wanted.append((address(original, shape), key, local))
    return sorted(wanted), bad_keys


def repair_tiles(axes, data):
    wanted, keys = requests(axes)
    answers = []
    head = 0
    for source, key, local in wanted:
        assert source >= head
        head = source
        answers.append((key, local, data[source]))
    answers.sort(key=lambda row: (row[0], row[1]))
    size = prod(a['side'] for a in axes)
    tiles = {key: [v for _, _, v in answers[i*size:(i+1)*size]]
             for i, key in enumerate(keys)}
    assert all(tiles[key] == tile_stream(axes, data, key) for key in keys)
    return tiles, dict(requests=len(wanted), tiles=len(keys), join_head_travel=head)


def source_core(a, k, s):
    left = k*a['core']
    right = min((k+1)*a['core'], a['t'])
    return range(left*s//a['t'], right*s//a['t'])


def nearest(j, t, s):
    return (2*t*j+s)//(2*s)


STENCIL = ((-1, Q(1, 8)), (0, Q(1, 2)), (1, Q(1, 16)))


def apply_tile(axes, source_shape, key, values):
    """Local contraction fixture, not the inherited Gaussian inverse."""
    shape = [a['side'] for a in axes]
    out = []
    for js in product(*[source_core(a, k, s) for a, k, s in zip(axes, key, source_shape)]):
        value = Q(0)
        for terms in product(STENCIL, repeat=len(axes)):
            offsets = [nearest(j, a['t'], s)+shift-(k*a['core']-a['halo'])
                       for j, a, s, k, (shift, _) in zip(js, axes, source_shape, key, terms)]
            assert all(0 <= x < n for x, n in zip(offsets, shape))
            value += prod(weight for _, weight in terms)*values[address(offsets, shape)]
        out.append((address(js, source_shape), value))
    return out


def direct(axes, source_shape, data):
    shape = [a['t'] for a in axes]
    result = []
    for js in product(*[range(s) for s in source_shape]):
        value = Q(0)
        for terms in product(STENCIL, repeat=len(axes)):
            coords = [(nearest(j, a['t'], s)+shift) % a['t']
                      for j, a, s, (shift, _) in zip(js, axes, source_shape, terms)]
            value += prod(weight for _, weight in terms)*data[address(coords, shape)]
        result.append(value)
    return result


def pipeline(axes, source_shape, data, mutation=None):
    main, travel = fused_main(axes, data)
    routed = route_main(axes, main)
    tile_size = prod(a['side'] for a in axes)
    assert return_main(axes, routed) == main
    primary_padded = []
    for i, key in enumerate(product(*[range(a['nominal']) for a in axes])):
        values = routed[i*tile_size:(i+1)*tile_size]
        assert values == tile_stream(axes, data, key, periodic=False)
        rows = dict(apply_tile(axes, source_shape, key, values))
        cores = [source_core(a, k, s) for a, k, s in zip(axes, key, source_shape)]
        for local in product(*[range(a['side']) for a in axes]):
            if all(x < len(core) for x, core in zip(local, cores)):
                pos = address([core.start+x for x, core in zip(local, cores)], source_shape)
                primary_padded.append((pos, rows[pos]))
            else:
                primary_padded.append(None)
    # Actual inverse slot permutation then one fused padding-deletion stream.
    primary = [row for row in return_main(axes, primary_padded) if row is not None]
    assert all(a[0] < b[0] for a, b in zip(primary, primary[1:]))
    repaired, sparse = repair_tiles(axes, data)
    exceptions = []
    for key, values in repaired.items():
        if mutation == 'omit-wrap' and all(k < a['nominal'] for k, a in zip(key, axes)):
            continue
        if mutation == 'omit-tail' and any(k >= a['nominal'] for k, a in zip(key, axes)):
            continue
        exceptions.extend(apply_tile(axes, source_shape, key, values))
    exceptions.sort()
    # Ordered two-stream merge; exceptional rows override the main boundary.
    out, i, j = [], 0, 0
    while i < len(primary) or j < len(exceptions):
        if j == len(exceptions) or (i < len(primary) and primary[i][0] < exceptions[j][0]):
            out.append(primary[i]); i += 1
        elif i == len(primary) or exceptions[j][0] < primary[i][0]:
            out.append(exceptions[j]); j += 1
        else:
            out.append(primary[i] if mutation == 'prefer-main-over-repair' else exceptions[j])
            i += 1; j += 1
    return out, dict(travel=travel, sparse=sparse, primary_rows=len(primary),
                     exception_rows=len(exceptions), returned_rows=len(out))
