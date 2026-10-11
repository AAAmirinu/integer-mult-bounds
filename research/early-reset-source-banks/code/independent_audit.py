"""Independent source/template/invoice arithmetic readback of frozen PR433.
Prepared with OpenAI Codex assistance, 2026-10-11. Does not import producers.
"""
import gzip, hashlib, json, math, struct, sys
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q

D=Path(sys.argv[1]); OUT=Path(sys.argv[2]); OUT.mkdir(parents=True,exist_ok=True)
read=lambda p:json.loads(p.read_text())
unzip=lambda p:json.loads(gzip.decompress(p.read_bytes()))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B=D/'bit426-source-centres'; C=D/'split-centres'
bt=unzip(B/'global/GLOBAL-TEMPLATE.json.gz'); bg=read(B/'global/GLOBAL.json'); geo=read(B/'global/GEOMETRY.json')
ct=unzip(C/'GLOBAL-TEMPLATE.json.gz'); cg=read(C/'INTEGRATION.json'); cw=unzip(C/'CANONICAL-WORD.json.gz')
result=read(D/'RESULT.json')

# Reconstruct both local bit scalar programs from actual binary records, with
# original dirty columns represented individually. Track every copy's lifetime.
records=list(struct.iter_unpack('<6i',(B/'records/249-records.bin').read_bytes()))
frame=read(B/'records/frames.json')['frames']; dim={int(k):v['dim'] for k,v in frame.items()}
state=read(B/'records/249-states.json'); n=state['n']; R=n-240; WBIT=7680+9*R; assert 0<R<=758
local_profiles=[]; bit_prefix=[]; bit_adds=[]; copy_counts=[]
for rev in (False,True):
 cur=[state['final' if rev else 'initial'][str(i)] for i in range(n)]+[-1]
 values=[1<<i for i in range(n)]+[0]; norms=[1]*n+[0]
 hist=Counter(); maximum=1; copies=adds=0; parent=None
 for op,x,y,c,f,z in (reversed(records) if rev else records):
  if op==0:
   assert cur[x]==(c if rev else y)
   assert f==dim[c]-dim[y]>=0
   cur[x]=y if rev else c
   if f:hist[f]+=1
  elif op==1:
   assert cur[x]==cur[y]==f and x!=y and x!=parent
   if c%2:values[x]^=values[y]
   norms[x]+=abs(c)*norms[y];maximum=max(maximum,norms[x]);adds+=1
  elif op==(3 if rev else 2):
   assert parent is None and y==n and values[n]==0 and cur[x]==c
   parent=x;values[n]=values[x];norms[n]=norms[x];cur[n]=f
   hist[abs(dim[c]-dim[f])]+=1;copies+=1
  else:
   assert op==(2 if rev else 3) and parent==x and values[n]==values[x] and cur[x]==c and cur[n]==f
   values[n]=norms[n]=0;cur[n]=-1;parent=None
 assert parent is None and values[n]==0 and copies==9
 assert cur[:n]==[state['initial' if rev else 'final'][str(i)] for i in range(n)]
 assert values[:n]==[(1<<i)^((1<<(i-120)) if 120<=i<240 else 0) for i in range(n)]
 local_profiles.append(hist);bit_prefix.append(maximum);bit_adds.append(adds);copy_counts.append(copies)
assert local_profiles[0]==local_profiles[1] and bit_adds[0]==bit_adds[1]
BH=Counter({r:72*z for r,z in local_profiles[0].items()})
BH.update({7:3*1920,14:2*1920,28:2*1920,42:2*1920})
assert BH==Counter({int(k):v for k,v in bg['profile'].items()})
assert sum(r*z for r,z in BH.items())==64*WBIT-2496
assert bt['bank_padding'] is None and bt['live']==WBIT
occupied=set();calls=set()
for call in bt['calls']:
 st,rep=call['stage'],call['replica']; pair=max(0,(st-1)//2);reverse=st in (1,3,5,7)
 assert call['pair']==pair and call['orientation']==('reverse' if reverse else 'forward')
 assert (st,rep) not in calls;calls.add((st,rep));assert len(call['owners'])==n
 for reg,(family,route) in enumerate(call['owners']):
  if reg<240:
   side=reg//120;side=1-side if reverse else side
   assert family==rep*960+(2*pair+side)*120+reg%120 and route==['data',st,reg%120]
  else:
   bank,slot=divmod(rep*R+reg-240,8)
   assert family==7680+st*R+bank and route==['bank',slot]
   assert (family,slot) not in occupied;occupied.add((family,slot))
assert calls=={(s,r) for s in range(9) for r in range(8)}
assert occupied=={(f,s) for f in range(7680,WBIT) for s in range(8)}

# Recount complex primitive operations directly; copied/private scalar words
# are admitted separately, here every emitted macro is billed from its value.
cp={};cc={};cm={}
for name,events in ct['local_programs'].items():
 hist=Counter();prims=macros=0
 for event in events:
  tag=event[0]
  if tag=='climb':hist[event[5]]+=1
  elif tag=='center':hist[event[4]]+=1
  elif tag=='scalar':
   e=event[1];macros+=1
   if e[0] in ('clear','copy'):prims+=2;continue
   q=Q(*e[3:5]) if e[0]=='add' else Q(*e[2:4]);a,b=abs(q.numerator),q.denominator
   assert b>0 and not b&(b-1)
   if e[0]=='scale':
    assert a>0 and not a&(a-1);prims+=2*(abs(a.bit_length()-b.bit_length())+(q<0))
   else:
    # clear, Horner additions/doubles, halvings, accumulation, clear.
    prims+=2*(3+a.bit_length()-1+sum(map(int,bin(a)[2:]))+b.bit_length()-1)
 cp[name]=hist;cc[name]=prims;cm[name]=macros
 assert prims==cg['local_program_checks'][name]['real_component_primitive_bound']
assert cp['forward']==cp['backward']
CH=Counter({r:72*z for r,z in cp['forward'].items()});CH.update({1:5040,8:3*1920,16:2*1920,32:2*1920,48:2*1920})
assert CH==Counter({int(k):v for k,v in cg['global_profile'].items()})
assert sum(r*z for r,z in CH.items())==73*12720-2496
assert ct['live']==12720 and ct['physical']==13298
assigned=set();calls=set()
for call in ct['calls']:
 st,rep=call['stage'],call['replica'];pair=max(0,(st-1)//2)
 assert call['pair']==pair and call['orientation']==('backward' if st in (1,3,5,7) else 'forward')
 assert (st,rep) not in calls;calls.add((st,rep));assert len(call['owners'])==800
 for reg,(family,route) in enumerate(call['owners']):
  if reg<240:assert family==rep*960+(2*pair+reg//120)*120+reg%120 and route==[1,st,reg%120]
  else:
   bank,slot=divmod(rep*560+reg-240,8)
   assert family==7680+st*560+bank and route==[2,slot]
   assert (family,slot) not in assigned;assigned.add((family,slot))
assert calls=={(s,r) for s in range(9) for r in range(8)}
assert assigned=={(f,s) for f in range(7680,12720) for s in range(8)}
assert ct['bank_padding']==dict(families=list(range(7680,12720)),axis=72,child_rank=1)
assert ct['private_namespace']==dict(centers=[12720,12736],reserved_tableau=[12736,13296],coefficient=[13296,13298])

# Both finite invoices are reconstructed from the emitted counts.
m=64;E=sum(BH.values());W=WBIT;physical=W+9
units=72*bit_adds[0]+18*120*8
J=8*72*n+8*7680+2*(72*R)+2*648
selectors=2*72*((W-1)+R*64*(geo['max_route_factors']+63+64))
prefix=(1<<18)*bit_prefix[0]**5*bit_prefix[1]**4
assert prefix==int(bg['global_prefix_bound'])
coefficient=units+J*16*(4096+1)**2+J*physical+E*(8*4096+8+128*128**3)+16*64**3+648+selectors+prefix+1
two=(coefficient+1)**2*(E+1)**2
charged_prefix=max(256,64*((prefix.bit_length()+63)//64)); charged_two=max(512,64*((two.bit_length()+63)//64))
assert prefix<1<<charged_prefix and two<1<<charged_two
bi=dict(unit_additions=units,route_items=J,selector_calls=selectors,coefficient=str(coefficient),two_level_coefficient=str(two),prefix_bits=prefix.bit_length(),charged_prefix_bits=charged_prefix,coefficient_bits=coefficient.bit_length(),two_level_coefficient_bits=two.bit_length(),charged_two_level_coefficient_bits=charged_two,row_coefficient=18355,live=W,physical=physical)
assert bi==result['bit_invoice']
m=73;physical=13298;compiler=64*74**3
adapters=16*(max(cm.values())+sum(cp['forward'].values())+800+16)+64*m
local=max(cc.values())+adapters*compiler
idle_count=sum(e['replicas'] for e in ct['idle_children'])
outside=8*(6*120*8*9+2*9*8*560+idle_count+5040+17280+3840+7680+12720+physical)+64*m
scalar=sum(cc[c['orientation']] for c in ct['calls'])
pervertex=scalar+17280+3840+7680+12720+(72*adapters+outside)*compiler+64*physical
group=2**1296*math.prod(2**(2*i)-1 for i in range(1,37));stock=group*physical
mass=group*sum(r*z for r,z in CH.items());logical=group*pervertex+64
router=compiler*(logical+1)*(stock+1)**2;Blarge=mass+(1<<100000)
literal=2*(1<<30000)*stock**2+8*mass+4*stock+4+32*m
assert local<1<<48 and logical<1<<6050 and router<1<<30000 and literal<1<<100000
assert 32*m*Blarge*Blarge<1<<210000 and 2*Blarge+18<1<<210000
ci=dict(local_primitive_bound=local,local_adapters=adapters,pervertex=pervertex,physical_stock_bits=stock.bit_length(),router_bits=router.bit_length(),literal_bits=literal.bit_length(),physical_row_coefficient=2*stock.bit_length()+9909+252,retained_row_coefficient=20161,compiler=compiler,G_exponent=30000,E_exponent=100000,C0_exponent=210000,required_C0_bits=(32*m*Blarge*Blarge).bit_length(),halving_degree=2,halving_integer_inequality=[73**2,2*48**2])
assert ci==cg['finite_invoice']

# Independent strict outer arithmetic; compare all 47 exact inequalities.
c=Q(result['bit_lower']);b=Q(result['complex_lower']);eta=beta=Q(1,10**18)
s=min(c,(1-beta)*b)-Q(1,10**24);a=Q(384599,10**10)
for receipt in result['bootstrap']:
 old=a;a=(1-s)*s+s*a;gap=min(s-a,1-a-s,1-a-s*(1-old),1-s)
 assert gap==Q(receipt['gap']) and old<a<s<1-a
 cutoff=int(receipt['cutoff_log2']);assert cutoff*gap**2>=36 and cutoff*gap>=2*(4+charged_two)
q=a*(1-2*eta);eps=(1-eta)/(1+q);minimum=eps*q;k=Q(result['kappa'])
assert k<minimum<=k+Q(1,10**18)
tau,sigma=1-a,1-b;lam=(tau+1-q)/2;lp=1-q;reservation=q+eta/4;r=(minimum+1-eps)/2;delta=eta/8
internal=tau+(1-beta)*max(sigma-tau,Q(0));leaf=sigma+beta*(1-sigma)
margins=dict(balanced_prefix=1-eps,coordinate_movement=a,compact_phase_layer=minimum,bulk_exposure=a,Gaussian_arithmetic=min(1-eps-delta,r-delta),scalar_work=1-eps-delta,dimension=eps)
slacks=dict(bit_positive=a,complex_above_bit=b-a,complex_below_one_over32=Q(1,32)-b,beta_positive=beta,beta_below_one=1-beta,leaf_saving_above_bit=(1-beta)*b-a,q_positive=q,q_below_internal=1-internal-q,q_below_leaf=1-leaf-q,c_positive=reservation,c_below_one=1-reservation,q_below_reservations=reservation-q,lambda_above_tau=lam-tau,lambda_above_sigma=lam-sigma,lambda_above_internal=lam-internal,lambda_prime_above_lambda=lp-lam,compact_leaf=lp-leaf,compact_reservations=lp-(1-reservation),lambda_prime_below_one=q,epsilon_positive=eps,epsilon_below_one=1-eps,guard_width=1-eps,K_geometry=1-eps*(1+reservation),K_dominates_log=eps*reservation,record_suffix=1-eps,phase_local=1-eps-delta,phase_boundary=r-delta,gamma_sublinear=1-eps-r,cell_above_band=eps-(1-r)/2,prime_interval_packing=1-eps,alpha_positive=r,alpha_below_one=1-r,alpha_below_one_fourth=Q(1,4)-r,delta_positive=delta,delta_below_one_eighth=Q(1,8)-delta,short_record_fallback=eps-a,small_field_exposure=1-eps-minimum,artificial_boundary=8-eps+r-delta-minimum,literal_scalar_guard=Q(1),row_product_gap=Q(10**6)-Q(51*20161,25))
slacks.update({n+'_above_kappa':z-k for n,z in margins.items()})
assert len(slacks)==47 and min(slacks.values())>0
assert {n:str(z) for n,z in slacks.items()}==result['strict_outer_constraints']
report=dict(status='PASS_EARLY_RESET_INDEPENDENT_RECORD_BANK_INVOICE_OUTER_AUDIT',bit_columns_both_orientations=n,bit_assignments=len(occupied),complex_assignments=len(assigned),bit_profile=dict(sorted(BH.items())),complex_profile=dict(sorted(CH.items())),bit_invoice=bi,complex_invoice=ci,kappa=str(k),strict_constraints=47,adjacent_grid_rejected=True,source_sha256=sha(Path(__file__)),input_hashes={str(p):sha(p) for p in [B/'records/249-records.bin',B/'global/GLOBAL-TEMPLATE.json.gz',C/'GLOBAL-TEMPLATE.json.gz',D/'RESULT.json']},scope='Independent finite source/program accounting and exact arithmetic. Scalar primitive and phase audits separate; inherited all-size interfaces remain conditional.')
(OUT/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],str(k))
