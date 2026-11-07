import copy
import unittest
import xml.etree.ElementTree as ET
from scripts.person_mentions import is_person_reference, pronoun_errors, identity_surfaces_supported
from scripts.render_corpus import render


class PersonReferenceKinds(unittest.TestCase):
    def marker(self):
        return dict(id='synthetic-pronoun', start=4, end=5, surface='之',
                    kind='pronoun', person_id='synthetic-person',
                    interpretation_note='測試用已判定代詞共指',
                    status='contextual_provisional')

    def test_resolved_pronoun_preserves_referent_without_becoming_a_name(self):
        marker = self.marker()
        self.assertTrue(is_person_reference(marker))
        self.assertEqual(pronoun_errors(marker, '王羲之見之。', {'synthetic-person'}), [])
        without_note = dict(marker)
        del without_note['interpretation_note']
        self.assertEqual(pronoun_errors(without_note, '王羲之見之。'), [])
        for status in (None, 'source_attested', 'resolved_contextual'):
            self.assertEqual(pronoun_errors(dict(marker, status=status), '王羲之見之。'), [])

    def test_invalid_referent_span_work_and_classification_are_rejected(self):
        marker = self.marker()
        for patch in ({'person_id': None}, {'person_id': 'unknown'},
                      {'start': 3}, {'end': 6}, {'surface': '王羲之'},
                      {'work_id': 'synthetic-work'}, {'status': 'unresolved'},
                      {'kind': 'non_person'}):
            with self.subTest(patch=patch):
                self.assertTrue(pronoun_errors(dict(marker, **patch), '王羲之見之。', {'synthetic-person'}))
        self.assertFalse(is_person_reference({'kind': 'pronoun', 'surface': '王羲之', 'person_id': 'synthetic-person'}))
        self.assertFalse(is_person_reference({'kind': 'unresolved', 'surface': '之', 'person_id': None}))

    def test_xml_uses_a_plain_segment_and_preserves_name_text_and_anchor(self):
        marker = self.marker()
        chapter = dict(work_id='synthetic-work', book_id='synthetic-book',
                       id='synthetic-chapter', source_id='synthetic-source',
                       paragraphs=[dict(id='synthetic-p', text='王羲之見之。', mentions=[
                           dict(id='synthetic-name', start=0, end=3, surface='王羲之', kind='person', person_id='synthetic-person'), marker])])
        before = copy.deepcopy(chapter)
        paragraph = ET.fromstring(render(chapter)).find('p')
        self.assertEqual(''.join(paragraph.itertext()), '王羲之見之。')
        self.assertEqual([e.tag for e in paragraph], ['persName', 'seg'])
        self.assertEqual(paragraph[1].attrib, {'id':'synthetic-pronoun', 'type':'pronoun', 'ref':'synthetic-person'})
        self.assertEqual(chapter, before)
        chapter['paragraphs'][0]['mentions'][1]['surface'] = '王羲之'
        with self.assertRaises(ValueError):
            render(chapter)

    def test_identity_form_requires_its_own_scoped_source_and_referent(self):
        p = dict(id='synthetic-p', text='王羲之見之。', mentions=[self.marker()])
        paragraphs = {'synthetic-p': ('synthetic-c', p)}
        chapters = {'synthetic-c': {'source_id': 'synthetic-source'}}
        person = {'id':'synthetic-person', 'aliases': [{'surface': '王羲之'}],
                  'evidence':[{'chapter_id':'synthetic-c','paragraph_id':'synthetic-p','mention_id':'synthetic-pronoun','quote':'之'}]}
        evidence = dict(chapter_id='synthetic-c', source_id='synthetic-source',
                        paragraph_id='synthetic-p', quote='見之')
        decision = dict(person_id='synthetic-person', surfaces=['王羲之', '之'], evidence=[evidence])
        self.assertTrue(identity_surfaces_supported(decision, person, paragraphs, chapters))
        for patch in ({'quote': '不存在的引文'}, {'source_id': 'wrong'},
                      {'chapter_id': 'wrong'}, {'paragraph_id': 'wrong'}):
            candidate = dict(decision, evidence=[dict(evidence, **patch)])
            self.assertFalse(identity_surfaces_supported(candidate, person, paragraphs, chapters))
        self.assertFalse(identity_surfaces_supported(dict(decision, person_id='another'), person, paragraphs, chapters))
        self.assertFalse(identity_surfaces_supported(decision, dict(person, evidence=[]), paragraphs, chapters))
        self.assertFalse(identity_surfaces_supported(decision, person, paragraphs, chapters, ['another-c']))
        # A representative quote need not repeat every chapter-wide form.
        self.assertTrue(identity_surfaces_supported(dict(decision, evidence=[dict(evidence, quote='王羲之')]), person, paragraphs, chapters))
        legacy = dict(decision, chapter_ids=['synthetic-c'], evidence=[{'paragraph_id':'synthetic-p','quote':'見之'}])
        self.assertTrue(identity_surfaces_supported(legacy, person, paragraphs, chapters))
        for field in ('source_id', 'work_id', 'book_id'):
            corrupt_reverse = dict(person, evidence=[dict(person['evidence'][0], **{field:'wrong'})])
            self.assertFalse(identity_surfaces_supported(decision, corrupt_reverse, paragraphs, chapters))
            corrupt_decision = dict(decision, evidence=[dict(evidence, **{field:'wrong'})])
            self.assertFalse(identity_surfaces_supported(corrupt_decision, person, paragraphs, chapters))
        self.assertEqual(person['aliases'], [{'surface': '王羲之'}])
