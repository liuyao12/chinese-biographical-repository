from tests.portable_fixture_copy import fixture_copy2
from pathlib import Path
import sys,json,copy,hashlib,unittest,tempfile,shutil
F=Path(__file__).resolve().parents[1];sys.path.insert(0,str(F))
from scripts.fixed_wuyingdian_jin040_jiachong import validate_source,source_errors
from scripts.render_corpus import render
ACTUAL=json.loads((F/'corpus/jinshu/040-wyd1739-jiachong.json').read_text())
CH=copy.deepcopy(ACTUAL)
SC=json.loads((F/'source-evidence/jin040-wyd1739-jiachong/transcription-witness-contract.json').read_text())
CH['annotation']=copy.deepcopy(SC['required_annotation']);CH['paragraphs']=copy.deepcopy(SC['paragraphs'])
class Cases(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  global F
  cls.tmp=tempfile.TemporaryDirectory();F=Path(cls.tmp.name)
  shutil.copytree(Path(__file__).resolve().parents[1]/'source-evidence/jin040-wyd1739-jiachong',F/'source-evidence/jin040-wyd1739-jiachong', copy_function=fixture_copy2)
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def bad(self,mut):
  c=copy.deepcopy(CH);mut(c)
  with self.assertRaises(ValueError):validate_source(c,F)
 def test_01_actual(self):self.assertTrue(validate_source(CH,F));self.assertEqual(source_errors(CH,F),[])
 def test_02_text(self):self.bad(lambda c:c['paragraphs'][0].update(text='王'+c['paragraphs'][0]['text'][1:]))
 def test_03_position(self):self.bad(lambda c:c['paragraphs'][0]['source_position'].update(first_line=2))
 def test_04_layer(self):self.bad(lambda c:c['paragraphs'][-1].update(text_layer='received_compiler_appraisal'))
 def test_05_pending(self):self.bad(lambda c:c['paragraphs'][0].update(annotation_status='complete'))
 def test_06_human(self):self.bad(lambda c:c['annotation'].update(human_reviewed=True))
 def test_07_revision(self):self.bad(lambda c:c['source'].update(revision_id=None))
 def test_08_XML(self):
  self.assertEqual(render(ACTUAL),(Path(__file__).resolve().parents[1]/'corpus/jinshu/040-wyd1739-jiachong.xml').read_text())
  self.assertEqual([p['text']for p in CH['paragraphs']],[p['text']for p in ACTUAL['paragraphs']])
 def test_09_mentions(self):self.bad(lambda c:c['paragraphs'][0]['mentions'].append({'kind':'person','person_id':'fake'}))
 def test_10_raw_drift(self):
  p=F/'source-evidence/jin040-wyd1739-jiachong/transcription-columns.txt';old=p.read_bytes()
  try:
   p.write_bytes(old+'錯'.encode())
   with self.assertRaises(ValueError):validate_source(CH,F)
  finally:p.write_bytes(old)
 def test_11_page_side_column_pin(self):
  p=F/'source-evidence/jin040-wyd1739-jiachong/image-column-locations.json';old=p.read_bytes()
  try:
   for key,val in [('pdf_page',40),('side','right'),('physical_column_from_right_1based',6),('raw_character_offsets_0based',[1,21])]:
    d=json.loads(old);d['column_coordinates'][0][key]=val;p.write_text(json.dumps(d))
    with self.assertRaises(ValueError):validate_source(CH,F)
  finally:p.write_bytes(old)
 def test_12_printed_scope(self):
  self.assertEqual(len(CH['paragraphs']),25)
  text=''.join(p['text']for p in CH['paragraphs']);self.assertEqual(len(text),5016)
  self.assertIn('中騶三百人收之',text);self.assertIn('豫謀楊駿',text);self.assertNotIn('楊駿字文長',text)
 def test_13_bad_AI_type(self):self.bad(lambda c:c['annotation'].update(human_reviewed=0))
if __name__=='__main__':unittest.main()
