"""結構匯入的來源及數值約束，不改史料。"""
import unittest
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
