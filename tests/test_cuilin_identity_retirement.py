"""Source-specific identity decision, not a surname-wide equivalence."""
import json, unittest
from pathlib import Path
try:
 from scripts.retired_person_ids import retired_person_ids, allocation_conflicts
except ImportError:
 from retired_person_ids import retired_person_ids, allocation_conflicts
ROOT=Path(__file__).resolve().parents[1]
class CuilinIdentityRetirement(unittest.TestCase):
 def test_inverse_anchors_and_no_alias(self):
  people={x['id']:x for x in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
  keep=people['9g7_n2e_6ho'];self.assertNotIn('cvr_exv_dku',people)
  self.assertNotIn('cvr_exv_dku',[a for x in people.values()for a in x.get('id_aliases',[])])
  for path,pid,mid in [('corpus/weishu-weishou/024-cuixuanbo.json','c-weishu-weishou-024-cuixuanbo:p001','m0019'),('corpus/beishi/021-cuihong.json','c-beishi-021-cuihong:p001','m0014')]:
   c=json.loads((ROOT/path).read_text());p=next(p for p in c['paragraphs']if p['id']==pid);m=next(m for m in p['mentions']if m['id']==pid+':'+mid)
   self.assertEqual((m['surface'],m['person_id']),('林',keep['id']));self.assertTrue(any(e['mention_id']==m['id']for e in keep['evidence']))
 def test_premerge_notes_do_not_claim_new_support(self):
  keep=next(x for x in json.loads((ROOT/'registry/persons.json').read_text())['persons']if x['id']=='9g7_n2e_6ho')
  old_mids={'c-weishu-weishou-024-cuixuanbo:p001:m0019','c-beishi-021-cuihong:p001:m0014'}
  prior=[x for x in keep['source_identity_notes']if x.get('prior_label')=='崔林']
  self.assertEqual(len(prior),1);self.assertEqual(len(prior[0]['source_mention_ids']),24);self.assertFalse(old_mids.intersection(prior[0]['source_mention_ids']))
  separate=[x for x in keep['source_identity_notes']if x.get('prior_label')=='林〔魏司空，玄伯六世祖〕']
  self.assertEqual(len(separate),1);self.assertEqual(set(separate[0]['source_mention_ids']),old_mids)
 def test_reported_generation_not_fabricated_distance(self):
  a=next(a for a in json.loads((ROOT/'corpus/weishu-weishou/024-cuixuanbo-assertions.json').read_text())['assertions']if a['id']=='a-cui53-012')
  self.assertEqual(a['object_person_id'],'9g7_n2e_6ho');self.assertEqual(a['qualifiers']['reported_generational_term'],'六世孫');self.assertIsNone(a['qualifiers']['generation_distance']);self.assertTrue(a['qualifiers']['not_used_for_family_id_placement'])
 def test_retired_reservations(self):
  reserved=retired_person_ids(ROOT);self.assertIn('cvr_exv_dku',reserved)
  for candidate in ('cvr_exv_dku','cvr_exv_dku_A'):self.assertTrue(allocation_conflicts(candidate,reserved))
 def test_decision_source_specific(self):
  d=next(d for d in json.loads((ROOT/'corpus/sanguozhi/024-cuilin-identities.json').read_text())['decisions']if d['id']=='d-sgz024-cuilin-weishu024-lin')
  self.assertEqual(d['scope'],'cross_chapter');self.assertEqual(d['status'],'contextual_provisional');self.assertFalse(d['human_reviewed']);self.assertEqual(len(d['evidence']),4)
  self.assertTrue(any('司隸校尉' in e['quote']and'司空' in e['quote']for e in d['evidence']))
if __name__=='__main__':unittest.main()
