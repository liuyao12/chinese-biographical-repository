import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def para(n):return read('corpus/shiji/097.json')['paragraphs'][n-1]
def ids(n,s):return {m['person_id'] for m in para(n)['mentions'] if m['surface']==s and m['kind']=='person'}
class LiLuSecondPassTests(unittest.TestCase):
    def test_court_people_follow_particular_events(self):
        for n,s,pid in [(5,'項羽','ob7_g6i_7pp'),(8,'黥布','zxd_afr_2xg'),(14,'絳侯','koy_6jg_gcc'),(18,'呂太后','i30_mjq_6q8_A'),(18,'孝惠帝','yqp_nlb_p1p_AA'),(20,'淮南厲王','yqp_nlb_p1p_AF')]:
            self.assertEqual(ids(n,s),{pid})
        self.assertEqual(ids(14,'陳平'),{'i3f_9l9_g53'})
        self.assertNotIn('rwg_skp_gbq',ids(14,'陳平'))

    def test_hongru_corrected_identity_preserves_received_spelling(self):
        self.assertEqual(ids(18,'閎籍孺'),{'nxn_szf_9gi'})
        self.assertEqual(para(18)['text'].count('閎籍孺'),2)
        b=read('exports/persons/nxn_szf_9gi.json')
        corrections=[d['preferred_reading'] for d in b['identity_decisions'] if d.get('preferred_reading')]
        self.assertEqual({d['person_mention_id'] for d in corrections},{'c-shiji-097-luli:m018-0093','c-shiji-097-luli:m018-0196'})
        self.assertTrue(all(d['source_spelling_is_not_alias'] and d['preferred_surface']=='閎孺' for d in corrections))
        self.assertNotIn('wbf_66x_6s2',b['person_ids'])
        profile=read('data/corpus/profiles/nxn_szf_9gi.json')
        self.assertNotIn('閎籍孺',profile['names'])

    def test_jian_son_link_is_commentary_based_not_all_children_merged(self):
        self.assertEqual(ids(20,'其子'),{'tkc_9z3_91l_A'})
        self.assertEqual(ids(24,'子'),{'tkc_9z3_91l_A'})
        self.assertTrue(any(m['surface']=='諸子' and m['person_id'] is None for m in para(20)['mentions']))
        b=read('exports/persons/tkc_9z3_91l_A.json')
        eq=next(x for x in b['equivalence_decisions'] if x['id']=='eq-shiji097-zhujian-son-commentary')
        self.assertIn('與太史公善',eq['references'][0]['quote'])
        self.assertEqual(eq['references'][0]['revision_id'],2514767)
        self.assertFalse(eq['references'][0]['image_verified'])
        fathers=[x for x in b['relations'] if x['subject_person_id']=='tkc_9z3_91l_A' and x['predicate']=='father']
        self.assertTrue(fathers)
        self.assertEqual({x['object_person_id'] for x in fathers},{'tkc_9z3_91l'})

    def test_unknown_narrator_stays_unresolved_after_unrelated_merges(self):
        c=read('corpus/shiji/096.json')
        case=next(x for x in c['annotation']['unresolved_identity_cases'] if x['id']=='ic-shiji096-final-narrator')
        self.assertTrue(case['unknown_identity_possible'])
        self.assertEqual(case['status'],'unresolved')
        self.assertFalse(any(x['id']==case['id'] for x in c['annotation'].get('resolved_identity_cases',[])))

    def test_eight_retired_candidates_have_no_registry_or_public_files(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        for old in ['50g_j9s_2le','m68_ewg_gly','rg1_213_xlb','otq_r9b_d3z','noy_49h_qor','k4e_4tr_lg0','9hr_p35_zdj','tkc_9z3_91l_B']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())

class LiLuLifeEventTests(unittest.TestCase):
    def test_deaths_keep_actual_subjects_and_not_threats(self):
        events=read('corpus/shiji/097-life-events.json')['events']
        self.assertEqual(len(events),13)
        by_term={e['source_term']:e for e in events}
        for term,pid in [('平原君母死','clw_2zf_477'),('遂自剄','tkc_9z3_91l'),('遂死匈奴中','tkc_9z3_91l_A'),('淮南厲王殺辟陽侯','qg7_n12_fne'),('病死','oge_g2v_hqw')]:
            self.assertEqual(by_term[term]['person_id'],pid)
        self.assertFalse(any(e['evidence'][0]['paragraph_id'].endswith((':p011',':p013',':p018')) for e in events))
        self.assertFalse(any(e['source_term'] in ('欲自殺','當棄市','卒不誅') for e in events))

    def test_yuanshou_death_uses_year_window_not_the_opening_han_year(self):
        e=next(e for e in read('corpus/shiji/097-life-events.json')['events'] if e['person_id']=='oge_g2v_hqw')
        self.assertEqual(e['date_expression'],'元狩元年中')
        d=e['normalized_date_range']
        self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(123,122))
        self.assertNotIn('normalized_date',e)
        self.assertTrue(any(r.get('table_cell_id')=='shiji-022-t1-r085-c00' and r['quote']=='122' for r in d['references']))
        self.assertTrue(any(r.get('text_layer')=='suoyin_commentary' and r['revision_id']==2514838 for r in d['references']))
        self.assertIsNone(next(e for e in read('corpus/shiji/097-life-events.json')['events'] if e['person_id']=='tkc_9z3_91l_A')['date_expression'])

    def test_self_reported_age_has_no_invented_death_age_or_birth_year(self):
        a=read('corpus/shiji/097.json')['annotation']['age_assertions'][0]
        self.assertEqual((a['person_id'],a['source_term'],a['source_number']),('eya_qj3_tev','年六十餘','六十'))
        self.assertEqual(a['bounds'],{'lower':60,'lower_inclusive':False,'upper':None,'upper_inclusive':None})
        self.assertIsNone(a['value']);self.assertIsNone(a['birth_year'])
        self.assertEqual(a['reporting_status'],'direct_report')
        self.assertIn(a['source_term'],a['evidence'][0]['quote'])
        self.assertNotIn('歲',a['source_term'])

    def test_three_title_candidates_reconcile_with_same_events(self):
        self.assertEqual(ids(6,'義帝'),{'c2w_s7g_en0_*A'})
        self.assertEqual(ids(6,'成安君'),{'rx0_vif_1xq'})
        self.assertEqual(ids(20,'辟陽侯'),{'qg7_n12_fne'})
        for old in ['eqd_qrh_r6x','82r_i62_9f9','697_9f9_d41']:
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())

    def test_source_bundle_exposes_death_range_and_age_without_nlu(self):
        b=read('exports/persons/oge_g2v_hqw.json')
        self.assertTrue(any(e['id']=='le-shiji097-004' for e in b['life_events']))
        self.assertTrue(any(e['record_id']=='le-shiji097-004' for e in b['date_range_normalizations']))
        b=read('exports/persons/eya_qj3_tev.json')
        self.assertTrue(any(a['id']=='age-shiji097-001' for a in b['age_assertions']))
