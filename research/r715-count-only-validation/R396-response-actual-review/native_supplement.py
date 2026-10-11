import pathlib,json,hashlib
R=pathlib.Path(__file__).parent;P=pathlib.Path('F:/integer-mult-frontier/work/R385-response28-full/data/full-002/bit');read=lambda p:json.loads(p.read_bytes());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
checks={}
for name,status in [('cout/legality.json','PASS_INDEPENDENT_COHORT_LEGALITY_SOURCE_OWNERS_AND_LIFECYCLE'),('cout/columns.json','PASS_NEW_COHORT249_ALL_FIVE_STAGE_FORMAL_COLUMNS_AND_PREFIX_BILL'),('LABELS.json','PASS_TARGET_COMMON_LABEL_LIFT_CONTROLS'),('nested/NESTED-AUDIT.json','PASS_NESTED_DONOR_FLAG_CONSTRUCTION'),('hosted/GEOMETRY.json','PASS_COMPRESSED_ELEVEN_BIT_GEOMETRY')]:
 x=read(P/name);need(x['status']==status,'native/geometry enum '+name);checks[name]=sha(P/name)
l=read(P/'cout/legality.json');c=read(P/'cout/columns.json');n=read(P/'nested/NESTED-AUDIT.json');g=read(P/'hosted/GEOMETRY.json')
need(l['copies']==l['erasures']==9 and l['all_final_frames_pass']is True,'lifecycles');need(c['formal_columns_checked']==1195 and bool(c['negative_controls']),'signed formal columns');need(n['candidate_kernel_rows']==120 and n['source_kernel_rows']==102 and n['distinct_donor_roles']==102 and n['monotone_donor_chains']is True and bool(n['controls']),'actual flags');need(n['after']['columns']==955 and n['candidate_sha256']==sha(P/'word.json'),'flag word binding');need(g['m']==78 and g['stages']==11 and len(g['ports'])==120 and not g['bank_slots']and not g['bank_permutations']and bool(g['missing_route_factor_controls']),'actual geometry')
result=dict(status='PASS_ACTUAL_NATIVE_FRAME_GEOMETRY_ENUMS_AND_HASHES',bindings=checks,formal_signed_columns=1195,dirty_columns=955,copies=9,donors=102,correction_rows=120,scope='Actual completed native/frame/geometry outputs, checked metadata and byte bindings; no independent re-execution or all-size theorem.')
(R/'NATIVE-SUPPLEMENT-001.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
