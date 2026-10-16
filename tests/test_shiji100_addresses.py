import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def rows():return json.loads((ROOT/'corpus/shiji/100-addresses.json').read_text())['assertions']
class JibuAddressTests(unittest.TestCase):
 def test_refuge_is_not_native_or_birth_place(self):
  for pid,place in [('udu_dyy_4wd','濮陽'),('cte_yao_v47','呉')]:
   rs=[r for r in rows() if r['person_id']==pid and r['place']['source_name']==place];self.assertEqual(len(rs),1);self.assertEqual(rs[0]['relation'],'residence');self.assertIsNone(rs[0]['place']['modern_identification'])
  self.assertEqual({r['place']['source_name'] for r in rows() if r['relation']=='biographical_origin'},{'楚','梁'})
 def test_luan_qi_employment_and_diplomatic_mission_are_separate(self):
  rs=[r for r in rows() if r['person_id']=='jx9_cov_qe0' and r['place']['source_name']=='齊'];self.assertEqual(len(rs),2)
  self.assertEqual({r['qualifiers']['source_position'] for r in rs},{'酒人保','使'});self.assertTrue(all(r['relation']=='service_location' for r in rs));self.assertEqual(len({r['evidence'][0]['paragraph_id'] for r in rs}),2)
 def test_governorship_is_not_unrealized_censor_office_or_continuous_tenure(self):
  r=next(r for r in rows() if r['place']['source_name']=='河東');self.assertEqual(r['qualifiers']['source_position'],'河東守');self.assertNotIn('御史大夫',r['source_term'])
  for r in rows():self.assertIsNone(r['place']['modern_identification']);self.assertNotIn('normalized_date',r);self.assertNotIn('reported_duration',r)
  self.assertFalse(any(r['relation'] in ['death_place','burial_place','birth_place'] for r in rows()))
