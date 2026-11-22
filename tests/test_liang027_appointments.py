import json
from copy import deepcopy
from pathlib import Path
import unittest

from scripts.unassumed_appointments import unassumed_appointment_valid


class LiangAppointments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = {}
        directory = Path(__file__).resolve().parents[1] / 'corpus' / 'liangshu'
        for name in ('daoqia', 'mingshanbin', 'yinjun'):
            cls.chapters[name] = json.loads((directory / f'027-{name}-complete.json').read_text())

    def proposal(self, name, title):
        chapter = self.chapters[name]
        row, = (r for r in chapter['annotation']['title_proposals'] if r['title'] == title)
        return chapter, deepcopy(row)

    def test_each_declined_title_and_its_source_clause(self):
        for name, titles in [('daoqia', ['晉安王國左常侍','太子中庶子','步兵校尉']),
                             ('mingshanbin', ['國子博士']), ('yinjun', ['五兵尚書'])]:
            for title in titles:
                with self.subTest(name=name, title=title):
                    chapter, row = self.proposal(name, title)
                    self.assertTrue(unassumed_appointment_valid(row, chapter))

    def test_same_title_in_an_earlier_year(self):
        chapter, row = self.proposal('daoqia', '太子中庶子')
        p = chapter['paragraphs'][3]
        start = p['text'].index('行太子中庶子') + 1
        row['role_anchor'].update(start=start, end=start + len(row['title']))
        self.assertFalse(unassumed_appointment_valid(row, chapter))

    def test_house_construction_cannot_supply_refusal(self):
        chapter, row = self.proposal('mingshanbin', '國子博士')
        p = chapter['paragraphs'][2]
        start = p['text'].index('築室不就') + 2
        row['non_assumption_anchor'].update(paragraph_id=p['id'], start=start, end=start+2)
        self.assertFalse(unassumed_appointment_valid(row, chapter))

    def test_fathers_refusal_cannot_be_transferred_to_son(self):
        chapter, row = self.proposal('mingshanbin', '國子博士')
        subject, = (m for m in chapter['paragraphs'][0]['mentions'] if m['surface'] == '明山賓')
        row.update(person_id=subject['person_id'], person_mention_id=subject['id'])
        row['evidence'][0]['person_mention_id'] = subject['id']
        self.assertFalse(unassumed_appointment_valid(row, chapter))

    def test_acceptance_after_illness(self):
        chapter, row = self.proposal('yinjun', '五兵尚書')
        title = '散騎常侍'
        p = chapter['paragraphs'][2]
        start = p['text'].index('乃更授'+title) + 3
        row.update(title=title)
        row['role_anchor'].update(surface=title, start=start, end=start+len(title))
        self.assertFalse(unassumed_appointment_valid(row, chapter))

    def test_substituted_source_even_when_evidence_agrees(self):
        chapter, row = self.proposal('daoqia', '晉安王國左常侍')
        changed = deepcopy(chapter)
        changed['source_id'] = row['evidence'][0]['source_id'] = 's-liangshu-other-copy'
        self.assertFalse(unassumed_appointment_valid(row, changed))
