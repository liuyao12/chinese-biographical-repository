# coding: utf-8
"""王氏年號初中末、原行內承接及原字報齡的受限回歸。

負例只deepcopy記憶體物件；不修改來源檔。
"""
from pathlib import Path
import json,copy,unittest
from scripts.validate_corpus import normalized_date_errors,source_age_number,direct_source_age_valid
from scripts.relative_regnal_year import relative_regnal_year_valid
from scripts.era_stage_dates import binding_valid
from scripts.subject_continuation import prior_subject_valid
from scripts.unassumed_appointments import unassumed_appointment_valid
ROOT=Path(__file__).resolve().parents[1]
sq=json.loads((ROOT/'corpus/nanqishu/033-wangsengqian.json').read_text())
ns=json.loads((ROOT/'corpus/nanshi/022-wangzhi.json').read_text())
h=json.loads((ROOT/'corpus/nanshi/022-wangzhi-titles.json').read_text())['holdings']
death=next(e for e in json.loads((ROOT/'corpus/nanshi/022-wangzhi-life-events.json').read_text())['events']if e['id']=='le-wang25-94')
ds=[x['effective_period']['start']['normalized_date']for x in h if x['id']in ['th-wang25-86','th-wang25-87','th-wang25-88','th-wang25-89']]+[death['normalized_date']]
proposals={p['id']:p for p in sq['annotation']['title_proposals']if p['id'].startswith('tp-wang26-')}
age=next(a for a in ns['annotation']['age_assertions']if a['id']=='age-wang26-96')
valid=lambda d,ch=ns:relative_regnal_year_valid(d,source_age_number,{ch['id']:ch})

class NewModelTests(unittest.TestCase):
 def test_actual_five_dates_and_no_initial_equals_first_year(self):
  self.assertEqual([d['year']for d in ds],[504,504,510,510,510])
  for d in ds:self.assertTrue(valid(d));self.assertEqual(normalized_date_errors(d,{ns['id']:ns}),[]);self.assertEqual(d['relative_year_reference']['era_expression'],'天監初');self.assertNotEqual(d['regnal_year_mapping']['source_number'],'元')
 def test_middle_and_last_stage_generalize_without_year_one(self):
  for suffix in ['中','末']:
   d=copy.deepcopy(ds[-1]);ch=copy.deepcopy(ns);p=ch['paragraphs'][0];p['text']=p['text'].replace('天監初','天監'+suffix)
   d['relative_year_reference']['era_expression']='天監'+suffix;d['narrative_era_scope']['era_anchor']['surface']='天監'+suffix
   d['narrative_era_scope']['full_paragraphs'][0]['quote']=p['text'];d['original_quote']=p['text'];d['evidence'][0]['quote']=p['text']
   self.assertTrue(valid(d,ch));self.assertEqual(d['year'],510)
 def test_stage_without_exact_scope_rejected(self):
  d=copy.deepcopy(ds[-1]);d.pop('narrative_era_scope');self.assertFalse(valid(d))
 def test_cannot_turn_initial_into_explicit_first_year(self):
  d=copy.deepcopy(ds[-1]);d['relative_year_reference']['era_expression']='天監元年';self.assertFalse(valid(d))
 def test_death_cannot_be_reburial_year_523(self):
  d=copy.deepcopy(ds[-1]);d['year']=d['era_year']=523;self.assertFalse(valid(d))
 def test_quote_scope_missing_or_extending_past_event_rejected(self):
  d=copy.deepcopy(ds[-1]);d['narrative_era_scope']['embedded_quotation_scopes']=[];d['narrative_era_scope']['quotation_introducers']=[];self.assertFalse(valid(d))
  d=copy.deepcopy(ds[-1]);q=d['narrative_era_scope']['embedded_quotation_scopes'][0];q['end']=ns['paragraphs'][0]['text'].index('普通四年');q['surface']=ns['paragraphs'][0]['text'][q['start']:q['end']];self.assertFalse(valid(d))
 def test_quotation_introducer_or_return_boundary_wrong_rejected(self):
  d=copy.deepcopy(ds[-1]);d['narrative_era_scope']['quotation_introducers'][0]['end']-=1;self.assertFalse(valid(d))
  d=copy.deepcopy(ds[-1]);q=d['narrative_era_scope']['embedded_quotation_scopes'][0];q['end']-=1;q['surface']=q['surface'][:-1];self.assertFalse(valid(d))
 def test_wrong_subject_even_when_near_or_after_event_rejected(self):
  d=copy.deepcopy(ds[-1]);d['narrative_era_scope']['event_binding']['subject_mention_id']=next(m['id']for m in ns['paragraphs'][0]['mentions']if m['surface']=='謝莊');self.assertFalse(valid(d))
  d=copy.deepcopy(ds[-1]);d['narrative_era_scope']['event_binding']['subject_mention_id']=next(m['id']for m in ns['paragraphs'][0]['mentions']if m['start']==414);self.assertFalse(valid(d))
 def test_switched_topic_cannot_hide_behind_unit_heading(self):
  d=copy.deepcopy(ds[-1]);ch=copy.deepcopy(ns);ch['paragraphs'][0]['mentions'].append(dict(id='test-only-foreign-topic',kind='person',person_id='test-only-foreign',start=392,end=394,surface=ch['paragraphs'][0]['text'][392:394]));self.assertFalse(valid(d,ch))
 def test_competing_era_detected_even_if_caller_omits_it(self):
  d=copy.deepcopy(ds[-1]);ch=copy.deepcopy(ns);p=ch['paragraphs'][0];p['text']=p['text'].replace('簡通賓客','普通四年');d['narrative_era_scope']['known_era_names']=['天監'];d['narrative_era_scope']['full_paragraphs'][0]['quote']=p['text'];d['original_quote']=p['text'];d['evidence'][0]['quote']=p['text'];self.assertFalse(valid(d,ch))
 def test_skipped_paragraph_wrong_revision_or_ruler_rejected(self):
  for field,value in [('paragraph_ids',[]),('source_commit','wrong'),('event_ruler_person_id','another-ruler')]:
   d=copy.deepcopy(ds[-1]);d['narrative_era_scope'][field]=value;self.assertFalse(valid(d))
 def test_record_binding_rejects_wrong_person_id_title_and_role(self):
  self.assertTrue(binding_valid(ds[-1],death,'life_event'));e=copy.deepcopy(death);e['person_id']='other';self.assertFalse(binding_valid(ds[-1],e,'life_event'));e=copy.deepcopy(death);e['id']='another';self.assertFalse(binding_valid(ds[-1],e,'life_event'))
  record=next(x for x in h if x['id']=='th-wang25-86');self.assertTrue(binding_valid(ds[0],record,'start'));record=copy.deepcopy(record);record['title']='另一職';self.assertFalse(binding_valid(ds[0],record,'start'));self.assertFalse(binding_valid(ds[0],record,'end'))
  later=next(x for x in h if x['id']=='th-wang25-88');borrowed=copy.deepcopy(ds[0]);borrowed['narrative_era_scope']['event_binding']['record_id']=later['id'];self.assertFalse(binding_valid(borrowed,later,'start'))
  wrong_anchor=copy.deepcopy(ds[2]);wrong_anchor['narrative_era_scope']['event_binding']['title_anchor']=copy.deepcopy(ds[0]['narrative_era_scope']['event_binding']['title_anchor']);self.assertFalse(binding_valid(wrong_anchor,later,'start'))
 def test_actual_shared_line_and_full_refusals(self):
  for p in proposals.values():self.assertTrue(unassumed_appointment_valid(p,sq))
 def test_same_rawline_without_fragment_proof_rejected(self):
  p=copy.deepcopy(proposals['tp-wang26-55']);p['evidence'][0]['context'].pop('source_continuity');self.assertFalse(unassumed_appointment_valid(p,sq))
 def test_same_line_overlapping_reversed_or_missing_char_rejected(self):
  for field,amount in [('source_start',-1),('source_start',1)]:
   ch=copy.deepcopy(sq);u=ch['source']['normalization']['selected_source_line_units'][8];u['source_fragments'][0][field]+=amount;self.assertFalse(unassumed_appointment_valid(proposals['tp-wang26-55'],ch))
  ch=copy.deepcopy(sq);ch['source']['normalization']['selected_source_line_units'][8]['body_start']-=1;self.assertFalse(unassumed_appointment_valid(proposals['tp-wang26-55'],ch))
 def test_shared_original_line_sha_or_text_tamper_rejected(self):
  ch=copy.deepcopy(sq);ch['source']['normalization']['selected_source_line_units'][8]['source_fragments'][0]['raw_line_sha256']='bad';self.assertFalse(unassumed_appointment_valid(proposals['tp-wang26-55'],ch))
  ch=copy.deepcopy(sq);ch['source']['normalization']['selected_source_line_units'][8]['source_fragments'][0]['selected_text']='偽';self.assertFalse(unassumed_appointment_valid(proposals['tp-wang26-55'],ch))
 def test_short_prefix_or_later_resumption_cannot_evade_wrong_subject(self):
  p=copy.deepcopy(proposals['tp-wang26-55']);a=p['evidence'][0]['context']['source_continuity']['target_prefix_anchor'];a['end']=1;a['surface']=a['surface'][:1];self.assertFalse(unassumed_appointment_valid(p,sq))
  p=copy.deepcopy(proposals['tp-wang26-55']);p['evidence'][0]['context']['source_continuity']['target_resumption_mention_id']=sq['paragraphs'][8]['mentions'][1]['id'];self.assertFalse(unassumed_appointment_valid(p,sq))
 def test_first_named_resumption_is_foreign_not_nearest_same_name(self):
  ch=copy.deepcopy(sq);ch['paragraphs'][8]['mentions'][0]['person_id']='foreign';self.assertFalse(unassumed_appointment_valid(proposals['tp-wang26-55'],ch))
 def test_full_refusal_requires_bound_named_speaker(self):
  p=copy.deepcopy(proposals['tp-wang26-64']);p.pop('refusal_subject_scope');self.assertFalse(unassumed_appointment_valid(p,sq))
  p=copy.deepcopy(proposals['tp-wang26-64']);p['refusal_subject_scope']['subject_mention_id']=next(m['id']for m in sq['paragraphs'][11]['mentions']if m['surface']=='儉');self.assertFalse(unassumed_appointment_valid(p,sq))
 def test_speech_overlap_and_wrong_resumption_rejected(self):
  p=copy.deepcopy(proposals['tp-wang26-64']);p['refusal_subject_scope']['speech_anchor']['end']+=1;self.assertFalse(unassumed_appointment_valid(p,sq))
  p=copy.deepcopy(proposals['tp-wang26-64']);p['refusal_subject_scope']['resumption_anchor']['surface']='固辭不拜';self.assertFalse(unassumed_appointment_valid(p,sq))
 def test_cannot_truncate_declined_into_bare_non_assumption(self):
  p=copy.deepcopy(proposals['tp-wang26-64']);p['non_assumption_kind']='did_not_take_up';a=p['non_assumption_anchor'];a['start']+=2;a['surface']='不拜';self.assertFalse(unassumed_appointment_valid(p,sq))
 def test_original_sui_age_exact_and_lifetime(self):
  self.assertEqual(age['source_term'],'九嵗');self.assertTrue(direct_source_age_valid(age));self.assertEqual(age['age_context'],{'kind':'during_life'});self.assertIsNone(age['birth_year'])
  for term in ['九歲','九歳','九嵗','年九']:
   a=copy.deepcopy(age);a['source_term']=term;self.assertTrue(direct_source_age_valid(a))
 def test_wrong_age_numeral_value_or_extra_char_not_accepted(self):
  for field,value in [('value',8),('value',True),('source_number','十'),('source_term','九嵗餘'),('source_term','九')]:
   a=copy.deepcopy(age);a[field]=value;self.assertFalse(direct_source_age_valid(a))

if __name__=='__main__':unittest.main()
