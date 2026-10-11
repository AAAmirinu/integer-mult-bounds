"""Independent exact formulas, full small streams and wide carry probes."""
from fractions import Fraction as Q
import hashlib
import importlib.util
from itertools import islice, product
import json
from math import prod
from pathlib import Path
import random

from stream import ChirpStream, direct_phase

ROOT = Path(__file__).resolve().parents[3]


def unrank(index, radices):
    coordinates = []
    for t in reversed(radices):
        index, digit = divmod(index, t)
        coordinates.append(digit)
    assert index == 0
    return tuple(reversed(coordinates))


def full_case(r, radices, sources):
    stream = ChirpStream(r, radices, sources)
    T = prod(radices)
    digest = hashlib.sha256()
    phases = [] if T <= 64 else None
    count = 0
    for coordinates, actual in zip(product(*(range(t) for t in radices)), stream.phases(), strict=True):
        expected = -sum(s*j*j*(r//t) for s, j, t in zip(sources, coordinates, radices)) % (2*r)
        assert actual == expected
        digest.update(actual.to_bytes((2*r).bit_length()//8+1, 'big'))
        if phases is not None:
            phases.append(actual)
        count += 1
    assert count == T and stream.phase == 0
    assert all(x.index == x.value == 0 and x.difference == x.coefficient for x in stream.axes)
    visits = sum(T//prod(radices[i+1:]) for i in range(len(radices)))
    assert stream.visits == visits < 2*T
    assert stream.rewinds == max(0, visits-T)
    assert stream.max_residue_bits <= r.bit_length()
    operator_entries = 0
    if phases is not None:
        for jrank, j in enumerate(product(*(range(t) for t in radices))):
            for krank, k in enumerate(product(*(range(t) for t in radices))):
                diff = tuple((x-y) % t for x, y, t in zip(j, k, radices))
                rank = 0
                for digit, t in zip(diff, radices):
                    rank = rank*t+digit
                actual = (phases[rank]-phases[jrank]-phases[krank]) % (2*r)
                expected = 2*sum(s*x*y*(r//t) for s, x, y, t in zip(sources, j, k, radices)) % (2*r)
                assert actual == expected
                operator_entries += 1
    # Independent bounded-width recomputation at both ends of the rectangle.
    max_raw = 0
    for coordinates in [tuple(0 for t in radices), tuple(t-1 for t in radices)]:
        value = 0
        for s, j, t in zip(sources, coordinates, radices):
            square = j*j
            raw = s*square*(r//t)
            max_raw = max(max_raw, raw.bit_length())
            assert square.bit_length() <= 2*(r.bit_length()-1)
            assert raw.bit_length() <= 3*(r.bit_length()-1)+1
            value = (value-raw % (2*r)) % (2*r)
        assert value == direct_phase(r, radices, sources, coordinates)
    return dict(r=r, radices=radices, sources=sources, entries=T, visits=visits,
                return_traversals=stream.rewinds, residue_bits=stream.max_residue_bits,
                direct_max_raw_bits=max_raw, operator_entries=operator_entries,
                phase_sha256=digest.hexdigest(), full_period_restored=True)


def wide_cases(rng):
    rows = []
    for ell in (31, 63, 127, 257, 521):
        r = 1 << ell
        for d in (1, 2, 5, 9):
            radices = tuple(r if i % 2 else r//2 for i in range(d))
            sources = tuple(rng.randrange(1, t, 2) for t in radices)
            T = prod(radices)
            for tag, initial in [('zero', 0), ('final', T-1), ('mixed', rng.randrange(T))]:
                stream = ChirpStream(r, radices, sources)
                coords = unrank(initial, radices)
                # Direct invariant initialization is only a bounded probe of a
                # distant state, not a claim to have executed its huge prefix.
                for x, j in zip(stream.axes, coords):
                    x.index = j
                    x.value = x.coefficient*j*j % (2*r)
                    x.difference = x.coefficient*(2*j+1) % (2*r)
                stream.phase = direct_phase(r, radices, sources, coords)
                digest = hashlib.sha256()
                checked = 0
                for offset in range(64):
                    rank = (initial+offset) % T
                    coordinates = unrank(rank, radices)
                    expected = -sum(s*j*j*(r//t) for s, j, t in zip(sources, coordinates, radices)) % (2*r)
                    assert stream.phase == expected
                    assert tuple(x.index for x in stream.axes) == coordinates
                    digest.update(stream.phase.to_bytes((ell+8)//8, 'big'))
                    checked += 1
                    more = stream.advance()
                    if not more:
                        assert rank == T-1 and stream.phase == 0
                        break
                rows.append(dict(ell=ell, axes=d, initial=tag, states_checked=checked,
                                 phase_sha256=digest.hexdigest(), complete_large_prefix_executed=False))
    return rows


def arithmetic_control():
    path = ROOT/'research/e8-r740-replica32/code/engines/outer.py'
    spec = importlib.util.spec_from_file_location('retained_outer_for_chirp', path)
    outer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(outer)
    prior = json.loads((ROOT/'research/e8-r715-whole-hosted/EXPECTED.json').read_text())
    a, b = Q(prior['strict_outer_constraints']['bit_positive']), Q(prior['complex_lower'])
    k, eta = Q(prior['kappa']), Q(1, 10**18)
    bridge = {'semantic': {'C0': {'base': 2, 'exponent': 210000}, 'strict_literal_gap': 1},
              'rows': {'degree_gap': Q(10**6)-Q(51*20161, 25)}}
    old = outer.assembly(a, b, bridge, k, eta, eta)
    assert {n: str(v) for n, v in old['strict_constraints'].items()} == prior['strict_outer_constraints']
    eps, delta = old['parameters']['epsilon'], old['parameters']['delta']
    changed = dict(old['margins'], scalar_work=1-delta)
    assert changed['scalar_work']-old['margins']['scalar_work'] == eps
    assert old['margins']['Gaussian_arithmetic'] <= old['margins']['scalar_work']
    assert min(changed.values()) == min(old['margins'].values())
    return dict(reference_kappa=str(k), old_scalar_margin=str(old['margins']['scalar_work']),
                new_scalar_margin=str(changed['scalar_work']), improvement=str(eps),
                Gaussian_margin_unchanged=str(changed['Gaussian_arithmetic']),
                minimum_unchanged=str(min(changed.values())), new_kappa_claim=False)


def run():
    rng = random.Random(20261011)
    cases = set()
    for r, maximum_d in [(2, 8), (4, 5), (8, 4), (16, 3), (32, 2), (256, 2)]:
        for d in range(1, maximum_d+1):
            for radices in product(sorted({t for t in (r//2, r) if t >= 2}), repeat=d):
                for sources in [tuple(1 for t in radices), tuple(t-1 for t in radices),
                                tuple(rng.randrange(1, t, 2) for t in radices)]:
                    cases.add((r, radices, sources))
    rows = [full_case(r, t, s) for r, t, s in sorted(cases)]
    wide = wide_cases(rng)
    r, radices, sources = 8, (4, 8, 4), (3, 5, 1)
    T = prod(radices)
    expected = [direct_phase(r, radices, sources, j) for j in product(*(range(t) for t in radices))]
    rejected = []
    for name in ['wrong second difference', 'omitted carry subtraction', 'zero wrap difference', 'stopped carry']:
        actual = list(islice(ChirpStream(r, radices, sources).phases(name), T+1))
        assert actual != expected, name
        rejected.append(name)
    bad = ChirpStream(r, radices, sources)
    bad.modulus = r
    assert list(islice(bad.phases(), T+1)) != expected
    rejected.append('wrong phase modulus')
    assert [(-e) % (2*r) for e in expected] != expected
    rejected.append('conjugated phase convention')
    return dict(status='PASS', full_stream_cases=rows, wide_probes=wide,
                full_stream_count=len(rows), full_phase_entries=sum(x['entries'] for x in rows),
                operator_entries=sum(x['operator_entries'] for x in rows),
                wide_probe_count=len(wide), wide_states=sum(x['states_checked'] for x in wide),
                mutations_rejected=rejected, arithmetic=arithmetic_control(),
                scope='Exact chirp residues, full small periods and bounded distant-state probes; unchanged numerical exponential and all-size tape cost transferred by written argument.')
