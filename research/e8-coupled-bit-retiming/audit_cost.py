"""Exact cost dominance for 0.998 <= p <= 0.9999, including fallback.

The implication uses rational log bounds and Taylor's remainder, not samples. The
source-independent all-column checker separately establishes legality.
"""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def audit(old,new,old_hist,new_hist):
    for key in old:
        if key not in ('frames','D','A','B','C'):assert old[key]==new[key],key
    changed=[]
    for phase in ('D','A','B','C'):
        assert len(old[phase])==len(new[phase])
        for i,(a,b) in enumerate(zip(old[phase],new[phase])):
            assert a[1:]==b[1:],'A scalar gate changed'
            if old['frames'][a[0]]!=new['frames'][b[0]]:
                changed.append(dict(phase=phase,index=i,old=a[0],new=b[0]))
    assert changed
    delta={r:new_hist.get(r,0)-old_hist.get(r,0) for r in set(old_hist)|set(new_hist)}
    delta={r:n for r,n in delta.items() if n}
    assert sum(r*n for r,n in delta.items())==0
    spec=importlib.util.spec_from_file_location('dominance_log',ROOT/'vendor/source375/code/pricing/moment.py')
    moment=importlib.util.module_from_spec(spec);spec.loader.exec_module(moment)
    # r^(1-e)=r*exp(-e*log(r)). The constant term cancels by rank mass.
    # For e>=0, the absolute second derivative is <=r*log(r)^2.
    first=Q(0);second=Q(0)
    for r,n in delta.items():
        lo,hi=moment.logarithm(Q(r));first+=n*r*(lo if n>0 else hi)
        second+=abs(n)*r*hi**2
    lower,upper=Q(1,10000),Q(1,500)
    margin=first-upper*second/2
    fallback=Q(32*56**2*sum(delta.values()),10**16)
    assert margin>0 and lower*margin>max(fallback,Q(0))
    return dict(status='PASS_EXACT_NEAR_ONE_EXPONENT_COST_DOMINANCE',
        local_histogram_delta=delta,exponent_interval=['499/500','9999/10000'],
        first_derivative_lower=str(first),second_derivative_absolute_upper=str(second),
        uniform_cost_decrease_lower=str(lower*margin),fallback_increase_upper=str(max(fallback,Q(0))),
        positive_rank_child_count_change=sum(delta.values()),rank_mass_change=0,
        changed_gates=len(changed),frame_patch=changed,
        fallback_count_change_five_stage=5*sum(delta.values()),fallback_count_change_seven_stage=7*sum(delta.values()),
        proof='For e=1-p, delta cost <= -e*A+e^2*B/2 <= -e_min*(A-e_max*B/2). Rational bounds give a negative gap larger than the positive fallback increase for m<=56. Idle/copy terms cancel. This does not claim dominance for all 0<p<1.')
