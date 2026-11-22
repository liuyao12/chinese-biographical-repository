from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import unittest

from scripts.chenshu023_wangyang import mother_valid, proposal_valid

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'source-evidence/chenshu023-shenwanglu'


def read(path):
    return json.loads(path.read_bytes())


class WangBrothers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = ROOT / 'corpus/chenshu'
        cls.yang = read(base / '023-wangyang-complete.json')
        cls.yu = read(base / '023-wangyu-complete.json')
        cls.mother = next(a for a in read(base / '023-wangyang-complete-assertions.json')['assertions']
                          if a['predicate'] == 'mother')

    def test_all_sentences_reproduce_printed_and_digital_readings(self):
        raw = (ROOT / self.yang['source']['raw_path']).read_bytes()
        self.assertEqual(sha256(raw).hexdigest(), self.yang['source']['raw_file_sha256'])
        for ch, total in [(self.yang, 27), (self.yu, 6)]:
            readings = ch['annotation']['source_reading_cases']
            self.assertEqual(len(readings), total)
            for p in ch['paragraphs']:
                self.assertEqual(''.join(raw.decode()[i] for i in p['source_position']['raw_character_offsets']), p['text'])
                quotes = [d for d in readings if d['paragraph_id'] == p['id']]
                self.assertEqual(''.join(d['source_quote'] for d in quotes), p['text'])
                for d in quotes:
                    self.assertEqual(p['text'][d['start_codepoint']:d['end_codepoint']], d['source_quote'])
        cols = read(EVIDENCE/'wang-brothers-wuyingdian.json')['columns']
        self.assertEqual(len(cols), 26)
        self.assertEqual(len({(c['pdf_page'], c['half'], c['column_from_right']) for c in cols}), 26)
        text = ''.join(c['text'] for c in cols)
        for words in ('永定九年遷守五兵尚書', '太建六年卒時年五十四', '諡曰光子瑒第十三弟瑜', '年五十官至侍中', '頃之卒時年四十'):
            self.assertIn(words, text)

    def test_birth_mother_requires_her_own_role_and_named_son(self):
        a = self.mother
        self.assertTrue(mother_valid(a, a['evidence'][0], self.yang))
        for changed in ('subject_person_id', 'object_person_id', 'role', 'offset'):
            b = deepcopy(a)
            if changed == 'role':
                b['evidence'][0]['object_person_reference_id'] = self.yang['annotation']['person_reference_occurrences'][1]['id']
            elif changed == 'offset':
                b['qualifiers']['reading_basis']['relationship_anchor']['start'] += 1
            else:
                b[changed] = '7r6_k52_qji_ABAAAAAABAAB'
            self.assertFalse(mother_valid(b, b['evidence'][0], self.yang))

    def test_offers_require_independent_outcome_anchors(self):
        proposals = self.yang['annotation']['title_proposals']
        self.assertEqual({p['title'] for p in proposals}, {'信威將軍', '雲麾始興王長史', '尚書右僕射'})
        for p in proposals:
            self.assertTrue(proposal_valid(p, self.yang))
            for key in ('role_anchor', 'appointment_anchor', 'non_assumption_anchor'):
                b = deepcopy(p)
                b[key]['start'] += 1
                self.assertFalse(proposal_valid(b, self.yang))
            b = deepcopy(p)
            b['person_id'] = 'icd_mkz_d9n_B'
            self.assertFalse(proposal_valid(b, self.yang))

    def test_annals_preserve_month_correction_separately_from_biography(self):
        annals = read(ROOT/'corpus/chenshu/005-wangyang-office-death.json')
        self.assertEqual(annals['paragraphs'][-1]['text'], '〔五月〕庚寅，尚書左僕射王瑒卒。')
        self.assertIn('太建（六）〔八〕年卒', self.yang['paragraphs'][-1]['text'])
        self.assertIn('年（五）〔三〕十', self.yu['paragraphs'][0]['text'])
        for ch, value in [(self.yang,54),(self.yu,40)]:
            a, = ch['annotation']['age_assertions']
            self.assertEqual(a['value'],value)
            self.assertIsNone(a['birth_year'])
