# coding: utf-8
import unittest

from scripts.temporal_constraints import collect_temporal_constraints, temporal_constraint_errors


PERSON = 'abc_def_123'
CHAPTER_ID = 'c-test-source'
PARAGRAPH_ID = CHAPTER_ID + ':p001'
CHAPTER_ID_2 = 'c-test-parallel'
PARAGRAPH_ID_2 = CHAPTER_ID_2 + ':p001'
TEXT = '公主永徽中卒，年八十六。'
TEXT_2 = '永徽三年，太宗幸公主第。'
MENTION_ID = PARAGRAPH_ID + ':m0001'
MENTION_ID_2 = PARAGRAPH_ID_2 + ':m0001'
DEATH_ID = 'death-test-person'


def make_constraint(identifier, operator, year, chapter_id=CHAPTER_ID,
                    paragraph_id=PARAGRAPH_ID, mention_id=MENTION_ID,
                    text=TEXT, source_term='永徽中', derivation_kind='named_era_span'):
    anchor_start = text.index(source_term)
    suffix = '1' if chapter_id == CHAPTER_ID else '2'
    return {
        'id': identifier,
        'person_id': PERSON,
        'target': {'entity_type': 'life_event', 'entity_id': DEATH_ID, 'property': 'year'},
        'operator': operator,
        'value': {'kind': 'chinese_regnal_year', 'era_name': '永徽', 'year': year},
        'derivation': {'kind': derivation_kind, 'source_term': source_term,
                       'rationale': 'Synthetic validation fixture; not a historical assertion.'},
        'evidence': [{
            'work_id': 'w-test-' + suffix, 'book_id': 'b-test-' + suffix, 'source_id': 's-test-' + suffix,
            'chapter_id': chapter_id, 'paragraph_id': paragraph_id, 'quote': text,
            'person_mention_id': mention_id,
            'anchor': {'start': anchor_start, 'end': anchor_start + len(source_term), 'surface': source_term}
        }],
        'status': 'editorial_provisional',
        'human_reviewed': False,
        'reviewer': 'Codex（AI代理）'
    }


def fixture_record():
    return {
        'format_version': '0.1', 'record_type': 'person_temporal_constraint_set',
        'chapter_id': CHAPTER_ID,
        'constraints': [make_constraint('tc-test-gte', 'gte', 3)]
    }


def fixture_chapters():
    return {
        CHAPTER_ID: {
            'work_id': 'w-test-1', 'book_id': 'b-test-1', 'source_id': 's-test-1',
            'paragraphs': [{'id': PARAGRAPH_ID, 'text': TEXT, 'mentions': [{
                'id': MENTION_ID, 'kind': 'person', 'person_id': PERSON,
                'start': 0, 'end': 2, 'surface': '公主'
            }]}]
        },
        CHAPTER_ID_2: {
            'work_id': 'w-test-2', 'book_id': 'b-test-2', 'source_id': 's-test-2',
            'paragraphs': [{'id': PARAGRAPH_ID_2, 'text': TEXT_2, 'mentions': [{
                'id': MENTION_ID_2, 'kind': 'person', 'person_id': PERSON,
                'start': TEXT_2.index('公主'), 'end': TEXT_2.index('公主') + 2, 'surface': '公主'
            }]}]
        }
    }


class TemporalConstraintTests(unittest.TestCase):
    def test_source_attested_equality_keeps_the_exact_passage_and_anchor(self):
        text = '公主永徽三年卒。'
        record = fixture_record()
        item = make_constraint('tc-exact-death-year', 'eq', 3,
                               text=text, source_term='永徽三年',
                               derivation_kind='explicit_date')
        item['status'] = 'source_attested'
        record['constraints'] = [item]
        chapters = fixture_chapters()
        chapters[CHAPTER_ID]['paragraphs'][0]['text'] = text
        errors = temporal_constraint_errors(record, chapters, {PERSON}, {
            ('life_event', DEATH_ID): PERSON
        })
        self.assertEqual(errors, [])
        exported = collect_temporal_constraints([record], {PERSON})
        self.assertEqual(exported[0]['operator'], 'eq')
        evidence = exported[0]['evidence'][0]
        self.assertEqual(evidence['quote'], text)
        self.assertEqual(text[evidence['anchor']['start']:evidence['anchor']['end']], '永徽三年')

    def test_keeps_independent_source_bounds_for_consumer_intersection(self):
        era_record = fixture_record()
        era_record['constraints'] = [make_constraint('tc-lower', 'gte', 1),
                                     make_constraint('tc-upper', 'lte', 6)]
        alive_record = {'format_version': '0.1', 'record_type': 'person_temporal_constraint_set',
                        'chapter_id': CHAPTER_ID_2,
                        'constraints': [make_constraint('tc-later-lower', 'gte', 3,
                            chapter_id=CHAPTER_ID_2, paragraph_id=PARAGRAPH_ID_2,
                            mention_id=MENTION_ID_2, text=TEXT_2, source_term='永徽三年',
                            derivation_kind='alive_at_date')]}
        chapters = fixture_chapters()
        targets = {('life_event', DEATH_ID): PERSON}
        errors = temporal_constraint_errors(era_record, chapters, {PERSON}, targets)
        errors.extend(temporal_constraint_errors(alive_record, chapters, {PERSON}, targets))
        self.assertEqual(errors, [])
        records = [era_record, alive_record]
        collected = collect_temporal_constraints(records, {PERSON})
        self.assertEqual([item['operator'] for item in collected], ['gte', 'lte', 'gte'])
        self.assertEqual([item['value']['year'] for item in collected], [1, 6, 3])
        self.assertEqual(len({item['evidence'][0]['quote'] for item in collected}), 2)

    def test_rejects_bad_source_anchor_and_person_binding(self):
        record = fixture_record()
        record['constraints'][0]['evidence'][0]['anchor']['end'] += 1
        errors = temporal_constraint_errors(record, fixture_chapters(), {PERSON}, {
            ('life_event', DEATH_ID): PERSON
        })
        self.assertTrue(any('原詞字位不符' in error for error in errors))

        record = fixture_record()
        record['constraints'][0]['evidence'][0]['person_mention_id'] = 'missing-mention'
        errors = temporal_constraint_errors(record, fixture_chapters(), {PERSON}, {
            ('life_event', DEATH_ID): PERSON
        })
        self.assertTrue(any('人物錨點不符' in error for error in errors))

    def test_rejects_cross_person_death_event(self):
        errors = temporal_constraint_errors(fixture_record(), fixture_chapters(), {PERSON}, {
            ('life_event', DEATH_ID): 'other_person_001'
        })
        self.assertTrue(any('目標不存在、人物不符' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
