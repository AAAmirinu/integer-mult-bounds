"""Check the charged cycle-layout reduction, including non-coprime strides."""
from pathlib import Path
from fractions import Fraction as F
import argparse,importlib.util,json,math
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('mixed',P/'check.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.c
def keys(length,step,wrong_inverse=False):
    step%=length;d=math.gcd(length,step);size=length//d
    inverse=(step//d if wrong_inverse else pow(step//d,-1,size)) if size>1 else 0
    out=[];a=t=0
    for _ in range(length):
        out.append((a,t));a+=1
        if a==d:
            a=0;t+=inverse
            if t>=size:t-=size
    return out
def verify_layout(length,step,ks):
    order=sorted(range(length),key=lambda i:ks[i]);d=math.gcd(length,step);size=length//d
    c.need(len(set(ks))==length,'layout not bijective')
    for a in range(d):
        cycle=order[a*size:(a+1)*size]
        c.need(all((cycle[t]-step)%length==cycle[(t-1)%size] for t in range(size)),'stride adjacency')
    return order
def merge_sort(records):
    width=1;passes=0;comparisons=0;copies=0
    while width<len(records):
        out=[]
        for left in range(0,len(records),2*width):
            mid=min(left+width,len(records));end=min(left+2*width,len(records));i,j=left,mid
            while i<mid or j<end:
                if i<mid and j<end:comparisons+=1
                if j==end or (i<mid and records[i][0]<=records[j][0]):out.append(records[i]);i+=1
                else:out.append(records[j]);j+=1
                copies+=1
        records=out;width*=2;passes+=1
    c.need(copies==len(records)*passes and comparisons<=copies,'merge pass accounting')
    return records,dict(passes=passes,record_copies=copies,key_comparisons=comparisons)
def routed_apply(x,step,tau,state):
    length=len(x);ks=keys(length,step)
    records,forward=merge_sort([(key,(i,value)) for i,(key,value) in enumerate(zip(ks,x))])
    d=math.gcd(length,step);size=length//d;out=[]
    for a in range(d):
        group=records[a*size:(a+1)*size]
        values=[rec[1][1] for rec in group]
        result=m.apply(values,state,1,tau)
        out.extend(((rec[1][0],0),(rec[1][0],value)) for rec,value in zip(group,result))
    restored,backward=merge_sort(out)
    c.need([row[1][0] for row in restored]==list(range(length)),'restore original indices')
    return [row[1][1] for row in restored],dict(cycles=d,cycle_length=size,forward_sort=forward,backward_sort=backward)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);args=ap.parse_args()
    mappings=0
    for length in range(1,65):
        for step in range(-2*length,2*length+1):
            verify_layout(length,step,keys(length,step));mappings+=1
    data=json.loads((P/'FACTORS.json').read_text());state=m.certify(next(x for x in data if x['radix']==9 and x['embedding']==1))
    tau=(F(3,5),F(4,5));cases=[]
    for length in (1,2,3,4,5,8,12,17):
        for step in sorted(set((0,1,-1,2,length//2,2*length+3))):
            x=[(F((5*i)%7-3,8),F((7*i)%11-5,16)) for i in range(length)]
            y,counts=routed_apply(x,step,tau,state);m.residual_check(x,y,state,step,tau)
            if length<=3:
                exact=m.matrix_solve(x,m.phased_polynomial(state['q'],tau),step)
                c.need(all(c.norm2(c.sub(v,w))<=state['budgets'][-1]**2 for v,w in zip(y,exact)),'global dense stride solve')
            cases.append(dict(length=length,step=step,dense=length<=3,**counts))
    controls=[]
    try:verify_layout(7,2,keys(7,2,wrong_inverse=True))
    except ValueError as error:controls.append(dict(name='omitted_modular_inverse',rejected=str(error)))
    else:raise ValueError('wrong modular inverse accepted')
    x=[c.ONE,c.ZERO,c.ZERO];y,_=routed_apply(x,2,tau,state)
    try:m.residual_check(x,y,state,1,tau)
    except ValueError as error:controls.append(dict(name='wrong_stride',rejected=str(error)))
    else:raise ValueError('wrong stride accepted')
    args.out.write_text(json.dumps(dict(status='passed',mapping_cases=mappings,execution_cases=cases,controls=controls,scope='Explicit charged two-sort cycle layout; Python lists verify routing and pass counts, not physical tape execution.'),indent=2)+'\n')
    print(json.dumps(dict(status='passed',mapping_cases=mappings,execution_cases=len(cases),controls=len(controls))))
if __name__=='__main__':main()
