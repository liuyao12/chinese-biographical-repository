import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LianLinSecondPassTests(unittest.TestCase):
    def chapter(self, number):
        return json.loads((ROOT / f'corpus/shiji/{number}.json').read_text())

    def paragraph(self, number, suffix):
        return next(p for p in self.chapter(number)['paragraphs'] if p['id'].endswith(suffix))

    def test_succession_changes_king_without_merging_father_and_son(self):
        earlier = self.paragraph('081', ':p003')
        later = self.paragraph('081', ':p014')
        self.assertEqual({m['person_id'] for m in earlier['mentions'] if m['surface'] == '趙王'}, {'txj_z8z_5me_AB'})
        self.assertEqual({m['person_id'] for m in later['mentions'] if m['surface'] == '趙王'}, {'q6w_qm5_w2b'})
        names = {m['surface']: m['person_id'] for m in later['mentions']}
        self.assertEqual(names['趙括'], 'ja0_1pr_vhk')
        self.assertEqual(names['馬服君趙奢'], 'nrd_0cq_zyz')
        self.assertNotEqual(names['趙括'], names['馬服君趙奢'])

    def test_shared_campaign_preserves_different_received_outcomes(self):
        current = self.paragraph('081', ':p017')
        parallel = self.paragraph('080', ':p015')
        self.assertIn('殺栗腹', current['text'])
        self.assertIn('禽栗腹', parallel['text'])
        for p in (current, parallel):
            self.assertEqual({m['person_id'] for m in p['mentions'] if m['surface'] == '栗腹'}, {'fo2_the_x22'})
        battle = self.paragraph('081', ':p016')
        self.assertIn('四十餘日', battle['text'])
        self.assertEqual({m['person_id'] for m in battle['mentions'] if m['surface'] == '秦將白起'}, {'2bk_fz6_icl'})
        self.assertEqual({m['person_id'] for m in battle['mentions'] if m['surface'] in ('括', '趙括')}, {'ja0_1pr_vhk'})
