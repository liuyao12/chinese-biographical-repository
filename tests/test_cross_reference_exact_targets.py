import copy,json,unittest
from pathlib import Path
from scripts.cross_chapter_references import errors
ROOT=Path(__file__).resolve().parents[1]
class ExactTargetTests(unittest.TestCase):
 def test_actual_targets_and_wrong_membership(self):
  chapters={}
  for f in (ROOT/'corpus').glob('*/*.json'):
   c=json.loads(f.read_text())
   if c.get('record_type')=='marked_chapter':chapters[c['id']]=c
  self.assertEqual(errors(chapters,ROOT),[])
  refs=[(cid,r)for cid,c in chapters.items()for r in c.get('cross_chapter_references',[])if r.get('target',{}).get('text_status')=='imported']
  self.assertGreaterEqual(len(refs),5)
  for cid,r in refs:
   for field,value in [('work_id','w-wrong'),('book_id','b-wrong'),('chapter_id','c-missing'),('paragraph_id','c-missing:p001')]:
    bad=copy.deepcopy(chapters);rr=next(x for x in bad[cid]['cross_chapter_references']if x['id']==r['id']);rr['target'][field]=value
    self.assertTrue(errors(bad,ROOT))
 def test_legacy_absence_and_malformed_index(self):
  self.assertEqual(errors({},ROOT),[])
  self.assertTrue(errors(None,ROOT))
if __name__=='__main__':unittest.main()
