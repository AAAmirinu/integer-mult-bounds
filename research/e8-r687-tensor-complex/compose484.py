"""Composition of the R687 bit supplier with our draft PR #484's complex supplier (research/e8-complex-gauge-kernel, gauge80 +
kernel42; conditional on its Lemmas A and G), CITED from #484's pinned full-run result (evidence/pr484; a full run at #484 head d30a05f, manifest pinned in SOURCE.json), as #484's own assembler
composes external bit suppliers: the outer assembly below is #484's code/assemble_gk.py per-supplier loop, unchanged in substance
(six-level bootstrap with the supplier's charged two-level coefficient, row allowance max(20161, bit row, complex row),
#434's 47 strict outer inequalities, next-grid and parameter controls), on PR #443's pinned engines.
The bit inputs (c, charged two-level coefficient bits, row coefficient) are the R687 supplier's own assembly fields.
usage: compose484.py BIT_RESULT.json OUT.json.   Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util, json, sys
ROOT = Path(__file__).resolve().parent; RES = ROOT.parent
bitr, outp = json.loads(Path(sys.argv[1]).read_text()), Path(sys.argv[2])
cx = json.loads((ROOT / 'evidence/pr484/RESULT-gauge80-kernel42.json').read_text()); rc = json.loads((ROOT / 'evidence/pr484/RECEIPT.json').read_text())
assert rc['status'] == 'PASS_FULL_COMPLEX_GAUGE_KERNEL_COMPOSITION' and rc['complex_lower'] == cx['complex_lower']
pin = json.loads((ROOT / 'SOURCE.json').read_text())['complex_cited']
assert rc['manifest_sha256'] == pin['manifest_sha256'], ('pinned #484 receipt is not from the pinned head', rc['manifest_sha256'])
def load(n):
    sp = importlib.util.spec_from_file_location('c484_' + n, RES / 'e8-r740-replica32/code/engines' / (n + '.py')); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
Outer = load('outer')
b = Q(cx['complex_lower']); rowc = int(cx['complex']['row_coefficient'])
c = Q(bitr['bit_lower']); two_bits = int(bitr['bit']['charged_two_level_coefficient_bits']); row = int(bitr['bit']['row_coefficient'])
assert bitr['halving_depth'] == 3 and int(bitr['bit']['two_level_coefficient_bits']) <= two_bits
eta = beta = Q(1, 10 ** 18); grid = Q(1, 10 ** 18); ALLOW = max(20161, row, rowc)
def ceil(x): return -((-x.numerator) // x.denominator)
s = min(c, (1 - beta) * b) - Q(1, 10 ** 24); assert 0 < s < c and s < (1 - beta) * b
chain = [Q(384599, 10 ** 10)]; cutoffs = []
for j in range(6):
    old = chain[-1]; a = (1 - s) * s + s * old
    gap = min(s - a, 1 - a - s, 1 - a - s * (1 - old), 1 - s); assert old < a < s < 1 - a and gap > 0
    cutoff = max(ceil(36 / gap ** 2), ceil(2 * (4 + two_bits) / gap)); assert cutoff * gap ** 2 >= 36 and cutoff * gap >= 2 * (4 + two_bits)
    cutoffs.append(dict(gap=str(gap), cutoff_log2=str(cutoff))); chain.append(a)
q = chain[-1] * (1 - 2 * eta); margin = (1 - eta) * q / (1 + q); ticks = margin / grid; k = grid * ((ticks.numerator - 1) // ticks.denominator)
bridge = {'semantic': {'C0': {'base': 2, 'exponent': 210000}, 'strict_literal_gap': 1}, 'rows': {'degree_gap': Q(10 ** 6) - Q(51 * ALLOW, 25)}}
asm = Outer.assembly(chain[-1], b, bridge, k, eta=eta, beta=beta)
assert len(asm['strict_constraints']) == 47 and all(x > 0 for x in asm['strict_constraints'].values())
controls = []
for name, kk, ee, bb in [('next_grid', k + grid, eta, beta), ('zero_eta', k, Q(0), beta), ('zero_beta', k, eta, Q(0)), ('unit_beta', k, eta, Q(1))]:
    try: Outer.assembly(chain[-1], b, bridge, kk, eta=ee, beta=bb)
    except AssertionError: controls.append(name)
    else: raise AssertionError(name)
K493_484 = Q(662515748707749, 5 * 10 ** 17); K473 = Q(1295629942587122, 10 ** 18); K483 = Q(1296606691405309, 10 ** 18)
res = dict(status='PASS_R687_PR484_CITED_COMPOSITION', kappa=str(k), kappa_decimal=format(float(k), '.18f'), bit_lower=str(c), complex_lower=str(b),
           binding_component='bit' if c < (1 - beta) * b else 'complex', external_row_allowance=ALLOW, charged_coefficient_bits=two_bits,
           gain_over_pr483_percent=float(100 * (k / K483 - 1)), gain_over_pr473_percent=float(100 * (k / K473 - 1)), vs_pr493_with_pr484_percent=float(100 * (k / K493_484 - 1)),
           complex_template_sha256=cx['complex_template_sha256'], complex_scope='PR #484 draft: conditional on its Lemmas A and G; cited from its pinned full-run result, not rebuilt here',
           bootstrap=cutoffs, strict_outer_constraints={n: str(x) for n, x in asm['strict_constraints'].items()}, outer_controls=controls)
outp.write_text(json.dumps(res, indent=2) + '\n'); print(res['kappa_decimal'], res['binding_component'], 'vs #483 %+.4f%%' % res['gain_over_pr483_percent'], 'vs #493+#484 %+.4f%%' % res['vs_pr493_with_pr484_percent'])
