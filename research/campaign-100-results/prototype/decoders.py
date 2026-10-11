#!/usr/bin/env python3
"""T3 decoder analysis on the paired-cube port set (h = 2p, v = 8 C(p,3), cap rule |S∩T| = 1).

For each architecture 21-30 this script settles, by exact F2 linear algebra and exact Q-rank, the two
questions the verifier asks of a decoder: (a) is the mod-2 identity realisable with the proposed centres
(centres = port sets, cost = dim_Q span{chi_S : S in centre}; side reads only ports with |S∩T| = 1), and
(b) what is ell = Σ centre dims, hence D = 4v - 5 ell.

Model (N's lemma, = the verifier mod 2): design {P_j} feasible iff for every target T there is c in
span_F2{1_{P_j}} with c_T = 1 and c_S = 0 for every S in N_T = {S != T : |S∩T| in {0,2}}.
usage: decoders.py p [p ...]
"""
import sys
from itertools import combinations, product
from fractions import Fraction

PRIME = (1 << 61) - 1


def ports_of(p):
    allb = list(product(range(2), repeat=3))
    return [tuple(2 * i + b for i, b in zip(I, bits)) for I in combinations(range(p), 3) for bits in allb]


def qrank(vecs, h):
    rows = []
    piv = {}
    for vec in vecs:
        x = [a % PRIME for a in vec]
        for c, y in piv.items():
            if x[c]:
                f = x[c]
                x = [(a - f * b) % PRIME for a, b in zip(x, y)]
        nz = next((j for j in range(h) if x[j]), None)
        if nz is None:
            continue
        inv = pow(x[nz], PRIME - 2, PRIME)
        piv[nz] = [(a * inv) % PRIME for a in x]
    return len(piv)


def chi(S, h):
    return [1 if j in S else 0 for j in range(h)]


class Instance:
    def __init__(self, p):
        self.p, self.h = p, 2 * p
        self.ports = ports_of(p)
        self.v = len(self.ports)
        self.idx = {S: i for i, S in enumerate(self.ports)}
        self.sets = [set(S) for S in self.ports]
        # forbidden mask per target: T itself plus N_T
        self.forb = []
        self.free = []
        for t, T in enumerate(self.sets):
            m = 0
            fr = 0
            for s, S in enumerate(self.sets):
                k = len(S & T)
                if k in (0, 2):
                    m |= 1 << s
                elif k == 1:
                    fr |= 1 << s
            self.forb.append(m | (1 << t))
            self.free.append(fr)

    def rank(self, P):
        return qrank([chi(self.ports[s], self.h) for s in P], self.h)

    def feasible(self, gens, verbose=False):
        """gens: list of bitmasks (centre supports). Returns (#delivered targets, list of failing targets)."""
        fails = []
        for t in range(self.v):
            m = self.forb[t]
            # restrict generators to the forbidden coordinates; need e_t in the F2-span
            basis = {}
            for g in gens:
                x = g & m
                while x:
                    hb = x.bit_length() - 1
                    if hb in basis:
                        x ^= basis[hb]
                    else:
                        basis[hb] = x
                        break
            x = 1 << t
            while x:
                hb = x.bit_length() - 1
                if hb in basis:
                    x ^= basis[hb]
                else:
                    break
            if x:
                fails.append(t)
        return self.v - len(fails), fails

    def cost(self, gens):
        return sum(self.rank([s for s in range(self.v) if g >> s & 1]) for g in gens)

    # ---- structured families
    def star(self, c):
        return sum(1 << s for s in range(self.v) if c in self.sets[s])

    def pair_union(self, i):
        return self.star(2 * i) | self.star(2 * i + 1)

    def pair_avoider(self, i):
        return sum(1 << s for s in range(self.v) if not ({2 * i, 2 * i + 1} & self.sets[s]))

    def clique(self, a, b):
        return sum(1 << s for s in range(self.v) if {a, b} <= self.sets[s])

    def cube(self, I):
        return sum(1 << s for s in range(self.v) if {x // 2 for x in self.sets[s]} == set(I))

    def half_star(self, c, A):
        """ports containing c whose other two coordinates come from pairs in A (|A| = (p-1)/2 -> rank p = h/2)."""
        return sum(1 << s for s in range(self.v) if c in self.sets[s] and all(x // 2 in A for x in self.sets[s] if x != c))


def report(inst, name, gens, expect=None):
    ok, fails = inst.feasible(gens)
    cost = inst.cost(gens)
    ranks = sorted({inst.rank([s for s in range(inst.v) if g >> s & 1]) for g in gens})
    D = 4 * inst.v - 5 * cost
    print('  %-46s centres=%3d ranks=%-14s ell=%5d  D=4v-5ell=%6d  delivered %d/%d %s' % (
        name, len(gens), ranks, cost, D, ok, inst.v, 'FEASIBLE' if ok == inst.v else 'INFEASIBLE'))
    return ok == inst.v, cost


def main():
    for p in map(int, sys.argv[1:]):
        inst = Instance(p)
        h, v = inst.h, inst.v
        print('=== p=%d h=%d v=%d h(h-2)=%d 4v=%d 4v-5h(h-2)=%d' % (p, h, v, h * (h - 2), 4 * v, 4 * v - 5 * h * (h - 2)))
        stars = [inst.star(c) for c in range(h)]
        # 21: no centres at all
        print('[21] inclusion-exclusion, no centres:')
        report(inst, 'no centres (ell=0)', [])
        report(inst, 'singletons {T} (IE over sub-port T itself)', [1 << t for t in range(v)])
        cl = [inst.clique(a, b) for a in range(h) for b in range(a + 1, h) if a // 2 != b // 2]
        report(inst, 'IE over 2-sub-ports: cliques K_ab', cl)
        report(inst, 'IE over 1-sub-ports: stars (= paired cube)', stars)
        report(inst, 'IE 1- and 2-sub-ports: stars + cliques', stars + cl)
        # 22: parity-check families
        print('[22] parity-check / code-syndrome families (rows = centre supports):')
        report(inst, 'incidence code (2p stars)', stars)
        pu = [inst.pair_union(i) for i in range(p)]
        report(inst, 'pair-union rows (p, rank h-1)', pu)
        pa = [inst.pair_avoider(i) for i in range(p)]
        report(inst, 'pair-avoider rows (p, rank h-2)', pa)
        report(inst, 'stars + pair-avoiders', stars + pa)
        report(inst, 'cube rows (C(p,3), rank 4)', [inst.cube(I) for I in combinations(range(p), 3)])
        report(inst, 'cliques K_ab (4C(p,2), rank 2(p-2))', cl)
        # Hamming-like: XOR of two stars from different pairs, all such
        xs = [stars[a] ^ stars[b] for a in range(h) for b in range(a + 1, h) if a // 2 != b // 2]
        report(inst, 'star-XOR rows (all pairs of coordinates)', xs[: 2 * h])
        # minimal subfamilies of stars: dropping one star
        ok, _ = inst.feasible(stars[1:])
        print('  stars minus one: delivered %d/%d -> %s' % (ok, v, 'FEASIBLE' if ok == v else 'INFEASIBLE (every star is needed)'))
        # 23: two-level centres (super-centre = disjoint union of small centres), unions of stars by pair
        print('[23] two-level: super-centres = unions of stars (ell counted once per super-centre):')
        report(inst, 'pair unions star(2i) u star(2i+1)', pu)
        report(inst, 'pair unions + one star per pair (even coord)', pu + stars[0::2])
        # 24: 2h centres of rank h/2 (half-stars)
        print('[24] 2h centres of rank h/2 (half-stars H(c,A), H(c,B): ports with c and both other pairs in A resp. B; rank 2|A|):')
        gens = []
        for c in range(h):
            others = [i for i in range(p) if i != c // 2]
            A = others[: p // 2]
            Bp = others[p // 2:]
            gens += [inst.half_star(c, set(A)), inst.half_star(c, set(Bp))]
        report(inst, 'half-stars (2h of them, |A| = p/2)', gens)
        report(inst, 'half-stars + cross parts (= stars split in 3)', gens + [stars[c] ^ gens[2 * c] ^ gens[2 * c + 1] for c in range(h)])
        # sub-stars by selector: ports containing c with a given selector bit at the lowest other pair
        sub = []
        for c in range(h):
            for e in range(2):
                sub.append(sum(1 << s for s in range(v) if c in inst.sets[s] and min(x for x in inst.sets[s] if x != c) % 2 == e))
        report(inst, 'sub-stars by selector at the lowest other pair', sub)
        # 27/29: uniqueness of the star identity
        print('[27/29] star-centre combinations C with |T∩C| odd, |S∩C| even on N_T (all 2^h C):')
        counts = []
        for t in range(min(v, 16)):
            T = inst.sets[t]
            n = 0
            for C in range(1 << h):
                Cs = {j for j in range(h) if C >> j & 1}
                if len(T & Cs) % 2 == 0:
                    continue
                if all(len(inst.sets[s] & Cs) % 2 == 0 for s in range(v) if inst.forb[t] >> s & 1 and s != t):
                    n += 1
            counts.append(n)
        print('  valid combinations per target (first %d targets): %s  -> %s' % (len(counts), counts,
              'unique (C = T only)' if all(c == 1 for c in counts) else 'NOT unique'))
        # 28: Walsh-Hadamard: the F2 reduction of the Hadamard matrix of order 2^k is the all-ones matrix
        k = 3
        import itertools
        Hm = [[(-1) ** bin(a & b).count('1') for b in range(1 << k)] for a in range(1 << k)]
        rk = qrank([[x % 2 for x in row] for row in Hm], 1 << k)
        print('[28] Walsh-Hadamard H_%d mod 2: rank %d of %d (det = %d = 2^%d) -> not invertible over F2' % (1 << k, rk, 1 << k, (1 << k) ** ((1 << k) // 2), ((1 << k) // 2) * k))
        print()


if __name__ == '__main__':
    main()
