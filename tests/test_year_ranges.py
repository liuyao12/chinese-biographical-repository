# coding: utf-8
import copy,json,unittest
from pathlib import Path
from scripts.date_ranges import year_range_errors, year_range_label
ROOT=Path(__file__).resolve().parents[1]
class YearRangeTests(unittest.TestCase):
    def boundary(self):
        data=json.loads((ROOT/'corpus/shiji/093-titles.json').read_text())
        return next(h for h in data['holdings'] if h['id']=='th-shiji093-030')['effective_period']['start']
    def test_cross_year_dates_remain_ranges_not_exact_event_years(self):
        b=self.boundary();r=b['normalized_date_range']
        self.assertEqual(year_range_errors(r,b['evidence'],b['date_expression']),[])
        self.assertEqual(year_range_label(r),'西元前145至144年（暫定範圍）')
        self.assertNotIn('normalized_date',b)
        profile=json.loads((ROOT/'data/corpus/profiles/jjl_irg_zke_A*A.json').read_text())
        h=next(h for h in profile['titles'] if h['id']=='th-shiji093-030')
        self.assertIn('145至144',h['period'])
    def test_rejects_false_range_order_single_year_and_numbering(self):
        b=self.boundary()
        for mutation in ('reverse','single','numbering','boolean'):
            r=copy.deepcopy(b['normalized_date_range'])
            if mutation=='reverse':r['earliest'],r['latest']=r['latest'],r['earliest']
            if mutation=='single':r['latest']=copy.deepcopy(r['earliest'])
            if mutation=='numbering':r['earliest']['year']=-167
            if mutation=='boolean':r['latest']['era_year']=True
            self.assertTrue(year_range_errors(r,b['evidence'],b['date_expression']),mutation)
    def test_rejects_missing_calendar_and_mismatched_evidence(self):
        b=self.boundary();r=copy.deepcopy(b['normalized_date_range'])
        r['references']=[v for v in r['references'] if v['scope']!='received_calendar_rule']
        self.assertTrue(year_range_errors(r,b['evidence'],b['date_expression']))
        r=copy.deepcopy(b['normalized_date_range']);r['original_quote']='孝文十五年'
        self.assertTrue(year_range_errors(r,b['evidence'],b['date_expression']))
        self.assertTrue(year_range_errors(b['normalized_date_range'],b['evidence'],None))
        self.assertTrue(year_range_errors(b['normalized_date_range'],b['evidence'],'孝文十五年'))

    def test_tuidang_and_ying_grants_follow_dated_table_not_surrender_year(self):
        holdings=json.loads((ROOT/'corpus/shiji/093-titles.json').read_text())['holdings']
        for hid in ('th-shiji093-013','th-shiji093-014'):
            h=next(h for h in holdings if h['id']==hid)
            b=h['effective_period']['start']
            self.assertIsNone(b['date_expression'])
            self.assertEqual(b['normalized_date']['era_year'],164)
            self.assertEqual(b['normalized_date']['basis']['kind'],'parallel_event')
            self.assertNotIn('normalized_date_range',b)
            self.assertIn('十六年六月丙子',b['normalized_date']['basis']['reference_event_quote'])
        table=json.loads((ROOT/'data/historical-tables/shiji-019.json').read_text())
        names={m['surface']:m['person_id'] for f in table['fragments'] for r in f['rows'] for c in r['cells'] for m in c.get('person_mentions',[]) if m['surface'] in ('韓頹當','韓嬰')}
        self.assertEqual(names,{'韓頹當':'l9e_fbr_36a_*AB','韓嬰':'l9e_fbr_36a_*AAA'})
        cells={c['id']:c for f in table['fragments'] for r in f['rows'] for c in r['cells']}
        for cid in ('shiji-019-t3-r024-c01','shiji-019-t3-r025-c01'):
            self.assertTrue(any(m['surface']=='韓王信' and m['person_id']=='l9e_fbr_36a_*A' for m in cells[cid]['person_mentions']))
        self.assertTrue(any(m['surface']=='太子' and m['person_id']=='l9e_fbr_36a_*AA' for m in cells['shiji-019-t3-r025-c01']['person_mentions']))
