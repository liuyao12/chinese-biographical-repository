import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

class QuJiaSecondPassTests(unittest.TestCase):
    def chapter(self):
        return json.loads((ROOT / 'corpus/shiji/084.json').read_text())

    def test_named_quyuan_and_parallel_release_event(self):
        c = self.chapter()
        self.assertEqual({m['person_id'] for m in c['paragraphs'][0]['mentions'] if m['surface'] in ('屈原','平')}, {'4dm_2h1_9je'})
        p = c['paragraphs'][4]
        expected = {'屈平':'4dm_2h1_9je','張儀':'uq6_74z_vtv','靳尚':'puc_9qz_obg','鄭袖':'ify_oqo_7fy'}
        for surface,pid in expected.items():
            self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']==surface},{pid})
        self.assertIn('何不殺張儀',p['text'])

    def test_unnamed_shangguan_is_not_jinshang(self):
        p = self.chapter()['paragraphs'][1]
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']=='上官大夫'}, {'xwc_7eh_kj1'})
        self.assertNotIn('puc_9qz_obg',{m['person_id'] for m in p['mentions']})

    def test_qin_kings_and_chu_advice_disagreement_are_preserved(self):
        c = self.chapter()
        self.assertEqual({m['person_id'] for m in c['paragraphs'][3]['mentions'] if m['surface']=='惠王'}, {'y97_huh_vuz_AAAAAAAAAAAAABAAAAAA'})
        p = c['paragraphs'][6]
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface']=='秦昭王'}, {'ao3_0fy_d45'})
        self.assertIn('屈平曰',p['text'])
        parallel=json.loads((ROOT/'corpus/shiji/040.json').read_text())['paragraphs'][77]
        self.assertIn('昭雎曰',parallel['text'])
        self.assertEqual({m['person_id'] for m in c['paragraphs'][7]['mentions'] if m['surface']=='頃襄王'}, {'pgu_6kt_nz1'})

    def test_qugai_spellings_share_identity_without_rewriting_fate(self):
        from scripts.person_bundle import bundle
        result=bundle('c38_dzq_0o4', include_provisional=True)
        passages={p['id']:p for p in result['passages']}
        self.assertIn('虜我大將軍屈匄',passages['c-shiji-040-chu:p072']['text'])
        self.assertIn('虜楚將屈丐',passages['c-shiji-084-qujia:p004']['text'])
        self.assertIn('殺屈丐',passages['c-shiji-070-zhang:p022']['text'])
        for pid,surface in [('c-shiji-040-chu:p072','屈匄'),('c-shiji-084-qujia:p004','楚將屈丐')]:
            self.assertEqual({m['person_id'] for m in passages[pid]['mentions'] if m['surface']==surface},{'c38_dzq_0o4'})
        death=next(e for e in result['life_events'] if e['id']=='le-shiji070-002')
        self.assertEqual(death['source_term'],'殺屈丐')
        self.assertNotIn('normalized_date',death)

    def test_huai_release_parallel_does_not_identify_zhengxiu_child(self):
        c=json.loads((ROOT/'corpus/shiji/070.json').read_text())
        p=c['paragraphs'][22]
        self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] in ('楚懷王','楚王','懷王')},{'c2w_s7g_en0'})
        self.assertIn('子母俱遷江南',p['text'])
        relations=json.loads((ROOT/'corpus/shiji/084-assertions.json').read_text())['assertions']
        self.assertFalse(any(a['predicate']=='mother' and a.get('object_person_id')=='ify_oqo_7fy' for a in relations))
