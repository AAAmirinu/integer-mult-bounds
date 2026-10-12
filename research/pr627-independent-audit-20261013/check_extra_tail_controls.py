"""Additional PR627 controls beyond the contributor's fourteen helper mutants.

Both middle accumulator additions and signs of both helper writes are tested.
Chi Zhao, with substantial OpenAI Codex assistance; Apache-2.0.
Uses the unchanged inherited native auditor.
"""
import argparse
import contextlib
import copy
import gzip
import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

ap = argparse.ArgumentParser()
for key in ('package', 'word', 'routing', 'out'):
    ap.add_argument('--'+key, type=Path, required=True)
a = ap.parse_args()
if not __debug__:
    raise RuntimeError('Assertions required')
a.out.mkdir(parents=True, exist_ok=False)
s = importlib.util.spec_from_file_location('native', a.package/'code/hpe_audit_and_transport.py')
native = importlib.util.module_from_spec(s); s.loader.exec_module(native)
word = json.loads(gzip.decompress(a.word.read_bytes()))
definition = json.loads((a.package/'data/FACTORED-END.json').read_text())
cases = [('positive', copy.deepcopy(word))]
for k, helper in enumerate(definition['helpers']):
    tail = definition['extra_tail'][3*k:3*k+3]
    positions = [i for i in range(len(word['cleanup'])-2) if word['cleanup'][i:i+3] == tail]
    assert len(positions) == 1
    i = positions[0]
    z = copy.deepcopy(word)
    z['cleanup'].pop(i+1)
    z['early_cleanup'] = [[j-(j>i+1),frame] for j,frame in z['early_cleanup'] if j != i+1]
    cases.append((str(helper['helper'])+'_middle_accumulator_omitted', z))
    z = copy.deepcopy(word)
    z['cleanup'][i+2][3] *= -1
    cases.append((str(helper['helper'])+'_helper_write_sign_flipped', z))
results = []
for name, mutant in cases:
    with tempfile.TemporaryDirectory(prefix='pr627-extra-control-') as tmp:
        tmp = Path(tmp); raw = tmp/'WORD.json.gz'
        raw.write_bytes(gzip.compress(json.dumps(mutant,sort_keys=True,separators=(',',':')).encode(),mtime=0))
        with (a.out/(name+'.log')).open('w') as log, contextlib.redirect_stdout(log):
            try:
                native.run(raw, a.routing, tmp/'audit')
            except AssertionError as exc:
                if name == 'positive':
                    raise
                results.append(dict(name=name,status='REJECTED',reason=str(exc)))
                print('EXPECTED REJECTION', exc)
            else:
                if name != 'positive':
                    raise RuntimeError('Mutant accepted: '+name)
    print('PASS', name, flush=True)
(a.out/'CONTROLS.json').write_text(json.dumps(dict(status='PASS_FOUR_ADDITIONAL_TAIL_CONTROLS',positive_pass=True,rejected=results,input_content_sha256=hashlib.sha256(gzip.decompress(a.word.read_bytes())).hexdigest()),indent=2)+'\n')
