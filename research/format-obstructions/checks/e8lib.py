"""The 120 E8 root lines in Construction-A (Hamming) coordinates, and the graphs on them.

Excerpt of the local research file cxlib.py (DreamingOfClouds, with Anthropic Claude assistance). The coordinates
are those of PR #370 (Dylan Crow): 8 coordinate lines 2e_i and 112 sign lines on the 14 weight-4 blocks of the
extended Hamming code H8. With <a, b> = (a . b)/2 on the integer representatives:
  * the 'in-cap' (lossless-helper) graph of the E8 complex word joins lines with <a, b> = +-1 (degree 56);
  * the E8-orthogonal pairs (<a, b> = 0) have degree 63.
"""
import itertools

V = 120


def _ham():
    g = [(1, 1, 1, 1, 0, 0, 0, 0), (1, 1, 0, 0, 1, 1, 0, 0), (1, 0, 1, 0, 1, 0, 1, 0), (0, 1, 1, 0, 1, 0, 0, 1)]
    H = set()
    for a in itertools.product((0, 1), repeat=4):
        H.add(tuple(sum(a[k] * g[k][i] for k in range(4)) % 2 for i in range(8)))
    return sorted(H)


H8 = _ham()
BLOCKS = sorted(tuple(i for i in range(8) if w[i]) for w in H8 if sum(w) == 4)
assert len(BLOCKS) == 14
LINES = []
for i in range(8):
    v = [0] * 8
    v[i] = 2
    LINES.append(tuple(v))
for c in BLOCKS:
    for sg in itertools.product((1, -1), repeat=3):
        v = [0] * 8
        v[c[0]] = 1
        for k, s in zip(c[1:], sg):
            v[k] = s
        LINES.append(tuple(v))
assert len(LINES) == V


def ip(u, v):
    return sum(a * b for a, b in zip(u, v)) // 2


G = [[ip(LINES[a], LINES[b]) for b in range(V)] for a in range(V)]
NB = [[b for b in range(V) if abs(G[a][b]) == 1] for a in range(V)]          # in-cap (non-orthogonal) neighbours
OR = [[b for b in range(V) if a != b and G[a][b] == 0] for a in range(V)]     # E8-orthogonal pairs
assert all(len(x) == 56 for x in NB) and all(len(x) == 63 for x in OR)
assert all(G[a][a] == 2 for a in range(V))
ORTH_PAIRS = [(a, b) for a in range(V) for b in range(a + 1, V) if G[a][b] == 0]
assert len(ORTH_PAIRS) == V * 63 // 2
