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
