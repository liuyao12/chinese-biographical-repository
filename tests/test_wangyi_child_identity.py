import copy
import json
import unittest
from pathlib import Path

from scripts.unresolved_relation_identity import group_errors

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class WangYiChildIdentityTests(unittest.TestCase):
    def setUp(self):
        sources = ('weishu-weishou/063-wangyi', 'beishi/042-wangyi')
        self.chapters = {chapter['id']: chapter for name in sources
                         for chapter in [read(f'corpus/{name}.json')]}
        self.chapter = self.chapters['c-weishu-weishou-063-wangyi']
        self.group, = self.chapter['annotation']['unresolved_relation_identity_groups']
        self.assertions = {a['id']: a for name in sources
                           for a in read(f'corpus/{name}-assertions.json')['assertions']}
        self.people = {*self.group['candidate_person_ids'], self.group['common_person_id']}

    def test_group_uses_both_witnesses_and_rejects_swapped_person_or_revision(self):
        self.assertEqual(group_errors(self.chapter, self.assertions, self.people, self.chapters), [])
        for key, wrong in (
                ('candidate_person_id', self.group['candidate_person_ids'][0]),
                ('revision_id', self.group['references'][0]['revision_id'])):
            with self.subTest(key=key):
                chapter = copy.deepcopy(self.chapter)
                chapter['annotation']['unresolved_relation_identity_groups'][0]['references'][1][key] = wrong
                self.assertTrue(group_errors(chapter, self.assertions, self.people, self.chapters))

    def test_parent_export_keeps_both_reports_and_neither_default_edge(self):
        parent = self.group['common_person_id']
        export = read(f'exports/persons/{parent}.json')
        group, = export['unresolved_relation_identity_groups']
        self.assertIsNone(group['same_person'])
        self.assertIsNone(group['distinct_people'])
        self.assertEqual(
            [r['quote'] for r in group['references']],
            ['子淵，武定中，儀同開府記室參軍。', '子琛，武定中，儀同、開府記室參軍。'])
        ids = set(group['assertion_ids'])
        self.assertTrue(ids.issubset(a['id'] for a in export['relations']))
        self.assertFalse(ids.intersection(a['id'] for a in export['preferred_relations']))
