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

    def test_general_date_does_not_spread_to_other_grants(self):
        holdings = json.loads((ROOT / 'corpus/shiji/080-titles.json').read_text())['holdings']
        general = next(h for h in holdings if h['id'] == 'th-shiji080-003')
        date = general['effective_period']['start']['normalized_date']
        self.assertEqual(date['era_year'], 284)
        self.assertEqual(date['basis']['kind'], 'parallel_event')
        self.assertIn('二十八年', date['basis']['reference_event_quote'])
        for holding_id in ('th-shiji080-004', 'th-shiji080-005'):
            grant = next(h for h in holdings if h['id'] == holding_id)
            self.assertNotIn('normalized_date', grant['effective_period']['start'])

    def test_cao_title_resolves_by_teacher_context(self):
        chapter = json.loads((ROOT / 'corpus/shiji/080.json').read_text())
        p20 = next(p for p in chapter['paragraphs'] if p['id'].endswith(':p020'))
        names = {m['surface']:m['person_id'] for m in p20['mentions']}
        self.assertEqual(names['曹相國'], '37j_16p_7n8')
        self.assertEqual(names['蓋公'], 'g9g_mv1_6zj')
        self.assertIn('河上丈人', p20['text'])
        self.assertNotEqual(names['河上丈人'], names['蓋公'])
