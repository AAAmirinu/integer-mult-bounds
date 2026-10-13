#!/usr/bin/env python3
"""Check that every assembly in the repository keeps the reduction behind the square-root wall.

Standard library only.  Usage:  python3 -B research/sqrt-log-wall/wall_check.py [repository-root]

The script checks the source text, not a model of it:

1. the manuscript assembly (upstream/build/sections/08-assembly.tex) contains the d-axis box, the ell
   simultaneous butterfly rounds, the axis-by-axis Gaussian line maps, the d-term chirp numerators, and the
   dimension (saving eps) and scalar-work (saving 1-eps-delta) rows of its cost table;
2. each of the nine notes/*-assembly.tex files lists both margins and its boxed kappa;
3. every research outer engine (research/**/outer.py defining `margins=dict(`) has the margins
   `dimension=eps` and `scalar_work=1-eps-delta` and requires every margin to exceed kappa;
4. the selected record (certificates/selected-result.json) is re-derived from its certificate's outer table:
   eps and delta are recovered exactly from the two margin gaps, and kappa < min(eps, 1-eps-delta) <= (1-delta)/2
   and kappa < eps*q < q/(1+q) < 1/2 are checked in exact rational arithmetic;
5. the box inequality d + ell >= 2 sqrt(log2 T), with ell = ceil(log2 T / d), is checked exhaustively for
   log2 T <= 4096.

Any failure exits with status 1.
"""
import json
import math
import re
import sys
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
FAIL = []


def norm(text):
    return re.sub(r'\s+', ' ', text)


def need(ok, message):
    print(('PASS ' if ok else 'FAIL ') + message)
    if not ok:
        FAIL.append(message)


def frac(text):
    """parse 'p/q', a decimal string, or an int into an exact Fraction"""
    return Q(str(text))


# 1. the manuscript's reduction ------------------------------------------------------------------------------
MANUSCRIPT = 'upstream/build/sections/08-assembly.tex'
REDUCTION = [
    ('box volume Tp = Theta(n)', r'Tp=\Theta(n)'),
    ('box axis lengths t_i in {r/2, r} with product T', r't_i\in\{r/2,r\},\qquad \prod_i t_i=T'),
    ('box axis bound r = 2^ell', r'r=2^{\lceil(\log_2T)/d\rceil}$ and $\ell=\log_2r'),
    ('one pass per butterfly level: ell simultaneous rounds', r'For the at most $\ell$ simultaneous rounds'),
    ('one pass per axis: Gaussian lines processed axis by axis', r'axis $i$ has at most $T/t_i$ processed lines'),
    ('chirp numerators are sums of d terms', r'sums of $d$ terms'),
    ('cost row: simultaneous butterfly rounds, saving eps(1-lambda\')',
     r"Simultaneous butterfly rounds & $\ell d^{\lambda'}$ & $1-\epsilon(1-\lambda')$"),
    ('cost row (dimension): packed polynomial products, saving eps',
     r'Packed polynomial products & $\log(rp)$ & $1-\epsilon$'),
    ('cost row (scalar work): chirps, twists and scalar products, saving 1-eps-delta',
     r'Chirps, twists and scalar products & $dp^\delta$ & $\epsilon+\delta$'),
    ('margin list contains g_6 = 1-delta-eps and g_7 = eps', r'g_6&=1-\delta-\epsilon,\qquad g_7=\epsilon.'),
    ('parameters: delta = 1/16, C_1 = 20, eps C_1 < 1, kappa = 2^-182',
     r'C_1=20,\qquad \epsilon=2^{-75},\qquad \kappa=2^{-182}'),
]
text = norm((ROOT / MANUSCRIPT).read_text())
for label, pattern in REDUCTION:
    need(norm(pattern) in text, f'manuscript: {label}')
need(norm(r'\epsilon<\frac1{12},\quad \epsilon C_1<1') in text, 'manuscript: eps C_1 < 1, so kappa < eps < 1/C_1 = 1/20')

# 2. the nine assembly notes ----------------------------------------------------------------------------------
NOTES = {
    # name: (dimension-margin text, scalar-work-margin text, boxed kappa text, kappa)
    'batched': (r'g_7&=\epsilon.', r'g_6&=1-\delta-\epsilon', r'\kappa=\frac{6149999}{5\cdot10^{13}}',
                Q(6149999, 5 * 10**13)),
    'copied-centers': (r'1-\epsilon-\delta,\quad\epsilon.', r'1-\epsilon-\delta,\quad\epsilon.',
                       r'\kappa=\frac{384569}{10000000000}', Q(384569, 10**10)),
    'endpoint-gauge': (r'g_7&=\epsilon.', r'g_6&=1-\delta-\epsilon', r'\kappa=\frac{119723}{20000000000}',
                       Q(119723, 2 * 10**10)),
    'paired-cube': (r'1-\epsilon-\delta,\ \epsilon.', r'1-\epsilon-\delta,\ \epsilon.',
                    r'\kappa=\frac{4609169}{10000000000}', Q(4609169, 10**10)),
    'partial-gauge': (r'1-\epsilon-\delta,\quad\epsilon.', r'1-\epsilon-\delta,\quad\epsilon.',
                      r'\kappa=\frac{7237}{78125000}', Q(7237, 78125000)),
    'partial-swap': (r'g_7&=\epsilon.', r'g_6&=1-\delta-\epsilon', r'\kappa=\frac{942293}{500000000000}',
                     Q(942293, 5 * 10**11)),
    'stopped-product': (r'1-\epsilon-\delta,\quad\epsilon.', r'1-\epsilon-\delta,\quad\epsilon.',
                        r'\kappa=\frac{194869}{2500000000}', Q(194869, 25 * 10**8)),
    'structured-bulk': (r'\text{dimension}&\epsilon', r'\text{scalar work}&1-\epsilon-\delta',
                        r'\kappa=\frac{2504683}{200000000000}', Q(2504683, 2 * 10**11)),
    'three-stage-cover': (r'1-\epsilon-\delta,\ \epsilon.', r'1-\epsilon-\delta,\ \epsilon.',
                          r'\kappa=\frac{3146011}{10000000000}', Q(3146011, 10**10)),
}
best_note = (Q(0), None)
for name, (dim_text, scalar_text, kappa_text, kappa) in NOTES.items():
    body = norm((ROOT / 'notes' / f'{name}-assembly.tex').read_text())
    ok = norm(dim_text) in body and norm(scalar_text) in body and norm(kappa_text) in body
    need(ok and kappa < Q(1, 2), f'notes/{name}-assembly.tex: dimension and scalar-work margins present, '
                                 f'kappa = {float(kappa):.6e} ({float(Q(1, 2) / kappa):,.0f}x below 1/2)')
    best_note = max(best_note, (kappa, name))

# 3. the research outer engines -------------------------------------------------------------------------------
engines = sorted(p for p in (ROOT / 'research').rglob('outer.py') if 'margins=dict(' in p.read_text())
bad = []
for path in engines:
    body = re.sub(r'\s+', '', path.read_text())
    if not ('dimension=eps' in body and 'scalar_work=1-eps-delta' in body
            and "slacks.update({name+'_above_kappa':val-kappafor" in body):
        bad.append(str(path.relative_to(ROOT)))
need(engines and not bad, f'research outer engines: {len(engines)} define margins; every one has dimension=eps, '
                          f'scalar_work=1-eps-delta and margin-above-kappa slacks' + (f'; missing in {bad}' if bad else ''))

# 4. the selected record, re-derived from its certificate -----------------------------------------------------
selected = json.loads((ROOT / 'certificates/selected-result.json').read_text())
kappa = frac(selected['kappa'])
cert = json.loads((ROOT / selected['certificate']).read_text())
outer = cert['outer']
need(frac(cert['kappa']) == kappa, f'selected record: certificate kappa equals selected kappa {float(kappa):.15f}')
dimension_gap = frac(outer['dimension_above_kappa'])
scalar_gap = frac(outer['scalar_work_above_kappa'])
layer_gap = frac(outer['compact_phase_layer_above_kappa'])
eps = kappa + dimension_gap                 # dimension margin = eps
scalar = kappa + scalar_gap                 # scalar-work margin = 1 - eps - delta
delta = 1 - eps - scalar
q = (kappa + layer_gap) / eps               # compact phase-layer margin = eps * q
need(dimension_gap > 0 and scalar_gap > 0 and delta > 0,
     f'selected record: eps = {float(eps):.9f}, delta = {float(delta):.3e} > 0 recovered from the two margin gaps')
need(kappa < min(eps, scalar) <= (1 - delta) / 2 < Q(1, 2),
     f'selected record: kappa < min(eps, 1-eps-delta) <= (1-delta)/2 = {float((1 - delta) / 2):.9f} < 1/2')
need(0 < q < 1 and kappa < eps * q < q / (1 + q) < Q(1, 2),
     f'selected record: network side kappa < eps*q < q/(1+q) = {float(q / (1 + q)):.6e} with q = {float(q):.6e}')

# 5. the box inequality -------------------------------------------------------------------------------------------
worst = min(Q(d + -(-k // d)) / Q(math.isqrt(4 * k * 10**12), 10**6) for k in range(1, 4097) for d in range(1, k + 1))
need(all(d + -(-k // d) >= 2 * math.sqrt(k) for k in range(1, 4097) for d in range(1, k + 1)),
     f'box: d + ceil(log2 T / d) >= 2 sqrt(log2 T) for every log2 T <= 4096 and every d (min ratio {float(worst):.4f})')

print()
print(f'largest tex-assembly kappa: notes/{best_note[1]}-assembly.tex, {float(best_note[0]):.6e}')
print(f'selected record kappa: {float(kappa):.12e} ({float(Q(1, 2) / kappa):,.0f}x below 1/2)')
if FAIL:
    print(f'{len(FAIL)} check(s) failed')
    sys.exit(1)
print('PASS_SQUARE_ROOT_WALL_REDUCTION')
