import copy,json,unittest
from pathlib import Path
from scripts.validate_corpus import source_age_number,normalized_date_errors
from scripts.local_death_date_evidence import local_death_date_evidence_valid
class Wang251Dates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.f=json.loads((Path(__file__).parent/'fixtures/wang251_dates46.json').read_text());cls.ch=cls.f['chapter'];cls.chs={cls.ch['id']:cls.ch}
 def test_same_two_events_with_year251_and_full_chain(self):
  self.assertEqual(2,len(self.f['operations']))
  for op in self.f['operations']:
   a,b=op['after'],op['before'];self.assertEqual(a['id'],b['id']);self.assertEqual(a['person_id'],b['person_id']);self.assertEqual(a['source_term'],b['source_term']);self.assertEqual(251,a['normalized_date']['year']);self.assertTrue(local_death_date_evidence_valid(a['normalized_date'],a,self.chs,source_age_number));self.assertEqual([],normalized_date_errors(a['normalized_date'],self.chs));self.assertTrue(a['interpretation_note'].startswith(b['interpretation_note']));self.assertLess(len(a['evidence'][0]['quote']),len(b['evidence'][0]['quote']))
 def test_month_is_explicit_chinese_month_not_modelled_as_numeric_yet(self):
  e=self.f['operations'][1]['after'];self.assertEqual('其年八月',e['date_expression']);self.assertEqual('year',e['normalized_date']['precision']);self.assertNotIn('month',e['normalized_date']);p=next(p for p in self.ch['paragraphs']if p['id']==e['evidence'][0]['paragraph_id']);self.assertEqual('八月',p['text'][442:444])
 def test_wrong_person_rejected(self):
  e=copy.deepcopy(self.f['operations'][0]['after']);e['person_id']=self.f['operations'][1]['after']['person_id'];self.assertFalse(local_death_date_evidence_valid(e['normalized_date'],e,self.chs,source_age_number))
 def test_same_id_required(self):
  e=copy.deepcopy(self.f['operations'][1]['after']);e['id']='new-duplicate-death';self.assertFalse(local_death_date_evidence_valid(e['normalized_date'],e,self.chs,source_age_number))
 def test_wrong_local_quote_rejected(self):
  e=copy.deepcopy(self.f['operations'][0]['after']);e['evidence'][0]['quote']+='改';self.assertFalse(local_death_date_evidence_valid(e['normalized_date'],e,self.chs,source_age_number))
 def test_chain_jump_rejected(self):
  e=copy.deepcopy(self.f['operations'][0]['after']);e['normalized_date']['evidence'].pop(1);self.assertFalse(local_death_date_evidence_valid(e['normalized_date'],e,self.chs,source_age_number))
if __name__=='__main__':unittest.main()
