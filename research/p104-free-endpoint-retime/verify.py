"""Reproduce the conditional kappa of the free helper-endpoint retime of PR5551's word.  Apache-2.0.

Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.
For each shipped word: (1) retime.py proves it is a legal retime of PR5551's pinned word
(same scalar program, only stops deleted and frame labels changed, all 208 main endpoints
unchanged); (2) the UNMODIFIED PR5545 local.py replay, transposed columns and native maps accept
it; (3) the physical caller and PR5551's own pricing (only census/claim literals changed) run
both moment engines and all 54 strict + 4 functional outer checks; (4) the exact crossing interval.
Use --part headline (about 6 min) or --part starts-only (about 6 min); default runs both.
"""
from fractions import Fraction
import json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from common import closure,need,load,read
import retime

BASE_LINE="KAPPA, TESTED = Q('.00304153'), Q('.0030415305')"
PAID_LINE='sum(targets.values()) == 12814 and sum(paid.values()) == 69912'
SURPLUS_LINE='== 760, '
PARTS={
 'headline':{'word':'WORD.json.gz','pricing':'pricing.py','kappa':"Q('.00308142'), Q('.0030814205')",'decimal':'.00308142',
             'paid':66852,'surplus':760,'helper_finals_changed':23,
             'interval':['15407121669/5000000000000','308142433381/100000000000000']},
 'starts-only':{'word':'WORD-STARTS-ONLY.json.gz','pricing':'pricing-starts-only.py','kappa':"Q('.003076879'), Q('.0030768795')",'decimal':'.003076879',
             'paid':67374,'surplus':760,'helper_finals_changed':0,
             'interval':['76922002003/25000000000000','307688008013/100000000000000']},
}

def patch(text,spec):
    for a,b in((BASE_LINE,'KAPPA, TESTED = '+spec['kappa']),
               ("'kappa_decimal':'.00304153'","'kappa_decimal':'%s'"%spec['decimal']),
               (PAID_LINE,'sum(targets.values()) == 12814 and sum(paid.values()) == %d'%spec['paid']),
               (SURPLUS_LINE,'== %d, '%spec['surplus'])):
        need(text.count(a)==1,'pinned pricing literal present once: '+a)
        text=text.replace(a,b)
    return text

def chain(root,L,pricing_text,word,tag):
    sys.modules['local']=L;L.ROOT=root
    C=L.load(root/'research/p104-productive-controller/caller.py','p104_free_retime_caller_'+tag)
    tmp=HERE/('.pricing-'+tag+'.py');tmp.write_text(pricing_text)
    try: P=L.load(tmp,'p104_free_retime_pricing_'+tag)
    finally: tmp.unlink()
    loc=L.replay(word);print(tag,'PASS replay: paid',loc['paid'],'public',loc['public_inputs'],'helpers',loc['helpers'],flush=True)
    L.reverse_columns(word);print(tag,'PASS transposed columns',flush=True)
    nat=L.native(word);print(tag,'PASS native maps',nat['distinct_maps'],'helpers',nat['helpers'],flush=True)
    ctl=C.construct();need(ctl==read(root/'research/p104-productive-controller/CONTROLLER.json'),'Exact complete caller')
    phys=C.physical(ctl,word);print(tag,'PASS physical caller',flush=True)
    return loc,P.run(loc,nat,ctl,phys)

def main():
    part=sys.argv[sys.argv.index('--part')+1] if '--part' in sys.argv else 'all'
    need(part in('all',)+tuple(PARTS),'--part must be headline or starts-only')
    pinned=read(HERE/'inputs/pr5551-WORD.json.gz')
    pr_pricing=(HERE/'inputs/pr5551-pricing.py').read_text()
    out={}
    with closure() as root:
        orig_local=(root/'research/p104-productive-controller/local.py').read_text()
        for name,spec in PARTS.items():
            if part not in('all',name): continue
            word=read(HERE/spec['word'])
            rep=retime.check(pinned,word);print(name,'PASS legal retime of PR5551 word:',rep,flush=True)
            need(rep['helper_final_spans_changed']==spec['helper_finals_changed'],'helper-final inventory')
            need((HERE/spec['pricing']).read_text()==patch(pr_pricing,spec),'shipped %s = PR5551 pricing.py + literal changes only'%spec['pricing'])
            L=load(root/'research/p104-productive-controller/local.py','local');L.ROOT=root
            need(Path(L.__file__).read_text()==orig_local,'UNMODIFIED PR5545 local.py (735 public inputs, no census literal)')
            loc,res=chain(root,L,(HERE/spec['pricing']).read_text(),word,name)
            print(name,'raw crossing interval',res['raw_root_interval'],flush=True)
            need(res['raw_root_interval']==spec['interval'],'exact crossing interval')
            need(res['productive_fields']==12814 and res['paid_calls']==spec['paid'] and res['rank_mass_surplus']==spec['surplus'],'invoice')
            need(len(res['outer']['strict_checks'])==54 and len(res['outer']['functional_checks'])==4,'outer inventory')
            need(all(Fraction(x)>0 for k in('strict_checks','functional_checks') for x in res['outer'][k].values()),'all outer checks strict')
            lo,hi=[Fraction(x) for x in spec['interval']]
            print(name,'crossing kappa in (%.14f, %.14f); 54 strict + 4 functional outer checks pass'%(lo,hi),flush=True)
            out[name]=res
    if '--write' in sys.argv and part=='all':
        (HERE/'RESULT.json').write_text(json.dumps({'status':'PASS_P104_FREE_ENDPOINT_RETIME_CONDITIONAL_KAPPA','headline':out['headline'],
            'starts_only':out['starts-only']},indent=1,sort_keys=True,default=str)+'\n')
    print('PASS P104_FREE_ENDPOINT_RETIME',part)
main()
