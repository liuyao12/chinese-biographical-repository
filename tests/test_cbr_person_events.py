# -*- coding: utf-8 -*-
from tests.portable_fixture_copy import fixture_copy2
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from scripts.validate_corpus import validate
from scripts.person_bundle import bundle
ROOT=Path(__file__).resolve().parents[1]
def copy_source_fixture(root):
    """Use the real received-source closure before mutating an event."""
    for name in ('registry','corpus','source-evidence','sources','scripts','docs','schema','data/historical-tables'):
        (root/name).parent.mkdir(parents=True,exist_ok=True)
        shutil.copytree(ROOT/name,root/name, copy_function=fixture_copy2)
    (root/'data/corpus').mkdir(parents=True,exist_ok=True)
    for name in ('profile-names.json','chapter-directory.json'):
        shutil.copy2(ROOT/'data/corpus'/name,root/'data/corpus'/name)
    # Preserve the declared immutable capture required by the Pei source proof.
    capture='tests/fixtures/occurrence-concordance/original-anchors.json'
    (root/capture).parent.mkdir(parents=True,exist_ok=True)
    fixture_copy2(ROOT/capture,root/capture)
class PersonEventsTests(unittest.TestCase):
    def test_unmodified_source_fixture_has_no_errors(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            copy_source_fixture(root)
            self.assertEqual(validate(root),[])

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
            copy_source_fixture(root)
            path=root/'corpus/shiji/121-person-events.json';data=json.loads(path.read_text());e=data['events'][0]
            e['normalized_date']['year']=-134
            e['person_id']='fmh_dmt_cql'
            path.write_text(json.dumps(data,ensure_ascii=False))
            errors=validate(root)
            self.assertIn('紀年換算天文年與時代年不一致',errors)
            self.assertIn('生卒事件人物錨點不符',errors)

    def test_burial_bundle_preserves_unknown_date(self):
        event=json.loads((ROOT/'corpus/shiji/065-person-events.json').read_text())['events'][0]
        result=bundle(event['person_id'])
        self.assertIn(event,result['person_events'])
        self.assertEqual(event['source_term'],'悼王既葬')
        self.assertIsNone(event['date_expression'])
        self.assertNotIn('normalized_date',event)
        self.assertTrue(any(e['event_type']=='death' for e in result['life_events']))
    def test_burial_requires_actual_source_term(self):
        for term in ('悼王死','未見於原文的葬詞'):
            with self.subTest(term=term), tempfile.TemporaryDirectory() as temp:
                root=Path(temp)
                copy_source_fixture(root)
                path=root/'corpus/shiji/065-person-events.json';data=json.loads(path.read_text())
                data['events'][0]['source_term']=term
                path.write_text(json.dumps(data,ensure_ascii=False))
                self.assertIn('埋葬事件須有原文明示葬詞及相符引句',validate(root))
    def test_burial_rejects_other_person_anchor(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            copy_source_fixture(root)
            path=root/'corpus/shiji/065-person-events.json';data=json.loads(path.read_text())
            data['events'][0]['evidence'][0]['person_mention_id']='c-shiji-065-sun:m013-0124'
            path.write_text(json.dumps(data,ensure_ascii=False))
            self.assertIn('生卒事件人物錨點不符',validate(root))
