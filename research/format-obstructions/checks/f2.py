"""Exact F_2 helpers (vectors are Python ints, the form is the standard dot product mod 2)."""


def par(x):
    return bin(x).count("1") & 1


def dot(a, b):
    return bin(a & b).count("1") & 1


def span_basis(vecs):
    """Echelon basis (list of ints, descending pivots) of the F_2 span."""
    basis = []
    for u in vecs:
        for b in basis:
            if u ^ b < u:
                u ^= b
        if u:
            basis.append(u)
            basis.sort(reverse=True)
    return basis


def rank(vecs):
    return len(span_basis(vecs))


def pairing_rank(A, B):
    """Rank of the bilinear pairing span(A) x span(B) -> F_2 (dot product)."""
    a, b = span_basis(A), span_basis(B)
    rows = []
    for x in a:
        r = 0
        for j, y in enumerate(b):
            if dot(x, y):
                r |= 1 << j
        rows.append(r)
    return rank(rows)
