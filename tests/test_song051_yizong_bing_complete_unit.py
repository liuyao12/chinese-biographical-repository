"""Complete received unit, typed family limits and visible unresolved age cycle."""
from pathlib import Path
import unittest,copy
from scripts import wyd_song051_yixin as y
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1]
class YizongBing(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.ch,cls.roles,cls.c,cls.docs=y.state(ROOT);cls.catalog=load_catalog(ROOT)
 def test_complete934_source_and_remaining_pending(self):
  u=next(u for u in self.c['additional_complete_units']if u['key']=='yizong-bing');self.assertEqual(sum(len(s['text'])for s in u['scope']),934)
  for s in u['scope']:
   p=next(p for p in self.ch['paragraphs']if p['id']==s['paragraph_id']);self.assertEqual(p['text'][s['start']:s['end']],s['text'])
  self.assertFalse(self.ch['annotation']['human_reviewed']);self.assertTrue(any(p['annotation_status']=='pending'for p in self.ch['paragraphs']))
 def test_raw_two_cousins_not_silently_dropped(self):
  b=bundle(self.roles['bing'],ROOT,include_provisional=True,catalog=self.catalog);d,=b['source_age_order_decisions'];self.assertEqual(len(d['cycle_edges']),7);self.assertEqual(len(d['preserved_direct_brother_assertion_ids']),5)
  raw={a['id']:a for a in b['relations']};pref={a['id']:a for a in b['preferred_relations']}
  for aid in d['affected_relation_ids']:
   self.assertEqual(raw[aid]['qualifiers']['kinship_structure']['subject_relative_age'],'younger');self.assertEqual(pref[aid]['qualifiers']['kinship_structure']['subject_relative_age'],'unknown');self.assertEqual(pref[aid]['relative_age_decision_ref']['id'],d['id'])
 def test_mother_care_and_marriage_do_not_claim_birth(self):
  aa=self.docs['corpus/songshu/051-wyd1739-yizong-assertions.json']['assertions'];m=next(a for a in aa if a['predicate']=='maternal_role');care=next(a for a in aa if a['predicate']=='raised_by');self.assertEqual(m['qualifiers']['role'],'principal_mother');self.assertIsNone(m['qualifiers']['biological_mother']);self.assertEqual(care['qualifiers']['legal_adoption_status'],'not_stated');self.assertFalse(any(a['predicate']=='birth_mother'for a in aa))
 def test_cycle_single_endpoint_rejected_but_consistent_rekey_retained(self):
  c=copy.deepcopy(self.c);c['age_order_conflicts'][0]['cycle_edges'][0]['older_person_id']={'$role':'yz_yin'}
  with self.assertRaises(ValueError):y.validated_age_order_decisions(self.roles,c,self.docs)
  roles={k:'tmp_'+v for k,v in self.roles.items()};docs={p:y.materialize(v,roles)for p,v in self.c['expected_documents'].items()};self.assertEqual(len(y.validated_age_order_decisions(roles,self.c,docs)),1)
if __name__=='__main__':unittest.main()
