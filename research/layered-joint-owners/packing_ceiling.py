"""Exact relaxed ceiling for owner changes with fixed local profile/capacities.

For 0<p<1 and 0<=x<=C, x**p >= x*C**(p-1). Thus concentrating the
fixed idle rank in C-dimensional remainders minimizes its homogeneous moment.
This relaxation need not have a feasible assignment. It bounds only this fixed
local provider and controller, not other circuits or multiplication algorithms.
"""
import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys


def main():
    if not __debug__:
        raise RuntimeError('Assertions required')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--parent', type=Path, required=True)
    ap.add_argument('--main', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args(); a.out.mkdir(exist_ok=False)
    plan = json.loads((a.parent / 'data/PLAN.json').read_text())
    assert (plan['M'], plan['live'], plan['deficit']) == (73, 7168, 2560)
    local = {int(r): n for r, n in plan['provider_registry']['gauge44']['actual_paid_profile'].items()}
    profile = Counter({r: 72*n for r, n in local.items()})
    maximum = max(cap for cap, _ in plan['windows'].values())
    assert maximum == 48 and len(plan['order']) == 72
    idle = 73*7168-2560-sum(r*n for r, n in profile.items())
    assert idle == 115200 and idle % maximum == 0
    profile[maximum] += idle // maximum
    (a.out / 'RELAXED-PROFILE.json').write_text(json.dumps(dict(sorted(profile.items())), indent=2)+'\n')
    subprocess.run([sys.executable, '-B', str(a.parent / 'independent/price_profile.py'),
                    '--main', str(a.main), '--profile', str(a.out / 'RELAXED-PROFILE.json'),
                    '--output', str(a.out / 'PRICE.json')], check=True)
    price = json.loads((a.out / 'PRICE.json').read_text())
    upper = Fraction(price['prices']['native']['root']['upper'])
    assert 0 < upper < 1
    ceiling = upper/(1+upper)
    with localcontext() as ctx:
        ctx.prec = 70
        decimal = str(Decimal(ceiling.numerator)/Decimal(ceiling.denominator))
    result = dict(status='PASS_EXACT_FIXED_PROVIDER_RELAXED_PACKING_CEILING',
                  max_idle_dimension=maximum, fixed_idle_rank=idle, relaxed_idle={str(maximum): idle//maximum},
                  native_root_upper=str(upper), kappa_upper_rational=str(ceiling),
                  kappa_upper_decimal=decimal, feasible_assignment_claimed=False,
                  scope='Upper bound for fixed local profile and controller capacities with retained outer transfer; '
                        'not a universal multiplication bound. Exact root upper endpoint is independently signed. '
                        'The retained outer transfer has kappa < b/(1+b).')
    (a.out / 'CEILING.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'], decimal)


if __name__ == '__main__':
    main()
