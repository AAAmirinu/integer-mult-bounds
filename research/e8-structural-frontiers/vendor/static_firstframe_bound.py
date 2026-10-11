"""All-bank-count relaxed firstframe moment bound at target b=1/499.

No source mutations. The all-bank-count proof is recorded in the JSON and
uses exact outward intervals for monotonicity of phi(r)-r/73, r=0..9.
"""
import json,importlib.util,hashlib,sys,gzip
from collections import Counter
from fractions import Fraction as Q
from decimal import Decimal,localcontext,ROUND_FLOOR
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
SOURCE=Path('C:/Users/AI/Documents/数学/session-research/extension-repo/research/e8-clean-reuse-extension/data/complex-candidate.json.gz')
PRICER=Path('C:/Users/AI/Documents/数学/integer-mult-bounds/research/e8-coupled-bit-retiming/vendor/source381/code/pricing/moment.py')
spec=importlib.util.spec_from_file_location('tier2_exact_moment',PRICER);M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)

def encode(z):
    if isinstance(z,Q):return str(z)
    if isinstance(z,dict):return {str(k):encode(v) for k,v in z.items()}
    if isinstance(z,(list,tuple)):return [encode(v) for v in z]
    return z

def main():
    blob=SOURCE.read_bytes();c=json.loads(gzip.decompress(blob));sourcehash=hashlib.sha256(blob).hexdigest()
    assert (c['h'],c['v'],c['R'],c['cst'])==(9,120,779,72)
    def gf2rank(xs):
        piv={}
        for value in xs:
            x=value
            while x:
                p=x.bit_length()-1
                if p in piv:x^=piv[p]
                else:piv[p]=x;break
        return len(piv)
    dims=[gf2rank(f) for f in c['frames']]
    assert dims==list(map(len,c['frames'])),'Independent canonical frame bases'
    assert all(dims[c['final'][r]]-dims[c['start'][r]]==8 for r in range(240))
    assert all(dims[c['start'][r]]==0 and dims[c['final'][r]]==9 for r in range(240,1019))
    assert len(c['ret'])==8 and all(dims[f]==9 for k,r,f in c['ret'])
    first_at={}
    for part in ['A','B']:
        if part=='B':
            for k,r,f in c['ret']:
                if r>=240:first_at.setdefault(r,f)
        for gate in c[part]:
            for r in [gate[2]]+[e[0] for e in gate[3]]+(gate[4] if gate[0]=='out' else []):
                if r>=240:first_at.setdefault(r,gate[1])
    for r in range(240,1019):first_at.setdefault(r,c['final'][r])
    assert set(first_at)==set(range(240,1019))
    first=dict(sorted(Counter(dims[f] for f in first_at.values()).items()))
    assert first=={1:257,2:185,3:147,4:35,5:43,6:109,7:3}
    m=73;h=9;replicas=8;stages=9;calls=72;fixedstock=7680;b=Q(1,499)
    helper=Counter({h-d:calls*n for d,n in first.items() if h-d})
    U=sum((h-d)*n for d,n in first.items());assert U==4913
    data=Counter({8:72*240,9:72*8})
    for r in [16,8,32,8,48,8,48,32,16]:data[r]+=1920
    H=data+helper
    effective_stock=Q(fixedstock)+Q(stages*replicas*U,m)
    lv,hv=M.moment(H,m,effective_stock,b,False)
    # Numerator-W has the same sign as this effective-stock moment minus1.
    gaplo=(lv-1)*effective_stock;gaphi=(hv-1)*effective_stock
    phi={0:(Q(0),Q(0))};g={0:(Q(0),Q(0))}
    for r in range(1,10):
        phi[r]=M.moment({r:1},m,1,b,False)
        g[r]=tuple(x-Q(r,m) for x in phi[r])
    monotonic=[dict(previous=r,next=r+1,exact_lower_gap=g[r+1][0]-g[r][1]) for r in range(9)]
    assert all(z['exact_lower_gap']>0 for z in monotonic)
    capacity=(replicas*U+m-1)//m;assert capacity==539
    padding=capacity*m-replicas*U;assert padding==43
    optimistic_integer_H=H+Counter({padding:stages})
    integerstock=fixedstock+stages*capacity
    il,iu=M.moment(optimistic_integer_H,m,integerstock,b,False)
    assert gaplo>0 and lv>1 and il>1
    with localcontext() as ctx:
        ctx.prec=70
        dw=Decimal(effective_stock.numerator)/Decimal(effective_stock.denominator)
        terms=[(Decimal(r*n)/(Decimal(m)*dw),(Decimal(m)/Decimal(r)).ln()) for r,n in H.items()]
        lo=Decimal(0);hi=Decimal('.003')
        for _ in range(210):
            mid=(lo+hi)/2
            if sum(p*(mid*x).exp() for p,x in terms)<1:lo=mid
            else:hi=mid
        ticks=int(((lo+hi)/2*10**24).to_integral_value(rounding=ROUND_FLOOR))
    rootlo=Q(ticks,10**24);roothi=rootlo+Q(1,10**24)
    assert M.moment(H,m,effective_stock,rootlo,False)[1]<1<M.moment(H,m,effective_stock,roothi,False)[0]
    root=dict(lower=M.decimal(rootlo),upper=M.decimal(roothi),nominal_k_ceiling_interval=[M.decimal(rootlo/(1+rootlo)),M.decimal(roothi/(1+roothi))])
    rootg={0:(Q(0),Q(0))}
    for r in range(1,10):rootg[r]=tuple(x-Q(r,m) for x in M.moment({r:1},m,1,roothi,False))
    rootmonotonic=[dict(previous=r,next=r+1,exact_lower_gap=rootg[r+1][0]-rootg[r][1]) for r in range(9)]
    assert all(z['exact_lower_gap']>0 for z in rootmonotonic)
    result=dict(status='PASS_EXACT_FIXED_FIRSTFRAME_ALL_BANK_COUNTS_TARGET_REJECTION',
        target_kappa=Q(1,500),necessary_coarse=b,source=str(SOURCE),source_sha256=sourcehash,pricer=str(PRICER),pricer_sha256=hashlib.sha256(PRICER.read_bytes()).hexdigest(),
        firstframe_histogram=first,static_entrance_mass_upper=2098,minimum_residual_dimensions_per_invocation=U,
        capacity_only_minimum_banks=capacity,minimum_bank_padding_dimensions=padding,
        relaxed_histogram=dict(sorted(H.items())),relaxed_fractional_effective_stock=effective_stock,
        relaxed_target_moment_interval=[lv,hv],unnormalized_target_gap_interval=[gaplo,gaphi],
        relaxed_coarse_root_interval=[root['lower'],root['upper']],
        relaxed_nominal_kappa_ceiling_interval=root['nominal_k_ceiling_interval'],
        minimum_integer_bank_model_histogram=dict(sorted(optimistic_integer_H.items())),minimum_integer_stock=integerstock,
        minimum_integer_target_moment_interval=[il,iu],
        helper_excess_monotonicity=monotonic,
        helper_excess_monotonicity_at_relaxed_root_upper=rootmonotonic,
        proof=[
            'Let d_r<=f_r=dim(original firstframe_r), s_r=9-d_r. Every helper remaining nested walk costs at least phi(s_r), because splitting total rank raises sum phi(rank), phi(x)=(x/73)^(1-b), 0<b<1.',
            'The family retains original data endpoints, center-copy children and nine-stage geometric blocks. Their most optimistic endpoint histogram is the recorded fixed data histogram. All response, cleanup, additional gate and phase costs are omitted.',
            'For B full width73 banks per stage, capacity requires 73B>=8 sum_r s_r. Padding rank P=73B-8 sum_r s_r has total moment cost at least P/73, even if arbitrary rank73 or fractional padding is granted.',
            'Therefore total moment numerator minus stock W=7680+9B is at least data_numerator-7680 +72 sum_r [phi(s_r)-s_r/73]. This expression is independent of B.',
            'Exact rational outward intervals certify g(r)=phi(r)-r/73 strictly increasing for r=0,...,9 at b=1/499. Thus d_r<=f_r implies g(s_r)>=g(9-f_r).',
            'Using all f_r simultaneously for free, relaxing stock to 7680+72*4913/73 and omitting all padding entropy gives the recorded lower bound. Its moment lower endpoint exceeds1, so every member of this precisely fixed-firstframe family fails the target coarse saving for every integer B.',
            'The integer539-bank histogram with a single rank43 padding child per stage is an additional stronger optimistic check, not needed for the all-B proof.'
            ,'The same exact g(r) monotonicity is checked at the relaxed root upper grid point, whose relaxed moment lower endpoint exceeds1; hence the coarse saving of any member of this family is strictly below that grid point. The listed fractional-root interval is an upper-bound benchmark, never an achieved supplier.'
        ],
        scope='Necessary bound for unchanged R779 first required frames, nine-axis final helpers, residual rank9-d per helper, 72 copies, same original data endpoints/center copies/geometry and complete width73 banks. Entrance gauges of any rational donor topology are granted maximal frame dimensions for free. This is not a global impossibility result and does not apply after changing firstframes, endpoints, copied centers, geometry, residual rank relation or bank semantics. No achieved supplier is asserted.',
        positive_fallback_omitted=True)
    (HERE/'STATIC-FIRSTFRAME-BOUND.json').write_text(json.dumps(encode(result),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(encode({k:result[k] for k in ['status','relaxed_fractional_effective_stock','relaxed_target_moment_interval','unnormalized_target_gap_interval','relaxed_coarse_root_interval','relaxed_nominal_kappa_ceiling_interval','minimum_integer_target_moment_interval']}),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
