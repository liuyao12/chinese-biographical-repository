import copy,json,unittest
from pathlib import Path
from scripts.source_author_prefix import source_author_errors
R=Path(__file__).resolve().parents[1];C=json.loads((R/'corpus/sanguozhi/015-pei-simabiao.json').read_text());ALL={w['id']:w for w in json.loads((R/'registry/works.json').read_text())['works']};W={wid:w for wid,w in ALL.items()if wid in ['w-simabiao-xuzhuan-sgz015-reference','w-hanshu-mingchen-liezhuan-sgz015-reference']};CH={C['id']:C}
class Sgz015WorkReferences(unittest.TestCase):
 def test_two_reference_spans_exact(self):
  ms=[m for m in C['paragraphs'][0]['mentions']if m['kind']=='work'];self.assertEqual({m['surface']for m in ms},{'序傳','漢書名臣列傳'})
  for m in ms:self.assertEqual(C['paragraphs'][0]['text'][m['start']:m['end']],m['surface']);self.assertIsNone(m['person_id'])
 def test_actual_author_prefix(self):self.assertEqual(source_author_errors(W,CH),[])
 def mutate(self,f):
  w=copy.deepcopy(W);e=w['w-simabiao-xuzhuan-sgz015-reference']['source_author_attributions'][0];f(e);return source_author_errors(w,CH)
 def test_wrong_source_referenced_endpoint(self):self.assertTrue(self.mutate(lambda e:e.update(work_id=e['referenced_work_id'])))
 def test_wrong_author(self):self.assertTrue(self.mutate(lambda e:e.update(author_person_id='wrong')))
 def test_truncated_quote(self):self.assertTrue(self.mutate(lambda e:e.update(quote=e['quote'][:-1])))
 def test_hanshu_link_not_identity(self):
  m=next(m for m in C['paragraphs'][0]['mentions']if m.get('surface')=='漢書名臣列傳');self.assertEqual(m['work_id'],'w-hanshu-mingchen-liezhuan-sgz015-reference');self.assertNotEqual(m['work_id'],'w-hanshu');self.assertIn('不憑現代連結',W[m['work_id']]['citation_qualification']);self.assertIsNone(W[m['work_id']]['author'])
