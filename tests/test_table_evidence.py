import json
import tempfile
import unittest
from pathlib import Path
from scripts.table_evidence import load_tables, table_evidence_errors

ROOT=Path(__file__).resolve().parents[1]

class TableKinshipEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables=load_tables(ROOT)
        cls.claim=json.loads((ROOT/'corpus/shiji/016-assertions.json').read_text())['assertions'][0]

    def errors(self, evidence, subject=None, parent=None):
        return table_evidence_errors(evidence,self.tables,subject or self.claim['subject_person_id'],parent or self.claim['object_person_id'])

    def test_actual_cell_and_person_anchors_support_claim(self):
        self.assertEqual(self.errors(self.claim['evidence'][0]),[])

    def test_wrong_source_or_prose_identity_is_rejected(self):
        for update in [{'source_revision':'synthetic_wrong_revision'}, {'source_id':'synthetic_wrong_source'},
                       {'paragraph_id':'synthetic_paragraph'}, {'kind':'paragraph'}]:
            e=dict(self.claim['evidence'][0],**update)
            self.assertIn('親屬表格證據來源或固定修訂不符',self.errors(e))

    def test_quote_must_be_whole_actual_cell(self):
        for quote in ['', '敖子', '合成錯誤引文']:
            self.assertIn('親屬表格引句須完整對應原格',self.errors(dict(self.claim['evidence'][0],quote=quote)))

    def test_cross_cell_anchor_or_other_parent_is_rejected(self):
        e=self.claim['evidence'][0]
        self.assertIn('親屬表格端點須有相符的逐人錨點',self.errors(dict(e,subject_mention_id='shiji-016-t2-r049-c04-m000')))
        self.assertIn('親屬表格端點須有相符的逐人錨點',self.errors(e,parent='synthetic_wrong_parent'))

    def test_table_index_cannot_read_outside_source_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'data/historical-tables';folder.mkdir(parents=True)
            (folder/'index.json').write_text(json.dumps({'tables':[{'id':'synthetic','path':'../../outside.json'}]}))
            with self.assertRaisesRegex(ValueError,'路徑與索引不符'):
                load_tables(root)
