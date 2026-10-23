# coding:utf-8
import unittest,json,copy,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts import fixed_witness_fact_slots as f
from scripts.fixed_witness_parallel_dates import normalized_valid
class DuYuLifePlaceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.c=json.loads((ROOT/'corpus/jinshu/034-duyu.json').read_text());cls.r=f.records(cls.c,ROOT);cls.new=[x for x in cls.r if x['fixed_source_fact_binding']['slot'].startswith('life_')];cls.by={x['fixed_source_fact_binding']['slot']:x for x in cls.new};cls.death=cls.by['life_duyu-death']
 def test_exact_ten_new_and_seven_kin_retained(self):
  self.assertEqual(len(self.new),10);self.assertEqual(len([x for x in self.r if x.get('predicate')]),7);self.assertTrue(all(f.valid(x,self.c,ROOT)for x in self.r))
 def test_death_284_year_chinese_civil_and_leap_original(self):
  d=self.death['normalized_date'];self.assertEqual((d['year'],d['calendar'],d['precision']),(284,'chinese_civil','year'));self.assertIn('閏月',d['references'][1]['quote']);self.assertTrue(normalized_valid(d,self.death,'life_event',{self.c['id']:self.c},ROOT))
 def test_bad_285_or_wrong_calendar_rejected(self):
  for field,value in [('year',285),('era_year',285),('calendar','gregorian')]:
   r=copy.deepcopy(self.death);r['normalized_date'][field]=value;self.assertFalse(normalized_valid(r['normalized_date'],r,'life_event',{self.c['id']:self.c},ROOT))
 def test_consistent_wrong_person_rejected(self):
  other=self.by['life_duxi-death'];r=copy.deepcopy(self.death);r['person_id']=other['person_id'];r['evidence']=copy.deepcopy(other['evidence']);r['normalized_date']['evidence']=copy.deepcopy(other['evidence']);self.assertFalse(f.valid(r,self.c,ROOT));self.assertFalse(normalized_valid(r['normalized_date'],r,'life_event',{self.c['id']:self.c},ROOT))
 def test_wrong_chapter_and_event_role_rejected(self):
  r=copy.deepcopy(self.death);r['evidence'][0]['chapter_id']='c-jinshu-034-yanghu';r['normalized_date']['evidence']=copy.deepcopy(r['evidence']);self.assertFalse(f.valid(r,self.c,ROOT));self.assertFalse(normalized_valid(self.death['normalized_date'],self.death,'title_holding',{self.c['id']:self.c},ROOT))
 def test_unyearned_deaths_remain_unyearned(self):
  for key in ('shu','yanghu','duxi','guo'):self.assertNotIn('normalized_date',self.by['life_'+key+'-death'])
 def test_age_numeric_not_birth(self):
  for who,n in [('duyu',63),('duxi',48)]:
   r=self.by['life_'+who+'-age'];self.assertEqual(r['value'],n);self.assertIsNone(r['birth_year']);self.assertEqual(r['age_context']['kind'],'at_death')
 def test_planned_grave_not_actual_address_or_other_tomb(self):
  r=self.by['life_duyu-burial-plan'];self.assertEqual(r['kind'],'intended_burial_place');self.assertFalse(r['values']['actual_burial_attested']);self.assertEqual(r['values']['place_source_name'],'洛陽城東首陽之南');self.assertNotIn('邢山',r['values']['place_source_name']);self.assertEqual(self.by['life_duyu-death-place']['place']['source_name'],'鄧縣')
 def test_guo_no_sex_or_family_inference(self):
  r=self.by['life_guo-death'];self.assertEqual(r['source_term'],'因郭氏喪亡');self.assertNotIn('gender',r);self.assertFalse(any(x.get('predicate')in('mother','spouse')and r['person_id']in(x.get('subject_person_id'),x.get('object_person_id'))for x in self.r))
 def test_real_cli_wrong_year_rejected_without_source_writes(self):
  code="""import runpy,json
from pathlib import Path
from unittest.mock import patch
p=Path('corpus/jinshu/034-duyu-life-events.json').resolve();d=json.loads(p.read_text());r=next(x for x in d['events']if 'normalized_date'in x);r['normalized_date']['year']=285;r['normalized_date']['era_year']=285;old=Path.read_text
def read(q,*a,**kw):return json.dumps(d,ensure_ascii=False)if q.resolve()==p else old(q,*a,**kw)
with patch.object(Path,'read_text',read):runpy.run_path('scripts/validate_corpus.py',run_name='__main__')
"""
  r=subprocess.run([sys.executable,'-c',code],cwd=ROOT,capture_output=True,text=True);self.assertEqual(r.returncode,1,r.stdout+r.stderr);self.assertNotIn('Traceback',r.stdout+r.stderr)
