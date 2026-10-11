"""Transfer PR495's main-word frame schedule onto PR484's frozen gauge selection.

Prepared by OpenAI Codex. Apache-2.0.
Usage: build_retimed.py COMPLEX484_PACKAGE BASE_WORD RETIMED495_WORD OUT
The caller must independently replay the resulting physical programs. This
builder certifies the structural transfer, not the inherited all-size contracts.
"""
from pathlib import Path
import copy
import gzip
import hashlib
import json
import sys

if not __debug__:
    raise RuntimeError('assertions must remain enabled')
assert len(sys.argv) == 5, __doc__
package, base_path, schedule_path, out = map(lambda s: Path(s).resolve(), sys.argv[1:])
assert not out.exists()
sys.path.insert(0, str(package / 'code'))
import gk_word as G


def read(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def transfer(base, candidate):
    word = copy.deepcopy(base)
    changed, prefixes = {}, {}
    for part in ('A', 'B'):
        assert len(candidate[part]) >= len(base[part])
        tail = candidate[part][-len(base[part]):]
        # Discard the separate PR495 entrance kernel. Only the frame field of
        # the identical original scalar word is permitted to cross this gate.
        assert [e[:-1] for e in tail] == [e[:-1] for e in base[part]], part
        changed[part] = sum(x[-1] != y[-1] for x, y in zip(base[part], tail))
        prefixes[part] = len(candidate[part]) - len(base[part])
        word[part] = copy.deepcopy(tail)
    word['cleanup'] = [G.inverse(e, G.FULL) for e in reversed(word['A'] + word['B'])
                       if not G.V <= e[1] < 2 * G.V]
    return word, changed, prefixes


base, candidate = read(base_path), read(schedule_path)
assert len(base['A']) == 2736 and len(base['B']) == 840
selection_path = package / 'data/selections/gauge80-kernel42.json'
selection = read(selection_path)
word, changed, discarded = transfer(base, candidate)
assert changed == {'A': 224, 'B': 504}
assert discarded == {'A': 229, 'B': 0}
original_gauge = G.build(base, selection)
retimed_gauge = G.build(word, selection)
preserved = ['centers', 'center_frames', 'target_levels', 'root_lines', 'ports',
             'cut', 'precondition', 'start_extra', 'scatter']
assert all(original_gauge[k] == retimed_gauge[k] for k in preserved)
assert len(retimed_gauge['start_extra']) == 122
assert sum(map(len, retimed_gauge['start_extra'].values())) == 148

# Check that the transfer gate cannot smuggle a changed scalar coefficient or
# register through the otherwise identical main-word tail.
controls = []
for part, field in [('A', 1), ('B', 3)]:
    bad = copy.deepcopy(candidate)
    event = bad[part][-len(base[part])]
    event[field] += 1
    try:
        transfer(base, bad)
    except AssertionError:
        controls.append([part, field])
    else:
        raise AssertionError('changed scalar field accepted')
assert len(controls) == 2

out.mkdir(parents=True)
for name, value in [('RETIMED-BASE.json.gz', word), ('FULL-WORD.json.gz', retimed_gauge)]:
    (out / name).write_bytes(G.dump(value))
receipt = dict(
    status='PASS_STRUCTURAL_MAIN_WORD_RETIMING_TRANSFER',
    source_files={str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [base_path, schedule_path, selection_path]},
    changed_frames=changed, discarded_prefix_events=discarded,
    preserved_gauge_fields=preserved, entering_helpers=122, entrance_rank=148,
    local_profile=retimed_gauge['report']['local_profile'],
    transfer_controls_rejected=controls,
    outputs={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir()},
    scope='Structural transfer; scalar, frame, phase, whole-program, hosting and finite assembly checks must run independently.')
(out / 'TRANSFER.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(receipt['status'], changed, flush=True)
