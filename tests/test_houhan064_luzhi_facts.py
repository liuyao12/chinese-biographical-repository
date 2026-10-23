import unittest,json,copy,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class LayeredBiographyFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  from scripts import layered_biography_titles as L
  cls.L=L;cls.ch=json.loads((R/'corpus/houhanshu/064-luzhi.json').read_text());cls.hs=json.loads((R/'corpus/houhanshu/064-luzhi-titles.json').read_text())['holdings'];cls.rs=json.loads((R/'corpus/houhanshu/064-luzhi-assertions.json').read_text())['assertions'];cls.ps={p['id']:(cls.ch['id'],p)for p in cls.ch['paragraphs']};cls.proposal=next(p for p in cls.ch['annotation']['title_proposals']if p['id']=='proposal-hhs064-luzhi-junshi');cls.events=json.loads((R/'corpus/houhanshu/064-luzhi-life-events.json').read_text())['events'];cls.people={m['person_id']for p in cls.ch['paragraphs']for m in p['mentions']if m.get('person_id')}
 def h(self,rule,recipient='subject'):return copy.deepcopy(next(h for h in self.hs if h['source_career_role']['rule']==rule and h['source_career_role']['recipient_role']==recipient))
 def test_all_28_source_titles(self):
  self.assertEqual(len(self.hs),28)
  for h in self.hs:self.assertTrue(self.L.holding_valid(h,self.ch),h['id'])
 def test_wrong_recipient_each_title(self):
  for old in self.hs:
   h=copy.deepcopy(old);h['person_id']=next(p for p in self.people if p!=h['person_id']);self.assertFalse(self.L.holding_valid(h,self.ch),h['id'])
 def test_no_death_as_all_tenure_ends(self):
  for old in self.hs:
   h=copy.deepcopy(old);h['effective_period']['end']=dict(status='source_event',event_type='explicit_end',date_expression='初平三年',evidence=h['evidence']);self.assertFalse(self.L.holding_valid(h,self.ch))
 def test_source_hash_and_offset(self):
  for old in self.hs:
   h=copy.deepcopy(old);h['source_career_role']['paragraph_sha256']='0'*64;self.assertFalse(self.L.holding_valid(h,self.ch))
  h=self.h('summoned_then_governor');h['source_career_role']['fields']['office1']['start']+=1;self.assertFalse(self.L.holding_valid(h,self.ch))
 def test_court_context_not_nearest_ruler(self):
  h=self.h('court_after_governorship');h['source_career_role']['roles']['subject']=h['source_career_role']['roles']['ruler'];self.assertFalse(self.L.holding_valid(h,self.ch))
 def test_context_cannot_drop_annotation(self):
  h=self.h('court_after_governorship');ctx=h['source_career_role']['subject_context'];ctx['paragraph_ids'].pop(1);self.assertFalse(self.L.holding_valid(h,self.ch))
 def test_other_body_breaks_continuation(self):
  h=self.h('court_after_governorship');ch=copy.deepcopy(self.ch);ctx=h['source_career_role']['subject_context'];idx=next(i for i,p in enumerate(ch['paragraphs'])if p['id']==ctx['paragraph_ids'][1]);ch['paragraphs'][idx]['text_layer']='received_chapter';ctx['full_paragraphs'][1]['source_position']=ch['paragraphs'][idx]['source_position'];self.assertFalse(self.L.holding_valid(h,ch))
 def test_178_not_previous_office_start(self):
  h=self.h('court_after_governorship');h['effective_period']['start']['date_expression']='光和元年';self.assertFalse(self.L.holding_valid(h,self.ch))
 def test_building_centre_not_one_year(self):
  from scripts.civil_era_ranges import civil_era_range_errors
  h=self.h('summoned_then_governor');n=h['effective_period']['start']['normalized_date_range'];self.assertEqual([n['earliest']['year'],n['latest']['year']],[168,172]);self.assertEqual(n['source_expression'],'建寜中');self.assertEqual(civil_era_range_errors(n,h['evidence'],'建寜中'),[]);n['earliest']['year']=170;self.assertTrue(civil_era_range_errors(n,h['evidence'],'建寜中'))
 def test_era_variant_not_arbitrary_name(self):
  from scripts.civil_era_ranges import civil_era_range_errors
  h=self.h('summoned_then_governor');n=h['effective_period']['start']['normalized_date_range'];n['era_span_mapping']['source_era_name']='未知';self.assertTrue(civil_era_range_errors(n,h['evidence'],'未知中'))
 def test_same_year_not_next_year(self):
  from scripts.validate_corpus import normalized_date_errors
  h=self.h('restored_after_campaign_report');h=next(x for x in self.hs if x['source_career_role']['rule']=='restored_after_campaign_report'and x['appointment_role']=='reappointment');n=copy.deepcopy(h['effective_period']['start']['normalized_date']);self.assertEqual(n['year'],184);self.assertFalse(normalized_date_errors(n,{self.ch['id']:self.ch},R));n['year']=n['era_year']=185;self.assertTrue(normalized_date_errors(n,{self.ch['id']:self.ch},R))
 def test_intervening_era_breaks_same_year(self):
  h=next(x for x in self.hs if x['source_career_role']['rule']=='restored_after_campaign_report'and x['appointment_role']=='reappointment');n=copy.deepcopy(h['effective_period']['start']['normalized_date']);ch=copy.deepcopy(self.ch);p=next(p for p in ch['paragraphs']if p['id']==n['narrative_era_scope']['paragraph_id']);at=10;insert='光和二年';p['text']=p['text'][:at]+insert+p['text'][at:];b=n['narrative_era_scope'];b['full_quote']=p['text'];b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();b['event_anchor']['start']+=len(insert);b['event_anchor']['end']+=len(insert)
  for e in n['evidence']:e['quote']=p['text']
  self.assertFalse(self.L.same_paragraph_year_valid(n,{ch['id']:ch}))
 def test_offer_not_refusal_or_fulfilment(self):
  q=copy.deepcopy(self.proposal);self.assertEqual(self.L.offered_errors(q,self.ch,self.people),[])
  for k,v in [('outcome','not_assumed'),('effective_service_attested',True),('non_assumption_anchor',{})]:
   d=copy.deepcopy(q);d[k]=v;self.assertTrue(self.L.offered_errors(d,self.ch,self.people))
 def test_offer_not_issuer(self):
  q=copy.deepcopy(self.proposal);b=q['source_appointment_context'];p=self.ps[b['paragraph_id']][1];q['person_id']=next(m['person_id']for m in p['mentions']if m['id']==b['roles']['issuer']);self.assertTrue(self.L.offered_errors(q,self.ch,self.people))
 def test_fathers_direction_and_no_biological_mother(self):
  for a in self.rs[:3]:
   self.assertTrue(self.L.family_valid(a,self.ps,{self.ch['id']:self.ch}));d=copy.deepcopy(a);d['subject_person_id'],d['object_person_id']=d['object_person_id'],d['subject_person_id'];self.assertFalse(self.L.family_valid(d,self.ps,{self.ch['id']:self.ch}));d=copy.deepcopy(a);d['qualifiers']['biological_mother_person_id']='invented';self.assertFalse(self.L.family_valid(d,self.ps,{self.ch['id']:self.ch}))
 def test_two_learners_not_siblings(self):
  for a in self.rs[3:]:
   self.assertTrue(self.L.teaching_valid(a,self.ps));d=copy.deepcopy(a);d['predicate']='brother';self.assertFalse(self.L.teaching_valid(d,self.ps))
 def test_death_subject_not_yuan_shao_or_son(self):
  e=copy.deepcopy(self.events[0]);ctx=e['evidence'][0]['context'];self.assertTrue(self.L.death_context_valid(ctx,e,self.ch,e['evidence'][0]));e['person_id']=next(m['person_id']for p in self.ch['paragraphs']for m in p['mentions']if m['id']==ctx['issuer_mention_id']);self.assertFalse(self.L.death_context_valid(ctx,e,self.ch,e['evidence'][0]))
 def test_orphan_age_does_not_create_birth(self):
  age=next(a for a in self.ch['annotation']['age_assertions']if a['id']=='age-hhs064-yu-orphan-ten');self.assertEqual(age['value'],10);self.assertIsNone(age['birth_year']);self.assertFalse(any(e['event_type']=='birth'for e in self.events));self.assertIsNone(self.events[0].get('place'))
 def test_posthumous_title_is_attestation(self):
  h=next(h for h in self.hs if h['source_career_role']['rule']=='past_prefix_office'and h['evidence'][0]['paragraph_id'].endswith(':p008'));self.assertEqual(h['mode'],'attestation');self.assertEqual(h['effective_period']['start']['status'],'unknown');self.assertEqual(h['attestations'][0]['normalized_date_range']['latest']['year'],220)
 def test_generic_ids_not_name_allowlist(self):
  h=self.h('prefix_office');ch=copy.deepcopy(self.ch);pid=h['person_id'];new='abc_def_123';h['person_id']=new
  for p in ch['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')==pid:m['person_id']=new
  self.assertTrue(self.L.holding_valid(h,ch))
 def test_addresses_bound_to_actual_people(self):
  rows=json.loads((R/'corpus/houhanshu/064-luzhi-addresses.json').read_text())['assertions']
  for a in rows:
   self.assertTrue(self.L.address_valid(a,self.ch));d=copy.deepcopy(a);d['person_id']=next(p for p in self.people if p!=a['person_id']);self.assertFalse(self.L.address_valid(d,self.ch))
 def test_seclusion_not_death_and_wrong_repeat(self):
  a=next(a for a in json.loads((R/'corpus/houhanshu/064-luzhi-addresses.json').read_text())['assertions']if a['relation']=='residence');d=copy.deepcopy(a);d['relation']='death_place';self.assertFalse(self.L.address_valid(d,self.ch));d=copy.deepcopy(a);p=self.ps[a['evidence'][0]['paragraph_id']][1];other=next(m for m in p['mentions']if m['surface']=='卓');d['source_address_binding']['roles']['pursuer']=other['id'];self.assertFalse(self.L.address_valid(d,self.ch))
 def test_shared_wei_not_jing_ke(self):
  a=next(a for a in json.loads((R/'corpus/houhanshu/064-luzhi-addresses.json').read_text())['assertions']if a['relation']=='source_locality_designation');p=self.ps[a['evidence'][0]['paragraph_id']][1];jing=next(m for m in p['mentions']if m['surface']=='荆軻');d=copy.deepcopy(a);d['person_id']=jing['person_id'];d['evidence'][0]['person_mention_id']=jing['id'];d['source_address_binding']['roles']['one']=jing['id'];d['source_address_binding']['subject_role']='one';self.assertFalse(self.L.address_valid(d,self.ch))
 def test_departure_reports_do_not_end_all_offices(self):
  rows=json.loads((R/'corpus/houhanshu/064-luzhi-source-details.json').read_text())['records'];holdings={h['id']:h for h in self.hs}
  for a in rows:self.assertTrue(self.L.detail_valid(a,self.ch,holdings))
  a=next(a for a in rows if a['kind']=='office_departure');d=copy.deepcopy(a);d['values']['all_other_offices_ended']=True;self.assertFalse(self.L.detail_valid(d,self.ch,holdings))
 def test_queen_death_not_dreamer(self):
  a=next(a for a in self.events if a['id']=='le-hhs064-song-empress-note');self.assertTrue(self.L.explicit_death_report_valid(a,self.ch));p=self.ps[a['evidence'][0]['paragraph_id']][1];other=next(m for m in p['mentions']if m['surface']=='靈帝');d=copy.deepcopy(a);d['person_id']=other['person_id'];d['evidence'][0]['person_mention_id']=other['id'];d['source_layered_death_report']['roles']['subject']=other['id'];self.assertFalse(self.L.explicit_death_report_valid(d,self.ch))
 def test_undated_death_not_memorial_year(self):
  for a in self.events[1:]:
   self.assertTrue(self.L.explicit_death_report_valid(a,self.ch));d=copy.deepcopy(a);d['date_expression']='光和元年';self.assertFalse(self.L.explicit_death_report_valid(d,self.ch))
 def test_intervening_next_year_breaks_same_year(self):
  h=next(x for x in self.hs if x['source_career_role']['rule']=='restored_after_campaign_report'and x['appointment_role']=='reappointment');n=copy.deepcopy(h['effective_period']['start']['normalized_date']);ch=copy.deepcopy(self.ch);p=next(p for p in ch['paragraphs']if p['id']==n['narrative_era_scope']['paragraph_id']);at=10;p['text']=p['text'][:at]+'明年'+p['text'][at:];b=n['narrative_era_scope'];b['full_quote']=p['text'];b['paragraph_sha256']=hashlib.sha256(p['text'].encode()).hexdigest();b['event_anchor']['start']+=2;b['event_anchor']['end']+=2
  for e in n['evidence']:e['quote']=p['text']
  self.assertFalse(self.L.same_paragraph_year_valid(n,{ch['id']:ch}))
