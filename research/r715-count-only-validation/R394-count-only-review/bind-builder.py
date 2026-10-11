import pathlib,json,hashlib,sys
B=pathlib.Path(__file__).resolve().parent;H=B.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();own=json.loads((B/'normal-001.json').read_bytes());rows=[]
for name,pkg in [('response28','r715-sharp-response28'),('replica84','r715-sharp-fallback')]:
 P=H/'R395-count-only-correction'/name/'revision-001'/'research'/pkg;mf=P/'MANIFEST.json';manifest=json.loads(mf.read_bytes())
 for path,digest in manifest.items():
  if sha(P/path)!=digest:raise ValueError('builder manifest mismatch')
 inventory={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and p!=mf and '__pycache__' not in p.parts}
 if inventory!=set(manifest):raise ValueError('builder manifest closure')
 x=json.loads((P/'EXPECTED.json').read_bytes());original=json.loads((B/(name+'-EXPECTED.json')).read_bytes());mine=next(p for p in own['profiles'] if p['preliminary']['profile']==name)
 source=json.loads((P/'SOURCE.json').read_bytes())
 if source['parent_expected_sha256']!=sha(B/(name+'-EXPECTED.json')):raise ValueError('parent expected raw binding')
 required={'kappa':mine['preliminary']['kappa'],'bit_lower':mine['root']['lower'],'bit_upper':mine['root']['upper'],'complex_lower':original['complex_lower'],'bootstrap':mine['outer']['count_only']['bootstrap'],'strict_outer_constraints':mine['outer']['count_only']['strict_outer_constraints'],'fallback_children':146478,'bad_fraction':'1/10000000000000000','gain_over_pinned_parent':mine['preliminary']['gain']}
 for key,val in required.items():
  if x[key]!=val:raise ValueError('builder mathematical mismatch'+key)
 rows.append({'profile':name,'package':str(P),'manifest_sha256':sha(mf),'files':len(manifest),'expected_sha256':sha(P/'EXPECTED.json'),'helper_sha256':sha(P/'code/sharp_bit_moment.py'),'assembler_sha256':sha(P/'code/assemble.py'),'proof_sha256':sha(P/'PROOF.md'),'exact_fields_compared':list(required),'kappa':x['kappa'],'source_audit':'Helper uses unchangedFraction1/10^16 and exact6N(N-1)+3N+6(N-1), m<=78. Assembler uses this charge in both independent source interval paths; complex charge remains original. PROOF explicitly preservesOcover and withdrawsGL transfer; historical evidence labelledwithdrawn.'})
out={'status':'PASS_DISTINCT_CORRECTED_BUILDER_SOURCE_AND_ARITHMETIC_BINDING','reviewer':'AI baseline_audit','packages':rows,'independent_math_review_sha256':sha(B/'REVIEW-001.md'),'script_sha256':sha(pathlib.Path(__file__)),'optimization':sys.flags.optimize,'scope':'Complete additive manifests, raw parent EXPECTED hash (binding inventories/invoices), compact correction roots/bootstrap/all47/kappa compared with independent R394 computation. No concrete corrected full-wrapper execution, no synthetic fixture inference, no all-sizeO law proof.'}
dest=B/('BUILDER-BINDING-OO-001.json' if sys.flags.optimize else 'BUILDER-BINDING-001.json');dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
