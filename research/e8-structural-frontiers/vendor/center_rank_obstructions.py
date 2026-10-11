"""Exact obstructions to merely rebasing the eight frozen center forms.
Q-rank lower bounds use explicit nonzero integer minors modulo prime 101.
OpenAI Codex assistance; Apache-2.0; read-only suppliers.
"""
from fractions import Fraction as Q
from pathlib import Path
from math import lcm
import argparse,gzip,json,hashlib
HERE=Path(__file__).resolve().parent
P=HERE.parents[1]/'extension-repo/research/e8-clean-reuse-extension/data/kernel-base.json.gz'
SOURCE_SHA256='785a6160912b8bf8535ccd438c7d13c0730f874d6a5d07ef530e50279e7cf7d8'

def add(d,s,q):
    for k,x in list(s.items()):
        z=d.get(k,Q(0))+q*x
        if z:d[k]=z
        else:d.pop(k,None)

def mod_minor(B,eligible,p):
    # Column basis in Q^8. Nonzero modulo p certifies rational independence.
    basis={};used=[];det=1
    for s in eligible:
        col=[x[s]%p for x in B]
        for j in sorted(basis):
            z=col[j]
            if z:col=[(x-z*y)%p for x,y in zip(col,basis[j])]
        j=next((i for i,x in enumerate(col) if x),None)
        if j is None:continue
        pivot=col[j];inv=pow(pivot,-1,p);basis[j]=[(x*inv)%p for x in col];used.append(s);det=det*pivot%p
        if len(used)==len(B):break
    return used,det

def det_mod(A,p):
    a=[[x%p for x in row] for row in A];d=1
    for j in range(len(a)):
        k=next((k for k in range(j,len(a)) if a[k][j]),None)
        if k is None:return 0
        if j!=k:a[j],a[k]=a[k],a[j];d=-d
        q=a[j][j];d=d*q%p;inv=pow(q,-1,p)
        for k in range(j+1,len(a)):
            z=a[k][j]*inv%p
            a[k]=[(x-z*y)%p for x,y in zip(a[k],a[j])]
    return d%p

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',type=Path,default=P)
    parser.add_argument('--output',type=Path,default=HERE/'CENTER-RANK-OBSTRUCTIONS.json')
    args=parser.parse_args();source=args.source.resolve()
    raw=source.read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA256,'Pinned supplier bytes changed'
    c=json.loads(gzip.decompress(raw));v=c['v'];ports=c['ports'];h=c['h'];p=101
    assert (h,v,c['R'],len(c['ret']))==(9,120,779,8)
    assert len(set(ports))==v and all(q.bit_count()%2==1 for q in ports)
    assert all(len(c['frames'][f])==9 for k,r,f in c['ret'])
    rows=[{i:Q(1)} if i<v else {} for i in range(2*v+c['R'])]
    for g in c['A']:
        for r,a,b in g[3]:
            d,s=(r,g[2]) if g[0]=='out' else (g[2],r)
            add(rows[d],rows[s],Q(a,b))
    Bq=[[rows[r].get(i,Q(0)) for i in range(v)] for k,r,f in c['ret']]
    scale=lcm(*(x.denominator for row in Bq for x in row))
    B=[[int(x*scale) for x in row] for row in Bq]
    C=[[Q(0) for _ in range(v)] for _ in range(v)]
    for t,terms in enumerate(c['scat']['table']):
        for k,a,b in terms:
            for s in range(v):C[t][s]+=Q(a,b)*Bq[k][s]
    odd=lambda a,b:(a&b).bit_count()%2
    assert all(C[t][t]==1 for t in range(v))
    assert all(not C[t][s] for t in range(v) for s in range(v) if t!=s and odd(ports[t],ports[s]))
    adj=[{j for j in range(v) if j!=i and odd(ports[i],ports[j])} for i in range(v)]
    def clique(chosen,candidates,goal):
        if len(chosen)==goal:return chosen
        if len(chosen)+len(candidates)<goal:return None
        while candidates:
            z=min(candidates);candidates.remove(z)
            r=clique(chosen+[z],candidates&adj[z],goal)
            if r:return r
        return None
    witness=clique([],set(range(v)),8);assert witness
    assert [[C[i][j] for j in witness] for i in witness]==[[Q(i==j) for j in range(8)] for i in range(8)]
    hyperplanes=[];low=[]
    for a in range(1,1<<h):
        outside=[i for i,q in enumerate(ports) if odd(a,q)]
        pivot,unused=mod_minor(B,outside,p)
        if len(pivot)==8:
            assert len(set(pivot))==8 and all(odd(a,ports[s]) for s in pivot)
            determinant=det_mod([[row[s] for s in pivot] for row in B],p);assert determinant
            hyperplanes.append(dict(normal=a,outside_ports=len(outside),minor_columns=pivot,nonzero_minor_mod101=determinant))
        else:low.append(dict(normal=a,outside_rank_mod101=len(pivot),outside_ports=len(outside)))
    result=dict(status='PASS_FROZEN_CENTER_RANK_OBSTRUCTIONS',source=str(source),source_sha256=hashlib.sha256(raw).hexdigest(),
        cleared_center_gather_denominator=scale,center_rows=8,ports=v,
        orthogonality_forbidden_pattern=True,identity_minor_ports=witness,identity_minor_binary_ports=[ports[i] for i in witness],
        scalar_channel_lower_bound=8,
        hyperplanes_checked=(1<<h)-1,full_rank_outside_hyperplanes=len(hyperplanes),
        lower_rank_outside_hyperplanes=low,explicit_modular_minors=hyperplanes,
        conclusion='If all 511 outside restrictions have rank8, every nonzero form in the frozen center row-space has full binary source-span9. Basis changes of those eight centers then cannot lower copied frame rank. This does not classify other central completions or joint nonmonotone constructions.')
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='explicit_modular_minors'},indent=2))

if __name__=='__main__':main()
