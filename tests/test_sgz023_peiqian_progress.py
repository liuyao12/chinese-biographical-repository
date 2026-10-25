import json,unittest
from pathlib import Path
from scripts.reading_catalog import outputs
ROOT=Path(__file__).resolve().parents[1]
class PeiqianProgress(unittest.TestCase):
 def test_distinct_partial_progress_and_actual_reader_outputs(self):
  ids={'c-sanguozhi-023-peiqian','c-sanguozhi-023-qing-collation'}
  progress=json.loads((ROOT/'corpus/progress.json').read_text())['books']
  rows=[r for r in progress if r['chapter_id']in ids]
  self.assertEqual(len(rows),2)
  for r in rows:self.assertIs(r['complete'],False);self.assertEqual(r['person_status'],'in_progress')
  result=outputs(ROOT)
  index=json.loads(result[ROOT/'data/corpus/sanguozhi/index.json'])
  chapters={c['chapter_id']:c for c in index['chapters']}
  for cid in ids:
   self.assertIn(cid,chapters);self.assertEqual(chapters[cid]['annotation_status'],'in_progress');self.assertEqual(chapters[cid]['text_scope'],'partial_chapter')
   self.assertIn(ROOT/chapters[cid]['path'],result)
  self.assertEqual(chapters['c-sanguozhi-023-peiqian']['paragraph_count'],21)
  self.assertEqual(chapters['c-sanguozhi-023-qing-collation']['paragraph_count'],1)
if __name__=='__main__':unittest.main()
