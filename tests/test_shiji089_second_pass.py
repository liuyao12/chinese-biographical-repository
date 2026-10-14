# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class ZhangerIdentityTests(unittest.TestCase):
    def paragraph(self, number, ending):
        data = json.loads((ROOT / f'corpus/shiji/{number}.json').read_text())
        return next(p for p in data['paragraphs'] if p['id'].endswith(':'+ending))
    def test_jingxing_hanxin_identity_preserves_capture_death_difference(self):
        local=self.paragraph('089','p023'); parallel=self.paragraph('092','p010')
        ids={m['person_id'] for p in [local,parallel] for m in p['mentions'] if m['surface']=='韓信'}
        self.assertEqual(ids,{'ofc_8ei_jb7'})
        self.assertIn('追殺趙王歇襄國',local['text'])
        self.assertIn('禽趙王歇',parallel['text'])
    def test_wuji_glyph_and_jizha_title_are_not_rewritten(self):
        p=self.paragraph('089','p001')
        self.assertTrue(any(m['surface']=='魏公子毋忌' and m['person_id']=='h8u_hld_5su' for m in p['mentions']))
        p=self.paragraph('089','p030')
        self.assertTrue(any(m['surface']=='延陵季子' and m['person_id']=='5dm_e40_rqh_AAAAAAAAAAAAAAAAAAD' for m in p['mentions']))
        self.assertIn('大伯',p['text'])
        self.assertIn('季札封於延陵，故號曰延陵季子',self.paragraph('031','p008')['text'])
    def test_deaths_exclude_substitute_and_unassigned_group_suicides(self):
        d=json.loads((ROOT/'corpus/shiji/089-life-events.json').read_text())['events']
        ear=next(e for e in d if e['person_id']=='agx_sqm_4ou')
        self.assertEqual(ear['source_term'],'張耳薨')
        self.assertEqual(ear['date_expression'],'漢五年')
        self.assertEqual(ear['normalized_date']['era_year'],202)
        self.assertFalse(any(e['person_id']=='ull_jgp_wdx' for e in d))
        self.assertEqual(next(e for e in d if e['person_id']=='2t1_1bj_ewv')['source_term'],'乃仰絶骯，遂死')
    def test_origin_residence_and_death_place_are_separate(self):
        d=json.loads((ROOT/'corpus/shiji/089-addresses.json').read_text())['assertions']
        self.assertTrue(any(e['person_id']=='agx_sqm_4ou' and e['relation']=='biographical_origin' and e['place']['source_name']=='大梁' for e in d))
        self.assertTrue(any(e['person_id']=='agx_sqm_4ou' and e['relation']=='residence' and e['place']['source_name']=='外黃' for e in d))
        self.assertFalse(any(e['relation']=='birth_place' or e['place']['source_name']=='趙苦陘' for e in d))
    def test_posthumous_name_and_gender_scoped_order_keep_unknowns(self):
        d=json.loads((ROOT/'corpus/shiji/089-titles.json').read_text())['holdings']
        h=next(h for h in d if h['id']=='th-shiji089-026')
        self.assertEqual(h['mode'],'posthumous_naming')
        self.assertIsNone(h['effective_period']['start']['date_expression'])
        a=json.loads((ROOT/'corpus/shiji/089-assertions.json').read_text())['assertions']
        order=next(x for x in a if x['id']=='a-shiji089-006')['qualifiers']['birth_order']
        self.assertEqual((order['ordinal'],order['scope']),(1,'daughters_of_parent'))
        order=next(x for x in a if x['id']=='a-shiji089-005')['qualifiers']['relative_birth_order']
        self.assertEqual(order['older_person_id'],'uvj_ezk_crm')
        self.assertIsNone(order['older_ordinal']);self.assertIsNone(order['younger_ordinal'])
    def test_luyuan_posthumous_ao_is_separate_from_yan(self):
        p=self.paragraph('009','p015')
        self.assertTrue(any(m['surface']=='魯元王' and m['person_id']=='agx_sqm_4ou_A' for m in p['mentions']))
        self.assertTrue(any(m['surface']=='子偃' and m['person_id']=='agx_sqm_4ou_AA' for m in p['mentions']))
        self.assertIn('敖賜謚為魯元王',p['text'])
    def test_children_with_reversed_enumeration_keep_same_identity(self):
        a=self.paragraph('009','p019');b=self.paragraph('089','p029')
        for p in [a,b]:
            self.assertTrue(any(m['surface']=='壽' and m['person_id']=='agx_sqm_4ou_AB' for m in p['mentions']))
            self.assertTrue(any(m['surface']=='侈' and m['person_id']=='agx_sqm_4ou_AC' for m in p['mentions']))
        self.assertIn('新都侯',a['text']);self.assertIn('信都侯',b['text']);self.assertIn('信諸侯',b['text'])
