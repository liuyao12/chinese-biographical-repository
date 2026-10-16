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

class LiLuContextTitleTests(unittest.TestCase):
    def test_king_reference_follows_dialogue_and_excludes_verbs(self):
        self.assertEqual(ids(6,'王'),{'0hs_fg6_1qj_A'})
        self.assertEqual(ids(10,'王'),{'r3c_eue_cqn'})
        self.assertEqual(ids(11,'王'),{'r3c_eue_cqn'})
        for n,phrase,offset in [(6,'先入咸陽者王之',5),(11,'故王此',1),(10,'君王王南越',2)]:
            p=para(n);start=p['text'].index(phrase)+offset
            self.assertEqual(p['text'][start],'王')
            self.assertFalse(any(m['start']<=start<m['end'] for m in p['mentions']))

    def test_emperor_and_recipient_in_same_speech_are_distinct(self):
        self.assertEqual(ids(10,'天子'),{'yqp_nlb_p1p_A'})
        self.assertEqual(ids(10,'君王'),{'r3c_eue_cqn'})
        self.assertEqual(ids(11,'皇帝'),{'yqp_nlb_p1p_A'})
        self.assertEqual(ids(5,'上'),{'yqp_nlb_p1p_A'})
        self.assertEqual(ids(8,'上'),{'yqp_nlb_p1p_A'})

    def test_county_magistrate_reference_does_not_include_hang_verb(self):
        p=para(23);start=p['text'].index('縣令首於長竿')
        m=next(m for m in p['mentions'] if m['start']==start+1)
        self.assertEqual((m['surface'],m['person_id']),('令','wfk_n4m_6x9'))
        self.assertFalse(any(m['start']<=start<m['end'] for m in p['mentions']))
        self.assertEqual(ids(23,'令'),{'wfk_n4m_6x9'})

    def test_remaining_leaders_use_source_biography_identities(self):
        for n,s,pid in [(2,'陳勝','pom_ycp_ha5'),(2,'項梁','5xt_rg8_7zs_A'),(11,'蕭何','xd8_uww_5ok'),(11,'曹參','37j_16p_7n8')]:self.assertEqual(ids(n,s),{pid})
        for old in ['x8j_rqz_jry','7s0_vhn_yay','s13_zwm_7o1','f8j_w3m_2ep']:
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())

    def test_grant_month_and_explicit_abolition_have_separate_boundaries(self):
        holdings={h['id']:h for h in read('corpus/shiji/097-titles.json')['holdings']}
        grant=holdings['th-shiji097-005']['effective_period']['start']
        self.assertEqual(grant['normalized_date']['era_year'],195)
        self.assertTrue(any('三月丙寅' in r['quote'] for r in grant['normalized_date']['references']))
        period=holdings['th-shiji097-006']['effective_period']
        self.assertEqual(period['start']['status'],'unknown')
        self.assertEqual(period['end']['event_type'],'abolition')
        d=period['end']['normalized_date_range']
        self.assertEqual((d['earliest']['era_year'],d['latest']['era_year']),(123,122))
        self.assertEqual(d['evidence'],period['end']['evidence'])
        self.assertNotIn('normalized_date',period['end'])

    def test_flattened_title_range_cannot_be_mistaken_for_life_event(self):
        b=read('exports/persons/oge_g2v_hqw.json')
        r=next(r for r in b['date_range_normalizations'] if r['record_id']=='th-shiji097-006')
        self.assertEqual((r['date_role'],r['endpoint'],r['title']),('title_period','end','武遂侯'))
        self.assertNotIn('event_type',r)
        self.assertTrue(any(r['record_id']=='le-shiji097-004' and r['date_role']=='life_event' for r in b['date_range_normalizations']))

class LiLuAllusionScopeTests(unittest.TestCase):
    def test_founding_kings_and_fuchai_keep_literal_allusion_scope(self):
        self.assertEqual(ids(12,'湯'),{'tpz_x3m_e0h'})
        self.assertEqual(ids(12,'武'),{'y4i_pjk_4gn_AA'})
        self.assertEqual(ids(12,'吳王夫差'),{'5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA'})
        p=para(12);start=p['text'].index('文武并用')
        self.assertFalse(any(m['start']<start+4 and start<m['end'] for m in p['mentions']))

    def test_zhibo_matches_jinyang_opponent_not_earlier_wenzi(self):
        self.assertEqual(ids(12,'智伯'),{'fks_8ov_okp'})
        eq=next(x for x in read('corpus/shiji/097-equivalences.json')['decisions'] if x['id']=='eq-shiji097-allusion-zhibo')
        self.assertTrue(any(e['paragraph_id']=='c-shiji-086-cike:p009' and '趙襄子與韓、魏合謀滅智伯' in e['quote'] for e in eq['evidence']))
        self.assertNotIn('n7k_r8y_fkr',eq['person_ids'])

    def test_legendary_comparison_does_not_create_han_participant(self):
        self.assertEqual(ids(6,'蚩尤'),{'7x2_x55_1b6'})
        b=read('exports/persons/7x2_x55_1b6.json')
        who=next(p for p in b['persons'] if p['id']=='7x2_x55_1b6')
        self.assertEqual(who['historicity'],'legendary_tradition')
        self.assertEqual(read('data/corpus/profiles/7x2_x55_1b6.json')['historicity'],'legendary_tradition')
        self.assertFalse(any(e['person_id']=='7x2_x55_1b6' for e in read('corpus/shiji/097-life-events.json')['events']))
        self.assertFalse(any(h['person_id']=='7x2_x55_1b6' for h in read('corpus/shiji/097-titles.json')['holdings']))

    def test_young_emperor_preserves_competing_office_chronologies(self):
        case=next(c for c in read('corpus/shiji/097.json')['annotation']['unresolved_identity_cases'] if c['id']=='ic-shiji097-young-emperor')
        self.assertEqual(case['status'],'unresolved')
        self.assertEqual(set(case['candidate_person_ids']),{'0bm_5gr_a7x','nc4_msq_h8a','zht_ze7_m2d'})
        quotes=[r['quote'] for r in case['references']]
        self.assertTrue(any('孝惠帝六年，置太尉官' in q for q in quotes))
        self.assertTrue(any('立常山王義為帝' in q and '置太尉官' in q for q in quotes))
        self.assertTrue(any(r.get('revision_id')==7904628 for r in case['references']))
        self.assertEqual(ids(14,'少主'),{'0bm_5gr_a7x'})
        for pid in case['candidate_person_ids']:
            self.assertTrue(any(c['id']==case['id'] for c in read(f'exports/persons/{pid}.json')['unresolved_identity_cases']))

    def test_five_allusive_candidates_have_no_public_alias_files(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        for old in ['p03_ogp_trh','bzw_kmw_yhu','byn_obj_9yj','tp1_kws_nsp','7hd_xs5_eks']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())
