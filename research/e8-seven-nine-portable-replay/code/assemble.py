"""Exact low-read PR376 bit / PR377 complex composition.
Prepared with OpenAI Codex assistance. Apache-2.0. Retains PR376 assembly,
PR373/PR363 bootstrap lineage, PR377's conditional complex bridge, and the
shared PR315 outer engine. This script is a composition gate, not a Lean proof.
Usage: assemble.py --parent PARENT_BIT --priced PRICED --finite FINITE --complex-proof COMPLEX_PROOF --output OUTPUT
"""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha256
import argparse,importlib.util,json,sys
assert __debug__
sys.dont_write_bytecode=True

def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def encode(x):
 if isinstance(x,Q):return str(x)
 if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return list(map(encode,x))
 return x

def read(p):return json.loads(Path(p).read_text())
def digest(p):return sha256(Path(p).read_bytes()).hexdigest()

def run(parent,priced_path,finite_path,complex_proof):
 parent,priced_path,finite_path,complex_proof=map(Path,(parent,priced_path,finite_path,complex_proof))
 priced,finite=read(priced_path),read(finite_path)
 assert finite['status']=='PASS_FRESH_SEVEN_STAGE_FINITE_INVOICE_WITH_EXACT_PREFIX_AND_SIGNED_OVERCHARGE'
 assert finite['source_hashes']['price']==digest(priced_path)
 assert finite['payload_method']=='Full actual seven-stage IR including all bridges and exchanges'
 assert finite['signed_local_unit_overcharge']-finite['raw_local_unit']==264
 verify=read(complex_proof/'VERIFICATION.json')
 assert verify['status']=='PASS_PORTABLE_NINE_STAGE_COMPLEX_FINITE_COMPONENT'
 assert len(verify['fresh_stages'])==8 and all(z['returncode']==0 for z in verify['fresh_stages'])
 cp=complex_proof/'work/complex-nine-native';cx=read(cp/'INDEPENDENT-TEMPLATE-AUDIT.json');guard=read(cp/'GLOBAL-REVIEW.json')
 assert cx['status']=='PASS_INDEPENDENT_EMITTED_TEMPLATE_AUDIT_AND_TWO_MOMENTS'
 assert guard['status']=='PASS_NINE_STAGE_SOURCE_BOUND_TEMPLATE_OWNERS_PROFILE_AND_FINITE_INVOICE'
 assert cx['template_sha256']==guard['template_sha256']
 b=Q(cx['coarse_complex']);assert str(b)==verify['complex_coarse']==priced['complex_coarse']
 assert b==Q(999240641319551,10**18)
 complex_contract=dict(source_manifest_sha256=verify['source_manifest_sha256'],status=verify['status'],fresh_stages=[dict(stage=z['stage'],returncode=z['returncode']) for z in verify['fresh_stages']],complex_coarse=verify['complex_coarse'],template_audit=cx,global_review={k:v for k,v in guard.items() if k not in ('seconds','source_hashes')})
 complex_contract_sha256=sha256(json.dumps(complex_contract,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 invo=guard['finite_invoice']
 assert (guard['m'],guard['live'],guard['physical'],guard['invocations'])==(73,14727,15520,72)
 assert (invo['G_exponent'],invo['E_exponent'],invo['C0_exponent'])==(30000,100000,210000)
 assert (invo['halving_degree'],invo['halving_integer_inequality'],invo['induction_gap_multiple_B'])==(2,[5329,4608],49)
 assert invo['physical_row_coefficient']==15445<invo['retained_row_coefficient']==20161
 assert invo['logical_groups_bits']<6050 and invo['router_bits']<30000 and invo['literal_bits']<100000 and invo['required_C0_bits']<210000
 pricing=parent/'code/pricing';moment=load('composition_moment',pricing/'moment.py');other=load('composition_base_two',pricing/'base_two_moment.py');outer=load('composition_outer',pricing/'outer.py');fk=load('composition_finite',parent/'code/bit/checkers/finite_k.py')
 # Both suppliers use exactly the same outer contract, not merely equal names.
 cx_outer=complex_proof/'work/pr361/code/engines/outer.py'
 assert digest(pricing/'outer.py')==digest(cx_outer)
 H={int(k):v for k,v in priced['normalized_histogram'].items()};m,W=priced['m'],priced['W'];c=Q(priced['bit_coarse'])
 assert (priced['K'],priced['stages'],priced['h'],priced['T'],m,W)==(3,7,8,7,56,10794)
 assert c==Q(198986994618331,2*10**17)
 assert max(H)*2<m and sum(H.values())==finite['positive_rank_children'] and sum(r*n for r,n in H.items())==finite['rank_mass']
 assert m*W-sum(r*n for r,n in H.items())==7*216
 assert finite['low_matrix_power']==3136 and finite['strict_upper']=='q^3137'
 assert finite['row_reserve']==dict(internal_coefficient=3137,external_complex_coefficient=20161)
 assert finite['payload_prefix_upper']<2**104 and finite['payload_prefix_bits']==finite['payload_prefix_upper'].bit_length()
 coefficient=finite['coefficient'];assert 1<=coefficient<2**80
 grid=10**27;eta,beta=Q(1,10**24),Q(1,10**9);cap=(1-beta)*b;selected=c
 assert 0<selected<cap
 interval=moment.moment(H,m,W,selected,True);assert interval[1]<1
 _,upper=other.moment(m,W,list(H.items()),selected);fallback=32*m*m*sum(H.values());_,bad=other.moment(m,W,[(1,fallback)],selected);assert upper+Q(1,10**16)*bad<1
 assert Q(finite['delta_tau_lower'])==1-interval[1]
 chain=[Q(384599,10**10)];cutoffs=[]
 for j in range(8):
  old=chain[-1];new=(1-selected)*selected+selected*old;assert old<new<selected<1-new
  gaps=dict(atom=selected-new,borrowing=1-new-selected,remainder=1-new-selected*(1-old),stock=1-selected);delta=min(gaps.values());assert delta>0
  cutoff=fk.cutoff_log2(delta,coefficient)
  # Independent reconstruction of the inherited cutoff rule.
  ceilq=lambda x:-((-x.numerator)//x.denominator)
  expected=max(1,ceilq(36/delta**2),ceilq(2*(4+(coefficient-1).bit_length())/delta));assert cutoff==expected
  assert Q(cutoff)*delta**2>=36 and Q(cutoff)*delta>=2*(4+(coefficient-1).bit_length())
  cutoffs.append(dict(stage=j+1,gaps=gaps,minimum_gap=delta,cutoff_log2=cutoff,charged_coefficient=coefficient));chain.append(new)
 assert list(map(str,chain))==finite['bootstrap_chain']
 assert len(finite['gaps'])==len(cutoffs)==8
 for mine,source in zip(cutoffs,finite['gaps']):
  assert mine['stage']==source['stage'] and str(mine['minimum_gap'])==source['minimum_gap']
  assert mine['cutoff_log2']==int(source['cutoff_log2_at_charged_coefficient'])
  assert mine['charged_coefficient']==source['charged_coefficient']==coefficient
 bridge=dict(proof='PR377 PROOF.txt plus source-bound bit finite receipt',representation='Exact powers with source-bound finite overcharges',semantic=dict(G=dict(base=2,exponent=30000),E=dict(base=2,exponent=100000),B_upper=dict(base=2,exponent=100001),C0=dict(base=2,exponent=210000),C1=1,strict_literal_gap=1,induction_gap_lower=1),rows=dict(coefficient=20161,degree=10**6,suffix_slope=4*10**6,degree_gap=Q(10**6)-Q(51*20161,25)))
 bit=chain[-1];q=bit*(1-2*eta);minimum=(1-eta)*q/(1+q);ticks=minimum*grid;kappa=Q((ticks.numerator-1)//ticks.denominator,grid)
 a=outer.assembly(bit,b,bridge,kappa,eta=eta,beta=beta);assert len(a['strict_constraints'])==47 and min(a['strict_constraints'].values())>0
 try:outer.assembly(bit,b,bridge,kappa+Q(1,grid),eta=eta,beta=beta)
 except AssertionError as err:adjacent_error=str(err)
 else:raise AssertionError('adjacent grid accepted')
 try:outer.assembly(cap,b,bridge,kappa,eta=eta,beta=beta)
 except AssertionError as err:assert 'leaf_saving_above_bit' in str(err)
 else:raise AssertionError('complex leaf cap accepted')
 return encode(dict(status='PASS_EXACT_FINAL_B_ORDER376_PR377_COMPOSITION',bit_coarse=c,complex_coarse=b,selected_saving=selected,binding='bit',eta=eta,beta=beta,grid_denominator=grid,bootstrap_steps=8,selected_moment_interval=interval,independent_moment_upper=upper+Q(1,10**16)*bad,chain=chain,finite_cutoffs=cutoffs,assembly=a,kappa=kappa,kappa_float=float(kappa),adjacent_grid_rejected=True,adjacent_grid_error=adjacent_error,complex_leaf_cap_rejected=True,finite_coefficient=coefficient,source_binding=dict(priced_sha256=digest(priced_path),finite_sha256=digest(finite_path),complex_contract_sha256=complex_contract_sha256,complex_source_manifest_sha256=verify['source_manifest_sha256'],complex_moment_sha256=digest(cp/'INDEPENDENT-TEMPLATE-AUDIT.json'),shared_outer_sha256=digest(pricing/'outer.py')),common_interface=dict(bit_dimension=56,complex_dimension=73,dimensions_may_differ='Separate recursive suppliers communicate by certified savings and row/finite envelopes, not shared label banks.',bit_row_power='q^3137',external_complex_row_reserve=20161,complex_actual_row_coefficient=15445,complex_halving_degree=2,complex_halving_integer_gap=5329-4608,bit_half_shrink_gap=56-2*max(H),shared_guard_exponents=[30000,100000,210000],payload_prefix_bits=finite['payload_prefix_bits'],payload_limit_bits=104),retained_assumptions=['Bit source word, signed restoration, reflected ledgers, label charts, global bank/owner lift and full emitted prefix bound must be independently admitted.','Complex source retains local E8 theorem, exact Clifford compiler, common-grid precision/recovery and row/analytic interfaces; PR377 has no new Lean multiplication theorem.','The inherited bootstrap theorem is applied eight times; each finite cutoff is rebound to the fresh finite coefficient.','Balanced outer assembly and additive row interfaces 9909+252 and reserve20161 are inherited; the arithmetic check does not newly prove these analytic interfaces.']))

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 for name in ['parent','priced','finite','complex-proof','output']:ap.add_argument('--'+name,type=Path,required=True)
 args=ap.parse_args();result=run(args.parent,args.priced,args.finite,args.complex_proof);args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],result['kappa'],result['kappa_float'])
