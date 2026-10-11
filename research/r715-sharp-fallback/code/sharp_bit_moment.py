"""Sharper inherited bit bad-class invoice; OpenAI Codex assistance.

Source: retained notes/three-stage-cover-bit.tex, Gaussian fallback count and
per-edge bad fraction for every q>2^80. Does not change the local word,
physical owner, row reserve, finite prefix or routing bill.
"""
from decimal import Decimal, localcontext, ROUND_FLOOR
from fractions import Fraction as Q

def require(test,message):
    if not test:raise ValueError(message)

def source_charge(m):
    require(type(m) is int and 1<m<=78,'sharp invoice outside verified dimension range')
    n=2*m
    children=6*n*(n-1)+3*n+6*(n-1)
    fraction=Q(2*m**3,1<<80)
    require(children<32*m*m and fraction<Q(1,10**16),'source charge not bounded by inherited charge')
    return children,fraction

def moment(engine,profile,m,W,saving):
    children,fraction=source_charge(m)
    require(0<saving<Q(1,100),'saving outside interval-engine range')
    require(type(W) is int and W>0,'invalid live family count')
    require(all(type(r) is int and type(n) is int and 0<r<m and n>0 for r,n in profile.items()),'invalid exact profile')
    lo=hi=Q(0)
    for rank,count in profile.items():
        a,b=engine.logarithm(Q(m,rank));x,y=engine.exponential(saving*a,saving*b)
        weight=Q(rank*count,m*W);lo+=weight*x;hi+=weight*y
    a,b=engine.logarithm(Q(m));x,y=engine.exponential(saving*a,saving*b)
    weight=Q(children*sum(profile.values()),m*W)*fraction
    return engine.floor(lo+weight*x),engine.ceil(hi+weight*y)

def certify(engine,profile,m,W):
    children,fraction=source_charge(m)
    with localcontext() as ctx:
        ctx.prec=80
        terms=[(Decimal(r*n)/Decimal(m*W),(Decimal(m)/Decimal(r)).ln()) for r,n in profile.items()]
        fb=Decimal(children*sum(profile.values()))*Decimal(fraction.numerator)/Decimal(fraction.denominator)/Decimal(m*W)
        lm=Decimal(m).ln();lo=Decimal(0);hi=Decimal('.003')
        for _ in range(220):
            mid=(lo+hi)/2
            if sum(w*(mid*l).exp() for w,l in terms)+fb*(mid*lm).exp()<1:lo=mid
            else:hi=mid
        tick=int((lo*Decimal(10)**24).to_integral_value(rounding=ROUND_FLOOR))
    lower=Q(tick,10**24);upper=lower+Q(1,10**24)
    lv=moment(engine,profile,m,W,lower);uv=moment(engine,profile,m,W,upper)
    require(lv[1]<1<uv[0],'sharp exact root endpoints not separated')
    return {'lower':str(lower),'upper':str(upper),'strict_rational_signs':True,
            'fallback_children':children,'bad_fraction':str(fraction),
            'lower_endpoint_residual_upper':str(lv[1]-1),'upper_endpoint_residual_lower':str(uv[0]-1)}
