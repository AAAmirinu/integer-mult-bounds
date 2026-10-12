#!/usr/bin/env python3
"""Piece-count remark (note 4, section 3): no profile family with many paid pieces per live role reaches kappa -> 1.

Moment equation (as in the hub's moment engines, without the 1e-16 bad-class term, which only lowers a):
    F_P(a) = sum_children (r/(mW)) (m/r)^a = 1.
F_P is increasing in a, so F_P(a_up) >= 1 certifies a <= a_up; certificates use mpmath interval arithmetic.
Extremal facts (proofs in notes/4-loss-chain.md):
  E2  with n children, mass S, ranks in [1, rbar]: sum r^(1-a) >= y + x rbar^(1-a), x = (S-n)/(rbar-1), y = n - x
      (chord / LP dual; the two-point profile is extremal);
  E3  mass M in children of rank <= rbar: sum r^(1-a) >= M rbar^(-a);
  E4  a <= delta / Lambda, Lambda = sum p_r ln(m/r).
Outputs: Theorem 4 values a <= (m-1)/((m nu + 1) ln m); the copy-free window-h values under H6; E2 chord certificates.
Derived from the kappa-push ceiling script; the frozen-word and E8-architecture tables are omitted here because
#595 (research/format-limits) supersedes them within its scope.
"""
from fractions import Fraction as Fr
import mpmath as mp
from mpmath import iv, mpf, log

mp.mp.dps = 40
iv.dps = 40

def Fgen(terms, m, W, a, ctx=mp):
    """terms: list of (rank, count) with count possibly fractional (Fraction/float).  Returns F(a)."""
    m_ = ctx.mpf(m); a_ = a
    s = 0
    for r, n in terms:
        nn = ctx.mpf(n.numerator) / n.denominator if isinstance(n, Fr) else ctx.mpf(n)
        s += nn * (ctx.mpf(r) / m_) ** (1 - a_)
    W_ = ctx.mpf(W.numerator) / W.denominator if isinstance(W, Fr) else ctx.mpf(W)
    return s / W_

def root(terms, m, W, lo=0, hi=1):
    lo, hi = mpf(lo), mpf(hi)
    for _ in range(160):
        mid = (lo + hi) / 2
        if Fgen(terms, m, W, mid) < 1: lo = mid
        else: hi = mid
    return hi

def certify_upper(terms, m, W, a_up):
    """True iff interval F(a_up) >= 1, i.e. every profile dominated by `terms` has a <= a_up."""
    A = iv.mpf(str(a_up))
    val = Fgen(terms, m, W, A, ctx=iv)
    return val.a >= 1

def certify_lower(terms, m, W, a_lo):
    A = iv.mpf(str(a_lo))
    val = Fgen(terms, m, W, A, ctx=iv)
    return val.b < 1

def bracket(terms, m, W):
    """root, rounded outward at 1e-15 relative and interval-certified on both sides."""
    a = root(terms, m, W)
    up = a * (1 + mpf('1e-15')); lo = a * (1 - mpf('1e-15'))
    ok = certify_upper(terms, m, W, up) and certify_lower(terms, m, W, lo)
    return a, up, ok

def two_point(n, S, rbar):
    """Extremal two-point profile (E2): x children of rank rbar, y of rank 1 (fractional counts)."""
    n, S = Fr(n), Fr(S)
    assert n <= S <= n * rbar, (n, S, rbar)
    x = (S - n) / (rbar - 1); y = n - x
    return [(1, y), (rbar, x)]

def first_order(H, m, W):
    S = sum(r*n for r, n in H.items()); D = m*W - S
    delta = mpf(D) / (m*W)
    Lam = sum(mpf(r*n)/(m*W) * log(mpf(m)/r) for r, n in H.items())
    return delta / Lam

def arch_sup(h, K, rho, muhat, rloc):
    """Hosted compressed architecture, per data line: copy ratio rho = cst/v, local mass per line per invocation muhat,
    local pieces of rank <= rloc (E3), idle pieces <= m.  v cancels.  Returns certified sup root or None."""
    v = 1
    L = 2*K + 1; m = 1 + L*(h-1); W = Fr(2*K); D = W - L*Fr(rho)
    mu = Fr(muhat)
    I = m*W - D - L*mu
    if D <= 0: return None
    if I < 0: W = W - I/m; I = 0        # fractional banks, extremal as in word_terms
    terms = [(rloc, L*mu/rloc)]
    if I > 0: terms.append((m, I/m))
    a, up, ok = bracket(terms, m, W)
    assert ok
    return up

def best_over_K(h, rho, muhat, rloc, Ks=range(1, 13)):
    best = None
    for K in Ks:
        up = arch_sup(h, K, rho, muhat, rloc)
        if up is not None and (best is None or up > best[1]): best = (K, up)
    return best

def table_absolute():
    print("=" * 110)
    print("T5  Theorem 4 (thin labels, D <= W, n >= (1+nu) W):  a <= (m-1)/((m*nu+1) ln m) < 1/(nu ln m);  kappa < a/(1+a)")
    print("=" * 110)
    for nu in (1, 2, Fr(25, 10), 5, 10, Fr(347, 10)):
        line = []
        for m in (4, 10, 25, 41, 73, 145, 1000, 10**6):
            a = mpf(m-1) / ((m*mpf(nu.numerator if isinstance(nu, Fr) else nu)/(nu.denominator if isinstance(nu, Fr) else 1) + 1) * log(m))
            line.append(f"m={m}:{mp.nstr(a, 3)}")
        print(f"   nu={float(nu):5.1f}: " + "  ".join(line))

def check_chord(m=73, rbar=8, a='0.0013453'):
    """E2 is the LP  min sum_r n_r r^(1-a)  s.t. sum n_r = n, sum r n_r = S, n_r >= 0 (r = 1..rbar).
    Dual certificate: alpha + beta r <= r^(1-a) on 1..rbar with equality at r = 1, rbar.  Verified in interval arithmetic."""
    A = iv.mpf(a)
    f = lambda r: iv.mpf(r) ** (1 - A)
    beta = (f(rbar) - f(1)) / (rbar - 1); alpha = f(1) - beta
    ok = all((f(r) - (alpha + beta*r)).a >= -iv.mpf('1e-35') for r in range(1, rbar+1))
    print(f"LP dual (chord) certificate for E2 at m={m}, rbar={rbar}, a={a}: {'valid' if ok else 'FAILED'}")
    return ok


def table_copy_free():
    print("Copy-free limit (rho = cst/v = 0, so D/W = 1) under H6: local mass per line >= 2(h-1), local pieces <= h,")
    print("idle pieces <= m, max over K = 1..12 (certified upper bounds on a):")
    vals = []
    for h in (2, 3, 4, 8, 9, 16, 64, 128):
        b = best_over_K(h, Fr(0), 2*(h-1), h)
        vals.append((h, b[1]))
        print(f"   h={h:3d}: a <= {mp.nstr(b[1], 4)} (K={b[0]})   (h-1)*a = {mp.nstr((h-1)*b[1], 4)}")
    assert all(vals[i][1] > vals[i+1][1] for i in range(len(vals)-1))
    return vals

if __name__ == '__main__':
    table_absolute()
    table_copy_free()
    assert check_chord() and check_chord(78, 56, '0.0015654') and check_chord(73, 48, '0.0016153')
    print("PASS Theorem 4 table, copy-free decay (monotone in h) and E2 chord certificates")
