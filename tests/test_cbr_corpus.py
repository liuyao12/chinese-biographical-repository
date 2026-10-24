import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('corpus_validator',ROOT/'scripts/validate_corpus.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve()
        for folder in ('registry','corpus','source-evidence'):shutil.copytree(ROOT/folder,self.root/folder)
        shutil.copytree(ROOT/'data/historical-tables',self.root/'data/historical-tables')
        # Source-scoped display choices bind records in the editorial name dataset.
        (self.root/'data/corpus').mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/'data/corpus/profile-names.json', self.root/'data/corpus/profile-names.json')
        # Source-bound claims need their complete fixed witnesses and date references.
        shutil.copytree(ROOT/'sources', self.root/'sources')
        shutil.copytree(ROOT/'data/works', self.root/'data/works')
        # Validators bind complete witnesses to trusted JSON recipes/pins in root/scripts.
        # Copy data only; production code stays imported from the actual repository.
        (self.root/'scripts').mkdir()
        for config in (ROOT/'scripts').glob('*.json'):
            shutil.copy2(config, self.root/'scripts'/config.name)
    def change(self,path,fn):
        p=self.root/path;d=json.loads(p.read_text());fn(d);p.write_text(json.dumps(d,ensure_ascii=False))
    def test_work_mention_cannot_link_person(self):
        self.change('corpus/shiji/063.json', lambda d: next(m for p in d['paragraphs'] for m in p['mentions'] if m['id'].endswith('m011-0079')).update(person_id='vtn_thh_540'))
        self.assertIn('著作提及須引用已登記著作且不得連人物', v.validate(self.root))
    def test_work_mention_requires_registered_work(self):
        self.change('corpus/shiji/063.json', lambda d: next(m for p in d['paragraphs'] for m in p['mentions'] if m['id'].endswith('m011-0079')).update(work_id='w-missing'))
        self.assertIn('著作提及須引用已登記著作且不得連人物', v.validate(self.root))
    def test_work_attestation_cannot_point_to_person_occurrence(self):
        self.change('registry/works.json', lambda d: next(w for w in d['works'] if w['id']=='w-shenzi')['reference_attestations'][0].update(mention_id='c-shiji-063-laohan:m011-0044'))
        self.assertIn('著作登記證據須對應同一書名錨點及完整原文', v.validate(self.root))
    def test_later_naming_requires_death_in_its_scoped_source_term(self):
        self.change('corpus/shiji/088-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji088-017')['naming_basis'].update(source_term='故立號曰『繆』'))
        self.assertIn('死後諡名缺少相符命名詞、死亡詞與起點證據', v.validate(self.root))
    def test_later_naming_must_match_received_name(self):
        self.change('corpus/shiji/088-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji088-017').update(title='穆'))
        self.assertIn('死後諡名缺少相符命名詞、死亡詞與起點證據', v.validate(self.root))
    def test_adoptive_mother_requires_explicit_received_term(self):
        self.change('corpus/shiji/085-assertions.json', lambda d: d['assertions'][-1]['qualifiers'].update(source_term='母'))
        self.assertIn('所母關係須保存原詞，不得由一般母稱推定', v.validate(self.root))
    def test_household_revenue_cannot_be_relabelled_residence(self):
        self.change('corpus/shiji/085-addresses.json', lambda d: d['assertions'][1].update(relation='residence'))
        self.assertIn('食邑主張須保存湯沐邑或奉原詞及類型，不得改為籍貫', v.validate(self.root))
    def test_household_revenue_requires_full_allocation_wording(self):
        self.change('corpus/shiji/085-addresses.json', lambda d: d['assertions'][1].update(source_term='食'))
        self.assertIn('食戶地望須保存食地名與戶數原語，不得當人口或居處', v.validate(self.root))
    def test_tangmu_estate_cannot_be_relabelled_native_place(self):
        self.change('corpus/shiji/077-addresses.json', lambda d: d['assertions'][4].update(relation='native_place'))
        self.assertIn('食邑主張須保存湯沐邑或奉原詞及類型，不得改為籍貫', v.validate(self.root))
    def test_maintenance_allocation_cannot_be_relabelled_tangmu(self):
        self.change('corpus/shiji/077-addresses.json', lambda d: d['assertions'][5]['qualifiers'].update(fief_kind='tangmu_estate'))
        self.assertIn('食邑主張須保存湯沐邑或奉原詞及類型，不得改為籍貫', v.validate(self.root))
    def test_residence_years_cannot_be_title_years(self):
        self.change('corpus/shiji/077-addresses.json', lambda d: d['assertions'][6]['reported_duration'].update(unit='title_year'))
        self.assertIn('居留來源年數須有數值、原數詞與同項證據，不得當官爵任期或推曆日', v.validate(self.root))
    def test_residence_duration_cannot_change_source_numeral(self):
        self.change('corpus/shiji/077-addresses.json', lambda d: d['assertions'][6]['reported_duration'].update(value=11))
        self.assertIn('居留來源年數須有數值、原數詞與同項證據，不得當官爵任期或推曆日', v.validate(self.root))
    def test_continuous_address_requires_all_intervening_paragraphs(self):
        self.change('corpus/shiji/069-addresses.json', lambda d: d['assertions'][3]['evidence'][0]['context'].update(intervening_paragraph_ids=['c-shiji-069-su:p004']))
        self.assertIn('地址主語承接須有同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_continuous_address_cannot_reverse_paragraph_order(self):
        self.change('corpus/shiji/069-addresses.json', lambda d: d['assertions'][3]['evidence'][0]['context']['intervening_paragraph_ids'].reverse())
        self.assertIn('地址主語承接須有同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_continuous_address_cannot_replace_subject_with_local_ruler(self):
        self.change('corpus/shiji/069-addresses.json', lambda d: d['assertions'][2].update(person_id='ho4_me8_not'))
        self.assertIn('地址主語承接須有同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_unspecified_affinity_cannot_invent_connecting_daughter(self):
        self.change('corpus/shiji/069-assertions.json', lambda d: d['assertions'][-1]['qualifiers'].update(connecting_person_ids=['invented-daughter']))
        self.assertIn('未明姻親須保存婚原詞，不得補配偶、連接人物或世代', v.validate(self.root))
    def test_unspecified_affinity_requires_marriage_wording(self):
        self.change('corpus/shiji/069-assertions.json', lambda d: d['assertions'][-1]['qualifiers'].update(source_term='燕相子之'))
        self.assertIn('未明姻親須保存婚原詞，不得補配偶、連接人物或世代', v.validate(self.root))
    def test_unknown_office_restoration_cannot_bind_known_title(self):
        self.change('corpus/shiji/069-person-events.json', lambda d: d['events'][1].update(office_title='從約長',title_holding_id='th-shiji069-004'))
        self.assertIn('未名官職不復任或恢復須保留原詞，不得補官名或已知持職連結', v.validate(self.root))
    def test_office_non_reinstatement_cannot_be_relabelled_restoration(self):
        self.change('corpus/shiji/069-person-events.json', lambda d: d['events'][0].update(event_type='office_restoration'))
        self.assertIn('未名官職不復任或恢復須保留原詞，不得補官名或已知持職連結', v.validate(self.root))
    def test_polity_lineage_address_requires_royal_scope(self):
        self.change('corpus/shiji/068-addresses.json', lambda d: next(a for a in d['assertions'] if a['id']=='pa-shiji068-007').update(qualifiers={}))
        self.assertIn('宗族政體地望須有來源身份詞，不改作出生籍貫', v.validate(self.root))
    def test_polity_lineage_address_cannot_drop_lineage_phrase(self):
        self.change('corpus/shiji/068-addresses.json', lambda d: next(a for a in d['assertions'] if a['id']=='pa-shiji068-007').update(source_term='衛'))
        self.assertIn('宗族政體地望須有來源身份詞，不改作出生籍貫', v.validate(self.root))
    def change_shang_approximation(self, fn):
        self.change('corpus/shiji/068-titles.json', lambda d: fn(next(h for h in d['holdings'] if h['id']=='th-shiji068-020')['reported_duration']))
    def test_title_adjacent_years_cannot_be_exact(self):
        self.change_shang_approximation(lambda d: d.update(value=6))
        self.assertIn('稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字', v.validate(self.root))
    def test_title_adjacent_years_cannot_be_strict_bounds(self):
        self.change_shang_approximation(lambda d: d.update(bounds={'lower':6,'upper':7,'lower_inclusive':True,'upper_inclusive':True}))
        self.assertIn('稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字', v.validate(self.root))
    def test_title_adjacent_years_require_source_numbers(self):
        self.change_shang_approximation(lambda d: d['approximation'].update(numbers=[6,8]))
        self.assertIn('稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字', v.validate(self.root))
    def test_title_adjacent_years_cannot_change_unit(self):
        self.change_shang_approximation(lambda d: d.update(unit='title_month',counting='unspecified_source_months'))
        self.assertIn('稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字', v.validate(self.root))
    def test_title_adjacent_years_cannot_change_source_numeral(self):
        self.change_shang_approximation(lambda d: d.update(source_number='六八'))
        self.assertIn('稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字', v.validate(self.root))
    def test_title_adjacent_years_reject_nonadjacent_source_reading(self):
        self.change_shang_approximation(lambda d: d.update(source_number='六八',source_term='相秦六八年',approximation={'kind':'adjacent_year_numbers','numbers':[6,8]}))
        self.assertIn('稱號相鄰年數約數須保留原數詞、未知精確值及非界限數字', v.validate(self.root))
    def test_reported_age_group_cannot_switch_person(self):
        self.change('corpus/shiji/063.json', lambda d: d['annotation']['age_assertions'][1].update(person_id='huf_d39_8pf'))
        self.assertIn('同組報齡須同人物及來源段落', v.validate(self.root))
    def test_reported_age_alternative_cannot_orphan_group(self):
        self.change('corpus/shiji/063.json', lambda d: d['annotation']['age_assertions'][1].update(report_group_id='orphan-report'))
        self.assertIn('報齡替代傳聞缺同組主報齡', v.validate(self.root))
    def test_reported_age_lower_bound_matches_number(self):
        self.change('corpus/shiji/063.json', lambda d: d['annotation']['age_assertions'][0]['bounds'].update(lower=200))
        self.assertIn('個人報齡餘歲界限與原詞不符', v.validate(self.root))
    def test_age_source_hundreds_keep_explicit_number(self):
        self.assertEqual(v.source_age_number('百有六十'),160)
        self.assertEqual(v.source_age_number('二百'),200)
        self.assertIsNone(v.source_age_number('百餘'))
    def test_reported_age_cannot_be_exact(self):
        self.change('corpus/shiji/063.json', lambda d: d['annotation']['age_assertions'][0].update(value=160))
        self.assertIn('個人報齡餘歲界限與原詞不符', v.validate(self.root))
    def test_reported_age_cannot_invent_upper(self):
        self.change('corpus/shiji/063.json', lambda d: d['annotation']['age_assertions'][0]['bounds'].update(upper=170))
        self.assertIn('個人報齡餘歲界限與原詞不符', v.validate(self.root))
    def test_reported_age_cannot_drop_qualification(self):
        self.change('corpus/shiji/063.json', lambda d: d['annotation']['age_assertions'][1].update(qualified_source_term='二百餘歲'))
        self.assertIn('個人報齡缺來源限定詞或傳聞狀態', v.validate(self.root))
    def test_royal_inheritance_rejects_unrelated_predecessor(self):
        self.change('corpus/shiji/058-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji058-026')['inheritance'].update(predecessor_person_id='yqp_nlb_p1p_ACC'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_royal_inheritance_rejects_changed_kingdom(self):
        self.change('corpus/shiji/058-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji058-026')['inheritance'].update(resolved_title='代王'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_royal_inheritance_rejects_mixed_rank_kind(self):
        self.change('corpus/shiji/058-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji058-026').update(kind='noble_rank'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_royal_inheritance_chain_rejects_cycle(self):
        self.change('corpus/shiji/058-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji058-026')['inheritance'].update(predecessor_holding_id='th-shiji058-038'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_royal_inheritance_chain_rejects_missing_predecessor(self):
        self.change('corpus/shiji/058-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji058-038')['inheritance'].update(predecessor_holding_id='th-shiji058-999'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_life_subject_context_rejects_wrong_person(self):
        self.change('corpus/shiji/059-life-events.json', lambda d: next(e for e in d['events'] if e['id']=='le-shiji059-015').update(person_id='yqp_nlb_p1p_ACAC'))
        self.assertIn('生卒主語承接須有近前同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_life_subject_context_requires_intervening_paragraph(self):
        self.change('corpus/shiji/059-life-events.json', lambda d: next(e for e in d['events'] if e['id']=='le-shiji059-017')['evidence'][0]['context'].update(intervening_paragraph_ids=[]))
        self.assertIn('生卒主語承接須有近前同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_life_subject_context_anchor_must_be_in_quote(self):
        self.change('corpus/shiji/059-life-events.json', lambda d: next(e for e in d['events'] if e['id']=='le-shiji059-015')['evidence'][0]['context'].update(quote='好儒學'))
        self.assertIn('生卒主語承接須有近前同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_life_subject_context_requires_event_term(self):
        self.change('corpus/shiji/059-life-events.json', lambda d: next(e for e in d['events'] if e['id']=='le-shiji059-015').update(source_term='德自殺'))
        self.assertIn('生卒主語承接須有近前同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_brother_inheritance_cannot_become_father(self):
        self.change('corpus/shiji/059-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji059-065')['inheritance'].update(predecessor_relation='father'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_brother_inheritance_rejects_unattested_relationship(self):
        self.change('corpus/shiji/059-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji059-065')['inheritance'].update(predecessor_relation='cousin'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_title_excess_years_cannot_be_exact(self):
        self.change('corpus/shiji/104-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji104-005')['reported_duration'].update(value=10))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_title_excess_years_cannot_change_unit(self):
        self.change('corpus/shiji/104-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji104-005')['reported_duration'].update(unit='title_month', counting='unspecified_source_months'))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_title_excess_years_cannot_invent_upper(self):
        self.change('corpus/shiji/104-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji104-005')['reported_duration']['bounds'].update(upper=20))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_title_bare_month_yu_cannot_be_year(self):
        self.change('corpus/shiji/104-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji104-013')['reported_duration'].update(unit='title_year', counting='unspecified_source_years'))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_parallel_death_window_rejects_unmatched_event(self):
        self.change('corpus/shiji/105-life-events.json', lambda d: d['events'][-1]['normalized_date_range']['parallel_event'].update(reference_event_quote='虛構死亡'))
        self.assertIn('生卒跨年範圍平行事件對讀無效', v.validate(self.root))
    def test_parallel_death_window_rejects_absent_source_quote(self):
        self.change('corpus/shiji/105-life-events.json', lambda d: d['events'][-1]['normalized_date_range']['parallel_event'].update(source_event_quote='虢太子死'))
        self.assertIn('生卒跨年範圍平行事件對讀無效', v.validate(self.root))
    def test_parallel_death_window_rejects_unmatched_year(self):
        self.change('corpus/shiji/105-life-events.json', lambda d: d['events'][-1]['normalized_date_range']['parallel_event'].update(reference_year_quote='166'))
        self.assertIn('生卒跨年範圍平行事件對讀無效', v.validate(self.root))
    def change_upper_age(self, fn):
        self.change('corpus/shiji/105.json', lambda d: fn(d['annotation']['age_assertions'][2]))
    def test_upper_age_cannot_be_exact_nineteen(self):
        self.change_upper_age(lambda a: a.update(value=19))
        self.assertIn('來源未滿報齡須保存開放上界及原詞，不得補確切歲數', v.validate(self.root))
    def test_upper_age_cannot_include_twenty(self):
        self.change_upper_age(lambda a: a['bounds'].update(upper_inclusive=True))
        self.assertIn('來源未滿報齡須保存開放上界及原詞，不得補確切歲數', v.validate(self.root))
    def test_upper_age_requires_not_full_wording(self):
        self.change_upper_age(lambda a: a.update(source_term='年二十'))
        self.assertIn('來源未滿報齡須保存開放上界及原詞，不得補確切歲數', v.validate(self.root))
    def change_teacher(self, fn):
        self.change('corpus/shiji/105-assertions.json', lambda d: fn(next(a for a in d['assertions'] if a['predicate']=='teacher')))
    def test_teacher_cannot_become_father(self):
        self.change_teacher(lambda a: a.update(predicate='father'))
        self.assertIn('師承須有學教原詞及同引句學生老師雙錨點，不得改作親屬', v.validate(self.root))
    def test_teacher_requires_teaching_wording(self):
        self.change_teacher(lambda a: a['qualifiers'].update(source_term='扁鵲者'))
        self.assertIn('師承須有學教原詞及同引句學生老師雙錨點，不得改作親屬', v.validate(self.root))
    def test_teacher_requires_correct_teacher_anchor(self):
        self.change_teacher(lambda a: a['evidence'][0].update(object_person_mention_id=a['evidence'][0]['subject_person_mention_id']))
        self.assertIn('師承須有學教原詞及同引句學生老師雙錨點，不得改作親屬', v.validate(self.root))
    def test_corpus(self):self.assertEqual(v.validate(self.root),[])
    def test_title_excess_months_cannot_be_exact(self):
        self.change('corpus/shiji/057-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji057-045')['reported_duration'].update(value=10))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_title_excess_month_lower_is_exclusive(self):
        self.change('corpus/shiji/057-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji057-044')['reported_duration']['bounds'].update(lower_inclusive=True))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_title_excess_months_cannot_invent_upper(self):
        self.change('corpus/shiji/057-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji057-045')['reported_duration']['bounds'].update(upper=20))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_title_excess_months_require_literal_yu(self):
        self.change('corpus/shiji/057-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji057-045')['reported_duration'].update(source_term='十月'))
        self.assertIn('稱號時長界限須保留餘字、未知精確值及排他下界', v.validate(self.root))
    def test_address_subject_cannot_skip_paragraph(self):
        def change(d):
            e=next(a for a in d['assertions'] if 'context' in a['evidence'][0])['evidence'][0]
            e['context']['paragraph_id']='c-shiji-057-zhou:p002'
            e['context']['person_mention_id']='c-shiji-057-zhou:m002-0009'
        self.change('corpus/shiji/057-addresses.json', change)
        self.assertIn('地址主語承接須有同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_address_subject_requires_same_person(self):
        def change(d):
            e=next(a for a in d['assertions'] if 'context' in a['evidence'][0])['evidence'][0]
            e['context']['person_mention_id']='c-shiji-057-zhou:m004-0008'
        self.change('corpus/shiji/057-addresses.json', change)
        self.assertIn('地址主語承接須有同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_address_subject_anchor_must_be_in_quote(self):
        def change(d):
            e=next(a for a in d['assertions'] if 'context' in a['evidence'][0])['evidence'][0]
            e['context']['quote']='以將軍從高帝'
        self.change('corpus/shiji/057-addresses.json', change)
        self.assertIn('地址主語承接須有同篇人物錨點、引句及完整中間段落', v.validate(self.root))
    def test_address_subject_cannot_be_implicit(self):
        def change(d):
            e=next(a for a in d['assertions'] if 'context' in a['evidence'][0])['evidence'][0]
            del e['context']
        self.change('corpus/shiji/057-addresses.json', change)
        self.assertIn('地址人物未見於證據段', v.validate(self.root))
    def test_posthumous_naming_preserves_wei_variant(self):
        data=json.loads((self.root/'corpus/shiji/056-titles.json').read_text())
        h=next(h for h in data['holdings'] if h['id']=='th-shiji056-051')
        self.assertEqual(h['naming_basis']['source_term'], '諡爲獻侯')
        self.assertEqual(v.validate(self.root), [])
    def test_posthumous_naming_must_name_this_title(self):
        def change(d):
            h=next(h for h in d['holdings'] if h['id']=='th-shiji056-051')
            h['title']='共侯'
            h['naming_basis']['source_term']='諡爲獻侯。子共侯買代侯'
        self.change('corpus/shiji/056-titles.json', change)
        self.assertIn('死後諡名缺少相符命名詞、死亡詞與起點證據', v.validate(self.root))
    def test_group_age_excess_cannot_be_exact(self):
        self.change('corpus/shiji/055.json', lambda d: d['annotation']['age_assertions'][0].update(value=80))
        self.assertIn('來源年齡界限與有餘原詞不符', v.validate(self.root))
    def test_group_age_lower_bound_is_exclusive(self):
        self.change('corpus/shiji/055.json', lambda d: d['annotation']['age_assertions'][0]['bounds'].update(lower_inclusive=True))
        self.assertIn('來源年齡界限與有餘原詞不符', v.validate(self.root))
    def test_group_age_cannot_include_emperor(self):
        self.change('corpus/shiji/055.json', lambda d: d['annotation']['age_assertions'][0]['group_reference']['person_ids'].__setitem__(1, 'yqp_nlb_p1p_A'))
        self.assertIn('群體報齡具名名單未見於引句', v.validate(self.root))
    def test_group_age_cannot_infer_birth(self):
        self.change('corpus/shiji/055.json', lambda d: d['annotation']['age_assertions'][0].update(birth_year=-275))
        self.assertIn('來源年齡不得推定計歲方式或出生年', v.validate(self.root))
    def test_waisun_preserves_maternal_two_generations(self):
        self.change('corpus/shiji/124-assertions.json', lambda d: d['assertions'][-1]['qualifiers'].update(generation_difference=-1))
        self.assertIn('外孫祖母關係須保留母系兩代與原句未名母親', v.validate(self.root))
    def test_waisun_cannot_be_paternal(self):
        self.change('corpus/shiji/124-assertions.json', lambda d: d['assertions'][-1]['qualifiers'].update(lineage='paternal'))
        self.assertIn('外孫祖母關係須保留母系兩代與原句未名母親', v.validate(self.root))

    def test_inheritance_rejects_unrelated_predecessor(self):
        self.change('corpus/shiji/111-titles.json', lambda d: next(h for h in d['holdings'] if 'inheritance' in h)['inheritance'].update(predecessor_person_id='5dd_l1c_6g8'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_inheritance_rejects_changed_rank(self):
        self.change('corpus/shiji/111-titles.json', lambda d: next(h for h in d['holdings'] if 'inheritance' in h)['inheritance'].update(resolved_title='長平侯'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_inheritance_requires_source_term(self):
        self.change('corpus/shiji/111-titles.json', lambda d: next(h for h in d['holdings'] if 'inheritance' in h)['inheritance'].update(source_term='嬗封冠軍侯'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_title_years_cannot_be_elapsed_calendar_years(self):
        self.change('corpus/shiji/111-titles.json', lambda d: next(h for h in d['holdings'] if h.get('reported_duration', {}).get('unit') == 'title_year')['reported_duration'].update(counting='elapsed_calendar_years'))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_parallel_event_accepts_received_regnal_year_with_separate_quotes(self):
        data = json.loads((self.root/'corpus/shiji/111-titles.json').read_text())
        date = next(h for h in data['holdings'] if h['attestations'][0]['paragraph_id'].endswith(':p010'))['attestations'][0]['normalized_date']
        self.assertTrue(v.parallel_event_date(date))
        year_ref = next(r for r in date['references'] if r['scope'] == 'received_regnal_year_attestation')
        year_ref['scope'] = 'unspecified_reference'
        self.assertFalse(v.parallel_event_date(date))
    def test_sui_age_rejects_wrong_number(self):
        self.change('corpus/shiji/052.json', lambda d: d['annotation']['age_assertions'][1].update(value=14))
        self.assertIn('來源年齡數值與原詞不符', v.validate(self.root))
    def test_sui_age_cannot_infer_birth_year(self):
        self.change('corpus/shiji/052.json', lambda d: d['annotation']['age_assertions'][2].update(birth_year=-39))
        self.assertIn('來源年齡不得推定計歲方式或出生年', v.validate(self.root))
    def test_sui_age_requires_literal_source_word(self):
        self.change('corpus/shiji/052.json', lambda d: d['annotation']['age_assertions'][1].update(source_term='十五歳'))
        self.assertIn('來源年齡引句不符', v.validate(self.root))
    def test_posthumous_naming_requires_death_word(self):
        self.change('corpus/shiji/053-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji053-016')['naming_basis'].update(death_term=''))
        self.assertIn('死後諡名缺少相符命名詞、死亡詞與起點證據', v.validate(self.root))
    def test_posthumous_naming_requires_naming_word(self):
        self.change('corpus/shiji/053-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji053-016')['naming_basis'].update(source_term='文終侯'))
        self.assertIn('死後諡名缺少相符命名詞、死亡詞與起點證據', v.validate(self.root))
    def test_posthumous_naming_binds_its_title(self):
        self.change('corpus/shiji/053-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji053-016').update(title='文成侯'))
        self.assertIn('死後諡名缺少相符命名詞、死亡詞與起點證據', v.validate(self.root))
    def test_posthumous_naming_cannot_be_living_grant(self):
        self.change('corpus/shiji/053-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji053-016').update(mode='grant'))
        self.assertIn('死後諡名缺少相符命名詞、死亡詞與起點證據', v.validate(self.root))
    def test_inherited_title_chain_rejects_wrong_root_title(self):
        self.change('corpus/shiji/054-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji054-052').update(title='別侯'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_inherited_title_chain_rejects_cycle(self):
        self.change('corpus/shiji/054-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji054-056')['inheritance'].update(predecessor_holding_id='th-shiji054-058'))
        self.assertIn('承爵判讀缺少相符的前任爵位、父子或原詞證據', v.validate(self.root))
    def test_duration_scope_rejects_other_person(self):
        self.change('corpus/shiji/054-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji054-019')['duration_scope'].update(holding_ids=['th-shiji054-019','th-shiji054-021']))
        self.assertIn('跨稱號任事年數缺少同人同類稱號與明示範圍', v.validate(self.root))
    def test_duration_scope_rejects_single_title(self):
        self.change('corpus/shiji/054-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji054-019')['duration_scope'].update(holding_ids=['th-shiji054-019']))
        self.assertIn('跨稱號任事年數缺少同人同類稱號與明示範圍', v.validate(self.root))
    def test_duration_scope_requires_reported_number(self):
        self.change('corpus/shiji/054-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji054-019').pop('reported_duration'))
        self.assertIn('跨稱號任事年數缺少同人同類稱號與明示範圍', v.validate(self.root))
    def test_source_age_rejects_wrong_number(self):
        self.change('corpus/shiji/111.json', lambda d: d['annotation']['age_assertions'][0].update(value=19))
        self.assertIn('來源年齡數值與原詞不符', v.validate(self.root))
    def test_chu_age_report_keeps_strict_open_lower_bound(self):
        def mutate(d):
            age = next(a for a in d['annotation']['age_assertions'] if a['id'] == 'age-jin076-xiaowu-over-ten')
            age['bounds']['lower_inclusive'] = True
        self.change('corpus/jinshu/076-wangbiaozhi.json', mutate)
        self.assertIn('直接報齡餘歲須保存開放下界及原詞，不得補限定詞或傳聞分組', v.validate(self.root))
    def test_chu_age_report_cannot_claim_exact_age(self):
        def mutate(d):
            age = next(a for a in d['annotation']['age_assertions'] if a['id'] == 'age-jin076-xiaowu-over-ten')
            age['value'] = 11
        self.change('corpus/jinshu/076-wangbiaozhi.json', mutate)
        self.assertIn('直接報齡餘歲須保存開放下界及原詞，不得補限定詞或傳聞分組', v.validate(self.root))
    def test_lifetime_age_cannot_be_exported_as_death_age(self):
        def mutate(d):
            ages = d['annotation']['age_assertions']
            first = next(a for a in ages if a['value'] == 20)
            first['age_context'] = next(a for a in ages if a['value'] == 73)['age_context']
        self.change('corpus/jinshu/076-wangbiaozhi.json', mutate)
        self.assertIn('報齡時點須區分生前與同人同段死亡事件，不得把生前年齡充享年', v.validate(self.root))
    def test_source_age_cannot_infer_birth_year(self):
        self.change('corpus/shiji/111.json', lambda d: d['annotation']['age_assertions'][0].update(birth_year=-139))
        self.assertIn('來源年齡不得推定計歲方式或出生年', v.validate(self.root))
    def test_dafu_hang_cannot_become_direct_grandfather(self):
        self.change('corpus/shiji/111-assertions.json', lambda d: next(a for a in d['assertions'] if a['predicate'] == 'kinship_generation').update(predicate='grandfather'))
        self.assertIn('大父行只記祖父輩，不得補直系祖父或親等', v.validate(self.root))
    def test_dafu_hang_cannot_gain_exact_distance(self):
        self.change('corpus/shiji/111-assertions.json', lambda d: next(a for a in d['assertions'] if a['predicate'] == 'kinship_generation')['qualifiers'].update(exact_distance=2))
        self.assertIn('大父行只記祖父輩，不得補直系祖父或親等', v.validate(self.root))
    def test_jiezi_keeps_maternal_generation(self):
        self.change('corpus/shiji/111-assertions.json', lambda d: next(a for a in d['assertions'] if a['predicate'] == 'maternal_uncle')['qualifiers'].update(lineage='paternal'))
        self.assertIn('甥舅關係須有姊子原詞、舅某或相鄰具名某之外甥錨點，保留母系世代與未名母親', v.validate(self.root))
    def test_title_month_rejects_number_mismatch(self):
        self.change('corpus/shiji/048-titles.json', lambda d: next(h for h in d['holdings'] if h.get('reported_duration', {}).get('unit') == 'title_month')['reported_duration'].update(value=7))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_title_month_rejects_year_unit(self):
        self.change('corpus/shiji/048-titles.json', lambda d: next(h for h in d['holdings'] if h.get('reported_duration', {}).get('unit') == 'title_month')['reported_duration'].update(unit='title_year', counting='unspecified_source_years'))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_title_month_rejects_regnal_counting(self):
        self.change('corpus/shiji/048-titles.json', lambda d: next(h for h in d['holdings'] if h.get('reported_duration', {}).get('unit') == 'title_month')['reported_duration'].update(counting='inclusive_regnal_years'))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_death_then_designation_rejects_wrong_title(self):
        self.change('corpus/shiji/061-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji061-006')['posthumous_basis'].update(grant_term='號為武王'))
        self.assertIn('追尊授號缺少相符原詞與起點證據', v.validate(self.root))
    def test_death_then_designation_rejects_missing_death(self):
        self.change('corpus/shiji/061-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji061-006')['posthumous_basis'].update(death_term='武王卒'))
        self.assertIn('追尊授號缺少相符原詞與起點證據', v.validate(self.root))
    def test_death_then_grant_rejects_wrong_death(self):
        self.change('corpus/shiji/060-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji060-034')['posthumous_basis'].update(death_term='閎死'))
        self.assertIn('追尊授號缺少相符原詞與起點證據', v.validate(self.root))
    def test_death_then_grant_rejects_changed_title(self):
        self.change('corpus/shiji/060-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji060-034').update(title='皇太后'))
        self.assertIn('追尊授號缺少相符原詞與起點證據', v.validate(self.root))
    def test_posthumous_grant_rejects_missing_quote(self):
        def mutate(d):
            h=next(h for h in d['holdings'] if h['mode']=='posthumous_grant')
            h.pop('posthumous_basis')
        self.change('corpus/shiji/049-titles.json', mutate)
        self.assertIn('追尊授號缺少相符原詞與起點證據', v.validate(self.root))
    def test_posthumous_grant_rejects_not_retrospective(self):
        def mutate(d):
            h=next(h for h in d['holdings'] if h['mode']=='posthumous_grant')
            h['posthumous_basis'].update(source_term='封為共侯')
        self.change('corpus/shiji/049-titles.json', mutate)
        self.assertIn('追尊授號缺少相符原詞與起點證據', v.validate(self.root))
    def test_posthumous_grant_rejects_living_grant(self):
        def mutate(d):
            h=next(h for h in d['holdings'] if h['mode']=='posthumous_grant')
            h.update(mode='grant')
        self.change('corpus/shiji/049-titles.json', mutate)
        self.assertIn('追尊授號缺少相符原詞與起點證據', v.validate(self.root))
    def test_reported_tenure_rejects_number_mismatch(self):
        self.change('corpus/shiji/110-titles.json', lambda d: next(h for h in d['holdings'] if 'reported_duration' in h)['reported_duration'].update(value=14))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_reported_tenure_rejects_partial_source_numeral(self):
        self.change('corpus/shiji/110-titles.json', lambda d: next(h for h in d['holdings'] if 'reported_duration' in h)['reported_duration'].update(value=3, source_number='三'))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_reported_tenure_requires_quote(self):
        self.change('corpus/shiji/110-titles.json', lambda d: next(h for h in d['holdings'] if 'reported_duration' in h)['reported_duration'].update(source_term='立十四年死'))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_reported_tenure_cannot_be_elapsed_calendar_years(self):
        self.change('corpus/shiji/110-titles.json', lambda d: next(h for h in d['holdings'] if 'reported_duration' in h)['reported_duration'].update(unit='calendar_year'))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_reported_tenure_rejects_elapsed_counting(self):
        self.change('corpus/shiji/110-titles.json', lambda d: next(h for h in d['holdings'] if 'reported_duration' in h)['reported_duration'].update(counting='elapsed_calendar_years'))
        self.assertIn('稱號來源在位年數或原詞證據無效', v.validate(self.root))
    def test_stepmother_requires_received_term(self):
        self.change('corpus/shiji/110-assertions.json', lambda d: next(a for a in d['assertions'] if a['predicate'] == 'stepmother')['qualifiers'].update(source_term='母'))
        self.assertIn('繼母或後母關係須有相符原詞證據', v.validate(self.root))
    def test_accession_requires_matching_start_event(self):
        self.change('corpus/shiji/110-titles.json', lambda d: next(h for h in d['holdings'] if h['mode'] == 'accession')['effective_period']['start'].update(event_type='grant'))
        self.assertIn('稱號起點與事件種類不符', v.validate(self.root))
    def test_posthumous_child_requires_received_term(self):
        self.change('corpus/shiji/109-assertions.json', lambda d: next(a for a in d['assertions'] if a['id'] == 'a-shiji109-007')['qualifiers'].update(source_term='當戸子陵'))
        self.assertIn('遺腹子欄位須有父親與原詞證據', v.validate(self.root))
    def test_unspecified_kinship_cannot_gain_agnatic_structure(self):
        self.change('corpus/shiji/109-assertions.json', lambda d: next(a for a in d['assertions'] if a['id'] == 'a-shiji109-010')['qualifiers'].update(kinship_structure={'lineage': 'paternal'}))
        self.assertIn('未定親屬不得補具體親等', v.validate(self.root))
    def test_following_life_date_requires_explicit_date_paragraph(self):
        self.change('corpus/shiji/110-life-events.json', lambda d: next(e for e in d['events'] if e['id'] == 'le-shiji110-wuwei')['date_context'].pop('date_paragraph_id'))
        self.assertIn('生卒紀年承接須有連續同篇段落與明示日期段', v.validate(self.root))
    def test_following_life_date_paragraph_must_contain_expression(self):
        self.change('corpus/shiji/110-life-events.json', lambda d: next(e for e in d['events'] if e['id'] == 'le-shiji110-wuwei')['date_context'].update(date_paragraph_id='c-shiji-110-xiongnu:p048'))
        self.assertIn('生卒紀年承接須有連續同篇段落與明示日期段', v.validate(self.root))
    def test_following_life_date_paragraph_must_be_in_sequence(self):
        self.change('corpus/shiji/110-life-events.json', lambda d: next(e for e in d['events'] if e['id'] == 'le-shiji110-wuwei')['date_context'].update(date_paragraph_id='c-shiji-110-xiongnu:p043'))
        self.assertIn('生卒紀年承接須有連續同篇段落與明示日期段', v.validate(self.root))
    def test_repeated_death_date_requires_primary_event_anchor(self):
        self.change('corpus/shiji/052-life-events.json', lambda d: d['events'][0]['date_context'].update(date_paragraph_id='c-shiji-052-qidaohui:p012'))
        self.assertIn('同一生卒事件回述須以首筆明示事件引句作紀年錨點', v.validate(self.root))
    def test_repeated_death_date_requires_exact_attestation_list(self):
        self.change('corpus/shiji/052-life-events.json', lambda d: d['events'][0]['date_context']['paragraph_ids'].pop())
        self.assertIn('同一生卒事件回述須以首筆明示事件引句作紀年錨點', v.validate(self.root))
    def test_repeated_death_date_requires_event_source_term(self):
        self.change('corpus/shiji/052-life-events.json', lambda d: d['events'][0].update(source_term='未見原文的死亡句'))
        self.assertIn('同一生卒事件回述須以首筆明示事件引句作紀年錨點', v.validate(self.root))
    def test_life_date_context_cannot_skip_a_paragraph(self):
        self.change('corpus/shiji/109-life-events.json', lambda d: next(e for e in d['events'] if e['id'] == 'le-shiji109-liguang')['date_context'].update(paragraph_ids=['c-shiji-109-liguang:p012', 'c-shiji-109-liguang:p014']))
        self.assertIn('生卒紀年承接須有連續同篇段落與明示日期段', v.validate(self.root))
    def test_life_date_context_cannot_be_implicit(self):
        self.change('corpus/shiji/109-life-events.json', lambda d: next(e for e in d['events'] if e['id'] == 'le-shiji109-liguang').pop('date_context'))
        self.assertIn('生卒日期未見於事件引句', v.validate(self.root))
    def test_office_jurisdiction_requires_source_quote(self):
        self.change('corpus/shiji/109-titles.json', lambda d: next(h for h in d['holdings'] if h['id'] == 'th-shiji109-020')['jurisdictions'][0].update(source_name='未見原文的郡'))
        self.assertIn('稱號所屬原地名缺少引句或未保留未知定位', v.validate(self.root))
    def test_office_jurisdiction_cannot_invent_modern_location(self):
        self.change('corpus/shiji/109-titles.json', lambda d: next(h for h in d['holdings'] if h['id'] == 'th-shiji109-020')['jurisdictions'][0].update(modern_identification='今地'))
        self.assertIn('稱號所屬原地名缺少引句或未保留未知定位', v.validate(self.root))
    def test_unresolved_case_requires_local_anchor(self):
        self.change('corpus/shiji/108.json', lambda d: d['annotation']['unresolved_identity_cases'][0].update(paragraph_ids=['c-shiji-107-weiqi:p002', 'c-shiji-107-weiqi:p006']))
        self.assertIn('未決身份段落引用無效', v.validate(self.root))
    def test_unresolved_case_rejects_missing_foreign_reference(self):
        self.change('corpus/shiji/108.json', lambda d: d['annotation']['unresolved_identity_cases'][0]['paragraph_ids'].append('c-shiji-107-weiqi:p999'))
        self.assertIn('未決身份段落引用無效', v.validate(self.root))
    def test_unresolved_case_requires_candidate_support(self):
        self.change('corpus/shiji/108.json', lambda d: d['annotation']['unresolved_identity_cases'][0].update(paragraph_ids=['c-shiji-108-han:p006']))
        self.assertIn('未決身份缺少各候選人物的段落證據', v.validate(self.root))
    def test_life_event_cannot_use_other_person_anchor(self):
        self.change('corpus/shiji/108-life-events.json', lambda d: d['events'][1]['evidence'][0].update(person_mention_id='c-shiji-108-han:m011-0000'))
        self.assertIn('生卒事件人物錨點不符', v.validate(self.root))
    def test_life_event_cannot_invent_unknown_date(self):
        self.change('corpus/shiji/108-life-events.json', lambda d: d['events'][1].update(normalized_date=d['events'][0]['normalized_date']))
        self.assertIn('生卒數字紀年缺原日期表述', v.validate(self.root))
    def test_life_event_requires_quoted_date(self):
        self.change('corpus/shiji/108-life-events.json', lambda d: d['events'][0].update(date_expression='元朔三年'))
        self.assertIn('生卒日期未見於事件引句', v.validate(self.root))
    def test_registry_cannot_omit_a_received_person_mention(self):
        def mutate(d):
            person = next(p for p in d['persons'] if len(p['evidence']) > 2)
            mid = person['evidence'].pop()['mention_id']
            for alias in person['aliases']:
                alias['mention_ids'] = [m for m in alias['mention_ids'] if m != mid]
            person['aliases'] = [a for a in person['aliases'] if a['mention_ids']]
        self.change('registry/persons.json', mutate)
        self.assertTrue(any('雙向索引不完整' in e for e in v.validate(self.root)))

    def test_unknown_person_rejected(self):
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0]['mentions'][0].update(person_id='missing'))
        self.assertTrue(any('未知人物' in e for e in v.validate(self.root)))
    def test_changed_offsets_rejected(self):
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0]['mentions'][0].update(start=1))
        self.assertTrue(any('位置不符' in e for e in v.validate(self.root)))
    def test_punctuation_only_person_anchor_rejected(self):
        def mutate(d):
            paragraph = next(p for p in d['paragraphs'] if p['id'].endswith(':p018'))
            mention = next(m for m in paragraph['mentions'] if m['id'].endswith(':m018-0183'))
            self.assertEqual(paragraph['text'][183:184], '，')
            mention.update(start=183, end=184, surface='，')
        self.change('corpus/shiji/086.json', mutate)
        self.assertIn('人物提及不得僅為標點或空白', v.validate(self.root))
    def test_wrong_book_rejected(self):
        self.change('corpus/shiji/001.json',lambda d:d.update(book_id='b-shiji-002'))
        self.assertTrue(any('歸屬不符' in e for e in v.validate(self.root)))
    def test_xml_text_drift_rejected(self):
        p=self.root/'corpus/shiji/001.xml';p.write_text(p.read_text().replace('生而神靈','改竄正文',1))
        self.assertTrue(any('正文還原' in e for e in v.validate(self.root)))
    def test_unresolved_does_not_claim_person(self):
        def mutate(d):next(m for p in d['paragraphs'] for m in p['mentions'] if m['kind']=='unresolved').update(person_id='8jz_o3s_obt')
        self.change('corpus/shiji/001.json',mutate)
        self.assertTrue(any('不得暗選' in e for e in v.validate(self.root)))
    def test_cross_chapter_identity_needs_both_sources(self):
        def mutate(d):
            decision=next(v for v in d['decisions'] if v['scope']=='cross_chapter')
            decision['evidence']=decision['evidence'][:1]
        self.change('corpus/shiji/002-identities.json',mutate)
        self.assertTrue(any('各篇證據' in e for e in v.validate(self.root)))
    def test_relationship_requires_exact_source(self):
        def mutate(d):d['assertions'][0]['evidence'][0]['source_id']='s-shiji-001-wudi'
        self.change('corpus/shiji/002-assertions.json',mutate)
        self.assertTrue(any('來源 ID 不符' in e for e in v.validate(self.root)))
    def test_relationship_unknown_person_rejected(self):
        def mutate(d):d['assertions'][0]['object_person_id']='missing'
        self.change('corpus/shiji/002-assertions.json',mutate)
        self.assertTrue(any('引用未知人物' in e for e in v.validate(self.root)))
    def test_xia_context_does_not_merge_officials_across_generations(self):
        chapter=json.loads((self.root/'corpus/shiji/002.json').read_text())
        paragraph=next(p for p in chapter['paragraphs'] if '羲、和湎淫' in p['text'])
        mention=next(m for m in paragraph['mentions'] if m['surface']=='羲、和')
        self.assertIsNone(mention['person_id'])
        start=paragraph['text'].index('作胤征')+1
        self.assertFalse(any(m['kind']=='person' and m['start']==start for m in paragraph['mentions']))

    def test_yin_same_title_keeps_distinct_people(self):
        d=json.loads((self.root/'corpus/shiji/003.json').read_text())
        def people_at(n,surface):
            return {m['person_id'] for m in d['paragraphs'][n-1]['mentions'] if m['surface']==surface}
        self.assertTrue(people_at(7,'武王').isdisjoint(people_at(30,'武王')))
        self.assertTrue(people_at(11,'太丁').isdisjoint(people_at(26,'帝太丁')))
        self.assertEqual(len(people_at(7,'武王')),1)
        self.assertEqual(len(people_at(30,'武王')),1)
    def test_distinction_rejects_same_person_twice(self):
        def mutate(d):
            ids=d['distinctions'][0]['person_ids'];ids[1]=ids[0]
        self.change('corpus/shiji/003-distinctions.json',mutate)
        self.assertTrue(any('區分端點無效' in e for e in v.validate(self.root)))
    def test_distinction_needs_each_person_evidence(self):
        self.change('corpus/shiji/003-distinctions.json',lambda d:d['distinctions'][0].update(evidence=d['distinctions'][0]['evidence'][:1]))
        self.assertTrue(any('各端點證據' in e for e in v.validate(self.root)))
    def test_yin_book_title_is_not_person_occurrence(self):
        d=json.loads((self.root/'corpus/shiji/003.json').read_text())
        for n,term in [(4,'作湯征'),(5,'作女鳩女房'),(17,'仲丁書'),(20,'作盤庚'),(23,'高宗肜日')]:
            p=d['paragraphs'][n-1];start=p['text'].index(term);end=start+len(term)
            self.assertFalse(any(m['kind']=='person' and start<=m['start']<end for m in p['mentions']))
        self.assertTrue(any(m['kind']=='person' and m['start']==0 for m in d['paragraphs'][3]['mentions']))
    def test_yin_verb_yi_is_not_an_unrelated_person(self):
        d=json.loads((self.root/'corpus/shiji/003.json').read_text())
        for n,term in [(28,'益收'),(28,'益廣'),(29,'益疏')]:
            p=d['paragraphs'][n-1];start=p['text'].index(term)
            self.assertFalse(any(m['kind']=='person' and m['start']==start for m in p['mentions']))

    def test_partial_chapter_cannot_claim_first_pass(self):
        def mutate(d):
            d['annotation']['status'] = 'named_mentions_first_pass'
            d['paragraphs'][-1].update(annotation_status='pending', mentions=[])
        self.change('corpus/shiji/004.json', mutate)
        self.assertTrue(any('不得宣稱首輪完成' in e for e in v.validate(self.root)))
    def test_partial_progress_cannot_skip_pending_paragraphs(self):
        def mutate(d):
            next(b for b in d['books'] if b['book_id']=='b-shiji-004')['person_status']='named_mentions_first_pass'
        self.change('corpus/shiji/004.json',lambda d:d['paragraphs'][-1].update(annotation_status='pending',mentions=[]))
        self.change('corpus/progress.json',mutate)
        self.assertTrue(any('有待標註段落' in e for e in v.validate(self.root)))
    def test_zhou_qi_verb_is_not_a_person(self):
        d=json.loads((self.root/'corpus/shiji/004.json').read_text())
        p=d['paragraphs'][0]
        for term in ('棄之隘巷','棄渠中','初欲棄之'):
            start=p['text'].index(term)+(2 if term=='初欲棄之' else 0)
            self.assertFalse(any(m['kind']=='person' and m['start']==start for m in p['mentions']))
    def test_zhou_boyi_is_distinct_from_shun_official(self):
        d=json.loads((self.root/'corpus/shiji/004.json').read_text())
        m=next(m for m in d['paragraphs'][6]['mentions'] if m['surface']=='伯夷')
        self.assertNotEqual(m['person_id'],'uxv_pg9_8rm')

    def test_unresolved_identity_rejects_unknown_candidate(self):
        def mutate(d):d['annotation']['unresolved_identity_cases'][0]['candidate_person_ids'][0]='missing'
        self.change('corpus/shiji/004.json',mutate)
        self.assertTrue(any('候選人物無效' in e for e in v.validate(self.root)))
    def test_unresolved_identity_requires_candidate_evidence(self):
        def mutate(d):d['annotation']['unresolved_identity_cases'][0]['paragraph_ids']=['c-shiji-004-zhou:p083']
        self.change('corpus/shiji/004.json',mutate)
        self.assertTrue(any('各候選人物的段落證據' in e for e in v.validate(self.root)))
    def test_zhou_succession_preserves_explicit_generations(self):
        d=json.loads((self.root/'corpus/shiji/004-assertions.json').read_text())
        claims={(a['subject_person_id'],a['predicate'],a['object_person_id']) for a in d['assertions']}
        self.assertIn(('ttx_okj_hbd','father','qk9_ejk_fnc'),claims)
        self.assertIn(('ttx_okj_hbd','grandfather','f3g_x6y_1iy'),claims)
        self.assertNotIn(('ttx_okj_hbd','father','f3g_x6y_1iy'),claims)

    def test_qin_sisters_keep_literal_kinship_and_anonymity(self):
        c=json.loads((self.root/'corpus/shiji/005.json').read_text())
        a=json.loads((self.root/'corpus/shiji/005-assertions.json').read_text())
        sister=next(m for m in c['paragraphs'][20]['mentions'] if m['surface']=='姊')
        claim=next(a for a in a['assertions'] if a['subject_person_id']==sister['person_id'] and a['predicate']=='sister')
        self.assertEqual(claim['qualifiers']['source_term'],'姊')
        self.assertIn('晉太子申生姊也',claim['evidence'][0]['quote'])
        p=next(p for p in json.loads((self.root/'registry/persons.json').read_text())['persons'] if p['id']==sister['person_id'])
        self.assertFalse(any(a['surface']=='穆姬' for a in p['aliases']))

    def test_qin_qi_daogong_resolved_per_occurrence(self):
        c=json.loads((self.root/'corpus/shiji/005.json').read_text())
        p=c['paragraphs'][45]
        def at(term):
            start=p['text'].index(term)+term.index('悼公')
            return next(m['person_id'] for m in p['mentions'] if m['start']==start)
        self.assertEqual(at('悼公二年'),at('秦悼公'))
        self.assertEqual(at('是為悼公'),at('齊人弒悼公'))
        self.assertNotEqual(at('悼公二年'),at('是為悼公'))
    def test_shangjun_title_and_work_pointer_are_distinct(self):
        c=json.loads((self.root/'corpus/shiji/005.json').read_text())
        p=c['paragraphs'][57];start=p['text'].index('商君語')
        self.assertFalse(any(m['kind']=='person' and start<=m['start']<start+3 for m in p['mentions']))
        p=c['paragraphs'][60]
        title=next(m for m in p['mentions'] if m['surface']=='商君')
        name=next(m for m in p['mentions'] if m['surface']=='衛鞅')
        self.assertEqual(title['person_id'],name['person_id'])
        self.assertEqual(title['kind'],'person')

    def test_appended_note_layer_survives_xml(self):
        c=json.loads((self.root/'corpus/shiji/006.json').read_text())
        self.assertEqual(next(p for p in c['paragraphs'] if p['id']=='c-shiji-006-shihuang:p106')['text_layer'],'received_chapter')
        self.assertEqual(next(p for p in c['paragraphs'] if p['id']=='c-shiji-006-shihuang:p107')['text_layer'],'witness_appended_bangu_note')
        p=self.root/'corpus/shiji/006.xml'
        p.write_text(p.read_text().replace('text-layer="witness_appended_bangu_note"','text-layer="received_chapter"',1))
        self.assertTrue(any('文字層次不符' in e for e in v.validate(self.root)))

    def test_appended_edict_layer_must_match_xml(self):
        # Synthetic layer change checks that an edict cannot silently become body text.
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0].update(text_layer='witness_appended_edict'))
        xml=self.root/'corpus/shiji/001.xml'
        xml.write_text(xml.read_text().replace('<p id="c-shiji-001-wudi:p001"','<p text-layer="witness_appended_edict" id="c-shiji-001-wudi:p001"',1))
        self.assertEqual(v.validate(self.root),[])
        xml.write_text(xml.read_text().replace('text-layer="witness_appended_edict"','text-layer="received_chapter"',1))
        self.assertTrue(any('文字層次不符' in e for e in v.validate(self.root)))

    def test_suoyin_layer_mismatch_and_unknown_layer_rejected(self):
        # Synthetic edits verify that a commentary cannot silently become body text.
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0].update(text_layer='witness_appended_suoyin_zan'))
        xml=self.root/'corpus/shiji/001.xml'
        xml.write_text(xml.read_text().replace('<p id="c-shiji-001-wudi:p001"','<p text-layer="witness_appended_suoyin_zan" id="c-shiji-001-wudi:p001"',1))
        self.assertEqual(v.validate(self.root),[])
        xml.write_text(xml.read_text().replace('text-layer="witness_appended_suoyin_zan"','text-layer="received_chapter"',1))
        self.assertTrue(any('文字層次不符' in e for e in v.validate(self.root)))
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0].update(text_layer='synthetic_unknown_layer'))
        self.assertTrue(any('文字層次無效' in e for e in v.validate(self.root)))

    def test_chu_note_layer_must_match_xml(self):
        # Synthetic attribution checks the layer boundary, not historical authorship.
        self.change('corpus/shiji/001.json',lambda d:d['paragraphs'][0].update(text_layer='witness_appended_chu_note'))
        xml=self.root/'corpus/shiji/001.xml'
        xml.write_text(xml.read_text().replace('<p id="c-shiji-001-wudi:p001"','<p text-layer="witness_appended_chu_note" id="c-shiji-001-wudi:p001"',1))
        self.assertEqual(v.validate(self.root),[])
        xml.write_text(xml.read_text().replace('text-layer="witness_appended_chu_note"','text-layer="received_chapter"',1))
        self.assertTrue(any('文字層次不符' in e for e in v.validate(self.root)))

    def test_shihuang_dd_quotes_preserve_order_and_xml_text(self):
        c=json.loads((self.root/'corpus/shiji/006.json').read_text())
        ids=[p['id'] for p in c['paragraphs']]
        self.assertEqual(sum(p.get('source_block_kind')=='witness_dd' for p in c['paragraphs']),16)
        self.assertLess(ids.index('c-shiji-006-shihuang:p029'),ids.index('c-shiji-006-shihuang:p029:block01'))
        self.assertLess(ids.index('c-shiji-006-shihuang:p029:block01'),ids.index('c-shiji-006-shihuang:p030'))
        p=next(p for p in c['paragraphs'] if p['id']=='c-shiji-006-shihuang:p029:block01')
        self.assertTrue(p['text'].startswith('維二十八年，皇帝作始'))
        self.assertEqual(v.validate(self.root),[])

    def test_shihuang_conflicting_genealogy_claims_are_preserved(self):
        c=json.loads((self.root/'corpus/shiji/006.json').read_text())
        by={p['id']:p for p in c['paragraphs']}
        p=by['c-shiji-006-shihuang:p085']
        person=next(m['person_id'] for m in p['mentions'] if m['surface']=='靈公')
        claims=json.loads((self.root/'corpus/shiji/006-assertions.json').read_text())['assertions']
        selected=[a for a in claims if a['subject_person_id']==person and a['predicate']=='father' and a['evidence'][0]['paragraph_id'] in ('c-shiji-006-shihuang:p085','c-shiji-006-shihuang:p086')]
        self.assertEqual(len(selected),2)
        self.assertEqual(len({a['object_person_id'] for a in selected}),2)
        self.assertTrue(any('生靈公' in a['evidence'][0]['quote'] for a in selected))
        self.assertTrue(any('昭子子也' in a['evidence'][0]['quote'] for a in selected))

    def test_epithet_context_is_not_a_name(self):
        d=json.loads((self.root/'corpus/shiji/001.json').read_text())
        for p in d['paragraphs']:
            for term in ('軒轅之丘','象以典刑','夔夔唯謹','九男皆益篤'):
                if term in p['text']:
                    start=p['text'].index(term)
                    for m in p['mentions']:
                        self.assertFalse(m['kind']=='person' and start<=m['start']<start+len(term))
    def test_xiangyu_paternal_uncle_does_not_create_father(self):
        data=json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())
        relations=[a for a in data['assertions'] if a['subject_person_id']=='ob7_g6i_7pp']
        people=json.loads((self.root/'registry/persons.json').read_text())['persons']
        bo=next(p['id'] for p in people if p['label']=='項伯')
        self.assertEqual({(a['predicate'],a['object_person_id']) for a in relations},{('paternal_uncle','5xt_rg8_7zs_A'),('paternal_uncle',bo)})
        self.assertEqual(relations[0]['qualifiers']['source_term'],'季父')
    def test_huaiwang_grandson_phrase_keeps_two_generations(self):
        chapter=json.loads((self.root/'corpus/shiji/007.json').read_text())
        p=chapter['paragraphs'][5]
        grandfather=p['text'].index('乃求楚懷王')+2
        grandson=p['text'].index('立以為楚懷王')+3
        mentions={m['start']:m for m in p['mentions']}
        self.assertEqual(mentions[grandfather]['person_id'],'c2w_s7g_en0')
        self.assertNotEqual(mentions[grandfather]['person_id'],mentions[grandson]['person_id'])
        relation=next(a for a in json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())['assertions'] if a['predicate']=='grandfather')
        self.assertEqual(relation['subject_person_id'],mentions[grandson]['person_id'])
        self.assertEqual(relation['object_person_id'],mentions[grandfather]['person_id'])
    def test_kuaiji_governor_succession_not_same_title_identity(self):
        p=json.loads((self.root/'corpus/shiji/007.json').read_text())['paragraphs'][2]
        governor=p['text'].index('會稽守通')
        successor=p['text'].rindex('會稽守')
        mentions={m['start']:m for m in p['mentions']}
        self.assertEqual(mentions[governor]['kind'],'person')
        self.assertEqual(mentions[successor]['kind'],'unresolved')
        self.assertIsNone(mentions[successor]['person_id'])

    def test_equivalence_keeps_published_dangyang_mentions(self):
        c=json.loads((self.root/'corpus/shiji/007.json').read_text())
        old=[m for p in c['paragraphs'][:12] for m in p['mentions'] if m['surface']=='當陽君']
        self.assertTrue(old)
        self.assertEqual({m['person_id'] for m in old},{'zxd_afr_2xg'})
        decision=json.loads((self.root/'corpus/shiji/007-equivalences.json').read_text())['decisions'][0]
        self.assertEqual(set(decision['person_ids']),{'zxd_afr_2xg'})
        self.assertEqual(decision['canonical_person_id'],'zxd_afr_2xg')
        self.assertEqual(v.validate(self.root),[])
    def test_materialized_flag_cannot_accept_multiple_person_ids(self):
        self.change('corpus/shiji/007-equivalences.json',
                    lambda d: d['decisions'][0].update(identity_materialized=True, person_ids=['zxd_afr_2xg', 'ao3_0fy_d45_AAA']))
        self.assertIn('同指決定端點無效或重複', v.validate(self.root))

    def test_equivalence_rejects_unrelated_quote(self):
        def mutate(d):d['decisions'][0]['evidence'][0]['quote']='故立布為九江王'
        self.change('corpus/shiji/007-equivalences.json',mutate)
        self.assertTrue(any('同指決定提及不在精確引句' in e for e in v.validate(self.root)))
    def test_equivalence_rejects_invalid_representative(self):
        self.change('corpus/shiji/007-equivalences.json',lambda d:d['decisions'][0].update(canonical_person_id='ao3_0fy_d45_AAA'))
        self.assertTrue(any('代表不在端點' in e for e in v.validate(self.root)))
    def test_equivalence_rejects_canonical_cycle(self):
        def mutate(d):
            d['decisions'][0].update(person_ids=['zxd_afr_2xg', 'ao3_0fy_d45_AAA'], identity_materialized=False);other=json.loads(json.dumps(d['decisions'][0]));other['id']='synthetic-cycle';other['canonical_person_id']='ao3_0fy_d45_AAA';d['decisions'].append(other)
        self.change('corpus/shiji/007-equivalences.json',mutate)
        self.assertTrue(any('同指決定代表循環' in e for e in v.validate(self.root)))
    def test_xiangyu_verb_ji_and_ritual_names_do_not_create_kin(self):
        c=json.loads((self.root/'corpus/shiji/007.json').read_text())
        p=c['paragraphs'][16];a=p['text'].index('籍吏民')
        self.assertFalse(any(m['kind']=='person' and m['start']==a for m in p['mentions']))
        claims=json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())['assertions']
        self.assertFalse(any(a['subject_person_id']=='ob7_g6i_7pp' and a['predicate'] in ('ancestor','father') for a in claims))
        self.assertFalse(any(a['object_person_id']=='ddb_l4j_4j2' for a in claims))
    def test_title_grant_is_separate_from_retrospective_attestation(self):
        holdings=json.loads((self.root/'corpus/shiji/007-titles.json').read_text())['holdings']
        h=next(h for h in holdings if h['title']=='赤泉侯')
        self.assertEqual(h['effective_period']['start']['evidence'][0]['paragraph_id'],'c-shiji-007-xiangyu:p042')
        self.assertTrue(any(a['paragraph_id']=='c-shiji-007-xiangyu:p041' and a['usage']=='retrospective' for a in h['attestations']))
        self.assertEqual(h['effective_period']['end']['status'],'unknown')
        lu=next(h for h in holdings if h['title']=='魯公')
        self.assertTrue(any(a['usage']=='posthumous_usage' for a in lu['attestations']))
        self.assertEqual(lu['effective_period']['end']['status'],'unknown')
    def test_title_period_rejects_unsourced_date(self):
        self.change('corpus/shiji/007-titles.json',lambda d:d['holdings'][0]['effective_period']['start'].update(date_expression='合成日期'))
        self.assertTrue(any('稱號日期表述不在端點證據' in e for e in v.validate(self.root)))
    def test_title_period_rejects_death_as_automatic_end(self):
        def mutate(d):
            h=d['holdings'][0];h['effective_period']['end']={'status':'source_event','event_type':'death','date_expression':None,'evidence':h['evidence']}
        self.change('corpus/shiji/007-titles.json',mutate)
        self.assertTrue(any('死亡或首次用稱不得自動替代起訖' in e for e in v.validate(self.root)))
    def test_title_occurrence_rejects_wrong_person(self):
        def mutate(d):d['holdings'][0]['attestations'][0]['person_mention_id']='c-shiji-007-xiangyu:m001-0000'
        self.change('corpus/shiji/007-titles.json',mutate)
        self.assertTrue(any('稱號用稱人物提及不符' in e for e in v.validate(self.root)))
    def test_sister_assertion_follows_subject_orientation(self):
        people=json.loads((self.root/'registry/persons.json').read_text())['persons']
        ids={p['label']:p['id'] for p in people}
        claims=json.loads((self.root/'corpus/shiji/007-assertions.json').read_text())['assertions']
        a=next(a for a in claims if a['qualifiers']['source_term']=='兄')
        self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),(ids['呂后'],'sister',ids['周呂侯（呂后兄）']))

    def test_unknown_title_endpoint_cannot_hide_normalized_year(self):
        self.change('corpus/shiji/007-titles.json',lambda d:d['holdings'][0]['effective_period']['end'].update(year=207))
        self.assertTrue(any('不能暗補正規化日期' in e for e in v.validate(self.root)))

    def test_gaozu_hanxin_ambiguity_is_preserved(self):
        chapter=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=chapter['paragraphs'][29]
        bare=next(m for m in p['mentions'] if m['surface']=='韓信')
        self.assertIsNone(bare['person_id'])
        named=next(m for m in p['mentions'] if m['surface']=='韓太尉信')
        adviser=next(m for m in chapter['paragraphs'][26]['mentions'] if m['surface']=='韓信')
        self.assertNotEqual(named['person_id'],adviser['person_id'])
        case=chapter['annotation']['unresolved_identity_cases'][0]
        self.assertEqual(set(case['candidate_person_ids']),{named['person_id'],adviser['person_id']})

    def test_gaozu_conditional_and_impersonated_titles_are_unresolved(self):
        chapter=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=chapter['paragraphs'][21]
        mentions=[m for m in p['mentions'] if m['surface']=='秦王']
        self.assertTrue(all(m['person_id'] is not None for m in mentions[:-1]))
        self.assertIsNone(mentions[-1]['person_id'])
        p=chapter['paragraphs'][39]
        a=p['text'].index('詐為漢王')+2
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))
        self.assertTrue(any(m['kind']=='unresolved' and m['start']<=a<m['end'] for m in p['mentions']))

    def test_gaozu_qi_king_in_execution_is_tian_guang(self):
        c=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=c['paragraphs'][43]
        named=next(m for m in p['mentions'] if m['surface']=='田廣')
        a=p['text'].index('齊王烹')
        king=next(m for m in p['mentions'] if m['start']==a)
        han=next(m for m in p['mentions'] if m['surface']=='韓信')
        self.assertEqual(king['person_id'],named['person_id'])
        self.assertNotEqual(king['person_id'],han['person_id'])

    def test_gaozu_successor_emperor_and_nonpersonal_words(self):
        c=json.loads((self.root/'corpus/shiji/008.json').read_text())
        p=c['paragraphs'][87]
        successor=next(m for m in p['mentions'] if m['surface']=='孝惠帝')
        emperor=next(m for m in p['mentions'] if m['surface']=='皇帝')
        self.assertEqual(successor['person_id'],emperor['person_id'])
        for n,word in [(60,'通侯籍'),(73,'甚有信'),(88,'上尊號')]:
            p=c['paragraphs'][n-1];a=p['text'].index(word)
            pos=a+2 if n in (60,73) else a
            self.assertFalse(any(m['person_id'] and m['start']<=pos<m['end'] for m in p['mentions']))

    def test_gaozu_title_deposition_requires_explicit_evidence(self):
        h=json.loads((self.root/'corpus/shiji/008-titles.json').read_text())['holdings']
        ends=[x['effective_period']['end'] for x in h if x['effective_period']['end']['status']=='source_event']
        self.assertEqual(len(ends),3)
        self.assertTrue(all(x['event_type']=='deposition' and '廢' in x['evidence'][0]['quote'] for x in ends))
        father=next(x for x in h if x['title']=='太上皇')
        self.assertEqual(father['effective_period']['end']['status'],'unknown')

    def test_lvhou_titles_do_not_merge_mother_and_daughter(self):
        c=json.loads((self.root/'corpus/shiji/009.json').read_text())
        p=c['paragraphs'][0]
        mother=next(m for m in p['mentions'] if m['surface']=='呂太后')
        daughter=next(m for m in p['mentions'] if m['surface']=='魯元太后')
        self.assertNotEqual(mother['person_id'],daughter['person_id'])
        queen=next(m for m in c['paragraphs'][4]['mentions'] if m['surface']=='王太后')
        self.assertEqual(queen['person_id'],daughter['person_id'])

    def test_lvhou_zhao_king_changes_after_ruyi_death(self):
        c=json.loads((self.root/'corpus/shiji/009.json').read_text())
        p=c['paragraphs'][3]
        king=next(m for m in p['mentions'] if m['start']==p['text'].index('友為趙王')+2)
        friend=next(m for m in p['mentions'] if m['surface']=='友')
        previous=next(m for m in p['mentions'] if m['surface']=='趙王')
        self.assertEqual(king['person_id'],friend['person_id'])
        self.assertNotEqual(king['person_id'],previous['person_id'])

    def test_lvhou_bo_family_queen_is_not_empress_lv(self):
        c=json.loads((self.root/'corpus/shiji/009.json').read_text())
        p=c['paragraphs'][29];a=p['text'].index('太后家薄氏')
        queen=next(m for m in p['mentions'] if m['start']==a)
        bo=next(m for m in c['paragraphs'][2]['mentions'] if m['surface']=='薄夫人')
        lv=next(m for m in c['paragraphs'][0]['mentions'] if m['surface']=='呂太后')
        self.assertEqual(queen['person_id'],bo['person_id'])
        self.assertNotEqual(queen['person_id'],lv['person_id'])
        p=c['paragraphs'][21];a=p['text'].index('語在齊王語')+2
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))

    def test_cross_chapter_equivalence_requires_every_declared_chapter(self):
        self.change('corpus/shiji/010-equivalences.json',lambda d:d['decisions'][0]['evidence'].pop(0))
        self.assertTrue(any('同指決定缺少各篇證據' in e for e in v.validate(self.root)))

    def test_cross_chapter_equivalence_cannot_hide_as_single_chapter(self):
        self.change('corpus/shiji/010-equivalences.json',lambda d:d['decisions'][0].update(scope='same_chapter'))
        self.assertTrue(any('同指決定範圍與篇數不符' in e for e in v.validate(self.root)))

    def test_wendi_successor_and_other_word_are_separate(self):
        c=json.loads((self.root/'corpus/shiji/010.json').read_text())
        previous=next(m for m in c['paragraphs'][37]['mentions'] if m['surface']=='孝文皇帝')
        successor=next(m for m in c['paragraphs'][38]['mentions'] if m['surface']=='皇帝')
        self.assertNotEqual(previous['person_id'],successor['person_id'])
        p=c['paragraphs'][36];a=p['text'].index('佗不在令中')
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))
        p=c['paragraphs'][29];a=p['text'].index('古者天子')+2
        self.assertFalse(any(m['person_id'] and m['start']<=a<m['end'] for m in p['mentions']))

    def test_jingdi_same_given_name_sheng_stays_separate(self):
        c=json.loads((self.root/'corpus/shiji/011.json').read_text())
        son=next(m for m in c['paragraphs'][3]['mentions'] if m['surface']=='子勝')
        uncle=next(m for m in c['paragraphs'][16]['mentions'] if m['surface']=='弟勝')
        self.assertNotEqual(son['person_id'],uncle['person_id'])

    def test_jingdi_king_mother_is_not_king(self):
        c=json.loads((self.root/'corpus/shiji/011.json').read_text())
        p=c['paragraphs'][7]
        mother=next(m for m in p['mentions'] if m['surface']=='膠東王太后')
        son=next(m for m in p['mentions'] if m['surface']=='膠東王')
        self.assertNotEqual(mother['person_id'],son['person_id'])
        titles=json.loads((self.root/'corpus/shiji/011-titles.json').read_text())['holdings']
        queen=next(h for h in titles if h['title']=='皇后')
        self.assertEqual(queen['person_id'],mother['person_id'])


    def test_adjacent_relation_requires_explicit_context(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            del a['context']
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('端點未見' in e for e in v.validate(self.root)))

    def test_adjacent_relation_rejects_reversed_evidence(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            a['evidence'].reverse()
            a['context']['paragraph_ids'].reverse()
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('相鄰兩段' in e for e in v.validate(self.root)))

    def test_adjacent_relation_requires_endpoint_in_quote(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            a['evidence'][0]['quote']='好儒學'
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('未見於引句' in e for e in v.validate(self.root)))

    def test_adjacent_relation_context_must_match_evidence(self):
        def mutate(d):
            a=next(a for a in d['assertions'] if 'context' in a)
            a['context']['paragraph_ids'][1]=a['context']['paragraph_ids'][0]
        self.change('corpus/shiji/059-assertions.json',mutate)
        self.assertTrue(any('相鄰兩段' in e for e in v.validate(self.root)))


    def test_title_antecedent_rejects_wrong_holder_anchor(self):
        def mutate(d):
            h=next(h for h in d['holdings'] if h['title']=='膠西王')
            e=next(e for e in h['evidence'] if 'context' in e)
            e['context']['person_mention_id']='c-shiji-059-wuzong:m001-0000'
        self.change('corpus/shiji/059-titles.json',mutate)
        self.assertTrue(any('前段錨點或引句無效' in e for e in v.validate(self.root)))

    def test_title_antecedent_rejects_nonadjacent_paragraph(self):
        def mutate(d):
            h=next(h for h in d['holdings'] if h['title']=='膠西王')
            e=next(e for e in h['evidence'] if 'context' in e)
            e['context']['paragraph_id']='c-shiji-059-wuzong:p013'
        self.change('corpus/shiji/059-titles.json',mutate)
        self.assertTrue(any('前段錨點或引句無效' in e for e in v.validate(self.root)))

    def test_kinship_default_must_match_recorded_alternative(self):
        def mutate(d):
            d['annotation']['kinship_interpretation_cases'][0]['default_alternative_id'] = 'invented'
        self.change('corpus/shiji/100.json', mutate)
        self.assertTrue(any('親屬預設選項' in error for error in v.validate(self.root)))

    def test_migration_snapshot_allows_later_canonical_people(self):
        self.change('registry/person-id-migrations.json', lambda d: d.update(person_count=d['person_count'] - 1))
        self.assertEqual(v.validate(self.root), [])

    def test_migration_snapshot_rejects_impossible_count(self):
        self.change('registry/person-id-migrations.json', lambda d: d.update(person_count=10**9))
        self.assertTrue(any('全面遷移範圍' in e for e in v.validate(self.root)))

    def test_retired_id_alias_cannot_be_reintroduced(self):
        self.change('registry/persons.json', lambda d: d['persons'][0].update(id_aliases=['cbr-p999999']))
        self.assertTrue(any('舊 ID 撤除後' in e for e in v.validate(self.root)))

    def test_retired_id_policy_rejects_unupdated_references(self):
        self.change('registry/person-id-migrations.json', lambda d: d['alias_retirement'].update(active_reference_count=1))
        self.assertTrue(any('舊 ID 撤除後' in e for e in v.validate(self.root)))

    def test_title_numeric_year_rejects_bce_numbering_error(self):
        def mutate(d):
            h = next(h for h in d['holdings'] if h['title'] == '太常')
            h['effective_period']['start']['normalized_date']['year'] = -154
        self.change('corpus/shiji/101-titles.json', mutate)
        self.assertTrue(any('天文年' in e for e in v.validate(self.root)))

    def test_title_numeric_year_must_anchor_its_own_event(self):
        def mutate(d):
            h = next(h for h in d['holdings'] if h['title'] == '太常')
            date = h['effective_period']['start']['normalized_date']
            date['original_quote'] = '三年正月乙巳'
        self.change('corpus/shiji/101-titles.json', mutate)
        self.assertTrue(any('本筆事件證據' in e for e in v.validate(self.root)))

    def test_title_usage_year_rejects_bce_numbering_error(self):
        def mutate(d):
            h = next(h for h in d['holdings'] if h['title'] == '主爵都尉')
            h['attestations'][0]['normalized_date']['year'] = -131
        self.change('corpus/shiji/107-titles.json', mutate)
        self.assertTrue(any('天文年' in e for e in v.validate(self.root)))

    def test_title_usage_year_requires_its_own_source_quote(self):
        def mutate(d):
            h = next(h for h in d['holdings'] if h['title'] == '主爵都尉')
            h['attestations'][0]['normalized_date']['original_quote'] = '元朔三年'
        self.change('corpus/shiji/107-titles.json', mutate)
        self.assertTrue(any('本筆事件證據' in e for e in v.validate(self.root)))

    def test_parallel_event_year_requires_source_event_quote(self):
        d = json.loads((self.root/'corpus/shiji/110-life-events.json').read_text())
        date = next(e for e in d['events'] if e['id'] == 'le-shiji110-wanghui')['normalized_date']
        self.assertTrue(v.parallel_event_date(date))
        date['basis']['source_event_quote'] = '此為合成測試的未見原文事件'
        self.assertIn('平行事件定年缺少原句或分層參考證據', v.normalized_date_errors(date))

    def test_parallel_event_year_requires_separate_year_reference(self):
        d = json.loads((self.root/'corpus/shiji/110-life-events.json').read_text())
        date = next(e for e in d['events'] if e['id'] == 'le-shiji110-wanghui')['normalized_date']
        date['references'] = [r for r in date['references'] if r['scope'] == 'received_parallel_event']
        self.assertFalse(v.parallel_event_date(date))
        self.assertIn('平行事件定年缺少原句或分層參考證據', v.normalized_date_errors(date))

    def test_posthumous_huainan_title_of_son_is_not_the_father(self):
        d = json.loads((self.root/'corpus/shiji/010.json').read_text())
        m = next(m for p in d['paragraphs'] for m in p['mentions'] if m['id'] == 'c-shiji-010-wendi:m023-0149')
        self.assertEqual(m['surface'], '淮南王')
        self.assertEqual(m['kind'], 'unresolved')
        self.assertIsNone(m['person_id'])
        reg = json.loads((self.root/'registry/persons.json').read_text())
        father = next(p for p in reg['persons'] if p['id'] == 'yqp_nlb_p1p_AF')
        self.assertNotIn(m['id'], {e['mention_id'] for e in father['evidence']})

    def test_appended_zhengyi_layer_requires_matching_xml(self):
        def mutate(d):
            d['paragraphs'][-1]['text_layer'] = 'witness_appended_zhengyi_note'
        self.change('corpus/shiji/103.json', mutate)
        self.assertTrue(any('XML 文字層次不符' in e for e in v.validate(self.root)))
        from scripts.render_corpus import render
        chapter = json.loads((self.root/'corpus/shiji/103.json').read_text())
        (self.root/'corpus/shiji/103.xml').write_text(render(chapter))
        self.assertEqual(v.validate(self.root), [])

    def test_ancestral_origin_cannot_invent_named_ancestor(self):
        def mutate(d):
            a = next(a for a in d['assertions'] if a['relation'] == 'ancestral_origin')
            a['qualifiers']['ancestor_person_id'] = a['person_id']
        self.change('corpus/shiji/103-addresses.json', mutate)
        self.assertTrue(any('祖先出身不得暗補' in error for error in v.validate(self.root)))


    def test_daughter_birth_order_scope_preserves_unknown_ordinal(self):
        d=json.loads((self.root/'corpus/shiji/105-assertions.json').read_text())
        order=d['assertions'][0]['qualifiers']['birth_order']
        self.assertEqual(order['scope'],'daughters_of_parent')
        self.assertIsNone(order['ordinal'])
        self.assertEqual(order['position'],'younger_or_youngest')
        self.assertEqual(v.validate(self.root),[])
        def mutate(d):
            d['assertions'][0]['qualifiers']['birth_order']['scope']='unknown_sequence'
        self.change('corpus/shiji/105-assertions.json',mutate)
        self.assertTrue(any('排行序列範圍未知' in e for e in v.validate(self.root)))

    def test_named_age_subset_cannot_drop_unknown_members(self):
        self.change('corpus/shiji/089.json', lambda d: d['annotation']['age_assertions'][0]['group_reference'].update(additional_members_unknown=False))
        self.assertIn('群體報齡具名範圍或未名成員不符', v.validate(self.root))
    def test_named_age_subset_cannot_add_another_person(self):
        self.change('corpus/shiji/089.json', lambda d: d['annotation']['age_assertions'][0]['group_reference']['person_ids'].__setitem__(1,'agx_sqm_4ou_A'))
        self.assertIn('群體報齡具名名單未見於引句', v.validate(self.root))
    def test_named_age_subset_cannot_invent_upper_age(self):
        self.change('corpus/shiji/089.json', lambda d: d['annotation']['age_assertions'][0]['bounds'].update(upper=69))
        self.assertIn('來源年齡界限與有餘原詞不符', v.validate(self.root))

    def test_royal_territory_requires_reigning_phrase_not_any_locality(self):
        self.change('corpus/shiji/094-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji094-011')['jurisdictions'][0].update(source_name='臨淄'))
        self.assertIn('王國範圍須保留王某地原句，不得由任意地名補入',v.validate(self.root))
    def test_royal_territory_cannot_invent_modern_location(self):
        self.change('corpus/shiji/094-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji094-011')['jurisdictions'][0].update(modern_identification='今地'))
        self.assertIn('稱號所屬原地名缺少引句或未保留未知定位',v.validate(self.root))


    def test_life_year_range_cannot_also_claim_exact_year(self):
        def change(d):
            e=d['events'][3];r=e['normalized_date_range']
            e['normalized_date']=dict(r['latest'],year_numbering='astronomical',precision='year',status='editorial_provisional',original_quote=r['original_quote'],evidence=r['evidence'],references=r['references'],rationale='測試夾帶單年，應拒絕',reviewer='synthetic',human_reviewed=False)
        self.change('corpus/shiji/096-life-events.json',change)
        self.assertIn('生卒或事件跨年範圍不得另填確定單年',v.validate(self.root))

    def test_life_year_range_cannot_collapse_to_one_year(self):
        self.change('corpus/shiji/096-life-events.json',lambda d: d['events'][3]['normalized_date_range'].update(earliest=d['events'][3]['normalized_date_range']['latest'].copy()))
        self.assertIn('歲首跨年範圍須涵蓋相鄰兩年，不可倒序或冒作單年',v.validate(self.root))

    def test_direct_bounded_age_cannot_be_exact_hundred(self):
        self.change('corpus/shiji/096.json',lambda d:d['annotation']['age_assertions'][0].update(value=100))
        self.assertIn('直接報齡餘歲須保存開放下界及原詞，不得補限定詞或傳聞分組',v.validate(self.root))

    def test_unknown_narrator_requires_unlinked_source_anchor(self):
        self.change('corpus/shiji/096.json', lambda d: d['annotation']['unresolved_identity_cases'][-1].update(unresolved_mention_ids=['c-shiji-096-zhang:m020-0000']))
        self.assertIn('未知敘者可能須有未連人物的原文錨點',v.validate(self.root))
    def test_single_known_candidate_requires_unknown_identity_flag(self):
        self.change('corpus/shiji/096.json', lambda d: d['annotation']['unresolved_identity_cases'][-1].pop('unknown_identity_possible'))
        self.assertIn('未決身份候選人物無效',v.validate(self.root))
    def test_unknown_narrator_cannot_have_no_known_candidate(self):
        self.change('corpus/shiji/096.json', lambda d: d['annotation']['unresolved_identity_cases'][-1].update(candidate_person_ids=[]))
        self.assertIn('未決身份候選人物無效',v.validate(self.root))

    def test_direct_age_year_prefix_cannot_be_tenure_wording(self):
        self.change('corpus/shiji/097.json', lambda d: d['annotation']['age_assertions'][0].update(source_term='六十年餘'))
        self.assertIn('直接報齡餘歲須保存開放下界及原詞，不得補限定詞或傳聞分組',v.validate(self.root))

    def test_candidate_exhaustiveness_cannot_be_a_string(self):
        self.change('corpus/shiji/097.json', lambda d: next(c for c in d['annotation']['unresolved_identity_cases'] if c['id']=='ic-shiji097-unnamed-chanyu').update(candidate_list_exhaustive='false'))
        self.assertIn('候選名單是否窮盡須明示布林值',v.validate(self.root))

    def test_nonexhaustive_case_accepts_single_supported_candidate(self):
        def change(d):
            case = next(c for c in d['annotation']['unresolved_identity_cases'] if c['id']=='ic-shiji097-unnamed-chanyu')
            case['candidate_person_ids'] = case['candidate_person_ids'][:1]
        self.change('corpus/shiji/097.json', change)
        self.assertNotIn('未決身份候選人物無效', v.validate(self.root))

    def test_table_parent_quote_cannot_be_edited_independently(self):
        self.change('corpus/shiji/016-assertions.json',lambda d:d['assertions'][0]['evidence'][0].update(quote='敖子'))
        self.assertIn('親屬表格引句須完整對應原格',v.validate(self.root))

    def test_table_parent_source_requires_registered_book(self):
        def change(d):
            work=next(w for w in d['works'] if w['id']=='w-shiji')
            work['books']=[b for b in work['books'] if b['id']!='b-shiji-016']
        self.change('registry/works.json',change)
        self.assertIn('表格證據著作卷篇未登記或歸屬不符',v.validate(self.root))

    def test_succession_rejects_an_office_as_inherited_noble_title(self):
        path = self.root / 'corpus/hanshu/041-assertions.json'
        data = json.loads(path.read_text())
        claim = next(a for a in data['assertions'] if a['id'] == 'a-hanshu041-jin-001')
        claim['qualifiers']['succession']['predecessor_holding_id'] = 'th-hanshu041-jin-004'
        path.write_text(json.dumps(data, ensure_ascii=False))
        self.assertIn('嗣位原詞須有父子、前任爵位及同段人物錨點，不得虛構爵名或起訖', v.validate(self.root))

    def test_cross_work_evidence_cannot_relabel_hanshu_as_shiji(self):
        self.change('corpus/hanshu/041-assertions.json',lambda d:d['assertions'][0]['evidence'][0].update(work_id='w-shiji'))
        self.assertIn('引文著作卷ID與實際來源不符',v.validate(self.root))


    def test_age_range_rejects_wrong_numbering(self):
        self.change('corpus/shiji/106.json', lambda d: d['annotation']['age_assertions'][0]['normalized_date_range']['earliest'].update(year=-197))
        self.assertIn('紀年範圍端點年編號不符', v.validate(self.root))
    def test_age_range_requires_own_source_quote(self):
        self.change('corpus/shiji/106.json', lambda d: d['annotation']['age_assertions'][0]['normalized_date_range'].update(original_quote='他篇原句'))
        self.assertIn('紀年範圍缺相符原紀年與事件引句', v.validate(self.root))
    def test_age_range_cannot_also_claim_single_year(self):
        self.change('corpus/shiji/106.json', lambda d: d['annotation']['age_assertions'][0].update(normalized_date={'era':'BCE','era_year':196,'year':-195}))
        self.assertIn('來源報齡跨年範圍不得另填確定單年', v.validate(self.root))

    def test_title_parallel_range_requires_fixed_same_person_table_event(self):
        self.change('corpus/shiji/106-titles.json', lambda d: next(h for h in d['holdings'] if h['id']=='th-shiji106-005')['effective_period']['start']['normalized_date_range']['table_event'].update(source_revision='1'))
        self.assertIn('稱號平行紀年表格來源或固定修訂不符',v.validate(self.root))

    def test_fixed_biography_explicit_name_cannot_bypass_native_source_guard(self):
        # Explicit full names have no inferred-surname path; the native validator
        # must still reject a given name that is absent from the fixed witness.
        def change_explicit_name(record):
            name = next(n for n in record['records']
                        if n.get('fixed_biography_name_binding', {}).get('mode') == 'full_name'
                        and not n.get('surname_basis'))
            name['ming'] = '非原文姓名'
        self.change('corpus/jinshu/040-jiachong-family-name-components.json', change_explicit_name)
        self.assertIn('固定傳記姓名構件須綁原人物、原名與字詞及完整見證', v.validate(self.root))

if __name__=='__main__':unittest.main()
