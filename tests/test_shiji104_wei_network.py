import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class WeiNetwork(unittest.TestCase):
 def test_three_contextual_identities_and_retired_ids(self):
  c=json.loads((ROOT/'corpus/shiji/104.json').read_text());ids={m.get('person_id') for p in c['paragraphs'] for m in p['mentions']}
  self.assertFalse(ids & {'hmf_0gk_k9w','6bp_mr9_l3w','3xa_jvi_o6n'})
  self.assertTrue({'5dd_l1c_6g8','nad_18h_5jc','vkr_lkp_dme'}<=ids)
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m['surface']=='衛將軍':self.assertEqual(m['person_id'],'5dd_l1c_6g8')
    if m['surface']=='平陽主':self.assertEqual(m['person_id'],'nad_18h_5jc')
 def test_shared_household_does_not_make_kinship(self):
  c=json.loads((ROOT/'corpus/shiji/104.json').read_text());p=next(p for p in c['paragraphs'] if p['id'].endswith('p011'))
  self.assertEqual(p['text_layer'],'witness_appended_chu_note')
  self.assertIn('俱為舍人',p['text'])
  eq=json.loads((ROOT/'corpus/shiji/104-equivalences.json').read_text())
  rows=[r for r in eq['decisions'] if r['id'].startswith('eq-shiji104-wei-')]
  self.assertEqual(len(rows),3)
  self.assertTrue(all('不補任官絕對年' in r['rationale'] for r in rows))
 def test_zhaoyu_has_explicit_shaofu_parallel(self):
  eq=json.loads((ROOT/'corpus/shiji/104-equivalences.json').read_text())
  r=next(r for r in eq['decisions'] if r['id']=='eq-shiji104-wei-003')
  self.assertTrue(any('趙禹遷爲中尉，徙爲少府' in e['quote'] for e in r['evidence']))
  self.assertTrue(any('少府趙禹' in e['quote'] for e in r['evidence']))
