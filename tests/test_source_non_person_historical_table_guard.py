import unittest,json,tempfile
from pathlib import Path
from scripts.source_non_person_retirement import reservation_ids,REVIEW_PATH,RECEIPT_PATH,MIRRORS
from scripts.retired_person_ids import retired_person_ids

class NonPersonHistoricalTableGuardTests(unittest.TestCase):
 def setUp(self):self.root=Path(__file__).resolve().parents[1]
 def minimal_root(self,directory):
  root=Path(directory)
  for rel in ['registry/persons.json','corpus/shiji/130.json','corpus/shiji/037.json',REVIEW_PATH,RECEIPT_PATH,*MIRRORS,'data/historical-tables/shiji-015.json']:
   f=root/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes((self.root/rel).read_bytes())
  return root
 def test_real_native_table_person_mention_cannot_keep_retired_annotation_id(self):
  with tempfile.TemporaryDirectory()as directory:
   root=self.minimal_root(directory);review=json.loads((root/REVIEW_PATH).read_text());old=review['prior_editorial_record']['id'];self.assertIn(old,retired_person_ids(root))
   f=root/'data/historical-tables/shiji-015.json';table=json.loads(f.read_text());cell=table['fragments'][0]['rows'][0]['cells'][1];mention=cell['person_mentions'][0];self.assertEqual(mention['surface'],'元王');self.assertEqual(cell['text'][mention['start']:mention['end']],mention['surface']);mention['person_id']=old;f.write_text(json.dumps(table,ensure_ascii=False))
   with self.assertRaisesRegex(ValueError,'data/historical-tables/shiji-015.json'):retired_person_ids(root)
 def test_derived_data_and_exports_are_not_source_guard_inputs(self):
  with tempfile.TemporaryDirectory()as directory:
   root=self.minimal_root(directory);review=json.loads((root/REVIEW_PATH).read_text());old=review['prior_editorial_record']['id']
   for rel in ['data/corpus/stale-generated.json','exports/persons/stale-generated.json']:
    f=root/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(json.dumps({'person_id':old}))
   self.assertIn(old,retired_person_ids(root))
