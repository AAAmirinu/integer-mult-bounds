"""Legal extremal-frame coalescence on the pinned PR370 word.

New code prepared with OpenAI Codex assistance, Apache-2.0.
The float rank_cost guides discovery; acceptance is certified independently."""
import copy, math, random
from collections import defaultdict
from pathlib import Path
import os, sys
os.environ['E8COORD']='ham'
sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor/source375/code/bit/producer'))
import frames as F

def rank_cost(r):
    return r*math.log(40/r) if r else 0.0

def nodes_of(c):
    masks=[sum(1<<s for s in fr) for fr in c['frames']]
    # Pins at the scatter keep each retained total at full and each target at zero.
    nodes=[]
    for phase in ('D','A','B','C'):
        if phase=='B':
            for r in c['ret']:nodes.append(dict(mask=F.FULL,regs=[r],fixed=True,pin=True))
            for r in range(120,240):nodes.append(dict(mask=0,regs=[r],fixed=True,pin=True))
        for j,gate in enumerate(c[phase]):
            f,d,ss=gate
            nodes.append(dict(mask=masks[f],regs=[d]+ss,fixed=phase=='D',phase=phase,index=j,gate=gate,pin=False))
    return nodes,masks

def links(nodes,c,masks):
    byreg=defaultdict(list)
    for i,n in enumerate(nodes):
        for r in n['regs']:byreg[r].append(i)
    previous={};following={}
    for r,ids in byreg.items():
        for p,i in enumerate(ids):
            previous[i,r]=ids[p-1] if p else ('start',r)
            following[i,r]=ids[p+1] if p+1<len(ids) else ('final',r)
    def frame(key):
        if isinstance(key,int):return nodes[key]['mask']
        kind,r=key;return masks[c[kind][r]]
    return previous,following,frame

def edge_cost(a,b):
    assert F.inside(a,b)
    return rank_cost(F.dim(b)-F.dim(a))

def interval(group,nodes,previous,following,frame):
    low=0;high=F.FULL;edges={}
    for i in group:
        for r in nodes[i]['regs']:
            a=previous[i,r];b=following[i,r]
            if a not in group:
                low=F.join(low,frame(a));edges.setdefault(r,[None,None])[0]=a
            if b not in group:
                high &= frame(b);edges.setdefault(r,[None,None])[1]=b
    assert F.inside(low,high)
    return low,high,edges

def cost(mask,edges,frame):
    return sum(edge_cost(frame(a),mask)+edge_cost(mask,frame(b)) for a,b in edges.values())

def write_nodes(c,nodes):
    out=copy.deepcopy(c);masks=[sum(1<<s for s in f) for f in out['frames']];ids={m:i for i,m in enumerate(masks)}
    for phase in ('D','A','B','C'):out[phase]=[]
    for n in nodes:
        if n.get('pin'):continue
        m=n['mask']
        if m not in ids:
            ids[m]=len(out['frames']);out['frames'].append([s for s in range(120) if m>>s&1])
        _,d,ss=n['gate'];out[n['phase']].append([ids[m],d,list(ss)])
    return out

def retime(c,method,sweeps=3,seed=0):
    nodes,masks=nodes_of(c);changes=[];rng=random.Random(seed)
    previous,following,frame=links(nodes,c,masks)
    for sweep in range(sweeps):
        moved=0
        order=[i for i,n in enumerate(nodes) if not n['fixed']]
        if sweep%2:order.reverse()
        if seed:rng.shuffle(order)
        for i in order:
            low,high,edges=interval({i},nodes,previous,following,frame)
            candidates=[low] if method=='retime_lower' else [high] if method=='retime_upper' else [low,high]
            old=nodes[i]['mask'];before=cost(old,edges,frame)
            chosen=min(candidates+[old],key=lambda m:cost(m,edges,frame))
            delta=cost(chosen,edges,frame)-before
            if delta < -1e-9:
                nodes[i]['mask']=chosen;moved+=1
                changes.append(dict(sweep=sweep,phase=nodes[i]['phase'],index=nodes[i]['index'],old=str(old),new=str(chosen),entropy_delta=delta))
        if not moved:break
    return write_nodes(c,nodes),changes

def components(c,sweeps=3):
    nodes,masks=nodes_of(c);previous,following,frame=links(nodes,c,masks);changes=[]
    for sweep in range(sweeps):
        groups=[];seen=set()
        for i,n in enumerate(nodes):
            if n['fixed'] or i in seen:continue
            group={i};todo=[i]
            while todo:
                j=todo.pop()
                for r in nodes[j]['regs']:
                    for k in (previous[j,r],following[j,r]):
                        if isinstance(k,int) and not nodes[k]['fixed'] and k not in group and nodes[k]['mask']==n['mask']:
                            group.add(k);todo.append(k)
            seen.update(group);groups.append(group)
        moved=0
        for group in groups:
            if len(group)<2:continue
            low,high,edges=interval(group,nodes,previous,following,frame)
            old=nodes[min(group)]['mask'];before=cost(old,edges,frame)
            chosen=min((low,high,old),key=lambda m:cost(m,edges,frame));delta=cost(chosen,edges,frame)-before
            if delta < -1e-9:
                for i in group:nodes[i]['mask']=chosen
                moved+=1;changes.append(dict(sweep=sweep,size=len(group),old=str(old),new=str(chosen),entropy_delta=delta))
        if not moved:break
    return write_nodes(c,nodes),changes

def pairs(c,sweeps=2,seed=0):
    nodes,masks=nodes_of(c);previous,following,frame=links(nodes,c,masks);changes=[];rng=random.Random(seed)
    for sweep in range(sweeps):
        candidates=set()
        for i,n in enumerate(nodes):
            if n['fixed']:continue
            for r in n['regs']:
                j=following[i,r]
                if isinstance(j,int) and not nodes[j]['fixed'] and n['phase']==nodes[j]['phase']:
                    candidates.add((i,j))
        order=sorted(candidates)
        if seed:rng.shuffle(order)
        moved=0
        for i,j in order:
            group={i,j};occurrences=defaultdict(list)
            for k in (i,j):
                for r in nodes[k]['regs']:occurrences[r].append(k)
            # A pair sharing multiple roles may have an outside occurrence
            # between its members. Such a pair cannot be coalesced here.
            if any(len(ids)==2 and following[ids[0],r]!=ids[1] for r,ids in occurrences.items()):continue
            low=0;high=F.FULL;before=0.0;edges={}
            for r,ids in occurrences.items():
                a=previous[ids[0],r];b=following[ids[-1],r]
                low=F.join(low,frame(a));high &= frame(b);edges[r]=(a,b)
                chain=[frame(a)]+[nodes[k]['mask'] for k in ids]+[frame(b)]
                before+=sum(edge_cost(x,y) for x,y in zip(chain,chain[1:]))
            if not F.inside(low,high):continue
            chosen=min((low,high),key=lambda m:cost(m,edges,frame));delta=cost(chosen,edges,frame)-before
            if delta<-1e-9:
                old=[nodes[i]['mask'],nodes[j]['mask']]
                nodes[i]['mask']=nodes[j]['mask']=chosen;moved+=1
                changes.append(dict(sweep=sweep,phase=nodes[i]['phase'],indices=[nodes[i]['index'],nodes[j]['index']],old=list(map(str,old)),new=str(chosen),entropy_delta=delta))
        if not moved:break
    return write_nodes(c,nodes),changes

def commute(c,direction,cleanup=False,max_distance=32):
    nodes,masks=nodes_of(c);changes=[]
    # Preserve the order of every pair of operations that share a register.
    # Scatter pins block every move across the copied-total boundary.
    i=0
    while i<len(nodes):
        n=nodes[i]
        if n['fixed'] or n.get('pin') or (cleanup and n['phase']!='C'):
            i+=1;continue
        step=1 if direction=='forward' else -1;dest=i;own=set(n['regs'])
        for d in range(1,max_distance+1):
            j=i+step*d
            if not 0<=j<len(nodes):break
            other=nodes[j]
            if other.get('pin') or other['fixed'] or (not cleanup and other['phase']!=n['phase']):break
            if own.intersection(other['regs']):break
            dest=j
        if dest!=i:
            old_nodes=list(nodes);nodes.pop(i);nodes.insert(dest,n)
            previous,following,frame=links(nodes,c,masks)
            low,high,edges=interval({dest},nodes,previous,following,frame)
            old=n['mask'];before=cost(old,edges,frame)
            chosen=min((low,high,old),key=lambda m:cost(m,edges,frame))
            if cost(chosen,edges,frame)<before-1e-9:
                n['mask']=chosen
                if cleanup and nodes[dest-1].get('phase')=='B':n['phase']='B'
                changes.append(dict(index=i,destination=dest,old=str(old),new=str(chosen)))
            else:nodes=old_nodes
        i+=1
    return write_nodes(c,nodes),changes

def groups(c,size=3,sweeps=3,limit=100000):
    nodes,masks=nodes_of(c);prev,nxt,frame=links(nodes,c,masks);changes=[]
    adjacency=defaultdict(set)
    for i,n in enumerate(nodes):
        if n['fixed']:continue
        for r in n['regs']:
            j=nxt[i,r]
            if isinstance(j,int) and not nodes[j]['fixed'] and n['phase']==nodes[j]['phase']:
                adjacency[i].add(j);adjacency[j].add(i)
    pairs={tuple(sorted((i,j))) for i in adjacency for j in adjacency[i]}
    candidates=pairs
    for target_size in range(3,size+1):
        expanded=set()
        for previous_group in sorted(candidates):
            neighbors=set().union(*(adjacency[i] for i in previous_group))
            for j in sorted(neighbors):
                group=tuple(sorted(set(previous_group)|{j}))
                if len(group)==target_size:expanded.add(group)
                if len(expanded)>=limit:break
            if len(expanded)>=limit:break
        candidates=expanded
    for sweep in range(sweeps):
        moved=0
        for group in sorted(candidates):
            occurrences=defaultdict(list)
            for i in group:
                for r in nodes[i]['regs']:occurrences[r].append(i)
            if any(any(nxt[a,r]!=b for a,b in zip(ids,ids[1:])) for r,ids in occurrences.items()):continue
            low=0;high=F.FULL;before=0.;edges={}
            for r,ids in occurrences.items():
                a=prev[ids[0],r];b=nxt[ids[-1],r]
                low=F.join(low,frame(a));high &= frame(b);edges[r]=(a,b)
                chain=[frame(a)]+[nodes[i]['mask'] for i in ids]+[frame(b)]
                before+=sum(edge_cost(a,b) for a,b in zip(chain,chain[1:]))
            if not F.inside(low,high):continue
            chosen=min((low,high),key=lambda m:cost(m,edges,frame))
            delta=cost(chosen,edges,frame)-before
            if delta < -1e-9:
                changes.append(dict(sweep=sweep,phase=nodes[group[0]]['phase'],indices=[nodes[i]['index'] for i in group],old=[str(nodes[i]['mask']) for i in group],new=str(chosen),entropy_delta=delta))
                for i in group:nodes[i]['mask']=chosen
                moved+=1
        if not moved:break
    return write_nodes(c,nodes),changes,len(candidates)
