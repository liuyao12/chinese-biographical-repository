import copy
import json
import unittest
from pathlib import Path
from scripts import jin096_huifeng, liang021_print_columns

ROOT = Path(__file__).resolve().parents[1]
def get(rel):
    return json.loads((ROOT / rel).read_text())

class HuifengReadings(unittest.TestCase):
    def test_print_layout_and_false_leaf(self):
        chapter=get('corpus/jinshu/096-wanghuifeng-wyd.json')
        self.assertEqual(liang021_print_columns.errors(chapter,ROOT),[])
        wrong=copy.deepcopy(chapter)
        wrong['paragraphs'][0]['source_position']['column_projection'][0]['leaf']='六上'
        self.assertTrue(liang021_print_columns.errors(wrong,ROOT))

    def test_petition_preserves_father_and_married_daughter(self):
        for suffix in ('','-wyd'):
            name='corpus/jinshu/096-wanghuifeng'+suffix
            c=get(name+'.json'); p=c['paragraphs'][0]
            a=next(x for x in get(name+'-assertions.json')['assertions'] if x['predicate']=='spouse')
            lookup={p['id']:(c['id'],p)}
            self.assertTrue(jin096_huifeng.petition_valid(a,lookup))
            false=copy.deepcopy(a)
            false['qualifiers']['dissolution_petition']['formal_decision_reported']=True
            self.assertFalse(jin096_huifeng.petition_valid(false,lookup))
            false=copy.deepcopy(a)
            false['qualifiers']['dissolution_petition']['petitioner_person_id']=a['object_person_id']
            self.assertFalse(jin096_huifeng.petition_valid(false,lookup))

    def test_elder_is_her_own_person(self):
        c=get('corpus/jinshu/053-jin096-huifeng.json')
        a=next(x for x in get('corpus/jinshu/053-jin096-huifeng-assertions.json')['assertions']
               if x['id']=='a-jin053-huifeng-elder-father')
        self.assertTrue(jin096_huifeng.elder_valid(a,a['evidence'][0],c))
        swapped=copy.deepcopy(a);swapped['subject_person_id']='y5y_cch_05n'
        self.assertFalse(jin096_huifeng.elder_valid(swapped,swapped['evidence'][0],c))
