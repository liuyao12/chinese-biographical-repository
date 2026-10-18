import unittest

from scripts.date_ranges import year_range_errors, year_range_label


class CivilEraRanges(unittest.TestCase):
    def fixture(self):
        evidence = [{'quote': 'Synthetic event in 甲元中.'}]
        value = dict(basis='within_named_era', calendar='chinese_civil', precision='year_range',
                     year_numbering='astronomical', status='editorial_provisional',
                     source_expression='甲元中', original_quote=evidence[0]['quote'], evidence=evidence,
                     earliest={'era':'CE','era_year':100,'year':100},
                     latest={'era':'CE','era_year':108,'year':108},
                     era_span_mapping=dict(kind='ce_regnal_era_span',era_name='甲元',
                                           polity_source_name='Synthetic polity',start_ce_year=100,
                                           end_ce_year=108,reference_index=0),
                     references=[dict(url='https://example.org/synthetic-era-table',quote='甲元',
                                      scope='modern_era_year_equivalence_only',
                                      columns=dict(era_name='甲元',dynasty='Synthetic polity',first_year='100',last_year='108'))],
                     rationale='Synthetic whole-era outer bounds, not a tenure or chosen middle year.',
                     reviewer='Synthetic test',human_reviewed=False)
        return value, evidence

    def test_whole_era_outer_bounds_are_not_a_two_year_calendar_projection(self):
        value, evidence = self.fixture()
        self.assertEqual(year_range_errors(value,evidence,'甲元中'),[])
        self.assertEqual(year_range_label(value),'西元100至108年（中國曆年範圍）')

    def test_endpoint_cannot_be_narrowed_or_promoted_to_one_event_year(self):
        for change in ['first','last','exact']:
            value,evidence=self.fixture()
            if change=='first':value['earliest'].update(era_year=104,year=104)
            if change=='last':value['latest'].update(era_year=104,year=104)
            if change=='exact':value['year']=104
            self.assertTrue(year_range_errors(value,evidence,'甲元中'))

    def test_era_name_and_polity_must_both_match_reference_columns(self):
        for key in ['era_name','dynasty','first_year','last_year']:
            value,evidence=self.fixture();value['references'][0]['columns'][key]='unrelated'
            self.assertTrue(year_range_errors(value,evidence,'甲元中'))

    def test_original_expression_and_evidence_cannot_be_replaced(self):
        value,evidence=self.fixture()
        self.assertTrue(year_range_errors(value,evidence,'甲元元年'))
        self.assertTrue(year_range_errors(value,[{'quote':'Different event.'}],'甲元中'))

    def test_malformed_reference_or_quote_returns_errors_without_crashing(self):
        for change in ['mapping','references','quote','columns']:
            value,evidence=self.fixture()
            if change=='mapping':value['era_span_mapping']=None
            if change=='references':value['references']=[None]
            if change=='quote':value['original_quote']=None;value['evidence'][0]['quote']=None
            if change=='columns':value['references'][0]['columns']=None
            self.assertTrue(year_range_errors(value,evidence,'甲元中'))
