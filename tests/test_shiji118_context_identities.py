# coding: utf-8
import json
import unittest
from pathlib import Path
from scripts.consolidate_person_ids import reference_files
ROOT=Path(__file__).resolve().parents[1]
RETIRED = {'3rn_zwc_d5j': 'oho_r3f_c6y', 'a8k_u91_d8m': 'ddb_l4j_4j2', 'l6h_c2o_giv': 'y4i_pjk_4gn_AD', 'wkq_pb7_afj': 'y4i_pjk_4gn_AB', 'won_vq8_gwj': 'y4i_pjk_4gn_AC', 'koo_4b5_1jm': 'yqp_nlb_p1p_AA', 'wef_drj_j44': 'yqp_nlb_p1p_AC', 'f6m_8uv_uww': 'yqp_nlb_p1p_ABFA', 'amr_ua3_4f4': 'yqp_nlb_p1p_ACA', 'nds_eog_ibo': 'yqp_nlb_p1p_ACAA', '9dr_4ei_3dx': '7mz_d13_9ka_A', 'iei_xyz_ug6': '6d6_eg1_o3a_A', 'a0l_q87_lrt': 'g9h_5ih_ug1_A', 'td8_hn8_05z': '5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA', 'gzq_ays_htq': 'y4i_pjk_4gn_A', 'uc7_aa8_117': 'k2p_5ol_dwh_AA', 'b07_lt3_42x': 'ao3_0fy_d45_AAA', 'yen_v2i_ohj': 'bvb_d1z_fd0', 'xzf_o56_oi3': 'pom_ycp_ha5', '6x0_cwt_92g': 'h2h_z86_a3d', '1yn_q66_ob5': 'yqp_nlb_p1p_CA', '3cu_tas_uzd': 'buv_igi_gpn_A', 'yfa_z4u_ovv': 'lwx_9yq_ad7', '727_fiw_151': 'xtq_oi8_w82', 'bk9_i1s_chb': '5dd_l1c_6g8', 'k7q_ibh_l9h': '4jv_qte_5p4', 's7w_fi5_1wh': 'v4m_7yp_xr3', 'f17_3yr_n21': 'saz_old_5fi', 'zd5_eyz_mxn': '9nc_i02_15v', 'bpp_y9r_t8v': 'yqp_nlb_p1p_ACAF', 'fn8_b63_zph': 'yqp_nlb_p1p_ACAN', 'd1v_by0_yie': '04o_yps_sg0', 'utw_e38_exq': 'xgx_g4a_c28', 'ej5_85e_5xj': 'tmv_5d7_bx2', '6r8_jki_snj': 'xgx_g4a_c28', 'v8g_xyw_4v9': '2t1_1bj_ewv', '2gx_dt8_kun': 'i30_mjq_6q8_A', 'k8q_kv9_k4o': 'yqp_nlb_p1p_AH', '1a9_czu_fzj': 'j32_wtj_khz_A', 'if3_kx7_acc': 'n3t_awm_sp8', '6r8_jki_snj_A': 'xgx_g4a_c28_A'}
class HuainanContextIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people={p['id']:p for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        cls.chapter=json.loads((ROOT/'corpus/shiji/118.json').read_text())
        cls.mentions={m['id'].split(':')[-1]:m for p in cls.chapter['paragraphs']for m in p['mentions']}
    def test_all_reviewed_duplicates_and_dependent_id_retired(self):
        for old,new in RETIRED.items():
            self.assertNotIn(old,self.people)
            self.assertIn(new,self.people)
        for path in reference_files(ROOT):
            text=path.read_text()
            self.assertFalse(any('"'+old+'"'in text for old in RETIRED),str(path))
    def test_zhaojian_son_has_same_root_and_attested_surname(self):
        son=self.people['xgx_g4a_c28_A']
        self.assertEqual(son['label'],'周陽由')
        self.assertEqual(son['family_path']['parent_person_id'],'xgx_g4a_c28')
        self.assertTrue(any(a['surface']=='周陽由'for a in son['aliases']))
        self.assertTrue(any('其父趙兼' in e['quote']for e in son['family_path']['evidence']))
    def test_mengzi_is_attributed_person_not_lu_dukes_wife(self):
        self.assertEqual(self.mentions['m019-1024']['person_id'],'saz_old_5fi')
        self.assertNotEqual(self.mentions['m019-1024']['person_id'],'ux3_la0_38d')
        self.assertEqual(self.people['saz_old_5fi']['label'],'孟軻')
    def test_cross_period_wu_rulers_stay_distinct(self):
        paragraph=next(p for p in self.chapter['paragraphs']if p['id'].endswith(':p019'))
        rulers=[m['person_id']for m in paragraph['mentions']if m['surface']=='吳王']
        self.assertIn('5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA',rulers)
        self.assertIn('yqp_nlb_p1p_CA',rulers)
    def test_louhuan_not_folded_into_warring_states_person(self):
        self.assertEqual(self.mentions['m021-0140']['person_id'],'2nl_q1p_8z0')
        self.assertIn('p41_n3z_dlq',self.people)
    def test_xufu_received_spelling_preserved(self):
        for mid in ['m019-0357','m019-0534']:
            self.assertEqual(self.mentions[mid]['surface'],'徐福')
            self.assertEqual(self.mentions[mid]['person_id'],'9nc_i02_15v')
        self.assertTrue(any(a['surface']=='徐巿'for a in self.people['9nc_i02_15v']['aliases']))
    def test_royal_referents_do_not_assert_hypothetical_accession(self):
        for mid,pid in [('m018-0041','yqp_nlb_p1p_ACAM'),('m018-0047','yqp_nlb_p1p_ACAG'),('m002-0333','yqp_nlb_p1p_ACA')]:
            self.assertEqual(self.mentions[mid]['person_id'],pid)
        self.assertIsNone(self.mentions['m018-0028']['person_id'])
        self.assertIsNone(self.mentions['m018-0097']['person_id'])
        self.assertIn('ixa_izg_wta',self.people)
        data=json.loads((ROOT/'corpus/shiji/118-identities.json').read_text())
        self.assertEqual(data['record_type'],'identity_decision_set')
        royal=[d for d in data['decisions'] if d['id'].startswith('d-shiji118-royal-context-')]
        self.assertEqual(len(royal),3)
        hypothetical=[d for d in royal if d['identification_basis']['hypothetical_accession_not_inferred']]
        self.assertEqual(len(hypothetical),2)
    def test_all_materialized_decisions_have_multiple_source_anchors(self):
        ds=json.loads((ROOT/'corpus/shiji/118-equivalences.json').read_text())['decisions']
        reviewed=[d for d in ds if d['id'].startswith('eq-shiji118-context-')]
        self.assertEqual(len(reviewed),40)
        for d in reviewed:
            self.assertTrue(d['identity_materialized'])
            self.assertFalse(d['human_reviewed'])
            self.assertGreaterEqual(len({m for e in d['evidence']for m in e['mention_ids']}),2)
if __name__=='__main__':unittest.main()
