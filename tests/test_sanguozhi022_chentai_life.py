import copy,json,unittest
from pathlib import Path
from scripts.validate_corpus import normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class ChentaiLife(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.chapter=json.loads((ROOT/'corpus/sanguozhi/022-chenqun-chentai.json').read_text());cls.ps={p['id'].split(':')[-1]:p for p in cls.chapter['paragraphs']}
  cls.events={x['id']:x for x in json.loads((ROOT/'corpus/sanguozhi/022-chenqun-chentai-life-events.json').read_text())['events']}
  cls.body=cls.events['le-sgz022-chentai-jingyuan1-death'];cls.note=cls.events['le-sgz022-chentai-weishichunqiu-death-report']
 def test_received_death_subject_and_successor_boundary(self):
  p=self.ps['p010'];e=self.body['evidence'][0];m=next(m for m in p['mentions']if m['id']==e['person_mention_id']);i=m['start'];q=e['quote']
  self.assertEqual(p['text'][i:i+len(q)],q);self.assertEqual(q,'泰前後以功增邑二千六百尸賜子弟一人亭侯二人關内侯景元元年薨追贈司空諡曰穆侯子恂嗣');self.assertEqual(m['person_id'],self.body['person_id'])
  self.assertNotIn('恂薨',q);self.assertEqual(p['text'][i+len(q):i+len(q)+2],'恂薨')
 def test_note_death_is_speaker_not_ruler_or_victim_of_proposal(self):
  p=self.ps['p013'];e=self.note['evidence'][0];m=next(m for m in p['mentions']if m['id']==e['person_mention_id'])
  self.assertEqual(p['text'][m['start']:],e['quote']);self.assertEqual(e['quote'],'泰曰豈可使泰復發後言遂歐血薨');self.assertEqual(m['person_id'],self.note['person_id']);self.assertTrue(p['text'].startswith('魏氏春秋曰帝之崩也'))
  work=next(m for m in p['mentions']if m['kind']=='work');self.assertEqual(work['work_id'],'w-weishichunqiu-sgz022-reference');self.assertEqual(p['source_position']['source_layer'],'pei_annotation')
 def test_date_uses_independent_era_row_and_exact_original(self):
  d=self.body['normalized_date'];self.assertEqual(d['evidence'],self.body['evidence']);self.assertEqual(d['original_quote'],self.body['evidence'][0]['quote']);self.assertEqual(d['source_expression'],self.body['date_expression']);self.assertEqual(d['year'],260)
  self.assertEqual(normalized_date_errors(d,{self.chapter['id']:self.chapter},root=ROOT),[])
  ref=json.loads((ROOT/'source-evidence/sanguozhi022-chentai-life/era-reference-reading.json').read_text());self.assertEqual(ref['columns'],d['references'][0]['columns']);self.assertIsNone(ref['raw_revision']);self.assertIn('260 264',ref['row_quote'])
 def test_wrong_numeric_year_rejected_by_existing_validator(self):
  d=copy.deepcopy(self.body['normalized_date']);d['year']=d['era_year']=261
  self.assertTrue(normalized_date_errors(d,{self.chapter['id']:self.chapter},root=ROOT))
 def test_wrong_era_number_rejected_by_existing_validator(self):
  d=copy.deepcopy(self.body['normalized_date']);d['regnal_year_mapping']['source_number']='二';d['regnal_year_mapping']['regnal_year']=2
  self.assertTrue(normalized_date_errors(d,{self.chapter['id']:self.chapter},root=ROOT))
 def test_wrong_reference_columns_rejected_by_existing_validator(self):
  d=copy.deepcopy(self.body['normalized_date']);d['references'][0]['columns']['first_year']='261'
  self.assertTrue(normalized_date_errors(d,{self.chapter['id']:self.chapter},root=ROOT))
 def test_note_and_existing_jin039_not_backfilled(self):
  self.assertIsNone(self.note['date_expression']);self.assertNotIn('normalized_date',self.note)
  prior=next(x for x in json.loads((ROOT/'corpus/jinshu/039-life-events.json').read_text())['events']if x['id']=='le-jin039-yi28-chentai')
  self.assertIsNone(prior['date_expression']);self.assertNotIn('normalized_date',prior);self.assertEqual(prior['source_term'],'陳泰卒');self.assertEqual(prior['person_id'],self.body['person_id'])
 def test_no_biographical_inferences_or_medical_diagnosis(self):
  for e in (self.body,self.note):
   for k in ('birth_year','age','age_at_death','death_place','cause_of_death','birth_place','burial_place'):self.assertNotIn(k,e)
  p=self.ps['p014'];self.assertIn('本傳泰不為太常未詳干寶所由知之',p['text']);self.assertIn('孫盛改易泰言',p['text'])
 def test_no_inherited_address_or_new_office_from_batch(self):
  review=json.loads((ROOT/'source-evidence/sanguozhi022-chentai-life/review.json').read_text());self.assertIn('native_place',review['absent_fields']);self.assertEqual(review['names']['new_aliases'],[])
  for e in (self.body,self.note):self.assertNotIn('title',e);self.assertEqual(e['event_type'],'death')
if __name__=='__main__':unittest.main()
