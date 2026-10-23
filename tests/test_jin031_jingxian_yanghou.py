import unittest,json,copy
from pathlib import Path
from scripts.fixed_witness_fact_slots import records,valid,errors,grammar
from scripts.age_context import age_context_valid
ROOT=Path(__file__).resolve().parents[1]
class JingxianFacts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/jinshu/031-jingxian-yanghou.json').read_bytes());cls.rows=records(cls.ch,ROOT);cls.by={v['fixed_source_fact_binding']['slot']:v for v in cls.rows}
 def reject(self,key,fn):
  v=copy.deepcopy(self.by[key]);fn(v);self.assertFalse(valid(v,self.ch,ROOT))
 def test_complete_source_and_all27_slots(self):
  self.assertEqual((len(self.ch['paragraphs']),sum(len(p['text'])for p in self.ch['paragraphs']),sum(len(p['mentions'])for p in self.ch['paragraphs'])),(2,132,18));self.assertEqual(len(self.rows),27)
  for v in self.rows:self.assertTrue(valid(v,self.ch,ROOT),v['id'])
 def test_abdication_relative_event_not_numeric_year(self):
  v=self.by['queen-dowager'];self.assertEqual(v['source_time_context']['event_kind'],'acceptance_of_abdication');self.assertIsNone(v['source_time_context']['numeric_year'])
  self.reject('queen-dowager',lambda x:x['source_time_context'].update(numeric_year=265))
 def test_mother_father_not_queens_father(self):
  a=self.by['mother-father'];self.assertEqual(a['subject_person_id'],self.by['mother-name']['person_id']);self.assertNotEqual(a['subject_person_id'],self.by['queen-name']['person_id'])
  def reverse(v):
   v['subject_person_id'],v['object_person_id']=v['object_person_id'],v['subject_person_id']
   for e in v['evidence']:e['subject_person_mention_id'],e['object_person_mention_id']=e['object_person_mention_id'],e['subject_person_mention_id']
  self.reject('mother-father',reverse)
 def test_two_spouses_not_same_woman(self):
  self.assertNotEqual(self.by['queen-spouse']['subject_person_id'],self.by['wu-spouse']['subject_person_id'])
  self.reject('wu-spouse',lambda v:v.update(subject_person_id=self.by['queen-spouse']['subject_person_id']))
 def test_mother_posthumous_title_not_queen(self):
  self.assertEqual(self.by['mother-county']['person_id'],self.by['mother-name']['person_id'])
  def shift(v):
   v['person_id']=self.by['queen-name']['person_id']
   for e in v['evidence']:e['person_mention_id']=self.by['queen-death']['evidence'][0]['person_mention_id']
   for a in v['attestations']:a['person_mention_id']=self.by['queen-death']['evidence'][0]['person_mention_id']
  self.reject('mother-county',shift)
 def test_mother_naming_does_not_borrow_queens_death(self):
  self.assertEqual(self.by['mother-postname']['naming_basis']['kind'],'explicit_posthumous_grant_then_naming');self.assertNotIn('death_term',self.by['mother-postname']['naming_basis'])
  self.reject('mother-postname',lambda v:v['naming_basis'].update(death_term='崩'))
 def test_273_and278_actor_scope(self):
  self.assertEqual(self.by['mother-county']['effective_period']['start']['normalized_date']['year'],273)
  self.assertEqual(self.by['queen-death']['normalized_date']['year'],278)
  self.assertNotIn('normalized_date',self.by['jinghuai-death'])
  self.reject('queen-death',lambda v:v['normalized_date'].update(year=273,era_year=273))
 def test_age_at_same_death_no_birth(self):
  age=self.by['queen-age'];death=self.by['queen-death'];self.assertTrue(age_context_valid(age,{death['id']:death}));self.assertIsNone(age['birth_year']);self.assertEqual(age['value'],65)
  self.reject('queen-age',lambda v:v.update(birth_year=214))
  self.reject('queen-age',lambda v:v['age_context'].update(life_event_id=self.by['jinghuai-death']['id']))
 def test_no_sons_does_not_become_no_children(self):
  v=self.by['queen-no-sons']['values'];self.assertEqual(v['sons_or_male_heirs_reported'],0);self.assertIsNone(v['all_children_count']);self.assertIsNone(v['daughters_count'])
  self.reject('queen-no-sons',lambda v:v['values'].update(all_children_count=0))
 def test_residence_and_burial_not_birth_or_modern(self):
  self.assertEqual(self.by['queen-residence']['relation'],'residence');self.assertEqual(self.by['queen-burial-place']['relation'],'burial_place')
  self.reject('queen-burial-place',lambda v:v.update(relation='birth_place'))
 def test_father_raw_ming_not_silently_normalized(self):self.reject('father-name',lambda v:v.update(ming='道'))
 def test_source_and_metadata_layers_rejected(self):
  for where in [('source',None),('paragraphs',0)]:
   c=copy.deepcopy(self.ch)
   if where[0]=='source':c['source']['annotator']='modern'
   else:c['paragraphs'][0]['text_layer']='modern_note'
   with self.assertRaises((AssertionError,KeyError,ValueError)):grammar(c,ROOT)
 def test_missing_and_duplicate_slot(self):
  rs=[v for v in self.rows if v['fixed_source_fact_binding']['slot']!='queen-age'];r=dict(chapter_id=self.ch['id'],records=rs)
  self.assertFalse(errors(ROOT,[self.ch,r]))
  for bad in [rs[:-1],rs+[rs[0]]]:self.assertTrue(errors(ROOT,[self.ch,dict(r,records=bad)]))
 def test_coherent_rekey_does_not_change_source(self):
  c=copy.deepcopy(self.ch)
  for p in c['paragraphs']:
   for m in p['mentions']:m['person_id']='synthetic_'+m['person_id']
  # Cross-witness maternal qualification now requires coherent IDs on both ends.
  with self.assertRaises(AssertionError):records(c,ROOT)
  from unittest.mock import patch
  other=json.loads((ROOT/'corpus/jinshu/034-yanghu.json').read_bytes())
  for p in other['paragraphs']:
   for m in p['mentions']:
    if m['kind']=='person':m['person_id']='synthetic_'+m['person_id']
  replacements={ROOT/'corpus/jinshu/031-jingxian-yanghou.json':json.dumps(c,ensure_ascii=False).encode(),ROOT/'corpus/jinshu/034-yanghu.json':json.dumps(other,ensure_ascii=False).encode()}
  original=Path.read_bytes
  def source_read(path):return replacements[path]if path in replacements else original(path)
  with patch.object(Path,'read_bytes',source_read):
   rows=records(c,ROOT)
   for v in rows:self.assertTrue(valid(v,c,ROOT))
 def test_previous_yangxiu36_preserved(self):
  c=json.loads((ROOT/'corpus/jinshu/093-yangxiu.json').read_bytes());rs=records(c,ROOT);self.assertEqual(len(rs),36)
  for v in rs:self.assertTrue(valid(v,c,ROOT))
if __name__=='__main__':unittest.main()
