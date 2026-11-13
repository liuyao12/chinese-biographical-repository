import unittest

from scripts.ancestor_distance_difference import ancestor_path_valid, parent_edge_valid


URL = 'https://example.org/fixed-witness?oldid=7'
QUOTE = '後裔甲玄孫祖父丙父丁'


def assertion(aid, predicate, object_id, distance=None, *, subject='descendant',
              paragraph='p001', source='source-7', lineage='paternal'):
    qualifiers = {'lineage': lineage}
    if distance is not None:
        qualifiers['generation_distance'] = distance
    return {
        'id': aid, 'subject_person_id': subject, 'predicate': predicate,
        'object_person_id': object_id, 'status': 'source_attested',
        'qualifiers': qualifiers,
        'evidence': [{
            'work_id': 'work', 'book_id': 'book', 'chapter_id': 'chapter',
            'source_id': source, 'paragraph_id': paragraph, 'quote': QUOTE,
        }],
    }


def setup_claims():
    claims = {
        'd4': assertion('d4', 'ancestor', 'root', 4),
        'd2': assertion('d2', 'grandfather', 'grandfather', 2),
        'd1': assertion('d1', 'father', 'father', 1),
    }
    chapters = {'chapter': {'source_id': 'source-7', 'source': {'url': URL, 'permalink': URL}}}

    def connection(ids):
        return {
            'type': 'same_descendant_distance_difference',
            'status': 'contextual_provisional', 'human_reviewed': False,
            'rationale': '以同一後裔的父系世代距離相減；不增造來源父子斷言。',
            'assertion_ids': ids,
            'references': [{
                'assertion_id': aid, 'quote': QUOTE, 'paragraph_id': 'p001',
                'chapter_id': 'chapter', 'source_id': 'source-7',
                'url': URL, 'scope': 'exact_source_clause',
            } for aid in ids],
        }
    return claims, chapters, connection


class AncestorDistanceDifferenceTests(unittest.TestCase):
    def test_known_intermediate_with_one_missing_generation(self):
        claims, chapters, connection = setup_claims()
        rows = {
            'root': {'source_person_ids': ['root']},
            'grandfather': {'source_person_ids': ['grandfather']},
            'descendant': {'source_person_ids': ['descendant']},
        }
        member = {
            'source_person_ids': ['grandfather'], 'source_assertion_id': None,
            'ancestor_person_id': 'root', 'parent_person_id': None,
            'connection': 'ancestor', 'generation_distance': 2,
            'intermediate_person_ids': [None],
            'ancestor_connection': connection(['d4', 'd2']),
        }
        self.assertTrue(ancestor_path_valid(member, rows, claims, chapters))

    def test_adjacent_known_ancestor_distance_derives_parent_edge(self):
        claims, chapters, connection = setup_claims()
        rows = {
            'grandfather': {'source_person_ids': ['grandfather']},
            'father': {'source_person_ids': ['father']},
            'descendant': {'source_person_ids': ['descendant']},
        }
        member = {
            'source_person_ids': ['father'], 'source_assertion_id': None,
            'parent_person_id': 'grandfather',
            'parent_connection': connection(['d2', 'd1']),
        }
        self.assertTrue(parent_edge_valid(member, rows, claims, chapters))

    def test_unrelated_descendants_are_rejected(self):
        claims, chapters, connection = setup_claims()
        claims['d2']['subject_person_id'] = 'other'
        rows = {'root': {'source_person_ids': ['root']},
                'grandfather': {'source_person_ids': ['grandfather']},
                'descendant': {'source_person_ids': ['descendant']}}
        member = {'source_person_ids': ['grandfather'], 'source_assertion_id': None,
                  'ancestor_person_id': 'root', 'parent_person_id': None,
                  'connection': 'ancestor', 'generation_distance': 2,
                  'intermediate_person_ids': [None],
                  'ancestor_connection': connection(['d4', 'd2'])}
        self.assertFalse(ancestor_path_valid(member, rows, claims, chapters))

    def test_different_paragraph_or_source_is_rejected(self):
        for field, value in [('paragraph', 'p002'), ('source', 'source-8')]:
            with self.subTest(field=field):
                claims, chapters, connection = setup_claims()
                claims['d2']['evidence'][0][field + ('_id' if field == 'source' else '_id')] = value
                rows = {'root': {'source_person_ids': ['root']},
                        'grandfather': {'source_person_ids': ['grandfather']},
                'descendant': {'source_person_ids': ['descendant']}}
                member = {'source_person_ids': ['grandfather'], 'source_assertion_id': None,
                          'ancestor_person_id': 'root', 'parent_person_id': None,
                          'connection': 'ancestor', 'generation_distance': 2,
                          'intermediate_person_ids': [None],
                          'ancestor_connection': connection(['d4', 'd2'])}
                self.assertFalse(ancestor_path_valid(member, rows, claims, chapters))

    def test_distance_mismatch_is_rejected(self):
        claims, chapters, connection = setup_claims()
        claims['d4']['qualifiers']['generation_distance'] = 5
        rows = {'root': {'source_person_ids': ['root']},
                'grandfather': {'source_person_ids': ['grandfather']},
                'descendant': {'source_person_ids': ['descendant']}}
        member = {'source_person_ids': ['grandfather'], 'source_assertion_id': None,
                  'ancestor_person_id': 'root', 'parent_person_id': None,
                  'connection': 'ancestor', 'generation_distance': 2,
                  'intermediate_person_ids': [None],
                  'ancestor_connection': connection(['d4', 'd2'])}
        self.assertFalse(ancestor_path_valid(member, rows, claims, chapters))

    def test_maternal_lineage_is_rejected(self):
        claims, chapters, connection = setup_claims()
        claims['d2']['qualifiers']['lineage'] = 'maternal'
        rows = {'root': {'source_person_ids': ['root']},
                'grandfather': {'source_person_ids': ['grandfather']},
                'descendant': {'source_person_ids': ['descendant']}}
        member = {'source_person_ids': ['grandfather'], 'source_assertion_id': None,
                  'ancestor_person_id': 'root', 'parent_person_id': None,
                  'connection': 'ancestor', 'generation_distance': 2,
                  'intermediate_person_ids': [None],
                  'ancestor_connection': connection(['d4', 'd2'])}
        self.assertFalse(ancestor_path_valid(member, rows, claims, chapters))

    def test_ambiguous_extra_claim_is_rejected(self):
        claims, chapters, connection = setup_claims()
        claims['d2-alt'] = assertion('d2-alt', 'grandfather', 'grandfather', 2)
        rows = {'root': {'source_person_ids': ['root']},
                'grandfather': {'source_person_ids': ['grandfather']},
                'descendant': {'source_person_ids': ['descendant']}}
        member = {'source_person_ids': ['grandfather'], 'source_assertion_id': None,
                  'ancestor_person_id': 'root', 'parent_person_id': None,
                  'connection': 'ancestor', 'generation_distance': 2,
                  'intermediate_person_ids': [None],
                  'ancestor_connection': connection(['d4', 'd2', 'd2-alt'])}
        self.assertFalse(ancestor_path_valid(member, rows, claims, chapters))


if __name__ == '__main__':
    unittest.main()
