import copy
import json
import unittest
from pathlib import Path
from scripts.life_event_dates import date_decision_errors, selected_dates
from scripts.person_bundle import bundle, load_catalog
from scripts.validate_corpus import reported_office_event_count_valid

ROOT = Path(__file__).resolve().parents[1]


class PingyuanEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people, cls.records = load_catalog(ROOT)
        cls.events = {e['id']: e for r in cls.records if r.get('record_type') == 'person_life_event_assertion_set' for e in r['events']}
        cls.equivalences = [d for r in cls.records if r.get('record_type') == 'person_equivalence_set' for d in r['decisions']]
        cls.decision = json.loads((ROOT/'corpus/shiji/076-date-decisions.json').read_text())['decisions'][0]

    def errors(self, d, events=None):
        return date_decision_errors(d, events or self.events, self.equivalences, self.people)

    def test_office_departures_and_reinstatements_do_not_invent_tenure(self):
        h = json.loads((ROOT/'corpus/shiji/076-titles.json').read_text())['holdings'][0]
        for key in ('departure', 'reinstatement'):
            c = h['reported_office_event_counts'][key]
            self.assertEqual(c['value'], 3)
            self.assertTrue(reported_office_event_count_valid(c, key))
            for field, value in [('value', True), ('value', 4), ('unit', 'title_year'), ('source_number', None), ('source_term', '三為相')]:
                altered = copy.deepcopy(c); altered[field] = value
                self.assertFalse(reported_office_event_count_valid(altered, key))
            self.assertFalse(reported_office_event_count_valid(c, 'appointment'))
        self.assertNotIn('reported_duration', h)
        self.assertTrue(all(x['status'] == 'unknown' for x in h['effective_period'].values()))

    def test_conflicting_death_years_preserve_sources_and_machine_readable_selection(self):
        b = bundle('03v_bhv_img', include_provisional=True, catalog=(self.people, self.records))
        e = {e['id']: e for e in b['life_events']}
        self.assertEqual(e['le-shiji043-055']['date_expression'], '十四年')
        self.assertEqual(e['le-shiji043-055']['normalized_date']['era_year'], 252)
        self.assertEqual(e['le-shiji076-003']['date_expression'], '趙孝成王十五年')
        self.assertEqual(e['le-shiji076-003']['normalized_date']['era_year'], 251)
        d = b['life_event_date_decisions'][0]
        self.assertEqual(d['preferred_event_id'], 'le-shiji076-003')
        self.assertEqual(b['selected_life_event_dates'][0]['year'], -250)
        self.assertEqual(b['selected_life_event_dates'][0]['selection_decision_id'], d['id'])
        self.assertFalse(self.errors(d))
        self.assertNotIn('life_event_date_decisions', bundle('lrj_utu_y6w', catalog=(self.people, self.records)))

    def test_selection_cannot_point_outside_candidates_or_drop_an_account(self):
        d = copy.deepcopy(self.decision); d['preferred_event_id'] = 'le-shiji076-002'
        self.assertIn('生卒紀年取捨預設須屬候選；未解不得選定', self.errors(d))
        d = copy.deepcopy(self.decision); d['evidence'].pop()
        self.assertIn('生卒紀年取捨須完整保留各候選事件證據', self.errors(d))

    def test_date_selection_cannot_merge_unrelated_people_or_change_event_type(self):
        d = copy.deepcopy(self.decision); d['person_ids'] = ['03v_bhv_img', 'cdg_kvt_y0p']
        self.assertIn('生卒紀年取捨不得跨未判同指人物', self.errors(d))
        d = copy.deepcopy(self.decision); d['event_type'] = 'birth'
        self.assertIn('生卒紀年取捨事件種類或人物不符', self.errors(d))

    def test_unresolved_years_produce_no_selected_date_and_unknown_dates_cannot_be_ranked(self):
        d = copy.deepcopy(self.decision); d.update(status='unresolved', preferred_event_id=None)
        self.assertFalse(self.errors(d))
        self.assertEqual(selected_dates(list(self.events.values()), [d]), [])
        e = copy.deepcopy(self.events); e['le-shiji043-055'].pop('normalized_date')
        self.assertIn('生卒紀年取捨須有不同的已存數字換年', self.errors(self.decision, e))

    def test_yuqing_finally_in_liang_is_not_a_death_or_native_place(self):
        b = bundle('cdg_kvt_y0p', catalog=(self.people, self.records))
        self.assertEqual(b.get('life_events', []), [])
        addresses = b['address_assertions']
        self.assertEqual({a['place']['source_name'] for a in addresses if a['relation']=='residence'}, {'梁', '大梁'})
        self.assertFalse(any(a['relation'] in ('biographical_origin', 'death_place', 'birth_place') for a in addresses))
        mission = next(a for a in addresses if a['id'] == 'pa-shiji076-008')
        self.assertEqual(mission['qualifiers']['arrival_status'], 'not_explicitly_attested')

    def test_li_hou_is_the_father_and_dead_son_gets_no_automatic_posthumous_rank(self):
        b = bundle('y0c_hok_598_A', catalog=(self.people, self.records))
        self.assertEqual([e['source_term'] for e in b['life_events']], ['李同戰死'])
        self.assertNotIn('normalized_date', b['life_events'][0])
        self.assertFalse(any(h['title'] == '李侯' for h in b['title_holdings']))
        father = bundle('y0c_hok_598', catalog=(self.people, self.records))
        h = next(h for h in father['title_holdings'] if h['title']=='李侯')
        self.assertEqual(h['mode'], 'grant')
        self.assertEqual(h['effective_period']['end']['status'], 'unknown')

    def test_public_profile_preserves_both_accounts_and_the_recorded_counts(self):
        profile = json.loads((ROOT/'data/corpus/profiles/03v_bhv_img.json').read_text())
        self.assertEqual({e['date_expression'] for e in profile['life_events']}, {'十四年', '趙孝成王十五年'})
        self.assertEqual(profile['selected_life_event_dates'][0]['era_year'], 251)
        h = next(h for h in profile['titles'] if h['id']=='th-shiji076-001')
        self.assertEqual(h['reported_office_event_counts']['departure']['value'], 3)
        self.assertEqual(h['period'], '未定 → 未定')
