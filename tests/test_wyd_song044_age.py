import copy,json,unittest
from pathlib import Path
from scripts.wyd_song044_age import records,answer_valid
from scripts.wyd_song044_formal_roles import source_errors
from scripts.age_context import age_context_valid
ROOT=Path(__file__).resolve().parents[1]
class WydAgeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_text())
  cls.ages=cls.ch['annotation']['age_assertions']
  cls.events=json.loads((ROOT/'corpus/songshu/044-wyd1739-life-events.json').read_text())['events']
 def test_three_speakers_and_occasions(self):
  self.assertEqual(self.ages,records(self.ch));self.assertEqual([x['value']for x in self.ages],[33,27,37])
  self.assertEqual(self.ages[0]['person_id'],self.ages[2]['person_id']);self.assertNotEqual(self.ages[0]['person_id'],self.ages[1]['person_id'])
  self.assertEqual([x['age_context']['kind']for x in self.ages],['during_life','during_life','at_death'])
  self.assertTrue(all(age_context_valid(x,{e['id']:e for e in self.events})for x in self.ages))
 def test_question_and_answer_preserve_original_words(self):
  a=self.ages[0];self.assertEqual(a['source_term'],'晦答曰三十三');self.assertNotIn('年三十三',a['evidence'][0]['quote'])
  self.assertTrue(answer_valid(a,self.ch,ROOT))
  b=a['source_age_answer_binding'];self.assertEqual(b['clause']['surface'],'澹問晦年晦答曰三十三')
  for key,value in [('value',27),('source_term','年三十三'),('person_id',self.ages[1]['person_id'])]:
   bad=copy.deepcopy(a);bad[key]=value;self.assertFalse(answer_valid(bad,self.ch,ROOT),key)
 def test_asker_and_reported_xun_are_not_the_answerer(self):
  for key in ['question_person_mention_id','answer_person_mention_id','asker_person_mention_id']:
   bad=copy.deepcopy(self.ages[0]);bad['source_age_answer_binding'][key]=self.ages[1]['evidence'][0]['person_mention_id'];self.assertFalse(answer_valid(bad,self.ch,ROOT),key)
 def test_source_guard_rejects_changed_age_or_borrowed_anchor(self):
  self.assertEqual(source_errors(self.ch,ROOT),[])
  for key,value in [('value',27),('person_id',self.ages[1]['person_id']),('birth_year',390),('human_reviewed',True)]:
   bad=copy.deepcopy(self.ch);bad['annotation']['age_assertions'][0][key]=value;self.assertTrue(source_errors(bad,ROOT),key)
  bad=copy.deepcopy(self.ch);bad['annotation']['age_assertions'][2]['evidence'][0]['person_mention_id']=self.ages[1]['evidence'][0]['person_mention_id'];self.assertTrue(source_errors(bad,ROOT))
 def test_no_birth_year_or_counting_method_inferred(self):
  for a in self.ages:
   self.assertIsNone(a['birth_year']);self.assertIsNone(a['date_expression']);self.assertEqual(a['counting'],'unspecified_source_age');self.assertFalse(a['human_reviewed'])
 def test_death_age_needs_same_person_same_death_source(self):
  a=self.ages[-1];ev={e['id']:e for e in self.events};self.assertTrue(age_context_valid(a,ev))
  ev=copy.deepcopy(ev);ev['le-song044-wyd-hui']['person_id']=self.ages[1]['person_id'];self.assertFalse(age_context_valid(a,ev))
  a=copy.deepcopy(a);a['age_context']['life_event_id']='le-song044-wyd-shiji';self.assertFalse(age_context_valid(a,{e['id']:e for e in self.events}))
 def test_unknown_annotation_still_rejected(self):
  bad=copy.deepcopy(self.ch);bad['annotation']['other_editor_note']='新增未核';self.assertTrue(source_errors(bad,ROOT))
if __name__=='__main__':unittest.main()
