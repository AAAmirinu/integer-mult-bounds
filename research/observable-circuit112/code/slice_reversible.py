"""Exact reversible observable slicing. No optimizer, no external dependencies.
Usage: python -B slice_reversible.py INPUT_WORD.json.gz NEW_OUTPUT_DIRECTORY
Every background update must be invertible and read only background registers.
The receipt establishes scalar observed-map equality, not physical frame pricing.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,gzip,copy,hashlib,sys
if not __debug__:raise RuntimeError('Assertions must remain enabled')
src,out=map(Path,sys.argv[1:]);assert not out.exists()
raw=src.read_bytes();word=json.loads(gzip.decompress(raw));w=copy.deepcopy(word)
v=len(w['ports']);n=2*v+w['report']['R'];targets=set(range(v,2*v))
for name in ['A','cut','B']:
 for e in w[name]:
  assert e[0]in ['add','scale']
  if e[0]=='add':assert e[1]!=e[2], 'Elementary shear needs distinct registers'
  if e[0]=='scale':assert Q(e[2],e[3])!=0
  elif e[1]not in targets:assert e[2]not in targets,('background reads an observed register',name,e)
  if name=='cut':assert e[1]in targets
live=[({r-v:Q(1)}if r in targets else {})for r in range(n)];removed=[]
for name in ['B','cut','A']:
 kept=[]
 for i in reversed(range(len(w[name]))):
  e=w[name][i];t=e[1]
  if t not in targets and not live[t]:removed.append(dict(part=name,index=i,event=e));continue
  kept.append(e)
  if e[0]=='add':
   q=Q(e[3],e[4]);s=e[2]
   for j,a in live[t].items():
    z=live[s].get(j,Q(0))+q*a
    if z:live[s][j]=z
    else:live[s].pop(j,None)
  else:
   q=Q(e[2],e[3]);live[t]={j:q*a for j,a in live[t].items()}
 w[name]=list(reversed(kept))
assert w['cut']==word['cut']
def inverse(e):
 e=copy.deepcopy(e)
 if e[0]=='add':e[3]*=-1
 else:e[2],e[3]=e[3],e[2]
 return e
oldcleanup=[inverse(e)for e in reversed(word['A']+word['B'])if e[1]not in targets]
assert [e[:-1]for e in oldcleanup]==[e[:-1]for e in word['cleanup']]
full=word['cleanup'][0][-1]if word['cleanup']else list(range(9))
w['cleanup']=[]
for e in reversed(w['A']+w['B']):
 if e[1]not in targets:
  q=inverse(e);q[-1]=copy.deepcopy(full);w['cleanup'].append(q)
def execute(ops):
 rows=[{r:Q(1)}for r in range(n)]
 for e in ops:
  t=e[1]
  if e[0]=='scale':
   q=Q(e[2],e[3]);rows[t]={j:q*a for j,a in rows[t].items()}
  else:
   q=Q(e[3],e[4]);s=e[2]
   for j,a in list(rows[s].items()):
    z=rows[t].get(j,Q(0))+q*a
    if z:rows[t][j]=z
    else:rows[t].pop(j,None)
 return rows
old=execute(word['A']+word['cut']+word['B']+word['cleanup']);new=execute(w['A']+w['cut']+w['B']+w['cleanup'])
assert old==new
assert all(new[r]=={r:Q(1)}for r in range(n)if r not in targets)
for part in ['A','B','cut','cleanup','precondition']:
 for e in w.get(part,[]):
  q=Q(e[3],e[4])if e[0]=='add'else Q(e[2],e[3]);assert q.denominator&(q.denominator-1)==0
  if e[0]=='scale':assert abs(q.numerator)&(abs(q.numerator)-1)==0
out.mkdir();data=gzip.compress(json.dumps(w,sort_keys=True,separators=(',',':')).encode(),mtime=0);(out/'WORD.json.gz').write_bytes(data)
receipt=dict(status='PASS_EXACT_ALL_COLUMN_OBSERVATION_AND_BACKGROUND_RESTORATION',input_sha256=hashlib.sha256(raw).hexdigest(),output_sha256=hashlib.sha256(data).hexdigest(),columns=n,ports=v,helpers=w['report']['R'],removed_forward=len(removed),removed_cleanup=len(word['cleanup'])-len(w['cleanup']),removed=removed,scope='Exact scalar transformation including arbitrary dirt and background restoration. All original frame labels retained; paid profile and physical phases require separate verification.')
(out/'SLICE-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],n,receipt['removed_forward'],receipt['removed_cleanup'])
