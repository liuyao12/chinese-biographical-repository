# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def para(n,i):return next(p for p in read(f'corpus/shiji/{n:03}.json')['paragraphs'] if p['id'].endswith(f':p{i:03}'))
def ids(p,s):return {m['person_id'] for m in p['mentions'] if m['surface']==s}

class ZhangOpeningIdentityTests(unittest.TestCase):
    def test_opening_campaigns_reconcile_people_not_events(self):
        p=para(96,1)
        for surface,pid in [('淮陰侯','ofc_8ei_jb7'),('陳餘','rx0_vif_1xq'),('張耳','agx_sqm_4ou'),('耳','agx_sqm_4ou'),('趙王敖','agx_sqm_4ou_A'),('臧荼','xaa_ewn_4ro')]:
            self.assertEqual(ids(p,surface),{pid})
        self.assertIn('蒼得陳餘',p['text'])
        self.assertIn('斬陳餘泜水上',para(89,23)['text'])
        self.assertIn('斬成安君泜水上',para(92,10)['text'])

    def test_retrospective_huaiyin_title_has_no_campaign_grant_date(self):
        h=next(x for x in read('corpus/shiji/096-titles.json')['holdings'] if x['id']=='th-shiji096-105')
        self.assertEqual((h['person_id'],h['mode']),('ofc_8ei_jb7','attestation'))
        self.assertEqual(h['effective_period']['start']['status'],'unknown')
        self.assertIsNone(h['effective_period']['start']['date_expression'])
        self.assertIn('以爲淮陰侯',para(92,23)['text'])
        self.assertEqual(ids(para(95,20),'韓信'),{'l9e_fbr_36a_*A'})

    def test_xiao_cao_short_forms_follow_han_court_context(self):
        self.assertEqual(ids(para(96,2),'蕭何'),{'xd8_uww_5ok'})
        for i in [4,5,20]:
            self.assertEqual(ids(para(96,i),'蕭'),{'xd8_uww_5ok'})
            self.assertEqual(ids(para(96,i),'曹'),{'37j_16p_7n8'})
        self.assertEqual(ids(para(96,10),'曹窋'),{'pyt_ft7_8h4'})
        self.assertEqual(ids(para(96,23),'陳平'),{'rwg_skp_gbq'})

    def test_zhangao_inherits_evidenced_father_and_not_liuchang_paternity(self):
        self.assertEqual(ids(para(118,1),'趙王張敖'),{'agx_sqm_4ou_A'})
        bundle=read('exports/persons/agx_sqm_4ou_A.json')
        fathers=[a for a in bundle['relations'] if a['subject_person_id']=='agx_sqm_4ou_A' and a['predicate']=='father']
        self.assertTrue(any(a['object_person_id']=='agx_sqm_4ou' and any('子敖嗣立' in e['quote'] for e in a['evidence']) for a in fathers))
        self.assertFalse(any(a['predicate']=='father' and a['subject_person_id']=='yqp_nlb_p1p_AF' and a['object_person_id']=='agx_sqm_4ou_A' for a in bundle['relations']))

    def test_huainan_successor_is_not_predecessor_or_unnamed_father(self):
        p=para(96,2)
        self.assertEqual(ids(p,'黥布'),{'zxd_afr_2xg'})
        self.assertEqual(ids(p,'皇子長'),{'yqp_nlb_p1p_AF'})
        self.assertEqual(ids(para(118,2),'淮南王黥布'),{'zxd_afr_2xg'})
        a=read('corpus/shiji/096-assertions.json')['assertions']
        father=next(x for x in a if x['subject_person_id']=='68u_x4k_2k4' and x['predicate']=='father')
        self.assertEqual(father['object_person_id'],'796_nkw_0jz')
        self.assertNotEqual(father['object_person_id'],'5do_703_rfz')

    def test_twelve_retired_candidates_have_no_registry_or_export(self):
        people={x['id'] for x in read('registry/persons.json')['persons']}
        for old in ['r6y_t2l_ntc','65r_40m_v04','shk_1za_du3','41m_4yl_j39','zs9_uq9_odj','kzp_s69_eh7','15d_u8k_luo','9dx_y3b_try','ifc_1dx_zrh','e4c_pkg_cq7','7o5_xwk_v9c','z0c_6ka_3bd']:
            self.assertNotIn(old,people)
            self.assertFalse((ROOT/f'exports/persons/{old}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{old}.json').exists())
