"""Exact polynomial FFT controls for two complementary physical passes.

The pinned reviewer supplies only arithmetic primitives. The schedule and
physical permutations here are new; the comparator is the closed Fourier sum.
Tiny operator layouts do not simulate the asymptotically large compact core.
"""
from fractions import Fraction as Q
from itertools import product
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'references/semantic-bulk/rad20/code/review_balanced_transform.py'
spec = importlib.util.spec_from_file_location('pinned_polynomial_arithmetic', SOURCE)
poly = importlib.util.module_from_spec(spec)
spec.loader.exec_module(poly)


def masks(slots):
    assert len(slots) == len(set(slots))
    return {slot: 1 << (len(slots)-1-j) for j, slot in enumerate(slots)}


def layout(ell, K, lengths, active):
    widths, _, _ = poly.shape(ell, K, lengths)
    other = [i for i in range(len(lengths)) if i not in active]
    # Small Fourier controls need an actual permutation, not large reservoirs.
    # Literal complete-field capacity is checked independently in capacity.py.
    cut = (len(other)+1)//2
    order = other[:cut] + list(active) + other[cut:]
    slots = [(i, ell-1) for i, a in enumerate(lengths) if a == ell]
    low = ell-1
    for width in widths:
        slots += [(i, h) for i in order for h in range(low-1, low-width-1, -1)]
        low -= width
    assert low == 0 and len(slots) == sum(lengths)
    return masks(slots)


def route(values, old, new):
    assert old.keys() == new.keys()
    output = [None] * len(values)
    for index, value in enumerate(values):
        target = sum(new[slot] for slot, bit in old.items() if index & bit)
        assert output[target] is None
        output[target] = value
    assert all(x is not None for x in output)
    return output


def top_layout(ell, K, lengths, axes):
    selected = [(i, ell-1) for i in axes if lengths[i] == ell]
    unused = [(i, h) for i, a in enumerate(lengths) for h in range(a-1, -1, -1)
              if (i, h) not in selected]
    needed = len(selected)*(K-1)
    assert len(unused) >= needed
    active = []
    for j, slot in enumerate(selected):
        active += unused[j*(K-1):(j+1)*(K-1)] + [slot]
    rest = unused[needed:]
    cut = len(rest)//2
    slots = rest[:cut] + active + rest[cut:]
    assert len(slots) == sum(lengths)
    assert all(slots[cut+j*K+K-1] == slot for j, slot in enumerate(selected))
    return masks(slots)


def schedule(ell, K, lengths, mutation=None):
    original = masks([(i, h) for i, a in enumerate(lengths) for h in range(a-1, -1, -1)])
    D = len(lengths)
    groups = [list(range(D//2)), list(range(D//2, D))]
    current = original
    steps = []
    for number, axes in enumerate(groups):
        if mutation == 'omitted complementary pass' and number == 1:
            continue
        top_axes = [i for i in axes if lengths[i] == ell]
        if top_axes:
            target = top_layout(ell, K, lengths, axes)
            if not (mutation == 'unpaid between-pass relabel' and number == 1):
                steps.append(('route', current, target))
            current = target
            steps.append(('layer', ell-1, top_axes, current))
            steps.append(('twiddle', ell-1, top_axes, current,
                          mutation == 'wrong twiddle sign' and number == 1))
        target = layout(ell, K, lengths, axes)
        if not (mutation == 'unpaid between-pass relabel' and number == 1 and not top_axes):
            steps.append(('route', current, target))
        current = target
        rounds = [(h, axes) for h in range(ell-2, -1, -1)]
        for h, selected in rounds:
            if selected:
                steps.append(('layer', h, selected, current))
                steps.append(('twiddle', h, selected, current,
                              mutation == 'wrong twiddle sign' and number == 1))
        if mutation == 'unrestored dirty reservoir' and number == 0:
            steps.append(('xor', current[groups[1][0], 0]))
    steps.append(('route', current, original))
    return original, steps


def apply(values, steps, r, opposite=False):
    for op in reversed(steps) if opposite else steps:
        if op[0] == 'route':
            _, old, new = op
            values = route(values, new, old) if opposite else route(values, old, new)
        elif op[0] == 'layer':
            poly.layer(values, *op[1:])
        elif op[0] == 'twiddle':
            _, h, axes, current, wrong_sign = op
            poly.twiddle(values, h, axes, current, r, opposite != wrong_sign)
        elif op[0] == 'xor':
            values = [values[j ^ op[1]] for j in range(len(values))]
        else:
            raise AssertionError(op)
    return values


def control(ell, K, lengths, exhaustive):
    original, steps = schedule(ell, K, lengths)
    M = 1 << sum(lengths)
    r = 1 << ell
    bases = range(M) if exhaustive else sorted({0, 1, M//3, M//2, M-1})
    entries = 0
    for basis in bases:
        coordinates = poly.coordinates(basis, lengths)
        target = poly.encoded(coordinates, lengths, original)
        values = [{} for _ in range(M)]
        values[target] = {0: Q(1)}
        values = apply(values, steps, r)
        for frequency in range(M):
            js = poly.coordinates(frequency, lengths)
            exponent = -sum((2*r//(1 << a))*j*k
                            for a, j, k in zip(lengths, js, coordinates)) % (2*r)
            expected = {exponent % r: Q(-1 if exponent >= r else 1, M)}
            assert values[poly.encoded(js, lengths, original, True)] == expected
            entries += 1
        values = apply(values, steps, r, opposite=True)
        assert values[target] == {0: Q(1, M)}
        assert all(not value for j, value in enumerate(values) if j != target)
    return dict(ell=ell, K=K, lengths=lengths, full_basis=exhaustive,
                basis_columns=len(bases), polynomial_entries=entries,
                global_routes=sum(op[0] == 'route' for op in steps),
                layers=sum(op[0] == 'layer' for op in steps),
                opposite_exact=True)


def run():
    rows = []
    for ell in (2, 3):
        for K in range(1, ell):
            for flags in product((0, 1), repeat=2):
                rows.append(control(ell, K, [ell-1+x for x in flags], True))
    for ell, K, D in [(2, 1, 4), (3, 1, 3), (3, 2, 3), (4, 2, 2),
                      (4, 3, 2), (6, 2, 2), (6, 3, 2)]:
        for flags in [(0,)*D, (1,)*D, tuple(i % 2 for i in range(D))]:
            rows.append(control(ell, K, [ell-1+x for x in flags], False))
    assert all(3 <= row['global_routes'] <= 5 and row['layers'] <= 2*row['ell'] for row in rows)
    rejected = []
    ell, K, lengths = 3, 1, [3, 2, 3]
    _, good = schedule(ell, K, lengths)
    M = 1 << sum(lengths)
    values = [{j % 8: Q((j % 7)-3, 8)} for j in range(M)]
    expected = apply(values, good, 8)
    for name in ['omitted complementary pass', 'unpaid between-pass relabel',
                 'wrong twiddle sign', 'unrestored dirty reservoir']:
        _, bad = schedule(ell, K, lengths, name)
        actual = apply([{j % 8: Q((j % 7)-3, 8)} for j in range(M)], bad, 8)
        assert actual != expected, name
        rejected.append(name)
    return dict(status='PASS', shapes=rows, shape_count=len(rows),
                basis_columns=sum(x['basis_columns'] for x in rows),
                polynomial_entries=sum(x['polynomial_entries'] for x in rows),
                mutations_rejected=rejected,
                scope='Actual two-pass polynomial Fourier operators and physical routes; compact-core all-size cost remains a conditional written proof.')
