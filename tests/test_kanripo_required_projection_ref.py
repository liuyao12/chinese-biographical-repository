import unittest,tempfile,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from fixed_kanripo_projection import errors
class RequiredProjectionRefTests(unittest.TestCase):
 def run_case(self,catalog,chapter):
  with tempfile.TemporaryDirectory()as d:
   r=Path(d);(r/'scripts').mkdir();(r/'scripts/fixed_kanripo_witness_pins.json').write_text(json.dumps(catalog));return errors(chapter,r)
 def catalog(self):return {'format_version':'0.1','witnesses':{'fixed':{}},'chapter_bindings':{'known':'fixed'}}
 def test_known_missing_entire_ref_rejected(self):self.assertTrue(self.run_case(self.catalog(),{'id':'known'}))
 def test_known_empty_ref_rejected(self):self.assertTrue(self.run_case(self.catalog(),{'id':'known','annotation':{'fixed_kanripo_projection_ref':''}}))
 def test_known_nonstring_ref_rejected(self):self.assertTrue(self.run_case(self.catalog(),{'id':'known','annotation':{'fixed_kanripo_projection_ref':7}}))
 def test_legacy_unregistered_missing_ref_preserved(self):self.assertEqual([],self.run_case(self.catalog(),{'id':'legacy'}))
 def test_dangling_trusted_binding_rejected(self):
  c=self.catalog();c['witnesses']={};self.assertTrue(self.run_case(c,{'id':'known'}))
 def test_symlink_trusted_config_rejected(self):
  with tempfile.TemporaryDirectory()as d:
   r=Path(d);(r/'scripts').mkdir();(r/'actual').write_text(json.dumps(self.catalog()));(r/'scripts/fixed_kanripo_witness_pins.json').symlink_to(r/'actual');self.assertTrue(errors({'id':'known'},r))
if __name__=='__main__':unittest.main()
