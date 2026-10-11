"""usage: mksel.py PKG SEL.json : write PKG/stages/kernel-selection.json and PKG/data/final word from our ILS selection"""
import sys, os, json, subprocess
P = sys.argv[1]; sys.path.insert(0, P + '/code')
from stages import *
import apply376, gzip
raw = open(P + '/data/input/bitE8-r865.json.gz', 'rb').read(); c0 = json.loads(gzip.decompress(raw))
fs = json.load(open(P + '/data/pr376/frame-selection.json')); rs = json.load(open(P + '/data/pr376/reuse-selection.json'))
c = apply376.apply_reuse(apply376.apply_frames(c0, fs), rs); assert content_sha(c) == rs['output_sha256']
c = json.loads(json.dumps(c))
sel = json.load(open(sys.argv[2])); v = c['v']
lines = lambda m: [i for i in range(v) if m >> i & 1]
S = sorted([[lines(E), p, sorted(D)] for E, p, D in sel], key=lambda x: (x[1]))
w, ne, tot, nd = kernel(c, S)
out = dict(stage='kernel', input='PR376 word (our reconstruction; canonical sha256 = PR376 reuse-selection output_sha256)',
           input_sha256=content_sha(c), output_sha256=content_sha(w), entries_count=ne, total_entrance_rank=tot, donor_slots=nd, entries=S)
json.dump(out, open(P + '/stages/kernel-selection.json', 'w'), indent=0); save_word(w, P + '/data/final/bitE8-nine-kernel.json.gz')
print(ne, tot, nd, out['output_sha256'])
