# coding: utf-8
"""Contextual short names, rare surname, and relative chronology boundaries."""
import json
from pathlib import Path
import unittest
from scripts.consolidate_person_ids import reference_files
ROOT = Path(__file__).resolve().parents[1]
RETIRED = ['xne_qdl_46g', 'wnn_236_u9x', '903_fwd_xdq', '87x_kxf_d86']
def read(path):
    return json.loads((ROOT / path).read_text())
class StrengthNameContext(unittest.TestCase):
    def test_exact_source_anchors_and_short_forms(self):
        cases = [('117', 'm045-0110', '賁', 'dwv_5hn_680'),
                 ('117', 'm045-0112', '育', '66l_m67_5ie'),
                 ('117', 'm045-0105', '慶忌', 'n7l_j5p_4wl'),
                 ('059', 'm027-0070', '所忠', 'gns_w0b_kfj')]
        for book, suffix, surface, pid in cases:
            p, m = next((p,m) for p in read(f'corpus/shiji/{book}.json')['paragraphs']
                        for m in p['mentions'] if m['id'].endswith(suffix))
            self.assertEqual((m['surface'], m['person_id']), (surface,pid))
            self.assertEqual(p['text'][m['start']:m['end']], surface)
    def test_four_cross_chapter_decisions_keep_commentary_separate(self):
        ds = [d for d in read('corpus/shiji/117-equivalences.json')['decisions']
              if d['id'].startswith('eq-shiji117-strength-') or d['id']=='eq-shiji117-suozhong-wuzong']
        self.assertEqual(len(ds),4)
        for d in ds:
            self.assertTrue(d['identity_materialized'])
            self.assertEqual(d['person_ids'],[d['canonical_person_id']])
            self.assertEqual(d['confidence_level'],'high')
            self.assertFalse(d['human_reviewed'])
            self.assertEqual(len(d['chapter_ids']),2)
            for ref in d['references']:
                self.assertIn(ref['source_commit'],ref['url'])
                self.assertFalse(ref['image_verified'])
                self.assertEqual(len(ref['response_sha256']),64)
    def test_rare_surname_has_explicit_commentary_not_character_slicing(self):
        n=next(n for n in read('data/corpus/profile-names.json')['records'] if n['person_id']=='gns_w0b_kfj')
        self.assertEqual((n['surname'],n['ming'],n['title']),('所','忠',None))
        self.assertIn('所姓/也忠名也',n['references'][0]['quote'])
        self.assertIn('並一人也',n['references'][0]['quote'])
        t=next(t for t in read('corpus/shiji/059-titles.json')['holdings'] if t['id']=='th-shiji059-045')
        self.assertEqual((t['kind'],t['mode']),('unclassified','attestation'))
    def test_qingji_is_not_han_scholar_and_wang_is_not_invented_surname(self):
        people={p['id']:p for p in read('registry/persons.json')['persons']}
        self.assertEqual(people['n7l_j5p_4wl']['label'],'慶忌')
        self.assertIn('yep_hlx_57i',people)
        d,=read('corpus/shiji/117-distinctions.json')['distinctions']
        self.assertEqual(set(d['person_ids']),{'n7l_j5p_4wl','yep_hlx_57i'})
        for n in read('data/corpus/profile-names.json')['records']:
            if n['person_id']=='n7l_j5p_4wl': self.assertNotEqual(n['surname'],'王')
    def test_wuhuo_confidence_is_supported_by_new_explicit_note(self):
        d=next(d for d in read('corpus/shiji/117-equivalences.json')['decisions'] if d['id']=='eq-shiji117-allusion-wuhuo')
        self.assertEqual(d['confidence_level'],'high')
        self.assertTrue(any('烏獲秦武王力士也' in r['quote'] for r in d['references']))
    def test_relative_interval_is_not_a_short_death_year(self):
        e=next(e for e in read('corpus/shiji/002-life-events.json')['events'] if e['id']=='le-shiji002-003')
        self.assertIsNone(e['date_expression'])
        self.assertEqual(e['person_id'],'ddb_l4j_4j2')
        self.assertEqual(e['source_term'],'十七年而帝舜崩')
        self.assertIn('帝舜薦禹於天',e['evidence'][0]['quote'])
    def test_retired_ids_have_no_editable_references_or_files(self):
        for path in reference_files(ROOT):
            for old in RETIRED: self.assertNotIn(old,path.read_text(),str(path))
        for old in RETIRED:
            for directory in ['exports/persons','data/corpus/profiles']:
                self.assertFalse((ROOT/directory/f'{old}.json').exists())
if __name__=='__main__': unittest.main()
