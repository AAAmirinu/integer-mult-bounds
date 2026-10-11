"""Hash-bound exact scalar admission optimizations; every replay still runs.

The clean integer proof uses the same freshly derived residual bound and the
same strict radix inequality. Adverse controls keep the original packing width.
Geometry predicates are cached by their complete current row contents.
"""
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT.parent/'e8-pipeline-profile/pr358-source/vendor/source353354/pkg'
SCALAR_PIN='7df8fcca1d866087f982549df8424ee0b26d5dd3bbb2a725e5ddfb347ed125e4'
WORD_PIN='e675d4eb9d90ff0b44279fae0b46f1a8b39f65421cc38454b70a6b75d0e10b42'
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def packing_bits(bound):
    if type(bound) is not int or bound<0:raise ValueError('nonnegative integer bound required')
    bits=8*max(1,((2*bound).bit_length()+7)//8)
    assert (1<<bits)>2*bound
    return bits

def original_bits(bound):return 8*((bound.bit_length()+9)//8)

def integer_triple(values):
    a,b,c=values
    if not all(type(x) is int for x in (a,b,c)):raise TypeError('three native integer operands required')
    return ('['+str(a)+','+str(b)+','+str(c)+']').encode()

class Geometry:
    def __init__(self,maxsize=32768):
        self.cache=lru_cache(maxsize=maxsize)(
            lambda dot,left,right:all(dot(a,b)==0 for a in left for b in right))

    def orthogonal(self,dot,left,right):
        # Frame IDs, object identities and mutable lists are never the key.
        return self.cache(dot,tuple(map(tuple,left)),tuple(map(tuple,right)))

    def statistics(self):return self.cache.cache_info()._asdict()

def substitute(tree,replacements):
    mapping={ast.dump(ast.parse(before,mode='eval').body):after for before,after in replacements}
    counts={key:0 for key in mapping}
    class Replace(ast.NodeTransformer):
        def visit(self,node):
            key=ast.dump(node)
            if key in mapping:
                counts[key]+=1
                return ast.copy_location(ast.parse(mapping[key],mode='eval').body,node)
            return super().visit(node)
    tree=Replace().visit(tree)
    assert all(n==1 for n in counts.values()),('pinned AST shape changed',list(counts.values()))
    return ast.fix_missing_locations(tree)

def compile_word(source,geometry=True,unit_add=True):
    assert hashlib.sha256(source.encode()).hexdigest()==WORD_PIN
    replacements=[]
    if geometry:
        replacements.extend([
            ('all(W.module.dot(C.cov[t], b) == 0 for b in C.B[f])',
             '_scalar_orthogonal(W.module.dot, (C.cov[t],), C.B[f])'),
            ('all(W.module.dot(a, b) == 0 for a in previous for b in C.B[f])',
             '_scalar_orthogonal(W.module.dot, previous, C.B[f])')])
    if unit_add:
        replacements.append(('x + c * y','x + y if c == 1 else x - y if c == -1 else x + c * y'))
    tree=substitute(ast.parse(source),replacements)
    return compile(tree,'retained source527 exact scalar word','exec')

def install(module,*,geometry=True,unit_add=True,packing=True,transcript=True):
    assert SHA(module.__file__)==SCALAR_PIN
    geometry_cache=Geometry()
    replay_rows=[]
    compiled={}
    def timed_compile(source):
        # All controls still exec into their own namespace; only the identical
        # immutable code object is reused. No replay result is cached.
        assert hashlib.sha256(source.encode()).hexdigest()==WORD_PIN
        if source not in compiled:compiled[source]=compile_word(source,geometry,unit_add)
        return compiled[source]
    replacements=[("compile(source, 'retained source527 exact scalar word', 'exec')",'_compile_scalar_word(source)')]
    # The compile expression occurs twice intentionally: clean and adverse
    # namespaces. Require exactly those two sites before the shared replacer.
    tree=ast.parse(Path(module.__file__).read_text())
    needle=ast.dump(ast.parse(replacements[0][0],mode='eval').body)
    found=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and ast.dump(n)==needle]
    assert len(found)==2
    for n in found:
        n.func=ast.Name(id='_compile_scalar_word',ctx=ast.Load());n.args=[n.args[0]];n.keywords=[]
    replacements=[]
    if packing:
        replacements.extend([
            ('8 * ((bound.bit_length() + 2 + 7) // 8)','_scalar_packing_bits(bound)'),
            ("bad['replay'](mode, bits=bits)","bad['replay'](mode, bits=_scalar_original_bits(bound))")])
    if transcript:
        replacements.append(("json.dumps([a, b, c], separators=(',', ':')).encode()",'_scalar_integer_triple([a, b, c])'))
    tree=substitute(tree,replacements)
    # Measure real replays, including failed controls, with both CPU and wall
    # clocks. Distinct namespace executions remain unchanged.
    run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
    calls=0
    for n in ast.walk(run):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Subscript) and isinstance(n.func.value,ast.Name) and n.func.value.id in ('ns','bad') and isinstance(n.func.slice,ast.Constant) and n.func.slice.value=='replay':
            n.args.insert(0,ast.Name(id=n.func.value.id,ctx=ast.Load()))
            n.func=ast.Name(id='_scalar_timed_replay',ctx=ast.Load());calls+=1
    assert calls==4
    def timed_replay(namespace,*args,**kwargs):
        begin=time.perf_counter();cpu=time.process_time();passed=False
        try:
            value=namespace['replay'](*args,**kwargs);passed=True;return value
        finally:
            replay_rows.append(dict(args=list(args),kwargs=kwargs,passed=passed,
                seconds=time.perf_counter()-begin,cpu_seconds=time.process_time()-cpu))
    namespace=dict(module.__dict__)
    namespace.update(_compile_scalar_word=timed_compile,_scalar_packing_bits=packing_bits,
        _scalar_original_bits=original_bits,_scalar_integer_triple=integer_triple,
        _scalar_timed_replay=timed_replay)
    exec(compile(ast.fix_missing_locations(tree),str(module.__file__),'exec'),namespace)
    original=namespace['run']
    def run(context,*args,**kwargs):
        fresh=dict(context,_scalar_orthogonal=geometry_cache.orthogonal)
        return original(fresh,*args,**kwargs)
    module.run=run
    def report():
        return dict(status='PASS_EXACT_SCALAR_ADMISSION_ADAPTER',
            flags=dict(geometry=geometry,unit_add=unit_add,packing=packing,transcript=transcript),
            replays=replay_rows,geometry_cache=geometry_cache.statistics(),
            implementation_sha256=SHA(__file__),original_scalar_sha256=SCALAR_PIN,
            original_word_sha256=WORD_PIN,
            clean_packing='Smallest byte-aligned radix with 2**bits > 2*fresh_residual_bound.',
            adverse_packing='Original width unchanged for every corruption control.')
    module._performance_report=report
