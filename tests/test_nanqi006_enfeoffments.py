"""Six royal grants: exact source roles, local day + grouped month/year, no ordinal."""
import copy,json,unittest,ast,subprocess,sys
from pathlib import Path
from unittest.mock import patch
from scripts.nanqi006_royal_enfeoffments import valid,normalized_valid,CID,BASE,expected
from scripts.received_career_roles import holding_valid
from scripts.validate_corpus import normalized_date_errors
ROOT=Path(__file__).resolve().parents[1]
class SixPrinceGrants(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ch=json.loads((ROOT/'corpus/nanqishu/006-jianwu1-nov.json').read_bytes());cls.rows=json.loads((ROOT/'corpus/nanqishu/006-jianwu1-nov-titles.json').read_bytes())['holdings']
 def good(self,h):return valid(h,self.ch,ROOT)
 def test_all_six_real_dispatchers(self):
  self.assertEqual(6,len(self.rows));self.assertEqual(6,len({h['person_id']for h in self.rows}))
  for h in self.rows:
   self.assertTrue(holding_valid(h,self.ch,ROOT));d=h['effective_period']['start']['normalized_date'];self.assertTrue(normalized_valid(d,h,'start',{CID:self.ch},ROOT));self.assertEqual([],normalized_date_errors(d,{CID:self.ch},ROOT,h,'start'))
 def test_ends_unknown_and_no_ordinal(self):
  for h in self.rows:
   self.assertEqual({'status':'unknown','date_expression':None,'evidence':[]},h['effective_period']['end']);self.assertFalse(h['source_career_role']['absolute_birth_order_inferred']);self.assertNotIn('birth_order',h)
 def test_date_parts_and_editorial_join(self):
  for h in self.rows:
   d=h['effective_period']['start']['normalized_date'];p=d['source_date_parts'];self.assertEqual((494,'year','庚辰'),(d['year'],d['precision'],d['source_expression']));self.assertEqual((11,None,None,'庚辰'),(p['month'],p['day'],p['leap_month'],p['sexagenary_day']));self.assertEqual('建武元年十一月庚辰',p['composed_display']);self.assertIn('not_continuous_literal_quote',p['composition_status']);self.assertNotIn(p['composed_display'],d['original_quote'])
 def test_wrong_person_or_rank(self):
  for key,value in [('person_id',self.rows[1]['person_id']),('title',self.rows[1]['title']),('kind','office'),('mode','attestation')]:
   h=copy.deepcopy(self.rows[0]);h[key]=value;self.assertFalse(holding_valid(h,self.ch,ROOT))
 def test_wrong_source_role_and_shift(self):
  for key,value in [('recipient_mention_id',self.rows[1]['attestations'][0]['person_mention_id']),('group_id','other'),('absolute_birth_order_inferred',True)]:
   h=copy.deepcopy(self.rows[0]);h['source_career_role'][key]=value;self.assertFalse(self.good(h))
  h=copy.deepcopy(self.rows[0]);h['attestations'][0]['start']+=1;h['source_career_role']['title_anchor']['start']+=1;self.assertFalse(self.good(h))
 def test_wrong_year_and_wrong_era(self):
  for key,value in [('year',495),('source_expression','建武元年'),('precision','month')]:
   h=copy.deepcopy(self.rows[0]);h['effective_period']['start']['normalized_date'][key]=value;self.assertFalse(self.good(h));self.assertTrue(normalized_date_errors(h['effective_period']['start']['normalized_date'],{CID:self.ch},ROOT,h,'start'))
  h=copy.deepcopy(self.rows[0]);h['effective_period']['start']['normalized_date']['regnal_year_mapping']['start_ce_year']=317;self.assertFalse(self.good(h))
 def test_missing_month_wrong_day_cross_month(self):
  for key,value in [('month',None),('month',12),('sexagenary_day','庚子'),('day',1),('leap_month',False)]:
   h=copy.deepcopy(self.rows[0]);h['effective_period']['start']['normalized_date']['source_date_parts'][key]=value;self.assertFalse(self.good(h))
  h=copy.deepcopy(self.rows[0]);h['effective_period']['start']['normalized_date']['source_date_parts'].pop('month');self.assertFalse(self.good(h))
 def test_no_borrowed_whole_year_or_end(self):
  h=copy.deepcopy(self.rows[0]);h['evidence'][0]['quote']='建武元年';self.assertFalse(self.good(h))
  h=copy.deepcopy(self.rows[0]);h['effective_period']['end']={'status':'source_event','event_type':'explicit_end','date_expression':'永明七年','evidence':h['evidence']};self.assertFalse(self.good(h))
 def test_raw_year_and_calendar_pins(self):
  original=Path.read_bytes
  for name in ['year-context.json','calendar-row.json']:
   target=ROOT/BASE/name;v=json.loads(target.read_bytes())
   if name=='year-context.json':v['year_anchor']['raw_start']+=1
   else:v['columns']['dynasty']='晉';v['columns']['first_year']='317'
   raw=json.dumps(v,ensure_ascii=False).encode()
   with patch.object(Path,'read_bytes',lambda p:raw if p==target else original(p)):self.assertFalse(self.good(self.rows[0]))
 def test_boolean_or_float_not_integer(self):
  for value in (True,1.0):
   h=copy.deepcopy(self.rows[0]);h['effective_period']['start']['normalized_date']['regnal_year_mapping']['regnal_year']=value;self.assertFalse(self.good(h))
 def test_malformed_fail_closed(self):
  for obj in (None,[],1,'grant',{}):
   self.assertFalse(valid(obj,self.ch,ROOT));self.assertFalse(normalized_valid(obj,None,'start',{},ROOT));self.assertFalse(holding_valid(obj,self.ch,ROOT))
  for ch in (None,[],{},'chapter'):self.assertFalse(valid(self.rows[0],ch,ROOT))
 def test_direct_import(self):
  code="import sys,json;from pathlib import Path;r=Path(sys.argv[1]);sys.path.insert(0,str(r/'scripts'));from nanqi006_royal_enfeoffments import valid;c=json.loads((r/'corpus/nanqishu/006-jianwu1-nov.json').read_bytes());hs=json.loads((r/'corpus/nanqishu/006-jianwu1-nov-titles.json').read_bytes())['holdings'];assert all(valid(h,c,r)for h in hs)"
  r=subprocess.run([sys.executable,'-c',code,str(ROOT)],capture_output=True,text=True);self.assertEqual(0,r.returncode,r.stderr)
if __name__=='__main__':unittest.main()
