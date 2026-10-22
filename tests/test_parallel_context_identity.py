# coding: utf-8
from pathlib import Path
import copy,json,unittest
ROOT=Path(__file__).resolve().parents[1]
from scripts.parallel_context_identity import valid,affirmative,received_anchor
class ParallelContextIdentity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  J=lambda p:json.loads(p.read_text());cls.people={p['id']:p for p in J(ROOT/'registry/persons.json')['persons']};cls.c=J(ROOT/'corpus/jinshu/043-wangyan.json');cls.w=J(ROOT/'corpus/jinshu/059.json');cls.ch={cls.c['id']:cls.c,cls.w['id']:cls.w};cls.d=next(d for d in J(ROOT/'corpus/jinshu/043-wangyan-identities.json')['decisions']if d['id']=='d-jin043-qiwang-jiong-parallel')
 def test_fixed_full_primary_positive(self):self.assertTrue(valid(self.d,self.ch,self.people,ROOT))
 def test_two_candidates_cannot_swap_selected_person(self):
  d=copy.deepcopy(self.d);d['person_id']=d['parallel_context_reading']['countercandidate_person_id'];self.assertFalse(valid(d,self.ch,self.people,ROOT))
 def test_both_complete_units_required(self):
  d=copy.deepcopy(self.d);d['parallel_context_reading']['parallel_reference']['units'].pop();self.assertFalse(valid(d,self.ch,self.people,ROOT))
 def test_reference_fragment_does_not_replace_complete_unit(self):
  d=copy.deepcopy(self.d);d['parallel_context_reading']['parallel_reference']['units'][0]['start']+=1;self.assertFalse(valid(d,self.ch,self.people,ROOT))
 def test_local_quote_cannot_omit_original_conflict(self):
  d=copy.deepcopy(self.d);d['parallel_context_reading']['local_quote']='有匡復之功';self.assertFalse(valid(d,self.ch,self.people,ROOT))
 def test_same_event_anchor_cannot_be_removed(self):
  d=copy.deepcopy(self.d);d['parallel_context_reading']['parallel_reference']['anchors'].pop('bowing_event');self.assertFalse(valid(d,self.ch,self.people,ROOT))
 def test_anomaly_is_not_registered_alias(self):
  people=copy.deepcopy(self.people);r=self.d['parallel_context_reading'];people[self.d['person_id']]['aliases'].append(dict(surface=r['received_surface'],mention_ids=[r['person_mention_id']]));self.assertFalse(valid(self.d,self.ch,people,ROOT))
 def test_negative_cues_do_not_qualify_as_affirmative(self):
  for text in ['未有興復之功','不拜伏','非匡復之功','無匡復之功']:self.assertFalse(affirmative(text))
 def test_raw_reference_co_shift_rejected(self):
  d=copy.deepcopy(self.d)
  for u in d['parallel_context_reading']['parallel_reference']['units']:u['start']+=1;u['end']+=1
  self.assertFalse(valid(d,self.ch,self.people,ROOT))
 def test_selected_original_text_unchanged(self):
  p=next(p for p in self.c['paragraphs']if p['id'].endswith('p006'));self.assertIn('時齊王乂有匡復之功',p['text']);self.assertNotIn('時齊王冏有',p['text']);self.assertNotIn('reported_variants',self.c['annotation'])

 def test_raw_editorial_note_cannot_supply_primary_anchor(self):
  text='正文<ref>注家文字</ref>正文';self.assertFalse(received_anchor(text,7,9));self.assertTrue(received_anchor(text,0,2))
