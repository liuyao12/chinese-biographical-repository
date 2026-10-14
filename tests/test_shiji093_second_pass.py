# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class HanLuIdentityTests(unittest.TestCase):
    def paragraph(self, book, suffix):
        c = json.loads((ROOT / f'corpus/shiji/{book}.json').read_text())
        return next(p for p in c['paragraphs'] if p['id'].endswith(':' + suffix))
    def ids(self, p, surface):
        return {m['person_id'] for m in p['mentions'] if m['surface'] == surface}
    def test_kings_and_two_hanxin_people_stay_distinct(self):
        p = self.paragraph('093', 'p001')
        self.assertEqual(self.ids(p, '韓王信'), {'l9e_fbr_36a_*A'})
        self.assertEqual(self.ids(p, '橫陽君成'), {'8i3_5vf_iu9'})
        q = self.paragraph('093', 'p003')
        self.assertEqual(self.ids(q, '鄭昌'), {'vxt_uj1_8ym'})
        self.assertEqual(self.ids(q, '韓王昌'), {'vxt_uj1_8ym'})
        self.assertEqual(self.ids(self.paragraph('092', 'p001'), '淮陰侯韓信'), {'ofc_8ei_jb7'})
        self.assertIn('故吳令鄭昌', self.paragraph('007', 'p024')['text'])
    def test_new_huaiwang_is_not_earlier_captive_king(self):
        p = self.paragraph('093', 'p001')
        self.assertEqual(self.ids(p, '項梁'), {'5xt_rg8_7zs_A'})
        self.assertEqual(self.ids(p, '懷王'), {'c2w_s7g_en0_*A'})
        q = self.paragraph('007', 'p006')
        self.assertIn('自懷王入秦不反', q['text'])
        self.assertIn('求楚懷王孫心', q['text'])
        self.assertEqual(self.ids(q, '懷王'), {'c2w_s7g_en0', 'c2w_s7g_en0_*A'})
    def test_baideng_people_and_short_names_use_scoped_evidence(self):
        p = self.paragraph('093', 'p005')
        self.assertEqual(self.ids(p, '冒頓'), {'wjt_htu_081_A'})
        self.assertEqual(self.ids(p, '陳平'), {'i3f_9l9_g53'})
        self.assertIn('白登', self.paragraph('110', 'p012')['text'])
        self.assertIn('高帝用陳平奇計', self.paragraph('056', 'p012')['text'])
        p = self.paragraph('093', 'p008')
        self.assertEqual(self.ids(p, '蕭'), {'xd8_uww_5ok'})
        self.assertEqual(self.ids(p, '曹'), {'37j_16p_7n8'})
        rows = json.loads((ROOT / 'corpus/shiji/093-equivalences.json').read_text())['decisions']
        for key in ['xiao', 'cao']:
            row = next(x for x in rows if x['id'] == 'eq-shiji093-review-' + key)
            self.assertIn('較弱', row['rationale'])
            self.assertFalse(row['human_reviewed'])

    def test_gongwei_uses_the_same_liu_jia_lu_wan_campaign(self):
        p = self.paragraph('093', 'p009')
        self.assertEqual(self.ids(p, '共尉'), {'stm_voa_t08'})
        q = self.paragraph('051', 'p003')
        self.assertIn('太尉盧綰', q['text'])
        self.assertIn('臨江王共尉', q['text'])
    def test_zhao_officers_and_zhoubo_do_not_merge_same_office(self):
        self.assertEqual(self.ids(self.paragraph('093', 'p015'), '周昌'), {'gfr_55l_72s'})
        p = self.paragraph('093', 'p011')
        self.assertEqual(self.ids(p, '審食其'), {'qg7_n12_fne'})
        self.assertEqual(self.ids(p, '趙堯'), {'afb_ahe_sqp'})
        self.assertEqual(self.ids(self.paragraph('093', 'p017'), '勃'), {'koy_6jg_gcc'})
        self.assertIn('徙御史大夫周昌為趙相', self.paragraph('096', 'p006')['text'])
        self.assertIn('遂拜趙堯為御史大夫', self.paragraph('096', 'p007')['text'])
        self.assertIn('勃遷為太尉', self.paragraph('057', 'p004')['text'])

    def test_han_and_lu_direct_paths_keep_unknown_generations(self):
        people = {p['id']: p for p in json.loads((ROOT / 'registry/persons.json').read_text())['persons']}
        han = people['l9e_fbr_36a_*A']['family_path']
        self.assertEqual(han['ancestor_person_id'], 'l9e_fbr_36a')
        self.assertEqual(han['connection'], 'grandfather')
        self.assertIsNone(han['parent_person_id'])
        self.assertEqual(han['intermediate_person_ids'], [None])
        self.assertEqual(han['source_assertion_id'], 'a-shiji093-001')
        self.assertEqual(people['l9e_fbr_36a_*AB']['family_path']['parent_person_id'], 'l9e_fbr_36a_*A')
        self.assertEqual(people['l9e_fbr_36a_*AB*A']['family_path']['ancestor_person_id'], 'l9e_fbr_36a_*AB')
        self.assertEqual(people['jjl_irg_zke_A']['family_path']['parent_person_id'], 'jjl_irg_zke')
        self.assertEqual(people['jjl_irg_zke_A*A']['family_path']['intermediate_person_ids'], [None])
        self.assertFalse(any(p['id'].endswith('_*') for p in people.values()))

    def test_gonggao_and_hanyan_endpoints_match_in_both_chapters(self):
        p = self.paragraph('093', 'p007')
        q = self.paragraph('125', 'p003')
        self.assertEqual(self.ids(p, '韓嫣'), {'l9e_fbr_36a_*AB*A'})
        self.assertEqual(self.ids(q, '韓嫣'), {'l9e_fbr_36a_*AB*A'})
        self.assertEqual(self.ids(q, '弓高侯'), {'l9e_fbr_36a_*AB'})
        self.assertEqual(self.ids(q, '韓說'), {'gh3_d07_hkt'})
        self.assertEqual(self.ids(p, '說'), {'gh3_d07_hkt'})
        self.assertEqual(self.ids(self.paragraph('093', 'p001'), '韓襄王'), {'l9e_fbr_36a'})

    def test_sibling_grandfather_is_not_fabricated_as_direct_assertion(self):
        rows = json.loads((ROOT / 'corpus/shiji/093-assertions.json').read_text())['assertions']
        brother = next(x for x in rows if x['id'] == 'a-shiji093-006')
        self.assertEqual((brother['subject_person_id'], brother['object_person_id']),
                         ('gh3_d07_hkt', 'l9e_fbr_36a_*AB*A'))
        self.assertFalse(any(x['subject_person_id'] == 'gh3_d07_hkt' and x['predicate'] in ['father', 'grandfather'] for x in rows))

    def test_zi_dai_is_an_unnamed_son_and_succession_verb(self):
        p = self.paragraph('093', 'p007')
        m = next(x for x in p['mentions'] if x['id'] == 'c-shiji-093-hanlu:m007-0137')
        self.assertEqual(m['surface'], '子')
        self.assertEqual(p['text'][m['end']], '代')
        self.assertEqual(m['person_id'], 'gh3_d07_hkt_A')
        people = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        child = next(x for x in people if x['id'] == m['person_id'])
        self.assertIn('子未名', child['label'])
        self.assertEqual(child['family_path']['parent_person_id'], 'gh3_d07_hkt')
        self.assertFalse(any(a['surface'] in ['子代', '代', '長君'] for a in child['aliases']))
        rows = json.loads((ROOT / 'corpus/shiji/093-identities.json').read_text())['decisions']
        ref = next(x for x in rows if x['id'] == 'd-shiji093-032')['references'][0]
        self.assertEqual(ref['reported_name'], '長君')
        self.assertFalse(ref['adopted_as_received_name'])

    def test_han_emperor_short_names_follow_their_reigns(self):
        self.assertEqual(self.ids(self.paragraph('093', 'p007'), '孝文'), {'yqp_nlb_p1p_AC'})
        self.assertEqual(self.ids(self.paragraph('093', 'p013'), '孝景'), {'yqp_nlb_p1p_ACA'})
        self.assertIn('孝文皇帝，高祖中子', self.paragraph('010', 'p001')['text'])
        self.assertIn('孝景皇帝者，孝文之中子', self.paragraph('011', 'p001')['text'])
    def test_quoted_yue_and_wu_people_keep_departure_and_death_accounts(self):
        p = self.paragraph('093', 'p006')
        self.assertEqual(self.ids(p, '種'), {'gu2_fde_5bw'})
        self.assertEqual(self.ids(p, '蠡'), {'yhm_h9f_8p0'})
        self.assertEqual(self.ids(p, '伍子胥'), {'g9h_5ih_ug1_A'})
        self.assertIn('種、蠡無一罪，身死亡', p['text'])
        self.assertIn('范蠡浮海出齊', self.paragraph('041', 'p020')['text'])
        self.assertIn('種遂自殺', self.paragraph('041', 'p013')['text'])
        self.assertIn('乃自剄死', self.paragraph('066', 'p019')['text'])
