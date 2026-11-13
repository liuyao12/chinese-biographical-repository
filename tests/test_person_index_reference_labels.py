import tempfile
import unittest
from pathlib import Path

from scripts.export_person_bundles import write_reading_pages


class PersonIndexReferenceLabels(unittest.TestCase):
    def test_table_column_caption_has_its_source_definition(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_reading_pages(
                root, 'README.md', 'families', '# 人物', '',
                ['| 人物 | 來源 |\n|---|---|\n'
                 '| 甲 | [《漢書・功臣表》曲成列][2]、[《史記・列傳》][1] |'],
                ['[1]: https://example.invalid/shiji',
                 '[2]: https://example.invalid/hanshu',
                 '[3]: https://example.invalid/unused'],
            )
            text = (root / 'README.md').read_text()
            self.assertIn('[《漢書・功臣表》曲成列][2]', text)
            self.assertIn('[2]: https://example.invalid/hanshu', text)
            self.assertIn('[1]: https://example.invalid/shiji', text)
            self.assertNotIn('https://example.invalid/unused', text)

    def test_paginated_pages_keep_only_their_own_reference_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = write_reading_pages(
                root, 'README.md', 'families', '# 人物', '',
                ['x' * 150_000 + '\n[《史記・列傳》][1]',
                 'y' * 150_000 + '\n[《漢書・功臣表》曲成列][2]'],
                ['[1]: https://example.invalid/shiji',
                 '[2]: https://example.invalid/hanshu'],
            )
            self.assertEqual(names, ['README.md', 'families-002.md'])
            first, second = [(root / name).read_text() for name in names]
            self.assertTrue('[1]: https://example.invalid/shiji' in first,
                            'first page must define its source')
            self.assertFalse('[2]:' in first,
                             'first page must not include an unused source')
            self.assertTrue('[2]: https://example.invalid/hanshu' in second,
                            'second page must define the qualified table source')
            self.assertFalse('[1]:' in second,
                             'second page must not include an unused source')


if __name__ == '__main__':
    unittest.main()
