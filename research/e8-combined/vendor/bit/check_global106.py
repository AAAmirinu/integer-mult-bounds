"""Independent eleven-stage schedule, geometry embedding and hosted ownership audit.
Derived from PR386/436/443/444 and DaysSky PR442; all source notices retained.
Eleven-stage integration by chafreaky with OpenAI Codex assistance, Apache-2.0.
No emitter, schedule constructor, hosting solver or expander is imported.
The local programs come from a separate exact record replay.
"""
import copy,gzip,hashlib,json,sys
from collections import Counter,defaultdict
from pathlib import Path
K,L,M,T,V,R=5,11,78,4,120,705
DATA=2*K*V*T
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load_template=lambda p:json.loads(gzip.decompress(p.read_bytes()))

def windows(schedule):
    last={};seen=[];win={};ranks={};pairs={}
    for position,event in enumerate(schedule):
        kind=event['kind']
        if kind=='local_cover_sweep':
            seen.append((position,event['stage'],event['pair']));last[event['pair']]=position
        elif kind=='bridge':
            last[event['dst']]=position;last[event['src']]=position
        elif kind=='idle':
            i=event['idx'];assert i not in win
            win[i]={s for pos,s,p in seen if last.get(event['pair'],-1)<pos<position and p!=event['pair']}
            ranks[i]=event['rank'];pairs[i]=event['pair']
        else:assert kind=='exchange' and position==len(schedule)-1
    return win,ranks,pairs

def schedule_check(schedule):
    # Ten formal integer rows, keeping the signs lost by F2 reduction.
    rows=[[int(i==j) for j in range(2*K)] for i in range(2*K)]
    levels=[-1]*K;stages=[];bridges=0;exchanged=False;idles=[]
    def add(dst,src,c):rows[dst]=[x+c*y for x,y in zip(rows[dst],rows[src])]
    for e in schedule:
        kind=e['kind'];assert not exchanged
        if kind=='local_cover_sweep':
            s,p,rev=e['stage'],e['pair'],e['reverse']
            assert s==len(stages) and 0<=s<L and p==max(0,(s-1)//2) and rev==bool(s%2)
            assert levels[p]==s-1
            add(2*p,2*p+1,-1) if rev else add(2*p+1,2*p,1)
            levels[p]=s;stages.append(s)
        elif kind=='idle':
            p,lo,hi=e['pair'],e['source_level'],e['target_level']
            assert 0<=p<K and levels[p]==lo and lo<=hi<=L-1 and e['rank']==7*(hi-lo)
            assert e['idx']==len(idles);idles.append((p,lo,hi,e['rank']));levels[p]=hi
        elif kind=='bridge':
            dst,src,c=e['dst'],e['src'],e['coefficient']
            assert 0<=dst<K and 0<=src<K and dst!=src and c in (-1,1) and levels[dst]==levels[src]
            add(2*dst,2*src,c);add(2*src+1,2*dst+1,-c);bridges+=1
        else:
            assert kind=='exchange' and levels==[L-1]*K
            for p in range(K):rows[2*p],rows[2*p+1]=rows[2*p+1],[-x for x in rows[2*p]]
            exchanged=True
    assert exchanged and rows==[[int(i==j) for j in range(2*K)] for i in range(2*K)]
    assert stages==list(range(L)) and bridges==3*(K-1)
    return idles

def audit(t,parent,widths):
    # The separate route checker verifies the concrete signed maps.
    assert (t['m'],t['h'],t['stages'],t['replicas'],t['live'],t['private_centre_reserve'])==(M,8,L,T,DATA,9)
    assert t['banks_per_stage']==0 and t['bank_padding'] is None
    for key in ('local_programs','entrance_rank_total','source_record_sha256'):
        assert t[key]==parent[key],key
    schedule_check(t['schedule'])
    win,rank,pair=windows(t['schedule']);hs=t['hosting'];used=defaultdict(set);hosted={}
    assert hs['windows']=={str(i):[pair[i],rank[i],sorted(win[i])] for i in win if rank[i] and win[i]}
    for i,cp,off,w,s,h in hs['slots']:
        assert i in win and s in win[i] and 0<=s<L and 0<=h<R*T and 0<=cp<2*V*T
        assert w==widths[h%R]>0 and 0<=off and off+w<=rank[i]
        cells=set(range(off,off+w));assert not cells&used[i,cp];used[i,cp]|=cells
        assert (s,h) not in hosted;hosted[s,h]=(i,cp,off,w)
    assert set(hosted)=={(s,h) for s in range(L) for h in range(R*T)}
    rem={};summaries={}
    for i in rank:
        if not rank[i]:continue
        for cp in range(2*V*T):rem[i,cp]=rank[i]-len(used[i,cp])
        if str(i) in hs['windows']:
            summaries[str(i)]={str(r):n for r,n in sorted(Counter(rem[i,cp] for cp in range(2*V*T)).items())}
    assert hs['remainders']==summaries
    assert len(t['calls'])==L*T;seen=set();paid=Counter()
    localhash={ori:hashlib.sha256(json.dumps(es,separators=(',',':')).encode()).hexdigest() for ori,es in t['local_programs'].items()}
    for index,c in enumerate(t['calls']):
        s,rep=c['stage'],c['replica'];p=max(0,(s-1)//2);rev=bool(s%2)
        assert (s,rep)==divmod(index,T) and c['pair']==p and c['orientation']==('reverse' if rev else 'forward')
        assert c['local_hash']==localhash[c['orientation']]
        own=c['owners'];assert len(own)==2*V+R
        assert len({(f,tuple(route)) for f,route in own})==2*V+R
        for j,(f,route) in enumerate(own):
            assert 0<=f<DATA
            if j<2*V:
                side=j//V;side=1-side if rev else side
                assert f==rep*(2*K*V)+(2*p+side)*V+j%V and route==['data',s,j%V]
            else:
                h=j-2*V;i,cp,off,w=hosted[s,rep*R+h];owner_rep,within=divmod(cp,2*V);side,port=divmod(within,V)
                assert pair[i]!=p and f==owner_rep*(2*K*V)+(2*pair[i]+side)*V+port
                assert route[:4]==['hosted',i,off,w] and len(route)==6
                assert (s,rep,h) not in seen;seen.add((s,rep,h))
        for z in t['local_programs'][c['orientation']]:
            if z[0]==0 and z[4]:paid[z[4]]+=1
            if z[0]==2:paid[z[5]]+=1
    assert len(seen)==L*T*R
    for r in rem.values():
        if r:paid[r]+=1
    assert M*DATA-sum(r*n for r,n in paid.items())==T*(2*K*V-72*L)
    assert M**2<=2*max(paid)**2 and M**3>2*max(paid)**3
    return paid

def expanded_digest(t):
    h=hashlib.sha256();count=0
    for call in t['calls']:
        for op in t['local_programs'][call['orientation']]:
            row=[op[0],call['owners'][op[1]]]
            if op[0]==0:row.extend(op[2:])
            else:
                row.append(call['owners'][op[2]] if op[2]<2*V+R else [t['live'],['private',0]])
                row.extend(op[3:])
            h.update(json.dumps(row,separators=(',',':')).encode());h.update(b'\n');count+=1
    return h.hexdigest(),count


def physical_prefix(t):
    bounds={i:1 for i in range(t['live'])};scratch=t['live'];bounds[scratch]=0;maximum=1
    stages=defaultdict(list)
    for c in t['calls']:stages[c['stage']].append(c)
    for e in t['schedule']:
        if e['kind']=='local_cover_sweep':
            for c in stages[e['stage']]:
                for z in t['local_programs'][c['orientation']]:
                    tag=z[0]
                    if tag==0:continue
                    dst=c['owners'][z[1]][0]
                    if tag==1:
                        sr=scratch if z[2]==2*V+R else c['owners'][z[2]][0]
                        bounds[dst]=bounds[dst]+abs(z[3])*bounds[sr]
                    elif tag==2:bounds[scratch]=bounds[dst]
                    else:assert tag==3;bounds[scratch]=0
                    maximum=max(maximum,bounds[dst],bounds[scratch])
        elif e['kind']=='bridge':
            for replica in range(T):
                for port in range(V):
                    for side in (0,1):
                        dp,sp=(e['dst'],e['src']) if side==0 else (e['src'],e['dst'])
                        dst=replica*2*K*V+(2*dp+side)*V+port;sr=replica*2*K*V+(2*sp+side)*V+port
                        bounds[dst]+=bounds[sr];maximum=max(maximum,bounds[dst])
    assert bounds[scratch]==0
    return maximum

def scalar_replay(t):
    n=2*K*V+L*R;local=2*V+R;scratch=n
    values=[1<<i for i in range(n)]+[0]
    for event in t['schedule']:
        kind=event['kind']
        if kind=='local_cover_sweep':
            stage,pair,reverse=event['stage'],event['pair'],event['reverse']
            def owner(r):
                if r==local:return scratch
                if r<2*V:
                    side,port=divmod(r,V)
                    return (2*pair+(1-side if reverse else side))*V+port
                return 2*K*V+stage*R+r-2*V
            before=values[:];center=None
            for row in t['local_programs']['reverse' if reverse else 'forward']:
                op=row[0]
                if op==0:continue
                dst,src=owner(row[1]),owner(row[2])
                if op==1:
                    assert dst!=center
                    if row[3]%2:values[dst]^=values[src]
                elif op==2:
                    assert center is None and not values[scratch]
                    center=dst;values[scratch]=values[dst]
                else:
                    assert center==dst and values[scratch]==values[dst]
                    center=None;values[scratch]=0
            assert center is None
            dst=(2*pair+(0 if reverse else 1))*V
            src=(2*pair+(1 if reverse else 0))*V
            for port in range(V):before[dst+port]^=before[src+port]
            assert before==values
        elif kind=='bridge':
            dst,src=event['dst'],event['src']
            for port in range(V):
                values[2*dst*V+port]^=values[2*src*V+port]
                values[(2*src+1)*V+port]^=values[(2*dst+1)*V+port]
        elif kind=='exchange':
            for pair in range(K):
                for port in range(V):
                    x,y=2*pair*V+port,(2*pair+1)*V+port
                    values[x],values[y]=values[y],values[x]
    assert values==[1<<i for i in range(n)]+[0]
    return n


def omitted_bridge_controls(schedule):
    def replay(skip):
        rows=[[int(i==j) for j in range(2*K)] for i in range(2*K)]
        bridge_index=0
        def add(dst,src,c):rows[dst]=[x+c*y for x,y in zip(rows[dst],rows[src])]
        for event in schedule:
            kind=event['kind']
            if kind=='local_cover_sweep':
                p=event['pair']
                if event['reverse']:add(2*p,2*p+1,-1)
                else:add(2*p+1,2*p,1)
            elif kind=='bridge':
                d,s,c=event['dst'],event['src'],event['coefficient']
                for dst,src,sign in ((2*d,2*s,c),(2*s+1,2*d+1,-c)):
                    if bridge_index!=skip:add(dst,src,sign)
                    bridge_index+=1
            elif kind=='exchange':
                for p in range(K):rows[2*p],rows[2*p+1]=rows[2*p+1],[-x for x in rows[2*p]]
        assert bridge_index==24
        return rows
    identity=[[int(i==j) for j in range(2*K)] for i in range(2*K)]
    assert replay(None)==identity
    for skip in range(24):assert replay(skip)!=identity
    return list(range(24))


def main():
    out,records_path,word_result_path,result_path,word_path=map(Path,sys.argv[1:])
    t=load_template(out/'GLOBAL-TEMPLATE.json.gz');g=read(out/'GLOBAL.json')
    records=read(records_path);word=read(word_result_path)
    assert records['word_sha256']==word['word_sha256']
    assert gzip.decompress((out/'word.json.gz').read_bytes())==word_path.read_bytes()
    assert sha(out/'word.json.gz')==g['word_sha256']
    state=read(out/'local/records/249-states.json');fs=read(out/'local/records/frames.json')['frames']
    widths=[8-fs[str(state['initial'][str(h)])]['dim'] for h in range(240,240+R)]
    parent=dict(local_programs=records['programs'],entrance_rank_total=word['entrance_rank_total'],source_record_sha256=records['record_sha256'])
    profile=audit(t,parent,widths)
    assert profile==Counter({int(k):v for k,v in g['profile'].items()})
    for name,check in records['checks'].items():
        assert check['sha256']==g['local_checks'][name]['sha256']
        assert check['profile']==g['local_checks'][name]['profile']
        assert check['row_l1_bound']==g['local_checks'][name]['cancellation_free_row_l1']
    assert t['geometry_sha256']==g['geometry_sha256']==sha(out/'GEOMETRY.json')
    assert t['source_record_sha256']==g['source_records_sha256']==sha(out/'local/records/249-records.bin')
    th=hashlib.sha256(gzip.decompress((out/'GLOBAL-TEMPLATE.json.gz').read_bytes())).hexdigest()
    assert th==g['template_sha256']
    digest,count=expanded_digest(t)
    assert (digest,count)==(g['emitted_program_sha256'],g['emitted_events'])
    assert (g['live'],g['physical'],g['hosted_residuals'],g['bank_assignments'],g['deficit'])==(4800,4809,L*T*R,0,1632)
    assert g['rank_mass']==sum(r*n for r,n in profile.items()) and g['paid_calls']==sum(profile.values()) and g['maxchild']==max(profile)
    columns=scalar_replay(t)
    omitted=omitted_bridge_controls(t['schedule'])
    assert omitted==g['omitted_bridge_shears_rejected']
    assert g['independent_unbanked_scalar_columns']==columns and len(g['scalar_stages'])==11 and g['all_scalar_columns_restored']
    prefix=physical_prefix(t)
    assert prefix==int(g['global_prefix_bound']) and prefix.bit_length()==g['global_prefix_bits']
    charged=64*((prefix.bit_length()+63)//64);assert charged==g['charged_prefix_bits']
    controls=[]
    def reject(name,fn):
        q=copy.deepcopy(t);fn(q)
        try:audit(q,parent,widths)
        except (AssertionError,KeyError,IndexError,TypeError):controls.append(name)
        else:raise AssertionError('accepted '+name)
    reject('slot outside idle window',lambda q:q['hosting']['slots'][0].__setitem__(4,10))
    reject('missing helper assignment',lambda q:q['hosting']['slots'].pop())
    reject('wrong residual width',lambda q:q['hosting']['slots'][0].__setitem__(3,9))
    reject('cross replica data owner',lambda q:q['calls'][0]['owners'][0].__setitem__(0,1200))
    reject('missing local instruction',lambda q:q['local_programs']['forward'].pop())
    reject('wrong reflected copy rank',lambda q:next(z for z in q['local_programs']['reverse'] if z[0]==2).__setitem__(5,0))
    reject('wrong bridge sign',lambda q:next(e for e in q['schedule'] if e['kind']=='bridge').__setitem__('coefficient',-1))
    reject('missing terminal exchange',lambda q:q['schedule'].pop())
    result=dict(status='PASS_INDEPENDENT_LOCAL_AND_GLOBAL_AUDIT_ROUTES_SEPARATE',template_sha256=th,
        emitted_program_sha256=digest,emitted_events=count,profile={str(r):n for r,n in sorted(profile.items())},
        live=DATA,physical=DATA+9,hosted_residuals=L*T*R,bank_assignments=0,
        rank_mass=sum(r*n for r,n in profile.items()),deficit=1632,maxchild=max(profile),halving_depth=3,
        physical_prefix_bits=prefix.bit_length(),charged_prefix_bits=charged,unbanked_scalar_columns=columns,
        word_sha256=word['word_sha256'],records_sha256=records['record_sha256'],mutations_rejected=controls,
        omitted_bridge_shears_rejected=omitted,
        independent_local_checks=records['checks'],entrance_rank_total=word['entrance_rank_total'],
        scope='Exact local word, actual exported records, full unbanked eleven-stage identity, whole-slot windows, emitted profile and positive physical-family prefix. Concrete signed route and geometry audit is a separate receipt. Complete-cover hosting and compiler interfaces remain conditional.')
    result_path.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='independent_local_checks'},indent=2))

if __name__=='__main__':main()
