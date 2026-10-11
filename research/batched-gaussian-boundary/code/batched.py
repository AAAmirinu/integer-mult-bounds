"""Rounded block-bidiagonal and cyclic solves with exact Strassen products.

Finite prototype, not a tape-machine implementation. Offline rational tables
are rounded once. Each online matrix product is exact until its output grid.
"""
from fractions import Fraction as Q


def zeros(n, m):
    return [[Q(0) for _ in range(m)] for _ in range(n)]


def add(a, b, sign=1):
    return [[x+sign*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def rounded(x, bits):
    if bits is None:
        return x
    scale = 1 << bits
    k = abs(x.numerator*scale)//x.denominator
    return Q(k if x >= 0 else -k, scale)


def grid(a, bits):
    return [[rounded(x, bits) for x in row] for row in a]


def strassen(a, b, count):
    n = len(a)
    assert n and n & (n-1) == 0
    assert all(len(row) == n for row in a+b) and len(b) == n
    if n == 1:
        count['scalar_products'] += 1
        return [[a[0][0]*b[0][0]]]
    h = n//2
    def split(x):
        return ([r[:h] for r in x[:h]], [r[h:] for r in x[:h]],
                [r[:h] for r in x[h:]], [r[h:] for r in x[h:]])
    a11, a12, a21, a22 = split(a)
    b11, b12, b21, b22 = split(b)
    mul = lambda x, y: strassen(x, y, count)
    p1 = mul(add(a11, a22), add(b11, b22))
    p2 = mul(add(a21, a22), b11)
    p3 = mul(a11, add(b12, b22, -1))
    p4 = mul(a22, add(b21, b11, -1))
    p5 = mul(add(a11, a12), b22)
    p6 = mul(add(a21, a11, -1), add(b11, b12))
    p7 = mul(add(a12, a22, -1), add(b21, b22))
    c11 = add(add(add(p1, p4), p5, -1), p7)
    c12 = add(p3, p5)
    c21 = add(p2, p4)
    c22 = add(add(add(p1, p3), p2, -1), p6)
    count['scalar_additions'] += 18*h*h
    return [x+y for x, y in zip(c11, c12)]+[x+y for x, y in zip(c21, c22)]


def product(a, b, h, count, bits=None):
    """Rectangular tiling by h-square products; exact accumulation then grid."""
    n, k, m = len(a), len(b), len(b[0])
    assert n and k and m and all(len(row) == k for row in a)
    assert all(len(row) == m for row in b)
    out = zeros(n, m)
    for i in range(0, n, h):
        for j in range(0, m, h):
            block = zeros(h, h)
            for t in range(0, k, h):
                aa, bb = zeros(h, h), zeros(h, h)
                for x in range(min(h, n-i)):
                    for y in range(min(h, k-t)):
                        aa[x][y] = a[i+x][t+y]
                for x in range(min(h, k-t)):
                    for y in range(min(h, m-j)):
                        bb[x][y] = b[t+x][j+y]
                block = add(block, strassen(aa, bb, count))
                count['tiles'] += 1
            for x in range(min(h, n-i)):
                for y in range(min(h, m-j)):
                    out[i+x][j+y] = rounded(block[x][y], bits)
    return out


def prepare_triangle(t, h, upper, inverse, bits):
    """Only diagonal/adjacent blocks are allowed; inversions are offline."""
    n = len(t)
    assert all(len(row) == n for row in t)
    blocks = []
    for i in range(0, n, h):
        end = min(i+h, n)
        prev = i+h if upper else i-h
        near = list(range(max(0, prev), min(n, prev+h))) if 0 <= prev < n else []
        for row in range(i, end):
            assert all(t[row][col] == 0 for col in range(n)
                       if not i <= col < end and col not in near)
        diag = [row[i:end] for row in t[i:end]]
        c = inverse(diag)
        # This polynomial-time product is setup, never online work.
        a = [[-sum((c[x][j]*t[i+j][y] for j in range(end-i)), Q(0))
              for y in near] for x in range(end-i)]
        blocks.append(dict(start=i, end=end, near=near, c=grid(c, bits), a=grid(a, bits)))
    return dict(blocks=blocks, upper=upper, h=h, bits=bits, n=n)


def triangle(table, b, count):
    assert len(b) == table['n']
    h, bits = table['h'], table['bits']
    out = zeros(len(b), len(b[0]))
    seq = reversed(table['blocks']) if table['upper'] else table['blocks']
    for block in seq:
        i, end = block['start'], block['end']
        y = product(block['c'], b[i:end], h, count)
        if block['near']:
            y = add(y, product(block['a'], [out[j] for j in block['near']], h, count))
        out[i:end] = grid(y, bits)
    return out


def prepare(s, bandwidth, bits):
    from downstream_banded_inverse import lu_banded, inverse_exact, solve_exact
    n = len(s)
    assert n >= 2*bandwidth
    assert all(s[i][j] == 0 for i in range(n) for j in range(n)
               if min(abs(i-j), n-abs(i-j)) > bandwidth)
    a = [[x if abs(i-j) <= bandwidth else Q(0) for j, x in enumerate(row)]
         for i, row in enumerate(s)]
    low, high, metadata = lu_banded(a, bandwidth)
    h = 1 << (bandwidth-1).bit_length()
    border = list(range(bandwidth))+list(range(n-bandwidth, n))
    v = [[s[i][j]-a[i][j] for j in range(n)] for i in border]
    support = [j for j in range(n) if any(row[j] for row in v)]
    assert len(support) <= 2*bandwidth
    columns = [solve_exact(low, high, [Q(i == j) for i in range(n)], bandwidth)
               for j in border]
    z = list(map(list, zip(*columns)))
    k = [[Q(i == j)+sum((v[i][l]*z[l][j] for l in support), Q(0))
          for j in range(len(border))] for i in range(len(border))]
    ki = inverse_exact(k)
    return dict(low=prepare_triangle(low, h, False, inverse_exact, bits),
                high=prepare_triangle(high, h, True, inverse_exact, bits),
                v=grid([[row[j] for j in support] for row in v], bits),
                support=support, z=grid(z, bits), ki=grid(ki, bits),
                h=h, bits=bits, metadata=metadata)


def solve(table, b, count):
    h, bits = table['h'], table['bits']
    y = triangle(table['low'], b, count)
    x = triangle(table['high'], y, count)
    if not table['support']:
        return x
    vb = product(table['v'], [x[j] for j in table['support']], h, count, bits)
    c = product(table['ki'], vb, h, count, bits)
    correction = product(table['z'], c, h, count, bits)
    return grid(add(x, correction, -1), bits)


def counter():
    return dict(scalar_products=0, scalar_additions=0, tiles=0)


def compile_coupling(a, row_groups, col_groups, h, bits):
    """Offline cell-local sparse pages; reject an edge outside its named cell."""
    assert len(row_groups) == len(col_groups)
    pages, covered = [], set()
    for rows, cols in zip(row_groups, col_groups):
        rr = [i for i in rows if any(a[i][j] for j in cols)]
        cc = [j for j in cols if any(a[i][j] for i in rows)]
        assert len(rr) <= h and len(cc) <= h
        for i in rows:
            for j in cols:
                if a[i][j]:
                    assert (i, j) not in covered
                    covered.add((i, j))
        if rr and cc:
            pages.append(dict(rows=rr, cols=cc, values=grid([[a[i][j] for j in cc] for i in rr], bits)))
    assert covered == {(i, j) for i, row in enumerate(a) for j, x in enumerate(row) if x}
    assert len({i for page in pages for i in page['rows']}) == sum(len(p['rows']) for p in pages)
    return dict(pages=pages, n=len(a), h=h, bits=bits)


def coupling(table, b, count):
    out = zeros(table['n'], len(b[0]))
    for page in table['pages']:
        values = product(page['values'], [b[j] for j in page['cols']],
                         table['h'], count, table['bits'])
        for i, row in zip(page['rows'], values):
            out[i] = row
    return out
