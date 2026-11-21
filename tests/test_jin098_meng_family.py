import copy
import json
from pathlib import Path
import unittest
from scripts.tao_meng_family import kin_valid,context_valid

root=Path(__file__).resolve().parents[1]
read=lambda f:json.loads((root/f).read_text())
class MengHousehold(unittest.TestCase):
    def test_two_daughters_fixed_source_and_different_fathers(self):
        base='corpus/taoyuanmingji/006-jin098-mengjia'
        ch=read(base+'.json');all=read(base+'-assertions.json')['assertions']
        rows=[a for a in all if a['qualifiers'].get('reading_basis')]
        self.assertEqual(len(rows),4)
        for a in rows:self.assertTrue(kin_valid(a,a['evidence'][0],ch,root))
        women=[a for a in rows if a['predicate']=='father']
        self.assertEqual(len({a['subject_person_id']for a in women}),2)
        self.assertEqual(len({a['object_person_id']for a in women}),2)
        a=copy.deepcopy(women[0]);a['object_person_id']=women[1]['object_person_id'];self.assertFalse(kin_valid(a,a['evidence'][0],ch,root))
    def test_two_reported_ages_and_authorial_reference(self):
        t=read('corpus/taoyuanmingji/006-jin098-mengjia.json');j=read('corpus/jinshu/098-mengjia.json')
        aa=t['annotation']['age_assertions'][0];bb=j['annotation']['age_assertions'][0];self.assertEqual((aa['value'],bb['value']),(51,53));self.assertEqual(aa['person_id'],bb['person_id']);self.assertIsNone(aa['birth_year']);self.assertIsNone(bb['birth_year'])
        e=aa['evidence'][0];self.assertTrue(context_valid(e['context'],e,aa['person_id'],t))
        bad=copy.deepcopy(e['context']);bad['person_reference_id']+='X';self.assertFalse(context_valid(bad,e,aa['person_id'],t))
