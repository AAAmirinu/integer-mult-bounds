from pathlib import Path
r=Path(__file__).parent;old=r.parent/'R398-count-only-package-review'
for name,oldline,newline in [
 ('actual28.py',"PK=R/'snapshot-28-001'","PK=pathlib.Path('F:/integer-mult-frontier/work/R395-count-only-correction/response28/revision-002/research/r715-sharp-response28')"),
 ('actual84.py',"PACKAGE=R/'snapshot-84-001'","PACKAGE=pathlib.Path('F:/integer-mult-frontier/work/R395-count-only-correction/replica84/revision-002/research/r715-sharp-fallback')")]:
 source=(old/name).read_bytes()
 if source.count(oldline.encode())!=1:raise ValueError('exact source adaptation')
 (r/name).write_bytes(source.replace(oldline.encode(),newline.encode()))
