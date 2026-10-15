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
