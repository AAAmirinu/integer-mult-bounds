"""Check a local word and emit its complete instruction records."""
from pathlib import Path
import gzip, hashlib, json, sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import e8core as E
from export249 import export
from check_streams import check

word,out=map(Path,sys.argv[1:]);out.mkdir(parents=True,exist_ok=True)
raw=word.read_bytes();c=json.loads(gzip.decompress(raw) if word.suffix=='.gz' else raw)
replay=E.replay(c,span_mode='z');assert not replay['viol'],replay['viol'][:5]
streams=check(c)
assert streams['forward']['histogram']==dict(replay['H'])
state,frames,records=export(c,str(out/'records'))
(out/'cout').mkdir(exist_ok=True)
legality=dict(status='PASS_PYTHON_EXACT_LOCAL_AND_REFLECTED_REPLAY',copies=len(c['ret']),erasures=len(c['ret']),
              common_frame_ADDs=streams['forward']['adds'],integer_union_violations=0)
columns=dict(status='PASS_PYTHON_ALL_FORMAL_COLUMNS',formal_columns_checked=replay['n'],
             local_scalar_additions=streams['forward']['adds'],local_raw_H=sorted(replay['H'].items()))
for name,value in [('legality',legality),('columns',columns)]:
 (out/'cout'/f'{name}.json').write_text(json.dumps(value,indent=2)+'\n')
roots=c['lines'];isos=[]
axes={i:next(j for j,x in enumerate(roots) if x==[2*int(k==i) for k in range(8)]) for i in range(8)}
for f in sorted(set(state['initial'][str(h)] for h in range(240,state['n']))):
 B=frames[str(f)]['B'];dim=frames[str(f)]['dim']
 active=[i for i in range(8) if any(row[i] for row in B)]
 assert len(active)==dim,('entrance must be a coordinate subspace',f,B)
 order=active+[i for i in range(8) if i not in active]
 current=order[:];ops=[]
 for i in range(8):
  j=current.index(i)
  if j!=i:current[i],current[j]=current[j],current[i];ops.append(['swap',i,j,None])
 basis=[axes[i] for i in order]
 isos.append(dict(frame=f,entrance_rank=dim,denominator=2,entrance_basis=basis[:dim],residual_basis=basis[dim:],
                  orthogonal_rows_numerator=[roots[i] for i in basis],gaussian_reduction=ops))
from bank_routes import validate_isometries
assert validate_isometries(isos,c['frames'],roots,{int(f):v['dim'] for f,v in frames.items()})=={x['frame'] for x in isos}
(out/'isometries.json').write_text(json.dumps(isos,indent=2)+'\n')
receipt=dict(status='PASS_LOCAL_REPLAY_AND_RECORD_EXPORT',word_sha256=hashlib.sha256(raw).hexdigest(),
             columns=replay['n'],records=len(records),frames=len(frames),residual_isometries=len(isos),
             local_profile=dict(sorted(replay['H'].items())),streams=streams,
             scope='Two Python local replays and exact record export. Independent global audit is separate.')
(out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
