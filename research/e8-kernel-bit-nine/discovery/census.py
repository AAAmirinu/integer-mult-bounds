import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));sys.path.insert(1,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','code'))
from retime import *
from collections import Counter,defaultdict
def f2rank(vs):
    piv={};r=0
    for x in vs:
        while x:
            hb=x.bit_length()-1
            if hb in piv: x^=piv[hb]
            else: piv[hb]=x;r+=1;break
    return r
def census(c,M):
    v=c['v'];n=M.n
    dread=defaultdict(int)
    for f,t,srcs in c['D']:
        for s in srcs: dread[s]|=1<<(t-v)
    first={}
    for h in range(2*v,n):
        o=M.occ[h]; first[h]=next(M.fr(h,i) for i in range(1,len(o)) if M.fr(h,i)!=0)
    return dread,first
if __name__=='__main__':
    c=load_word(sys.argv[1]);M=Model(c);d=M.L.dim;v=120
    dread,first=census(c,M)
    ret=set(c['ret'])
    g=defaultdict(list)
    for h,f in first.items():
        if h not in ret: g[f].append(h)
    tot=0
    rows=[]
    for f,hs in g.items():
        k=len(hs);r=f2rank([dread[h] for h in hs]);rows.append((d(f),k,r));tot+=k-r
    print('exact-first-frame groups',len(g),'free pivots',tot)
    print(Counter((a,k,r) for a,k,r in rows).most_common(30))

def candidates(c,M,first,ret):
    L=M.L;v=c['v']
    fs=set(f for h,f in first.items() if h not in ret)
    cand=set()
    for f in fs:
        for i in range(v):
            if f>>i&1: cand.add(L.close(1<<i))
    fl=list(fs)
    for i in range(len(fl)):
        for j in range(i+1,len(fl)):
            x=fl[i]&fl[j]
            if x: cand.add(L.close(x))
    cand|=fs
    import os
    if os.environ.get('CAND2'):
        sub=set()
        for f in fs:
            ls=[i for i in range(v) if f>>i&1]
            for a in range(len(ls)):
                for b in range(a+1,len(ls)):
                    sub.add((1<<ls[a])|(1<<ls[b]))
        for x in sub: cand.add(L.close(x))
    return cand
