"""結構匯入的來源及數值約束，不改史料。"""
import unittest
import tempfile
from pathlib import Path
from scripts import historical_tables


class HistoricalTablesTests(unittest.TestCase):
    def test_public_table_data_validates(self):
        historical_tables.validate()

    def test_parser_preserves_merged_cells_and_line_breaks(self):
        parser = historical_tables.TableParser()
        parser.feed('<table class="wikitable"><tr><td>甲<br>乙</td><td colspan="2">丙</td></tr></table>')
        cells = parser.tables[0]['rows'][0]
        self.assertEqual(cells[0]['text'], '甲\n乙')
        self.assertEqual(cells[1]['attrs']['colspan'], '2')

    def test_general_import_does_not_invent_years_or_merge_unlike_sections(self):
        raw = '<a href="?oldid=123">revision</a><table class="wikitable"><tr><th>generation</th><th>lineage</th></tr><tr><td>ancestor</td><td colspan="2">descendants</td></tr></table><table class="wikitable"><tr><td>continuation</td></tr></table>'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'synthetic.html'
            path.write_text(raw)
            table = historical_tables.import_general_table(path, '013', 'synthetic table')
        self.assertEqual(len(table['fragments']), 2)
        first, second = table['fragments']
        self.assertIsNone(first['rows'][0]['year'])
        self.assertEqual(first['rows'][0]['cells'][1]['colspan'], 2)
        self.assertEqual(second['rows'][0]['cells'][0]['text'], 'continuation')
        self.assertTrue(table['independent_sections'])
        self.assertNotEqual(first['source_header'], second['source_header'])
