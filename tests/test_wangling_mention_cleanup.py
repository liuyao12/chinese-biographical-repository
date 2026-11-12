import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CID = 'c-sanguozhi-028-wangling'
PREFIX = CID + ':'
PRONOUNS = '''
unit001:m0038
unit002:m0022 unit002:m0033
unit003:m0117
unit004:m0028 unit004:m0152 unit004:m0172 unit004:m0236
unit006:m0036 unit006:m0054
unit006:m0175 unit006:m0181 unit008:m0023 unit009:m0094 unit009:m0141
unit010:m0104 unit010:m0106 unit010:m0246 unit010:m0288 unit010:m0379 unit010:m0170 unit010:m0179 unit010:m0206 unit010:m0211 unit010:m0213 unit010:m0238 unit010:m0243 unit010:m0260 unit010:m0272 unit010:m0278 unit010:m0308 unit010:m0314 unit010:m0315 unit010:m0331 unit010:m0342 unit010:m0344 unit010:m0348 unit010:m0351 unit010:m0363 unit010:m0401 unit010:m0435
unit012:m0283 unit012:m0067 unit012:m0073 unit012:m0076 unit012:m0160 unit012:m0178 unit012:m0241 unit012:m0244 unit012:m0262 unit012:m0270 unit012:m0275 unit012:m0278 unit012:m0287 unit012:m0296 unit012:m0300 unit012:m0313 unit012:m0317 unit012:m0321 unit012:m0337 unit012:m0367 unit012:m0378
unit016:m0055 appraisal:m0089 appraisal-note:m0047 appraisal-note:m0072 qing-02:m0015
'''.split()
NON_NAME_REFERENCES = '''unit001:m0042 unit002:m0036 unit003:m0273 unit012:m0027 unit012:m0068 unit016:m0045'''.split()
REMOVED = '''unit002:m0039'''.split()


class WanglingMentionCleanup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapter = json.loads((ROOT / 'corpus/sanguozhi/028-wangling.json').read_text())
        cls.by_id = {m['id']: (p, m)
                     for p in cls.chapter['paragraphs'] for m in p['mentions']}
        cls.registry = json.loads((ROOT / 'registry/persons.json').read_text())
        cls.people = {p['id']: p for p in cls.registry['persons']}
        cls.alias_ids = {mid for person in cls.registry['persons'] for alias in person.get('aliases', [])
                         for mid in alias.get('mention_ids', [])}

    def test_pronouns_keep_referents_but_are_not_personal_name_aliases(self):
        self.assertEqual(len(PRONOUNS), 67)
        evidence_ids = {e.get('mention_id') for person in self.people.values() for e in person.get('evidence', [])}
        self.assertTrue(set(PREFIX + x for x in PRONOUNS).issubset(evidence_ids))
        for short in PRONOUNS:
            _, mention = self.by_id[PREFIX + short]
            self.assertEqual(mention['kind'], 'pronoun', short)
            self.assertTrue(mention.get('person_id'), short)
            self.assertNotIn(mention['id'], self.alias_ids, short)
            self.assertNotIn('第二人稱', mention.get('interpretation_note', ''), short)

    def test_relation_words_remain_references_without_becoming_name_aliases(self):
        for short in NON_NAME_REFERENCES:
            _, mention = self.by_id[PREFIX + short]
            self.assertEqual(mention['kind'], 'person', short)
            self.assertTrue(mention.get('person_id'), short)
            if short != 'unit001:m0042':
                self.assertNotIn(mention['id'], self.alias_ids, short)
            self.assertNotIn('第二人稱', mention.get('interpretation_note', ''), short)
        wangchen = self.people['b0e_c9d_d1f']
        self.assertIn('晨', [a['surface'] for a in wangchen['aliases']])
        self.assertNotIn('兄晨', [a['surface'] for a in wangchen['aliases']])

    def test_generic_interrogative_and_offense_are_not_person_mentions(self):
        for short in REMOVED:
            self.assertNotIn(PREFIX + short, self.by_id)
            self.assertNotIn(PREFIX + short, self.alias_ids)
        self.assertIn('所坐亦公耳', next(p['text'] for p in self.chapter['paragraphs']
                                        if p['id'].endswith('unit002')))
        for mid, start in [('unit002:m0022', 22), ('unit002:m0033', 33)]:
            _, mention = self.by_id[PREFIX + mid]
            self.assertEqual((mention['surface'], mention['kind'], mention['start'], mention['end']), ('此', 'pronoun', start, start + 1))
        self.assertNotIn(PREFIX + 'unit003:m0377', self.by_id)

    def test_son_name_anchor_and_father_assertion_use_guang_not_zi(self):
        _, name = self.by_id[PREFIX + 'unit003:m0378']
        self.assertEqual(name['surface'], '廣')
        self.assertNotIn(PREFIX + 'unit003:m0377', self.by_id)
        self.assertIn('語子廣廣言廢立大事', next(p['text'] for p in self.chapter['paragraphs'] if p['id'].endswith('unit003')))
        self.assertEqual(name['kind'], 'person')
        wangguang = self.people['f89_ad1_61d_A']
        self.assertNotIn(PREFIX + 'unit003:m0377', self.alias_ids)
        evidence_ids = {e.get('mention_id') for person in self.people.values() for e in person.get('evidence', [])}
        self.assertNotIn(PREFIX + 'unit003:m0377', evidence_ids)
        self.assertIn('廣', [a['surface'] for a in wangguang['aliases']])
        self.assertTrue(any(PREFIX + 'unit003:m0378' in a['mention_ids'] and a['surface'] == '廣'
                            for a in wangguang['aliases']))
        assertions = json.loads((ROOT / 'corpus/sanguozhi/028-wangling-assertions.json').read_text())['assertions']
        father = next(a for a in assertions if a['id'] == 'a-sanguozhi028-wangling-003')
        self.assertEqual(father['evidence'][0]['subject_person_mention_id'], PREFIX + 'unit003:m0378')

    def test_rank_title_anchor_no_longer_points_to_nonperson_suo_zuo(self):
        titles = json.loads((ROOT / 'corpus/sanguozhi/028-wangling-titles.json').read_text())['holdings']
        row = next(x for x in titles if x['id'] == 'th-wang41-061')
        self.assertEqual(row['evidence'][0]['person_mention_id'], PREFIX + 'unit002:m0003')
        self.assertEqual(row['attestations'][0]['person_mention_id'], PREFIX + 'unit002:m0003')
        self.assertEqual(row['effective_period']['start']['evidence'][0]['person_mention_id'],
                         PREFIX + 'unit002:m0003')


if __name__ == '__main__':
    unittest.main()
