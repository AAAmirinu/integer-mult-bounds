#!/usr/bin/env python3
"""Exact exceptional-root census; coordinates are twice norm-squared-two roots.

This corrects the E6 geometry in PR620's ADE screen. It does not construct
a multiplication supplier or certify the full-rank-totals cost assumption.
Python 3.9+ standard library only. Apache-2.0; see README.md for attribution.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def canonical(v):
    first = next(x for x in v if x)
    return tuple(v) if first > 0 else tuple(-x for x in v)


def exceptional_lines(name):
    roots = []
    for i, j in combinations(range(8), 2):
        for sign in (1, -1):
            r = [0] * 8
            r[i], r[j] = 2, 2 * sign
            roots.append(tuple(r))
    roots.extend(s for s in product((1, -1), repeat=8)
                 if s[0] == 1 and s.count(-1) % 2 == 0)
    a = (1,) * 8
    if name == "E8":
        return roots
    roots = [r for r in roots if dot(a, r) == 0]
    if name == "E7":
        return roots
    if name == "E6":
        # a and b have inner product 1 before doubling: they span A2.
        b = (2, 2, 0, 0, 0, 0, 0, 0)
    elif name == "D6-control":
        # The archived E6() instead chooses this root perpendicular to a.
        b = (2, -2, 0, 0, 0, 0, 0, 0)
    else:
        raise ValueError("unknown root system: " + name)
    return [r for r in roots if dot(b, r) == 0]


def rational_rank(rows):
    basis = {}
    for row in rows:
        row = list(map(Fraction, row))
        for col in sorted(basis):
            factor = row[col]
            row = [x - factor * y for x, y in zip(row, basis[col])]
        pivot = next((i for i, x in enumerate(row) if x), None)
        if pivot is not None:
            value = row[pivot]
            basis[pivot] = [x / value for x in row]
    return len(basis)


def binary_rank(rows):
    basis = {}
    for row in rows:
        value = sum((int(x) % 2) << i for i, x in enumerate(row))
        while value:
            pivot = value.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value
                break
            value ^= basis[pivot]
    return len(basis)


def determinant(rows):
    a = [list(map(Fraction, row)) for row in rows]
    result = Fraction(1)
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result
        value = a[col][col]
        result *= value
        for i in range(col + 1, len(a)):
            factor = a[i][col] / value
            a[i] = [x - factor * y for x, y in zip(a[i], a[col])]
    return result


def dynkin_arms(cartan):
    n = len(cartan)
    if any(cartan[i][j] not in ({2} if i == j else {0, -1})
           for i in range(n) for j in range(n)):
        raise ValueError("not a simply laced simple-root Gram matrix")
    graph = [[j for j in range(n) if cartan[i][j] == -1] for i in range(n)]
    branch = [i for i in range(n) if len(graph[i]) == 3]
    if len(branch) != 1 or sum(map(len, graph)) != 2 * (n - 1):
        raise ValueError("expected a trivalent Dynkin tree")
    center = branch[0]
    seen, lengths = {center}, []
    for node in graph[center]:
        length, previous = 0, center
        while True:
            if node in seen:
                raise ValueError("cycle in Dynkin graph")
            seen.add(node)
            length += 1
            following = [i for i in graph[node] if i != previous]
            if not following:
                break
            if len(following) != 1:
                raise ValueError("additional Dynkin branching")
            previous, node = node, following[0]
        lengths.append(length)
    if len(seen) != n:
        raise ValueError("disconnected Dynkin graph")
    return sorted(lengths)


def analyze(roots):
    roots = [tuple(r) for r in roots]
    if not roots or any(len(r) != 8 or any(type(x) is not int for x in r)
                        or dot(r, r) != 8 for r in roots):
        raise ValueError("expected doubled integral norm-two roots in dimension eight")
    positive = set(roots)
    if len(positive) != len(roots) or any(canonical(r) != r for r in roots):
        raise ValueError("expected one canonical representative per root line")
    # Exhaust all pairs; reflection in s is r - (<r,s>/4) s in doubled coordinates.
    gram = []
    for r in roots:
        row = []
        for s in roots:
            pairing = dot(r, s)
            if pairing % 4:
                raise ValueError("nonintegral root pairing")
            pairing //= 4
            reflected = tuple(x - pairing * y for x, y in zip(r, s))
            if canonical(reflected) not in positive:
                raise ValueError("root set is not closed under reflection")
            row.append(pairing)
        gram.append(row)
    # Lexicographic positivity defines a positive system. Its indecomposable
    # positive roots are simple; check that they span the full root space.
    simple = [r for r in roots if not any(
        tuple(x - y for x, y in zip(r, s)) in positive for s in roots)]
    h = rational_rank(roots)
    if len(simple) != h or rational_rank(simple) != h:
        raise ValueError("simple roots do not form a basis")
    cartan = [[dot(r, s) // 4 for s in simple] for r in simple]
    det = determinant(cartan)
    if det.denominator != 1 or det <= 0:
        raise ValueError("invalid finite Cartan determinant")
    c = binary_rank([[1 + x for x in row] for row in gram])
    return {
        "lines": len(roots), "roots": 2 * len(roots), "dimension": h,
        "simple_roots_doubled": simple, "cartan_matrix": cartan,
        "cartan_determinant": int(det), "dynkin_arms": dynkin_arms(cartan),
        "binary_decoder_rank": c,
        "full_rank_totals_proxy": str(Fraction(c * h, len(roots))),
        "reflection_pairs_checked": len(roots) ** 2,
    }


def report():
    return {name: analyze(exceptional_lines(name))
            for name in ("E6", "E7", "E8", "D6-control")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="compare with a saved JSON census")
    args = parser.parse_args()
    result = json.dumps(report(), indent=2, sort_keys=True) + "\n"
    if args.check:
        if json.loads(result) != json.loads(args.check.read_text()):
            raise SystemExit("FAIL: saved census differs from exact recomputation")
        print("PASS: exact census, root closure, Cartan types and binary ranks")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
