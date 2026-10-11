"""Exact modular inverse A/B for the pinned frozen-arc generator."""
import argparse
import ast
import cProfile
import hashlib
import json
from pathlib import Path
import pstats
import sys
import time

ROOT=Path(__file__).resolve().parent
FROZEN=ROOT.parent/'e8-pipeline-profile/pr358-source/vendor/source353354/pkg/bitword/producer/paired_cube_bit_word.py'
SHA=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
GENERATOR_PIN='d13a8df9734a57c1b46a8b1bb145b46cb3f6bfd00703f6cdb3675ac23f252e03'

def compile_generator(script,euclid):
    assert SHA(script)==GENERATOR_PIN,'generator pin mismatch'
    tree=ast.parse(script.read_text())
    count=0
    class Inverse(ast.NodeTransformer):
        def visit_Call(self,node):
            nonlocal count
            if (isinstance(node.func,ast.Name) and node.func.id=='pow'
                and len(node.args)==3 and not node.keywords
                and ast.dump(node.args[1])==ast.dump(ast.parse('P - 2',mode='eval').body)
                and isinstance(node.args[2],ast.Name) and node.args[2].id=='P'):
                count+=1
                if euclid:node.args[1]=ast.copy_location(ast.UnaryOp(op=ast.USub(),operand=ast.Constant(1)),node.args[1])
            return self.generic_visit(node)
    tree=Inverse().visit(tree)
    assert count==2,'modular inverse call shape changed'
    return compile(ast.fix_missing_locations(tree),str(script),'exec')

def parse_arguments(argv=None):
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--script',type=Path,default=FROZEN)
    ap.add_argument('--inverse',choices=('fermat','euclid'),required=True)
    ap.add_argument('--profile',type=Path)
    ap.add_argument('--receipt',type=Path,required=True)
    return ap.parse_known_args(argv)

def main():
    assert __debug__
    args,remaining=parse_arguments()
    assert not args.receipt.exists()
    script=args.script.resolve()
    code=compile_generator(script,args.inverse=='euclid')
    ns=dict(__name__='__main__',__file__=str(script),__package__=None)
    sys.argv=[str(script),*remaining]
    before=time.perf_counter()
    if args.profile:
        assert not args.profile.exists()
        profiler=cProfile.Profile()
        profiler.runcall(exec,code,ns)
        profiler.dump_stats(str(args.profile))
    else:exec(code,ns)
    result=dict(seconds=time.perf_counter()-before,inverse=args.inverse,
        original_generator_sha256=SHA(script),implementation_sha256=SHA(__file__),
        scope='Same complete frozen-arc generator; modular inverses equal in the fixed prime field.')
    if args.profile:
        stats=pstats.Stats(str(args.profile))
        functions=[]
        for (file,line,name),(primitive,calls,own,cumulative,callers) in stats.stats.items():
            functions.append(dict(file=file,line=line,name=name,calls=calls,own_seconds=own,cumulative_seconds=cumulative))
        result['profile_top_30']=sorted(functions,key=lambda x:-x['cumulative_seconds'])[:30]
    args.receipt.write_text(json.dumps(result,indent=2)+'\n')
    print('GENERATOR',args.inverse,round(result['seconds'],3),flush=True)

if __name__=='__main__':main()
