# coding: utf-8
import copy
import json
import unittest
from pathlib import Path
from scripts.unassumed_appointments import unassumed_appointment_valid
ROOT = Path(__file__).resolve().parents[1]
class ChuPouDeclinedAppointments(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT / 'corpus/jinshu/093-chupou.json').read_text())
        self.p = next(x for x in self.c['annotation']['title_proposals'] if x['title'] == '開府儀同三司')
    def test_refused_kaifu_keeps_parallel_military_appointment(self):
        self.assertTrue(unassumed_appointment_valid(self.p, self.c))
        hs = json.loads((ROOT / 'corpus/jinshu/093-chupou-titles.json').read_text())['holdings']
        self.assertTrue(any(h['title'] == '征北大將軍' and h['mode'] == 'grant' for h in hs))
        self.assertFalse(any(h['title'] == '開府儀同三司' for h in hs))
    def test_refusal_does_not_apply_to_parallel_title(self):
        a = copy.deepcopy(self.p);p = next(p for p in self.c['paragraphs'] if p['id'] == a['role_anchor']['paragraph_id'])
        title = '征北大將軍';i = p['text'].index(title)
        a['title'] = title;a['role_anchor'].update(start=i,end=i+len(title),surface=title)
        self.assertFalse(unassumed_appointment_valid(a, self.c))
