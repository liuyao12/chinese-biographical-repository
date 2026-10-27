import copy,json,unittest
from pathlib import Path
from scripts.wyd_song044_life import record,valid
ROOT=Path(__file__).resolve().parents[1]
class WydLifeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.record=json.loads((ROOT/'corpus/songshu/044-wyd1739-life-events.json').read_text())
  cls.chapter=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_text())
 def test_source_list_and_subjects(self):
  self.assertTrue(valid(self.record,ROOT));self.assertEqual(len(self.record['events']),12)
  roles=[a['id'].removeprefix('le-song044-wyd-')for a in self.record['events']]
  self.assertEqual(roles,['hui','xiedun','shiji','shiyou','kongyanxiu','zhouchao','feiyin','douyingqi','jiangqian','yanqiansi','xuan-brother','shangxuanshi'])
  ps={p['id']:p for p in self.chapter['paragraphs']}
  for a in self.record['events']:
   e,=a['evidence'];p=ps[e['paragraph_id']];m=next(m for m in p['mentions']if m['id']==e['person_mention_id'])
   self.assertEqual(m['person_id'],a['person_id']);self.assertIn(a['source_term'],p['text']);self.assertEqual(p['text'],e['quote'])
 def test_dengzhi_conflict_is_not_a_certain_death(self):
  p=next(p for p in self.chapter['paragraphs']if p['id'].endswith(':p016'))
  d=next(m for m in p['mentions']if m.get('source_role_key')=='dengzhi')
  self.assertIn('庾登之殿道鸞何承天並皆原免',p['text'])
  self.assertNotIn(d['person_id'],[a['person_id']for a in self.record['events']])
  wrong=copy.deepcopy(self.record);wrong['events'][0]['person_id']=d['person_id']
  self.assertFalse(valid(wrong,ROOT))
 def test_nearby_living_people_rejected(self):
  p=next(p for p in self.chapter['paragraphs']if p['id'].endswith(':p016'))
  for role in ['daoyanzhi','liucui','shenfuzhi','chengtian']:
   m=next(m for m in p['mentions']if m.get('source_role_key')==role)
   wrong=copy.deepcopy(self.record);wrong['events'][0]['person_id']=m['person_id'];wrong['events'][0]['evidence'][0]['person_mention_id']=m['id']
   self.assertFalse(valid(wrong,ROOT),role)
 def test_death_terms_do_not_invent_years_or_ages(self):
  for original in self.record['events']:
   self.assertFalse(original['human_reviewed'])
   if 'normalized_date'in original:
    self.assertEqual(original['date_expression'],'三年');self.assertEqual(original['normalized_date']['year'],426)
    self.assertFalse(any(k in original['normalized_date']for k in ['month','day','lunar_month','birth_year']))
   else:self.assertIsNone(original['date_expression'])
  for key,value in [('date_expression','元嘉三年'),('normalized_date',{'ce_year':426}),('human_reviewed',True),('source_term','卒')]:
   wrong=copy.deepcopy(self.record);wrong['events'][0][key]=value;self.assertFalse(valid(wrong,ROOT),key)
 def test_early_death_and_drowning_do_not_transfer_subjects(self):
  rows={e['id']:e for e in self.record['events']}
  self.assertEqual(rows['le-song044-wyd-xuan-brother']['source_term'],'蚤卒')
  self.assertEqual(rows['le-song044-wyd-shangxuanshi']['source_term'],'投水死')
  wrong=copy.deepcopy(self.record);wrong['events'][-1]['person_id']=wrong['events'][0]['person_id'];self.assertFalse(valid(wrong,ROOT))
 def test_numeric_year_has_complete_same_campaign_context(self):
  from scripts.wyd_song044_life import date_valid
  from scripts.validate_corpus import normalized_date_errors
  dated=[a for a in self.record['events']if 'normalized_date'in a];self.assertEqual(len(dated),10)
  a=dated[0];d=a['normalized_date'];self.assertEqual(d['year'],424+3-1)
  chain=d['event_evidence_binding'];self.assertEqual(chain['era_anchor']['surface'],'元嘉二年');self.assertEqual(chain['year_anchor']['surface'],'三年正月')
  self.assertEqual(len(chain['full_narrative']),14)
  self.assertTrue(date_valid(d,a,{self.chapter['id']:self.chapter},ROOT))
  self.assertEqual(normalized_date_errors(d,{self.chapter['id']:self.chapter},ROOT,a,'life_event'),[])
 def test_year_month_and_campaign_chain_mutations_rejected(self):
  from scripts.wyd_song044_life import date_valid
  for mutation in ['year','month','chain','person','era']:
   a=copy.deepcopy(self.record['events'][0]);d=a['normalized_date']
   if mutation=='year':d['year']=427;d['era_year']=427
   elif mutation=='month':d['month']=1
   elif mutation=='chain':d['event_evidence_binding']['full_narrative'].pop(4)
   elif mutation=='person':a['person_id']=self.record['events'][1]['person_id']
   else:d['regnal_year_mapping']['era_name']='永初'
   self.assertFalse(date_valid(d,a,{self.chapter['id']:self.chapter},ROOT),mutation)
 def test_missing_events_and_malformed_input_rejected(self):
  for x in [None,[],{},dict(self.record,events=self.record['events'][:-1])]:self.assertFalse(valid(x,ROOT))
if __name__=='__main__':unittest.main()
