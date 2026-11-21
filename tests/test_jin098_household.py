import copy
import json
from pathlib import Path
import unittest
from scripts.jin098_household import adoption_valid

ROOT = Path(__file__).resolve().parents[1]
def get(f):
    return json.loads((ROOT/f).read_text())
class WangDunAdoption(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = 'corpus/jinshu/098-jin033-wangji'
        chapter = get(root+'.json')
        cls.paras = {p['id']:(chapter['id'],p) for p in chapter['paragraphs']}
        cls.rows = get(root+'-assertions.json')['assertions']
        cls.adoption = next(v for v in cls.rows if v['id']=='a-w098-family-ying-adoption')
        cls.birth = next(v for v in cls.rows if v['id']==cls.adoption['qualifiers']['birth_parent_assertion_id'])
    def test_three_named_people_and_two_source_relations(self):
        self.assertTrue(adoption_valid(self.adoption,self.paras,self.rows))
        self.assertEqual(self.adoption['subject_person_id'],self.birth['subject_person_id'])
        self.assertNotEqual(self.adoption['object_person_id'],self.birth['object_person_id'])
    def test_another_biological_father_or_unbound_character_rejected(self):
        for key,value in [('object_person_id',self.birth['object_person_id']),('subject_person_id',self.adoption['object_person_id'])]:
            bad=copy.deepcopy(self.adoption);bad[key]=value
            self.assertFalse(adoption_valid(bad,self.paras,self.rows))
        for key,value in [('source_term','養含子應'),('birth_parent_assertion_id','a-w098-family-yu-birth')]:
            bad=copy.deepcopy(self.adoption);bad['qualifiers'][key]=value
            self.assertFalse(adoption_valid(bad,self.paras,self.rows))
