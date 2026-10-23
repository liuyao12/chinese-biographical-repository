# coding: utf-8
import unittest,json,copy,tempfile,hashlib
from pathlib import Path
from scripts import fixed_kanripo_accession_dates as f
from scripts.fixed_kanripo_fact_slots import records
R=Path(__file__).resolve().parents[1]
class XinpiAccessionDates(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((R/'corpus/sanguozhi/025-xinpi.json').read_text());cls.hs=json.loads((R/'corpus/sanguozhi/025-xinpi-titles.json').read_text())['holdings'];cls.h={v['fixed_source_fact_binding']['slot']:v for v in cls.hs};cls.chs={cls.c['id']:cls.c}
 def norm(self,h):return h['effective_period']['start']['normalized_date']
 def test_three_exact_years_and_preserved_source_expressions(self):
  for key,year,expr in [('holding_004',220,'文帝踐阼'),('holding_005',220,'文帝踐阼'),('holding_010',226,'明帝即位')]:
   h=self.h[key];d=self.norm(h);self.assertEqual(d['year'],year);self.assertEqual(d['precision'],'year');self.assertEqual(h['effective_period']['start']['date_expression'],expr);self.assertEqual(d['source_expression'],expr);self.assertTrue(f.normalized_valid(d,h,'start',self.chs,R))
 def test_mingdi_accession_not_taihe_first_year(self):
  h=copy.deepcopy(self.h['holding_010']);d=self.norm(h);d['year']=d['era_year']=227;d['regnal_year_mapping'].update(era_name='太和',source_era_name='太和',source_number='元',regnal_year=1,start_ce_year=227,end_ce_year=233);self.assertFalse(f.normalized_valid(d,h,'start',self.chs,R));self.assertFalse(f.bound_valid(d,h,self.c,R))
 def test_wrong_office_same_person_consistent_date_transplant(self):
  h=copy.deepcopy(self.h['holding_003']);d=copy.deepcopy(self.norm(self.h['holding_004']));h['effective_period']['start']['normalized_date']=d;d['source_accession_year_binding']['holding_id']=h['id'];self.assertFalse(f.normalized_valid(d,h,'start',self.chs,R));self.assertFalse(f.bound_valid(d,h,self.c,R))
 def test_wrong_recipient_consistent_transplant(self):
  h=copy.deepcopy(self.h['holding_004']);d=self.norm(h);m=next(m for m in self.c['paragraphs'][2]['mentions']if m['surface']=='文帝');old=h['person_id'];mid=h['evidence'][0]['person_mention_id']
  def change(x):
   if isinstance(x,dict):return{k:change(v)for k,v in x.items()}
   if isinstance(x,list):return[change(v)for v in x]
   return m['person_id']if x==old else m['id']if x==mid else x
  h=change(h);self.assertFalse(f.normalized_valid(self.norm(h),h,'start',self.chs,R))
 def test_proof_or_ruler_swapping_rejected(self):
  h=copy.deepcopy(self.h['holding_004']);h['effective_period']['start']['normalized_date']=copy.deepcopy(self.norm(self.h['holding_010']));self.assertFalse(f.bound_valid(self.norm(h),h,self.c,R));self.assertFalse(f.normalized_valid(self.norm(h),h,'start',self.chs,R))
 def test_numeric_date_fields_reject_bool_and_float(self):
  for field,value in [('era_year',220.0),('year',True),('regnal_year',True)]:
   h=copy.deepcopy(self.h['holding_004']);d=self.norm(h)
   if field=='regnal_year':d['regnal_year_mapping'][field]=value
   else:d[field]=value
   self.assertFalse(f.bound_valid(d,h,self.c,R));self.assertFalse(f.normalized_valid(d,h,'start',self.chs,R))
 def test_no_month_day_first_service_birth_or_office_end(self):
  for key in ('holding_004','holding_005','holding_010'):
   h=self.h[key];d=self.norm(h);self.assertEqual(h['effective_period']['end'],dict(status='unknown',date_expression=None,evidence=[]));self.assertFalse(any(k in d for k in ('month','day','lunar_month','lunar_day','birth_year')));self.assertFalse(f.normalized_valid(d,h,'end',self.chs,R))
 def test_primary_fixed_hash_and_full_read_boundaries(self):
  data=f.proofs(R);self.assertEqual(set(data),{'imperial_accession','successor_accession'})
  for ref in data.values():self.assertEqual(hashlib.sha256((R/ref['path']).read_bytes()).hexdigest(),ref['sha256'])
  r=json.loads((R/'source-evidence/sgz025-xinpi-accession-dates/reading-review.json').read_text());units={u['id']:u for u in r['complete_read_units']};self.assertEqual(units['wendi-complete-abdication-event']['last_line'],370);u=units['mingdi-accession-to-next-year-boundary'];raw=(R/u['raw_path']).read_text();self.assertEqual(raw[u['start']:u['end']],u['text']);self.assertIn('七年夏五月帝病篤',u['text']);self.assertIn('太和元年春正月',u['text'])
 def test_changed_metadata_cannot_rehash_itself(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);p=root/f.PROOF_PATH;p.parent.mkdir(parents=True);d=json.loads((R/f.PROOF_PATH).read_text());d['proofs']['successor_accession']['mapping']['first']=221;p.write_text(json.dumps(d))
   with self.assertRaises(AssertionError):f.proofs(root)
 def test_raw_co_shift_or_symlink_rejected(self):
  h=self.h['holding_010'];d=self.norm(h);ref=f.proofs(R)['successor_accession']
  for symlink in (False,True):
   with tempfile.TemporaryDirectory()as t:
    root=Path(t);p=root/f.PROOF_PATH;p.parent.mkdir(parents=True);p.write_bytes((R/f.PROOF_PATH).read_bytes());p=root/ref['path'];p.parent.mkdir(parents=True,exist_ok=True)
    if symlink:p.symlink_to(R/ref['path'])
    else:p.write_bytes(b' '+(R/ref['path']).read_bytes())
    self.assertFalse(f.bound_valid(d,h,self.c,root))
 def test_three_dates_do_not_erase_correct_sister_direction(self):
  aa=json.loads((R/'corpus/sanguozhi/025-xinpi-assertions.json').read_text())['assertions'];a=next(a for a in aa if a['id']=='a-sgz025-xinpi-kin_004');p=self.c['paragraphs'][7];female=next(m for m in p['mentions']if m['start']==p['text'].index('毗女憲英')+2);self.assertEqual(a['subject_person_id'],female['person_id']);self.assertEqual(a['qualifiers']['relative_age'],'older')
if __name__=='__main__':unittest.main()
