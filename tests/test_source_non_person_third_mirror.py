import unittest,json,copy,tempfile,shutil
from pathlib import Path
from scripts.retired_person_ids import retired_person_ids
from scripts.source_non_person_retirement import REVIEW_PATH,RECEIPT_PATH
ROOT=Path(__file__).resolve().parents[1];THIRD='source-evidence/shiji130-remaining11-identity/context-reading.json'
class ThirdMirror(unittest.TestCase):
 def test_exact_third_classification_and_receipt(self):
  d=json.loads((ROOT/THIRD).read_bytes());review=json.loads((ROOT/REVIEW_PATH).read_bytes());unit=next(u for u in d['complete_units']if u['paragraph']['id']=='c-shiji-130-taishigong:p049');m=next(m for m in unit['paragraph']['mentions']if m['id']=='c-shiji-130-taishigong:m049-0025');self.assertEqual(m,review['classification']);self.assertEqual(review['current_reading_mirrors'][-1],THIRD);self.assertIn(json.loads((ROOT/RECEIPT_PATH).read_bytes())['retired_person_ids'][0],retired_person_ids(ROOT))
 def test_wrong_source_quote_and_restored_person_rejected(self):
  # No source-tree writes: inject a changed payload at the real file read boundary in memory only.
  from unittest.mock import patch
  original=Path.read_text;target=(ROOT/THIRD).resolve();base=json.loads(original(target))
  for mode in ['source','quote','person']:
   d=copy.deepcopy(base);u=next(u for u in d['complete_units']if u['paragraph']['id']=='c-shiji-130-taishigong:p049')
   if mode=='source':u['source']['revision_id']=1
   if mode=='quote':u['paragraph']['text']='錯'+u['paragraph']['text']
   if mode=='person':
    m=next(m for m in u['paragraph']['mentions']if m['id']=='c-shiji-130-taishigong:m049-0025');m['kind']='person';m['person_id']='hidden_old_person'
   payload=json.dumps(d,ensure_ascii=False)
   def view(path,*args,**kwargs):return payload if path.resolve()==target else original(path,*args,**kwargs)
   with patch.object(Path,'read_text',view):
    with self.assertRaises(ValueError):retired_person_ids(ROOT)
if __name__=='__main__':unittest.main()
