import unittest,tempfile,json
from pathlib import Path
try:from scripts.work_title_index import outputs
except ImportError:from work_title_index import outputs
class WorkTitleIndex(unittest.TestCase):
 def write(self,root,works):
  p=root/'registry/works.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps({'works':works}))
 def test_all_registered_even_without_chapters_and_no_inference(self):
  with tempfile.TemporaryDirectory()as d:
   r=Path(d);self.write(r,[{'id':'w-cited','title':'完整題名','books':[]},{'id':'w-other','title':'另一書','books':[]}]);v=json.loads(outputs(r)[r/'data/corpus/work-titles.json']);self.assertEqual(v['works'],[{'id':'w-cited','title':'完整題名'},{'id':'w-other','title':'另一書'}]);self.assertFalse((r/'data/corpus/work-titles.json').exists())
 def test_roots_are_independent(self):
  with tempfile.TemporaryDirectory()as a,tempfile.TemporaryDirectory()as b:
   a,b=Path(a),Path(b);self.write(a,[{'id':'w-same','title':'甲'}]);self.write(b,[{'id':'w-same','title':'乙'}]);self.assertNotEqual(list(outputs(a).values()),list(outputs(b).values()))
 def test_malformed_or_duplicate_registry_refused(self):
  with tempfile.TemporaryDirectory()as d:
   r=Path(d)
   for rows in [[{'id':'w-x','title':''}],[{'id':'bad','title':'書'}],[{'id':'w-x','title':'一'},{'id':'w-x','title':'二'}]]:
    self.write(r,rows)
    with self.assertRaises(ValueError):outputs(r)
if __name__=='__main__':unittest.main()
