import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text())

def para(number):
    return read('corpus/shiji/098.json')['paragraphs'][number - 1]

def ids(number, surface):
    return {m['person_id'] for m in para(number)['mentions']
            if m['kind'] == 'person' and m['surface'] == surface}

class FuJinCoreIdentityTests(unittest.TestCase):
    def test_two_hanxins_follow_different_campaigns(self):
        for n, surface in [(2, '淮陰'), (7, '楚王信'), (10, '淮陰侯')]:
            self.assertEqual(ids(n, surface), {'ofc_8ei_jb7'})
        self.assertEqual(ids(8, '韓信'), {'l9e_fbr_36a_*A'})
        self.assertIn('取楚王信', para(7)['text'])
        self.assertIn('攻韓信平城下', para(8)['text'])
        b = read('exports/persons/ofc_8ei_jb7.json')
        self.assertNotIn('l9e_fbr_36a_*A', b['person_ids'])

    def test_short_names_and_titles_resolve_without_adding_surnames_to_text(self):
        for n, surface, pid in [(2, '參', '37j_16p_7n8'),
                                (3, '勃', 'koy_6jg_gcc'),
                                (3, '哙', 'b1r_inb_fts')]:
            self.assertEqual(ids(n, surface), {pid})
        self.assertIn('以相國代丞相哙擊豨', para(3)['text'])
        self.assertEqual(ids(3, '相國'), {'w8j_vnd_rs4'})
        holdings = read('corpus/shiji/098-titles.json')['holdings']
        self.assertEqual(next(h for h in holdings if h['id']=='th-shiji098-016')['person_id'], 'b1r_inb_fts')
        self.assertEqual(next(h for h in holdings if h['id']=='th-shiji098-018')['person_id'], 'w8j_vnd_rs4')

    def test_same_noble_title_does_not_merge_different_subjects(self):
        self.assertEqual(ids(7, '信武侯'), {'7dv_lqp_y4z'})
        self.assertEqual(ids(10, '信武侯'), {'fvm_66f_0k3'})
        self.assertEqual(ids(12, '昌'), {'fvm_66f_0k3_A'})
        self.assertIn('三十一年', para(4)['text'])

    def test_equivalence_evidence_is_queryable_in_each_person_bundle(self):
        eq = read('corpus/shiji/098-equivalences.json')['decisions']
        self.assertEqual(len(eq), 10)
        for decision in eq:
            self.assertTrue(decision['identity_materialized'])
            b = read('exports/persons/'+decision['canonical_person_id']+'.json')
            actual = next(x for x in b['equivalence_decisions'] if x['id']==decision['id'])
            self.assertTrue(any(e['chapter_id']=='c-shiji-098-fujin' for e in actual['evidence']))
            self.assertTrue(all(e['mention_ids'] for e in actual['evidence']))
        self.assertFalse(next(b for b in read('corpus/progress.json')['books'] if b['book_id']=='b-shiji-098')['complete'])

    def test_eleven_retired_ids_have_no_registry_or_public_files(self):
        registered = {p['id'] for p in read('registry/persons.json')['persons']}
        for old in ['nrp_vv5_hry','5k8_ms4_y3k','mfd_hor_95c','hjx_5rx_wzu',
                    'ebz_s7c_pds','1tz_1iv_r3r','rdw_qwe_aa0','och_1lh_hgs',
                    'rzl_t6n_y63','jki_ijf_2w1','rke_c0u_y8f']:
            self.assertNotIn(old, registered)
            self.assertFalse((ROOT / ('exports/persons/'+old+'.json')).exists())
            self.assertFalse((ROOT / ('data/corpus/profiles/'+old+'.json')).exists())
