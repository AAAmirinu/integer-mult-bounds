#!/usr/bin/env python3
"""Check exact seed identities and finite instances of the modular lifting lemma.

The all-exponent conclusion is a written proof, not a finite enumeration.
Only the standard library and this package's integer verifier are imported.
"""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from math import gcd, isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('integer_bezout', HERE / 'verify.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
require = base.require
SEEDS = (2, 3, 4)
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 43)
LIMIT = 512
MAX_EXPONENT = 5


def is_prime(n):
    return type(n) is int and n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


class Modular:
    """(F_p[u]/Phi_s(u))[z]; no field assumption on the coefficient ring."""
    def __init__(self, order, prime):
        require(is_prime(prime), 'Modulus is not prime')
        require(gcd(order, prime) == 1, 'Prime divides the seed radix')
        self.ring = base.Ring(order)
        self.p = prime
        self.order = order
        self.powers = [self.reduce(c) for c in self.ring.powers]

    def reduce(self, value):
        return base.trim([c % self.p for c in self.ring.reduce(value)])

    def add(self, a, b):
        return self.reduce(base.add(a, b))

    def neg(self, a):
        return self.reduce([-c for c in a])

    def mul(self, a, b):
        return self.reduce(base.multiply(a, b))

    def zadd(self, a, b):
        return base.ztrim([self.add(a[i] if i < len(a) else (0,),
                                   b[i] if i < len(b) else (0,))
                           for i in range(max(len(a), len(b)))])

    def zmul(self, a, b):
        result = [(0,)] * (len(a) + len(b) - 1)
        for i, left in enumerate(a):
            for j, right in enumerate(b):
                result[i + j] = self.add(result[i + j], self.mul(left, right))
        return base.ztrim(result)

    def zdiv(self, a, b):
        # The constant leading coefficient of f_s* is s, invertible mod p.
        b = base.ztrim(b)
        require(len(b[-1]) == 1 and b[-1] != (0,), 'Nonunit scalar leading coefficient')
        leading_inverse = pow(b[-1][0], -1, self.p)
        remainder = list(a)
        quotient = [(0,)] * max(1, len(a) - len(b) + 1)
        while len(remainder) >= len(b) and remainder != [(0,)]:
            offset = len(remainder) - len(b)
            coefficient = self.mul(remainder[-1], (leading_inverse,))
            quotient[offset] = coefficient
            for j, value in enumerate(b):
                remainder[offset + j] = self.add(remainder[offset + j],
                                                  self.neg(self.mul(coefficient, value)))
            remainder = base.ztrim(remainder)
        return base.ztrim(quotient), base.ztrim(remainder)

    def zpowmod(self, value, exponent, modulus):
        require(type(exponent) is int and exponent >= 0, 'Power exponent must be nonnegative')
        result = [(1,)]
        while exponent:
            if exponent & 1:
                result = self.zdiv(self.zmul(result, value), modulus)[1]
            value = self.zdiv(self.zmul(value, value), modulus)[1]
            exponent //= 2
        return result


def exact_seed(case):
    require(set(case) == {'order', 'denominator', 'a', 'b'}, 'Wrong seed fields')
    order = case['order']
    require(type(order) is int and order in SEEDS, 'Unexpected seed radix')
    ring = base.Ring(order)
    f = base.kernel(ring)
    star = [ring.conjugate(c) for c in reversed(f)]
    a, b = base.decode(case['a'], ring), base.decode(case['b'], ring)
    denominator = base.integer(case['denominator'])
    require(denominator > 0, 'Nonpositive seed denominator')
    base.check_identity(ring, f, star, a, b, denominator)
    return ring, f, star, a, b, denominator


def admission(case, prime, exponent):
    require(is_prime(prime), 'Modulus is not prime')
    require(type(exponent) is int and exponent >= 1, 'Exponent must be positive')
    require(gcd(case['order'], prime) == 1, 'Prime divides the seed radix')
    require(int(case['denominator']) % prime != 0, 'Seed denominator vanishes modulo prime')


def literal_reduction(mod, radix, reciprocal=False):
    # Direct tail products for f_r, then invert u and reverse for f_r*.
    coefficients = [(1,)] * radix
    for j in range(radix - 2, -1, -1):
        exponent = -(j + 1) if reciprocal else j + 1
        factor = mod.add((1,), mod.neg(mod.powers[exponent % mod.order]))
        coefficients[j] = mod.mul(coefficients[j + 1], factor)
    return list(reversed(coefficients)) if reciprocal else coefficients


def check_cyclotomic_reduction(order, prime, exponent):
    radix = order * prime ** exponent
    actual = base.trim([c % prime for c in base.cyclotomic(radix)])
    # Deliberately use repeated multiplication, not the integer cyclotomic recursion.
    expected = (1,)
    for _ in range(prime ** (exponent - 1) * (prime - 1)):
        expected = base.trim([c % prime for c in base.multiply(expected, base.cyclotomic(order))])
    require(actual == expected, 'Cyclotomic reduction identity failed')


def check_reductions(f, star, reduced, reduced_star, shift):
    require(reduced == [(0,)] * shift + f, 'Tail-product shift identity failed')
    require(base.ztrim(reduced_star) == star, 'Reciprocal reduction identity failed')


def check_modular_identity(mod, f, star, a, b, denominator):
    require(mod.zadd(mod.zmul(a, f), mod.zmul(b, star)) == [(denominator % mod.p,)],
            'Modular Bezout identity failed')


def finite_instance(case, prime, exponent):
    admission(case, prime, exponent)
    order = case['order']
    radix = order * prime ** exponent
    mod = Modular(order, prime)
    _, f, star, a, b, denominator = exact_seed(case)
    f, star, a, b = ([mod.reduce(c) for c in p] for p in (f, star, a, b))
    reduced = literal_reduction(mod, radix)
    reduced_star = literal_reduction(mod, radix, reciprocal=True)
    check_reductions(f, star, reduced, reduced_star, radix - order)
    check_cyclotomic_reduction(order, prime, exponent)
    check_modular_identity(mod, f, star, a, b, denominator)
    require(star[0] == (1,), 'Reciprocal constant is not one')

    # z*U = 1 - star. Thus U^(r-s) is the inverse of z^(r-s) modulo star.
    u = [mod.neg(c) for c in star[1:]]
    require(mod.zadd([(1,)], [mod.neg(c) for c in star]) == [(0,)] + u,
            'Inverse-of-z identity failed')
    inverse_power = mod.zpowmod(u, radix - order, star)
    lifted_a = mod.zdiv(mod.zmul(a, inverse_power), star)[1]
    difference = mod.zadd([(denominator % prime,)],
                         [mod.neg(c) for c in mod.zmul(lifted_a, reduced)])
    lifted_b, remainder = mod.zdiv(difference, star)
    require(remainder == [(0,)], 'Lifted Bezout quotient is not exact')
    check_modular_identity(mod, reduced, star, lifted_a, lifted_b, denominator)
    # Feed altered obligations through the same validators as the valid case.
    # In particular, unequal arrays alone are not evidence of rejection.
    changed = list(reduced)
    changed[-1] = mod.add(changed[-1], (1,))
    controls = [
        base.reject('missing_shift', lambda: check_reductions(
            f, star, f, reduced_star, radix - order)),
        base.reject('shifted_reciprocal', lambda: check_reductions(
            f, star, reduced, [(0,)] * (radix - order) + star, radix - order)),
        base.reject('changed_leading_term', lambda: check_modular_identity(
            mod, changed, star, lifted_a, lifted_b, denominator)),
    ]
    payload = {'f': reduced, 'star': base.ztrim(reduced_star), 'a': lifted_a, 'b': lifted_b}
    return {'seed': order, 'prime': prime, 'exponent': exponent, 'radix': radix,
            'modular_identity_sha256': hashlib.sha256(json.dumps(payload, separators=(',', ':')).encode()).hexdigest(),
            'mutation_controls': len(controls)}


def scalar_evaluate(polynomial, at, prime):
    value = 0
    for coefficient in reversed(polynomial):
        value = (value * at + coefficient) % prime
    return value


def finite_field_divide(a, b, prime):
    a, b = list(base.trim(a)), base.trim(b)
    require(b != (0,), 'Zero finite-field divisor')
    inverse = pow(b[-1], -1, prime)
    quotient = [0] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and a != [0]:
        offset = len(a) - len(b)
        coefficient = a[-1] * inverse % prime
        quotient[offset] = coefficient
        for j, value in enumerate(b):
            a[offset + j] = (a[offset + j] - coefficient * value) % prime
        a = list(base.trim(a))
    return base.trim(quotient), base.trim(a)


def bad_prime_witness(case, prime):
    # A nonconstant common factor witnesses a root in the algebraic closure;
    # that root need not lie in F_p itself. No characteristic-zero claim.
    order = case['order']
    _, f, star, _, _, denominator = exact_seed(case)
    require(denominator % prime == 0, 'Expected excluded prime')
    for root in range(1, prime):
        if scalar_evaluate(base.cyclotomic(order), root, prime):
            continue
        fp = tuple(scalar_evaluate(c, root, prime) for c in f)
        gp = tuple(scalar_evaluate(c, root, prime) for c in star)
        left, right = fp, gp
        while right != (0,):
            left, right = right, finite_field_divide(left, right, prime)[1]
        inverse = pow(left[-1], -1, prime)
        common = tuple(c * inverse % prime for c in left)
        if len(common) > 1:
            require(finite_field_divide(fp, common, prime)[1] == (0,), 'Invalid common factor of f')
            require(finite_field_divide(gp, common, prime)[1] == (0,), 'Invalid common factor of f*')
            return {'seed': order, 'prime': prime, 'primitive_root': root, 'common_factor': list(common),
                    'scope': 'common factor after reduction only; no complex-unit-circle counterexample'}
    raise ValueError('Expected modular common-factor witness not found')


def verify(document):
    require(document['format'] == 'cyclic-lifting-seeds-v1', 'Wrong seed format')
    require(document['coefficient_order'] == 'ascending z, ascending u', 'Wrong coefficient order')
    require([case['order'] for case in document['cases']] == list(SEEDS), 'Incomplete seed domain')
    require([int(c['denominator']) for c in document['cases']] == [3, 43, 37], 'Changed seed exclusions')
    rows = []
    seeds = []
    bad = []
    controls = []
    for case, excluded in zip(document['cases'], (3, 43, 37)):
        exact_seed(case)
        seeds.append({'seed': case['order'], 'denominator': case['denominator'],
                      'excluded_prime_divisors': sorted(set([excluded] + [p for p in PRIMES if case['order'] % p == 0]))})
        for prime in PRIMES:
            if case['order'] % prime == 0 or int(case['denominator']) % prime == 0:
                continue
            for exponent in range(1, MAX_EXPONENT + 1):
                if case['order'] * prime ** exponent <= LIMIT:
                    rows.append(finite_instance(case, prime, exponent))
        controls.append(base.reject('excluded_prime_s%d' % case['order'],
                                    lambda: admission(case, excluded, 1)))
        dividing_prime = next(p for p in PRIMES if case['order'] % p == 0)
        controls.append(base.reject('noncoprime_seed_s%d' % case['order'],
                                    lambda: admission(case, dividing_prime, 1)))
        bad.append(bad_prime_witness(case, excluded))
        mutant = deepcopy(case)
        mutant['a'][0][0] = str(int(mutant['a'][0][0]) + 1)
        controls.append(base.reject('changed_seed_coefficient_s%d' % case['order'],
                                    lambda: exact_seed(mutant)))
    controls.append(base.reject('composite_modulus', lambda: admission(document['cases'][0], 25, 1)))
    controls.append(base.reject('zero_exponent', lambda: admission(document['cases'][0], 5, 0)))
    return {'status': 'PASS', 'scope': 'exact seed identities and finite checks of a separately proved all-exponent lifting lemma',
            'seeds': seeds, 'domain': {'primes': list(PRIMES), 'max_exponent': MAX_EXPONENT, 'max_radix': LIMIT},
            'finite_instances': rows, 'instances_checked': len(rows),
            'bad_prime_witnesses': bad, 'rejected_admission_and_seed_controls': controls,
            'mutation_controls_checked': sum(row['mutation_controls'] for row in rows) + len(controls)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seeds', type=Path, default=HERE / 'LIFTING-SEEDS.json')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    base.check_sources()
    result = verify(json.loads(args.seeds.read_text()))
    text = json.dumps(result, indent=2) + '\n'
    if args.check:
        require(args.check.read_text() == text, 'Lifting receipt differs')
    if args.output:
        args.output.write_text(text)
    print('PASS: 3 exact seeds, %d modular lifts, 3 excluded-prime witnesses, %d controls' % (
        result['instances_checked'], result['mutation_controls_checked']))


if __name__ == '__main__':
    main()
