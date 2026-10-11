"""Exact arithmetic, stale-geometry and proof-width adverse controls."""
import ast
from copy import copy
from fractions import Fraction
import json
from operator import mul
from pathlib import Path
import random
import sys
import unittest

from bench_scalar import load,PACKAGE
from scalar_adapter import Geometry,packing_bits,original_bits,integer_triple,compile_word,substitute

def dot(a,b):return sum(map(mul,a,b))

class ScalarTests(unittest.TestCase):
    def test_radix_bound_and_minimal_byte_width(self):
        for bound in [0,1,127,128,255,256,23954,32767,32768,65536,2**128,*range(10000)]:
            bits=packing_bits(bound)
            self.assertEqual(bits%8,0)
            self.assertGreater(1<<bits,2*bound)
            if bits>8:self.assertLessEqual(1<<(bits-8),2*bound)
            self.assertEqual(original_bits(bound),8*((bound.bit_length()+2+7)//8))
        self.assertEqual(packing_bits(23954),16)
        self.assertEqual(original_bits(23954),24)
        for bad in (-1,1.5,True):
            with self.assertRaises(ValueError):packing_bits(bad)

    def test_signed_packing_and_undersized_carry_counterexample(self):
        rng=random.Random(358)
        for _ in range(1000):
            bound=rng.randrange(1,100000)
            radix=1<<packing_bits(bound)
            coefficients=[rng.randrange(-bound,bound+1) for _ in range(rng.randrange(1,12))]
            packed=sum(c*radix**i for i,c in enumerate(coefficients))
            self.assertEqual(packed==0,not any(coefficients))
        # A too-small radix can hide a nonzero exact residual.
        self.assertEqual(-256+1*(1<<8),0)
        self.assertNotEqual(-256+1*(1<<packing_bits(257)),0)

    def test_unit_addition_all_modes_big_integers(self):
        source=(PACKAGE/'scalar/word.py').read_text()
        replay=ast.parse(source).body[0]
        add=next(n for n in replay.body if isinstance(n,ast.FunctionDef) and n.name=='add')
        optimized=substitute(ast.parse(ast.unparse(add)),[('x + c * y','x + y if c == 1 else x - y if c == -1 else x + c * y')])
        rng=random.Random(10)
        for major,binary in ((False,False),(False,True),(True,False)):
            a=dict(major=major,binary=binary);b=dict(a)
            exec(compile(ast.fix_missing_locations(ast.Module(body=[add],type_ignores=[])),'original add','exec'),a)
            exec(compile(optimized,'optimized add','exec'),b)
            for _ in range(200):
                x=rng.getrandbits(rng.randrange(1,250000));y=-rng.getrandbits(rng.randrange(1,250000))
                for c in (-3,-2,-1,0,1,2,3,Fraction(1,2)):
                    if binary and isinstance(c,Fraction):continue
                    self.assertEqual(a['add'](x,c,y),b['add'](x,c,y))

    def test_integer_transcript_exact_and_type_refusals(self):
        rng=random.Random(24)
        for _ in range(1000):
            values=[rng.randrange(-2**100,2**100) for _ in range(3)]
            self.assertEqual(integer_triple(values),json.dumps(values,separators=(',',':')).encode())
        for x in (True,1.,Fraction(1,2),'1'):
            with self.assertRaises(TypeError):integer_triple([1,2,x])

    def test_geometry_full_content_mutation_and_eviction(self):
        geometry=Geometry(maxsize=2)
        a,b=[[1,0]],[[0,1]]
        self.assertTrue(geometry.orthogonal(dot,a,b))
        self.assertTrue(geometry.orthogonal(dot,a,b))
        b[0][0]=1
        self.assertFalse(geometry.orthogonal(dot,a,b))
        a[0]=[0,1]
        self.assertFalse(geometry.orthogonal(dot,a,b))
        self.assertLessEqual(geometry.statistics()['currsize'],2)
        rng=random.Random(16)
        for _ in range(200):
            a=[[rng.randrange(-4,5) for _ in range(20)] for _ in range(rng.randrange(5))]
            b=[[rng.randrange(-4,5) for _ in range(20)] for _ in range(rng.randrange(5))]
            self.assertEqual(geometry.orthogonal(dot,a,b),all(dot(x,y)==0 for x in a for y in b))

    def test_actual_replay_rejects_changed_basis_and_covector_after_warm_cache(self):
        sys.path.insert(0,str(PACKAGE))
        context=load('test_scalar_prepare',PACKAGE/'prepare.py').prepare()
        geometry=Geometry()
        namespace=dict(context,_scalar_orthogonal=geometry.orthogonal)
        exec(compile_word(context['SOURCE_TEXT']),namespace)
        valid=namespace['replay']('F2')
        self.assertTrue(valid['all_source_and_dirty_restored'])
        W,C=context['W'],context['C']
        role=next(s for s in W.order if context['adj'][s])
        t=next(iter(context['adj'][role]));f=W.gauge[role]['frame']
        self.assertTrue(geometry.orthogonal(W.module.dot,[C.cov[t]],C.B[f]))
        changed_basis=copy(C)
        changed_basis.B=dict(C.B);changed_basis.B[f]=[*C.B[f],tuple(C.cov[t])]
        changed_covector=copy(C)
        changed_covector.cov=list(C.cov);changed_covector.cov[t]=tuple(C.B[f][0])
        for mutant in (changed_basis,changed_covector):
            bad=dict(context,C=mutant,_scalar_orthogonal=geometry.orthogonal)
            exec(compile_word(context['SOURCE_TEXT']),bad)
            with self.assertRaisesRegex(AssertionError,'actual target cap'):
                bad['replay']('F2')

    def test_changed_source_and_ast_shape_refused(self):
        with self.assertRaises(AssertionError):compile_word((PACKAGE/'scalar/word.py').read_text()+'\n')
        with self.assertRaises(AssertionError):substitute(ast.parse('x+y'),[('x-y','0')])

if __name__=='__main__':unittest.main()
