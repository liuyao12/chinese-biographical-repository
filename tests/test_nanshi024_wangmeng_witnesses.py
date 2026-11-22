"""不同見證的王猛卒地、家人與身後贈號不得相互挪用。"""
from pathlib import Path
import unittest
import copy
import json

from scripts.nanshi024_wangmeng import death_valid, funeral_award, kin_valid


ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    return json.loads((ROOT / relative).read_text())


class WangMengReadings(unittest.TestCase):
    def test_witness_specific_deaths_and_awards(self):
        locations = {'nanshi/024-wangmeng': '卒于廣州', 'chenshu/014-wangyong': '行至荊州，道病卒'}
        for path, original in locations.items():
            stem = f'corpus/{path}'
            chapter = load(stem + '.json')
            events = {e['id']: e for e in load(stem + '-life-events.json')['events']}
            death, = [e for e in events.values() if e['person_id'] == '72e_1a7_3ac_AAAA']
            evidence, = death['evidence']
            self.assertIn(original, evidence['quote'])
            self.assertIsNone(death['date_expression'])
            self.assertTrue(death_valid(death, evidence, chapter, ROOT))
            self.assertFalse(death_valid(dict(death, date_expression='仁壽元年'), evidence, chapter, ROOT))
            for holding in load(stem + '-titles.json')['holdings']:
                if not holding['mode'].startswith('posthumous'):
                    continue
                self.assertTrue(funeral_award(holding, chapter, events, ROOT))
                wrong_son = dict(holding, person_id='72e_1a7_3ac_AAAAA')
                self.assertFalse(funeral_award(wrong_son, chapter, events, ROOT))
                self.assertFalse(funeral_award(holding, chapter, {}, ROOT))

    def test_deng_is_a_maternal_brother(self):
        stem = 'corpus/chenshu/014-wangyong'
        chapter = load(stem + '.json')
        sibling, = load(stem + '-assertions.json')['assertions']
        self.assertTrue(kin_valid(sibling, chapter, ROOT))
        self.assertTrue(sibling['qualifiers']['shared_mother'])
        self.assertNotIn('shared_father', sibling['qualifiers'])
        changed = copy.deepcopy(sibling)
        changed['qualifiers']['shared_father'] = True
        self.assertFalse(kin_valid(changed, chapter, ROOT))
