"""Fixed-source facts regressions; no private files, network or derived data required."""
import copy,json,unittest
from pathlib import Path
from scripts.age_context import age_context_valid
from scripts.named_posthumous_naming import named_posthumous_naming_valid
from scripts.validate_corpus import direct_source_age_valid
class XunFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((Path(__file__).parent/'fixtures/houhan062_xun_facts44.json').read_text());cls.d=cls.f['delta'];cls.paragraphs={p['id']:(cls.f['chapter_id'],p)for p in cls.f['paragraphs']};cls.mentions={m['id']:(cls.f['chapter_id'],p['id'],m)for p in cls.f['paragraphs']for m in p['mentions']};cls.events={o['after']['id']:o['after']for o in cls.d['life_operations']};cls.death=cls.events['le-houhan062-xun43-jing-death'];cls.age=next(o['after']for o in cls.d['age_operations']if o['after']['person_id']==cls.death['person_id']);cls.h=next(o['after']for o in cls.d['title_operations']if o['after']['mode']=='posthumous_naming')
 def test_one_death_two_sources_age50_and_named_honorific(self):
  self.assertEqual(1,sum(e['person_id']==self.death['person_id']for e in self.events.values()));self.assertEqual(2,len(self.death['evidence']));self.assertEqual(50,self.age['value']);self.assertTrue(age_context_valid(self.age,self.events));self.assertTrue(direct_source_age_valid(self.age));self.assertTrue(named_posthumous_naming_valid(self.h,self.paragraphs,self.mentions,self.events))
 def test_wrong_person_age_rejected(self):
  a=copy.deepcopy(self.age);a['person_id']='someone_else';self.assertFalse(age_context_valid(a,self.events))
 def test_wrong_event_rejected(self):
  e=copy.deepcopy(self.events);e[self.death['id']]['event_type']='birth';self.assertFalse(age_context_valid(self.age,e))
 def test_empty_age_evidence_rejected(self):
  a=copy.deepcopy(self.age);a['evidence']=[];self.assertFalse(age_context_valid(a,self.events))
 def test_age_scope_outside_death_rejected(self):
  a=copy.deepcopy(self.age);a['evidence'][0]['paragraph_id']='outside';self.assertFalse(age_context_valid(a,self.events))
 def test_age_value_not_from_original_rejected(self):
  a=copy.deepcopy(self.age);a['value']=26;self.assertFalse(direct_source_age_valid(a))
 def test_wrong_recipient_rejected(self):
  h=copy.deepcopy(self.h);h['person_id']='someone_else';self.assertFalse(named_posthumous_naming_valid(h,self.paragraphs,self.mentions,self.events))
 def test_borrowed_death_rejected(self):
  h=copy.deepcopy(self.h);h['naming_basis']['death_event_id']='le-houhan062-xun44-shuang-death';self.assertFalse(named_posthumous_naming_valid(h,self.paragraphs,self.mentions,self.events))
 def test_wrong_issuer_rejected(self):
  h=copy.deepcopy(self.h);h['naming_basis']['issuer_person_mention_id']=h['naming_basis']['recipient_person_mention_id'];self.assertFalse(named_posthumous_naming_valid(h,self.paragraphs,self.mentions,self.events))
 def test_false_naming_offset_rejected(self):
  h=copy.deepcopy(self.h);h['naming_basis']['naming_anchor']['start']-=1;self.assertFalse(named_posthumous_naming_valid(h,self.paragraphs,self.mentions,self.events))
 def test_posthumous_not_lifetime_appointment(self):
  self.assertEqual('honorific',self.h['kind']);self.assertEqual('posthumous_naming',self.h['mode']);self.assertIsNone(self.h['effective_period']['start']['date_expression']);self.assertTrue(self.h['naming_basis']['source_term'].endswith('先生也'))
 def test_deaths_no_backcalculated_birth(self):
  for e in self.events.values():self.assertNotIn('birth_year',e)
  for a in self.d['age_operations']:self.assertIsNone(a['after']['birth_year'])
  s=next(e for e in self.events.values()if e['person_id']=='yoo_ox0_545_F');self.assertIsNone(s['date_expression']);self.assertNotIn('normalized_date',s)
 def test_yue209_and_zhaodian158_attestation_not_start(self):
  y=next(e for e in self.events.values()if e['person_id']=='yoo_ox0_545_AA');self.assertEqual(209,y['normalized_date']['year']);self.assertEqual('建安十四年',y['date_expression'])
  z=next(o['after']for o in self.d['title_operations']if o['after']['id']=='th-houhan062-xun44-076');self.assertEqual('unknown',z['effective_period']['start']['status']);self.assertEqual(158,z['attestations'][0]['normalized_date']['year'])
 def test_refused_or_interrupted_not_held(self):
  ss=[o['after']for o in self.d['title_operations']if o['after']['person_id']=='yoo_ox0_545_F'];self.assertNotIn('從事中郎',[x['title']for x in ss]);self.assertNotIn('侍中',[x['title']for x in ss]);self.assertEqual('grant',next(h for h in ss if h['title']=='平原相')['mode'])
 def test_only_three_explicit_resignations(self):
  ended=[o['after']for o in self.d['title_operations']if o['after']['effective_period']['end']['status']=='source_event'];self.assertEqual({'當塗長','朗陵侯相','郎中'},{h['title']for h in ended});self.assertTrue(all(h['effective_period']['end']['date_expression']is None for h in ended))
 def test_waypoint_not_residence_or_deathplace(self):
  places=[o['after']for o in self.d['address_additions']];self.assertNotIn('宛陵',[a['place']['source_name']for a in places]);self.assertFalse(any(a['relation']in('birth_place','death_place','burial_place')for a in places))
 def test_all195_consumed_without_erasing_typed_scope(self):self.assertEqual(195,sum(self.f['ledger_counts'].values()));self.assertGreater(self.f['ledger_counts']['typed_retained'],0)
if __name__=='__main__':unittest.main()
