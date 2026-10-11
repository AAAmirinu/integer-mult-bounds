"""Small differential and refusal tests; full replay supplies integration QA."""
import ast
import importlib.util
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest

from fast_transcript import LineEncoder, integer_triple
import proof_adapter as adapter
import run_native
from fractions import Fraction as Q
from integer_factors import replay_factors


class Tests(unittest.TestCase):
    def test_line_bytes_and_typed_keys(self):
        encoder = LineEncoder(maxsize=16)
        values = [('main',('accumulate',('L',9),('W',0),-1)),
                  ('é\n\\"', (1,True,1.0,None)), (True,), (1,), (1.0,),
                  (10**150,-10**150), (), ('main',('clear',('W',0)))]
        rng = random.Random(358)
        values.extend((rng.choice(('cleanup','main','old_response')),
                       ('add',('L',rng.randrange(10000)),('T',rng.randrange(10000)),
                        rng.randrange(-10**40,10**40),rng.choice((1,2,3,6)))) for _ in range(150))
        for value in values * 2:
            self.assertEqual(encoder.line(value),(json.dumps(value,separators=(',',':'))+'\n').encode())
        self.assertEqual(encoder.line((1,)),b'[1]\n')
        self.assertEqual(encoder.line((True,)),b'[true]\n')
        self.assertEqual(encoder.line((1.0,)),b'[1.0]\n')
        self.assertLessEqual(encoder.statistics()['currsize'],16)

    def test_integer_triples(self):
        for value in ((0,1,-1),(10**300,-10**200,3),(-0,2,3)):
            self.assertEqual(integer_triple(value),json.dumps(list(value),separators=(',',':')).encode())
        for value in ((True,1,2),(1.0,2,3),('1',2,3)):
            with self.assertRaises(TypeError): integer_triple(value)

    def test_source_shapes_and_changed_bytes_refused(self):
        path = adapter.PREDECESSOR/'code/complex_splice.py'
        tree = adapter.checked_tree(path,adapter.PINS[path.relative_to(adapter.SOURCE).as_posix()])
        fn = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='validate')
        change = adapter.TranscriptCalls(); change.visit(fn)
        self.assertEqual(change.count,4)
        with tempfile.TemporaryDirectory() as d:
            changed = Path(d)/'changed.py'; changed.write_text(path.read_text()+'\n')
            with self.assertRaises(ValueError): adapter.checked_tree(changed,adapter.sha(path))

    def test_scalar_substitution_preserves_all_other_code(self):
        paths = (adapter.SCALAR_PACKAGE/'reference/gx.py',adapter.SCALAR_PACKAGE/'gx_fast.py')
        def other(path):
            t=ast.parse(path.read_text());t.body=[n for n in t.body if not (isinstance(n,ast.FunctionDef) and n.name=='scal')]
            return ast.dump(t)
        self.assertEqual(other(paths[0]),other(paths[1]))
        self.assertEqual(adapter.sha(paths[0]),adapter.PINS['vendor/predecessor/inputs/complex/sources/tools__gx__gx.py'])

    def test_dot_memo_uses_current_row_contents(self):
        path = adapter.PREDECESSOR/'bitword/references/pr168-v4/research/paired-cube-bit/check_paired_cube_bit.py'
        spec = importlib.util.spec_from_file_location('test_backend',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        original=module.dot;opt=adapter.Optimizations();opt.patch(module,path)
        a,b=[1,2,3],[4,5,6]
        self.assertEqual(module.dot(a,b),original(a,b))
        self.assertEqual(module.dot(a,b),32)
        a[0]=10
        self.assertEqual(module.dot(a,b),original(a,b))
        self.assertEqual(module.dot(a,b),68)
        self.assertGreater(opt.statistics()['predicates'][0]['hits'],0)

    def test_integer_factor_replay_every_prefix(self):
        rng=random.Random(358)
        for n in (1,2,3,7,20):
            initial=[[rng.randrange(-20,21) for _ in range(n)] for _ in range(n)]
            rational=[list(map(Q,row)) for row in initial]
            ops=[]
            for k in range(35):
                i=rng.randrange(n);j=rng.randrange(n)
                a=rng.choice((-10**50-3,-7,-1,0,1,2,10**50+1));b=rng.choice((1,2,3,6,17))
                op=rng.choice(('scale','add','swap'));ops.append((op,i,j,a,b))
                if op=='swap':rational[i],rational[j]=rational[j],rational[i]
                elif op=='scale':rational[i]=[Q(a,b)*x for x in rational[i]]
                else:rational[i]=[x+Q(a,b)*y for x,y in zip(rational[i],rational[j])]
                self.assertEqual(replay_factors(initial,ops),rational,(n,k))

    def test_bank_replay_substitution_and_corruption(self):
        path=adapter.PREDECESSOR/'bank_check.py'
        # Only compile the replacement; importing the bank module needs its
        # immutable package imports, which the full native integration supplies.
        import types
        mod=types.ModuleType('test_bank')
        adapter.replace_factors(mod,path,adapter.PINS['vendor/predecessor/bank_check.py'])
        self.assertTrue(callable(mod.run))
        B=[[2,1],[1,1]]
        ops=[('add',0,1,-1,1),('add',1,0,-1,1)]
        self.assertEqual(replay_factors(B,ops),[[Q(1),Q(0)],[Q(0),Q(1)]])
        corrupt=[('add',0,1,1,1),*ops[1:]]
        self.assertNotEqual(replay_factors(B,corrupt),[[Q(1),Q(0)],[Q(0),Q(1)]])

    def test_scheduling_inserts_exactly_one_worker_and_keeps_stage_order(self):
        driver=adapter.PROFILE/'parallel_verify358.py'
        ns=run_native.scheduled_namespace(driver,{},lambda *args:None)
        original={}
        # Module import only; neither namespace runs its main entry point.
        import os,runpy
        os.environ['E8_PROFILE_SOURCE']=str(adapter.SOURCE)
        original=runpy.run_path(str(driver),run_name='test_original_driver')
        self.assertEqual(ns['STAGES'],original['STAGES'])
        self.assertEqual(len(ns['STAGES']),24)


if __name__=='__main__':
    # scheduled_namespace needs this before its integrity-bound module import.
    import os
    os.environ['E8_PROFILE_SOURCE']=str(adapter.SOURCE)
    unittest.main()
