import copy,json,unittest
from pathlib import Path
from scripts.table_evidence import load_tables
from scripts.title_chronology_cautions import chronology_caution_errors
ROOT=Path(__file__).resolve().parents[1]
class QuChengChronologyCaution(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tables=load_tables(ROOT);ch=json.loads((ROOT/'corpus/shiji/118.json').read_text());cls.chapters={ch['id']:ch};cls.paragraphs={p['id']:(ch['id'],p)for p in ch['paragraphs']};cls.decision=next(d for d in json.loads((ROOT/'corpus/shiji/118-identities.json').read_text())['decisions']if d['id']=='d-shiji118-qucheng-jie')
 def check(self,d):return chronology_caution_errors(d,self.tables,self.chapters,self.paragraphs)
 def test_received_conflict_is_preserved_without_filling_a_tenure(self):
  self.assertEqual(self.check(self.decision),[]);c=self.decision['chronology_caution'];self.assertTrue(c['no_tenure_interpolation']);self.assertIn('孝景三年',c['event_evidence']['quote']);self.assertIn('十八年，復免',c['table_accounts'][0]['quote']);self.assertIn('孝景中五年，矦捷復封',c['table_accounts'][0]['quote'])
 def test_wrong_event_person_cannot_borrow_the_warning(self):
  d=copy.deepcopy(self.decision);d['person_id']='synthetic-other';self.assertTrue(self.check(d))
 def test_event_quote_cannot_omit_or_rewrite_the_source_date(self):
  d=copy.deepcopy(self.decision);d['chronology_caution']['event_evidence']['quote']='曲城侯';self.assertTrue(self.check(d))
 def test_wrong_table_work_and_revision_are_rejected(self):
  for key,value in [('work_id','w-shiji'),('source_revision','different')]:
   d=copy.deepcopy(self.decision);d['chronology_caution']['table_accounts'][0][key]=value;self.assertTrue(self.check(d))
 def test_different_table_person_is_not_a_tenure_account(self):
  d=copy.deepcopy(self.decision);d['chronology_caution']['table_accounts'][0]['person_mention_id']='missing';self.assertTrue(self.check(d))
 def test_source_digits_cannot_be_silently_harmonized(self):
  d=copy.deepcopy(self.decision);d['chronology_caution']['table_accounts'][0]['event_terms']=['孝景三年，矦捷復封'];self.assertTrue(self.check(d))
 def test_duplicate_cells_cannot_count_as_two_accounts(self):
  d=copy.deepcopy(self.decision);a=d['chronology_caution']['table_accounts'][0];d['chronology_caution']['table_accounts']=[a,copy.deepcopy(a)];self.assertTrue(self.check(d))
 def test_unresolved_cannot_be_changed_to_resolved_or_interpolated(self):
  for changes in [{'status':'resolved'},{'no_tenure_interpolation':False},{'human_reviewed':True},{'identity_basis':'title_tenure_interpolation'}]:
   d=copy.deepcopy(self.decision);d['chronology_caution'].update(changes);self.assertTrue(self.check(d))
 def test_malformed_source_objects_are_rejected_without_executing_them(self):
  for changes in [{'event_evidence':None},{'table_accounts':[None,None]}]:
   d=copy.deepcopy(self.decision);d['chronology_caution'].update(changes);self.assertTrue(self.check(d))
 def test_display_quote_cannot_change_the_received_name(self):
  d=copy.deepcopy(self.decision);d['references'][0]['display_quote']='姓蟲名達';self.assertTrue(self.check(d))
 def test_display_quote_requires_the_declared_fixed_transcription_format(self):
  d=copy.deepcopy(self.decision);del d['references'][0]['quote_format'];self.assertTrue(self.check(d))
 def test_unrelated_decisions_remain_unchanged(self):self.assertEqual(self.check({'person_id':'synthetic-no-caution'}),[])
if __name__=='__main__':unittest.main()
