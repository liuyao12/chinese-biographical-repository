# -*- coding: utf-8 -*-
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from scripts.validate_corpus import validate
from scripts.person_bundle import bundle
ROOT=Path(__file__).resolve().parents[1]
class AgeDifferenceTests(unittest.TestCase):
    def test_both_people_receive_difference_without_birth_year(self):
        age=json.loads((ROOT/'corpus/shiji/067.json').read_text())['annotation']['age_difference_assertions'][0]
        self.assertEqual(age['value'],30)
        for pid in [age['person_id'],age['reference_person_id']]:
            result=bundle(pid)
            self.assertIn(age,result['age_difference_assertions'])
            self.assertIn(age['evidence'][0]['paragraph_id'],[p['id'] for p in result['passages']])
        self.assertIsNone(age['birth_year'])
    def mutate_errors(self,change):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for name in ('registry','corpus'):shutil.copytree(ROOT/name,root/name)
            path=root/'corpus/shiji/067.json';data=json.loads(path.read_text())
            change(data['annotation']['age_difference_assertions'][0])
            path.write_text(json.dumps(data,ensure_ascii=False))
            return validate(root)
    def test_wrong_number_rejected(self):
        self.assertIn('年齡差數值或方向不符',self.mutate_errors(lambda a:a.update(value=31)))
    def test_swapped_reference_anchor_rejected(self):
        self.assertIn('年齡差人物錨點不符',self.mutate_errors(lambda a:a['evidence'][0].update(reference_person_mention_id=a['evidence'][0]['person_mention_id'])))
    def test_inferred_birth_rejected(self):
        self.assertIn('年齡差不得推生年日期或計歲方式',self.mutate_errors(lambda a:a.update(birth_year=-520)))
    def test_missing_source_comparison_rejected(self):
        self.assertIn('年齡差原詞與參考人物不符',self.mutate_errors(lambda a:a.update(source_term='三十歳')))
