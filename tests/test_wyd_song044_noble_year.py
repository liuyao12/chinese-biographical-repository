import copy,json,unittest,tempfile,shutil
from pathlib import Path
from scripts.wyd_song044_nobles import records,holding_valid
from scripts.wyd_song044_noble_year import date_record,valid,PATH,PINS
from scripts.validate_corpus import normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class NobleYearTests(unittest.TestCase):
 def setUp(self):
  self.ch=json.loads((ROOT/'corpus/songshu/044-wyd1739.json').read_text());self.h,self.q=records(self.ch,ROOT);self.d=self.h['effective_period']['start']['normalized_date'];self.chs={self.ch['id']:self.ch}
 def test_qualified_420_not_a_native_043_or_day(self):
  self.assertTrue(valid(self.d,self.h,'start',self.chs,ROOT));self.assertEqual(normalized_date_errors(self.d,self.chs,ROOT,self.h,'start'),[])
  self.assertEqual(self.d['year'],420);self.assertEqual(self.d['source_expression'],'永初元年');self.assertEqual(self.d['status'],'editorial_provisional');self.assertFalse(self.d['human_reviewed'])
  self.assertNotIn('永初元年',self.ch['paragraphs'][1]['text']);self.assertEqual(self.d['expression_scope'],'external_rendered_peer_biography_not_literal_in_wyd044')
  self.assertTrue(all(r['raw_obtained']is False and r['image_verified']is False and r['text_base_edition']is None for r in self.d['references'][:2]))
  self.assertEqual(self.h['effective_period']['end'],{'status':'unknown','date_expression':None,'evidence':[]});self.assertIsNone(self.q['date_expression']);self.assertEqual(self.q['outcome'],'not_reported')
 def test_numeric_era_qualification_and_borrowed_day_rejected(self):
  for key,value in [('year',421),('era_year',421),('source_expression','元嘉元年'),('original_quote','庚午'),('status','source_attested'),('human_reviewed',True),('month',6),('day_ganzhi','庚午')]:
   d=copy.deepcopy(self.d);d[key]=value;self.assertFalse(valid(d,self.h,'start',self.chs,ROOT),key);self.assertTrue(normalized_date_errors(d,self.chs,ROOT,self.h,'start'))
 def test_two_people_titles_and_event_not_interchangeable(self):
  for key,value in [('person_id','wrong'),('peer_person_id','wrong'),('title','建平郡公'),('peer_title','武昌縣公'),('households',4000),('peer_households',4000)]:
   d=copy.deepcopy(self.d);d['rendered_collective_award_year_binding'][key]=value;self.assertFalse(valid(d,self.h,'start',self.chs,ROOT),key)
  h=copy.deepcopy(self.h);h['person_id']='wrong';self.assertFalse(valid(self.d,h,'start',self.chs,ROOT));self.assertFalse(valid(self.d,self.h,'end',self.chs,ROOT))
  h=copy.deepcopy(self.h);h['effective_period']['end']['date_expression']='426';self.assertFalse(valid(self.d,h,'start',self.chs,ROOT))
 def test_year_and_award_roles_cannot_co_shift(self):
  d=copy.deepcopy(self.d);b=d['rendered_collective_award_year_binding'];b['peer_explicit_year']['start']+=1;b['peer_explicit_year']['end']+=1;self.assertFalse(valid(d,self.h,'start',self.chs,ROOT))
  d=copy.deepcopy(self.d);d['references'][1]['quote']=d['references'][1]['quote'].replace('永初元年','元嘉元年');self.assertFalse(valid(d,self.h,'start',self.chs,ROOT))
  d=copy.deepcopy(self.d);d['references'][0]['quote']=d['references'][0]['quote'].replace('武昌縣公','建平郡公');self.assertFalse(valid(d,self.h,'start',self.chs,ROOT))
 def test_external_payload_drift_uses_supplied_root(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);p=root/PATH;p.mkdir(parents=True)
   for n in PINS:shutil.copyfile(ROOT/PATH/n,p/n)
   self.assertTrue(valid(self.d,self.h,'start',self.chs,root))
   for n in PINS:
    raw=(p/n).read_bytes();(p/n).write_bytes(raw+b' ');self.assertFalse(valid(self.d,self.h,'start',self.chs,root),n);(p/n).write_bytes(raw)
   (p/'primary-units.json').unlink();self.assertFalse(valid(self.d,self.h,'start',self.chs,root))
 def test_regnal_table_not_other_era_or_year(self):
  for key,value in [('first_year','421'),('dynasty','齊'),('era_name','元嘉')]:
   d=copy.deepcopy(self.d);d['references'][2]['columns'][key]=value;self.assertFalse(valid(d,self.h,'start',self.chs,ROOT))
 def test_legal_same_identity_rekey_both_ends(self):
  c=copy.deepcopy(self.ch);b=self.d['rendered_collective_award_year_binding'];mp={b['person_id']:'abc_def_123',b['peer_person_id']:'xyz_456_789'}
  for p in c['paragraphs']:
   for m in p['mentions']:
    if m.get('person_id')in mp:m['person_id']=mp[m['person_id']]
  h,q=records(c,ROOT);d=h['effective_period']['start']['normalized_date'];self.assertEqual(d['rendered_collective_award_year_binding']['peer_person_id'],'xyz_456_789');self.assertTrue(valid(d,h,'start',{c['id']:c},ROOT));self.assertTrue(holding_valid(h,c,ROOT))
 def test_malformed_date_record_and_source_reject_without_throw(self):
  for bad in [None,[],{},'bad']:
   self.assertFalse(valid(bad,self.h,'start',self.chs,ROOT));self.assertFalse(valid(self.d,bad,'start',self.chs,ROOT));self.assertFalse(valid(self.d,self.h,'start',bad,ROOT))
  c=copy.deepcopy(self.ch);c['source']=None;self.assertFalse(valid(self.d,self.h,'start',{c['id']:c},ROOT))
if __name__=='__main__':unittest.main()
