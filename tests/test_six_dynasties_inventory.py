import unittest
import json
from pathlib import Path

from scripts.six_dynasties_inventory import chapter_passage, received_text, source_paragraphs, source_passage, verify
from scripts.person_references import reference_errors
from scripts.family_assemblies import registry_sibling_path_valid
from scripts.nanqi041_projection import decode_line
from scripts.sanguozhi_early_wu_layers import project_line, project_slice, shown


class SixDynastiesInventoryTest(unittest.TestCase):
    def test_early_wu_linked_names_and_note_in_quote_keep_raw_coordinates(self):
        raw = '{{quote|[[w:孫堅|{{ProperNoun|孫堅}}]]曰：甲。{{*|{{WavyBookMark|呉史}}曰乙。}}丙。}}'
        text, positions, notes = project_line(raw)
        self.assertEqual(text, '孫堅曰：甲。丙。')
        self.assertEqual(''.join(raw[i] for i in positions), text)
        start, end, anchor = notes[0]
        self.assertEqual(anchor, len('孫堅曰：甲。'))
        self.assertEqual(shown(raw[start:end])[0], '呉史曰乙。')
        self.assertEqual(project_slice(raw, raw.index('甲'), raw.index('丙') + 1), '甲。丙')
        self.assertEqual(project_slice(raw, start, end), '呉史曰乙。')

    def test_nanqi_blockquote_keeps_raw_coordinate_and_internal_punctuation(self):
        text, spans, _ = decode_line(':夫曰：甲。', 10)
        self.assertEqual(text, '夫曰：甲。')
        self.assertEqual(spans, [[11, 12], [12, 13], [13, 14], [14, 15], [15, 16]])
        self.assertEqual(source_paragraphs([':夫曰：甲。'], 'nanqi059_fixed_text'), [text])

    def test_song_memorials_strip_one_leading_layout_colon(self):
        lines = ['上表曰：', ':臣聞：甲。', '::乙。']
        self.assertEqual(source_paragraphs(lines, 'wikisource_blockquote_colon'),
                         ['上表曰：', '臣聞：甲。', ':乙。'])
        self.assertEqual(source_paragraphs(lines), lines)

    def test_fixed_paragraph_indents_and_multi_paragraph_quote(self):
        lines = ['　　疏曰：', '{{quote|　　甲。', '', '　　乙。}}', '　　乃止。']
        self.assertEqual(source_paragraphs(lines, 'wikisource_indented_quote'), ['疏曰：', '甲。', '乙。', '乃止。'])
        self.assertEqual(source_paragraphs(lines[:1]), ['　　疏曰：'])
        with self.assertRaises(AssertionError):
            source_paragraphs(lines[:2], 'wikisource_indented_quote')
        with self.assertRaises(AssertionError):
            source_paragraphs(['  甲。'], 'wikisource_indented_quote')

    def test_interrupted_account_preserves_both_headings_and_skips_the_other_subject(self):
        lines = ['==甲==', '甲傳首。', '===乙===', '乙傳。', '===甲續===', '甲傳末。']
        first = dict(heading_line=1, heading_raw=lines[0], first_line=2, last_line=2,
                     start_codepoint=0, end_codepoint=4, opening='甲', closing='首。')
        continuation = dict(first, heading_line=5, heading_raw=lines[4], first_line=6,
                            last_line=6, closing='末。')
        row = dict(first, book_id='book', title='甲', continuation_spans=[continuation])
        headings = set()
        self.assertEqual(source_passage(row, lines, headings, set()), [lines[1], lines[5]])
        self.assertEqual(headings, {1, 5})
        with self.assertRaises(AssertionError):
            source_passage(dict(row, continuation_spans=[first]), lines, set(), set())

    def test_slice_in_a_shared_paragraph_keeps_the_next_subject_outside(self):
        chapter = dict(paragraphs=[dict(id='p1', text='甲傳。乙有二子。'), dict(id='p2', text='丙傳。')])
        row = dict(title='甲', paragraph_ids=['p1'], paragraph_slices={'p1': dict(start=0, end=3)})
        self.assertEqual(chapter_passage(row, chapter)[1], ['甲傳。'])
        with self.assertRaises(AssertionError):
            chapter_passage(dict(row, paragraph_ids=['p2','p1']), chapter)
        with self.assertRaises(AssertionError):
            chapter_passage(dict(row, paragraph_slices={'p1': dict(start=0,end=100)}), chapter)

    def test_markup_projection_keeps_the_displayed_glyph(self):
        self.assertEqual(received_text('與-{范}-交，[[甲|乙]]見[[丙]]。{{YL|元年}}。'), '與范交，乙見丙。元年。')
        self.assertEqual(received_text('張合<ref>別本作張郃。</ref>'), '張合')

    def test_fixed_qi_markup_keeps_both_adjacent_and_joined_glyphs(self):
        raw = '蕭-{叡}--{眀}-，又見-{叡眀}-。'
        offset = 12
        text, spans, marks = decode_line(raw, offset)
        self.assertEqual(text, '蕭叡眀，又見叡眀。')
        self.assertEqual(''.join(raw[start-offset:end-offset] for start, end in spans), text)
        self.assertEqual([row['source'] for row in marks], ['叡', '眀', '叡眀'])

    def test_full_entries_match_fixed_witness_and_progress(self):
        books, counts = verify()
        self.assertIn('b-nanshi-080', books)
        self.assertIn('b-sanguozhi-046', books)
        self.assertGreaterEqual(counts['item_reviewed'], 2)

    def test_quote_must_cover_this_occurrence_of_the_pronoun(self):
        pid = 'c-example:p001'
        ref = dict(id=pid + ':r0004', paragraph_id=pid, start=4, end=5, surface='我',
                   quote='我問君', referent_role='speaker_self', person_id='甲', note='發言者自稱。')
        chapter = dict(id='c-example', paragraphs=[dict(id=pid, text='我問君，我答之。', mentions=[])],
                       annotation=dict(person_reference_occurrences=[ref]))
        self.assertTrue(reference_errors(chapter, {'甲'}))
        ref['quote'] = '我答之'
        self.assertFalse(reference_errors(chapter, {'甲'}))

    def test_inferred_parent_requires_every_sibling_link(self):
        root = Path(__file__).resolve().parents[1]
        people = json.loads((root / 'registry/persons.json').read_text())['persons']
        chapter = json.loads((root / 'corpus/weishu-weishou/024-cuidaogu.json').read_text())
        last = next(p for p in chapter['paragraphs'] if p['text'].startswith('景業弟景淵'))
        person = next(m['person_id'] for m in last['mentions'] if m['surface'] == '景淵')
        path = next(p['family_path'] for p in people if p['id'] == person)
        assertions = {}
        for source in ('corpus/weishu-weishou/024-cuidaogu-assertions.json', 'corpus/beishi/044-cuidaogu-assertions.json'):
            assertions.update({a['id']: a for a in json.loads((root / source).read_text())['assertions']})
        self.assertTrue(registry_sibling_path_valid(person, path, assertions))
        broken = dict(path, evidence=path['evidence'][1:])
        self.assertFalse(registry_sibling_path_valid(person, broken, assertions))
        broken = dict(path, parent_person_id=person)
        self.assertFalse(registry_sibling_path_valid(person, broken, assertions))
