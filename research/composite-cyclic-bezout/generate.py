#!/usr/bin/env python3
"""Nominate exact composite-radix Bezout witnesses using SymPy 1.14.0.

The standard-library verifier does not import this file or SymPy.
"""
import argparse
from functools import reduce
from math import gcd
import json
from pathlib import Path

import sympy
from sympy import Poly, QQ, Symbol, cyclotomic_poly

ORDERS = (6, 10, 12, 14, 15, 18)


def lcm(a, b):
    return a // gcd(a, b) * b


def nominate(order):
    x, z = Symbol('x'), Symbol('z')
    field = QQ.alg_field_from_poly(Poly(cyclotomic_poly(order, x), x), alias='u')
    u = field([1, 0])
    prefix = field.one
    coefficients = []
    for j in range(order):
        if j:
            prefix *= field.one - u ** j
        coefficients.append(field(order) / prefix)

    def conjugate(value):
        result = field.zero
        for coefficient in value.to_list():
            result = result * u ** (order - 1) + field(coefficient)
        return result

    f = Poly.from_list(list(reversed(coefficients)), z, domain=field)
    star = Poly.from_list([conjugate(a) for a in coefficients], z, domain=field)
    a, b, common = f.gcdex(star)
    if common != Poly(1, z, domain=field):
        raise ValueError('Nonconstant gcd at order %d: %s' % (order, common))
    if a * f + b * star != common:
        raise ValueError('SymPy Bezout identity failed')

    # Encode in ascending powers of z and then ascending powers of u.
    rows = [list(reversed(c.to_list())) for p in (a, b)
            for c in reversed(p.rep.to_list())]
    denominator = reduce(lcm, (int(c.denominator) for row in rows for c in row), 1)

    def encode(p):
        return [[str(int(c * denominator)) for c in reversed(value.to_list())] or ['0']
                for value in reversed(p.rep.to_list())]

    result = {'order': order, 'denominator': str(denominator),
              'a': encode(a), 'b': encode(b)}
    integers = [int(c) for key in ('a', 'b') for row in result[key] for c in row]
    divisor = reduce(gcd, integers, denominator)
    result['denominator'] = str(denominator // divisor)
    for key in ('a', 'b'):
        result[key] = [[str(int(c) // divisor) for c in row] for row in result[key]]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--lifting-seeds', action='store_true',
                        help='Generate the three small seeds for the lifting lemma')
    args = parser.parse_args()
    if sympy.__version__ != '1.14.0':
        raise ValueError('Regeneration is pinned to SymPy 1.14.0')
    cases = []
    for order in ((2, 3, 4) if args.lifting_seeds else ORDERS):
        cases.append(nominate(order))
        print('Nominated order %d' % order, flush=True)
    certificate = {'format': ('cyclic-lifting-seeds-v1' if args.lifting_seeds
                              else 'composite-cyclic-bezout-v1'),
                   'coefficient_order': 'ascending z, ascending u', 'cases': cases}
    args.output.write_text(json.dumps(certificate, indent=2) + '\n')


if __name__ == '__main__':
    main()
