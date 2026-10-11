"""Package-level refusal controls independent of the mathematical replay."""
import importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import fetch,replay

class PackageTests(unittest.TestCase):
    def test_blob_and_inventory(self):
        self.assertEqual(fetch.blob(b'test\n'),'9daeafb9864cf43055ae93beb0afd6c7d144bfa4')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            with self.assertRaisesRegex(ValueError,'inventory'):fetch.verify(root)
            link=root/'link';link.symlink_to(fetch.SOURCE,target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'symlink'):fetch.verify(link)

    def test_changed_tree_pin_refused(self):
        with patch.object(fetch,'TREE_PIN','0'*64):
            with self.assertRaisesRegex(ValueError,'inventory changed'):fetch.metadata()

    def test_changed_package_and_extra_file_refused(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'file').write_text('value')
            digest=__import__('hashlib').sha256(b'value').hexdigest()
            (root/'MANIFEST.json').write_text(json.dumps({'file':digest}))
            with patch.object(replay,'ROOT',root),patch.object(replay,'SOURCE',root/'cache'):
                replay.integrity();(root/'file').write_text('changed')
                with self.assertRaisesRegex(ValueError,'changed'):replay.integrity()
                (root/'file').write_text('value');(root/'extra').write_text('extra')
                with self.assertRaisesRegex(ValueError,'unexpected'):replay.integrity()

    def test_disabled_assertions_refused(self):
        p=subprocess.run([sys.executable,'-O','-B',str(Path(replay.__file__)),'--help'],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0);self.assertIn('assertions must remain enabled',p.stderr)

if __name__=='__main__':unittest.main()
