#!/usr/bin/env python3
"""Exact integer-Horner replacement for the retained 80-term log_unit.

Apache-2.0. Prepared for Tuomo Kiiskinen with substantial OpenAI ChatGPT
assistance. See NOTICE.md for the original rational-engine attribution.

This module changes polynomial evaluation, NOT series length, remainder,
precision, rounding, or any supplier admission rule. The intended input is
an exact Fraction in [1, 2]; integer endpoints are accepted exactly as well.
No memoized input-dependent state is used.
"""
from fractions import Fraction
from math import lcm

TERMS = 80
_ODDS = tuple(range(1, 2 * TERMS, 2))
_COMMON = lcm(*_ODDS)
_COEFFICIENTS = tuple(_COMMON // odd for odd in _ODDS)


def log_unit(x: Fraction) -> tuple[Fraction, Fraction]:
    """Return exactly the original lower/upper fractions for rational x.

    For z=a/b=(x-1)/(x+1), homogenize the 80-term atanh polynomial
    over common denominator L*b**159. All loop operations are integer
    operations. The original tail is 2*a**161/(161*b**159*(b*b-a*a)).
    """
    if not isinstance(x, (Fraction, int)):
        raise TypeError("an exact Fraction or integer is required")
    if not 1 <= x <= 2:
        raise ValueError("logarithm range")
    x = Fraction(x)
    z = (x - 1) / (x + 1)
    a, b = z.numerator, z.denominator
    a2, b2 = a * a, b * b
    numerator = _COEFFICIENTS[-1]
    b_power = b2
    for coefficient in reversed(_COEFFICIENTS[:-1]):
        numerator = a2 * numerator + coefficient * b_power
        b_power *= b2
    # At loop exit b_power=b**160, including z=0 without a special case.
    denominator_power = b_power // b
    lower = Fraction(2 * a * numerator, _COMMON * denominator_power)
    tail = Fraction(2 * a**161, 161 * denominator_power * (b2 - a2))
    return lower, lower + tail
