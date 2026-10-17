import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AgeAddress(unittest.TestCase):
 def test_source_ages_do_not_infer_birth(self):
  c=json.loads((ROOT/'corpus/shiji/105.json').read_text());ages=c['annotation']['age_assertions'];self.assertEqual(len(ages),3)
  a,b,d=ages;self.assertEqual(len(a['evidence']),2);self.assertEqual(a['bounds']['lower'],70);self.assertFalse(a['bounds']['lower_inclusive']);self.assertEqual(b['value'],39);self.assertIsNone(d['value']);self.assertEqual(d['bounds']['upper'],20);self.assertFalse(d['bounds']['upper_inclusive']);self.assertTrue(all(x['birth_year'] is None for x in ages))
 def test_locality_question_preserves_tangan_native(self):
  rows=json.loads((ROOT/'corpus/shiji/105-addresses.json').read_text())['assertions'];a=next(a for a in rows if a['id']=='pa-shiji105-010');self.assertEqual(a['relation'],'native_place');self.assertIn('何縣里人',a['evidence'][0]['quote']);self.assertEqual(sum(a['relation']=='source_locality_designation' for a in rows),6)
 def test_residences_remain_distinct_from_origin(self):
  rows=json.loads((ROOT/'corpus/shiji/105-addresses.json').read_text())['assertions'];r=[a for a in rows if a['relation']=='residence'];self.assertEqual({a['source_term'] for a in r},{'家在於鄭','身居陽虛侯國'});self.assertTrue(all(a['place']['modern_identification'] is None for a in rows))
