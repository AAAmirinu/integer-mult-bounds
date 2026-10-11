"""Negative controls: each mutation of the final word must be rejected by our exact replay.
usage: controls.py WORD.json.gz"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e8core import *
c = load_word(sys.argv[1]); v = c['v']
def rejected(w):
    try: r = replay(w); return bool(r['viol'])
    except AssertionError: return True
muts = []
w = json.loads(json.dumps(c)); w['C'] = w['C'][:-1]; muts.append(('omit the last donor payback at FULL', w))
w = json.loads(json.dumps(c)); w['A'] = w['A'][1:]; muts.append(('omit the first donor entrance gate', w))
w = json.loads(json.dumps(c)); piv = [r for r in range(2 * v, len(w['start'])) if w['start'][r] != w['start'][v]][0]
w['start'][piv] = w['final'][v]; muts.append(('a pivot entrance moved outside its first frame (to a target cap)', w))
w = json.loads(json.dumps(c)); g = w['B'][0]; w['B'][0] = [w['final'][v], g[1], g[2]]; muts.append(('a B gate raised to a target cap', w))
w = json.loads(json.dumps(c)); w['D'][0][2] = w['D'][0][2][1:]; muts.append(('drop one completion read', w))
for name, w in muts:
    assert rejected(w), name
    print('   control rejected:', name)
