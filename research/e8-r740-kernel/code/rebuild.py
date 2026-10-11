"""Rebuild the frozen kernel word and exercise construction-level failures.

Prepared by chafreaky with OpenAI Codex assistance; Apache-2.0.
"""
import copy
import json
from pathlib import Path

from e8core import load_word, replay
from iface386 import check
from stages import kernel, content_sha

ROOT = Path(__file__).resolve().parents[1]
parent = load_word(str(ROOT/'parent436/data/bit/bitE8-r740.json.gz'))
selected = json.loads((ROOT/'data/selection.json').read_text())
assert content_sha(parent) == selected['input_sha256']
word, entries, rank, donors = kernel(parent, selected['entries'])
assert (entries, rank, donors) == (115, 136, 103)
assert content_sha(word) == selected['output_sha256']
assert word == load_word(str(ROOT/'data/word.json.gz'))
audit = replay(word, span_mode='z')
assert not audit['viol'], audit['viol'][:5]
interface = check(word, 192)
assert interface['prefix_ok'] and interface['prefix_bits'] == 123

rejected = []
for name, mutate in [
    ('retained row used as pivot', lambda s: s[0].__setitem__(1, parent['ret'][0])),
    ('duplicate pivot', lambda s: s.append(copy.deepcopy(s[0]))),
]:
    bad = copy.deepcopy(selected['entries'])
    mutate(bad)
    try:
        kernel(parent, bad)
    except AssertionError:
        rejected.append(name)
    else:
        raise AssertionError('accepted invalid kernel selection: '+name)
bad = copy.deepcopy(word)
bad['A'][0][2].pop()
try:
    bad_audit = replay(bad, span_mode='z')
except AssertionError:
    pass
else:
    assert bad_audit['viol'], 'missing dirty-response correction accepted'
rejected.append('omit a kernel dirty-response correction')
print(json.dumps(dict(status='PASS_FROZEN_KERNEL_REBUILD_AND_LOCAL_INTERFACE',
                      input_sha256=content_sha(parent), output_sha256=content_sha(word),
                      entries=entries, entrance_rank=rank, donor_slots=donors,
                      interface=interface, mutations_rejected=rejected), sort_keys=True))
