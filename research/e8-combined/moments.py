"""Enclose the supplier moment with rational series and outward rounding."""
from fractions import Fraction as Q
from functools import cache
GRID=1<<192

def down(x):return Q(x.numerator*GRID//x.denominator,GRID)
def up(x):return -down(-x)

@cache
def log_bounds(x):
    x=Q(x);power=0
    while x>=2:x/=2;power+=1
    assert 1<=x<2
    def unit(y):
        z=(y-1)/(y+1);term=z;lower=Q(0)
        for j in range(64):
            lower+=2*term/(2*j+1);term*=z*z
        return lower,lower+2*term/(129*(1-z*z))
    lo,hi=unit(x);two_lo,two_hi=unit(Q(2))
    return down(lo+power*two_lo),up(hi+power*two_hi)

def exp_bounds(lo,hi):
    assert 0<=lo<=hi<Q(1,10)
    def polynomial(x):
        term=total=Q(1)
        for k in range(1,19):term*=x/k;total+=term
        return total,term*x/19/(1-x/20)
    lower,_=polynomial(lo);upper,tail=polynomial(hi)
    return down(lower),up(upper+tail)

def moment(histogram,dimension,live,saving):
    lower=upper=Q(0)
    terms=[(Q(rank*count,dimension*live),Q(dimension,rank)) for rank,count in histogram.items()]
    terms.append((Q(32*dimension*sum(histogram.values()),10**16*live),Q(dimension)))
    for weight,base in terms:
        lo,hi=log_bounds(base);lo,hi=exp_bounds(saving*lo,saving*hi)
        lower+=weight*lo;upper+=weight*hi
    return down(lower),up(upper)

def certify(histogram,dimension,live,lower):
    lower=Q(lower);upper=lower+Q(1,10**24)
    lower_interval=moment(histogram,dimension,live,lower)
    upper_interval=moment(histogram,dimension,live,upper)
    assert lower_interval[1]<1<upper_interval[0]
    return dict(lower=str(lower),upper=str(upper),
        lower_residual_upper=str(lower_interval[1]-1),
        upper_residual_lower=str(upper_interval[0]-1),
        method='64-term atanh log series after binary reduction;18-degree exponential;192-bit outward dyadic rounding')
