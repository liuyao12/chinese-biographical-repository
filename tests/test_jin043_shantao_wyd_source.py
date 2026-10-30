from pathlib import Path
import sys,json,copy,hashlib,unittest
F=Path(__file__).resolve().parents[1];sys.path.insert(0,str(F))
from scripts.fixed_wuyingdian_jin043_shantao import validate_source,source_errors
from scripts.render_corpus import render
CH=json.loads((F/'corpus/jinshu/043-wyd1739-shantao.json').read_text())
class Cases(unittest.TestCase):
 def bad(self,mut):
  c=copy.deepcopy(CH);mut(c)
  with self.assertRaises(ValueError):validate_source(c,F)
 def test_01_actual(self):self.assertTrue(validate_source(CH,F));self.assertEqual(source_errors(CH,F),[])
 def test_02_text(self):self.bad(lambda c:c['paragraphs'][0].update(text='王'+c['paragraphs'][0]['text'][1:]))
 def test_03_position(self):self.bad(lambda c:c['paragraphs'][0]['source_position'].update(first_line=2))
 def test_04_layer(self):self.bad(lambda c:c['paragraphs'][-1].update(text_layer='received_chapter'))
 def test_05_pending(self):self.bad(lambda c:c['paragraphs'][0].update(annotation_status='complete'))
 def test_06_human(self):self.bad(lambda c:c['annotation'].update(human_reviewed=True))
 def test_07_revision(self):self.bad(lambda c:c['source'].update(revision_id=None))
 def test_08_XML(self):self.assertEqual(render(CH),(F/'corpus/jinshu/043-wyd1739-shantao.xml').read_text())
 def test_09_mentions(self):self.bad(lambda c:c['paragraphs'][0]['mentions'].append({'kind':'person','person_id':'fake'}))
if __name__=='__main__':unittest.main()
