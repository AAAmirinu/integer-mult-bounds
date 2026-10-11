"""Field-inverse and actual generator RREF differential controls."""
import random
import unittest
from generator_adapter import compile_generator,FROZEN,parse_arguments

class GeneratorTests(unittest.TestCase):
    def test_producer_cube_size_argument_passed_through(self):
        args,remaining=parse_arguments(['--inverse','euclid','--receipt','receipt.json','--p','10','--out','fresh'])
        self.assertIsNone(args.profile)
        self.assertEqual(remaining,['--p','10','--out','fresh'])

    def test_modular_inverses_and_complete_rref(self):
        namespaces=[]
        for mode in (False,True):
            ns=dict(__name__='generator_test',__file__=str(FROZEN))
            exec(compile_generator(FROZEN,mode),ns)
            namespaces.append(ns)
        rng=random.Random(358)
        p=namespaces[0]['P']
        for a in [1,2,9,p-1,*[rng.randrange(1,p) for _ in range(1000)]]:
            self.assertEqual(pow(a,p-2,p),pow(a,-1,p))
        for _ in range(500):
            width=rng.randrange(1,21)
            rows=[[rng.choice((0,0,0,rng.randrange(-p,p))) for j in range(width)]
                  for i in range(rng.randrange(25))]
            if rows and rng.randrange(2):rows.extend([rows[0][:], [0]*width])
            left=namespaces[0]['rref'](rows,width)
            right=namespaces[1]['rref'](rows,width)
            self.assertEqual(left,right)
            self.assertEqual(namespaces[0]['kernel'](left,width),namespaces[1]['kernel'](right,width))
            self.assertEqual(namespaces[0]['gram_nondegenerate_frame'](left,width),namespaces[1]['gram_nondegenerate_frame'](right,width))

if __name__=='__main__':unittest.main()
