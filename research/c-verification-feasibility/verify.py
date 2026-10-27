"""Scoped fresh checks. This command does not admit a performance improvement."""
from hashlib import sha256
import json
from pathlib import Path
import runpy
import sys
from portable import prepared, require

HERE = Path(__file__).resolve().parent
require(len(sys.argv) == 2 and sys.argv[1] in ('baseline', 'integer', 'rational'), 'explicit finite scope')
mode = sys.argv[1]
manifest = json.loads((HERE / 'CODE-SOURCES.json').read_text())
for name, digest in manifest.items():
    path = HERE / name
    require(not path.is_symlink() and sha256(path.read_bytes()).hexdigest() == digest,
            'exact qualified prototype source: ' + name)
with prepared(mode) as (root, baseline, stage):
    if mode == 'baseline':
        sys.path.insert(0, str(baseline))
        sys.argv = [str(baseline / 'verify.py')]
        runpy.run_path(sys.argv[0], run_name='__main__')
    elif mode == 'integer':
        sys.path.insert(0, str(stage))
        sys.argv = [str(stage / 'finite_probe.py'), '--source-sha256', manifest['integer/integer_format.c']]
        runpy.run_path(sys.argv[0], run_name='__main__')
    else:
        sys.path.insert(0, str(stage))
        from finite_probe import main
        main(stage / 'package', micro=False)
        import arithmetic_binding as binding
        from fractions import Fraction as F
        token = binding.bind()
        require(token is not None, 'original arithmetic binding')
        F.__del__ = lambda self: None
        try:
            require(binding.bind() is None and not binding.fresh(token), 'destructor drift rejects')
        finally:
            del F.__del__
        print('PASS_ADDED_DESTRUCTOR_BINDING_CONTROL')
print('PASS_C_VERIFICATION_SCOPED_FINITE ' + mode)

