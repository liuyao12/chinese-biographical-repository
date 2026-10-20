import copy,unittest
from scripts.date_ranges import year_range_errors,year_range_label

class SingleYearEraRangeTests(unittest.TestCase):
    def setUp(self):
        self.e=[{'chapter_id':'c','paragraph_id':'p','source_id':'s','quote':'前廢帝景和中為義恭太宰從事中郎義恭敗以黨與下獄死'}]
        self.v={'basis':'within_named_era','calendar':'chinese_civil','precision':'year_range','year_numbering':'astronomical','status':'editorial_provisional','source_expression':'景和中','original_quote':self.e[0]['quote'],'evidence':self.e,
          'era_span_mapping':{'kind':'ce_regnal_era_span','era_name':'景和','polity_source_name':'宋','start_ce_year':465,'end_ce_year':465,'reference_index':0},
          'references':[{'scope':'modern_era_year_equivalence_only','url':'https://dict.revised.moe.edu.tw/appendix.jsp?ID=3&page=2','quote':'景和','columns':{'dynasty':'宋','era_name':'景和','first_year':'465','last_year':'465'}}],
          'earliest':{'era':'CE','era_year':465,'year':465},'latest':{'era':'CE','era_year':465,'year':465},'rationale':'年號表只證一年年號；原詞中照存，不改成元年或定月日。','reviewer':'AI','human_reviewed':False}

    def test_one_year_era_retains_stage_without_inventing_regnal_one_or_day(self):
        self.assertEqual([],year_range_errors(self.v,self.e,'景和中'))
        self.assertNotIn('year',self.v);self.assertNotIn('era_year',self.v)
        self.assertEqual('景和中',self.v['source_expression'])
        self.assertEqual('西元465年（中國曆年；月日未定）',year_range_label(self.v))
        self.assertNotIn('regnal_year',self.v['era_span_mapping'])

    def test_era_evidence_and_precision_mutations_rejected(self):
        mutations=[
         lambda v:v['era_span_mapping'].update(end_ce_year=464),
         lambda v:v['era_span_mapping'].update(start_ce_year=0),
         lambda v:v['references'][0]['columns'].update(first_year='464'),
         lambda v:v['references'][0].update(quote='義熙'),
         lambda v:v['latest'].update(year=466,era_year=466),
         lambda v:v['earliest'].update(month=1),
         lambda v:v.update(year=465),lambda v:v.update(era_year=465),
         lambda v:v.update(month=1),lambda v:v.update(day=1),
         lambda v:v.update(lunar_month=1),lambda v:v.update(lunar_day=1),
         lambda v:v.update(source_expression='景和元年'),
         lambda v:v.update(source_expression='景和末'),
         lambda v:v.update(human_reviewed=True),
        ]
        for m in mutations:
            v=copy.deepcopy(self.v);m(v)
            with self.subTest(mutation=m):self.assertTrue(year_range_errors(v,self.e,v['source_expression']))

    def test_multi_year_era_still_outer_window_without_selected_year(self):
        v=copy.deepcopy(self.v);e=[dict(self.e[0],quote='元嘉末為太尉諮議參軍')]
        v.update(source_expression='元嘉末',source_stage='末',evidence=e,original_quote=e[0]['quote'])
        v['era_span_mapping'].update(era_name='元嘉',start_ce_year=424,end_ce_year=453)
        v['references'][0].update(quote='元嘉');v['references'][0]['columns'].update(era_name='元嘉',first_year='424',last_year='453')
        v['earliest'].update(era_year=424,year=424);v['latest'].update(era_year=453,year=453)
        self.assertEqual([],year_range_errors(v,e,'元嘉末'))
        self.assertEqual('西元424至453年（中國曆年範圍）',year_range_label(v))

if __name__=='__main__':unittest.main()
