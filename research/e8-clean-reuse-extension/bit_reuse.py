"""Novel-stream screen: per-read exact clean aliases, with original frame guards.
This private search does not claim a finite invoice or multiplication exponent.
"""
import argparse,bisect,copy,gzip,json,math,pathlib,sys,time
from collections import Counter,defaultdict
HERE=pathlib.Path(__file__).resolve().parent
PACKAGE=HERE.parent/'e8-coupled-bit-retiming'
sys.path.insert(0,str(PACKAGE));import retime
F=retime.F
sys.path.insert(0,str(PACKAGE/'vendor/source381/code/complex/code'));import bridged
IDLE=bridged.check(3,8)['blocks_per_role_pair']

def audit(c):
    v=c['v'];n=2*v+c['R'];cur=list(c['start']);masks=[sum(1<<s for s in f)for f in c['frames']];H=Counter();value=[1<<r for r in range(n)]
    def climb(r,f):
        a,b=masks[cur[r]],masks[f];assert not a&~b,(r,cur[r],f)
        d=F.dim(b)-F.dim(a)
        if d:H[d]+=1
        cur[r]=f
    for phase in ('D','A','B','C'):
        if phase=='B':
            assert all(cur[r]==1 for r in c['ret']) and all(cur[r]==0 for r in range(v,2*v))
            totals=[value[r]for r in c['ret']]
            H[8]+=len(c['ret'])
            for t,cs in enumerate(c['scatter']):
                for k in cs:value[v+t]^=totals[k]
        for f,d,ss in c[phase]:
            for r in [d]+ss:climb(r,f)
            for s in ss:value[d]^=value[s]
    for r,f in enumerate(c['final']):climb(r,f)
    expected=[1<<r for r in range(n)]
    for t in range(v):expected[v+t]^=1<<t
    assert value==expected,'All independent arbitrary-dirt columns'
    assert sum(r*k for r,k in H.items())==8*c['R']+2*v*7+8*len(c['ret'])
    return H

def reconstruct(c,p):
    ops=c['A']+c['B'];v=c['v'];n=2*v+c['R'];old,new,at,f,parents=(p[k]for k in['old','new','at','frame','reset_sources'])
    assert ops[at][0]==f and ops[at][1]==new
    assert all(new not in[d]+ss for ff,d,ss in ops[:at]),'new helper already live'
    assert all(old not in[d]+ss for ff,d,ss in ops[at:]),'old helper still live'
    vals=[1<<r if r<v else 0 for r in range(n)]
    for i,(ff,d,ss)in enumerate(ops[:at]):
        for s in ss:vals[d]^=vals[s]
        if i==len(c['A'])-1:
            totals=[vals[r]for r in c['ret']]
            for t,cs in enumerate(c['scatter']):
                for k in cs:vals[v+t]^=totals[k]
    z=vals[old]
    for s in parents:z^=vals[s]
    assert z==0,'reset is not an exact clean zero'
    old,new,at,f,parents=(p[k]for k in ['old','new','at','frame','reset_sources']);n=240+c['R'];out=copy.deepcopy(c);out['R']-=1
    assert old!=new and old not in parents and new not in parents and old not in c['ret']and new not in c['ret']
    def rename(r):return old if r==new else r
    keep=[r for r in range(n)if r!=new];ix={r:i for i,r in enumerate(keep)}
    out['start']=[c['start'][r]for r in keep];out['final']=[c['final'][r]for r in keep];out['ret']=[ix[rename(r)]for r in c['ret']]
    for phase,start in [('A',0),('B',len(c['A']))]:
        word=[]
        for k,(ff,d,ss)in enumerate(c[phase]):
            if start+k==at and parents:word.append([f,ix[old],[ix[r]for r in parents]])
            dest=ix[rename(d)];sources=[ix[rename(s)]for s in ss];assert dest not in sources
            word.append([ff,dest,sources])
        out[phase]=word
    v=120;n-=1;values=[0]*240+[1<<(r-240)for r in range(240,n)]
    for f,d,ss in out['A']:
        for s in ss:values[d]^=values[s]
    totals=[values[r]for r in out['ret']]
    for t,cs in enumerate(out['scatter']):
        for k in cs:values[v+t]^=totals[k]
    for f,d,ss in out['B']:
        for s in ss:values[d]^=values[s]
    out['D']=[[0,v+t,[240+r for r in range(out['R'])if values[v+t]>>r&1]]for t in range(v)if values[v+t]]
    out['C']=[[1,d,list(ss)]for f,d,ss in reversed(out['A']+out['B'])if d>=240]
    audit(out)
    return out

