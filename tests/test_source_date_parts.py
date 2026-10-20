"""Actual month八月 plus explicitly synthetic leap-month lexical regressions."""
import copy,json,unittest
from pathlib import Path
from scripts.validate_corpus import source_age_number
from scripts.source_date_parts import source_date_parts_valid,explicit_month_parts_valid
class SourceMonth(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  f=json.loads((Path(__file__).parent/'fixtures/source_month47.json').read_text());cls.e=f['event'];cls.c=f['chapter'];cls.chs={cls.c['id']:cls.c};d=cls.e['normalized_date'];b=d['event_evidence_binding'];a=b['event_date_expression_anchor'];start=a['start']+a['surface'].index('八月');cls.p={'kind':'explicit_chinese_calendar_month','calendar':'chinese_civil','precision':'month','life_event_id':cls.e['id'],'person_id':cls.e['person_id'],'month':8,'source_number':'八','source_term':'八月','leap_month':None,'day':None,'source_anchor':{'paragraph_id':a['paragraph_id'],'start':start,'end':start+2,'surface':'八月'},'evidence':[copy.deepcopy(d['evidence'][b['date_evidence_index']])],'status':'source_attested','reviewer':'Codex（AI代理）','human_reviewed':False}
 def event(self):
  e=copy.deepcopy(self.e);e['source_date_parts']=copy.deepcopy(self.p);return e
 def valid(self,e):return source_date_parts_valid(e,self.chs,source_age_number)
 def test_actual_chinese_month8_and_independent_year_precision(self):
  e=self.event();self.assertTrue(self.valid(e));self.assertEqual(251,e['normalized_date']['year']);self.assertEqual('year',e['normalized_date']['precision']);self.assertEqual(8,e['source_date_parts']['month']);self.assertEqual('chinese_civil',e['source_date_parts']['calendar']);self.assertIsNone(e['source_date_parts']['day']);self.assertIsNone(e['source_date_parts']['leap_month'])
 def test_unknown_day_may_be_omitted(self):
  e=self.event();del e['source_date_parts']['day'];self.assertTrue(self.valid(e))
 def test_unknown_day_must_not_be_invented(self):
  e=self.event();e['source_date_parts']['day']=1;self.assertFalse(self.valid(e))
 def test_western_month_calendar_rejected(self):
  e=self.event();e['source_date_parts']['calendar']='gregorian';self.assertFalse(self.valid(e))
 def test_wrong_numeric_month_rejected(self):
  for n in[7,9,13,True]:
   e=self.event();e['source_date_parts']['month']=n;self.assertFalse(self.valid(e))
 def test_wrong_event_rejected(self):
  e=self.event();e['source_date_parts']['life_event_id']='other-death';self.assertFalse(self.valid(e))
 def test_wrong_person_rejected(self):
  e=self.event();e['source_date_parts']['person_id']='other-person';self.assertFalse(self.valid(e))
 def test_changed_month_source_term_rejected(self):
  e=self.event();e['source_date_parts']['source_term']='九月';self.assertFalse(self.valid(e))
 def test_month_anchor_may_not_borrow_another_date(self):
  e=self.event();e['source_date_parts']['source_anchor']['start']-=1;self.assertFalse(self.valid(e))
 def test_local_death_quote_cannot_replace_complete_month_evidence(self):
  e=self.event();e['source_date_parts']['evidence']=copy.deepcopy(e['evidence']);self.assertFalse(self.valid(e))
 def test_wrong_fixed_revision_rejected(self):
  e=self.event();e['normalized_date']['event_evidence_binding']['source_fingerprint']['source_commit']='0'*40;self.assertFalse(self.valid(e))
 def test_leap_marker_cannot_be_inferred(self):
  e=self.event();e['source_date_parts']['leap_month']=True;self.assertFalse(self.valid(e))
 def test_synthetic_explicit_leap_month(self):
  text='其年閏八月某有疾遂薨';a={'paragraph_id':'synthetic','start':0,'end':5,'surface':'其年閏八月'};p={'month':8,'source_number':'八','source_term':'閏八月','leap_month':True,'day':None,'source_anchor':{'paragraph_id':'synthetic','start':2,'end':5,'surface':'閏八月'}};self.assertTrue(explicit_month_parts_valid(p,text,a,source_age_number));p['leap_month']=None;self.assertFalse(explicit_month_parts_valid(p,text,a,source_age_number))
 def test_synthetic_out_of_range_month(self):
  text='其年十三月';a={'paragraph_id':'synthetic','start':0,'end':5,'surface':text};p={'month':13,'source_number':'十三','source_term':'十三月','leap_month':None,'source_anchor':{'paragraph_id':'synthetic','start':2,'end':5,'surface':'十三月'}};self.assertFalse(explicit_month_parts_valid(p,text,a,source_age_number))
 def test_synthetic_season_is_not_month(self):
  p={'month':1,'source_number':'春','source_term':'春','leap_month':None,'source_anchor':{'paragraph_id':'synthetic','start':0,'end':1,'surface':'春'}};self.assertFalse(explicit_month_parts_valid(p,'春',{'paragraph_id':'synthetic','start':0,'end':1,'surface':'春'},source_age_number))
 def test_arbitrary_extra_field_rejected(self):
  e=self.event();e['source_date_parts']['gregorian_day']='251-08-01';self.assertFalse(self.valid(e))
if __name__=='__main__':unittest.main()
