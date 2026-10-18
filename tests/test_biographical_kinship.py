import copy
import unittest
from scripts.biographical_kinship import child_continuation_errors
from scripts.family_assemblies import brother_connects


def fixture():
    # Synthetic three-paragraph biography; no historical claim is made here.
    paragraphs = []
    for i, text in enumerate(['甲任官。', '卒官。', '子乙。']):
        paragraphs.append({'id': f'p{i}', 'text': text, 'text_layer': 'received_chapter',
            'source_position': {'first_line': 10 + i * 2, 'last_line': 11 + i * 2,
                                'revision_id': 1, 'editorial_excerpt_boundary': True},
            'mentions': []})
    paragraphs[0]['mentions'] = [{'id': 'ma', 'kind': 'person', 'person_id': 'parent', 'start': 0, 'end': 1}]
    paragraphs[-1]['mentions'] = [{'id': 'mb', 'kind': 'person', 'person_id': 'child', 'start': 1, 'end': 2}]
    chapter = {'id': 'c', 'source_id': 's', 'source': {'revision_id': 1}, 'paragraphs': paragraphs}
    a = {'predicate': 'father', 'subject_person_id': 'child', 'object_person_id': 'parent',
         'qualifiers': {'source_term': '子', 'lineage': 'paternal'},
         'context': {'kind': 'biographical_child_continuation', 'paragraph_ids': ['p0', 'p1', 'p2'],
                     'parent_mention_id': 'ma', 'child_mention_id': 'mb', 'rationale': 'Synthetic continuous biography.',
                     'status': 'contextual_provisional', 'human_reviewed': False},
         'evidence': [{'chapter_id': 'c', 'source_id': 's', 'paragraph_id': p['id'], 'quote': p['text']} for p in paragraphs]}
    return a, chapter


class BiographyContinuationTests(unittest.TestCase):
    def test_complete_continuous_source(self):
        a, c = fixture()
        self.assertEqual(child_continuation_errors(a, c), [])

    def test_cannot_skip_middle_death_paragraph(self):
        a, c = fixture()
        a['context']['paragraph_ids'].pop(1)
        a['evidence'].pop(1)
        self.assertTrue(child_continuation_errors(a, c))

    def test_edited_excerpt_cannot_conceal_source_gap(self):
        a, c = fixture()
        c['paragraphs'][1]['source_position']['first_line'] += 1
        self.assertTrue(child_continuation_errors(a, c))

    def test_cannot_quote_only_selected_names(self):
        a, c = fixture()
        a['evidence'][0]['quote'] = '甲'
        self.assertTrue(child_continuation_errors(a, c))

    def test_other_person_or_reversed_relationship_rejected(self):
        a, c = fixture()
        a['object_person_id'] = 'someone-else'
        self.assertTrue(child_continuation_errors(a, c))
        a, c = fixture()
        a['subject_person_id'], a['object_person_id'] = a['object_person_id'], a['subject_person_id']
        self.assertTrue(child_continuation_errors(a, c))

    def test_cannot_cross_revision_or_annotation_layer(self):
        for key, value in [('text_layer', 'digital_editorial_note'), ('revision', 2)]:
            a, c = fixture()
            if key == 'revision': c['paragraphs'][1]['source_position']['revision_id'] = value
            else: c['paragraphs'][1][key] = value
            self.assertTrue(child_continuation_errors(a, c))

    def test_requires_child_expression_and_editorial_status(self):
        a, c = fixture()
        c['paragraphs'][2]['mentions'][0]['start'] = 0
        self.assertTrue(child_continuation_errors(a, c))
        a, c = fixture()
        a['context']['human_reviewed'] = True
        self.assertTrue(child_continuation_errors(a, c))

    def test_sister_can_support_reviewable_shared_paternal_inference(self):
        a = {'subject_person_id': 'sister', 'object_person_id': 'brother', 'predicate': 'sister', 'qualifiers': {}}
        self.assertTrue(brother_connects(a, ['sister'], ['brother']))
        a['qualifiers']['shared_father'] = False
        self.assertFalse(brother_connects(a, ['sister'], ['brother']))
        a['predicate'] = 'spouse'; a['qualifiers'] = {}
        self.assertFalse(brother_connects(a, ['sister'], ['brother']))
