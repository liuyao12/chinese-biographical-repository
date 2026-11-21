"""王悅的宋書年序須繫原段重提的本人與宋太宗。"""
import copy
import json
from pathlib import Path
import unittest

from scripts.era_stage_dates import binding_valid
from scripts.validate_corpus import normalized_date_errors

ROOT = Path(__file__).resolve().parents[1]

class WangYueDeathYear(unittest.TestCase):
    def setUp(self):
        chapter = json.loads((ROOT / 'corpus/songshu/092-wangyue.json').read_text())
        self.chapters = {chapter['id']: chapter}
        self.event, = json.loads((ROOT / 'corpus/songshu/092-wangyue-life-events.json').read_text())['events']

    def test_regnal_year_and_subject(self):
        date = self.event['normalized_date']
        self.assertEqual(self.event['date_expression'], '五年')
        self.assertEqual(date['year'], 469)
        self.assertFalse(normalized_date_errors(date, self.chapters, ROOT, self.event, 'life_event'))
        self.assertTrue(binding_valid(date, self.event, 'life_event'))
        for field, wrong in [('era_anchor', '五年'), ('event_date_anchor', '泰始中')]:
            changed = copy.deepcopy(date)
            changed['narrative_era_scope'][field]['surface'] = wrong
            self.assertTrue(normalized_date_errors(changed, self.chapters, ROOT, self.event, 'life_event'))
        changed = copy.deepcopy(date)
        changed['narrative_era_scope']['unit_subject_mention_id'] = 'c-songshu-092-wangyue:p001:m0033'
        self.assertTrue(normalized_date_errors(changed, self.chapters, ROOT, self.event, 'life_event'))
        self.assertFalse(binding_valid(date, dict(self.event, person_id='326_faf_cd3_*A'), 'life_event'))
        wrong_polity = copy.deepcopy(date)
        wrong_polity['references'][0]['columns']['dynasty'] = '晉'
        self.assertTrue(normalized_date_errors(wrong_polity, self.chapters, ROOT, self.event, 'life_event'))
