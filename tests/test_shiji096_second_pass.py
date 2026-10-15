# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def para(n,i):return next(p for p in read(f'corpus/shiji/{n:03}.json')['paragraphs'] if p['id'].endswith(f':p{i:03}'))
def ids(p,s):return {m['person_id'] for m in p['mentions'] if m['surface']==s and m['kind']=='person'}

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
        self.assertEqual(ids(para(96,10),'曹窋'),{'37j_16p_7n8_A'})
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

class ZhangCourtIdentityTests(unittest.TestCase):
    def test_attempted_prince_change_does_not_make_ruyi_crown_prince(self):
        p=para(96,5)
        self.assertEqual(ids(p,'太子'),{'yqp_nlb_p1p_AA'})
        self.assertEqual(ids(p,'如意'),{'yqp_nlb_p1p_AH'})
        self.assertEqual(ids(para(96,16),'孝惠'),{'yqp_nlb_p1p_AA'})
        self.assertEqual(ids(para(54,15),'惠帝'),{'yqp_nlb_p1p_AA'})
        self.assertIn('而立戚姬子如意為太子',p['text'])
        holdings=read('corpus/shiji/096-titles.json')['holdings']
        self.assertFalse(any(h['person_id']=='yqp_nlb_p1p_AH' and h['title']=='太子' for h in holdings))

    def test_family_and_mother_references_follow_distinct_people(self):
        self.assertEqual(ids(para(96,5),'戚姬'),{'thg_zvp_v5y'})
        self.assertEqual(ids(para(96,6),'戚夫人'),{'thg_zvp_v5y'})
        self.assertEqual(ids(para(96,8),'戚氏'),{'thg_zvp_v5y'})
        self.assertEqual(ids(para(96,8),'高后'),{'i30_mjq_6q8_A'})
        b=read('exports/persons/yqp_nlb_p1p_AH.json')
        self.assertTrue(any(a['subject_person_id']=='yqp_nlb_p1p_AH' and a['predicate']=='mother' and a['object_person_id']=='thg_zvp_v5y' for a in b['relations']))

    def test_new_king_and_xiangji_mentions_have_exact_boundaries(self):
        for i,start,surface,pid in [(8,18,'王','yqp_nlb_p1p_AH'),(10,para(96,10)['text'].index('項籍'),'項籍','ob7_g6i_7pp')]:
            p=para(96,i);m=next(m for m in p['mentions'] if m['start']==start)
            self.assertEqual((m['surface'],m['end'],m['person_id']),(surface,start+len(surface),pid))
            self.assertEqual(p['text'][m['start']:m['end']],surface)
        self.assertIn('周昌令王稱疾不行',para(96,8)['text'])

    def test_court_officers_and_same_name_clerk_remain_distinct(self):
        self.assertEqual(ids(para(96,5),'留侯'),{'ea5_zvr_hlp'})
        self.assertEqual(ids(para(96,7),'陳豨'),{'1xx_s1v_svn'})
        self.assertEqual(ids(para(96,11),'絳侯'),{'koy_6jg_gcc'})
        self.assertEqual(ids(para(96,20),'陳平'),{'i3f_9l9_g53'})
        self.assertEqual(ids(para(96,23),'陳平'),{'rwg_skp_gbq'})
        self.assertEqual(ids(para(96,10),'曹窋'),{'37j_16p_7n8_A'})
        self.assertEqual(ids(para(9,27),'平陽侯窋'),{'37j_16p_7n8_A'})
        self.assertEqual(ids(para(57,8),'呂祿'),{'561_608_i0z'})

    def test_current_emperor_scope_does_not_override_later_emperors(self):
        self.assertEqual(ids(para(96,19),'今上'),{'yqp_nlb_p1p_ACAA'})
        self.assertEqual(ids(para(96,21),'孝武'),{'yqp_nlb_p1p_ACAA'})
        self.assertNotIn('yqp_nlb_p1p_ACAA',ids(para(96,24),'孝宣帝'))
        self.assertNotIn('yqp_nlb_p1p_ACAA',ids(para(96,27),'孝元帝'))

    def test_sixteen_court_candidates_are_retired(self):
        people={p['id'] for p in read('registry/persons.json')['persons']}
        for pid in ['t5e_f83_p7l','srh_4ts_334','5f6_5r4_eni','9t0_psw_zf3','6a5_ca8_2a8','7p1_uko_gaz','xg3_url_fyn','jej_8s3_01z','ht8_t4d_vbc','pdd_ww5_imn','yzr_p69_1y0','pyt_ft7_8h4','865_tu4_a4b','9ul_wlf_q1k','vz1_n5y_mng','rhz_4fw_u1u']:
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

    def test_unenacted_title_is_exported_separately_from_actual_holdings(self):
        c=read('corpus/shiji/096.json');p=para(96,5)
        m=next(m for m in p['mentions'] if m['id']=='c-shiji-096-zhang:m005-0102')
        self.assertEqual((m['surface'],m['kind'],m['person_id']),('太子','unresolved',None))
        proposal=c['annotation']['title_proposals'][0]
        b=read('exports/persons/yqp_nlb_p1p_AH.json')
        self.assertIn(proposal,b['title_proposals'])
        self.assertEqual((proposal['person_id'],proposal['outcome']),('yqp_nlb_p1p_AH','not_enacted'))
        hui=read('exports/persons/yqp_nlb_p1p_AA.json')
        self.assertNotIn(m['id'],{x['id'] for x in hui['mentions']})
        from scripts.validate_corpus import title_proposal_errors
        self.assertEqual(title_proposal_errors(proposal,c,{'yqp_nlb_p1p_AH'}),[])

    def test_title_proposal_rejects_wrong_holder_person_role_and_missing_quote_anchor(self):
        import copy
        from scripts.validate_corpus import title_proposal_errors
        c=read('corpus/shiji/096.json');proposal=c['annotation']['title_proposals'][0]
        for changes in [{'person_id':'yqp_nlb_p1p_AA'}, {'outcome':'enacted'}, {'role_mention_id':'c-shiji-096-zhang:m005-0091'}]:
            broken=dict(proposal,**changes)
            self.assertTrue(title_proposal_errors(broken,c,{'yqp_nlb_p1p_AA','yqp_nlb_p1p_AH'}))
        broken=copy.deepcopy(proposal);broken['evidence'][0]['quote']='太子'
        self.assertTrue(title_proposal_errors(broken,c,{'yqp_nlb_p1p_AH'}))
