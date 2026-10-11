"""Use exact row reduction for the local stream check."""
from fractions import Fraction as Q


def row_space(rows):
    basis = {}
    for row in rows:
        row = list(map(Q, row))
        for p, b in sorted(basis.items()):
            a = row[p]
            row = [x - a * y for x, y in zip(row, b)]
        p = next((j for j, x in enumerate(row) if x), None)
        if p is None:
            continue
        a = row[p]
        row = tuple(x / a for x in row)
        for k, b in list(basis.items()):
            a = b[p]
            basis[k] = tuple(x - a * y for x, y in zip(b, row))
        basis[p] = row
    return tuple(b for _, b in sorted(basis.items()))
