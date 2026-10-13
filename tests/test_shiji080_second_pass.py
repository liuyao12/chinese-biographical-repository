import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LeYiSecondPassTests(unittest.TestCase):
    def test_reply_separates_two_wu_kings(self):
        chapter = json.loads((ROOT / 'corpus/shiji/080.json').read_text())
        paragraph = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p011'))
        kings = [m['person_id'] for m in paragraph['mentions'] if m['surface'] == '吳王']
        self.assertEqual(kings, ['5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAA',
                                 '5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA'])
        self.assertIn('夫差弗是也', paragraph['text'])

    def test_fuchai_succession_and_campaign_share_one_person(self):
        chapters = {n: json.loads((ROOT / f'corpus/shiji/{n}.json').read_text())
                    for n in ('031', '066')}
        candidates = []
        for no, suffix in (('031', ':p029'), ('066', ':p014')):
            p = next(p for p in chapters[no]['paragraphs'] if p['id'].endswith(suffix))
            candidates.append(next(m['person_id'] for m in p['mentions']
                                   if m['surface'] == '太子夫差'))
            self.assertIn('取番', p['text'])
        self.assertEqual(candidates, ['5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAA'] * 2)
        people = json.loads((ROOT / 'registry/persons.json').read_text())['persons']
        self.assertNotIn('5dm_e40_rqh_AAAAAAAAAAAAAAAAAAAAB', {p['id'] for p in people})

    def test_letters_keep_speaker_and_former_king_separate(self):
        chapter = json.loads((ROOT / 'corpus/shiji/080.json').read_text())
        letter = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p006'))
        reply = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p007'))
        self.assertEqual({m['person_id'] for m in letter['mentions'] if m['surface'] == '寡人'},
                         {'5pw_05i_uhv_A'})
        self.assertEqual({m['person_id'] for m in reply['mentions'] if m['surface'] == '臣'},
                         {'gz0_xuu_ont'})
        self.assertEqual({m['person_id'] for m in reply['mentions'] if m['surface'] == '先王'},
                         {'5pw_05i_uhv'})
