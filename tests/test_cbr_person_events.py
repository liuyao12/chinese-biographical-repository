# -*- coding: utf-8 -*-
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from scripts.validate_corpus import validate
from scripts.person_bundle import bundle
ROOT=Path(__file__).resolve().parents[1]
class PersonEventsTests(unittest.TestCase):
    def test_recruitment_bundle_keeps_date_separate_from_title(self):
        event=json.loads((ROOT/'corpus/shiji/121-person-events.json').read_text())['events'][0]
        result=bundle(event['person_id'])
        self.assertIn(event,result['person_events'])
        date=next(d for d in result['date_normalizations'] if d['record_id']==event['id'])
        self.assertEqual((date['date_role'],date['year']),('person_event',-133))
        holding=next(h for h in result['title_holdings'] if h['title']=='中大夫')
        self.assertEqual(holding['effective_period']['start']['status'],'unknown')
    def test_recruitment_rejects_wrong_person_and_bce_year(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for name in ('registry','corpus'):shutil.copytree(ROOT/name,root/name)
            path=root/'corpus/shiji/121-person-events.json';data=json.loads(path.read_text());e=data['events'][0]
            e['normalized_date']['year']=-134
            e['person_id']='g2z_cl6_w4r'
            path.write_text(json.dumps(data,ensure_ascii=False))
            errors=validate(root)
            self.assertIn('紀年換算天文年與時代年不一致',errors)
            self.assertIn('生卒事件人物錨點不符',errors)
