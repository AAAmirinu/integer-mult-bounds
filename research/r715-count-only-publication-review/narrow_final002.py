import pathlib,json,hashlib
R=pathlib.Path(__file__).parent;W=R.parent;P=W/'R404-corrected-publication/publish';V=P/'research/r715-count-only-validation'
def need(b,m):
 if not b:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
old=read(R/'FINAL-SNAPSHOT-001.json');new={p.relative_to(P).as_posix():sha(p) for p in P.rglob('*') if p.is_file()};changed=[k for k,h in old['published_file_inventory'].items() if new.get(k)!=h]
allowed={'research/r715-count-only-validation/ACCEPTANCE.json','research/r715-count-only-validation/MANIFEST.json','research/r715-count-only-validation/required-checks/STATUS.json'};need(set(changed)<=allowed,'changed scientific artifact')
mf=read(V/'MANIFEST.json');need(mf=={p.relative_to(V).as_posix():sha(p) for p in V.rglob('*') if p.is_file() and p.name!='MANIFEST.json'},'complete final manifest')
copies={}
for name,h in new.items():
 if name in old['published_file_inventory']:continue
 if '/required-checks/' in name:orig=W/'R393-required-repository-checks'/name.rsplit('/',1)[1]
 elif '/R405-' in name or '/r715-count-only-publication-review/' in name:orig=R/name.rsplit('/',1)[1]
 else:
  # The review attachment is outside the self-bound validation inventory.
  orig=R/name.rsplit('/',1)[1];need(orig.is_file(),'unknown added publication file '+name)
 need(orig.read_bytes()==(P/name).read_bytes(),'raw additional metadata '+name);copies[name]=h
status=read(V/'required-checks/STATUS.json');acc=read(V/'ACCEPTANCE.json');need('Terminal FAIL' in status['gen4'] and 'OOM' in status['gen4'] and 'pending' not in status['gen4'],'terminal baseline honest');need('NOT_ALL_PASS' in acc['required_baseline_checks'] and 'pending' not in acc['required_baseline_checks'],'acceptance not pending')
out={'status':'PASS_NARROW_TERMINAL_BASELINE_PUBLICATION_UPDATE','prior_snapshot_sha256':sha(R/'FINAL-SNAPSHOT-001.json'),'changed_metadata_only':sorted(changed),'additional_raw_copies':copies,'validation_manifest_sha256':sha(V/'MANIFEST.json'),'acceptance_sha256':sha(V/'ACCEPTANCE.json'),'published_file_inventory':new,'scientific_packages_actual_receipts_and_math_unchanged':True,'required_baseline_all_pass':False,'scope':'Both inherited baseline suites terminally fail at declared2GiB limit. Source-specific corrected finite admission unchanged; no broad all-checks-pass claim. Snapshot reviewer attachment may be copied separately without scientific mutation.','checker_sha256':sha(pathlib.Path(__file__))}
(R/'FINAL-SNAPSHOT-002.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(new),len(copies))
