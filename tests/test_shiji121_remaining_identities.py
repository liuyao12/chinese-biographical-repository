# coding: utf-8
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(rel):return json.loads((ROOT/rel).read_text())
def fixture():return read('tests/fixtures/shiji121-remaining-identities.json')
class RemainingSourceTests(unittest.TestCase):
    def test_all_forty_five_markers_and_original_text(self):
        f=fixture();self.assertEqual(len(f['mentions']),45);self.assertEqual(len(f['mapping']),10)
        for row in f['mentions']:
            p=next(p for p in read(row['path'])['paragraphs'] if p['id']==row['paragraph_id'])
            self.assertEqual(p['text'],row['text']);self.assertEqual(next(m for m in p['mentions'] if m['id']==row['marker']['id']),row['marker'])
    def test_wang_zang_retains_four_chapter_contexts(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']};e=people['jh5_a7h_pvv']['evidence']
        self.assertEqual({x['chapter_id'] for x in e},{'c-shiji-012-wudi','c-shiji-103-wanshi','c-shiji-107-weiqi','c-shiji-121-rulin'})
        self.assertIn('bt2_5iy_rhq',people)
        self.assertTrue(any(a['surface']=='太常臧' for a in people['bt2_5iy_rhq']['aliases']))
    def test_homonymous_kings_and_tang_wu_stay_distinct(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        for pid in ['jps_m3k_hu4','fd5_uxa_0c9','yqp_nlb_p1p_AE','yqp_nlb_p1p_AF','tpz_x3m_e0h','y4i_pjk_4gn_AA','y97_huh_vuz_AAAAAAAAAAAAABAAAAAAA']:self.assertIn(pid,people)
        p=next(p for p in read('corpus/shiji/121.json')['paragraphs'] if p['id'].endswith(':p010'))
        pairs=[m for m in p['mentions'] if m['surface'] in ['湯','武']]
        self.assertTrue(pairs)
        for m in pairs:self.assertEqual(m['person_id'],'tpz_x3m_e0h' if m['surface']=='湯' else 'y4i_pjk_4gn_AA')
    def test_ten_decisions_keep_source_context_and_review_limits(self):
        ds=[d for d in read('corpus/shiji/121-identities.json')['decisions'] if d['id'].startswith('d-shiji121-remaining-')]
        self.assertEqual(len(ds),10)
        for d in ds:self.assertFalse(d['human_reviewed']);self.assertIsNone(d['model']);self.assertGreaterEqual(len(d['chapter_ids']),2)
        wang=next(d for d in ds if d['person_id']=='jh5_a7h_pvv')
        self.assertTrue({'c-shiji-012-wudi','c-shiji-103-wanshi','c-shiji-107-weiqi','c-shiji-121-rulin'}.issubset(wang['chapter_ids']))
class RemainingPublicTests(unittest.TestCase):
    def test_retired_public_ids_are_absent(self):
        for old,new in fixture()['mapping'].items():
            for folder in ['exports/persons','data/corpus/profiles']:
                self.assertFalse((ROOT/folder/(old+'.json')).exists());self.assertTrue((ROOT/folder/(new+'.json')).exists())
    def test_canonical_profiles_keep_rulin_and_wang_contexts(self):
        for new in fixture()['mapping'].values():
            p=read('data/corpus/profiles/'+new+'.json');self.assertIn('c-shiji-121-rulin',{o['chapter_id'] for o in p['occurrences']})
        p=read('data/corpus/profiles/jh5_a7h_pvv.json');self.assertTrue({'c-shiji-012-wudi','c-shiji-103-wanshi','c-shiji-107-weiqi','c-shiji-121-rulin'}.issubset({o['chapter_id'] for o in p['occurrences']}))
if __name__=='__main__':unittest.main()
