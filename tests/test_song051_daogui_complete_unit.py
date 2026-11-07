"""Complete received2149 unit; immutable spelling, maternal path and prior family stages."""
from pathlib import Path
import unittest,copy,json
from scripts import wyd_song051_yixin as y
from scripts.person_bundle import load_catalog,bundle
ROOT=Path(__file__).resolve().parents[1]
class Daogui(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.ch,cls.roles,cls.c,cls.docs=y.state(ROOT);cls.catalog=load_catalog(ROOT)
 def test_complete2149_and_exact_printed_variants(self):
  u=next(u for u in self.c['additional_complete_units']if u['key']=='daogui');self.assertEqual(sum(len(s['text'])for s in u['scope']),2149)
  for s in u['scope']:
   p=next(p for p in self.ch['paragraphs']if p['id']==s['paragraph_id']);self.assertEqual(p['text'][s['start']:s['end']],s['text'])
  self.assertEqual(next(p for p in self.ch['paragraphs']if p['id'].endswith(':p021'))['text'][156:158],'桓謐');self.assertNotEqual(self.roles['dg_huanmi'],self.roles['dg_huanqian']);self.assertTrue(any(p['annotation_status']=='pending'for p in self.ch['paragraphs']))
 def test_maternal_older_cousin_not_paternal_or_common_ancestor(self):
  aa=self.docs['corpus/songshu/051-wyd1739-daogui-assertions.json']['assertions'];a=next(a for a in aa if a['predicate']=='maternal_cousin');k=a['qualifiers']['kinship_structure'];self.assertEqual((a['subject_person_id'],a['object_person_id']),(self.roles['dg_liuzun'],self.roles['dg_daogui']));self.assertEqual((k['lineage'],k['generation_difference'],k['subject_relative_age']),('maternal',0,'older'));self.assertIsNone(k['common_ancestor_person_id']);self.assertIsNone(k['mother_person_id']);self.assertEqual(a['qualifiers']['relative_birth_order']['older_person_id'],a['subject_person_id'])
  pp={p['id']:(self.ch['id'],p)for p in self.ch['paragraphs']};cc={self.ch['id']:self.ch};self.assertTrue(y.family_valid(a,pp,cc,ROOT))
  for bad in[dict(a,predicate='agnatic_cousin'),dict(a,subject_person_id=a['object_person_id'],object_person_id=a['subject_person_id'])]:self.assertFalse(y.family_valid(bad,pp,cc,ROOT))
 def test_old_adoption_care_sequence_and_tactical_false_claim(self):
  raw=json.loads((ROOT/'corpus/songshu/051-wyd1739-identities.json').read_bytes());d=next(d for d in raw['decisions']if d['id']=='d-song051-phase1-taizu');seq=d['historical_succession_reading']['events'];self.assertEqual([e['event_type']for e in seq],['raised_by','ordered_succession','ritual_objection','returned_to_original_line','heir_confirmed']);self.assertTrue(all(e['current_parent_edge_created']is False for e in seq));a=json.loads((ROOT/'corpus/songshu/051-wyd1739-assertions.json').read_bytes());self.assertTrue(any(x['predicate']=='adoptive_father'and x['subject_person_id']==self.roles['dg_yiqing']and x['object_person_id']==self.roles['dg_daogui']for x in a['assertions']));d=next(d for d in self.docs['corpus/songshu/051-wyd1739-daogui-identities.json']['decisions']if d['id']=='d-song051-daogui-hedanzhi');self.assertFalse(d['reported_speech_qualification']['asserts_actual_death'])
 def test_six_actual_profiles_and_source_names(self):
  for role in ['xunlin','liuzun','caozhongzong','daoer','caimeng','liuji','huanmi']:
   b=bundle(self.roles['dg_'+role],ROOT,include_provisional=True,catalog=self.catalog);self.assertEqual(b['canonical_person_id'],self.roles['dg_'+role]);self.assertTrue(b['mentions']);self.assertTrue(b['name_components'])
  n=next(n for n in self.docs['corpus/songshu/051-wyd1739-daogui-name-components.json']['records']if n['id']=='name-song051-daogui-restored-daoer');self.assertEqual((n['surname'],n['ming']),('桓','道兒'));self.assertEqual(n['surname_basis']['source_assertion_ids'],['a-song051-yixin-daogui-daoer-father'])
 def test_huanmi_source_local_and_unresolved_identity_not_glyph_change(self):
  d=next(d for d in self.docs['corpus/songshu/051-wyd1739-daogui-identities.json']['decisions']if d['id']=='d-song051-daogui-huanmi');self.assertEqual(d['person_id'],self.roles['dg_huanmi']);self.assertEqual(d['scope'],'same_chapter');a=d['identity_alternatives'][0];self.assertEqual(a['candidate_person_id'],self.roles['dg_huanqian']);self.assertEqual(a['status'],'unresolved');self.assertIs(a['preferred'],False);self.assertIs(a['global_not_same_asserted'],False);self.assertIn('馬頭',a['positive_evidence'][-1]['quote'])
  m=json.loads((ROOT/a['counterevidence_ref']).read_bytes());self.assertEqual(m['revision_id'],617578);self.assertIn('桓謙、桓怡、桓蔚、桓謐',m['counterevidence']['quote']);self.assertIsNone(m['edition']);self.assertFalse(m['image_verified'])
  n=next(n for n in self.docs['corpus/songshu/051-wyd1739-daogui-name-components.json']['records']if n['id']=='name-song051-daogui-literal-huanmi');self.assertEqual((n['surname'],n['ming'],n['person_id']),('桓','謐',self.roles['dg_huanmi']))
if __name__=='__main__':unittest.main()
