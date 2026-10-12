"""Deterministically rebuild the two factored extra cold-end recipe from pinned PR623.

Nomination only. The unchanged cold-end constructor, native replay, phase,
owner and exact global verifiers independently admit the resulting recipe.
Jeremy Diviney with OpenAI Codex assistance; Apache-2.0. Uses the inherited
DreamingOfClouds/jeremykothe2 exact scalar and cold-end machinery.
"""
import argparse,copy,gzip,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path


def main():
    if not __debug__:raise RuntimeError('Assertions required; run without -O')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base-word',type=Path,required=True,help='PR623 jp8 final cold-ended word')
    ap.add_argument('--base-hpe',type=Path,required=True,help='PR623 jp8 preceding hyperplane-ended word')
    ap.add_argument('--base-recipe',type=Path,required=True,help='Pinned PR623 cold-end recipe')
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();p=Path(__file__).resolve().parents[1]
    def load(name,path):
        s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
    b=load('coldbuild',p/'code/build_cold_end.py');au=load('scalar',p/'code/hpe_audit_and_transport.py')
    read=lambda f:json.loads(gzip.decompress(f.read_bytes()))
    enc=lambda x:json.dumps(x,sort_keys=True,separators=(',',':')).encode()
    sha=lambda x:hashlib.sha256(x).hexdigest()
    d=json.loads((p/'data/FACTORED-END.json').read_text())
    assert sha(gzip.decompress(a.base_word.read_bytes()))==d['base_cold_word_content_sha256']
    assert sha(a.base_recipe.read_bytes())==d['base_recipe_sha256']
    old=read(a.base_word);base=read(a.base_hpe);recipe=read(a.base_recipe)
    assert enc(b.apply(copy.deepcopy(base),copy.deepcopy(recipe)))==enc(old)
    w=copy.deepcopy(old);v=w['report']['v'];n=2*v+w['report']['R'];new_ends={z['helper']:z['terminal_frame']for z in d['helpers']}
    assert len(new_ends)==2 and all(str(h)not in w['start_extra']and str(h)not in w['helper_final']for h in new_ends)
    for e in d['premix']:
        assert e[0]=='add'and e[-1]==[]
        assert all(2*v<=r<n and str(r)not in w['start_extra']for r in b.regs(e))
    A=copy.deepcopy(base['A'])
    ins=recipe['forward_insertions']+d['additional_forward_insertions']
    assert len({t for t,e in ins})==len(ins)
    for t,gate in sorted(ins,key=lambda x:-x[0]):
        assert all(gate[1]not in b.regs(e)for e in base['A'][t+1:]+base['cut']+base['B'])
        A.insert(t+1,copy.deepcopy(gate))
    w['A']=d['premix']+recipe['premix']+A
    w['helper_final'].update({str(h):U for h,U in new_ends.items()})
    tail=[old['cleanup'][i][:-1]+[F]for i,F in old['early_cleanup']]+d['extra_tail']
    P,_=au.state_maps(w['A']+w['cut']+w['B']+tail,n);ended=set(map(int,w['helper_final']))
    for j in ended:
        assert P[j]=={j:Q(1)}
        assert all(not P[i].get(j)for i in range(n)if i!=j and not v<=i<2*v)
    full=[256,128,64,32,16,8,4,2,1];rest=[]
    def emit(e):au.apply(e,P);rest.append(e)
    def add(t,s,z):return ['add',t,s,z.numerator,z.denominator,full]
    def unit(z):return z and abs(z.numerator)&(abs(z.numerator)-1)==0 and z.denominator&(z.denominator-1)==0
    remaining=[j for j in range(n)if not v<=j<2*v and j not in ended]
    for k,j in enumerate(remaining):
        pivot=next((i for i in remaining[k:]if unit(P[i].get(j,Q(0)))),None)
        assert pivot is not None,('no signed dyadic unit pivot',j)
        if pivot!=j:
            emit(add(j,pivot,Q(1)));emit(add(pivot,j,Q(-1)));emit(add(j,pivot,Q(1)));emit(['scale',pivot,-1,1,full])
        z=P[j][j]
        if z!=1:emit(['scale',j,(1/z).numerator,(1/z).denominator,full])
        for i in remaining:
            if i!=j and P[i].get(j):emit(add(i,j,-P[i][j]))
    assert all(P[j]=={j:Q(1)}for j in range(n)if not v<=j<2*v)
    w['cleanup']=tail+rest;w['early_cleanup']=[[i,e[-1]]for i,e in enumerate(tail)]
    recipe['premix']=d['premix']+recipe['premix']
    recipe['forward_insertions'].extend(d['additional_forward_insertions'])
    recipe['cold_ends'].update({str(h):U for h,U in new_ends.items()});recipe['cleanup']=w['cleanup'];recipe['early_cleanup']=w['early_cleanup']
    meta=copy.deepcopy(old['refactored_cleanup']);meta['cold_low_frame_ended_helpers']=sorted(map(int,recipe['cold_ends']))
    meta['premix_gates']=len(recipe['premix']);meta['lower_frame_gates']+=len(d['extra_tail'])
    meta['forward_absorptions']=len(recipe['forward_insertions'])
    meta['forward_absorption_A_indices']=[len(recipe['premix'])+t+1+j for j,(t,e)in enumerate(sorted(recipe['forward_insertions']))]
    for i,(_,e)in zip(meta['forward_absorption_A_indices'],sorted(recipe['forward_insertions'])):assert w['A'][i]==e
    meta['construction']+='; two exploratory factored extra ends 590 and581'
    w['refactored_cleanup']=recipe['refactored_cleanup']=meta
    oldp,_=b.chain_profile(old);newp,_=b.chain_profile(w);prof=Counter({int(k):c for k,c in old['report']['local_profile'].items()});prof.subtract(oldp);prof.update(newp)
    assert {k:newp[k]-oldp[k]for k in set(oldp)|set(newp)if newp[k]!=oldp[k]}=={1:2,2:2,5:-2}
    w['report']['local_profile']={str(k):c for k,c in sorted(prof.items())if c};w['report']['local_rank_mass']=sum(k*c for k,c in prof.items())
    inv=Counter({int(k):c for k,c in old['report']['width_inventory'].items()});inv[9]-=2;inv[7]+=2;w['report']['width_inventory']={str(k):c for k,c in sorted(inv.items())if c}
    payload=enc(w);recipe['output_content_sha256']=sha(payload)
    assert sha(payload)==d['expected_output_content_sha256']
    assert enc(b.apply(copy.deepcopy(base),recipe))==payload
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'FULL-WORD.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    (a.out/'COLD-END-RECIPE.json.gz').write_bytes(gzip.compress(enc(recipe),mtime=0))
    print('NOMINATION REPRODUCED; unchanged full verification required;',sha(payload))


if __name__=='__main__':main()
