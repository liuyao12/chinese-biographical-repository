"""Synthetic records test one death with independent source evidence."""
import copy,unittest
from scripts.age_context import age_context_valid
class DeathAgeMultipleSourcesTests(unittest.TestCase):
 def setUp(self):
  self.a={'source_id':'synthetic-body','chapter_id':'synthetic-chapter','paragraph_id':'synthetic-body-p','quote':'某年五十而終'}
  self.b={'source_id':'synthetic-note','chapter_id':'synthetic-chapter','paragraph_id':'synthetic-note-p','quote':'及卒學士惜之'}
  self.age={'person_id':'synthetic-person','age_context':{'kind':'at_death','life_event_id':'synthetic-death'},'evidence':[self.a]}
  self.event={'event_type':'death','status':'source_attested','person_id':'synthetic-person','evidence':[self.a,self.b]}
 def valid(self):return age_context_valid(self.age,{'synthetic-death':self.event})
 def test_one_death_two_witnesses_one_age_quote(self):self.assertTrue(self.valid())
 def test_equal_scopes_still_supported(self):self.event['evidence']=[self.a];self.assertTrue(self.valid())
 def test_other_person_rejected(self):self.event['person_id']='synthetic-other';self.assertFalse(self.valid())
 def test_other_event_rejected(self):self.age['age_context']['life_event_id']='synthetic-other-death';self.assertFalse(self.valid())
 def test_outside_age_evidence_rejected(self):self.age['evidence'].append(dict(self.a,paragraph_id='synthetic-other-p'));self.assertFalse(self.valid())
 def test_changed_age_quote_rejected(self):self.age['evidence']=[dict(self.a,quote='某年六十而終')];self.assertFalse(self.valid())
 def test_empty_age_evidence_rejected(self):self.age['evidence']=[];self.assertFalse(self.valid())
 def test_no_death_evidence_rejected(self):self.event['evidence']=[];self.assertFalse(self.valid())
 def test_missing_age_scope_rejected(self):self.a['source_id']=None;self.assertFalse(self.valid())
 def test_unattested_death_rejected(self):self.event['status']='synthetic_unattested';self.assertFalse(self.valid())
 def test_birth_event_rejected(self):self.event['event_type']='birth';self.assertFalse(self.valid())
