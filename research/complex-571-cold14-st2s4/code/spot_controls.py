"""spot_controls.py PACKAGE AUDIT_DIR JP8_CANONICAL_WORD OUT.json

Packaged controls for the pivot-swap spot-width generalisation (witness.spot_widths).
Runs the package's own assemble() on its admitted owner/invoice receipts (AUDIT_DIR = <discover>/mixed-global/audit),
with WITNESS_DISCOVER=1 so that spec pins only record; the spot-width assert is then the deciding check, and every
control must be rejected at exactly that source line.
  baseline   the real receipts                                         -> accepted
  (a)        wrong width at a SWAPPED pivot spot   (jp8 (8,9,8,8))       -> rejected at the spot_widths line
  (b)        wrong width at an UNSWAPPED spot      (jp8 (9,9,9,8))       -> rejected at the spot_widths line
  (c)        revert: assemble.py with the old `all(...==8 for h in SPOT)` check, real receipts -> rejected at the old line;
             plus the old predicate evaluated on the real jp8 canonical word (as in bind/audit) is False, the new is True.
Each mutation swaps two helper widths, so the width inventory and sum are unchanged (the only failing check is the spot).
"""
import copy, gzip, hashlib, json, os, shutil, sys, tempfile, traceback
from pathlib import Path
PKG, AUD, WORD, OUT = map(Path, sys.argv[1:5])
os.environ['WITNESS_SPEC'] = str((PKG / 'data/SPEC.json').resolve()); os.environ['WITNESS_DISCOVER'] = '1'
os.environ.pop('WITNESS_RECORD', None)
assert os.environ.get('GAIN_PR564_SOURCE'), 'set GAIN_PR564_SOURCE to the pinned PR568 package (research/complex-multicold)'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
NEW = "assert tuple(p['widths'][h]for h in SPOT)==spot_widths(pid)"
OLD = "assert all(p['widths'][h]==8 for h in SPOT)"
owner_p, inv_p = AUD / 'OWNERS-AND-PROFILE.json', AUD / 'PREFIX-AND-INVOICE.json'
owner, invoice = json.loads(owner_p.read_text()), json.loads(inv_p.read_text())

def load_assemble(code_dir):
    for m in ('assemble', 'witness', 'generated_identity'): sys.modules.pop(m, None)
    sys.path.insert(0, str(code_dir))
    try:
        import assemble; return assemble.assemble
    finally:
        sys.path.remove(str(code_dir))

def outcome(fn, o, i):
    try:
        fn(o, i, sha(owner_p), sha(inv_p))
    except AssertionError:
        fr = traceback.extract_tb(sys.exc_info()[2])[-1]
        return dict(rejected=True, file=Path(fr.filename).name, line=fr.line.strip().split(';')[-1].strip() if fr.line else '')
    return dict(rejected=False)

new = load_assemble((PKG / 'code').resolve())
import witness
SPOT, want = witness.SPOT, witness.spot_widths('jp8')
assert want == (9, 9, 8, 8), want
res = {'spot': list(SPOT), 'jp8_expected': list(want)}
res['baseline'] = outcome(new, copy.deepcopy(owner), copy.deepcopy(invoice)); assert not res['baseline']['rejected'], res

def swapped(k, target_width):
    i = copy.deepcopy(invoice); w = i['providers']['jp8']['widths']; h = SPOT[k]
    j = next(j for j, x in enumerate(w) if x == target_width and j not in SPOT); w[h], w[j] = w[j], w[h]
    return i, [w[s] for s in SPOT]
ia, sa = swapped(0, 8); ib, sb = swapped(2, 9)
assert sa == [8, 9, 8, 8] and sb == [9, 9, 9, 8], (sa, sb)
res['a_swapped_pivot_spot'] = dict(spot_widths=sa, **outcome(new, copy.deepcopy(owner), ia))
res['b_unswapped_spot'] = dict(spot_widths=sb, **outcome(new, copy.deepcopy(owner), ib))
for k in ('a_swapped_pivot_spot', 'b_unswapped_spot'):
    assert res[k]['rejected'] and res[k]['file'] == 'assemble.py' and res[k]['line'] == NEW, res[k]

tmp = Path(tempfile.mkdtemp()); shutil.copytree(PKG / 'code', tmp / 'code')
src = (tmp / 'code/assemble.py').read_text(); assert src.count(NEW) == 1
(tmp / 'code/assemble.py').write_text(src.replace(NEW, OLD))
old = load_assemble(tmp / 'code')
res['c_revert_assemble'] = outcome(old, copy.deepcopy(owner), copy.deepcopy(invoice))
assert res['c_revert_assemble']['rejected'] and res['c_revert_assemble']['line'] == OLD, res['c_revert_assemble']
shutil.rmtree(tmp)
w = json.loads(gzip.decompress(WORD.read_bytes()))
widths = [len(w['frames'][w['final'][r]]) - len(w['frames'][w['start'][r]]) for r in range(2*112, 2*112 + w['R'])]
res['c_revert_word'] = dict(word_sha256=sha(WORD), spot_widths=[widths[h] for h in SPOT],
                            old_check=all(widths[h] == 8 for h in SPOT), new_check=tuple(widths[h] for h in SPOT) == want)
assert res['c_revert_word']['old_check'] is False and res['c_revert_word']['new_check'] is True, res['c_revert_word']
res['status'] = 'PASS_SPOT_WIDTH_CONTROLS'
OUT.write_text(json.dumps(res, indent=1) + '\n'); print(json.dumps(res, indent=1))
