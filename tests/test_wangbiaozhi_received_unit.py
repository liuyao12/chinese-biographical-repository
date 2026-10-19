# coding: utf-8
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return json.loads((ROOT / path).read_text())

class WangBiaoZhiReceivedUnit(unittest.TestCase):
    def setUp(self):
        self.c = read('corpus/jinshu/076-wangbiaozhi.json')
        self.paragraphs = {p['source_position']['first_line']: p for p in self.c['paragraphs']}
        self.decisions = {d['id']: d for d in read('corpus/jinshu/076-wangbiaozhi-identities.json')['decisions']}

    def test_complete_eighteen_paragraphs_include_the_entire_office_memorial(self):
        self.assertEqual(sorted(self.paragraphs), list(range(55, 90, 2)))
        self.assertTrue(self.paragraphs[63]['text'].endswith('彪之上議曰：'))
        self.assertTrue(self.paragraphs[65]['text'].startswith('為政之道'))
        self.assertTrue(self.paragraphs[67]['text'].startswith('今內外百官'))
        for p, raw in zip(self.c['paragraphs'], self.c['source']['normalization']['excerpts']):
            self.assertEqual(hashlib.sha256(raw['raw_quote'].encode()).hexdigest(), raw['raw_quote_sha256'])
            self.assertEqual(hashlib.sha256(p['text'].encode()).hexdigest(), raw['selected_text_sha256'])
            for m in p['mentions']:
                self.assertEqual(p['text'][m['start']:m['end']], m['surface'])

    def test_places_adjectives_and_question_words_are_not_people(self):
        for line, word in [(71, '長安'), (79, '毅然'), (83, '安可以')]:
            p = self.paragraphs[line]
            start = p['text'].index(word)
            self.assertFalse(any(m['start'] < start + len(word) and start < m['end'] for m in p['mentions']))

    def test_macro_form_and_xilang_short_forms_keep_contextual_identity(self):
        for line, forms, key in [(83, ['袁宏', '宏', '巨集'], 'yuanhong-digital-form'),
                                 (59, ['奚郎', '朗'], 'xilang-variant')]:
            mentions = [m for m in self.paragraphs[line]['mentions'] if m['surface'] in forms]
            self.assertEqual(len({m['person_id'] for m in mentions}), 1)
            d = self.decisions['d-jin076-biaozhi-' + key]
            self.assertEqual(set(d['identification_basis']['target_mention_ids']), {m['id'] for m in mentions})
            self.assertTrue(d['references'])
        self.assertIn('巨集', self.paragraphs[83]['text'])
        self.assertIn('奚郎', self.paragraphs[59]['text'])

    def test_source_zun_is_preserved_and_never_merges_father_and_son(self):
        p = self.paragraphs[79]
        m = next(m for m in p['mentions'] if m['surface'] == '武陵王遵')
        self.assertEqual(m['person_id'], 'dkn_ge4_286_AAAAAAAD')
        d = self.decisions['d-jin076-biaozhi-wuling-source-conflict']
        self.assertEqual(d['status'], 'contextual_provisional')
        self.assertEqual(d['confidence_level'], 'medium')
        self.assertTrue(any('晞三子' in ref['quote'] for ref in d['references']))
        self.assertTrue(any('shidianguji' in ref['url'] for ref in d['references']))

    def test_empress_and_retroactive_jianwen_title_are_not_confused(self):
        empress = self.decisions['d-jin076-biaozhi-empress-chu']
        self.assertNotEqual(empress['person_id'], '3ea_uzt_2n2_A')
        self.assertEqual([ref['source_position']['first_line'] for ref in empress['references']], [40, 50])
        self.assertTrue(all(ref['image_verified'] is False for ref in empress['references']))
        emperor = self.decisions['d-jin076-biaozhi-tianzi-mudi']
        self.assertEqual(emperor['person_id'], '84i_4jp_gmc')
        self.assertNotEqual(emperor['person_id'], 'dkn_ge4_286_AAAAAAAF')

    def test_sons_use_actual_adjacent_paragraphs_without_implied_order_or_mother(self):
        rows = read('corpus/jinshu/076-wangbiaozhi-assertions.json')['assertions']
        self.assertEqual(len(rows), 2)
        for a in rows:
            self.assertEqual(a['object_person_id'], '7r6_k52_qji_ABDBB')
            self.assertEqual(a['context']['paragraph_ids'], [self.paragraphs[n]['id'] for n in [87, 89]])
            self.assertNotIn('birth_order', a['qualifiers'])
            self.assertNotIn('mother_person_id', a['qualifiers'])
        self.assertNotIn('彪之', self.paragraphs[89]['text'])

    def test_false_death_report_and_proposed_province_are_not_asserted_events(self):
        self.assertIn('詐云殺苻健、苻眉', self.paragraphs[71]['text'])
        self.assertIn('其弟復處西籓', self.paragraphs[75]['text'])
        path = ROOT / 'corpus/jinshu/076-wangbiaozhi-life-events.json'
        if path.exists():
            for event in json.loads(path.read_text())['events']:
                self.assertFalse(event.get('event_type') == 'death' and any(e.get('paragraph_id') == self.paragraphs[71]['id'] for e in event['evidence']))

if __name__ == '__main__':
    unittest.main()

class WangBiaozhiReadingCases(unittest.TestCase):
    def test_office_variant_keeps_exact_source_and_unadopted_candidate(self):
        import json
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        c = json.loads((root / 'corpus/jinshu/076-wangbiaozhi.json').read_text())
        case = c['annotation']['source_reading_cases'][0]
        p = next(p for p in c['paragraphs'] if p['id'] == case['paragraph_id'])
        self.assertEqual(p['text'][case['start']:case['end']], '復僕為射')
        self.assertEqual(case['quote'], p['text'])
        self.assertEqual(case['candidate_readings'][0]['title'], '僕射')
        self.assertFalse(case['candidate_readings'][0]['adopted'])
        self.assertFalse(case['candidate_readings'][0]['reference']['image_verified'])
        holdings = json.loads((root / 'corpus/jinshu/076-wangbiaozhi-titles.json').read_text())['holdings']
        self.assertFalse(any(h['title'] == '僕為射' for h in holdings))
    def test_donghai_patron_is_not_the_literature_office_holder(self):
        import json
        from pathlib import Path
        root = Path(__file__).resolve().parents[1]
        c = json.loads((root / 'corpus/jinshu/076-wangbiaozhi.json').read_text())
        p = c['paragraphs'][0]
        m = next(m for m in p['mentions'] if m['surface'] == '東海王')
        self.assertEqual(m['person_id'], 'dkn_ge4_286_AAAAAAAC')
        self.assertEqual(p['text'][m['start']:m['end']], '東海王')
        holdings = json.loads((root / 'corpus/jinshu/076-wangbiaozhi-titles.json').read_text())['holdings']
        h = next(h for h in holdings if h['title'] == '東海王文學')
        self.assertEqual(h['person_id'], '7r6_k52_qji_ABDBB')
