# coding: utf-8
import unittest,copy,json
from pathlib import Path
from scripts.local_death_date_evidence import local_death_date_evidence_valid
from scripts.validate_corpus import source_age_number,normalized_date_errors
# Self-contained received witness fixture; synthetic mutations below are semantic
# counterexamples, never new historical source claims.
F=json.loads((Path(__file__).parent/'fixtures/song047_named_execution_death.json').read_bytes())
class NamedExecutionDeath(unittest.TestCase):
 def pair(self):return copy.deepcopy(F['event']),copy.deepcopy(F['chapter'])
 def valid(self,e,c):return local_death_date_evidence_valid(e['normalized_date'],e,{c['id']:c},source_age_number)
 def insert(self,e,c,at,value):
  p=c['paragraphs'][6];d=e['normalized_date'];b=d['event_evidence_binding'];p['text']=p['text'][:at]+value+p['text'][at:];size=len(value)
  for m in p['mentions']:
   if m['start']>=at:m['start']+=size;m['end']+=size
   elif m['end']>at:m['end']+=size
  anchors=[b['event_quote_anchor'],b['event_term_anchor'],b['event_date_expression_anchor'],b['death_subject_scope']['clause_anchor'],e['source_anchor'],d['narrative_era_scope']['event_date_anchor']]
  for a in anchors:
   if a['start']>=at:a['start']+=size;a['end']+=size
   elif a['end']>at:a['end']+=size
   a['surface']=p['text'][a['start']:a['end']]
  d['original_quote']=p['text']
  for evidence in d['evidence']:
   if evidence['paragraph_id']==p['id']:evidence['quote']=p['text']
  for q in d['narrative_era_scope']['full_paragraphs']:
   if q['paragraph_id']==p['id']:q['quote']=p['text']
  a=b['event_quote_anchor'];e['evidence'][0]['quote']=p['text'][a['start']:a['end']]
 def test_actual_442_local_victim_and_full_context(self):
  e,c=self.pair();self.assertTrue(self.valid(e,c));self.assertEqual([],normalized_date_errors(e['normalized_date'],{c['id']:c}));self.assertEqual(442,e['normalized_date']['year']);self.assertEqual('斬𢎞祖',e['source_term']);self.assertEqual(1,len(e['evidence']));self.assertNotIn('元嘉十三年',e['evidence'][0]['quote']);self.assertEqual(2,len(e['normalized_date']['evidence']))
 def test_same_narrow_grammar_accepts_xiao_verb(self):
  e,c=self.pair();p=c['paragraphs'][6];d=e['normalized_date'];b=d['event_evidence_binding'];at=b['event_term_anchor']['start'];p['text']=p['text'][:at]+'梟'+p['text'][at+1:]
  for a in [b['event_quote_anchor'],b['event_term_anchor'],b['death_subject_scope']['clause_anchor'],e['source_anchor']]:a['surface']=p['text'][a['start']:a['end']]
  e['source_term']=b['event_term_anchor']['surface'];b['source_term']=e['source_term'];e['evidence'][0]['quote']=b['event_quote_anchor']['surface'];d['original_quote']=p['text'];d['evidence'][-1]['quote']=p['text'];d['narrative_era_scope']['full_paragraphs'][-1]['quote']=p['text'];self.assertTrue(self.valid(e,c))
 def test_contradictory_chapter_primary_revision_rejected(self):
  e,c=self.pair();c['source']['source_commit']='0'*40;self.assertFalse(self.valid(e,c))
 def test_generic_event_id_not_record_allowlist(self):
  e,c=self.pair();e['id']='le-other-qualified-execution';e['normalized_date']['event_evidence_binding']['life_event_id']=e['id'];self.assertTrue(self.valid(e,c))
 def test_correct_fallback_preserves_primary_absence(self):
  e,c=self.pair();self.assertNotIn('source_commit',c['paragraphs'][5]['source_position']);self.assertTrue(self.valid(e,c))
 def test_contradictory_primary_not_hidden_by_correct_fallback(self):
  for key,value in [('source_commit','0'*40),('revision_id','0'*40),('source_commit',None)]:
   e,c=self.pair();c['paragraphs'][5]['source_position'][key]=value;e['normalized_date']['narrative_era_scope']['full_paragraphs'][0]['source_position']=copy.deepcopy(c['paragraphs'][5]['source_position']);self.assertFalse(self.valid(e,c),(key,value))
 def test_correct_explicit_primary_supported(self):
  e,c=self.pair()
  for p in c['paragraphs'][5:7]:p['source_position']['revision_id']=c['source']['revision_id']
  for q,p in zip(e['normalized_date']['narrative_era_scope']['full_paragraphs'],c['paragraphs'][5:7]):q['source_position']=copy.deepcopy(p['source_position'])
  self.assertTrue(self.valid(e,c))
 def test_changed_raw_hash_rejected(self):
  e,c=self.pair();c['source']['raw_file_sha256']='0'*64;self.assertFalse(self.valid(e,c))
 def test_changed_fixed_revision_rejected(self):
  e,c=self.pair();e['normalized_date']['event_evidence_binding']['source_fingerprint']['source_revision']='0'*40;self.assertFalse(self.valid(e,c))
 def test_no_remote_blob_or_empty_fingerprint_substitute(self):
  e,c=self.pair();b=e['normalized_date']['event_evidence_binding'];b['source_fingerprint']['source_blob_sha']='locally-computed';self.assertFalse(self.valid(e,c))
 def test_wrong_person_even_coordinated_binding_rejected(self):
  e,c=self.pair();e['person_id']='l26_15v_yeo';e['normalized_date']['event_evidence_binding']['person_id']=e['person_id'];self.assertFalse(self.valid(e,c))
 def test_actor_cannot_be_victim_anchor(self):
  e,c=self.pair();b=e['normalized_date']['event_evidence_binding'];b['event_person_mention_id']=b['death_subject_scope']['actor_person_mention_id'];e['evidence'][0]['person_mention_id']=b['event_person_mention_id'];e['normalized_date']['evidence'][-1]['person_mention_id']=b['event_person_mention_id'];self.assertFalse(self.valid(e,c))
 def test_actor_anchor_outside_clause_rejected(self):
  e,c=self.pair();e['normalized_date']['event_evidence_binding']['death_subject_scope']['actor_person_mention_id']='c-songshu-047-liuhuaisu:p007:m0160';self.assertFalse(self.valid(e,c))
 def test_only_execution_verb_and_exact_named_victim(self):
  e,c=self.pair();e['source_term']='敗𢎞祖';e['normalized_date']['event_evidence_binding']['source_term']=e['source_term'];self.assertFalse(self.valid(e,c))
 def test_negation_future_command_and_transfer_reanchored(self):
  for token in ['未','不','非','欲','將','當','令','命','曰','云','詔','「']:
   e,c=self.pair();self.insert(e,c,e['normalized_date']['event_evidence_binding']['event_term_anchor']['start'],token);self.assertFalse(self.valid(e,c),token)
 def test_hypothetical_before_actor_reanchored(self):
  e,c=self.pair();self.insert(e,c,e['normalized_date']['event_evidence_binding']['death_subject_scope']['clause_anchor']['start'],'欲使');self.assertFalse(self.valid(e,c))
 def test_pronoun_between_verb_and_victim_rejected(self):
  e,c=self.pair();self.insert(e,c,e['normalized_date']['event_evidence_binding']['event_term_anchor']['start']+1,'其');a=e['normalized_date']['event_evidence_binding']['event_term_anchor'];e['source_term']=a['surface'];e['normalized_date']['event_evidence_binding']['source_term']=a['surface'];self.assertFalse(self.valid(e,c))
 def test_new_year_between_date_and_victim_reanchored(self):
  for token in ['二十年','明年','翌年','其年','泰始元年']:
   e,c=self.pair();self.insert(e,c,e['normalized_date']['event_evidence_binding']['death_subject_scope']['clause_anchor']['start'],token);self.assertFalse(self.valid(e,c),token)
 def test_named_speech_between_year_and_local_clause_rejected(self):
  e,c=self.pair();self.insert(e,c,e['normalized_date']['event_evidence_binding']['death_subject_scope']['clause_anchor']['start'],'難當曰');self.assertFalse(self.valid(e,c))
 def test_clause_cannot_expand_to_next_person(self):
  e,c=self.pair();b=e['normalized_date']['event_evidence_binding'];p=c['paragraphs'][6];a=b['death_subject_scope']['clause_anchor'];a['end']=195;a['surface']=p['text'][a['start']:a['end']];b['event_quote_anchor']=copy.deepcopy(a);e['evidence'][0]['quote']=a['surface'];self.assertFalse(self.valid(e,c))
 def test_range_cannot_start_at_other_named_subject(self):
  e,c=self.pair();b=e['normalized_date']['event_evidence_binding'];a=b['death_subject_scope']['clause_anchor'];a['start']=168;a['surface']=c['paragraphs'][6]['text'][168:a['end']];b['event_quote_anchor']=copy.deepcopy(a);e['evidence'][0]['quote']=a['surface'];self.assertFalse(self.valid(e,c))
 def test_full_date_quote_must_remain_full_paragraph(self):
  e,c=self.pair();e['normalized_date']['evidence'][-1]['quote']=e['evidence'][0]['quote'];self.assertFalse(self.valid(e,c))
 def test_time_context_not_local_death_evidence(self):
  e,c=self.pair();e['evidence']=copy.deepcopy(e['normalized_date']['evidence']);self.assertFalse(self.valid(e,c))
 def test_missing_contiguous_context_rejected(self):
  e,c=self.pair();e['normalized_date']['evidence'].pop(0);self.assertFalse(self.valid(e,c))
 def test_unrelated_era_or_year_rejected(self):
  for key,value in [('year',443),('era_year',443)]:
   e,c=self.pair();e['normalized_date'][key]=value;self.assertFalse(self.valid(e,c),(key,value))
  e,c=self.pair();e['normalized_date']['regnal_year_mapping']['era_name']='太元';self.assertFalse(self.valid(e,c))
 def test_mismatched_monarch_scope_rejected(self):
  e,c=self.pair();e['normalized_date']['narrative_era_scope']['event_ruler_person_id']='3qs_nqa_ioa_AAA';self.assertFalse(self.valid(e,c))
 def test_unsupported_scope_cannot_fall_back(self):
  e,c=self.pair();e['normalized_date']['event_evidence_binding']['death_subject_scope']['kind']='anything';self.assertFalse(self.valid(e,c))
 def test_non_death_rejected(self):
  e,c=self.pair();e['event_type']='birth';self.assertFalse(self.valid(e,c))
if __name__=='__main__':unittest.main(verbosity=2)
