from copy import deepcopy
from pathlib import Path
import json
import unittest

from scripts.nanshi024_ruanwanling import errors, kin_valid, proposal_valid, side_errors

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


class RuanWanling(unittest.TestCase):
    def test_father_graph_and_orthography(self):
        chapter = read('corpus/jinshu/049-ruanyu-family.json')
        records = read('corpus/jinshu/049-ruanyu-family-assertions.json')['assertions']
        self.assertFalse(errors(chapter, ROOT))
        self.assertTrue(all(kin_valid(a, chapter, ROOT) for a in records))
        brother = deepcopy(records[-1])
        brother['predicate'] = 'father'
        self.assertFalse(kin_valid(brother, chapter, ROOT))
        changed = deepcopy(chapter)
        changed['paragraphs'][2]['text'] = changed['paragraphs'][2]['text'].replace('甯', '寧')
        self.assertTrue(errors(changed, ROOT))

    def test_declined_offices_and_death_age(self):
        chapter = read('corpus/songshu/093-ruanwanling.json')
        proposals = chapter['annotation']['title_proposals']
        self.assertEqual([p['title'] for p in proposals], ['祕書監', '給事中'])
        self.assertTrue(all(proposal_valid(p, chapter) for p in proposals))
        bad = deepcopy(proposals[0])
        bad['outcome'] = 'accepted'
        self.assertFalse(proposal_valid(bad, chapter))
        life = read('corpus/songshu/093-ruanwanling-life-events.json')
        self.assertFalse(side_errors(life, chapter, ROOT, 'events'))
        life['events'][0]['normalized_date']['year'] = 447
        self.assertTrue(side_errors(life, chapter, ROOT, 'events'))
