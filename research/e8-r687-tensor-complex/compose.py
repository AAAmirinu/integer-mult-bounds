"""Exact composition of the R687 bit supplier (research/e8-r687-read-then-climb) with PR #471's complex supplier
(research/e8-tensor-normalization: #449 kernel79, full-nine-axis normalisation, same-owner spectator borrowing; Dugongue).
The composition IS PR #471's own assembler (code/assemble.py, unchanged): two exact moments per supplier, both suppliers'
finite invoices (bit: PR #471's product-bound prefix and row bound; complex: #471's stock, router and literal invoices and
row bound), the six-level bootstrap and #434's 47 strict outer inequalities with next-grid and parameter controls.  Only its
bit inputs are replaced by the R687 supplier's eleven-stage whole-residual outputs.
  LIGHT: the inputs are the pinned evidence/ files (the bit supplier's GLOBAL/AUDIT and a geometry summary; the complex
         supplier's GLOBAL/AUDIT produced by code/complex471.py from PR #471's unchanged code); their hashes are checked against
         the bit package's EXPECTED.json and against EXPECTED.json here.
  FULL:  the inputs come from fresh runs (the bit package's verify.py and code/complex471.py).
usage: compose.py OUT_DIR --bit-v DIR --complex DIR      (DIR = .../eleven/mixed_d3 and .../complex)
Prepared by DreamingOfClouds with Claude Opus 5.5 (Anthropic), via Claude Code.  Apache-2.0."""
from pathlib import Path
import argparse, json, os, subprocess, sys
ROOT = Path(__file__).resolve().parent; RES = ROOT.parent; P471 = RES / 'e8-tensor-normalization'
ap = argparse.ArgumentParser(); ap.add_argument('out', type=Path); ap.add_argument('--bit-v', type=Path, required=True); ap.add_argument('--complex', type=Path, required=True)
a = ap.parse_args(); out = a.out.resolve(); out.mkdir(parents=True, exist_ok=True)
read = lambda p: json.loads(Path(p).read_text())
K473 = '1295629942587122/1000000000000000000'      # PR #473 (rohanarun): lemma-less frontier at submission
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONINTMAXSTRDIGITS='0', PYTHONUTF8='1',
           PYTHONPATH=os.pathsep.join(map(str, [P471 / 'vendor/runtime', P471 / 'vendor/complex', P471 / 'code']))); env.pop('PYTHONOPTIMIZE', None)
v = a.bit_v.resolve()
cmd = [sys.executable, '-B', P471 / 'code/assemble.py', v, v / 'hosted', v / 'hosted/AUDIT.json', out / 'ASSEMBLY.json', '--complex', a.complex.resolve(),
       '--engines', P471 / 'engines', '--inherited', P471 / 'inherited', '--route-extra', 3, '--label', 'PR473', '--parent-kappa', K473]
with (out / 'assemble.log').open('w') as f: q = subprocess.run(list(map(str, cmd)), env=env, stdout=f, stderr=subprocess.STDOUT)
assert q.returncode == 0, (out / 'assemble.log').read_text()[-4000:]
r = read(out / 'ASSEMBLY.json')
from fractions import Fraction as Q
C715, K471, K463 = Q(642564369945714399381, 5 * 10 ** 23), Q(1274548075945587, 10 ** 18), Q(641739651875561, 5 * 10 ** 17)
res = dict(status='PASS_R687_TENSOR_COMPLEX_COMPOSITION', kappa=r['kappa'], kappa_decimal=r['kappa_decimal'], binding_component=r['binding_component'],
           bit_lower=r['bit_lower'], complex_lower=r['complex_lower'], bit_only_kappa=r['bit_only_kappa'],
           gain_over_pr473_percent=r['gain_over_reference_percent'], gain_over_pr471_percent=float(100 * (Q(r['kappa']) / K471 - 1)),
           gain_over_pr463_percent=float(100 * (Q(r['kappa']) / K463 - 1)), bit_c_gain_over_r715_percent=float(100 * (Q(r['bit_lower']) / C715 - 1)),
           strict_constraints=len(r['strict_outer_constraints']), outer_controls=r['outer_controls'], external_row_allowance=r['external_row_allowance'],
           bit=r['bit'], complex=dict((k, r['complex'][k]) for k in ('live', 'physical', 'maxchild', 'rank_mass', 'hosted_residuals', 'physical_stock_bits', 'router_bits', 'literal_bits', 'row_coefficient', 'local_bound')),
           bit_profile=r['bit_profile'], complex_profile=r['complex_profile'], bit_template_sha256=r['bit_template_sha256'], complex_template_sha256=r['complex_template_sha256'],
           emitted_program_sha256=r['emitted_program_sha256'])
(out / 'RESULT.json').write_text(json.dumps(res, indent=2) + '\n')
print(res['kappa_decimal'], res['binding_component'], 'vs #473 %+.4f%%' % res['gain_over_pr473_percent'])
