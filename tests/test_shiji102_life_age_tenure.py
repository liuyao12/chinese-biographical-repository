import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'corpus/shiji'/name).read_text())
class LifeAgeTenure(unittest.TestCase):
    def test_deaths_do_not_turn_sentence_or_death_into_dates(self):
        es=read('102-life-events.json')['events']
        self.assertEqual(len(es),4)
        self.assertEqual({e['person_id'] for e in es},{'yqp_nlb_p1p_AC','dq6_ovk_58c','97s_gzq_ow9','hph_y6n_3zb'})
        for e in es:
            self.assertEqual(e['event_type'],'death')
            self.assertIsNone(e['date_expression'])
            self.assertNotIn('normalized_date_range',e)
            self.assertIn(e['source_term'],e['evidence'][0]['quote'])
        self.assertFalse(any(e['person_id']=='feo_rlp_5n7' for e in es))
    def test_feng_age_is_report_not_lifespan(self):
        a=read('102.json')['annotation']['age_assertions'][0]
        self.assertEqual(a['person_id'],'rl6_a40_3hj_AA')
        self.assertEqual(a['date_expression'],'武帝立')
        self.assertEqual(a['bounds'],{'lower':90,'lower_inclusive':False,'upper':None,'upper_inclusive':None})
        self.assertIsNone(a['birth_year'])
        self.assertIsNone(a['value'])
    def test_ten_source_years_do_not_set_calendar_endpoints(self):
        h=next(h for h in read('102-titles.json')['holdings'] if h['id']=='th-shiji102-001')
        self.assertEqual(h['reported_duration']['value'],10)
        self.assertEqual(h['reported_duration']['source_term'],'十歳')
        self.assertEqual(h['effective_period']['start']['status'],'unknown')
        self.assertEqual(h['effective_period']['end']['status'],'unknown')
        self.assertEqual(h['reported_duration']['evidence'][0]['person_mention_id'],'c-shiji-102-zhangfeng:m001-0013')
