"""Fixed source group: wrong dates/subjects cannot inherit the year."""
import json,copy,unittest
from pathlib import Path
from scripts.group_execution_year import valid
from scripts.validate_corpus import source_age_number
R=Path(__file__).resolve().parents[1]
class GroupExecutionYear(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  c=json.loads((R/'corpus/sanguozhi/009-caozhen.json').read_text());cls.chapters={c['id']:c};cls.events=[e for e in json.loads((R/'corpus/sanguozhi/009-caozhen-life-events.json').read_text())['events']if e.get('normalized_date',{}).get('event_evidence_binding',{}).get('kind')=='named_group_execution_after_biographical_year_chain']
 def check(self,e):return valid(e['normalized_date'],e,self.chapters,source_age_number)
 def test_ten_distinct_people(self):
  self.assertEqual(len(self.events),10);self.assertEqual(len({e['person_id']for e in self.events}),10);self.assertTrue(all(self.check(e)for e in self.events))
 def test_wrong_year(self):
  for y in [248,250]:
   e=copy.deepcopy(self.events[0]);e['normalized_date']['year']=y;self.assertFalse(self.check(e))
 def test_wrong_person(self):
  e=copy.deepcopy(self.events[0]);e['person_id']=self.events[1]['person_id'];self.assertFalse(self.check(e))
 def test_planned_march_or_any_month_cannot_be_execution_month(self):
  e=copy.deepcopy(self.events[0]);e['date_expression']='三月';self.assertFalse(self.check(e));e=copy.deepcopy(self.events[0]);e['normalized_date']['month']=3;self.assertFalse(self.check(e));e=copy.deepcopy(self.events[0]);e['source_date_parts']={'month':3};self.assertFalse(self.check(e))
 def test_skipping_notes_or_one_execution_member_rejected(self):
  for k in ['tail_paragraph_ids','tail_full_paragraphs','embedded_source_paragraph_ids','execution_member_mention_ids']:
   e=copy.deepcopy(self.events[0]);e['normalized_date']['event_evidence_binding'][k].pop();self.assertFalse(self.check(e))
