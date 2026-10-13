"""Run the pinned K-triangle constructor (research/complex-571-cold14-k492/code/construct_k_triangle.py, unchanged on disk) with a
role dump appended, so that every helper register's role (module register, face packet, 8-sum, slot copy, own row, pair, request)
is written to OUT/ROLES.json next to the constructor's own outputs. The pinned file is read, patched in memory and executed.
Usage: instrument_constructor.py --constructor PATH --inputs DIR --tri SCHEDULE.json|empty --out DIR"""
import argparse,json,runpy,sys,tempfile
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument('--constructor',required=True);a.add_argument('--inputs',required=True);a.add_argument('--tri',required=True);a.add_argument('--out',required=True);A=a.parse_args()
src=Path(A.constructor).read_text();marker="(OUT/'FULL-WORD.json.gz')";assert src.count(marker)==1
dump='''
_k=str
roles={'blocks':{_k(c):dict(sources=z['receipt']['source_lines'],module=[maps[c][i] for i in range(8,24)],tetrads=tetrads[c],totals={str(i):block_totals[c,i] for i in c}) for c,z in blocks.items()},
 'own_rows':{str(t):[r,str(coef),list(F)] for t,(r,coef,F) in own_rows.items()},
 'pairs':[dict(targets=list(p['targets']),keys=[[list(k[0]),list(k[1]),k[2]] for k in p['keys']],selected=p['selected'],matrix=[[int(x) for x in row] for row in p['matrix']]) for p in pairs],
 'packets':{_k(k):[r,str(a)] for k,(r,a) in packets.items()},'Ms':{_k(k):[r,str(a)] for k,(r,a) in Ms.items()},'slots':{_k(k):[r,str(a)] for k,(r,a) in slots.items()},
 'requests':{_k(k):[[t,str(c)] for t,c in v] for k,v in requests.items()},'centers':centers,'output_basis':[[t,u,str(z)] for t,u,z in output_basis],
 'regmap':{str(k):v for k,v in mp.items()},'NH':NH,'rows':{str(r):{str(s):str(x) for s,x in rows[r].items()} for r in range(len(cur))},'ports':P,'G':G,'frame_sources':{str(i):s for i,s in frame.items()}}
(OUT/'ROLES.json').write_text(json.dumps(roles))
'''
patched=src.replace(marker,dump+marker,1)
tri=A.tri
if tri=='empty':
    t=tempfile.NamedTemporaryFile('w',suffix='.json',delete=False);json.dump({'full_pairs':[],'triangles':[]},t);t.close();tri=t.name
with tempfile.NamedTemporaryFile('w',suffix='.py',delete=False) as f:f.write(patched);path=f.name
sys.argv=[path,A.inputs,A.out,tri];runpy.run_path(path,run_name='__main__')
