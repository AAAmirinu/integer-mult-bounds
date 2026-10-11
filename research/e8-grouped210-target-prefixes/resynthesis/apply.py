"""PR402's exact two-target resynthesis with fresh all-column/ledger checks.

Algorithm and fixed designs: Chafik Boukhalfa with Anthropic Claude, PR402,
7883c63ec724999b921c2304b66648cbb9e7a112. Integration: OpenAI Codex.
The unchanged upstream implementation and proof are retained beside this file.
"""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import copy, hashlib, json, sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/'frames'))
import reconstruct as R

def apply(c, design):
    v=c['v']; na=len(c['A']); d=copy.deepcopy(c); at={}; setups=[]
    for e in design:
        t=e['target']; assert v<=t<2*v
        for pos,f,s,a,b in e['deliveries']:
            assert na<pos<=na+len(c['B']) and a
            at.setdefault(pos,[]).append(['in',f,t,[[s,a,b]]])
            if v<=s<2*v: setups.append(['in',0,t,[[s,-a,b]]])
    targets={e['target'] for e in design}; B=list(setups)
    for bi,g in enumerate(c['B']):
        if g[0]=='in' and g[2] in targets:
            B.extend(['out',g[1],s,[],[]] for s,_,_ in g[3])
        else:
            assert not(g[0]=='out' and any(t in targets for t,_,_ in g[3]))
            B.append(copy.deepcopy(g))
        B.extend(at.get(na+bi+1,[]))
    d['B']=B; R.rehist_and_audit(d)
    return d

def main():
    source,out=map(Path,sys.argv[1:3]); assert not out.exists()
    c=json.loads(source.read_text()); design=json.loads((ROOT/'designs.json').read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='fa92093379f96b13689d4f95359b19440a7f968cd967a9e5d2ecb3f961b24fc3'
    assert len(c['A'])==2135 and len(c['B'])==1760
    original=json.loads((ROOT/'PR402-DESIGNS.json').read_text())
    relocated=copy.deepcopy(original)
    for e in relocated:
        for delivery in e['deliveries']:
            cut=delivery[0]-1700
            assert 0<cut<=1759
            # Shared gauges add435 A instructions. The certified chronological
            # target recovery inserts B25, removes oldB860, and inserts after
            # oldB1164. These are counts of completed source B instructions.
            delivery[0]+=435+(cut>=25)-(cut>=861)+(cut>=1165)
    assert design==relocated
    assert sorted(e['target'] for e in design)==[177,220]
    d=apply(c,design); before=R.replay(c); after=R.replay(d)
    assert before==after
    for k in ['A','ret','scat','frames','ext','start','final','h','v','R','cst','N']:
        assert d[k]==c[k],k
    delta=R.histogram(d);delta.subtract(R.histogram(c))
    assert {k:v for k,v in delta.items() if v}=={2:2,3:-2,5:-2,6:2}
    controls=[]
    for name in ['omit_setup','flip_delivery','wrong_frame']:
        bad=copy.deepcopy(d)
        if name=='omit_setup':bad['B'].pop(0)
        elif name=='flip_delivery':
            j=next(i for i,g in enumerate(bad['B']) if g[0]=='in' and g[2]==220 and g[3][0][0]==779)
            bad['B'][j][3][0][1]*=-1
        else:
            j=next(i for i,g in enumerate(bad['B']) if g[0]=='in' and g[2]==220 and g[3][0][0]==779)
            bad['B'][j][1]=892
        try:
            R.rehist_and_audit(bad);assert R.replay(bad)==before
        except AssertionError:controls.append(name)
        else:raise AssertionError('accepted mutation '+name)
    out.mkdir();blob=json.dumps(d,sort_keys=True,separators=(',',':')).encode()
    (out/'candidate.json').write_bytes(blob)
    receipt=dict(status='PASS_EXACT_ALL_1021_COLUMNS_AND_NESTED_LEDGERS',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),candidate_sha256=hashlib.sha256(blob).hexdigest(),controls_rejected=controls,targets=[177,220],histogram_delta={k:v for k,v in delta.items() if v},source_pr=402,source_head='7883c63ec724999b921c2304b66648cbb9e7a112')
    (out/'RESYNTHESIS.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
if __name__=='__main__': main()
