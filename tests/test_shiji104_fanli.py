import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class FanLiCrossChapters(unittest.TestCase):
 def test_four_accounts_share_existing_person(self):
  for num in ['041','104','126','129']:
   c=json.loads((ROOT/f'corpus/shiji/{num}.json').read_text());ms=[m for p in c['paragraphs']for m in p['mentions']if m['surface']=='范蠡']
   self.assertTrue(ms);self.assertTrue(all(m.get('person_id')=='yhm_h9f_8p0'for m in ms))
 def test_comparisons_stay_in_chu_layers(self):
  for num,tail in [('104','p016'),('126','p016')]:
   c=json.loads((ROOT/f'corpus/shiji/{num}.json').read_text());p=next(p for p in c['paragraphs']if p['id'].endswith(tail));self.assertEqual(p['text_layer'],'witness_appended_chu_note')
  d=json.loads((ROOT/'corpus/shiji/104-equivalences.json').read_text());r=next(r for r in d['decisions']if r['id']=='eq-shiji104-fanli');self.assertIn('不獨立證成',r['rationale']);self.assertTrue(r['identity_materialized'])
 def test_retired_candidates_are_removed_and_children_preserved(self):
  d=json.loads((ROOT/'registry/persons.json').read_text());ids={p['id']for p in d['persons']};self.assertFalse(ids&{'m5g_nw3_pnt','lix_yk4_xqp','ibh_9if_1dv'})
  self.assertTrue({'yhm_h9f_8p0_A','yhm_h9f_8p0_B','yhm_h9f_8p0_C'}<=ids)
