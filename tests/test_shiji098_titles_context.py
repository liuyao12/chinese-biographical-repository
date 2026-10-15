import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def holdings():return {h['id']:h for h in read('corpus/shiji/098-titles.json')['holdings']}
class FuJinTitleContextTests(unittest.TestCase):
    def test_five_emperor_references_resolve_in_their_narrative_context(self):
        c=read('corpus/shiji/098.json');actual=[]
        for n in [10,11,13]:
            p=c['paragraphs'][n-1]
            actual += [m for m in p['mentions'] if m['surface']=='上']
        self.assertEqual(len(actual),5)
        self.assertEqual({m['person_id'] for m in actual},{'yqp_nlb_p1p_A'})
        p=c['paragraphs'][9];at=p['text'].index('霸上')+1
        self.assertFalse(any(m['start']<=at<m['end'] for m in p['mentions']))
        p=c['paragraphs'][10];at=p['text'].index('秦攻破天下')
        self.assertFalse(any(m['start']<=at<m['end'] for m in p['mentions']))
    def test_interpretation_lists_actual_five_new_anchors(self):
        d=next(d for d in read('corpus/shiji/098-identities.json')['decisions'] if d['id']=='d-shiji098-040')
        self.assertEqual(sum(len(e['mention_ids']) for e in d['evidence']),5)
        self.assertEqual(len(d['evidence']),3)
    def test_qi_five_years_is_duration_not_appointment_year(self):
        h=holdings()['th-shiji098-013'];duration=h['reported_duration']
        self.assertEqual((duration['value'],duration['unit']),(5,'title_year'))
        self.assertEqual(duration['source_number'],'五')
        self.assertEqual(duration['source_term'],'五歲為齊相國')
        self.assertEqual(duration['counting'],'unspecified_source_years')
        self.assertEqual(h['effective_period']['start']['status'],'unknown')
        self.assertIsNone(h['effective_period']['start']['date_expression'])
        self.assertEqual(h['references'][0]['text_layer'],'zhengyi_commentary')
        self.assertEqual(h['references'][0]['quote'],'爲齊悼惠王劉肥相五歲也。')
    def test_four_title_endpoints_keep_their_own_date_expression_and_evidence(self):
        hs=holdings()
        for hid,endpoint,years in [('th-shiji098-035','end',(162,161)),('th-shiji098-040','start',(196,195)),('th-shiji098-043','start',(149,148)),('th-shiji098-043','end',(115,114))]:
            boundary=hs[hid]['effective_period'][endpoint];r=boundary['normalized_date_range']
            self.assertEqual((r['earliest']['era_year'],r['latest']['era_year']),years)
            self.assertEqual(r['evidence'],boundary['evidence'])
            self.assertIn(boundary['date_expression'],r['original_quote'])
            self.assertTrue(r['evidence'][0]['person_mention_id'])
            self.assertEqual(r['year_numbering'],'astronomical')
    def test_title_ranges_export_as_endpoints_and_never_as_deaths(self):
        b=read('exports/persons/fvm_66f_0k3_CA.json')
        ranges=[r for r in b['date_range_normalizations'] if r['record_id']=='th-shiji098-043']
        self.assertEqual({r['endpoint'] for r in ranges},{'start','end'})
        self.assertTrue(all(r['date_role']=='title_period' and 'event_type' not in r for r in ranges))
    def test_unresolved_month_and_year_phrases_remain_unconverted(self):
        for hid,term in [('th-shiji098-017','一月'),('th-shiji098-018','二歲')]:
            boundary=holdings()[hid]['effective_period']['start']
            self.assertEqual(boundary['date_expression'],term)
            self.assertNotIn('normalized_date',boundary)
            self.assertNotIn('normalized_date_range',boundary)
