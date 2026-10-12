"""Keep PR484's four selection controls; omit a proven-essential donor.
The historical last-donor assumption is inapplicable to PR518's donor ordering.
This changes the mutant, never the accepted selection or generated word.
"""
from pathlib import Path
import gzip,hashlib,json,sys
code,basefile,selfile,out=map(Path,sys.argv[1:]);sys.path.insert(0,str(code));import gk_word as G
base=json.load(gzip.open(basefile));sel=json.loads(selfile.read_text());c0=sel['kernel'][0];cols=G.responses(base)
omit=next(d for d in c0['donors']if G.solve_relation(cols,[x for x in c0['donors']if x!=d],c0['pivots'][0])is None)
text=(code/'controls_gk.py').read_text();old="q['kernel'][0].__setitem__('donors', q['kernel'][0]['donors'][:-1]) if len(c0['donors']) > 1 and GW.solve_relation(col, c0['donors'][:-1], c0['pivots'][0]) is None else (_ for _ in ()).throw(RuntimeError('control not applicable'))"
new="q['kernel'][0].__setitem__('donors', [d for d in q['kernel'][0]['donors'] if d != OMIT])"
assert text.count(old)==1;text=text.replace(old,new);ns={'__name__':'selection_controls_adapted','__file__':str(code/'controls_gk.py'),'OMIT':omit};exec(compile(text,str(code/'controls_gk.py'),'exec'),ns)
refused=ns['selection_controls'](base,sel);assert len(refused)==4
out.write_text(json.dumps(dict(status='PASS_SELECTION_MUTATION_CONTROLS',refused=refused,omitted_essential_donor=omit,pivot=c0['pivots'][0],source_sha256=hashlib.sha256((code/'controls_gk.py').read_bytes()).hexdigest(),scope='Original four controls, with historical last-donor mutation adapted to omit a proven-essential donor. Accepted selection and word unchanged.'),indent=2)+'\n')
print('PASS',len(refused),'controls',omit)
