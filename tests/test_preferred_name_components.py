import unittest,json,copy
from pathlib import Path
from scripts.preferred_name_components import reading_errors
ROOT=Path(__file__).resolve().parents[1]
class PreferredNameComponentTests(unittest.TestCase):
    def setUp(self):
        self.names=json.loads((ROOT/'data/corpus/profile-names.json').read_text())['records']
        self.chapters={r['id']:r for p in(ROOT/'corpus').glob('*/*.json')for r in[json.loads(p.read_text())]if r.get('record_type')=='marked_chapter'}
        self.reading=json.loads((ROOT/'corpus/jinshu/098-huanwen-preferred-name-components.json').read_text())['readings'][0]
    def errors(self,r=None):return reading_errors(self.reading if r is None else r,self.names,self.chapters)
    def test_actual_three_source_reading(self):self.assertEqual(self.errors(),[])
    def test_wrong_person(self):
        self.reading['person_id']='other';self.assertTrue(self.errors())
    def test_changed_record(self):
        self.reading['records'][0]['record']['quote']='false';self.assertTrue(self.errors())
    def test_wrong_anchor(self):
        self.reading['records'][0]['anchor']['start']+=1;self.assertTrue(self.errors())
    def test_omitted_third_known_source(self):
        self.reading['records'].pop();self.assertTrue(self.errors())
    def test_false_new_reading(self):
        self.reading['preferred_value']='文';self.assertTrue(self.errors())
    def test_new_third_name_not_consumed(self):
        n=copy.deepcopy(self.names[-1]);n.update(self.reading['records'][0]['record']);n['ming']='文';n['id']='new-source';self.names.append(n)
        self.assertEqual(self.errors(),[]);self.assertNotIn(n,[r['record']for r in self.reading['records']])
    def test_mixed_basis_must_be_real_same_person(self):
        self.reading['basis']['anchors'][0]['person_id']='other';self.assertTrue(self.errors())
