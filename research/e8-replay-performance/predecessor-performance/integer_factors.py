"""Exact replay of elementary rational row factors using integer row numerators.

Row i represents nums[i] / den[i], where den[i] is positive. Every update is
the original row operation over Q. Removing common content preserves the row.
No bounded integer, approximate test, or modular identity test is used.
"""
from fractions import Fraction
from math import gcd, lcm


def replay_factors(basis, factors):
    rows = [list(row) for row in basis]
    denominators = [1]*len(rows)
    for row in rows:
        if any(type(x) is not int for x in row):
            raise TypeError('integer input basis required')
    for op,i,j,a,b in factors:
        if b<=0:
            raise ValueError('positive coefficient denominator required')
        if op=='swap':
            rows[i],rows[j]=rows[j],rows[i]
            denominators[i],denominators[j]=denominators[j],denominators[i]
            continue
        if op=='scale':
            row=[a*x for x in rows[i]]
            q=denominators[i]*b
        elif op=='add':
            source_denominator=denominators[j]*b
            q=lcm(denominators[i],source_denominator)
            old_scale=q//denominators[i]
            source_scale=a*(q//source_denominator)
            row=[old_scale*x+source_scale*y for x,y in zip(rows[i],rows[j])]
        else:
            raise ValueError('unknown row factor: '+op)
        common=gcd(q,*row)
        rows[i]=[x//common for x in row]
        denominators[i]=q//common
    return [[Fraction(x,q) for x in row] for row,q in zip(rows,denominators)]
