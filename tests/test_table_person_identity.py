# coding: utf-8
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def cells(number):
    table = json.loads((ROOT / ('data/historical-tables/shiji-%03d.json' % number)).read_text())
    return [cell for fragment in table['fragments'] for row in fragment['rows'] for cell in row['cells']]
class TablePersonIdentityTests(unittest.TestCase):
    def test_all_ten_tables_have_inline_person_markup(self):
        for number in range(13, 23):
            with self.subTest(number=number):
                self.assertTrue(any(cell['person_mentions'] for cell in cells(number)))
    def test_two_shang_taidings_remain_distinct(self):
        people = {mention['person_id'] for cell in cells(13) for mention in cell['person_mentions'] if mention['surface'] == '太丁'}
        self.assertEqual(people, {'tlt_5h1_n6y', 'bnu_h9l_z1o'})
    def test_han_king_xin_is_not_huaiyin_general(self):
        cell = next(cell for cell in cells(17) if '初王韓信元年' in cell['text'])
        self.assertEqual(cell['person_mentions'][0]['person_id'], 'l9e_fbr_36a_*A')
        other = {mention['person_id'] for cell in cells(16) for mention in cell['person_mentions'] if mention['surface'] == '韓信'}
        self.assertEqual(other, {'ofc_8ei_jb7'})
    def test_titled_same_name_in_different_fiefs_is_not_merged(self):
        people = {mention['person_id'] for cell in cells(21) for mention in cell['person_mentions'] if mention['surface'] == '劉成'}
        self.assertGreaterEqual(len(people), 2)

class RoyalTableEvidenceTests(unittest.TestCase):
    def mention(self, cell_id, surface):
        cell = next(cell for cell in cells(17) if cell['id'] == cell_id)
        return next(m for m in cell['person_mentions'] if m['surface'] == surface)

    def test_two_shengs_are_resolved_by_parent_and_state(self):
        liang = self.mention('shiji-017-t1-r029-c21', '懷王勝')
        zhongshan = self.mention('shiji-017-t1-r053-c18', '靖王勝')
        self.assertNotEqual(liang['person_id'], zhongshan['person_id'])
        self.assertEqual(liang['identity_evidence'][0]['chapter_id'], 'c-shiji-058-liang')
        self.assertEqual(zhongshan['identity_evidence'][0]['chapter_id'], 'c-shiji-059-wuzong')

    def test_yan_jian_and_jiangdu_jian_are_distinct(self):
        self.assertNotEqual(self.mention('shiji-017-t1-r012-c14', '靈王建')['person_id'], self.mention('shiji-017-t1-r080-c12', '建')['person_id'])

    def test_han_pengzu_does_not_identify_legendary_pengzu(self):
        m = self.mention('shiji-017-t1-r052-c17', '彭祖')
        self.assertEqual(m['person_id'], 'yqp_nlb_p1p_ACAF')
        self.assertNotEqual(m['person_id'], '7hi_gqd_koj')

    def test_kan_ji_variant_is_unresolved_and_text_is_preserved(self):
        cell = next(cell for cell in cells(17) if cell['id'] == 'shiji-017-t1-r082-c16')
        self.assertEqual(cell['text'], '剛王堪元年')
        self.assertEqual(cell['person_mentions'], [])
        m = cell['unresolved_mentions'][0]
        self.assertIsNone(m['person_id'])
        self.assertEqual(m['candidate_person_ids'], ['yqp_nlb_p1p_ACABAA'])
        self.assertEqual(m['identity_evidence'][0]['quote'], '子剛王基代立')

    def test_identity_reference_rejects_wrong_person_quote_or_revision(self):
        import copy
        from scripts.historical_tables import validate_identity_evidence
        original = self.mention('shiji-017-t1-r052-c17', '彭祖')
        validate_identity_evidence(original)
        for key, value in [('person_id', '7hi_gqd_koj'), ('quote', '此句不見於指定篇文'), ('source_revision', 1)]:
            changed = copy.deepcopy(original)
            changed['identity_evidence'][0][key] = value
            with self.subTest(key=key), self.assertRaises(AssertionError):
                validate_identity_evidence(changed)

    def test_new_identity_evidence_cannot_downgrade_to_legacy_citation(self):
        import copy
        from scripts.historical_tables import validate_identity_evidence
        changed = copy.deepcopy(self.mention('shiji-017-t1-r052-c17', '彭祖'))
        evidence = changed['identity_evidence'][0]
        changed['identity_evidence'] = [{key: evidence[key] for key in ['chapter_id', 'paragraph_id', 'source_id', 'quote']}]
        with self.assertRaises(AssertionError):
            validate_identity_evidence(changed)
