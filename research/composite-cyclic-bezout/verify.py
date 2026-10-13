#!/usr/bin/env python3
"""Check six exact Bezout certificates without SymPy or producer imports."""
import argparse
from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from math import gcd
from pathlib import Path

ORDERS = (6, 10, 12, 14, 15, 18)
HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(values):
    values = list(values)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values or [0])


def add(a, b):
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def multiply(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, left in enumerate(a):
        for j, right in enumerate(b):
            result[i + j] += left * right
    return trim(result)


def monic_divide(a, b):
    require(b[-1] == 1, 'Nonmonic integer polynomial divisor')
    remainder = list(a)
    quotient = [0] * max(1, len(a) - len(b) + 1)
    while len(remainder) >= len(b) and trim(remainder) != (0,):
        offset = len(remainder) - len(b)
        coefficient = remainder[-1]
        quotient[offset] = coefficient
        for i, value in enumerate(b):
            remainder[offset + i] -= coefficient * value
        remainder = list(trim(remainder))
    return trim(quotient), trim(remainder)


@lru_cache(None)
def cyclotomic(order):
    # x^n - 1 = product_(d|n) Phi_d(x); no producer's field representation.
    polynomial = (-1,) + (0,) * (order - 1) + (1,)
    for divisor in range(1, order):
        if order % divisor == 0:
            polynomial, remainder = monic_divide(polynomial, cyclotomic(divisor))
            require(remainder == (0,), 'Cyclotomic factorization is not exact')
    return polynomial


class Ring:
    """Z[u] represented as integer coefficients modulo Phi_order(u)."""
    def __init__(self, order):
        self.order = order
        self.modulus = cyclotomic(order)
        self.degree = len(self.modulus) - 1
        self.u = self.reduce((0, 1))
        self.powers = [(1,)]
        for _ in range(order):
            self.powers.append(self.mul(self.powers[-1], self.u))
        require(self.powers[order] == (1,), 'u^order != 1')
        require(all(self.powers[j] != (1,) for j in range(1, order)),
                'u is not primitive')
        require(self.degree == sum(gcd(j, order) == 1 for j in range(order)),
                'Wrong cyclotomic degree')

    def reduce(self, value):
        return monic_divide(trim(value), self.modulus)[1]

    def mul(self, a, b):
        return self.reduce(multiply(a, b))

    def conjugate(self, value):
        result = (0,)
        for i, coefficient in enumerate(value):
            result = add(result, tuple(coefficient * x
                                      for x in self.powers[(-i) % self.order]))
        return trim(result)

    def zmul(self, a, b):
        result = [(0,)] * (len(a) + len(b) - 1)
        for i, left in enumerate(a):
            for j, right in enumerate(b):
                result[i + j] = add(result[i + j], self.mul(left, right))
        return ztrim(result)


def ztrim(values):
    values = list(values)
    while len(values) > 1 and values[-1] == (0,):
        values.pop()
    return values or [(0,)]


def zadd(a, b):
    return ztrim([add(a[i] if i < len(a) else (0,),
                      b[i] if i < len(b) else (0,))
                  for i in range(max(len(a), len(b)))])


def kernel(ring):
    # Reconstruct r*P using tail products, without field division or h_j.
    order = ring.order
    f = [(1,)] * order
    for j in range(order - 2, -1, -1):
        factor = add((1,), tuple(-c for c in ring.powers[j + 1]))
        f[j] = ring.mul(f[j + 1], factor)
    require(f[0] == (order,) and f[-1] == (1,), 'Wrong kernel endpoints')
    # Independently bind every tail coefficient to the prefix definition r*h_j.
    prefix = (1,)
    for j in range(order):
        if j:
            factor = add((1,), tuple(-c for c in ring.powers[j]))
            prefix = ring.mul(prefix, factor)
        require(ring.mul(prefix, f[j]) == (order,), 'Prefix/tail identity failed')
    return f


def integer(value):
    require(isinstance(value, str), 'Integer coefficients must be strings')
    result = int(value)
    require(str(result) == value, 'Noncanonical integer encoding')
    return result


def decode(rows, ring):
    require(isinstance(rows, list) and 1 <= len(rows) < ring.order,
            'Wrong z-degree or empty polynomial')
    result = []
    for row in rows:
        require(isinstance(row, list) and 1 <= len(row) <= ring.degree,
                'Wrong u-degree or empty coefficient')
        coefficient = tuple(integer(c) for c in row)
        require(trim(coefficient) == coefficient, 'Unreduced coefficient encoding')
        result.append(coefficient)
    require(ztrim(result) == result, 'Trailing zero z coefficient')
    return result


def check_identity(ring, f, star, a, b, denominator):
    actual = zadd(ring.zmul(a, f), ring.zmul(b, star))
    require(actual == [(denominator,)], 'Bezout identity failed')


def reject(name, action):
    try:
        action()
    except ValueError:
        return name
    raise ValueError('Negative control unexpectedly accepted: ' + name)


def check_case(case):
    require(set(case) == {'order', 'denominator', 'a', 'b'}, 'Wrong case fields')
    order = case['order']
    require(type(order) is int and order in ORDERS, 'Unexpected radix')
    ring = Ring(order)
    f = kernel(ring)
    star = [ring.conjugate(c) for c in reversed(f)]
    a, b = decode(case['a'], ring), decode(case['b'], ring)
    denominator = integer(case['denominator'])
    require(denominator > 0, 'Nonpositive Bezout denominator')
    check_identity(ring, f, star, a, b, denominator)
    coefficient_sum = sum(abs(c) for p in (a, b) for row in p for c in row)
    require(coefficient_sum > 0, 'Empty Bezout bound')
    delta = Fraction(denominator, order * coefficient_sum)
    inverse_bound = 1 / delta + Fraction(2 * (order - 1) * (2 ** order - 1), order) / delta ** 2

    circle_bits = 0
    while delta * (1 << circle_bits) < 1:
        circle_bits += 1
    inverse_bits = 0
    while (1 << inverse_bits) < inverse_bound:
        inverse_bits += 1

    # Mutate mathematical obligations; no hash check can reject these first.
    changed_a = list(a)
    changed_a[0] = add(changed_a[0], (1,))
    changed_f = list(f)
    changed_f[0] = add(changed_f[0], (1,))
    controls = [
        reject('changed_bezout_coefficient', lambda: check_identity(
            ring, f, star, changed_a, b, denominator)),
        reject('changed_denominator', lambda: check_identity(
            ring, f, star, a, b, denominator + 1)),
        reject('missing_conjugation', lambda: check_identity(
            ring, f, list(reversed(f)), a, b, denominator)),
        reject('missing_reversal', lambda: check_identity(
            ring, f, [ring.conjugate(c) for c in f], a, b, denominator)),
        reject('changed_kernel_constant', lambda: check_identity(
            ring, changed_f, star, a, b, denominator)),
        reject('omitted_second_bezout_term', lambda: check_identity(
            ring, f, star, a, [(0,)], denominator)),
    ]
    return {'order': order, 'primitive_embeddings_covered': ring.degree,
            'bezout_denominator': str(denominator),
            'bezout_coefficient_l1': str(coefficient_sum),
            'circle_lower_bound': str(delta),
            'circle_lower_bound_dyadic_exponent': -circle_bits,
            'inverse_infinity_upper_bound': str(inverse_bound),
            'inverse_infinity_upper_bound_dyadic_exponent': inverse_bits,
            'negative_controls_rejected': controls}


def validate_document(document):
    require(set(document) == {'format', 'coefficient_order', 'cases'}, 'Wrong document fields')
    require(document['format'] == 'composite-cyclic-bezout-v1', 'Wrong format')
    require(document['coefficient_order'] == 'ascending z, ascending u', 'Wrong coefficient order')
    require(isinstance(document['cases'], list), 'Cases must be a list')
    require([case['order'] for case in document['cases']] == list(ORDERS),
            'Missing, duplicate, reordered or unexpected radix')


def verify(document):
    validate_document(document)
    cases = [check_case(case) for case in document['cases']]
    missing, duplicate = deepcopy(document), deepcopy(document)
    missing['cases'].pop()
    duplicate['cases'][-1] = duplicate['cases'][0]
    controls = [reject('missing_radix', lambda: validate_document(missing)),
                reject('duplicate_radix', lambda: validate_document(duplicate))]
    # A unit-circle root must never admit a nonzero constant Bezout identity.
    # z-1 and its conjugate reciprocal 1-z vanish at z=1 over every field.
    ring = Ring(6)
    controls.append(reject('false_unit_root_witness', lambda: check_identity(
        ring, [(-1,), (1,)], [(1,), (-1,)], [(1,)], [(1,)], 1)))
    return {'status': 'PASS', 'scope': 'six exact composite-radix Bezout identities; no new kappa',
            'cases': cases, 'additional_negative_controls_rejected': controls,
            'identities': len(cases),
            'primitive_embeddings_covered': sum(c['primitive_embeddings_covered'] for c in cases),
            'negative_controls_rejected': sum(len(c['negative_controls_rejected']) for c in cases) + len(controls)}


def check_sources():
    source = json.loads((HERE / 'SOURCE.json').read_text())
    root = HERE.parent.parent
    for path, expected in source['input_sha256'].items():
        require(hashlib.sha256((root / path).read_bytes()).hexdigest() == expected,
                'Changed pinned source: ' + path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=HERE / 'CERTIFICATE.json')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path, help='Compare the recomputed receipt exactly')
    args = parser.parse_args()
    check_sources()
    result = verify(json.loads(args.certificate.read_text()))
    encoded = json.dumps(result, indent=2) + '\n'
    if args.check:
        require(args.check.read_text() == encoded, 'Receipt differs from expected')
    if args.output:
        args.output.write_text(encoded)
    print('PASS: %d identities, %d primitive embeddings, %d negative controls' % (
        result['identities'], result['primitive_embeddings_covered'], result['negative_controls_rejected']))


if __name__ == '__main__':
    main()
