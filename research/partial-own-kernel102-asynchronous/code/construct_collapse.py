"""Fresh source-bound blockwise pair factory and frozen102-pivot reconstruction.
Adapted from PR517/95 body binding and PR518 blockwise pair reconstruction.
No search or optimizer runs in verification. See SOURCE.json and NOTICE.md.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import copy,difflib,gzip,hashlib,json,subprocess,sys
source,oldbase,selection_path,candidate_path,spec_path,out=map(Path,sys.argv[1:]);assert not out.exists();out.mkdir(parents=True)
sys.path.insert(0,str(source/'code'));import gk_word as G
read=lambda p:json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=read(oldbase/'sc_base/FULL-WORD.json.gz');current=read(oldbase/'split-centres/FULL-WORD.json.gz');sel=read(selection_path);ret=copy.deepcopy(original)
prefix=len(current['A'])-len(original['A']);assert prefix==671
for part in ['A','B']:
 events=current[part][prefix:]if part=='A'else current[part]
 assert [e[:-1]for e in events]==[e[:-1]for e in original[part]],part
 ret[part]=copy.deepcopy(events)
ret['cleanup']=[G.inverse(e,G.FULL)for e in reversed(ret['A']+ret['B'])if not G.V<=e[1]<2*G.V]
assert G.build(ret,sel)==current,'Every baseline field must match the freshly verified dependency'
spec=read(spec_path);assert len(spec)==14
assert all(v==([1,1]if k in ['0,2,4,6','0,3,4,7']else[0,0])for k,v in spec.items())
factory_source=Path(__file__).resolve().parents[1]/'vendor/pr507/code/construct_partial.py'
s=factory_source.read_text();token='[(1,1)[parity]]';assert s.count(token)==1
s=s.replace(token,"[json.loads(Path(sys.argv[3]).read_text())[','.join(map(str,c))][parity]]")
patched=out/'pair_factory.py';patched.write_text(s)
with(out/'pair-factory.log').open('w')as log:subprocess.run([sys.executable,'-B',str(patched),str(oldbase/'work/complex-network/hamming'),str(out/'pair-factory'),str(spec_path)],stdout=log,stderr=subprocess.STDOUT,check=True)
base=read(out/'pair-factory/FULL-WORD.json.gz');assert base['report']['R']==original['report']['R']==560
transferred={}
for part in ['A','B']:
 aa=[tuple(e[:-1])for e in original[part]];bb=[tuple(e[:-1])for e in base[part]];count=0
 for ia,ib,n in difflib.SequenceMatcher(a=aa,b=bb,autojunk=False).get_matching_blocks():
  for j in range(n):
   assert original[part][ia+j][:-1]==base[part][ib+j][:-1]
   if original[part][ia+j][-1]!=ret[part][ia+j][-1]:base[part][ib+j][-1]=copy.deepcopy(ret[part][ia+j][-1]);count+=1
 transferred[part]=count
base['cleanup']=[G.inverse(e,G.FULL)for e in reversed(base['A']+base['B'])if not G.V<=e[1]<2*G.V]
changed=read(candidate_path);wanted=copy.deepcopy(sel['gauge'])
for h in ['540','541','542','543']:
 assert len(wanted[h])==4 and G.span([408,102])<=G.span(wanted[h]);wanted[h]=[408,102]
assert changed['gauge']==wanted and sum(len(c['pivots'])for c in changed['kernel'])==102
word=G.build(base,changed);after=G.profile(word)
assert after==Counter({1:2537,2:192,3:506,4:88,5:298,6:68,7:1,8:17})
assert Counter(G.widths_of(word))==Counter({9:378,8:164,7:18})
for key in ['ports','centers','center_frames','cut','precondition','root_lines','scatter']:assert word[key]==current[key],key
counts={}
for part in ['A','B','cut','cleanup','precondition']:
 counts[part]=len(word.get(part,[]))
 for e in word.get(part,[]):
  assert e[0]in ['add','scale']
  q=Fraction(e[3],e[4])if e[0]=='add'else Fraction(e[2],e[3]);assert q.denominator&(q.denominator-1)==0,(part,e)
  if e[0]=='scale':assert q.numerator and abs(q.numerator)&(abs(q.numerator)-1)==0,(part,e)
raw=G.dump(word);assert hashlib.sha256(raw).hexdigest()=='a56423fac9f06d864a42a32450a7dba22389330262551cd266066cb074202828'
receipt=dict(status='SOURCE_BOUND_STRUCTURE_AND_DYADIC_GATE',baseline_reconstruction_all_fields_equal=True,kernel_pivots=102,body_frame_transfer_prefix=prefix,pair_body_frames_transferred=transferred,local_profile=dict(sorted(after.items())),widths=dict(sorted(Counter(G.widths_of(word)).items())),dyadic_event_counts=counts,sources={str(p):sha(p)for p in [factory_source,selection_path,candidate_path,spec_path,oldbase/'sc_base/FULL-WORD.json.gz',oldbase/'split-centres/FULL-WORD.json.gz']},word_sha256=hashlib.sha256(raw).hexdigest(),scope='Whole new factory, exact baseline binding, selection relations, frames and dyadic primitives. Scalar/physical/global admission remains separate.')
(out/'RETIMED-BASE.json.gz').write_bytes(G.dump(base));(out/'FULL-WORD.json.gz').write_bytes(raw);(out/'SELECTION.json').write_text(json.dumps(changed,sort_keys=True,indent=2)+'\n');(out/'CONSTRUCTION.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps(receipt,indent=2))
