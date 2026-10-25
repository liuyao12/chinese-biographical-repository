"""Full raw sibling-boundary and role-bound finite facts; no mutable corpus tests."""
import copy,json,unittest
from pathlib import Path
from scripts.fixed_biography_subsections import project
from scripts.fixed_wikisource_units import source_errors
from scripts.fixed_witness_fact_slots import records,valid
R=Path(__file__).resolve().parents[1]
class WangyanFiniteTests(unittest.TestCase):
 def setUp(self):self.c=json.loads((R/'corpus/jinshu/043-wangyan.json').read_text())
 def test_full_received_unit_unchanged_and_no_death_years(self):
  self.assertEqual(source_errors(self.c,R),[])
  self.assertEqual(len(self.c['paragraphs']),10);self.assertEqual(sum(len(p['text'])for p in self.c['paragraphs']),1811)
  original_slots = {
   'age-yan-14',
   'age-yan-56',
   'cheng-younger-brother-yan',
   'daughter-father-yan',
   'daughter-prince-marriage',
   'death-xuan',
   'death-yan',
   'death-yi',
   'death-youngson',
   'dun-younger-agnatic-cousin-yan',
   'name-cheng',
   'name-xuan',
   'name-yan',
   'name-yi',
   'xuan-father-yan',
   'xuan-station',
   'yan-father-yi',
   'yan-guo-spouses',
   'yan-residence',
   'yangjun-daughter',
   'yi-death-place',
   'youngson-father-yan',
  }
  vs=[v for v in records(self.c,R)if v['fixed_source_fact_binding']['slot']in original_slots]
  self.assertEqual({v['fixed_source_fact_binding']['slot']for v in vs},original_slots)
  self.assertEqual(len(vs),len(original_slots))
  deaths=[v for v in vs if v.get('event_type')=='death'];self.assertEqual(len(deaths),4)
  self.assertTrue(all(v.get('date_expression')is None and 'normalized_date'not in v for v in deaths))
  self.assertTrue(all(v.get('birth_year')is None for v in vs if 'age_context'in v))
 def test_immediate_sibling_boundary_cannot_skip_or_shorten(self):
  raw=(R/self.c['source']['raw_file']).read_text()
  a,z,ps,ex=project(raw,self.c['title'],'===從弟衍===','===衍弟澄===')
  self.assertEqual([p['text']for p in ps],[p['text']for p in self.c['paragraphs']])
  for closing in ['===從弟衍===','===子玄===','===郭舒===']:
   with self.assertRaises(AssertionError):project(raw,self.c['title'],'===從弟衍===',closing)
  shifted=raw[:a]+raw[a:z].replace('子玄，字眉子，','\n===假附傳===\n子玄，字眉子，')+raw[z:]
  with self.assertRaises(AssertionError):project(shifted,self.c['title'],'===從弟衍===','===衍弟澄===')
 def test_trusted_ref_cannot_be_removed(self):
  c=copy.deepcopy(self.c);del c['annotation']['fixed_wikisource_unit_ref'];self.assertTrue(source_errors(c,R))
 def test_044_existing_boundary_contract_unchanged(self):
  c=json.loads((R/'corpus/jinshu/044-luchen-cuiyue.json').read_text());self.assertEqual(source_errors(c,R),[])
 def test_consistent_wrong_recipient_and_invented_year_rejected(self):
  vs=records(self.c,R);death=next(v for v in vs if v['id'].endswith('death-yan'));other=next(v for v in vs if v['id'].endswith('death-xuan'))
  v=copy.deepcopy(death);v['person_id']=other['person_id'];v['evidence']=other['evidence'];self.assertFalse(valid(v,self.c,R))
  v=copy.deepcopy(death);v['normalized_date']={'year':311};self.assertFalse(valid(v,self.c,R))
if __name__=='__main__':unittest.main()
