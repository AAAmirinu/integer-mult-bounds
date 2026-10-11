"""Recompute the finite costs, strict supplier moments, and outer bound."""
import json
import math
from fractions import Fraction as Q
from moments import certify as moment_certificate
from outer import outer

MAIN_COMMIT = '12a4934d15006e8c10f9b2264f13f8f341be802b'
MAIN_KAPPA = Q(90446448750933,125000000000000000)
KAPPA = Q(1307044366925301,10**18)
BIT_LOWER = Q(1308789373120170692069,10**24)
COMPLEX_LOWER = Q(654377483866781393011,5*10**23)


def read(path):
    return json.loads(path.read_text())


def round64(number):
    return 64*((number+63)//64)

def bit_invoice(g,geo):
    profile={int(k):v for k,v in g['profile'].items()};E=sum(profile.values())
    m,W,R,T,L,V=78,4800,705,4,11,120
    assert (g['m'],g['live'],g['R'],g['replicas'],g['physical'])==(m,W,R,T,W+9)
    assert sum(r*n for r,n in profile.items())==m*W-1632
    assert m**3>2*max(profile)**3
    J=L*T*(8*(2*V+R)+2*R)+8*W+2*g['copy_erase_episodes']
    coefficient=int(g['global_prefix_bound'])+1+L*T*g['local_additions']+g['bridge_additions']
    coefficient+=J*(16*(m*m+1)**2+g['physical'])+E*(8*m*m+8+128*(2*m)**3)
    coefficient+=16*m**3+g['copy_erase_episodes']
    coefficient+=2*L*T*((W-1)+R*m*(geo['max_route_factors']+144+4+m-1+m))
    three=((coefficient+1)*(E+1))**3
    stock_power=0
    while 3**stock_power<=g['physical']:stock_power+=1
    row=3*(m*(m+1)//2+stock_power)+9909+252
    additive=3*(m*(m+1)//2+stock_power)
    assert row<20161 and (20161-row)*32>additive
    bits=int(g['global_prefix_bound']).bit_length()
    return dict(live=W,physical=W+9,prefix_bits=bits,charged_prefix_bits=round64(bits),
        coefficient_bits=coefficient.bit_length(),three_level_coefficient_bits=three.bit_length(),
        charged_three_level_coefficient_bits=round64(three.bit_length()),row_coefficient=row,
        row_bound=dict(stock_exponent=m*(m+1)//2+stock_power,
                       additive_stock_charge=additive,minimum_log2_width=32,
                       threshold_margin=(20161-row)*32-additive))

def complex_invoice(g):
    p={int(k):v for k,v in g['profile'].items()};count=sum(p.values());mass=sum(r*n for r,n in p.items())
    assert (g['m'],g['live'],g['physical'],mass,max(p))==(89,9600,10178,851136,64)
    checks=g['source_local_checks'];forward,backward=checks['forward'],checks['backward']
    assert all(z['all_columns']==800 and z['private_centers_cleared'] and z['helpers_restored_as_scalar_rows'] for z in checks.values())
    macros=max(z['scalar_macros'] for z in checks.values());children=sum(forward['paid_profile'].values())
    compiler=64*90**3
    adapters=16*(macros+children+240+560+g['private_centers'])+64*89+2*560*8
    assert g['charged_wrapper_groups']==11*8*2*560*8 and g['wrapper_events']==11*8*158
    local=max(z['real_component_primitive_bound'] for z in checks.values())+adapters*compiler
    scalar=8*(6*forward['real_component_primitive_bound']+5*backward['real_component_primitive_bound'])
    bridges=6*4*120*8;shifts=5*120*8;moves=10*120*8
    external=6*120*8*11+4*11*8*560+26*120*8+bridges+shifts+moves+9600+10178
    pervertex=scalar+bridges+shifts+moves+9600+(88*adapters+8*external+64*89)*compiler+64*10178
    group=(1<<(44*44))*math.prod((1<<(2*j))-1 for j in range(1,45))
    stock=group*10178;logical=group*pervertex+64;router=compiler*(logical+1)*(stock+1)**2
    scaled_mass=group*mass;literal=2*(1<<30000)*stock**2+8*scaled_mass+4*stock+4+32*89
    boundary=scaled_mass+(1<<100000)
    assert local<1<<48 and logical<1<<6050 and router<1<<30000 and literal<1<<100000
    assert boundary<1<<100001 and 32*89*boundary**2<1<<210000 and 2*boundary+18<1<<210000
    assert (pervertex+1)**3*(count+1)**3<1<<1024
    bits=stock.bit_length();slope=Q(9,4)*bits+9909+252;additive=9*bits
    assert 89**2<=2*64**2 and 89**3>2*64**3
    assert 89**9>16*64**9 and (20161-slope)*32>additive
    expected=dict(live=9600,physical=10178,maxchild=64,rank_mass=mass,hosted_residuals=11*8*560,
        wrapper_events=g['wrapper_events'],charged_wrapper_groups=g['charged_wrapper_groups'],
        max_helpers_per_physical_family_per_call=1,physical_stock_bits=bits,router_bits=router.bit_length(),
        literal_bits=literal.bit_length(),row_coefficient=20161,local_bound=local,pervertex=pervertex,halving_depth=3)
    row=dict(status='PASS_FRACTIONAL_DEPTH_ROW_RESERVE',block_steps=9,block_halvings=4,
        exact_shrink_inequality=[89**9,16*64**9],stock_bits=bits,row_slope=str(slope),
        additive_stock_charge=additive,minimum_log2_width=32,retained_row_coefficient=20161,
        threshold_margin=str((20161-slope)*32-additive),coarse_three_level_row=3*bits+9909+252,
        finite_three_level_halving=[89**3,2*64**3])
    expected['row_bound']=row
    return expected

def compose(bit, complex_dir):
    """Use fresh emitted data and checked global audits."""
    bg = read(bit/'GLOBAL.json')
    ba = read(bit/'AUDIT.json')
    geo = read(bit/'GEOMETRY.json')
    cg = read(complex_dir/'GLOBAL.json')
    ca = read(complex_dir/'AUDIT.json')
    assert ba['status'] == 'PASS_INDEPENDENT_ELEVEN_STAGE_HOSTING_AUDIT'
    assert ca['status'] == 'PASS_INDEPENDENT_ADAPTED_KERNEL_GLOBAL_AUDIT'
    for data, audit in ((bg,ba),(cg,ca)):
        for key in ('profile','template_sha256','emitted_program_sha256'):
            assert data[key] == audit[key]
    bp = {int(rank): count for rank,count in ba['profile'].items()}
    cp = {int(rank): count for rank,count in ca['profile'].items()}
    bit_cost = bit_invoice(bg,geo)
    complex_cost = complex_invoice(cg)
    bit_moment = moment_certificate(bp,78,4800,BIT_LOWER)
    complex_moment = moment_certificate(cp,89,9600,COMPLEX_LOWER)
    combined = outer(BIT_LOWER,COMPLEX_LOWER)
    assert combined['kappa'] == KAPPA
    assert combined['binding_component'] == 'complex'
    assert len(combined['strict_outer_constraints']) == 47
    assert len(combined['bootstrap']) == 6
    assert combined['minimum_margin'] <= KAPPA+Q(1,10**18)
    assert KAPPA > Q(9,5)*MAIN_KAPPA
    gain = KAPPA/MAIN_KAPPA-1
    return {
        'status':'PASS_CONDITIONAL_COMBINED_E8_WITNESS',
        'kappa':str(KAPPA),
        'kappa_decimal':'0.001307044366925301',
        'main_commit':MAIN_COMMIT,
        'main_kappa':str(MAIN_KAPPA),
        'relative_gain':str(gain),
        'gain_percent':format(float(100*gain),'.12f'),
        'binding_component':combined['binding_component'],
        'bit':{'profile':bg['profile'],'invoice':bit_cost,'moment':bit_moment,
               'emitted_program_sha256':bg['emitted_program_sha256']},
        'complex':{'profile':cg['profile'],'invoice':complex_cost,'moment':complex_moment,
                   'emitted_program_sha256':cg['emitted_program_sha256']},
        'strict_outer_constraints':{name:str(value) for name,value in combined['strict_outer_constraints'].items()},
        'bootstrap':combined['bootstrap'],
        'next_grid_rejected':True,
        'scope':'Finite local identities, exact phases, routed templates, invoices, moment signs and outer arithmetic. The all-size interfaces in PROOF.txt remain conditions.'
    }
