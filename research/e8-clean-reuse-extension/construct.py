"""Reconstruct the fixed complex and bit witnesses, with mathematical controls."""
import copy,gzip,hashlib,json,pathlib,sys,types
from collections import defaultdict
from fractions import Fraction as Q
import exact,inline,bit_reuse
ROOT=pathlib.Path(__file__).resolve().parent;PARENT=ROOT.parent/'e8-coupled-bit-retiming'
sys.path.insert(0,str(ROOT/'vendor/source376'));import candidate_frames,transport
def signed(c):
    source=(ROOT/'vendor/source395/construct.py').read_text(encoding='utf-8')
    function=source[source.index('def transform(c,selection):'):source.index('def emit(out):')]
    ns={'copy':copy,'Q':Q,'defaultdict':defaultdict,'up':types.SimpleNamespace(rehist=exact.rehist)}
    exec(compile(function,'unmodified pinned PR395 transform','exec'),ns)
    return ns['transform'](c,exact.read(ROOT/'data/signed-selection.json'))
def complex_build():
    c=json.loads(candidate_frames.build((PARENT/'vendor/source384/data/gcert1-e8-r783-far.json.gz').read_bytes()))
    for drop,terms in [(556,{354:Q(-2),461:Q(-2)}),(576,{402:Q(-2),478:Q(-2)})]:
        plans={r:t for r,t,reads in inline.proposals(c,4)};assert plans[drop]==terms
        c=inline.repair(c,drop,terms)
    d=signed(c);assert exact.rawmap(c)==exact.rawmap(d)
    controls=[]
    bad=copy.deepcopy(d);bad['B'].pop(0);assert exact.rawmap(bad)!=exact.rawmap(c);controls.append('signed setup omitted')
    entry=exact.read(ROOT/'data/signed-selection.json')[0];recovery=['in',entry['recovery_frame'],entry['destination'],[[entry['donor_target'],int(entry['coefficient']),1]]]
    k=next(k for k,g in enumerate(d['B'])if g==recovery);bad=copy.deepcopy(d);bad['B'].pop(k);assert exact.rawmap(bad)!=exact.rawmap(c);controls.append('signed recovery omitted')
    return c,d,controls
def bit_build():
    c=exact.read(PARENT/'data/retimed.json.gz');selection=exact.read(ROOT/'data/reuse-selection.json');controls=[]
    bad=copy.deepcopy(selection[0]);bad['new']=bad['old']
    try:bit_reuse.reconstruct(c,bad)
    except(AssertionError,IndexError):controls.append('overlapping reuse rejected')
    else:raise AssertionError('invalid overlap accepted')
    bad=copy.deepcopy(selection[0]);bad['reset_sources']=[0]
    try:bit_reuse.reconstruct(c,bad)
    except(AssertionError,IndexError):controls.append('wrong reset rejected')
    else:raise AssertionError('wrong reset accepted')
    for e in selection:c=bit_reuse.reconstruct(c,e)
    R=bit_reuse.retime;nodes,masks=R.nodes_of(c);bygate={(n['phase'],n['index']):i for i,n in enumerate(nodes)if not n.get('pin')}
    previous,following,frame=R.links(nodes,c,masks)
    for block in exact.read(ROOT/'data/retime-selection.json'):
        assert block['method']=='extremes'
        for move in block['changes']:
            i=bygate[move['phase'],move['index']];assert nodes[i]['mask']==int(move['old'])
            low,high,edges=R.interval({i},nodes,previous,following,frame);m=int(move['new']);assert bit_reuse.F.inside(low,m)and bit_reuse.F.inside(m,high);nodes[i]['mask']=m
    c=R.write_nodes(c,nodes);bit_reuse.audit(c);return c,controls
def emit(out):
    out=pathlib.Path(out);out.mkdir(exist_ok=False);base,c,cc=complex_build();b,bc=bit_build()
    for name,z in [('kernel-base',base),('complex-candidate',c),('bit-candidate',b)]:
        raw=json.dumps(z,sort_keys=True,separators=(',',':')).encode();blob=transport.deterministic_gzip(raw);expected=(ROOT/'data'/(name+'.json.gz')).read_bytes();assert blob==expected,'changed fixed witness '+name;(out/(name+'.json.gz')).write_bytes(blob)
    report={'status':'PASS_FIXED_WITNESSES_AND_CONTROLS','complex_R':c['R'],'bit_R':b['R'],'all_complex_raw_columns':240+c['R'],'bit_reuses':27,'additional_bit_frame_moves':26,'negative_controls':cc+bc};(out/'RECONSTRUCTION.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':print(emit(sys.argv[1]))
