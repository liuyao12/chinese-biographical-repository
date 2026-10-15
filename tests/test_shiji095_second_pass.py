# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class FanLiCourtIdentityTests(unittest.TestCase):
    def paragraph(self,number,index):
        c=json.loads((ROOT/f'corpus/shiji/{number}.json').read_text())
        return next(p for p in c['paragraphs'] if p['id'].endswith(':p%03d'%index))
    def ids(self,p,surface):
        return {m['person_id'] for m in p['mentions'] if m['surface']==surface}

    def test_hongmen_and_court_people_follow_shared_events(self):
        p=self.paragraph('095',3)
        for name,pid in [('項伯','cyi_wjz_uxt'),('項莊','nsa_bp5_1dk'),('張良','ea5_zvr_hlp')]:self.assertEqual(self.ids(p,name),{pid})
        p=self.paragraph('095',9)
        for name,pid in [('陳平','i3f_9l9_g53'),('絳侯','koy_6jg_gcc'),('呂后','i30_mjq_6q8_A')]:self.assertEqual(self.ids(p,name),{pid})
        self.assertEqual(self.ids(self.paragraph('095',8),'趙高'),{'0xx_ozc_454'})
        self.assertIn('人有惡噲黨於呂氏',p['text'])
        self.assertIn('欲以兵盡誅滅戚氏',p['text'])

    def test_two_hanxin_people_switch_within_the_same_paragraph(self):
        p=self.paragraph('095',6);marks={m['start']:m for m in p['mentions']}
        self.assertEqual(marks[41]['person_id'],'ofc_8ei_jb7')
        self.assertEqual(marks[98]['person_id'],'l9e_fbr_36a_*A')
        self.assertEqual(marks[203]['person_id'],'l9e_fbr_36a_*A')
        self.assertEqual(marks[215]['person_id'],'l9e_fbr_36a_*A')
        p=self.paragraph('095',20)
        self.assertEqual(self.ids(p,'楚王信'),{'ofc_8ei_jb7'})
        self.assertEqual(self.ids(p,'韓信'),{'l9e_fbr_36a_*A'})
        self.assertEqual(self.ids(self.paragraph('095',25),'韓信'),{'ofc_8ei_jb7'})
        self.assertEqual(self.ids(self.paragraph('095',29),'韓信'),{'l9e_fbr_36a_*A'})

    def test_lvxu_spelling_and_mother_spouse_evidence_survive(self):
        self.assertEqual(self.ids(self.paragraph('095',7),'呂須'),{'nix_7ug_wxv'})
        self.assertEqual(self.ids(self.paragraph('056',15),'呂嬃'),{'nix_7ug_wxv'})
        rows=json.loads((ROOT/'corpus/shiji/095-assertions.json').read_text())['assertions']
        self.assertTrue(any(a['subject_person_id']=='nix_7ug_wxv' and a['predicate']=='spouse' and a['object_person_id']=='b1r_inb_fts' for a in rows))
        self.assertTrue(any(a['subject_person_id']=='b1r_inb_fts_B' and a['predicate']=='mother' and a['object_person_id']=='nix_7ug_wxv' for a in rows))
        self.assertIn('呂須',self.paragraph('095',10)['text'])
        self.assertIn('呂嬃之夫',self.paragraph('056',15)['text'])
        self.assertIn('斬陳豨將侯敞、王黃',self.paragraph('093',17)['text'])
        self.assertIn('皆生得',self.paragraph('093',17)['text'])

    def test_reconciled_candidates_are_retired(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('x0e_ivo_wsa','91e_89k_8p8','k7t_lyq_qf2','j4e_gam_0tl','39e_wj9_6m0','s8n_dgg_60b','4k0_mri_buk','mrj_1jl_2tk','vqw_ylp_5mq','664_wah_z4z','m5o_zsd_7jg','jyd_5a2_cil','z6m_hs4_r4a','2u6_7bk_902','37x_h50_3ls','ht1_kdz_izj','syo_21l_kzx','frp_bsu_g43'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())
            self.assertFalse((ROOT/f'data/corpus/profiles/{pid}.json').exists())

class FanLiScopedRoyalIdentityTests(unittest.TestCase):
    paragraph=FanLiCourtIdentityTests.paragraph
    ids=FanLiCourtIdentityTests.ids
    def test_royal_names_follow_the_event_epoch(self):
        self.assertEqual(self.ids(self.paragraph('095',15),'王'),{'yqp_nlb_p1p_AEA'})
        self.assertEqual(self.ids(self.paragraph('095',21),'東牟侯'),{'yqp_nlb_p1p_ABC'})
        self.assertEqual(self.ids(self.paragraph('095',33),'濟北王'),{'yqp_nlb_p1p_ABC'})
        self.assertEqual(self.ids(self.paragraph('095',21),'少帝'),{'zht_ze7_m2d'})
        self.assertEqual(self.ids(self.paragraph('052',36),'少帝'),{'zht_ze7_m2d'})
        self.assertEqual(self.ids(self.paragraph('095',32),'齊王'),{'yqp_nlb_p1p_ABA'})
        self.assertEqual(self.ids(self.paragraph('095',32),'呂祿'),{'561_608_i0z'})

    def test_pingyuan_is_zanger_with_commentarial_identification(self):
        self.assertEqual(self.ids(self.paragraph('095',15),'平原君'),{'6ks_x4x_dbf_*A'})
        ds=json.loads((ROOT/'corpus/shiji/095-equivalences.json').read_text())['decisions']
        d=next(x for x in ds if x['id']=='eq-shiji095-royal-pingyuan-zanger')
        self.assertEqual(d['references'][0]['quote'],'景帝王皇后母臧兒也。')
        self.assertFalse(d['references'][0]['image_verified'])
        self.assertIn('不據此把授號時間提前',d['rationale'])

    def test_person_boundaries_exclude_verbs_and_split_grandson(self):
        p=self.paragraph('095',15);m=next(m for m in p['mentions'] if m['id'].endswith('m015-0050'))
        self.assertEqual((m['surface'],m['start'],m['end']),('王',50,51))
        p=self.paragraph('095',21);m=next(m for m in p['mentions'] if m['id'].endswith('m021-0152'))
        self.assertEqual((m['surface'],m['start'],m['end']),('賜',152,153))
        p=self.paragraph('095',33)
        self.assertEqual(self.ids(p,'灌嬰'),{'sj9_pfu_fwh'})
        self.assertEqual(self.ids(p,'賢'),{'sj9_pfu_fwh_*A'})
        self.assertFalse(any(m['start']<=120<m['end'] for m in p['mentions']))
        person=json.loads((ROOT/'exports/persons/sj9_pfu_fwh_*A.json').read_text())
        self.assertNotIn('灌嬰孫賢',[a['surface'] for a in next(x for x in person['persons'] if x['id']=='sj9_pfu_fwh_*A')['aliases']])
        r=json.loads((ROOT/'registry/persons.json').read_text())['persons']
        x=next(x for x in r if x['id']=='sj9_pfu_fwh_*A')
        self.assertEqual(x['family_path']['generation_distance'],2)
        self.assertIsNone(x['family_path']['parent_person_id'])

class FanLiMilitaryIdentityTests(unittest.TestCase):
    paragraph=FanLiCourtIdentityTests.paragraph
    ids=FanLiCourtIdentityTests.ids

    def test_shared_campaigns_link_commanders_across_biographies(self):
        expected={'司馬夷':'m8o_g61_go9','章邯':'4jv_qte_5p4','李由':'49g_7az_e4i_A','趙賁':'bwv_p3h_q1j','楊熊':'v4m_7yp_xr3','章平':'fs1_3m9_rj3','齮':'4oq_2zh_bd2','王武':'qxu_jqe_evi','程處':'k9m_d4o_f34'}
        pids={}
        for i in (2,5,17,22,24):
            for m in self.paragraph('095',i)['mentions']:
                if m['surface'] in expected:pids.setdefault(m['surface'],set()).add(m['person_id'])
        self.assertEqual(pids,{k:{v} for k,v in expected.items()})
        self.assertEqual(self.ids(self.paragraph('054',3),'趙賁'),{'bwv_p3h_q1j'})
        self.assertEqual(self.ids(self.paragraph('057',3),'章平'),{'fs1_3m9_rj3'})
        self.assertEqual(self.ids(self.paragraph('098',6),'王武'),{'qxu_jqe_evi'})

    def test_liyou_keeps_lisi_father_branch_and_hanshu_reference(self):
        r=json.loads((ROOT/'registry/persons.json').read_text())['persons']
        p=next(x for x in r if x['id']=='49g_7az_e4i_A')
        self.assertEqual(p['family_path']['parent_person_id'],'49g_7az_e4i')
        self.assertEqual(self.ids(self.paragraph('007',7),'李由'),{'49g_7az_e4i_A'})
        self.assertEqual(self.ids(self.paragraph('048',5),'李由'),{'49g_7az_e4i_A'})
        ds=json.loads((ROOT/'corpus/shiji/095-equivalences.json').read_text())['decisions']
        d=next(x for x in ds if x['id']=='eq-shiji095-military-liyou')
        self.assertIn('斬三川守李由',d['references'][0]['quote'])
        self.assertIn('oldid=2647884',d['references'][0]['url'])

    def test_zhangping_commentarial_son_does_not_override_received_brother(self):
        rows=json.loads((ROOT/'corpus/shiji/008-assertions.json').read_text())['assertions']
        a=next(a for a in rows if a['id']=='a-shiji008-008')
        self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('fs1_3m9_rj3','brother','4jv_qte_5p4'))
        ds=json.loads((ROOT/'corpus/shiji/095-equivalences.json').read_text())['decisions']
        d=next(x for x in ds if x['id']=='eq-shiji095-military-zhangping')
        self.assertEqual(d['references'][0]['quote'],'章平即章邯子也。')
        self.assertFalse(d['references'][0]['image_verified'])
        self.assertIn('欲自剄',self.paragraph('008',20)['text'])

    def test_retired_military_candidates_are_removed_after_migration(self):
        ds=json.loads((ROOT/'corpus/shiji/095-equivalences.json').read_text())['decisions']
        military=[d for d in ds if d['id'].startswith('eq-shiji095-military-')]
        self.assertEqual(len(military),9)
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ['423_9wn_ew3','7st_a3s_dis','ekn_61g_qaz','lwx_fc0_0ce','452_xfy_50i','5ij_409_sfj','vnb_l2e_06w','3vk_jr4_vnd','6sl_m8t_cxz','92t_lra_3r9']:
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())

class FanLiCrossChapterFamilyTests(unittest.TestCase):
    paragraph=FanLiCourtIdentityTests.paragraph
    ids=FanLiCourtIdentityTests.ids

    def test_royal_and_common_name_actors_follow_named_parallel_events(self):
        for n,s,pid in [(11,'陳勝','pom_ycp_ha5'),(17,'蕭何','xd8_uww_5ok'),(18,'魯元','yqp_nlb_p1p_AI'),(22,'項梁','5xt_rg8_7zs_A'),(12,'鐘離眛','tb2_zhz_mol'),(23,'塞王','o8z_o5j_2e8'),(23,'殷王','ifc_pry_e72'),(34,'曹','37j_16p_7n8')]:
            self.assertEqual(self.ids(self.paragraph('095',n),s),{pid})
        self.assertEqual(self.ids(self.paragraph('095',20),'冒頓'),{'wjt_htu_081_A'})

    def test_baideng_consorte_keeps_other_two_women_distinct(self):
        self.assertEqual(self.ids(self.paragraph('095',20),'閼氏'),{'32k_yr7_5kv'})
        self.assertEqual(self.ids(self.paragraph('056',12),'閼氏'),{'32k_yr7_5kv'})
        self.assertEqual(self.ids(self.paragraph('110',12),'閼氏'),{'32k_yr7_5kv'})
        self.assertEqual(self.ids(self.paragraph('110',6),'後母'),{'vlp_pem_oj3'})
        self.assertEqual(self.ids(self.paragraph('110',7),'閼氏'),{'cjk_ll3_0g9'})
        rows=json.loads((ROOT/'corpus/shiji/110-assertions.json').read_text())['assertions']
        a=next(x for x in rows if x['id']=='a-shiji110-027')
        self.assertEqual((a['subject_person_id'],a['predicate'],a['object_person_id']),('32k_yr7_5kv','spouse','wjt_htu_081_A'))

    def test_pingyang_has_sourced_marriages_mother_and_partial_sister_order(self):
        self.assertEqual(self.ids(self.paragraph('095',21),'平陽公主'),{'921_w24_4mr'})
        self.assertEqual(self.ids(self.paragraph('054',17),'平陽公主'),{'nad_18h_5jc'})
        self.assertEqual(self.ids(self.paragraph('125',4),'平陽公主'),{'ase_y0g_7gy'})
        allrows=[]
        for n in ('049','054','095'):allrows+=json.loads((ROOT/f'corpus/shiji/{n}-assertions.json').read_text())['assertions']
        spouses=set()
        for a in allrows:
            if a['predicate']=='spouse' and 'nad_18h_5jc' in (a['subject_person_id'],a['object_person_id']):spouses.update({a['subject_person_id'],a['object_person_id']}-{'nad_18h_5jc'})
        self.assertEqual(spouses,{'37j_16p_7n8_AAA','5dd_l1c_6g8'})
        mothers=[a for a in allrows if a['id'] in ('a-shiji049-049','a-shiji049-050','a-shiji049-051')]
        self.assertEqual(len(mothers),3)
        self.assertTrue(all(a['object_person_id']=='6d6_eg1_o3a_A' and 'birth_order' not in a['qualifiers'] for a in mothers))
        ordered=[a['qualifiers']['relative_birth_order'] for a in allrows if a['id'] in ('a-shiji049-052','a-shiji049-053')]
        self.assertEqual([(o['older_person_id'],o['younger_person_id']) for o in ordered],[('nad_18h_5jc','nza_w1p_x8f'),('nza_w1p_x8f','0gy_vl6_l9g')])
        self.assertTrue(all(o['older_ordinal'] is None and o['younger_ordinal'] is None for o in ordered))

    def test_luanbu_keeps_existing_son_under_one_root(self):
        self.assertEqual(self.ids(self.paragraph('095',15),'欒布'),{'jx9_cov_qe0'})
        self.assertEqual(self.ids(self.paragraph('010',27),'欒布'),{'jx9_cov_qe0'})
        r=json.loads((ROOT/'registry/persons.json').read_text())['persons']
        son=next(x for x in r if x['id']=='jx9_cov_qe0_A')
        self.assertEqual(son['family_path']['parent_person_id'],'jx9_cov_qe0')

    def test_family_link_candidates_retired_after_all_references_move(self):
        people={p['id'] for p in json.loads((ROOT/'registry/persons.json').read_text())['persons']}
        for pid in ('kki_4ee_3i7','1aa_yn3_kv1','qdl_8tt_r4v','so1_ycw_xkv','g0p_ahe_0bb','73j_rq4_ugv','e4t_vcw_lrt'):
            self.assertNotIn(pid,people)
            self.assertFalse((ROOT/f'exports/persons/{pid}.json').exists())


    def test_pingyang_uncertainty_and_hanshu_reference_reach_person_api(self):
        b=json.loads((ROOT/'exports/persons/921_w24_4mr.json').read_text())
        c=next(c for c in b['unresolved_identity_cases'] if c['id']=='ic-shiji095-pingyang-princesses')
        self.assertEqual(set(c['candidate_person_ids']),{'921_w24_4mr','nad_18h_5jc','ase_y0g_7gy'})
        self.assertIn('號孫公主',c['references'][0]['quote'])
        self.assertEqual(b['person_ids'],['921_w24_4mr'])
        p=json.loads((ROOT/'data/corpus/profiles/921_w24_4mr.json').read_text())
        self.assertEqual(p['unresolved_identity_cases'][0]['candidate_person_ids'],c['candidate_person_ids'])
