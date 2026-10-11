"""External, exact-hash-bound optimizations for the pinned PR358 proofs.

All original checks run. Only gx.scal, pure frame predicates, and canonical
transcript encodings change. Frozen manifests and source files are untouched.
"""
import argparse
import ast
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import runpy
import sys
import time

from fast_transcript import LineEncoder, integer_triple
from integer_factors import replay_factors

ROOT = Path(__file__).resolve().parent
PROFILE = ROOT.parent / 'e8-pipeline-profile'
SOURCE = PROFILE / 'pr358-source'
PREDECESSOR = SOURCE / 'vendor/predecessor'
SHARING = ROOT.parent / 'producer-prefix-sharing'
SCALAR_PACKAGE = ROOT.parent / 'verification-performance/research/gcert-scalar-performance'
PINS = {
    'vendor/predecessor/verify.py': 'b0d2a2cf1e348545dbace3c5f3e98b1c91c1f7773969decdc76ca4240c174599',
    'vendor/predecessor/code/complex_splice.py': 'b1b4847652a9968d7afb8dd529bc371b656afa240f2e393f03c187dca250c4ce',
    'vendor/predecessor/scalar_check.py': '520c4549de9200811dd594d15cdf73de28f287b04778965491b2c5b3f6d6ed5a',
    'vendor/predecessor/bitword/references/pr168-v4/research/paired-cube-bit/check_paired_cube_bit.py': '4d7c86cd999a1519e0dfb6dcf33a8f26e442a353c3665a0f06881216a260fbf3',
    'vendor/predecessor/inputs/complex/sources/tools__gx__gx.py': '6f3dc8bb639933227a8dae181ec4a542e85c7276be9c9e330f49518e7b630b95',
    'vendor/predecessor/bank_check.py': 'b67d1e5870239a456a732caa8e56b836d3fa472f451790700276ce706bed1da8',
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def checked_tree(path, digest):
    if sha(path) != digest:
        raise ValueError('unsupported source bytes: ' + str(path))
    return ast.parse(Path(path).read_text())


class TranscriptCalls(ast.NodeTransformer):
    def __init__(self):
        self.count = 0

    def visit_Call(self, node):
        expected = "(json.dumps(x, separators=(',', ':')) + '\\n').encode()"
        template = ast.parse(expected, mode='eval').body
        # Only the expression's payload varies at the four pinned call sites.
        if (isinstance(node.func, ast.Attribute) and node.func.attr == 'encode'
                and isinstance(node.func.value, ast.BinOp)):
            candidate = node.func.value.left
            if isinstance(candidate, ast.Call) and candidate.args:
                template.func.value.left.args[0] = candidate.args[0]
                if ast.dump(node) == ast.dump(template):
                    self.count += 1
                    return ast.copy_location(ast.Call(
                        func=ast.Name(id='_transcript_line_'+str(self.count-1), ctx=ast.Load()),
                        args=candidate.args, keywords=[]), node)
        return self.generic_visit(node)


def replace_validate(module, path, digest, lines):
    tree = checked_tree(path, digest)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'validate')
    change = TranscriptCalls()
    fn = change.visit(fn)
    if change.count != 4:
        raise ValueError('expected exactly four transcript encoding calls')
    assert len(lines)==4
    for i,line in enumerate(lines):
        module.__dict__['_transcript_line_'+str(i)] = line
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), str(path), 'exec'), module.__dict__)


def replace_projection(module, path, digest):
    tree = checked_tree(path, digest)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'replay_projection')
    old = ast.parse("json.dumps([a,b,c], separators=(',', ':')).encode()", mode='eval').body
    class Replace(ast.NodeTransformer):
        count = 0
        def visit_Call(self, node):
            if ast.dump(node) == ast.dump(old):
                self.count += 1
                return ast.copy_location(ast.Call(func=ast.Name(id='_integer_triple', ctx=ast.Load()),
                    args=[ast.Tuple(elts=[ast.Name(id=x,ctx=ast.Load()) for x in ('a','b','c')],ctx=ast.Load())], keywords=[]), node)
            return self.generic_visit(node)
    change = Replace()
    fn = change.visit(fn)
    if change.count != 1:
        raise ValueError('expected one scalar event encoding call')
    module.__dict__['_integer_triple'] = integer_triple
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),module.__dict__)


def replace_factors(module,path,digest):
    tree=checked_tree(path,digest)
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
    expected=ast.parse("""
replay=[list(map(Q,row))for row in B]
for op,i,j,a,b in ops:
    if op=='swap':replay[i],replay[j]=replay[j],replay[i]
    elif op=='scale':replay[i]=[Q(a,b)*x for x in replay[i]]
    else:
        assert op=='add';replay[i]=[x+Q(a,b)*y for x,y in zip(replay[i],replay[j])]
""").body
    count=0
    for loop in ast.walk(fn):
        if not isinstance(loop,ast.For):continue
        for i in range(len(loop.body)-1):
            if all(ast.dump(loop.body[i+k])==ast.dump(n) for k,n in enumerate(expected)):
                loop.body[i:i+2]=ast.parse('replay=_factor_replay(B,ops)').body
                count+=1
                break
    if count!=1:raise ValueError('expected exactly one original rational factor replay')
    module.__dict__['_factor_replay']=replay_factors
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),str(path),'exec'),module.__dict__)


class Optimizations:
    def __init__(self, mode='all'):
        self.mode = mode
        self.encoders = []
        self.memoized = []
        self.loaded = []
        self.original_spec = importlib.util.spec_from_file_location
        self.dot = None

    def patch(self, module, path):
        relative = path.relative_to(SOURCE).as_posix()
        if relative not in PINS:
            return
        checked_tree(path, PINS[relative])
        self.loaded.append(relative)
        if relative.endswith('/tools__gx__gx.py'):
            # Independent check that only scal differs in the earlier utility.
            old = ast.parse((SCALAR_PACKAGE/'reference/gx.py').read_text())
            new = ast.parse((SCALAR_PACKAGE/'gx_fast.py').read_text())
            assert sha(SCALAR_PACKAGE/'reference/gx.py') == PINS[relative]
            without = lambda t: ast.dump(ast.Module(body=[n for n in t.body if not (isinstance(n,ast.FunctionDef) and n.name=='scal')],type_ignores=[]))
            assert without(old) == without(new)
            fn = next(n for n in new.body if isinstance(n,ast.FunctionDef) and n.name=='scal')
            exec(compile(ast.Module(body=[fn],type_ignores=[]),str(SCALAR_PACKAGE/'gx_fast.py'),'exec'),module.__dict__)
        elif relative.endswith('/complex_splice.py') and self.mode == 'all':
            # Whole events/projection pairs are mostly distinct. Cache only
            # elementary primitive lines, which repeat heavily within controls.
            encoders = [LineEncoder(maxsize=0) for _ in range(3)]+[LineEncoder(maxsize=131072)]
            self.encoders.extend(encoders)
            replace_validate(module,path,PINS[relative],[x.line for x in encoders])
            original = module.contains
            cached = lru_cache(maxsize=65536)(original)
            module.contains = lambda u,v: cached(tuple(u),tuple(v))
            self.memoized.append(('binary_containment',cached))
        elif relative.endswith('/scalar_check.py') and self.mode == 'all':
            replace_projection(module,path,PINS[relative])
        elif relative.endswith('/bank_check.py') and self.mode == 'all':
            replace_factors(module,path,PINS[relative])
        elif relative.endswith('/check_paired_cube_bit.py') and self.mode == 'all':
            # Multiple fresh backend imports have the same pinned pure dot.
            # Intern rows by content so pair keys do not retain duplicate row
            # tuples. No frame id, state, chronology or proof result is cached.
            if self.dot is None:
                original = module.dot
                rows = lru_cache(maxsize=65536)(lambda row:row)
                cached = lru_cache(maxsize=131072)(original)
                self.dot = lambda a,b: cached(rows(tuple(a)),rows(tuple(b)))
                self.memoized.extend([('integer_dot',cached),('interned_integer_rows',rows)])
            module.dot = self.dot

    def install(self):
        owner = self
        def specification(name, location, *args, **kw):
            spec = owner.original_spec(name,location,*args,**kw)
            path = Path(location).resolve()
            if spec is not None and path.is_relative_to(SOURCE) and path.relative_to(SOURCE).as_posix() in PINS:
                original = spec.loader
                class Loader:
                    def create_module(self,specification):
                        return original.create_module(specification)
                    def exec_module(self,module):
                        original.exec_module(module)
                        owner.patch(module,path)
                spec.loader = Loader()
            return spec
        importlib.util.spec_from_file_location = specification

    def restore(self):
        importlib.util.spec_from_file_location = self.original_spec

    def statistics(self):
        return dict(loaded=self.loaded, transcript_caches=[x.statistics() for x in self.encoders],
                    predicates=[dict(kind=kind,**fn.cache_info()._asdict()) for kind,fn in self.memoized])


def main():
    if not __debug__:
        raise RuntimeError('assertions required')
    ap = argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--mode',choices=('all','scalar-only'),default='all')
    args = ap.parse_args()
    implementation = {str(p):sha(p) for p in (Path(__file__),ROOT/'fast_transcript.py',
        ROOT/'integer_factors.py',SCALAR_PACKAGE/'gx_fast.py',SCALAR_PACKAGE/'reference/gx.py')}
    assert not args.output.exists()
    checked_tree(PREDECESSOR/'verify.py',PINS['vendor/predecessor/verify.py'])
    sys.path.insert(0,str(PREDECESSOR))
    ns = runpy.run_path(str(PREDECESSOR/'verify.py'),run_name='optimized_predecessor_driver')
    opt = Optimizations(args.mode)
    opt.install()
    sys.argv = [str(PREDECESSOR/'verify.py'),'--output',str(args.output.resolve())]
    start = time.perf_counter()
    try:
        ns['main']()
    finally:
        opt.restore()
    assert all(sha(path)==digest for path,digest in implementation.items()),'adapter changed during replay'
    report = dict(status='PASS_EXTERNAL_PREDECESSOR_OPTIMIZATIONS',seconds=time.perf_counter()-start,
                  mode=args.mode,statistics=opt.statistics(),source_files=PINS,
                  implementation_sha256=sha(__file__),scalar_implementation_sha256=sha(SCALAR_PACKAGE/'gx_fast.py'),
                  transcript_implementation_sha256=sha(ROOT/'fast_transcript.py'),
                  factor_implementation_sha256=sha(ROOT/'integer_factors.py'),
                  implementation_files_unchanged=implementation,
                  peak_rss_platform_units=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  scope='Fresh checks with externally substituted pure arithmetic and serialization; original source receipts require this provenance sidecar.')
    (args.output/'PERFORMANCE-ADAPTER.json').write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'],flush=True)


if __name__ == '__main__':
    main()
