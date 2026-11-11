import json
import tempfile
import unittest
import copy
from pathlib import Path
from unittest.mock import patch

from scripts import export_person_bundles as exporter


class ExportPersonBundlesResumeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.people = {
            'aaa_aaa_aaa': {'id': 'aaa_aaa_aaa', 'label': '甲', 'id_aliases': ['legacy_aaa']},
            'bbb_bbb_bbb': {'id': 'bbb_bbb_bbb', 'label': '乙', 'id_aliases': []},
        }
        self.assembly = {
            'person_id': 'aaa_aaa_aaa',
            'representative_source_person_id': 'aaa_aaa_aaa',
            'source_person_ids': ['aaa_aaa_aaa'],
            'root_person_id': 'aaa_aaa_aaa',
        }
        self.old_bundle = {
            'identity_policy': {'policy': 'source-backed'},
            'family_tree_decisions': [{
                'id': 'decision-parent-1',
                'default_view': 'omit_unproven_biological_parent_edge',
                'subject_person_id': 'aaa_aaa_aaa',
            }],
            'person_ids': ['aaa_aaa_aaa'],
            'mention_count': 17,
        }

    def _patch_export_dependencies(self, bundle_mock, prune_side_effect=None, assembly_data=None):
        assembly_data = assembly_data or ({'aaa_aaa_aaa': self.assembly}, {})
        stack = [
            patch.object(exporter, 'load_catalog', return_value=(self.people, [])),
            patch.object(exporter, 'load_assemblies', return_value=assembly_data),
            patch.object(exporter, 'bundle', bundle_mock),
            patch.object(exporter, 'index_counts', side_effect=lambda result: {
                'mention_count': result['mention_count'],
                'most_mentioned_source_ids': [],
            }),
            patch('scripts.calendar_wiring.export_calendar_contexts'),
            patch('scripts.formal_source_citations.load_citation_index', return_value={}),
            patch('scripts.personless_namespace.prune_person_files', side_effect=prune_side_effect),
        ]
        for context in stack:
            started = context.start()
            if context.attribute == 'prune_person_files':
                self.prune_mock = started
            elif context.attribute == 'export_calendar_contexts':
                self.calendar_mock = started
            self.addCleanup(context.stop)

    def test_resume_reuses_checkpoint_bundle_and_rebuilds_index_rows(self):
        destination = self.root / 'exports/persons'
        destination.mkdir(parents=True)
        checkpoint_file = destination / 'aaa_aaa_aaa.json'
        checkpoint_file.write_text(json.dumps(self.old_bundle))
        checkpoint_bytes = checkpoint_file.read_bytes()
        later_bundle = {
            'identity_policy': {'policy': 'source-backed'},
            'family_tree_decisions': [],
            'person_ids': ['bbb_bbb_bbb'],
            'mention_count': 3,
        }
        def build_bundle(pid, **kwargs):
            return copy.deepcopy(self.old_bundle if pid == 'aaa_aaa_aaa' else later_bundle)

        bundle_mock = unittest.mock.Mock(side_effect=build_bundle)
        self._patch_export_dependencies(bundle_mock)

        exporter.export(root=self.root, resume_after='aaa_aaa_aaa')

        bundle_mock.assert_any_call(
            'bbb_bbb_bbb', root=self.root, include_provisional=True,
            catalog=(self.people, []),
        )
        bundle_mock.assert_any_call(
            'aaa_aaa_aaa', root=self.root, include_provisional=True,
            catalog=(self.people, []),
        )
        self.assertEqual(checkpoint_file.read_bytes(), checkpoint_bytes)
        self.assertTrue((destination / 'legacy_aaa.json').is_file())
        alias = json.loads((destination / 'legacy_aaa.json').read_text())
        self.assertEqual(alias['requested_person_id'], 'legacy_aaa')
        self.prune_mock.assert_called_once_with(
            destination, {'aaa_aaa_aaa', 'bbb_bbb_bbb', 'legacy_aaa'},
        )
        self.assertTrue((destination / 'README.md').is_file())
        self.assertTrue((destination / 'unconnected.md').is_file())
        index = json.loads((destination / 'index.json').read_text())
        resumed = index['persons'][0]
        self.assertEqual(resumed['person_id'], 'aaa_aaa_aaa')
        self.assertEqual(resumed['mention_count'], 17)
        self.assertEqual(resumed['preferred_parent_status'], 'unresolved')
        self.assertEqual(resumed['parent_decision_ids'], ['decision-parent-1'])
        self.assertEqual(resumed['assembled_identity'], self.assembly)
        self.assertEqual(index['persons'][1]['person_id'], 'bbb_bbb_bbb')
        self.assertEqual(index['persons'][1]['mention_count'], 3)
        self.assertEqual(index['id_aliases'], {'legacy_aaa': 'aaa_aaa_aaa'})
        self.assertEqual(index['reading_indexes']['family_pages'], ['README.md'])
        self.assertEqual(index['reading_indexes']['unconnected_pages'], ['unconnected.md'])

    def test_resume_fails_if_checkpoint_bundle_is_missing(self):
        bundle_mock = unittest.mock.Mock()
        self._patch_export_dependencies(bundle_mock)
        with self.assertRaisesRegex(FileNotFoundError, 'aaa_aaa_aaa.json'):
            exporter.export(root=self.root, resume_after='aaa_aaa_aaa')
        bundle_mock.assert_not_called()

    def test_resume_checkpoint_must_be_in_current_registry(self):
        bundle_mock = unittest.mock.Mock()
        self._patch_export_dependencies(bundle_mock)
        with self.assertRaisesRegex(ValueError, '不在目前 registry'):
            exporter.export(root=self.root, resume_after='old_or_unknown')
        bundle_mock.assert_not_called()

    def test_selective_refresh_rebuilds_selected_bundle_and_reuses_others(self):
        destination = self.root / 'exports/persons'
        destination.mkdir(parents=True)
        old_selected = copy.deepcopy(self.old_bundle)
        old_selected['mention_count'] = 5
        selected_file = destination / 'aaa_aaa_aaa.json'
        selected_file.write_text(json.dumps(old_selected))
        reused_bundle = {
            'identity_policy': {'policy': 'source-backed'},
            'family_tree_decisions': [],
            'person_ids': ['bbb_bbb_bbb'],
            'mention_count': 23,
        }
        reused_file = destination / 'bbb_bbb_bbb.json'
        reused_file.write_text(json.dumps(reused_bundle))
        reused_bytes = reused_file.read_bytes()
        stale_file = destination / 'retired_person.json'
        stale_file.write_text('{}')
        refresh_file = self.root / 'refresh-ids.txt'
        refresh_file.write_text(json.dumps(['aaa_aaa_aaa']))
        refreshed_bundle = copy.deepcopy(old_selected)
        refreshed_bundle['mention_count'] = 99
        refreshed_bundle['family_tree_decisions'] = []
        bundle_mock = unittest.mock.Mock(side_effect=lambda pid, **kwargs: copy.deepcopy(refreshed_bundle))
        from scripts.personless_namespace import prune_person_files
        self._patch_export_dependencies(bundle_mock, prune_side_effect=prune_person_files)

        exporter.export(root=self.root, refresh_person_ids=refresh_file)

        self.assertEqual(json.loads(selected_file.read_text())['mention_count'], 99)
        self.assertEqual(reused_file.read_bytes(), reused_bytes)
        bundle_mock.assert_any_call(
            'aaa_aaa_aaa', root=self.root, include_provisional=True,
            catalog=(self.people, []),
        )
        self.assertFalse(any(call.args[0] == 'bbb_bbb_bbb' for call in bundle_mock.call_args_list))
        alias_bundle = json.loads((destination / 'legacy_aaa.json').read_text())
        self.assertEqual(alias_bundle['requested_person_id'], 'legacy_aaa')
        self.assertEqual(alias_bundle['mention_count'], 99)
        self.assertFalse(stale_file.exists())
        index = json.loads((destination / 'index.json').read_text())
        self.assertEqual([row['mention_count'] for row in index['persons']], [99, 23])
        self.assertTrue((destination / 'README.md').is_file())
        self.assertTrue((destination / 'unconnected.md').is_file())
        self.assertEqual(index['id_aliases'], {'legacy_aaa': 'aaa_aaa_aaa'})

    def test_selective_refresh_rejects_retired_ids_before_side_effects(self):
        refresh_file = self.root / 'refresh-ids.json'
        refresh_file.write_text(json.dumps(['retired_person_id']))
        bundle_mock = unittest.mock.Mock()
        self._patch_export_dependencies(bundle_mock)
        with self.assertRaisesRegex(ValueError, '無效或已退休'):
            exporter.export(root=self.root, refresh_person_ids=refresh_file)
        bundle_mock.assert_not_called()
        self.calendar_mock.assert_not_called()

    def test_refresh_id_file_accepts_one_id_per_line(self):
        refresh_file = self.root / 'refresh-ids.txt'
        refresh_file.write_text('aaa_aaa_aaa\nbbb_bbb_bbb\n')
        self.assertEqual(
            exporter._read_refresh_person_ids(refresh_file),
            {'aaa_aaa_aaa', 'bbb_bbb_bbb'},
        )

    def test_selective_refresh_fails_if_an_unselected_bundle_is_missing(self):
        destination = self.root / 'exports/persons'
        destination.mkdir(parents=True)
        (destination / 'aaa_aaa_aaa.json').write_text(json.dumps(self.old_bundle))
        refresh_file = self.root / 'refresh-ids.json'
        refresh_file.write_text(json.dumps(['aaa_aaa_aaa']))
        bundle_mock = unittest.mock.Mock(return_value=copy.deepcopy(self.old_bundle))
        self._patch_export_dependencies(bundle_mock)
        with self.assertRaisesRegex(FileNotFoundError, 'bbb_aaa_bbb|bbb_bbb_bbb'):
            exporter.export(root=self.root, refresh_person_ids=refresh_file)

    def test_selective_refresh_rebuilds_unselected_alias_when_assembly_projection_changes(self):
        destination = self.root / 'exports/persons'
        destination.mkdir(parents=True)
        for pid in self.people:
            (destination / (pid + '.json')).write_text(json.dumps(self.old_bundle))
        child = {
            'person_id': 'bbb_bbb_bbb',
            'parent_person_id': 'aaa_aaa_aaa',
            'parent_connection': {'assertion_id': 'a-parent-1'},
        }
        (destination / 'legacy_aaa.json').write_text(json.dumps({
            'requested_person_id': 'legacy_aaa',
            'assembled_identity': self.assembly,
            'assembled_children': [],
        }))
        (destination / 'index.json').write_text(json.dumps({
            'id_aliases': {'legacy_aaa': 'old_root_id'},
        }))
        refresh_file = self.root / 'refresh-ids.txt'
        refresh_file.write_text('bbb_bbb_bbb\n')
        output = copy.deepcopy(self.old_bundle)
        output['refreshed'] = True
        bundle_mock = unittest.mock.Mock(return_value=output)
        self._patch_export_dependencies(
            bundle_mock,
            assembly_data=({'aaa_aaa_aaa': self.assembly}, {'bbb_bbb_bbb': child}),
        )

        exporter.export(root=self.root, refresh_person_ids=refresh_file)

        bundle_mock.assert_any_call(
            'aaa_aaa_aaa', root=self.root, include_provisional=True,
            catalog=(self.people, []),
        )
        alias = json.loads((destination / 'legacy_aaa.json').read_text())
        self.assertTrue(alias['refreshed'])
        self.assertEqual(alias['assembled_children'], [child])

    def test_resume_and_selective_refresh_are_mutually_exclusive(self):
        refresh_file = self.root / 'refresh-ids.json'
        refresh_file.write_text(json.dumps(['aaa_aaa_aaa']))
        bundle_mock = unittest.mock.Mock()
        self._patch_export_dependencies(bundle_mock)
        with self.assertRaisesRegex(ValueError, '不可同時使用'):
            exporter.export(
                root=self.root,
                resume_after='aaa_aaa_aaa',
                refresh_person_ids=refresh_file,
            )
        bundle_mock.assert_not_called()
        self.calendar_mock.assert_not_called()


if __name__ == '__main__':
    unittest.main()
