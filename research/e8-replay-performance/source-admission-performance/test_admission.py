"""Controls for the private fork handoff and complete-input binding."""
from pathlib import Path
import tempfile
import unittest
from share_source import equal_packages, isolated_value

class AdmissionTests(unittest.TestCase):
    def test_child_nested_mutation_isolated_and_types_preserved(self):
        values={1:[2,3],2: {'tuple':(2**200,-3)},'bool':True}
        def mutate():
            values[4]=[9]
            return values
        with tempfile.TemporaryFile(mode='w+') as log:
            result,rss=isolated_value(mutate,log)
        self.assertNotIn(4,values)
        self.assertEqual(result[4],[9])
        self.assertEqual(result[2]['tuple'],(2**200,-3))
        self.assertIs(result['bool'],True)
        self.assertGreater(rss,0)

    def test_large_result_pipe_does_not_deadlock(self):
        value=list(range(100000))
        with tempfile.TemporaryFile(mode='w+') as log:
            result,_=isolated_value(lambda:value,log)
        self.assertEqual(result,value)

    def test_failed_admission_is_not_success(self):
        def fail():raise AssertionError('fresh adverse control')
        with tempfile.TemporaryFile(mode='w+') as log:
            with self.assertRaisesRegex(AssertionError,'isolated scalar admission failed'):
                isolated_value(fail,log)

    def test_complete_package_mismatch_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            a,b=Path(d)/'a',Path(d)/'b'
            a.mkdir();b.mkdir()
            for p in (a,b):(p/'input').write_text('fresh')
            self.assertEqual(equal_packages(a,b),equal_packages(a,b))
            (b/'input').write_text('changed')
            with self.assertRaises(AssertionError):equal_packages(a,b)
            (b/'input').unlink()
            with self.assertRaises(AssertionError):equal_packages(a,b)
            (b/'input').write_text('fresh');(b/'extra').write_text('unexpected')
            with self.assertRaises(AssertionError):equal_packages(a,b)
            (b/'extra').unlink();(b/'alias').symlink_to(b/'input')
            with self.assertRaises(AssertionError):equal_packages(a,b)

if __name__=='__main__':unittest.main()
