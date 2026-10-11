"""Labels and exact nondegeneracy. (1) the 120 labels are the root lines of E8 under <x,y> = x.y/2: norm 2, pairwise
|<a,b>| <= 1, rank 8; the form is positive definite; (2) every frame of the word (B rows of the exported snapshot):
Gram determinant under the E8 form, exactly, > 0; primes dividing them.
usage: nondeg.py WORD.json.gz SNAPDIR"""
import sys, os, json
from fractions import Fraction as Q
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from e8core import load_word, rank
c = load_word(sys.argv[1]); fr = json.load(open(sys.argv[2] + '/frames.json'))['frames']
lines = [tuple(x) for x in c['lines']]; v = len(lines); assert v == 120 and c['h'] == 8 and c['form'] == '<x,y>/2'
ip = lambda a, b: Q(sum(x * y for x, y in zip(a, b)), 2)
assert all(ip(a, a) == 2 for a in lines) and len(set(lines)) == v
assert all(abs(ip(lines[i], lines[j])) <= 1 for i in range(v) for j in range(i + 1, v))
assert rank(lines) == 8
def det(M):
    M = [[Q(x) for x in r] for r in M]; n = len(M); d = Q(1)
    for col in range(n):
        p = next((i for i in range(col, n) if M[i][col] != 0), None)
        if p is None: return Q(0)
        if p != col: M[col], M[p] = M[p], M[col]; d = -d
        d *= M[col][col]
        for i in range(col + 1, n):
            f = M[i][col] / M[col][col]; M[i] = [a - f * b for a, b in zip(M[i], M[col])]
    return d
I = [[int(i == j) for j in range(8)] for i in range(8)]
lead = [det([[ip(I[i], I[j]) for j in range(k)] for i in range(k)]) for k in range(1, 9)]
assert all(x > 0 for x in lead), 'form positive definite'
def factor(n):
    out = Counter(); p = 2
    while p * p <= n:
        while n % p == 0: out[p] += 1; n //= p
        p += 1
    if n > 1: out[n] += 1
    return out
primes = Counter(); maxbits = 0; cnt = 0
for k, f in fr.items():
    B = f['B']
    if not B: continue
    d = det([[ip(a, b) for b in B] for a in B]); assert d > 0, ('degenerate frame', k)
    cnt += 1; maxbits = max(maxbits, d.numerator.bit_length(), d.denominator.bit_length())
    for p in factor(d.numerator): primes[p] += 1
    for p in factor(d.denominator): primes[p] += 1
print('   labels: 120 E8 root lines (norm 2, |<a,b>| <= 1, rank 8); form positive definite')
print('   nondegeneracy: %d nonzero frames, every Gram determinant > 0 (max %d bits); primes in determinants %s -> any odd prime is a witness'
      % (cnt, maxbits, sorted(primes)))
