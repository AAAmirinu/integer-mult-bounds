"""Exercise actual certified prime-power factors using dirty inverse shears."""
from pathlib import Path
import importlib.util,json,argparse
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('dirty',P/'dirty.py');d=importlib.util.module_from_spec(s);s.loader.exec_module(d);c=d.c;F=d.F
rows=json.loads((P/'FACTORS.json').read_text());cases=[];certs=[]
for row in rows:
    if row['radix']not in(4,9):continue
    st=d.w.k.certify(row);certs.append(st['certificate']);nf=len(st['factors'])
    fs=[(inside,b,F(st['radix'])if i==0 else F(1))for i,(inside,b)in enumerate(st['factors'])]
    beta=st['beta'];G=2+F(st['radix'])/beta;N=4*nf*nf
    logG=max(0,G.numerator.bit_length()-G.denominator.bit_length()+1)
    bits=256+N*logG+100
    for n in(1,3):
        for direction in(-1,1):
            for dirt in(-7,11):
                x=[(F(i%5-2,4),F(i%3-1,8))for i in range(n)];x0=x[:];y=[(F(dirt+i),F(dirt-i))for i in range(n)];y0=y[:]
                scratch=[[(F(dirt+i+j),F(dirt+2*i-j))for i in range(n)]for j in range((nf-1).bit_length())];s0=[z[:]for z in scratch]
                units=[c.ONE,(F(0),F(1)),(F(3,5),F(4,5))];phases=[units[(i+1)%3]for i in range(n)]
                D=max(abs(a)+abs(b)for v in[x,y]+scratch for a,b in v);bound=d.certificate(nf,beta,st['radix'],D,bits)
                c.need(bound<=F(1,1<<128),'kernel target budget')
                stats=dict(leaves=0,scalar_steps=0);d.compose(x,y,fs,scratch,phases,beta,bits,direction,stats=stats)
                c.need(x==x0 and scratch==s0,'kernel dirty restoration')
                net=[c.sub(a,b)for a,b in zip(y,y0)];exact=d.w.solve(d.w.matrix(st['q'],phases,direction),x0)
                c.need(all(c.norm2(c.sub(a,b))<=bound**2 for a,b in zip(net,exact)),'expanded kernel dense oracle')
                d.compose(x,y,fs,scratch,phases,beta,bits,direction,-1);c.need(x==x0 and scratch==s0 and y==y0,'kernel inverse word')
                cases.append(dict(radix=st['radix'],embedding=st['embedding'],length=n,direction=direction,dirt=dirt,bits=bits,bound=str(bound),leaf_calls=stats['leaves']))
    print('PASS kernel',row['radix'],row['embedding'],flush=True)
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.write_text(json.dumps(dict(status='passed',certificates=certs,cases=cases),indent=2)+'\n');print('PASS',len(cases),'kernel cases')
