"""Compose pinned shared-donor plans with the reconstructed R779 word.

The selection is Dugongue's PR404, using PR401's response-space machinery.
Removed helpers are mapped explicitly. No independent gains are added.
Apache-2.0; prepared with substantial OpenAI Codex assistance.
"""
import copy,importlib.util,pathlib
from collections import defaultdict
from fractions import Fraction as Q
import exact
ROOT=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('pinned_response_frames',ROOT/'vendor/source401/frames/reconstruct.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
from vendor.source376.two_alias import inside,meet

def shared(signed,plans):
    base=copy.deepcopy(signed);rows=G.replay(base)
    hits=[g for g in base['B']if g==['in',203,201,[[491,1,2]]]]
    assert len(hits)==1 and len(base['frames'][203])==8 and len(base['frames'][942])==7
    hits[0][1]=942;G.rehist_and_audit(base)
    assert G.replay(base)==rows and exact.rawmap(base)==exact.rawmap(signed)
    first=G.first_frames(base);c=copy.deepcopy(base);removed={556,577}
    def mapped(r):
        assert r not in removed
        return r-sum(d<r for d in removed)
    selected=[];head=defaultdict(list)
    for frozen in plans['plans']:
        assert not removed&set(frozen['donors'])
        plan=copy.deepcopy(frozen);plan['pivots']=[p for p in plan['pivots']if p['pivot']not in removed]
        roles={mapped(r)for r in plan['donors']}|{mapped(p['pivot'])for p in plan['pivots']}
        basis=tuple(plan['basis'])
        for r in sorted(roles):basis=meet(basis,tuple(base['frames'][first[r]]))
        assert basis
        f=next((i for i,b in enumerate(c['frames'])if inside(basis,tuple(b))and len(b)==len(basis)),len(c['frames']))
        if f==len(c['frames']):c['frames'].append(list(basis))
        for p in plan['pivots']:
            pivot=mapped(p['pivot']);coef={mapped(int(r)):Q(a)for r,a in p['coefficients'].items()}
            assert all(rows[t].get(pivot,Q(0))+sum(q*rows[t].get(r,Q(0))for r,q in coef.items())==0 for t in range(120,240))
            c['start'][pivot]=f;selected.append((f,pivot,coef))
            for r,q in coef.items():head[r,f].append([pivot,q.numerator,q.denominator])
    pivots={p for f,p,coef in selected};donors={r for f,p,coef in selected for r in coef}
    assert not pivots&donors and len(pivots)==len(selected)
    unit=[]
    for(r,f),es in sorted(head.items(),key=lambda item:(len(c['frames'][item[0][1]]),item[0][1],item[0][0])):
        for p,a,b in sorted(es):
            assert b in(1,2) and a
            unit.extend(['in',f,r,[[p,1 if a>0 else-1,b]]]for _ in range(abs(a)))
    c['A']=unit+base['A'];c['ext']=sorted([p,f]for f,p,coef in selected)
    transitions=G.rehist_and_audit(c);actual=G.replay(c)
    for t in range(240+c['R']):
        wanted=dict(rows[t])
        for f,p,coef in selected:
            value=wanted.get(p,Q(0))+sum(a*rows[t].get(r,Q(0))for r,a in coef.items())
            if value:wanted[p]=value
            else:wanted.pop(p,None)
        assert actual[t]==wanted
    assert all(p not in actual[t]for f,p,coef in selected for t in range(120,240))
    mass=sum(len(c['frames'][f])for f,p,coef in selected)
    assert (len(selected),mass,len(unit))==(192,350,496)
    for i in(0,len(unit)//2,len(unit)-1):
        bad=copy.deepcopy(c);bad['A'].pop(i)
        assert G.replay(bad)!=actual
    report=dict(gauges=len(selected),entrance_rankmass=mass,unit_entrance_gates=len(unit),nested_transitions=transitions,raw_columns=240+c['R'],removed_original_helpers=sorted(removed),omission_controls=3,retimed_frame_control=exact.rawmap(base)==exact.rawmap(signed),excluded_composition='PR404 overlapping target125/124 recovery is incompatible with the R779 prefix input and is not imported.')
    return c,base,report

def build(signed):
    """Fixed checker-clean repivots, enlargements and ordered promotions.

    Four shared-donor repivots and two sequential repivots are from PR412.
    Eight entrance enlargements originate in PR410; the four ordered groups
    originate in PR409. Their actual composition is rebuilt on our R779 word.
    """
    src=ROOT/'vendor/source412'
    spec=importlib.util.spec_from_file_location('pinned407_repivot',src/'repivot.py')
    rp=importlib.util.module_from_spec(spec);spec.loader.exec_module(rp)
    text=(src/'seqenlarge.py').read_text(encoding='utf-8');scope={'copy':copy,'Q':Q}
    a=text.index('def enlarge(');b=text.index('\nPROM760',a)
    exec(compile(text[a:b],str(src/'seqenlarge.py'),'exec'),scope)
    a=text.index('def repivot_rows(')
    exec(compile(text[a:],str(src/'seqenlarge.py'),'exec'),scope)
    plans=exact.read(ROOT/'vendor/source404/selection194.json')
    for e in exact.read(src/'repivot-e8.json')['swaps']:
        plans=rp.swap(plans,e['plan'],e['out'],e['into'])
    plans=scope['enlarge'](plans,exact.read(src/'pr410/enlarged205.json')['changes'],{1020:1001})
    rp.check_global(plans)
    c,base,report=shared(signed,plans);prior=copy.deepcopy(c)
    selection=exact.read(src/'pr409/SELECTION.json')
    for e in exact.read(src/'repivot-e8seq.json')['swaps']:
        i=next(i for i,p in enumerate(selection)if p['vector']==e['plan_vector'])
        pivots=sorted(e['into']if p['pivot']==e['out']else p['pivot']for p in selection[i]['pivots'])
        selection[i]=scope['repivot_rows'](selection[i],pivots)
        assert selection[i]is not None
    removed={556,577}
    def mapped(r):
        assert r not in removed
        return r-sum(d<r for d in removed)
    first=G.first_frames(prior);used=set();ext=dict(c['ext']);prefix=[]
    for p in sorted(selection,key=lambda p:-p['gain']):
        roles={mapped(r)for r in p['donors']}|{mapped(z['pivot'])for z in p['pivots']}
        if roles&used:continue
        assert not roles&set(ext)
        basis=tuple(p['basis'])
        f=next((i for i,e in enumerate(c['frames'])if tuple(e)==basis),len(c['frames']))
        if f==len(c['frames']):c['frames'].append(list(basis))
        for r in roles:assert inside(basis,tuple(prior['frames'][first[r]]))
        for z in p['pivots']:
            pivot=mapped(z['pivot']);co={mapped(int(k)):Q(str(a))for k,a in z['coefficients'].items()}
            c['start'][pivot]=f;ext[pivot]=f
            for d,q in sorted(co.items()):
                assert q.denominator in(1,2)
                prefix.extend(['in',f,d,[[pivot,1 if q>0 else-1,q.denominator]]]for _ in range(abs(q.numerator)))
        used|=roles
    c['A']=prefix+c['A'];c['ext']=sorted([p,f]for p,f in ext.items());G.rehist_and_audit(c)
    actual,retained=exact.rawmap(c);before,ret=exact.rawmap(prior)
    wanted=copy.deepcopy(before);wanted_ret=copy.deepcopy(ret)
    for g in reversed(prefix):
        _,f,d,((p,a,b),)=g;q=Q(a,b)
        for row in wanted+list(wanted_ret.values()):
            z=row.get(p,Q(0))+q*row.get(d,Q(0))
            if z:row[p]=z
            else:row.pop(p,None)
    assert (actual,retained)==(wanted,wanted_ret)
    assert all(p not in actual[t]for p in ext for t in range(120,240))
    head=c['A'][:len(c['A'])-len(base['A'])];written=set()
    for g in head:
        (p,a,b),=g[3];assert p not in written;written.add(g[2])
    mass=sum(len(c['frames'][f])for f in ext.values())
    assert (len(ext),mass,len(head),len(prefix))==(202,360,551,55)
    # Preserve both unchanged legacy checker families, including the sixths
    # denominator guard that requires re-pivoting the half-valued donor.
    for name in ('gx','gxcore'):
        path=ROOT.parent/'e8-coupled-bit-retiming/vendor/source384/complex/gx'/(name+'.py')
        spec=importlib.util.spec_from_file_location('strict_entrance_'+name,path)
        checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
        if name=='gx':checker.check1(c)
        else:checker.mirror(checker.normal(c),batches=16)
    report.update(gauges=len(ext),entrance_rankmass=mass,unit_entrance_gates=len(head),sequential_prefix_gates=len(prefix),chronological_source_read_before_write=True,unchanged_gx_and_gxcore='PASS')
    return c,base,report
