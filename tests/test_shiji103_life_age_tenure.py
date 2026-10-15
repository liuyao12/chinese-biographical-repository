import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((ROOT/'corpus/shiji'/n).read_text())
class LifeAgeTenure(unittest.TestCase):
    def test_father_and_son_deaths_do_not_share_date(self):
        es=read('103-life-events.json')['events'];self.assertEqual(len(es),6)
        father,son=es[:2]
        self.assertEqual(father['person_id'],'esh_e0a_jrw_A')
        self.assertEqual(son['person_id'],'esh_e0a_jrw_AA')
        self.assertEqual(father['normalized_date_range']['earliest']['year'],-124)
        self.assertEqual(father['normalized_date_range']['latest']['year'],-123)
        self.assertIsNone(son['date_expression'])
        self.assertNotIn('normalized_date_range',son)
        for e in es:self.assertIn(e['source_term'],e['evidence'][0]['quote'])
    def test_qing_death_numeric_year_is_its_own_quote(self):
        e=read('103-life-events.json')['events'][2]
        self.assertEqual(e['person_id'],'esh_e0a_jrw_AD')
        self.assertEqual(e['normalized_date']['year'],-102)
        self.assertEqual(e['normalized_date']['evidence'],e['evidence'])
        self.assertIn('太初二年中',e['normalized_date']['original_quote'])
    def test_fifteen_is_reported_age_not_birth_year(self):
        a=read('103.json')['annotation']['age_assertions'][0]
        self.assertEqual(a['value'],15)
        self.assertEqual(a['person_id'],'esh_e0a_jrw_A')
        self.assertIsNone(a['birth_year'])
        self.assertEqual(a['date_expression'],'髙祖東撃項籍，過河内')
    def test_qing_tenures_do_not_end_noble_title_or_other_offices(self):
        hs={h['id']:h for h in read('103-titles.json')['holdings']}
        self.assertEqual(hs['th-shiji103-018']['reported_duration']['value'],7)
        self.assertEqual(hs['th-shiji103-020']['reported_duration']['value'],9)
        self.assertNotIn('reported_duration',hs['th-shiji103-021'])
        self.assertNotIn('reported_duration',hs['th-shiji103-035'])
        self.assertEqual(hs['th-shiji103-021']['effective_period']['end']['status'],'unknown')
