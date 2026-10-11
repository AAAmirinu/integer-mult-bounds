"""Portable source-bound seven-stage finite invoice with the actual prefix.
Retains source527/PR370/PR373/PR376 finite charges; corrects the legacy
five-stage payload and pays the signed defining-source supplement explicitly.
Prepared with OpenAI Codex assistance. Apache-2.0. All-size compiler, row,
prime/recovery and analytic interfaces remain inherited obligations.

Every input location is explicit; no previous working-directory state is read.
"""
import argparse,json,hashlib,gzip,struct,importlib.util
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
assert __debug__
read=lambda p:json.loads(Path(p).read_text())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run(parent,word_path,base_word,price_path,lowering_path,raw_records,signed_records,signed_result,parent_finite):
 parent,word_path,base_word,price_path,lowering_path,raw_records,signed_records,signed_result,parent_finite=map(Path,(parent,word_path,base_word,price_path,lowering_path,raw_records,signed_records,signed_result,parent_finite))
 price,lower,signed,old=map(read,(price_path,lowering_path,signed_result,parent_finite))
 w=json.load(gzip.open(word_path,'rt'));base=json.load(gzip.open(base_word,'rt'))
 # These are precisely the source data determining the unchanged E8 route
 # charts and endpoint/retained-total interface; no absent-key shortcut.
 route_fields=['h','v','R','coords','lines','form','ret','start','final']
 assert all(w[k]==base[k] for k in route_fields)
 assert lower['status']=='PASS_EXPLICIT_SEVEN_STAGE_LOWERING_CHART_LINKS_F2_ENDPOINT_BANKS_AND_FULL_PREFIX'
 assert signed['status']=='PASS_EXACT_SIGNED_DEFINING_DECODER_AND_LITERAL_PARITY_PROJECTION'
 assert sha(raw_records)==lower['source']['249-records.bin']==signed['exported_F2_record_sha256']
 assert sha(word_path)==signed['source_pr376_candidate_sha256']
 assert sha(signed_records)==signed['signed_record_sha256']
 assert sha(price_path)==lower['price_sha256']
 assert signed['literal_parity_record_equality'] and signed['arbitrary_helper_dirt_restored_exactly'] and signed['forward_then_signed_inverse_identity']
 assert signed['forward_and_reflected_ledgers'][0]==signed['forward_and_reflected_ledgers'][1]
 rawbytes=raw_records.read_bytes();signedbytes=signed_records.read_bytes();assert len(rawbytes)%24==len(signedbytes)%24==0
 ev=list(struct.iter_unpack('<6i',rawbytes));signed_ev=list(struct.iter_unpack('<6i',signedbytes))
 raw_weighted=sum(op==1 for op,*_ in ev);raw_unit=sum(abs(c) for op,x,y,c,f,z in ev if op==1)
 weighted=sum(op==1 for op,*_ in signed_ev);unit=sum(abs(c) for op,x,y,c,f,z in signed_ev if op==1)
 assert weighted>=raw_weighted and unit>=raw_unit
 h,v,R=w['h'],w['v'],w['R'];m,T,stock=price['m'],price['T'],price['W'];KP=price['K'];stages=2*KP+1;ncopy=len(w['ret'])
 assert (h,m,v,R,T,stock,KP,stages,ncopy)==(8,56,120,822,7,10794,3,7,9)
 literal=Counter({int(k):n for k,n in price['normalized_histogram'].items()});E=sum(literal.values());mass=sum(k*n for k,n in literal.items())
 assert literal==Counter({int(k):n for k,n in lower['paid_histogram'].items()})
 assert (lower['width'],lower['literal_stock'],lower['replicas'],lower['paid_calls'],lower['rank_mass'],lower['deficit'])==(m,stock,T,E,mass,1512)
 assert m*stock-mass==T*(2*KP*v-stages*ncopy*h)==1512 and max(literal)*2<m
 J=T*(2*stages*(2*v+R)+2*KP*v)
 # The source word has no additional frame gauge, so maxops=0, as in
 # receipts_k.py. Paid local chart compilations are charged by E*128*N^3.
 K=2*stages*T*((stock-1)+R*m*((m-1)+m))
 N=2*m;d=m*m;good=8*m*m+8;high=16*(d+1)**2
 weighted_total=T*(stages*weighted+6*(KP-1)*v);unit_total=T*(stages*unit+6*(KP-1)*v)
 coefficient=unit_total+J*high+J*(stock+ncopy)+E*good+E*(128*N**3)+16*m**3+stages*ncopy*T+E+K+1
 assert coefficient<2**80 and K<2**40 and stock+ncopy<2**80 and 2*m**3*10**16<2**80
 payload=lower['full_seven_stage_cancellation_free_prefix'];assert payload<2**104 and lower['legacy_five_stage_payload_guard_used'] is False and lower['payload_bits']==payload.bit_length()
 spec=importlib.util.spec_from_file_location('portable_moment',parent/'code/pricing/moment.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 c=Q(price['bit_coarse']);lo,hi=mod.moment(dict(literal),m,stock,c,True);delta_tau=1-hi;delta1=1-Q(mass,m*stock)-Q(1,10**16)*32*m*E/stock;assert min(delta_tau,delta1)>0
 ceilq=lambda q:-((-q.numerator)//q.denominator)
 chain=[Q(384599,10**10)];gaps=[]
 for stage in range(8):
  olda=chain[-1];aa=(1-c)*c+c*olda;dd=min(c-aa,1-aa-c,1-aa-c*(1-olda),1-c);assert olda<aa<c<1-aa and dd>0
  cutoff=max(1,ceilq(36/dd**2),ceilq(2*(4+(coefficient-1).bit_length())/dd));assert cutoff*dd**2>=36 and cutoff*dd>=2*(4+(coefficient-1).bit_length())
  gaps.append(dict(stage=stage+1,minimum_gap=str(dd),cutoff_log2_at_charged_coefficient=str(cutoff),charged_coefficient=coefficient));chain.append(aa)
 # Regenerate the entire inherited rational route receipt from this word.
 # The archived parent finite record is a pinned comparison, never a substitute
 # for running the exact route compiler here.
 import sys
 checkers=parent/'code/bit/checkers';sys.path.insert(0,str(checkers))
 spec=importlib.util.spec_from_file_location('fresh_route_finite',checkers/'finite_k.py');fk=importlib.util.module_from_spec(spec);spec.loader.exec_module(fk)
 L=w['lines'];q=L[0];form=lambda i,j:Q(int(i==j),2)
 route=fk.route_template(h,q,form);ip=lambda a,b:Q(sum(u*v for u,v in zip(a,b)),2)
 refl=lambda r:[[Q(int(i==j))-Q(r[i]*r[j],2)*2/ip(r,r) for j in range(h)] for i in range(h)]
 identity=[[Q(int(i==j)) for j in range(h)] for i in range(h)]
 isom={0:identity};frontier=[0]
 while frontier:
  nxt=[]
  for aa in frontier:
   for bb in range(len(L)):
    if bb in isom or abs(ip(L[aa],L[bb]))!=1:continue
    delta=[u-v for u,v in zip(L[aa],L[bb])] if ip(L[aa],L[bb])==1 else [u+v for u,v in zip(L[aa],L[bb])]
    isom[bb]=fk.mm(refl(delta),isom[aa]);nxt.append(bb)
  frontier=nxt
 assert len(isom)==len(L)==120
 denominators=set();maxf=0
 for port,g in isom.items():
  inv=list(map(list,zip(*g)));assert fk.mm(g,inv)==identity
  image=[sum(g[i][j]*q[j] for j in range(h)) for i in range(h)]
  assert image==L[port] or image==[-u for u in L[port]]
  rr=fk.route_template(h,q,form,g,inv);denominators.update(rr['denominators']);maxf=max(maxf,rr['factors'])
 assert all(d&(d-1)==0 for d in denominators)
 route['all_ports']=dict(ports=len(isom),max_factors=maxf,denominators=sorted(denominators))
 assert route==old['route'],'fresh rational route reconstruction disagrees'
 assert old['strict_upper']=='q^3137' and old['row_reserve']==dict(internal_coefficient=3137,external_complex_coefficient=20161)
 assert old['route']['all_ports']['ports']==v and old['route']['exact_inverse_reconstruction'] and old['route']['missing_addition_rejected']
 return dict(status='PASS_FRESH_SEVEN_STAGE_FINITE_INVOICE_WITH_EXACT_PREFIX_AND_SIGNED_OVERCHARGE',coefficient=coefficient,coefficient_bits=coefficient.bit_length(),low_matrix_power=d,strict_upper='q^'+str(d+1),positive_rank_children=E,rank_mass=mass,weighted_additions=weighted_total,unit_expanded_additions=unit_total,raw_local_weighted=raw_weighted,raw_local_unit=raw_unit,signed_local_weighted_overcharge=weighted,signed_local_unit_overcharge=unit,route_families=J,copy_erase_episodes=stages*ncopy*T,selector_charge=K,payload_prefix_upper=payload,payload_prefix_bits=payload.bit_length(),payload_method='Full actual seven-stage IR including all bridges and exchanges',delta_tau_lower=str(delta_tau),delta_linear=str(delta1),bootstrap_chain=list(map(str,chain)),gaps=gaps,row_reserve=dict(internal_coefficient=d+1,external_complex_coefficient=20161),route=old['route'],route_binding='All route-defining fields are byte-equivalent to the fresh full PR376 base word; exact route programs depend only on these unchanged fields.',route_binding_fields=route_fields,source_hashes=dict(word=sha(word_path),base_word=sha(base_word),raw_records=sha(raw_records),signed_records=sha(signed_records),signed_result=sha(signed_result),lowering=sha(lowering_path),price=sha(price_path),fresh_parent_finite=sha(parent_finite)),scope='Finite overcharges for the exact candidate bit program. The signed source supplement is conservatively paid even though only its parity program is emitted. All-size compiler and analytic assumptions retained.')

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 for name in ['parent','word','base-word','priced','lowering','raw-records','signed-records','signed-result','parent-finite','output']:ap.add_argument('--'+name,type=Path,required=True)
 a=ap.parse_args();r=run(a.parent,a.word,a.base_word,a.priced,a.lowering,a.raw_records,a.signed_records,a.signed_result,a.parent_finite);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'],r['coefficient'],r['payload_prefix_bits'])
