"""Independent occupancy and minimum-pool controls for weighted lifetimes."""
import copy
from hashlib import sha256
import itertools
import json
from pathlib import Path
import random
import runpy
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/'scripts/allocate_helper_lifetimes.py'
M=runpy.run_path(str(TOOL))

def problem(rows):
    return {'schema':'integer-mult-helper-lifetimes/v1','contract':'Declared zero-to-zero test slots',
            'lifetimes':[{'id':str(i),'start':a,'end':b,'width':w} for i,(a,b,w) in enumerate(rows)]}

class AllocationTests(unittest.TestCase):
    def test_frozen_pr5717_local_lifetimes(self):
        p=json.loads((ROOT/'tests/fixtures/helper-lifetimes-pr5717.json').read_text())
        self.assertEqual(len(p['lifetimes']),11)
        c=M['allocate'](p)
        self.assertEqual(c['capacity'],2)
        self.assertEqual(len(c['peak']['ids']),2)
        self.assertTrue(M['verify'](p,c)['valid'])

    def test_exhaustive_small_weighted_schedules(self):
        choices=[(a,b,w) for a in range(3) for b in range(a+1,4) for w in (1,2)]
        for rows in itertools.combinations_with_replacement(choices,3):
            p=problem(rows);c=M['allocate'](p)
            peak=max(sum(w for a,b,w in rows if a<=t<b) for t in range(4))
            self.assertEqual(c['capacity'],peak)
            for t in range(4):
                occupied=[]
                for row in p['lifetimes']:
                    if row['start']<=t<row['end']:
                        occupied.extend(x for lo,hi in c['allocations'][row['id']] for x in range(lo,hi))
                self.assertEqual(len(occupied),len(set(occupied)))

    def test_fragmented_reuse_and_touching_boundaries(self):
        p=problem([(0,2,2),(0,4,2),(0,2,2),(2,3,4)])
        c=M['allocate'](p)
        self.assertEqual(c['capacity'],6)
        self.assertEqual(c['allocations']['3'],[[0,2],[4,6]])
        self.assertTrue(M['verify'](p,c)['valid'])

    def test_large_widths_and_512_lifetimes(self):
        p=problem([(i,i+2,10**60) for i in range(512)])
        before=copy.deepcopy(p);c=M['allocate'](p)
        self.assertEqual(c['capacity'],2*10**60)
        self.assertEqual(sum(len(s) for s in c['allocations'].values()),512)
        self.assertEqual(p,before)

    def test_random_fragmentation_against_point_loads(self):
        rng=random.Random(2655)
        for case in range(100):
            rows=[]
            for _ in range(40):
                start=rng.randrange(30);rows.append((start,start+rng.randrange(1,15),rng.randrange(1,20)))
            p=problem(rows);c=M['allocate'](p)
            self.assertEqual(c['capacity'],max(sum(w for a,b,w in rows if a<=t<b) for t in range(45)))
            self.assertTrue(M['verify'](p,c)['valid'])

    def test_replay_rejects_alias_width_and_false_lower_bound(self):
        p=problem([(0,3,2),(1,4,2)]);good=M['allocate'](p)
        cases=[]
        c=copy.deepcopy(good);c['allocations']['1']=[[0,2]];cases.append(c)
        c=copy.deepcopy(good);c['allocations']['1']=[[2,3]];cases.append(c)
        c=copy.deepcopy(good);c['peak']['time']=0;cases.append(c)
        c=copy.deepcopy(good);c['capacity']=5;cases.append(c)
        c=copy.deepcopy(good);c['peak']['ids']=['0','0'];cases.append(c)
        c=copy.deepcopy(good);c['allocations']['0']=[[False,2]];cases.append(c)
        for c in cases:
            with self.assertRaises(ValueError):M['verify'](p,c)
        for row in ({'end':0},{'width':True},{'start':-1},{'extra':1}):
            bad=copy.deepcopy(p);bad['lifetimes'][0].update(row)
            with self.assertRaises(ValueError):M['allocate'](bad)

    def test_isolated_optimized_cli_and_replay_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'lifetimes.json';cert=Path(tmp)/'cert.json'
            source.write_text(json.dumps(problem([(0,2,2),(2,4,3)])))
            command=[sys.executable,'-I','-O',str(TOOL),str(source)]
            r=subprocess.run(command,capture_output=True,text=True,check=True,cwd=tmp)
            report=json.loads(r.stdout);cert.write_text(json.dumps(report['certificate']))
            r=subprocess.run(command+['--verify',str(cert)],capture_output=True,text=True,check=True)
            report=json.loads(r.stdout)
            self.assertEqual(report['inputs']['lifetimes']['sha256'],sha256(source.read_bytes()).hexdigest())
            self.assertEqual(report['inputs']['certificate']['sha256'],sha256(cert.read_bytes()).hexdigest())
            cert.write_text('{}');r=subprocess.run(command+['--verify',str(cert)],capture_output=True,text=True)
            self.assertEqual(r.returncode,2);self.assertEqual(r.stdout,'')

if __name__=='__main__':unittest.main()
