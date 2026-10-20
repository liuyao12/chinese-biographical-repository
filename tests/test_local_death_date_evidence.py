"""Actual fixed 王凌/司馬懿 year chains; self-contained, no private paths/network."""
import copy,json,unittest
from pathlib import Path
from scripts.local_death_date_evidence import local_death_date_evidence_valid
from scripts.validate_corpus import source_age_number,normalized_date_errors
class LocalDeathDateEvidence(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.fixture=json.loads((Path(__file__).parent/'fixtures/local_death_date_evidence.json').read_text());cls.ch=cls.fixture['chapter'];cls.chapters={cls.ch['id']:cls.ch};cls.events=[e for e in cls.fixture['event_set']['events']if'normalized_date'in e]
 def valid(self,e,chs=None):return local_death_date_evidence_valid(e['normalized_date'],e,chs or self.chapters,source_age_number)
 def local(self,e):
  e=copy.deepcopy(e);d=e['normalized_date'];b=d['event_evidence_binding'];p=next(p for p in self.ch['paragraphs']if p['id']==e['evidence'][0]['paragraph_id']);m=next(m for m in p['mentions']if m['id']==e['evidence'][0]['person_mention_id']);end=b['event_term_anchor']['end'];start=min(m['start'],b['event_term_anchor']['start']);q=p['text'][start:end];e['evidence'][0]['quote']=q;b['event_quote_anchor']={'paragraph_id':p['id'],'start':start,'end':end,'surface':q};return e
 def test_two_actual_persons251_original_scopes(self):
  self.assertEqual(2,len(self.events));self.assertNotEqual(self.events[0]['person_id'],self.events[1]['person_id'])
  for e in self.events:self.assertTrue(self.valid(e));self.assertEqual([],normalized_date_errors(e['normalized_date'],self.chapters));self.assertEqual(251,e['normalized_date']['year'])
 def test_actual_local_death_quotes_not_full_paragraphs(self):
  for base in self.events:
   e=self.local(base);self.assertTrue(self.valid(e));self.assertLess(len(e['evidence'][0]['quote']),len(e['normalized_date']['original_quote']));self.assertNotEqual(e['evidence'],e['normalized_date']['evidence']);self.assertNotIn(e['date_expression'],e['evidence'][0]['quote'])
 def test_old_relative_models_still_valid_without_binding(self):
  for e in self.events:
   d=copy.deepcopy(e['normalized_date']);del d['event_evidence_binding'];self.assertEqual([],normalized_date_errors(d,self.chapters))
 def test_jump_paragraph_rejected(self):
  e=copy.deepcopy(self.events[0]);e['normalized_date']['evidence'].pop(1);self.assertFalse(self.valid(e))
 def test_jump_matching_claimed_scope_also_rejected(self):
  e=copy.deepcopy(self.events[1]);d=e['normalized_date'];d['evidence'].pop(1);d['narrative_era_scope']['paragraph_ids'].pop(1);d['narrative_era_scope']['full_paragraphs'].pop(1);self.assertFalse(self.valid(e))
 def test_wrong_year_rejected(self):
  e=copy.deepcopy(self.events[0]);e['normalized_date']['year']=250;e['normalized_date']['era_year']=250;self.assertFalse(self.valid(e))
 def test_wrong_era_rejected(self):
  e=copy.deepcopy(self.events[0]);e['normalized_date']['regnal_year_mapping']['era_name']='正始';self.assertFalse(self.valid(e))
 def test_swapped_person_rejected(self):
  e=copy.deepcopy(self.events[0]);e['person_id']=self.events[1]['person_id'];self.assertFalse(self.valid(e))
 def test_wrong_event_rejected(self):
  e=copy.deepcopy(self.events[1]);e['id']='different-death';self.assertFalse(self.valid(e))
 def test_birth_instead_of_death_rejected(self):
  e=copy.deepcopy(self.events[0]);e['event_type']='birth';self.assertFalse(self.valid(e))
 def test_altered_full_chain_quote_rejected(self):
  e=copy.deepcopy(self.events[0]);e['normalized_date']['evidence'][1]['quote']+='改';self.assertFalse(self.valid(e))
 def test_local_event_quote_cannot_impersonate_full_date_paragraph(self):
  e=self.local(self.events[0]);e['normalized_date']['evidence'][-1]['quote']=e['evidence'][0]['quote'];self.assertFalse(self.valid(e))
 def test_wrong_fixed_revision_rejected(self):
  e=copy.deepcopy(self.events[0]);e['normalized_date']['event_evidence_binding']['source_fingerprint']['source_commit']='0'*40;self.assertFalse(self.valid(e))
 def test_changed_raw_witness_rejected(self):
  ch=copy.deepcopy(self.ch);ch['source']['raw_file_sha256']='0'*64;self.assertFalse(self.valid(self.events[0],{ch['id']:ch}))
 def test_event_literal_changed_rejected(self):
  e=self.local(self.events[0]);e['evidence'][0]['quote']+='改';self.assertFalse(self.valid(e))
 def test_same_source_but_other_event_term_rejected(self):
  e=copy.deepcopy(self.events[1]);e['source_term']='遂自殺';self.assertFalse(self.valid(e))
 def test_other_person_anchor_rejected(self):
  e=copy.deepcopy(self.events[1]);e['normalized_date']['event_evidence_binding']['event_person_mention_id']=self.events[0]['evidence'][0]['person_mention_id'];self.assertFalse(self.valid(e))
 def test_coordinated_person_swap_within_same_paragraph_rejected(self):
  e=copy.deepcopy(self.events[1]);d=e['normalized_date'];b=d['event_evidence_binding'];p=next(p for p in self.ch['paragraphs']if p['id']==e['evidence'][0]['paragraph_id']);m=next(m for m in p['mentions']if m.get('person_id')==self.events[0]['person_id']);e['person_id']=m['person_id'];b['person_id']=m['person_id'];e['evidence'][0]['person_mention_id']=m['id'];b['event_person_mention_id']=m['id'];d['evidence'][-1]['person_mention_id']=m['id'];z=b['event_term_anchor']['end'];b['death_subject_scope']['clause_anchor']={'paragraph_id':p['id'],'start':m['start'],'end':z,'surface':p['text'][m['start']:z]};self.assertFalse(self.valid(e))
 def test_event_date_anchor_outside_original_rejected(self):
  e=copy.deepcopy(self.events[0]);e['normalized_date']['event_evidence_binding']['event_date_expression_anchor']['start']=-1;self.assertFalse(self.valid(e))
 def test_not_arbitrary_date_evidence(self):
  e=copy.deepcopy(self.events[1]);e['normalized_date']['evidence'][0]['source_id']='other-version';self.assertFalse(self.valid(e))
 def test_unsupported_scope_does_not_silently_fallback(self):
  e=copy.deepcopy(self.events[0]);e['normalized_date']['narrative_era_scope']['kind']='anything';self.assertFalse(self.valid(e))
if __name__=='__main__':unittest.main()
