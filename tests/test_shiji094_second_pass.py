# coding: utf-8
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class TianDanIdentityTests(unittest.TestCase):
    def paragraph(self, number, index):
        return json.loads((ROOT / f'corpus/shiji/{number}.json').read_text())['paragraphs'][index-1]

    def ids(self, paragraph, surface):
        return {m['person_id'] for m in paragraph['mentions'] if m['surface']==surface}

    def test_qi_campaign_and_short_forms_link_to_same_people(self):
        p=self.paragraph('094',9)
        for surface,pid in [('韓信','ofc_8ei_jb7'),('酈生','eya_qj3_tev'),('曹參','37j_16p_7n8'),('灌嬰','sj9_pfu_fwh'),('嬰','sj9_pfu_fwh')]:
            self.assertEqual(self.ids(p,surface),{pid})
        self.assertEqual(self.ids(self.paragraph('094',13),'淮陰'),{'ofc_8ei_jb7'})
        self.assertEqual(self.ids(self.paragraph('094',14),'酈生'),{'eya_qj3_tev'})
        self.assertEqual(self.ids(self.paragraph('093',3),'韓王信'),{'l9e_fbr_36a_*A'})
        self.assertIn('酈生言其弟酈商',self.paragraph('097',4)['text'])

    def test_implicit_subject_context_does_not_invent_name_anchor(self):
        p=self.paragraph('095',25)
        self.assertNotIn('灌嬰',p['text'])
        self.assertFalse(any(m.get('person_id')=='sj9_pfu_fwh' for m in p['mentions']))
        rows=json.loads((ROOT/'corpus/shiji/094-equivalences.json').read_text())['decisions']
        decision=next(d for d in rows if d['id']=='eq-shiji094-qi-campaign-guanying')
        context=decision['references'][0]
        self.assertEqual(context['paragraph_id'],p['id'])
        self.assertEqual(context['quote'],p['text'])
        self.assertIn('得齊守相田光',context['quote'])
        self.assertIn('漢將灌嬰追得齊守相田光',self.paragraph('094',9)['text'])
        self.assertIn('得故齊王田廣相田光',self.paragraph('054',5)['text'])
        self.assertIn('嬰遷為御史大夫',self.paragraph('095',24)['text'])

    def test_qi_campaign_candidate_files_retired(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('lp3_npi_io0','uj5_nzw_pnc','349_zmu_2u4','1wk_2dd_421'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

    def test_opening_people_and_two_huai_kings_stay_distinct(self):
        self.assertEqual(self.ids(self.paragraph('094',2),'陳涉'),{'pom_ycp_ha5'})
        self.assertEqual(self.ids(self.paragraph('094',2),'周市'),{'i8y_6lu_30h'})
        self.assertEqual(self.ids(self.paragraph('094',3),'魏王'),{'kez_re1_kcr'})
        self.assertEqual(self.ids(self.paragraph('094',3),'魏王咎'),{'kez_re1_kcr'})
        self.assertEqual(self.ids(self.paragraph('094',4),'項梁'),{'5xt_rg8_7zs_A'})
        self.assertEqual(self.ids(self.paragraph('094',5),'楚懷王'),{'c2w_s7g_en0_*A'})
        p=self.paragraph('007',6)
        self.assertIn('自懷王入秦不反',p['text'])
        self.assertIn('求楚懷王孫心',p['text'])
        self.assertEqual(self.ids(p,'懷王'),{'c2w_s7g_en0','c2w_s7g_en0_*A'})

    def test_tian_jian_xian_keeps_literal_characters_and_refusal_attribution(self):
        self.assertEqual(self.ids(self.paragraph('094',3),'田間'),{'27q_nw7_jv8'})
        self.assertEqual(self.ids(self.paragraph('094',4),'田閒'),{'27q_nw7_jv8'})
        self.assertIn('楚懷王曰：「田假與國之王',self.paragraph('094',5)['text'])
        self.assertIn('項梁曰：「田假為與國之王',self.paragraph('007',7)['text'])

    def test_opening_candidate_files_retired(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('qy6_7i9_tgb','8ht_nw8_3lv','is3_9h6_hq6','5dl_6xj_187','okz_ham_pdc','8h7_82d_vjr','ld0_ysw_559','dgh_7wa_4c5'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

    def test_remaining_campaign_people_use_each_shared_event(self):
        p=self.paragraph('094',9)
        for surface,pid in [('龍且','sr6_5zr_1f3'),('彭越','9qt_orl_5f2'),('華無傷','bbt_vs5_5ka'),('田解','sac_peq_v1p'),('田光','pew_ob7_n0k'),('田既','o4h_qq4_taj'),('田吸','kfh_9sk_v4e')]:
            self.assertEqual(self.ids(p,surface),{pid})
        self.assertEqual(self.ids(self.paragraph('094',7),'陳餘'),{'rx0_vif_1xq'})
        self.assertEqual(self.ids(self.paragraph('094',10),'酈商'),{'xny_prn_zyi'})
        self.assertEqual(self.ids(self.paragraph('054',5),'田廣'),{'0hs_fg6_1qj_B'})
        self.assertEqual(self.ids(self.paragraph('095',25),'華毋傷'),{'bbt_vs5_5ka'})

    def test_qi_minister_is_not_yan_assassin_and_tian_guang_keeps_father(self):
        all_mentions=[m for p in json.loads((ROOT/'corpus/shiji/086.json').read_text())['paragraphs'] for m in p['mentions']]
        self.assertTrue(any(m.get('person_id')=='z0v_ish_b9u' and m['surface']=='田光' for m in all_mentions))
        self.assertFalse(any(m.get('person_id')=='pew_ob7_n0k' for m in all_mentions))
        people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        self.assertEqual(people['0hs_fg6_1qj_B']['family_path']['parent_person_id'],'0hs_fg6_1qj')
        self.assertIn('立田榮子廣為齊王',self.paragraph('094',8)['text'])

    def test_remaining_campaign_candidate_files_retired(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('ueq_svp_knr','y6z_6wd_ezf','qfk_7zb_jtn','zip_jr2_0be','27w_87k_66k','ecl_t01_cwr','14d_o9y_nd0','6mp_d5b_nax','hr1_cou_3hm','nnz_8gm_bdk','dnb_rcf_15u','k96_xfs_8qz','ybx_5gn_njg'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())
