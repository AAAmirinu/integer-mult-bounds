"""Bounded three-gate coalescence, extending the selected pair family."""
from pathlib import Path
import json, time, copy, gzip, argparse
from collections import defaultdict
import explore_e8 as X, retime_e8 as R
ROOT=Path(__file__).resolve().parent

def groups(c,size=3,sweeps=3,limit=100000):
    nodes,masks=R.nodes_of(c);prev,nxt,frame=R.links(nodes,c,masks);changes=[]
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
            low=0;high=R.F.FULL;before=0.;edges={}
            for r,ids in occurrences.items():
                a=prev[ids[0],r];b=nxt[ids[-1],r]
                low=R.F.join(low,frame(a));high &= frame(b);edges[r]=(a,b)
                chain=[frame(a)]+[nodes[i]['mask'] for i in ids]+[frame(b)]
                before+=sum(R.edge_cost(a,b) for a,b in zip(chain,chain[1:]))
            if not R.F.inside(low,high):continue
            chosen=min((low,high),key=lambda m:R.cost(m,edges,frame))
            delta=R.cost(chosen,edges,frame)-before
            if delta < -1e-9:
                changes.append(dict(sweep=sweep,phase=nodes[group[0]]['phase'],indices=[nodes[i]['index'] for i in group],old=[str(nodes[i]['mask']) for i in group],new=str(chosen),entropy_delta=delta))
                for i in group:nodes[i]['mask']=chosen
                moved+=1
        if not moved:break
    return R.write_nodes(c,nodes),changes,len(candidates)

def main():
    p=argparse.ArgumentParser();p.add_argument('--size',type=int,default=3);p.add_argument('--input',default='deep5-best.json.gz');args=p.parse_args()
    c=json.load(gzip.open(ROOT/args.input,'rt'));start=time.perf_counter();changes=[]
    for cycle in range(3):
        c,ch,count=groups(c,size=args.size);changes.extend(ch)
        c,ch=R.retime(c,'retime_both',sweeps=5);changes.extend(ch)
        c,ch=R.pairs(c,sweeps=3);changes.extend(ch)
    name='coupled-triples' if args.size==3 else f'coupled-groups-{args.size}'
    result=X.evaluate_word(c);result.update(name=name,changes=len(changes),candidate_groups=count,seconds=time.perf_counter()-start)
    out=ROOT/'deep5'/name;out.mkdir(parents=True,exist_ok=True)
    X.fullword.save(c,str(out/'word.json.gz'))
    (out/'changes.json').write_text(json.dumps(changes,indent=2)+'\n',encoding='utf-8')
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
