import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FanCaiIdentityTests(unittest.TestCase):
    def test_mengchang_short_forms_do_not_relink_other_wenzi(self):
        chapter = json.loads((ROOT / 'corpus/shiji/079.json').read_text())
        selected = [m for p in chapter['paragraphs'] for m in p['mentions']
                    if m['surface'] in ('文子', '田文')]
        self.assertEqual(len(selected), 3)
        self.assertEqual({m['person_id'] for m in selected}, {'7pl_s0g_rkh'})
        tian = json.loads((ROOT / 'corpus/shiji/046.json').read_text())
        older = [m for p in tian['paragraphs'] for m in p['mentions']
                 if m['surface'] in ('文子須無', '田文子', '文子')]
        self.assertTrue(older)
        self.assertTrue(all(m['person_id'] != '7pl_s0g_rkh' for m in older))

    def test_four_person_summary_resolves_local_baigong_only(self):
        chapter = json.loads((ROOT / 'corpus/shiji/079.json').read_text())
        paragraph = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p032'))
        mention = next(m for m in paragraph['mentions'] if m['surface'] == '白公')
        self.assertEqual(mention['person_id'], '2bk_fz6_icl')
        self.assertIn('則商君、白公、吳起、大夫種是也', paragraph['text'])
        people = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        chu = [p for p in people if p['label'].startswith('白公勝')]
        self.assertTrue(chu)
        self.assertTrue(all(p['id'] != mention['person_id'] for p in chu))

    def test_commentator_reference_preserves_unverified_image_status(self):
        decisions = json.loads((ROOT / 'corpus/shiji/079-equivalences.json').read_text())['decisions']
        decision = next(d for d in decisions if d['id'] == 'eq-shiji079-baigong')
        self.assertEqual(decision['person_ids'], ['2bk_fz6_icl'])
        self.assertTrue(decision['identity_materialized'])
        self.assertEqual(decision['references'][0]['quote'], '白起。')
        self.assertFalse(decision['references'][0]['image_verified'])
        self.assertFalse(decision['human_reviewed'])
