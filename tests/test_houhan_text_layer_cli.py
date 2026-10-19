import unittest,pathlib,subprocess,sys,re
ROOT=pathlib.Path(__file__).resolve().parents[1]
class HouhanLayerCLI(unittest.TestCase):
 def test_direct_script_import_path(self):
  code=(ROOT/'scripts/validate_corpus.py').read_text()
  snippet='try:\n    from scripts.houhan_text_layers import layer_errors\nexcept ImportError:\n    from houhan_text_layers import layer_errors'
  self.assertIn(snippet, '\n'.join(line[16:] if line.startswith(' '*16)else line for line in code.splitlines()))
  script='import sys\nsys.path[:]=['+repr(str(ROOT/'scripts'))+']\n'+snippet+'\nassert layer_errors({"text_layer":"received_chapter"})==[]\n'
  r=subprocess.run([sys.executable,'-I','-c',script],capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr)
