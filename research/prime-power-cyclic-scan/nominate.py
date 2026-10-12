"""Untrusted complex/Decimal root nominations; certificates are checked separately."""
from pathlib import Path
from decimal import Decimal as D,localcontext
from fractions import Fraction as F
import cmath,importlib.util,json,math,time
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('interval_kernel',P/'interval_kernel.py');ik=importlib.util.module_from_spec(s);s.loader.exec_module(ik)
def add(a,b):return(a[0]+b[0],a[1]+b[1])
def sub(a,b):return(a[0]-b[0],a[1]-b[1])
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b):
    d=b[0]*b[0]+b[1]*b[1];return((a[0]*b[0]+a[1]*b[1])/d,(a[1]*b[0]-a[0]*b[1])/d)
def float_roots(a):
    n=len(a)-1
    roots=[2*cmath.exp(2j*math.pi*(j+.173)/n) for j in range(n)]
    for step in range(4000):
        out=[];change=0
        for j,z in enumerate(roots):
            value=a[-1]
            for c in reversed(a[:-1]):value=value*z+c
            den=a[-1]
            for k,w in enumerate(roots):
                if k!=j:den*=z-w
            delta=value/den;out.append(z-delta);change=max(change,abs(delta))
        roots=out
        if change<1e-13:break
    return roots

out=[]
for r,k in ((3,1),(4,1),(5,1),(7,1),(8,1),(9,1),(9,2),(11,1),(13,1),(16,1)):
    start=time.monotonic();ci=ik.kernel(r,k)
    with localcontext() as ctx:
        ctx.prec=400
        coefficients=[]
        for v in ci:
            row=[]
            for lo,hi in v:
                mid=(lo+hi)/2;row.append(D(mid.numerator)/D(mid.denominator))
            coefficients.append(tuple(row))
        starts=float_roots([complex(float(v[0]),float(v[1])) for v in coefficients])
        roots=[]
        for initial in starts:
            z=(D(str(initial.real)),D(str(initial.imag)))
            for _ in range(24):
                value,derivative=coefficients[-1],(D(0),D(0))
                for c in reversed(coefficients[:-1]):
                    derivative=add(mul(derivative,z),value);value=add(mul(value,z),c)
                z=sub(z,div(value,derivative))
            roots.append([F(int(v*(1<<1024)),1<<1024) for v in z])
        gap=min(1-min(abs(complex(float(x),float(y))),1/abs(complex(float(x),float(y)))) for x,y in roots)
        beta=F(1,1<<math.ceil(math.log2(4/gap)))
        row=dict(radix=r,embedding=k,roots=[[str(v) for v in z] for z in roots],beta=str(beta),factor_bits=1024,working_bits=768,target_bits=128)
        out.append(row)
    print(json.dumps(dict(radix=r,embedding=k,beta=str(beta),seconds=time.monotonic()-start)),flush=True)
    (P/'FACTORS.json').write_text(json.dumps(out,indent=2)+'\n')
