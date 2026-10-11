"""Source-shape refusals and actual fork isolation controls."""
from array import array
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from share_source import PrefixBank, compile_consumer, EXPRESSIONS, FROZEN, RELATIVES


class SharingTests(unittest.TestCase):
    def test_pinned_consumer_shapes(self):
        for label,relative in RELATIVES.items():
            for deep in (False,True):
                _,count=compile_consumer(label,FROZEN/relative,deep)
                self.assertEqual(count,4 if deep and label in ('target-selection','restore-selection','sink-selection','stages-export') else 3)

    def test_missing_or_duplicated_prefix_rejected(self):
        original=(FROZEN/'code/export_p10.py').read_text()
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'consumer.py'
            p.write_text(original.replace('phys.run(context,context[\'SOURCE_TEXT\'],output_dir=None)','phys.run(context,"changed",output_dir=None)'))
            with self.assertRaises(ValueError):compile_consumer('base-export',p,True)
            p.write_text(original+'\n'+EXPRESSIONS['base-export'][0]+'\n')
            with self.assertRaises(ValueError):compile_consumer('base-export',p,True)

    def test_fork_isolates_registry_records_and_nested_state(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            C=SimpleNamespace(B={0:[[1,0]]},A={0:[[0,1]]},dimf={0:1})
            W=SimpleNamespace(C=C,frame_ids={((1,0),):0})
            prefix={'W':W,'C':C,'records':array('i',[1,2,3]),'initial_state':{0:0},'nested':{'value':1}}
            bank=PrefixBank(root,True)
            bank.prepared={'SOURCE_TEXT':'source','W':W,'C':C}
            bank.physical=prefix
            bank.prefixes={'parity':prefix}
            bank.initialized=True
            bank.advance=lambda label:None
            path=root/'consumer.py'
            path.write_text("from pathlib import Path\nP=Path('.')\nctx="+EXPRESSIONS['base-export'][0]+"\ncontext=dict(ctx)\nprod="+EXPRESSIONS['base-export'][1]+"\nrun="+EXPRESSIONS['base-export'][2]+"\nrun['records'][0]=999\nrun['nested']['value']=999\nrun['C'].B[9]=[[9,9]]\nrun['W'].frame_ids[((9,9),)]=9\n")
            before=bank.fingerprint()
            with (root/'child.log').open('w') as log:
                self.assertEqual(bank.execute('base-export',path,[],log),0)
            self.assertEqual(bank.fingerprint(),before)
            self.assertEqual(prefix['records'][0],1)
            self.assertEqual(prefix['nested']['value'],1)
            self.assertNotIn(9,C.B)
            self.assertNotIn(((9,9),),W.frame_ids)

    def test_failed_child_is_failure(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            C=SimpleNamespace(B={0:[]},A={0:[]},dimf={0:0})
            W=SimpleNamespace(C=C,frame_ids={():0})
            prefix={'W':W,'C':C,'records':array('i',[]),'initial_state':{}}
            bank=PrefixBank(root,False)
            bank.prepared={'SOURCE_TEXT':'source'};bank.physical=prefix
            bank.prefixes={'parity':prefix};bank.advance=lambda label:None
            p=root/'fail.py'
            p.write_text('ctx='+EXPRESSIONS['base-export'][0]+"\ncontext=dict(ctx)\nprod="+EXPRESSIONS['base-export'][1]+"\nrun="+EXPRESSIONS['base-export'][2]+"\nraise ValueError('negative control')\n")
            with (root/'failure.log').open('w') as log:
                self.assertEqual(bank.execute('base-export',p,[],log),1)
            self.assertEqual(bank.consumers[0]['returncode'],1)
            self.assertIn('negative control',(root/'failure.log').read_text())


if __name__=='__main__':
    unittest.main()
