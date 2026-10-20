import unittest,json,copy
from pathlib import Path
from scripts.cross_chapter_annal_date import cross_chapter_annal_date_valid
from scripts.validate_corpus import normalized_date_errors,source_age_number,direct_source_age_valid
from scripts.source_date_parts import source_date_parts_valid
from scripts.maternal_roles import maternal_role_valid
from scripts.reported_grandmother import reported_grandmother_valid
from scripts.directed_uncle_roles import paternal_uncle_direction_valid
from scripts.retrospective_parent_honorific import parent_honorific_grant_valid
Q=Path(__file__).parent/'fixtures/houhan009_fact_model/fixture.json'
class Houhan009FactModel(unittest.TestCase):
 def setUp(self):
  f=json.loads(Q.read_text());self.f=f;self.ch=f['chapters'];self.death=f['death'];self.title=f['title'];self.ps={p['id']:(c['id'],p)for c in self.ch.values()for p in c['paragraphs']}
 def valid(self,r=None,role='life_event'):
  r=r or self.death;d=r['normalized_date']if role=='life_event'else r['effective_period']['start']['normalized_date'];return cross_chapter_annal_date_valid(d,r,role,self.ch)and not normalized_date_errors(d,self.ch)
 def test_actual_same_death_190_and_chinese_may(self):
  self.assertTrue(self.valid());self.assertTrue(source_date_parts_valid(self.death,self.ch,source_age_number));self.assertEqual(self.death['source_date_parts']['month'],5);self.assertIsNone(self.death['source_date_parts']['day']);self.assertEqual(self.death['normalized_date']['precision'],'year')
 def test_actual_same_grant_189(self):self.assertTrue(self.valid(self.title,'start'))
 def test_wrong_year(self):
  self.death['normalized_date'].update(year=191,era_year=191);self.assertFalse(self.valid())
 def test_wrong_era(self):
  self.death['normalized_date']['regnal_year_mapping']['era_name']='光和';self.assertFalse(self.valid())
 def test_wrong_record(self):
  self.death['normalized_date']['cross_chapter_event_binding']['record_id']='other-event';self.assertFalse(self.valid())
 def test_wrong_person(self):
  self.death['person_id']='a50_1e6_4bf';self.assertFalse(self.valid())
 def test_wrong_original_death(self):
  self.death['source_term']='卒';self.assertFalse(self.valid())
 def test_different_source_revision(self):
  side=self.death['normalized_date']['cross_chapter_event_binding']['annal'];self.ch[side['chapter_id']]['source']['revision_id']='different';self.assertFalse(self.valid())
 def test_wrong_source_fingerprint(self):
  self.death['normalized_date']['cross_chapter_event_binding']['annal']['fingerprint']['raw_sha256']='0'*64;self.assertFalse(self.valid())
 def test_cannot_jump_to_another_year_paragraph(self):
  b=self.death['normalized_date']['cross_chapter_event_binding']['annal'];b['paragraph_id']=next(p['id']for c in self.ch.values()for p in c['paragraphs']if p['id'].endswith(':accession-zhongping06'));self.assertFalse(self.valid())
 def test_source_text_changed(self):
  b=self.death['normalized_date']['cross_chapter_event_binding']['annal'];p=self.ps[b['paragraph_id']][1];p['text']=p['text'].replace('荀爽薨','荀爽生');self.assertFalse(self.valid())
 def test_date_clause_not_another_person(self):
  b=self.title['effective_period']['start']['normalized_date']['cross_chapter_event_binding']['annal'];p=self.ps[b['paragraph_id']][1];i=p['text'].index('為司空');b['event_anchor']={'paragraph_id':p['id'],'start':i,'end':i+3,'surface':'為司空'};self.assertFalse(self.valid(self.title,'start'))
 def test_annal_note_not_annual_body(self):
  b=self.death['normalized_date']['cross_chapter_event_binding']['annal'];self.ps[b['paragraph_id']][1]['source_position']['source_layer']='lixian_commentary';self.assertFalse(self.valid())
 def test_wrong_month_and_not_gregorian(self):
  self.death['source_date_parts']['month']=6;self.assertFalse(source_date_parts_valid(self.death,self.ch,source_age_number));self.death['source_date_parts']['month']=5;self.death['source_date_parts']['calendar']='gregorian';self.assertFalse(source_date_parts_valid(self.death,self.ch,source_age_number))
 def test_cannot_invent_day_or_leap(self):
  self.death['source_date_parts']['day']=1;self.assertFalse(source_date_parts_valid(self.death,self.ch,source_age_number));self.death['source_date_parts']['day']=None;self.death['source_date_parts']['leap_month']=False;self.assertFalse(source_date_parts_valid(self.death,self.ch,source_age_number))
 def test_three_maternal_roles_not_birth_mothers(self):
  aa=[a for a in self.f['relations']if a['predicate']=='maternal_role'];self.assertEqual(len(aa),3)
  for a in aa:self.assertTrue(maternal_role_valid(a,self.ps));self.assertIsNone(a['qualifiers']['biological_mother'])
 def test_maternal_wrong_child(self):
  a=next(a for a in self.f['relations']if a['predicate']=='maternal_role');a['subject_person_id']='0wg_vtn_yqb';self.assertFalse(maternal_role_valid(a,self.ps))
 def test_cannot_turn_into_birth_mother(self):
  a=next(a for a in self.f['relations']if a['predicate']=='maternal_role');a['qualifiers']['biological_mother']=True;self.assertFalse(maternal_role_valid(a,self.ps))
 def test_grandmother_lineage_unknown(self):
  a=next(a for a in self.f['relations']if a['predicate']=='grandmother');self.assertTrue(reported_grandmother_valid(a,self.ps));self.assertEqual(a['qualifiers']['lineage'],'unspecified');self.assertIsNone(a['qualifiers']['parent_person_id'])
 def test_cannot_invent_grandmother_parent(self):
  a=next(a for a in self.f['relations']if a['predicate']=='grandmother');a['qualifiers']['parent_person_id']='invented';self.assertFalse(reported_grandmother_valid(a,self.ps))
 def test_two_inverse_uncles(self):
  aa=[a for a in self.f['relations']if a['predicate']=='paternal_uncle'];self.assertEqual(len(aa),2)
  for a in aa:self.assertTrue(paternal_uncle_direction_valid(a,self.ps))
 def test_inverse_uncle_endpoints_cannot_swap(self):
  for a in[a for a in self.f['relations']if a['predicate']=='paternal_uncle']:
   a['subject_person_id'],a['object_person_id']=a['object_person_id'],a['subject_person_id'];self.assertFalse(paternal_uncle_direction_valid(a,self.ps))
 def test_nine_is_lifetime_age_without_birth(self):
  a=self.f['age'];self.assertTrue(direct_source_age_valid(a));self.assertIsNone(a['birth_year']);self.assertEqual(a['age_context'],{'kind':'during_life'});self.assertEqual(a['source_term'],'九嵗')
 def test_same_person_other_appointment_not_same_event(self):
  # A distinct holding of the same person and office has its own occurrence;
  # name/title equality cannot borrow this grant's beginning.
  self.title['id']='same-person-other-appointment';d=self.title['effective_period']['start']['normalized_date'];d['cross_chapter_event_binding']['record_id']=self.title['id'];self.title['attestations'][0]['start']-=1;self.title['attestations'][0]['end']-=1;self.assertFalse(self.valid(self.title,'start'))
 def test_repeated_same_office_grant_needs_another_decision(self):
  d=self.title['effective_period']['start']['normalized_date'];b=d['cross_chapter_event_binding'];p=self.ps[b['origin']['paragraph_id']][1];p['text']+='進拜司空';self.title['evidence'][0]['quote']=p['text'];self.assertFalse(self.valid(self.title,'start'))
 def test_death_negation_or_intention_rejected(self):
  for term in ['未病薨','欲病死','疑病死','病將死']:
   d=copy.deepcopy(self.death);ch=copy.deepcopy(self.ch);b=d['normalized_date']['cross_chapter_event_binding'];side=b['origin'];p=next(p for p in ch[side['chapter_id']]['paragraphs']if p['id']==side['paragraph_id']);a=side['event_anchor'];old=a['surface'];p['text']=p['text'][:a['start']]+term+p['text'][a['end']:];d['evidence'][0]['quote']=p['text'];d['source_term']=term;a.update(end=a['start']+len(term),surface=term);sa=side['subject_clause_anchor'];sa.update(end=a['end'],surface=p['text'][sa['start']:a['end']]);self.assertFalse(cross_chapter_annal_date_valid(d['normalized_date'],d,'life_event',ch),term)
 def test_year_interrupted_by_another_year(self):
  b=self.death['normalized_date']['cross_chapter_event_binding'];p=self.ps[b['annal']['paragraph_id']][1];at=b['annal']['year_anchor']['end'];p['text']=p['text'][:at]+'二年'+p['text'][at:]
  # Re-anchor all later fields, so the rejection tests an actual intervening year,
  # not stale offsets or mismatched quote text.
  for m in p['mentions']:
   if m['start']>=at:m['start']+=2;m['end']+=2
  for key in ['event_anchor','subject_clause_anchor','date_clause_anchor']:
   b['annal'][key]['start']+=2;b['annal'][key]['end']+=2
  self.death['normalized_date']['original_quote']=p['text'];self.death['normalized_date']['evidence'][0]['quote']=p['text'];self.death['source_date_parts']['evidence'][0]['quote']=p['text'];self.death['source_date_parts']['source_anchor']['start']+=2;self.death['source_date_parts']['source_anchor']['end']+=2
  self.assertFalse(self.valid())
 def test_month_cannot_be_borrowed_across_clause(self):
  b=self.death['normalized_date']['cross_chapter_event_binding']['annal'];p=self.ps[b['paragraph_id']][1];q=b['date_clause_anchor'];start=p['text'].index('正月');q.update(start=start,surface=p['text'][start:q['end']]);parts=self.death['source_date_parts'];parts.update(month=1,source_number='正',source_term='正月',source_anchor={'paragraph_id':p['id'],'start':start,'end':start+2,'surface':'正月'});self.assertFalse(self.valid());self.assertFalse(source_date_parts_valid(self.death,self.ch,source_age_number))
 def test_three_named_honorific_grants_without_death_year(self):
  self.assertEqual(len(self.f['honorifics']),3)
  for h in self.f['honorifics']:self.assertTrue(parent_honorific_grant_valid(h,self.ps));self.assertIsNone(h['posthumous_basis']['named_parent_honorific']['death_year']);self.assertIsNone(h['effective_period']['start']['date_expression'])
 def test_honorific_wrong_issuer_and_living_queen_refused(self):
  for h in self.f['honorifics']:
   h['posthumous_basis']['named_parent_honorific']['issuer_person_id']=h['person_id'];self.assertFalse(parent_honorific_grant_valid(h,self.ps));h['mode']='grant';self.assertFalse(parent_honorific_grant_valid(h,self.ps))
 def test_respect_mother_alone_does_not_prove_posthumous(self):
  for h in self.f['honorifics']:
   del h['posthumous_basis']['named_parent_honorific']['primary_context'];self.assertFalse(parent_honorific_grant_valid(h,self.ps))
 def test_posthumous_bridge_wrong_recipient(self):
  for h in self.f['honorifics']:
   h['posthumous_basis']['named_parent_honorific']['primary_context']['recipient_person_id']='other';self.assertFalse(parent_honorific_grant_valid(h,self.ps))
 def test_posthumous_bridge_wrong_sha(self):
  for h in self.f['honorifics']:
   h['posthumous_basis']['named_parent_honorific']['primary_context']['source']['raw_sha256']='0'*64;self.assertFalse(parent_honorific_grant_valid(h,self.ps))
 def test_posthumous_bridge_changed_death_or_after_grant(self):
  for h in self.f['honorifics']:
   aa=h['posthumous_basis']['named_parent_honorific']['primary_context']['anchors'];aa['death'],aa['grant']=aa['grant'],aa['death'];self.assertFalse(parent_honorific_grant_valid(h,self.ps))
 def test_posthumous_bridge_invented_grant_title(self):
  for h in self.f['honorifics']:
   h['posthumous_basis']['named_parent_honorific']['primary_context']['title']='別皇后';self.assertFalse(parent_honorific_grant_valid(h,self.ps))
if __name__=='__main__':unittest.main()
