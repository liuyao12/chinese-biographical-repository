from pathlib import Path
import tempfile,json,unittest
from scripts.work_title_index import outputs
class WorkTitleQualification(unittest.TestCase):
 def render(self,work):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'registry').mkdir();(p/'registry/works.json').write_text(json.dumps({'works':[work]}));return json.loads(next(iter(outputs(p).values())))['works'][0]
 def test_separate_explicit(self):
  self.assertEqual(self.render({'id':'w-jin','title':'晉書（標籤）','citation_title':'晉書','citation_qualification':'作者未詳'}),{'id':'w-jin','title':'晉書','qualification':'作者未詳'})
 def test_no_guess(self):self.assertEqual(self.render({'id':'w-jin','title':'晉書（標籤）'})['title'],'晉書（標籤）')
 def test_malformed(self):
  for key in ['citation_title','citation_qualification']:
   for value in ['',None,42]:
    with self.assertRaises(ValueError):self.render({'id':'w-jin','title':'晉書',key:value})
