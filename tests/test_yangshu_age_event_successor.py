import unittest,copy
try:
 from tests.test_epitaph_named_lifecycle import fixture
except ImportError:
 from test_epitaph_named_lifecycle import fixture
from scripts.epitaph_named_lifecycle import valid
try:
 from tests.test_profile_person_events import ProfilePersonEvents
except ImportError:
 from test_profile_person_events import ProfilePersonEvents
class AgeDeathBinding(unittest.TestCase):
 def test_valid(self):valid(*fixture())
 def bad(self,mutate):
  c,r=fixture();mutate(c,r)
  with self.assertRaises((AssertionError,KeyError)):valid(c,r)
 def test_missing_context(self):self.bad(lambda c,r:c['annotation']['age_assertions'][0].pop('age_context'))
 def test_wrong_event(self):self.bad(lambda c,r:c['annotation']['age_assertions'][0]['age_context'].update(life_event_id='synthetic-burial'))
 def test_during_life(self):self.bad(lambda c,r:c['annotation']['age_assertions'][0].update(age_context=dict(kind='during_life')))
 def test_wrong_death_owner(self):self.bad(lambda c,r:r[2]['events'][0].update(person_id='other'))
 def test_burial_as_death(self):self.bad(lambda c,r:r[2]['events'][0].update(event_type='burial'))
 def test_wrong_evidence(self):self.bad(lambda c,r:c['annotation']['age_assertions'][0]['evidence'][0].update(quote='short'))
class EventOutput(ProfilePersonEvents):
 def test_foreign_only(self):self.assertNotIn('person_events',self.run_case([dict(id='foreign',person_id='beta',event_type='burial')]))
 def test_none(self):self.assertNotIn('person_events',self.run_case(None))
 def test_other_event_exact(self):
  e=dict(id='call',person_id='alpha',event_type='recruitment',status='offered',nested=dict(unknown=None))
  self.assertEqual(self.run_case([e])['person_events'],[e])
