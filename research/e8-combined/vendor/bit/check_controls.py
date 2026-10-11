"""Check rejection at the word and record boundaries."""
import copy,json,struct,tempfile,sys
from pathlib import Path
from check_word import check as word_check
from check_records import check as records_check

base,source,result_path=map(Path,sys.argv[1:])
word=json.loads(base.read_text());controls=[]

def reject_word(name,mutate):
    altered=copy.deepcopy(word);mutate(altered)
    try:word_check(altered)
    except AssertionError:controls.append(name)
    else:raise AssertionError('accepted '+name)

full=next(i for i,ids in enumerate(word['frames']) if len(ids)==120)
helper=next(r for r in range(240,945) if word['start'][r]!=0)
reject_word('full helper entrance has no residual',lambda c:c['start'].__setitem__(helper,full))
reject_word('missing dirty-target correction',lambda c:c['D'].pop(0))
with tempfile.TemporaryDirectory() as directory:
    folder=Path(directory)
    for name in ('249-records.bin','249-states.json','frames.json'):
        (folder/name).write_bytes((source/name).read_bytes())
    records=list(struct.iter_unpack('<6i',(folder/'249-records.bin').read_bytes()))
    index=next(i for i,row in enumerate(records) if row[0]==1)
    row=list(records[index]);row[3]=0;records[index]=tuple(row)
    (folder/'249-records.bin').write_bytes(b''.join(struct.pack('<6i',*row) for row in records))
    try:records_check(base,folder)
    except AssertionError:controls.append('exported ADD coefficient differs from word')
    else:raise AssertionError('accepted corrupt export')
result=dict(status='PASS_INDEPENDENT_BOUNDARY_CONTROLS',rejected=controls)
result_path.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
