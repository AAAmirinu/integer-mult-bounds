"""Check the record export against the word and replay all formal columns."""
from collections import Counter
import gzip, hashlib, json, struct, sys
from pathlib import Path
from check_word import row_space, contains


def check(word, folder):
    raw = word.read_bytes()
    c = json.loads(gzip.decompress(raw) if word.suffix == '.gz' else raw)
    roots, n, v = c['lines'], 240+c['R'], 120
    bases = [row_space(roots[i] for i in ids) for ids in c['frames']]
    first = {}
    canonical = []
    for i, b in enumerate(bases):
        canonical.append(first.setdefault(b, i))
    zero = first[()]
    full = first[row_space(roots)]
    state = json.loads((folder/'249-states.json').read_text())
    frames = json.loads((folder/'frames.json').read_text())['frames']
    assert (state['n'], state['v'], state['h'], state['R'], state['ZERO'], state['FULL']) == (n,v,8,c['R'],zero,full)
    assert set(map(int,frames)) == set(first.values())
    for i, entry in frames.items():
        b, a = row_space(entry['B']), row_space(entry['A'])
        assert b == bases[int(i)] and entry['dim'] == len(b)
        assert len(a) == 8-len(b)
        assert all(sum(x*y for x,y in zip(u,w)) == 0 for u in b for w in a)
    initial = [canonical[f] for f in c['start']]
    final = [canonical[f] for f in c['final']]
    assert state['initial'] == {str(i):f for i,f in enumerate(initial)}
    assert state['final'] == {str(i):f for i,f in enumerate(final)}
    assert state['retained_totals'] == c['ret']
    expected = []
    current = initial[:]
    def move(r, f):
        f=canonical[f]
        if current[r] != f:
            old=current[r]
            expected.append((0,r,old,f,len(bases[f])-len(bases[old]),0))
            current[r]=f
    def gates(phase, marker):
        for f,dst,sources in c[phase]:
            for r in [dst]+sources:move(r,f)
            expected.extend((1,dst,s,1,canonical[f],marker) for s in sources)
    gates('D',1);gates('A',2)
    for k,r in enumerate(c['ret']):
        f=current[r]
        expected.append((2,r,n,f,zero,len(bases[f])))
        expected.extend((1,v+t,n,1,zero,3) for t,ks in enumerate(c['scatter']) if k in ks)
        expected.append((3,r,n,f,zero,0))
    gates('B',4);gates('C',5)
    for r,f in enumerate(c['final']):move(r,f)
    raw_records=(folder/'249-records.bin').read_bytes()
    records=list(struct.iter_unpack('<6i',raw_records))
    assert records == expected, 'record stream differs from the word'
    results, programs = {}, {}
    for reverse in (False,True):
        current=(final if reverse else initial)[:]+[None]
        values=[{i} for i in range(n)]+[set()]
        norm=[1]*n+[0]
        center=None;maxnorm=1;hist=Counter();adds=0;copies=0;events=[]
        dim=lambda f:8-len(bases[f]) if reverse else len(bases[f])
        for op,x,y,c0,f,z in reversed(records) if reverse else records:
            if op==0:
                before,after=(c0,y) if reverse else (y,c0)
                assert current[x]==before and dim(after)-dim(before)==f>0
                old,new=bases[before],bases[after]
                low,high=(new,old) if reverse else (old,new)
                assert all(contains(high,row) for row in low)
                current[x]=after;hist[f]+=1
                events.append([0,x,before,after,f,int(reverse)])
            elif op==1:
                assert current[x]==current[y]==f and x<n and x!=y and x!=center
                assert y!=n or center is not None
                if c0%2:values[x].symmetric_difference_update(values[y])
                norm[x]+=abs(c0)*norm[y];maxnorm=max(maxnorm,norm[x]);adds+=1
                events.append([1,x,y,-c0 if reverse else c0,f,int(reverse)])
            elif op==(3 if reverse else 2):
                assert center is None and y==n and current[x]==c0 and not values[n] and current[n] is None
                rank=abs(dim(c0)-dim(f));assert rank==8 and z==(0 if reverse else rank)
                center=x;current[n]=f;values[n]=set(values[x]);norm[n]=norm[x];hist[rank]+=1;copies+=1
                events.append([2,x,n,c0,f,rank,int(reverse)])
            else:
                assert op==(2 if reverse else 3) and center==x and y==n
                assert current[x]==c0 and current[n]==f and values[n]==values[x]
                values[n]=set();norm[n]=0;current[n]=None;center=None
                events.append([3,x,n,c0,f,z,int(reverse)])
        assert center is None and not values[n]
        assert current[:n]==(initial if reverse else final)
        assert values==[({r,r-v} if v<=r<2*v else {r}) for r in range(n)]+[set()]
        key='reverse' if reverse else 'forward';programs[key]=events
        results[key]=dict(all_columns=n, records=len(records),copies=copies,adds=adds,
            profile=dict(sorted(hist.items())),row_l1_bound=maxnorm,
            sha256=hashlib.sha256(json.dumps(events,separators=(',',':')).encode()).hexdigest())
    assert results['forward']['profile']==results['reverse']['profile']
    return dict(status='PASS_INDEPENDENT_RECORD_EXPORT_AND_REPLAY',word_sha256=hashlib.sha256(raw).hexdigest(),
        record_sha256=hashlib.sha256(raw_records).hexdigest(),frames=len(frames),programs=programs,checks=results)

if __name__=='__main__':
    word,folder,out=map(Path,sys.argv[1:]);r=check(word,folder)
    out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='programs'},indent=2))
