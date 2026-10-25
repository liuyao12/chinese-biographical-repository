from pathlib import Path
import unittest,json,copy
from scripts.civil_era_ranges import civil_era_range_errors
from scripts.fixed_kanripo_fact_slots import valid
ROOT=Path(__file__).resolve().parents[1]
class NativeShape(unittest.TestCase):
 def test_both_supported_attestations_keep_single_date_source(self):
  ch=json.loads((ROOT/'corpus/sanguozhi/023-peiqian.json').read_text());h=next(h for h in json.loads((ROOT/'corpus/sanguozhi/023-peiqian-phaseb-titles.json').read_text())['holdings']if h['id'].endswith('-008'))
  self.assertTrue(valid(h,ch,ROOT));a=h['attestations'][0];v=a['normalized_date_range'];self.assertEqual(v['evidence'],h['evidence']);self.assertEqual(v['original_quote'],h['evidence'][0]['quote']);self.assertIsNone(h['attestations'][1]['date_expression']);self.assertEqual(civil_era_range_errors(v,h['evidence'],a['date_expression']),[])
  bad=copy.deepcopy(h);bad['attestations'][1]['date_expression']='咸熙中';self.assertFalse(valid(bad,ch,ROOT))
 def test_naming_has_actual_death_and_naming_quote(self):
  ch=json.loads((ROOT/'corpus/sanguozhi/023-peiqian.json').read_text());h=next(h for h in json.loads((ROOT/'corpus/sanguozhi/023-peiqian-phaseb-titles.json').read_text())['holdings']if h['id'].endswith('-027'));self.assertTrue(valid(h,ch,ROOT));b=h['naming_basis'];self.assertEqual(b['source_term'],'秦始七年薨諡元公');self.assertEqual(b['death_term'],'薨');self.assertEqual(b['evidence'],h['effective_period']['start']['evidence']);self.assertTrue(all(b['source_term']in e['quote']for e in b['evidence']));bad=copy.deepcopy(h);bad.pop('naming_basis');self.assertFalse(valid(bad,ch,ROOT))

 def test_explicit_posthumous_grant_has_standard_basis(self):
  ch=json.loads((ROOT/'corpus/sanguozhi/023-peiqian.json').read_text());h=next(h for h in json.loads((ROOT/'corpus/sanguozhi/023-peiqian-phaseb-titles.json').read_text())['holdings']if h['id'].endswith('-045'));self.assertTrue(valid(h,ch,ROOT));b=h['posthumous_basis'];self.assertEqual(b['source_term'],'追贈長水校尉');self.assertEqual(b['evidence'],h['effective_period']['start']['evidence']);self.assertTrue(all(b['source_term']in e['quote']for e in b['evidence']));bad=copy.deepcopy(h);bad.pop('posthumous_basis');self.assertFalse(valid(bad,ch,ROOT))
